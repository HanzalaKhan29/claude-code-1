#!/usr/bin/env python3
"""Composite rendered graphics (HyperFrames MOV/WebM with alpha, or MP4 cutaways) onto the edit.

Usage:
  python3 overlay.py <base.mp4> <graphics.json> <out.mp4>
graphics.json (times on the EDITED timeline, i.e. words_cut.json times):
  [
    {"file": "work/gfx/lower-third.mov", "at": 3.20},                          # alpha overlay, full frame
    {"file": "work/gfx/stat.webm", "at": 12.48, "x": 0, "y": 0},              # alpha WebM (VP9)
    {"file": "work/gfx/chart.mp4", "at": 30.0, "mode": "cutaway"},             # full-screen, base audio continues
    {"file": "work/gfx/broll.mp4", "at": 41.5, "mode": "cutaway", "dur": 2.4}  # trim a cutaway
  ]
Rules baked in: overlays never repeat their last frame (eof_action=pass); VP9 alpha is decoded with libvpx
(the native decoder silently drops alpha); the base audio is always kept; captions are burned AFTER this
step (subtitles go last, on top of every graphic).
"""
import argparse
import os
import subprocess
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, need, probe, read_json  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("graphics")
    ap.add_argument("out")
    ap.add_argument("--crf", type=int, default=18)
    args = ap.parse_args()
    need("ffmpeg")
    if os.path.abspath(args.out) == os.path.abspath(args.base):
        die("output must be a new file")
    base = probe(args.base)
    W, H = base["width"], base["height"]
    items = read_json(args.graphics)
    if not items:
        die("graphics.json is empty")

    inputs = ["-i", args.base]
    chains, last = [], "[0:v]"
    for k, g in enumerate(sorted(items, key=lambda x: float(x["at"]))):
        f = g["file"]
        if not os.path.exists(f):
            die(f"missing graphic: {f}")
        gi = probe(f)
        if f.lower().endswith(".webm"):
            inputs += ["-c:v", "libvpx-vp9"]
        inputs += ["-i", f]
        at = float(g["at"])
        dur = float(g.get("dur") or gi["duration"])
        mode = g.get("mode", "overlay")
        lab = f"[g{k}]"
        trim = f"trim=duration={dur:.3f}," if g.get("dur") else ""
        if mode == "cutaway":
            chains.append(f"[{k + 1}:v]{trim}scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                          f"setsar=1,format=yuv420p,setpts=PTS-STARTPTS+{at:.3f}/TB{lab}")
            x, y = 0, 0
        else:
            scale = "" if (gi.get("width"), gi.get("height")) == (W, H) or "x" in g else f"scale={W}:{H},"
            chains.append(f"[{k + 1}:v]{trim}{scale}format=yuva420p,setpts=PTS-STARTPTS+{at:.3f}/TB{lab}")
            x, y = g.get("x", 0), g.get("y", 0)
        out_lab = f"[b{k}]"
        chains.append(f"{last}{lab}overlay=x={x}:y={y}:eof_action=pass:enable='between(t,{at:.3f},{at + dur:.3f})'"
                      f"{out_lab}")
        last = out_lab
    chains[-1] = chains[-1].rsplit("[", 1)[0] + ",format=yuv420p[v]"
    graph = ";".join(chains)
    fps = round(base["fps"]) or 30
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostats", "-y"] + inputs + [
        "-filter_complex", graph, "-map", "[v]"]
    if base.get("has_audio"):
        cmd += ["-map", "0:a", "-c:a", "copy"]
    cmd += ["-c:v", "libx264", "-crf", str(args.crf), "-preset", "medium", "-pix_fmt", "yuv420p", "-g", str(fps),
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart",
            args.out]
    if subprocess.run(cmd).returncode != 0:
        die("overlay compositing failed")
    print(f"Composited {len(items)} graphic(s) -> {args.out}. Check frames at each 'at' time before moving on.")


if __name__ == "__main__":
    main()
