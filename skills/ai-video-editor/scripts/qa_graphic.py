#!/usr/bin/env python3
"""QA for a rendered graphic (transparent MOV/WebM or an MP4 cutaway) before it goes into the edit.

Usage: python3 qa_graphic.py <graphic.mov|webm|mp4> [--out qa_dir] [--times 0.5,2.4,4.6]
Checks:
  * alpha present (for overlays) and FIRST / LAST frames fully transparent (no stuck plate at the cut)
  * single-frame pops: a frame whose change from its neighbours is ~3x larger than both (a glitch, not motion)
  * spec: resolution, fps, duration
Builds review sheets the agent must look at:
  * over_black.png, over_white.png, over_grey.png at the sample times: hyperframes `check` cannot measure
    contrast on a transparent card, so judge legibility against the worst plausible background here
"""
import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, need, probe, run  # noqa: E402


def dec(path):
    return ["-c:v", "libvpx-vp9"] if path.lower().endswith(".webm") else []


def alpha_mean(path, t):
    proc = run(["ffmpeg", "-hide_banner", "-nostats"] + dec(path) + ["-ss", f"{t:.3f}", "-i", path, "-frames:v", "1",
                "-vf", "format=yuva444p,alphaextract,signalstats,metadata=print:key=lavfi.signalstats.YAVG",
                "-f", "null", "-"], check=False)
    m = re.findall(r"YAVG=([\d.]+)", proc.stderr)
    return float(m[0]) if m else None  # first printed frame = the frame at t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("graphic")
    ap.add_argument("--out")
    ap.add_argument("--times", help="comma-separated sample times; default 6 evenly spaced")
    args = ap.parse_args()
    need("ffmpeg")
    info = probe(args.graphic)
    out = args.out or os.path.splitext(args.graphic)[0] + "_qa"
    os.makedirs(out, exist_ok=True)
    dur, fps = info["duration"], info.get("fps") or 30
    print(f"spec: {info.get('width')}x{info.get('height')} @ {fps} fps, {dur:.2f}s, {info.get('vcodec')} "
          f"{info.get('pix_fmt')}")
    fails = 0

    has_alpha = "a" in (info.get("pix_fmt") or "").replace("yuv", "").replace("rgb", "") or \
        (args.graphic.lower().endswith(".webm"))
    if has_alpha:
        first = alpha_mean(args.graphic, 0)
        last = alpha_mean(args.graphic, max(0, dur - 3.0 / fps))
        peak = max((alpha_mean(args.graphic, dur * k / 8) or 0) for k in range(1, 8))
        print(f"alpha mean: first {first}, last {last}, peak {peak:.1f}")
        if peak is not None and peak < 1:
            print("FAIL nothing visible: alpha is empty in every sample (did the render capture the content?)")
            fails += 1
        for name, v in (("first", first), ("last", last)):
            if v is not None and v > 0.5:
                print(f"WARN {name} frame is not fully transparent (alpha mean {v:.2f}): the graphic will pop "
                      "on/off at the cut instead of animating")
    else:
        print("no alpha channel: treat as a full-frame cutaway (overlay.py mode 'cutaway')")

    # single-frame pops via YDIF spikes
    proc = run(["ffmpeg", "-hide_banner", "-nostats"] + dec(args.graphic) + ["-i", args.graphic, "-vf",
                "scale=480:-2,signalstats,metadata=print:key=lavfi.signalstats.YDIF", "-f", "null", "-"], check=False)
    ydif = [float(x) for x in re.findall(r"YDIF=([\d.]+)", proc.stderr)]
    pops = []
    for i in range(1, len(ydif) - 1):
        a, b, c = ydif[i - 1], ydif[i], ydif[i + 1]
        if b > 4 and b > 3 * max(a, 0.5) and b > 3 * max(c, 0.5):
            pops.append(round(i / fps, 3))
    print("PASS no single-frame pops" if not pops else f"WARN possible single-frame pops at {pops[:10]} s")

    times = [float(x) for x in args.times.split(",")] if args.times else [dur * k / 7 for k in range(1, 7)]
    for bg, color in (("black", "black"), ("white", "white"), ("grey", "0x808080")):
        sheet = os.path.join(out, f"over_{bg}.png")
        n = len(times)
        sel = "+".join(f"eq(n\\,{int(round(t * fps))})" for t in times)
        graph = (f"color=c={color}:s={info['width']}x{info['height']}:r={fps}:d={dur:.3f}[bg];"
                 f"[0:v]format=yuva420p[fg];[bg][fg]overlay=eof_action=pass,select='{sel}',"
                 f"scale=480:-2,tile={min(n, 3)}x{-(-n // 3)}:padding=4:margin=4")
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"] + dec(args.graphic) + [
            "-i", args.graphic, "-filter_complex", graph, "-frames:v", "1", "-vsync", "vfr", sheet]
        if subprocess.run(cmd).returncode != 0:
            print(f"WARN could not build {sheet}")
    print(f"LOOK {out}/over_black.png, over_white.png, over_grey.png: text readable on all three? "
          "If not, strengthen the plate/shadow (see captions.md section 7).")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
