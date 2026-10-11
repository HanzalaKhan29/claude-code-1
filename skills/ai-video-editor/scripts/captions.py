#!/usr/bin/env python3
"""Word-timed caption files (ASS for burn-in, SRT for platform upload) in named styles.

Usage:
  python3 captions.py <words_cut.json> --video v1.mp4 --style 6 [--keywords keywords.json]
                      [--y 0.70] [--burn out.mp4] [--fonts work/fonts] [--max-words 3]
  python3 captions.py --list                       # show the style catalog
keywords.json: ["profit", "3x", ...]  or  [{"text": "profit", "start": 12.3}, ...] (edited-timeline times).
The agent chooses keywords BY MEANING (max one per caption group). No keywords file = no highlight.

Styles (fontsize is % of frame height; body captions sit around 4-5% so they read on a phone):
  1 clean-caps     ALL CAPS rounded heavy sans, white, soft shadow, 2-4 words, pop-in
  2 lower-serif    lowercase bold sans; key word in light italic serif; no box
  3 pill           white box, dark spoken words, grey upcoming words, low on frame
  4 serif-italic   small lowercase italic serif, soft shadow; the newest word turns heavy
  5 editorial      bold sans; ONE key word as big italic serif in a single accent (lime)
  6 viral          UPPERCASE Montserrat Black, thick outline, active word yellow, 1-3 words, pops
  7 documentary    small white bold UPPERCASE sans, one line, no colour, no pop
  8 karaoke        bold sans, words light up as spoken (active = accent), 3-5 words
  9 hindi          Devanagari-safe bold sans (Noto Sans Devanagari / Hind), white + outline
 10 minimal        sentence case medium sans, 1-2 lines, soft scrim-free shadow (long-form YouTube)
Any field can be overridden with --style-json card.json (e.g. the creator's measured style card).
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, probe, read_json  # noqa: E402

BASE = {
    "font": "Inter", "weight": 800, "italic": False, "size_pct": 4.6, "case": "asis",
    "primary": "#FFFFFF", "upcoming": None, "active": None, "outline_pct": 0.0, "outline": "#000000",
    "shadow_pct": 0.25, "shadow": "#000000", "shadow_alpha": 0.55, "box": False, "box_color": "#FFFFFF",
    "box_pad_pct": 0.9, "max_words": 4, "max_chars_line": 22, "lines": 1, "anim": "fade", "tracking": 0.0,
    "key_font": None, "key_italic": False, "key_weight": None, "key_color": None, "key_size_mul": 1.0,
    "active_bold": False, "drop_punct": True, "fonts": ["Inter:800"],
}

STYLES = {
    "clean-caps": dict(font="Nunito", weight=900, case="upper", size_pct=4.8, shadow_pct=0.35, max_words=4,
                       anim="pop", tracking=0.5, fonts=["Nunito:900"]),
    "lower-serif": dict(font="Inter", weight=800, case="lower", size_pct=4.6, max_words=4, anim="fade",
                        tracking=-0.5, key_font="Instrument Serif", key_italic=True, key_weight=400,
                        key_size_mul=1.15, fonts=["Inter:800", "Instrument Serif:i400"]),
    "pill": dict(font="Inter", weight=700, case="lower", size_pct=3.6, primary="#141414", upcoming="#9A9A9A",
                 box=True, box_color="#FFFFFF", shadow_pct=0.0, max_words=5, max_chars_line=26, anim="none",
                 fonts=["Inter:700"]),
    "serif-italic": dict(font="Playfair Display", weight=400, italic=True, case="lower", size_pct=4.2,
                         shadow_pct=0.3, max_words=5, anim="fade", active_bold=True,
                         fonts=["Playfair Display:i400,i800"]),
    "editorial": dict(font="Inter", weight=800, case="asis", size_pct=4.4, max_words=4, anim="fade", tracking=-0.6,
                      key_font="Instrument Serif", key_italic=True, key_weight=400, key_color="#C6FF3D",
                      key_size_mul=1.6, fonts=["Inter:800", "Instrument Serif:i400"]),
    "viral": dict(font="Montserrat", weight=900, case="upper", size_pct=5.6, outline_pct=0.55, shadow_pct=0.3,
                  active="#FFE600", max_words=3, max_chars_line=16, anim="pop", fonts=["Montserrat:900"]),
    "documentary": dict(font="Inter", weight=700, case="upper", size_pct=3.0, shadow_pct=0.2, max_words=7,
                        max_chars_line=34, anim="none", tracking=1.5, fonts=["Inter:700"]),
    "karaoke": dict(font="Inter", weight=800, case="asis", size_pct=4.6, outline_pct=0.3, upcoming="#FFFFFF",
                    active="#FFD400", max_words=5, max_chars_line=22, anim="fade", fonts=["Inter:800"]),
    "hindi": dict(font="Noto Sans Devanagari", weight=700, case="asis", size_pct=4.8, outline_pct=0.4,
                  max_words=4, max_chars_line=20, anim="fade", fonts=["Noto Sans Devanagari:700"]),
    "minimal": dict(font="Inter", weight=600, case="asis", size_pct=3.6, shadow_pct=0.3, max_words=9,
                    max_chars_line=38, lines=2, anim="fade", drop_punct=False, fonts=["Inter:600"]),
}
IDS = {str(i + 1): k for i, k in enumerate(STYLES)}


def resolve_style(s):
    s = str(s).strip().lower()
    if s in IDS:
        return IDS[s]
    if s in STYLES:
        return s
    die(f"unknown style '{s}'. Use --list.")


def ass_color(hex_color, alpha=0.0):
    h = hex_color.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    a = int(round(alpha * 255))
    return f"&H{a:02X}{b}{g}{r}".upper()


def esc(t):
    return t.replace("\\", "\\\\").replace("{", "(").replace("}", ")")


def clean_word(t, cfg):
    t = t.strip()
    if cfg["drop_punct"]:
        t = re.sub(r"[,.;:]+$", "", t)
        t = t.replace("\u2014", "").replace("\u2013", "")
    if cfg["case"] == "upper":
        t = t.upper()
    elif cfg["case"] == "lower":
        t = t.lower()
    return t


def group_words(words, cfg):
    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        chars = sum(len(x["text"]) + 1 for x in cur)
        brk = (nxt is None or nxt["start"] - w["end"] >= 0.25 or w["text"].rstrip().endswith((".", "?", "!", "।"))
               or len(cur) >= cfg["max_words"] or chars >= cfg["max_chars_line"] * cfg["lines"]
               or (w["text"].rstrip().endswith(",") and nxt and nxt["start"] - w["end"] >= 0.15))
        if brk:
            groups.append(cur)
            cur = []
    # merge groups shorter than 0.5s into a neighbour when it stays within limits
    merged = []
    for g in groups:
        if merged and (g[-1]["end"] - g[0]["start"] < 0.5) and len(merged[-1]) + len(g) <= cfg["max_words"] + 1 \
                and g[0]["start"] - merged[-1][-1]["end"] < 0.25:
            merged[-1].extend(g)
        else:
            merged.append(g)
    return merged


def load_keywords(path, words):
    if not path:
        return set()
    data = read_json(path)
    keys = set()
    for k in data:
        if isinstance(k, dict):
            t = float(k.get("start", -1))
            for i, w in enumerate(words):
                if abs(w["start"] - t) < 0.15 and re.sub(r"\W", "", w["text"].lower()) == \
                        re.sub(r"\W", "", k["text"].lower()):
                    keys.add(i)
        else:
            target = re.sub(r"\W", "", str(k).lower())
            for i, w in enumerate(words):
                if re.sub(r"\W", "", w["text"].lower()) == target:
                    keys.add(i)
    return keys


def ts(t):
    t = max(0.0, t)
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def srt_ts(t):
    ms = int(round(max(0.0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def word_markup(text, role, is_key, cfg, H, pop_in):
    """Every word carries a complete tag set (no \\r resets, which would cancel line-level animation).
    role: spoken | active | upcoming."""
    color = cfg["primary"]
    if role == "upcoming" and cfg["upcoming"]:
        color = cfg["upcoming"]
    if role == "active" and cfg["active"]:
        color = cfg["active"]
    if is_key and cfg["key_color"]:
        color = cfg["key_color"]
    font, weight, italic = cfg["font"], cfg["weight"], cfg["italic"]
    if is_key and cfg["key_font"]:
        font, weight, italic = cfg["key_font"], cfg["key_weight"] or 400, cfg["key_italic"]
    if role == "active" and cfg["active_bold"]:
        weight = 800
    size = round(cfg["size_pct"] / 100 * H * (cfg["key_size_mul"] if is_key else 1.0))
    target = 112 if (role == "active" and cfg["anim"] == "pop" and cfg["active"]) else 100
    if pop_in:
        scale = (f"\\fscx{round(target * 0.82)}\\fscy{round(target * 0.82)}"
                 f"\\t(0,90,\\fscx{round(target * 1.06)}\\fscy{round(target * 1.06)})"
                 f"\\t(90,170,\\fscx{target}\\fscy{target})")
    else:
        scale = f"\\fscx{target}\\fscy{target}"
    tags = f"\\1c{ass_color(color)}\\fn{font}\\b{weight}\\i{1 if italic else 0}\\fs{size}{scale}"
    return "{" + tags + "}" + esc(text)


def split_lines(texts, cfg):
    if cfg["lines"] < 2:
        return [list(range(len(texts)))]
    total = sum(len(t) + 1 for t in texts)
    if total <= cfg["max_chars_line"]:
        return [list(range(len(texts)))]
    best, best_diff = 1, 10 ** 9
    for k in range(1, len(texts)):
        a = sum(len(t) + 1 for t in texts[:k])
        diff = abs(total - 2 * a)
        if diff < best_diff:
            best, best_diff = k, diff
    return [list(range(best)), list(range(best, len(texts)))]


def build(words, cfg, W, H, keys, y_frac):
    fs = round(cfg["size_pct"] / 100 * H)
    outline = round(cfg["outline_pct"] / 100 * H, 1)
    shadow = round(cfg["shadow_pct"] / 100 * H, 1)
    border_style = 3 if cfg["box"] else 1
    if cfg["box"]:
        outline = round(cfg["box_pad_pct"] / 100 * H, 1)
    outc = cfg["box_color"] if cfg["box"] else cfg["outline"]
    style_line = (f"Style: Cap,{cfg['font']},{fs},{ass_color(cfg['primary'])},{ass_color(cfg['upcoming'] or cfg['primary'])},"
                  f"{ass_color(outc)},{ass_color(cfg['shadow'], 1 - cfg['shadow_alpha'])},"
                  f"{cfg['weight'] if cfg['weight'] >= 600 else 0},{-1 if cfg['italic'] else 0},0,0,100,100,"
                  f"{cfg['tracking']},0,"
                  f"{border_style},{outline},{shadow},5,{int(W * 0.08)},{int(W * 0.08)},0,1")
    header = "\n".join([
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2",
        "ScaledBorderAndShadow: yes", "YCbCr Matrix: TV.709", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding",
        style_line, "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ])
    events, srt = [], []
    groups = group_words(words, cfg)
    idx = {id(w): i for i, w in enumerate(words)}
    x, y = W // 2, int(H * y_frac)
    for gi, g in enumerate(groups):
        g_in = max(0.0, g[0]["start"] - 0.05)
        nxt_in = groups[gi + 1][0]["start"] - 0.05 if gi + 1 < len(groups) else g[-1]["end"] + 0.6
        g_out = min(nxt_in, g[-1]["end"] + 0.5)
        if g_out - g_in < 0.5:
            g_out = min(nxt_in, g_in + 0.5) if nxt_in > g_in + 0.3 else g_in + 0.5
        texts = [clean_word(w["text"], cfg) for w in g]
        gkeys = [idx[id(w)] in keys for w in g]
        if sum(gkeys) > 1:  # one highlighted word per group, the first chosen
            first = gkeys.index(True)
            gkeys = [i == first for i in range(len(g))]
        srt.append((g_in, g_out, " ".join(texts)))
        lines = split_lines(texts, cfg)
        per_word = bool(cfg["active"] or cfg["upcoming"] or cfg["active_bold"])
        steps = range(len(g)) if per_word else [None]
        for k in steps:
            t0 = g_in if (k is None or k == 0) else g[k]["start"]
            t1 = g_out if (k is None or k == len(g) - 1) else g[k + 1]["start"]
            if t1 - t0 < 0.02:
                continue
            first_step = k is None or k == 0
            last_step = k is None or k == len(g) - 1
            parts = []
            for li, line in enumerate(lines):
                seg = []
                for j in line:
                    role = "spoken" if k is None or j < k else ("active" if j == k else "upcoming")
                    seg.append(word_markup(texts[j], role, gkeys[j], cfg, H,
                                           pop_in=first_step and cfg["anim"] == "pop"))
                parts.append(" ".join(seg))
            body = "\\N".join(parts)
            fade_in = 120 if first_step and cfg["anim"] == "fade" else 0
            fade_out = 90 if last_step and cfg["anim"] in ("fade", "pop") else 0
            lead = f"{{\\an5\\pos({x},{y})" + (f"\\fad({fade_in},{fade_out})" if fade_in or fade_out else "") + "}"
            events.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{lead}{body}")
    return header + "\n" + "\n".join(events) + "\n", srt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words", nargs="?")
    ap.add_argument("--video", help="edited video (for resolution); or give --size")
    ap.add_argument("--size", help="WxH, e.g. 1080x1920")
    ap.add_argument("--style", default="1")
    ap.add_argument("--style-json", help="override fields, e.g. measured creator style")
    ap.add_argument("--keywords")
    ap.add_argument("--y", type=float, help="vertical centre of captions as fraction of height")
    ap.add_argument("--max-words", type=int)
    ap.add_argument("--accent", help="hex colour for active/key word")
    ap.add_argument("--out", help="output .ass path (default next to words file)")
    ap.add_argument("--burn", help="also burn into this output video (needs --video)")
    ap.add_argument("--fonts", default="work/fonts", help="folder with .ttf files for burn-in")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        for i, (k, v) in enumerate(STYLES.items(), 1):
            print(f"{i:>2} {k:<13} font={v.get('font')} {v.get('weight')} case={v.get('case', 'asis')} "
                  f"size={v.get('size_pct')}%H max_words={v.get('max_words')} fonts={v.get('fonts')}")
        return
    if not args.words:
        ap.error("words json required")
    name = resolve_style(args.style)
    cfg = dict(BASE)
    cfg.update(STYLES[name])
    if args.style_json:
        cfg.update(read_json(args.style_json))
    if args.max_words:
        cfg["max_words"] = args.max_words
    if args.accent:
        if cfg["key_color"] or name == "editorial":
            cfg["key_color"] = args.accent
        cfg["active"] = args.accent if cfg["active"] else cfg["active"]
        if not cfg["active"] and not cfg["key_color"]:
            cfg["key_color"] = args.accent

    if args.video:
        info = probe(args.video)
        W, H = info["width"], info["height"]
    elif args.size:
        W, H = (int(v) for v in args.size.lower().split("x"))
    else:
        die("give --video or --size")
    # 9:16 default 0.60 keeps captions inside the cross-platform safe box (y 288-1248 of 1920): Meta reserves
    # the bottom 35%, TikTok/Shorts put description + buttons there. 16:9 sits low; 1:1/4:5 in between.
    y = args.y if args.y is not None else (0.60 if H > W * 1.2 else (0.78 if abs(H - W) < W * 0.3 else 0.86))

    words = read_json(args.words)
    if isinstance(words, dict):
        words = words.get("words", [])
    words = [w for w in words if re.sub(r"\W", "", w["text"].lower()) not in {"um", "uh", "umm", "uhh", "erm", "hmm"}]
    keys = load_keywords(args.keywords, words)
    ass, srt = build(words, cfg, W, H, keys, y)

    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.words)), f"captions_{name}.ass")
    with open(out, "w", encoding="utf-8") as f:
        f.write(ass)
    srt_path = os.path.splitext(out)[0] + ".srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, (a, b, t) in enumerate(srt, 1):
            f.write(f"{i}\n{srt_ts(a)} --> {srt_ts(b)}\n{t}\n\n")
    print(f"Wrote {out} ({len(srt)} caption groups, style {name}, {W}x{H}, y={y}) and {srt_path}")
    print("Fonts needed:", ", ".join(cfg["fonts"]), f"-> python3 fetch_fonts.py --style {name} --dir {args.fonts}")

    if args.burn:
        if not args.video:
            die("--burn needs --video")
        sub = out.replace("\\", "/").replace(":", "\\:")
        fdir = os.path.abspath(args.fonts).replace("\\", "/").replace(":", "\\:")
        vf = f"subtitles='{sub}':fontsdir='{fdir}'" if os.path.isdir(args.fonts) else f"subtitles='{sub}'"
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostats", "-y", "-i", args.video, "-vf", vf,
               "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
               "-g", str(round(probe(args.video)["fps"])), "-c:a", "copy", "-movflags", "+faststart", args.burn]
        if subprocess.run(cmd).returncode != 0:
            die("burn-in failed")
        print(f"Burned captions -> {args.burn}. Check frames: python3 qa.py {args.burn} --frames-at-captions {out}")


if __name__ == "__main__":
    main()
