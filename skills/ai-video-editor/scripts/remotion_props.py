#!/usr/bin/env python3
"""Build props.json for the Remotion starter (assets/remotion/) from this skill's own outputs.

Usage:
  python3 remotion_props.py --project work/remotion --video renders/v2_graded.mp4 --words work/words_cut.json \
      --platform reels [--keywords work/keywords.json] [--graphics work/graphics-remotion.json] [--style kinetic.json]
  python3 remotion_props.py --project work/remotion --words work/words_cut.json --duration 32   # pure motion, no footage

Copies the video (and every image a graphic names) into <project>/public/, reads width/height/fps/duration from
the file (no guessing), and writes <project>/props.json. Then:
  cd <project> && npx remotion render src/index.ts Edit out/edit.mp4 --props=props.json
Safe-zone QA (transparent, text and graphics only):
  python3 remotion_props.py ... --text-only --out props_qa.json
  npx remotion render src/index.ts Edit out/qa.mov --props=props_qa.json --codec=prores --prores-profile=4444 \
      --image-format=png --pixel-format=yuva444p10le
  python3 <skill>/scripts/safezone.py alpha out/qa.mov --platform reels
"""
import argparse
import os
import shutil
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import SAFE_ZONES, die, probe, read_json, write_json  # noqa: E402

CAPTIONS = {"enabled": True, "font": "Inter", "weight": 900, "sizePct": 4.8, "color": "#FFFFFF",
            "accent": "#FFD84D", "highlight": "key", "maxWords": 3, "yPct": 62, "uppercase": False, "hookUntil": 0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, help="the copied assets/remotion folder")
    ap.add_argument("--video", help="the locked cut (graded, no captions); omit for pure motion")
    ap.add_argument("--words", required=True, help="words_cut.json (edited timeline)")
    ap.add_argument("--platform", default="cross", choices=sorted(SAFE_ZONES))
    ap.add_argument("--keywords", help="json list of key words (chosen by meaning)")
    ap.add_argument("--graphics", help="json list of graphics: title / stat / image (see assets/remotion/README.md)")
    ap.add_argument("--style", help="json object overriding caption fields (font, sizePct, accent, ...)")
    ap.add_argument("--duration", type=float, help="seconds, for pure motion without a video")
    ap.add_argument("--size", default="1080x1920", help="WxH for pure motion")
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--hook-until", type=float, default=0.0)
    ap.add_argument("--no-captions", action="store_true", help="captions burned elsewhere (captions.py)")
    ap.add_argument("--text-only", action="store_true", help="transparent QA render for safezone.py alpha")
    ap.add_argument("--out", default="props.json")
    args = ap.parse_args()

    pub = os.path.join(args.project, "public")
    if not os.path.isdir(pub):
        die(f"{pub} not found: copy assets/remotion to {args.project} first")
    words = [{"text": w["text"], "start": w["start"], "end": w["end"]} for w in read_json(args.words)]
    w, h = (int(v) for v in args.size.lower().split("x"))
    fps, duration, video = args.fps, args.duration, None
    if args.video:
        info = probe(args.video)
        if not info.get("width"):
            die("--video has no picture; for a voiceover reel omit --video and give --duration")
        w, h, duration = info["width"], info["height"], info["duration"]
        fps = info.get("fps") or fps
        video = "cut" + os.path.splitext(args.video)[1].lower()
        shutil.copy2(args.video, os.path.join(pub, video))
        if abs(fps - round(fps)) > 0.01 and fps not in (23.976, 29.97, 59.94):
            print(f"WARN: odd frame rate {fps}; render the composition at the source rate or captions drift.")
    graphics = read_json(args.graphics) if args.graphics else []
    for g in graphics:
        if g.get("type") == "image":
            src = g["src"]
            if not os.path.exists(src):
                die(f"graphic image not found: {src}")
            g["src"] = os.path.basename(src)
            shutil.copy2(src, os.path.join(pub, g["src"]))
        end = g["at"] + g["duration"]
        if duration and end > duration + 0.01:
            print(f"WARN: graphic at {g['at']}s runs past the end ({end:.2f}s > {duration:.2f}s)")
    caps = dict(CAPTIONS, **(read_json(args.style) if args.style else {}))
    caps["hookUntil"] = args.hook_until
    caps["enabled"] = not args.no_captions
    props = {"video": video, "durationInSeconds": duration, "width": w, "height": h, "fps": fps,
             "platform": args.platform, "words": words,
             "keywords": read_json(args.keywords) if args.keywords else [],
             "captions": caps, "graphics": graphics, "texture": "none", "accent": caps["accent"],
             "showSafeZone": False, "textOnly": args.text_only}
    fonts = os.path.join(pub, "fonts")
    if not (os.path.isdir(fonts) and any(f.endswith((".ttf", ".otf", ".woff2")) for f in os.listdir(fonts))):
        print(f"WARN: no fonts in {fonts}: python3 scripts/fetch_fonts.py \"Inter:700,900\" --dir {fonts}")
    out = args.out if os.path.isabs(args.out) else os.path.join(args.project, args.out)
    write_json(props, out)
    print(f"Wrote {out}: {w}x{h} @ {fps} fps, {duration if duration else 'auto'} s, {len(words)} words, "
          f"{len(graphics)} graphics, zone {args.platform}{' (TEXT ONLY, transparent QA render)' if args.text_only else ''}")


if __name__ == "__main__":
    main()
