#!/usr/bin/env python3
"""Build the scene-by-scene storyboard the user approves BEFORE the final video is rendered.

Input: storyboard.json (fill assets/storyboard-template.json). Output: storyboard.html (one self-contained
page, frames embedded, opens in any browser) + storyboard.md (same content as text).

Usage:
  python3 storyboard.py work/storyboard.json --out renders/storyboard [--words work/words_cut.json]
                        [--duration 42.5]
Checks before writing (errors stop the build, they are not warnings):
  - scenes are numbered 1..N in order and their time ranges are contiguous with no gaps or overlaps
  - the last scene ends at the video duration (--duration, or the last word in --words)
  - every VO line is verbatim from the transcript (--words): no paraphrase, no invented lines
  - every scene has a beat label, a style tag, a visual and MOVES; at least two style options exist
"""
import argparse
import base64
import html
import json
import os
import re
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, read_json  # noqa: E402


def tc(t):
    m, s = divmod(int(round(float(t))), 60)
    return f"{m}:{s:02d}"


def norm(t):
    return " ".join(re.sub(r"[^\w\s']+", " ", t.lower()).split())


def validate(sb, words, duration):
    errs = []
    scenes = sb.get("scenes") or []
    if not scenes:
        errs.append("no scenes")
    if len(sb.get("options") or []) < 2:
        errs.append("give at least two style options (Option A / Option B) so the user chooses a direction")
    spoken = norm(" ".join(w["text"] for w in words)) if words else None
    prev_end = 0.0
    for i, s in enumerate(scenes, 1):
        tag = f"scene {i}"
        if int(s.get("n", i)) != i:
            errs.append(f"{tag}: numbered {s.get('n')}, expected {i}")
        a, b = float(s["start"]), float(s["end"])
        if abs(a - prev_end) > 0.05:
            errs.append(f"{tag}: starts at {a:.2f}s but the previous scene ends at {prev_end:.2f}s (gap/overlap)")
        if b <= a:
            errs.append(f"{tag}: end {b} is not after start {a}")
        prev_end = b
        for field in ("beat", "tag", "visual", "moves"):
            if not str(s.get(field, "")).strip():
                errs.append(f"{tag}: missing '{field}'")
        vo = str(s.get("vo", "")).strip()
        if vo and spoken is not None and norm(vo) not in spoken:
            errs.append(f"{tag}: VO line is not verbatim from the transcript: \"{vo}\"")
        if s.get("image") and not os.path.exists(s["image"]):
            errs.append(f"{tag}: image not found: {s['image']}")
    if duration and scenes and abs(prev_end - duration) > 0.3:
        errs.append(f"last scene ends at {prev_end:.2f}s but the video is {duration:.2f}s long")
    return errs


def img_tag(path):
    if not path:
        return ""
    ext = os.path.splitext(path)[1].lower().lstrip(".") or "png"
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/{mime};base64,{data}" alt="">'


CSS = """
:root{--bg:#0f0f0e;--card:#1a1a18;--ink:#f1eee6;--mute:#9c988e;--line:#2c2b28;--accent:#ddf53d;--accent-ink:#141414}
@media (prefers-color-scheme: light){:root{--bg:#f4f2ec;--card:#ffffff;--ink:#141412;--mute:#6b675e;--line:#e2ded4;--accent:#c9e21f;--accent-ink:#141414}}
*{box-sizing:border-box;min-width:0}p,h1{overflow-wrap:anywhere}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 Inter,system-ui,-apple-system,sans-serif}
main{max-width:1080px;margin:0 auto;padding:40px 16px 80px}
h1{font:600 clamp(28px,5vw,44px)/1.1 "Instrument Serif",Georgia,serif;margin:0 0 12px;letter-spacing:-.01em}
.intro{color:var(--mute);max-width:720px;margin:0 0 20px}
.opts{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:36px}
.opt{border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-size:13px}
.opt b{margin-right:6px}.opt.sel{background:var(--accent);color:var(--accent-ink);border-color:transparent}
.scene{display:grid;grid-template-columns:72px minmax(0,1fr);gap:20px;background:var(--card);border:1px solid var(--line);
border-radius:14px;padding:22px;margin-bottom:16px}
.num{font:600 56px/1 "Instrument Serif",Georgia,serif}
.meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:12px;font-size:13px;color:var(--mute)}
.pill{background:var(--accent);color:var(--accent-ink);border-radius:999px;padding:3px 10px;font-weight:600}
.grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:20px}
.frame img{width:100%;border-radius:8px;display:block;border:1px solid var(--line)}
.frame p{margin:8px 0 0;color:var(--mute);font-size:13px}
.vo{font:italic 19px/1.4 "Instrument Serif",Georgia,serif;margin:0 0 12px}
.lab{font:600 11px/1 "JetBrains Mono",ui-monospace,monospace;letter-spacing:.08em;color:var(--mute);margin-bottom:4px}
@media (max-width:720px){.scene{grid-template-columns:minmax(0,1fr)}.grid{grid-template-columns:1fr}.num{font-size:40px}}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--out", required=True, help="output path without extension")
    ap.add_argument("--words", help="words_cut.json, to check every VO line is verbatim")
    ap.add_argument("--duration", type=float)
    args = ap.parse_args()
    sb = read_json(args.storyboard)
    words = read_json(args.words) if args.words else None
    duration = args.duration or (words[-1]["end"] if words else None)
    errs = validate(sb, words, duration)
    if errs:
        die("storyboard not ready:\n  - " + "\n  - ".join(errs))

    scenes, opts = sb["scenes"], sb["options"]
    title = sb.get("title") or f"{len(scenes)} frames, {len(opts)} looks"
    e = html.escape
    parts = [f"<!doctype html><html lang=en><head><meta charset=utf-8>"
             f"<meta name=viewport content='width=device-width,initial-scale=1'><title>{e(title)}</title>"
             f"<style>{CSS}</style></head><body><main><h1>{e(title)}</h1>"
             f"<p class=intro>{e(sb.get('intro', ''))}</p><div class=opts>"]
    for o in opts:
        parts.append(f"<div class='opt{' sel' if o.get('selected') else ''}'><b>{e(o['name'])}</b>"
                     f"{e(o.get('note', ''))}</div>")
    parts.append("</div>")
    md = [f"# {title}", "", sb.get("intro", ""), "", "**Style options:** " +
          " | ".join(f"{'[selected] ' if o.get('selected') else ''}{o['name']}: {o.get('note', '')}" for o in opts), ""]
    for s in scenes:
        rng = f"{tc(s['start'])} - {tc(s['end'])}"
        vo = s.get("vo", "").strip()
        parts.append(
            f"<section class=scene><div class=num>{s.get('n')}</div><div>"
            f"<div class=meta><span>{rng}</span><span>&middot; {e(s['beat'])}</span>"
            f"<span class=pill>{e(s['tag'])}</span></div><div class=grid>"
            f"<div class=frame>{img_tag(s.get('image'))}<p>{e(s['visual'])}</p></div><div>"
            + (f"<div class=lab>VO</div><p class=vo>&ldquo;{e(vo)}&rdquo;</p>" if vo else
               "<div class=lab>VO</div><p class=vo>(no voice)</p>")
            + f"<div class=lab>MOVES</div><p>{e(s['moves'])}</p></div></div></div></section>")
        md += [f"## Scene {s.get('n')} . {rng} . {s['beat']}  [{s['tag']}]", "",
               f"**Visual:** {s['visual']}", "", f"**VO:** \"{vo}\"" if vo else "**VO:** (no voice)", "",
               f"**MOVES:** {s['moves']}", ""]
    parts.append("</main></body></html>")
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out + ".html", "w", encoding="utf-8") as f:
        f.write("".join(parts))
    with open(args.out + ".md", "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"Storyboard OK ({len(scenes)} scenes, {tc(scenes[-1]['end'])}). Wrote {args.out}.html and .md. "
          "Show it to the user and get approval before building the final video.")


if __name__ == "__main__":
    main()
