#!/usr/bin/env python3
"""Download static TTF files from Google Fonts (all OFL / Apache licensed) into a project fonts folder.

Usage:
  python3 fetch_fonts.py "Montserrat:900" "Inter:500,800" "Instrument Serif:i400" --dir work/fonts
  python3 fetch_fonts.py --style 6 --dir work/fonts        # fonts needed by caption style 6
Spec: Family:weights, where a weight prefixed with i is italic (i400). The Google CSS API is asked with a
desktop-less user agent so it returns .ttf (libass/ffmpeg and HyperFrames @font-face both accept TTF).
"""
import argparse
import os
import re
import sys
import urllib.parse
import urllib.request

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

UA = "Mozilla/5.0"  # minimal UA -> Google serves truetype URLs


def css_url(family, weights):
    ital = any(w.startswith("i") for w in weights)
    fam = urllib.parse.quote_plus(family)
    if ital:
        pairs = sorted({(1 if w.startswith("i") else 0, int(w.lstrip("i"))) for w in weights})
        axis = "ital,wght@" + ";".join(f"{i},{w}" for i, w in pairs)
    else:
        axis = "wght@" + ";".join(str(w) for w in sorted({int(w) for w in weights}))
    return f"https://fonts.googleapis.com/css2?family={fam}:{axis}"


def fetch(spec, out_dir):
    family, _, ws = spec.partition(":")
    weights = [w.strip() for w in (ws or "400").split(",") if w.strip()]
    req = urllib.request.Request(css_url(family.strip(), weights), headers={"User-Agent": UA})
    css = urllib.request.urlopen(req, timeout=30).read().decode()
    saved = []
    for block in css.split("@font-face")[1:]:
        style = re.search(r"font-style:\s*(\w+)", block).group(1)
        weight = re.search(r"font-weight:\s*(\d+)", block).group(1)
        url = re.search(r"url\((https://[^)]+\.ttf)\)", block)
        if not url:
            continue
        # unicode-range blocks repeat per subset; keep latin + devanagari by downloading each unique file
        name = f"{family.strip().replace(' ', '')}-{weight}{'Italic' if style == 'italic' else ''}"
        path = os.path.join(out_dir, name + ".ttf")
        if path in saved:  # extra unicode-range subset of a weight already saved this run
            path = os.path.join(out_dir, f"{name}-{len(saved)}.ttf")
        elif os.path.exists(path):  # fetched in an earlier run: keep it, do not download again
            saved.append(path)
            continue
        urllib.request.urlretrieve(url.group(1), path)
        saved.append(path)
    return saved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("specs", nargs="*")
    ap.add_argument("--dir", default="work/fonts")
    ap.add_argument("--style", help="caption style id/name from captions.py; fetches its fonts")
    args = ap.parse_args()
    specs = list(args.specs)
    if args.style:
        from captions import STYLES, resolve_style  # noqa: WPS433
        specs += STYLES[resolve_style(args.style)]["fonts"]
    if not specs:
        ap.error("give at least one Family:weights spec or --style")
    os.makedirs(args.dir, exist_ok=True)
    for s in specs:
        try:
            files = fetch(s, args.dir)
            print(f"{s}: {len(files)} file(s) -> {', '.join(os.path.basename(f) for f in files)}")
        except Exception as e:  # network / unknown family
            print(f"{s}: FAILED ({e}). Check the family name on fonts.google.com", file=sys.stderr)
    with open(os.path.join(args.dir, "LICENSES.txt"), "a", encoding="utf-8") as f:
        f.write("Fonts downloaded from Google Fonts (SIL Open Font License 1.1 or Apache 2.0). "
                "See https://fonts.google.com/attribution\n")


if __name__ == "__main__":
    main()
