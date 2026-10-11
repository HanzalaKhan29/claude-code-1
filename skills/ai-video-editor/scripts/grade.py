#!/usr/bin/env python3
"""Colour: correct, match, grade and finish with ffmpeg-only filters (all verified to exist in ffmpeg >= 5.1).

Usage:
  python3 grade.py in.mp4 out.mp4 --look warm [--strength 0.8] [--grain 2] [--glow 0.25]
  python3 grade.py broll.mp4 broll_matched.mp4 --match renders/v1.mp4 --look warm   # match B-roll to A-roll
  python3 grade.py in.mp4 --still 4.0 --look film --out-still work/grade_film.png     # before|after preview
  python3 grade.py --look warm --export-lut work/looks/warm.cube                      # ship the look as a LUT
  python3 grade.py in.mp4 out.mp4 --lut work/looks/warm.cube
Looks: clean (correction only), warm (talking head), split (teal shadows / warm highlights, subtle),
       film (lifted blacks, softer saturation), mono (black and white with contrast).
Order is fixed and matters: match (exposure + white balance) -> look -> strength blend -> glow -> grain.
Exposure and white balance are correction; everything after is look. Grade-match B-roll BEFORE the look.

Rules baked in: saturation via vibrance (protects skin); never crush blacks (mobile screens turn crushed
shadows into mud); grain 1-5% dithers banding after platform compression; glow is a blurred highlight
copy screened on top (ffmpeg has no bloom filter). selectivecolor values are -1..1, never Photoshop 0-100.
Never use colorbalance pl=1 (preserve lightness): in ffmpeg 6.x it turns any pixel with a zero channel
(pure yellow, green, logos, saturated graphics) flat grey.
Cannot do (say so instead of faking it): tracked face relight, AI subject masks, per-object keying, power
windows that follow motion, true HDR grading. Use DaVinci Resolve (free) for those.
"""
import argparse
import os
import struct
import subprocess
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, need, probe  # noqa: E402

LOOKS = {
    "clean": "eq=contrast=1.03,vibrance=intensity=0.10,curves=all='0/0 0.25/0.24 0.75/0.765 1/1'",
    "warm": ("colortemperature=temperature=5600:mix=0.35:pl=1,vibrance=intensity=0.05,"
             "curves=all='0/0.01 0.25/0.235 0.75/0.77 1/1'"),
    "split": ("colorbalance=rs=-0.05:gs=0.005:bs=0.06:rh=0.05:gh=0.01:bh=-0.04,eq=contrast=1.04,"
              "vibrance=intensity=0.08"),
    "film": ("curves=all='0/0.055 0.25/0.26 0.75/0.755 1/0.965',eq=saturation=0.88,"
             "colorbalance=rh=0.03:gh=0.005:bh=-0.025:rs=-0.01:bs=0.02"),
    "mono": "hue=s=0,curves=all='0/0.02 0.25/0.21 0.75/0.8 1/0.99'",
}


def mean_rgb(path, samples=12):
    dur = probe(path)["duration"] or 1
    fps = max(samples / dur, 0.05)
    raw = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", path, "-vf",
                          f"fps={fps:.4f},scale=32:18,format=rgb24", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    if not raw:
        die(f"could not read frames from {path}")
    n = len(raw) // 3
    return [sum(raw[c::3]) / n for c in range(3)]


def match_filter(src, ref):
    a, b = mean_rgb(src), mean_rgb(ref)
    gains = [min(1.33, max(0.75, (b[i] + 1) / (a[i] + 1))) for i in range(3)]
    print(f"Match: source mean RGB {[round(x) for x in a]} -> reference {[round(x) for x in b]}; "
          f"gains R{gains[0]:.3f} G{gains[1]:.3f} B{gains[2]:.3f}")
    return f"colorchannelmixer=rr={gains[0]:.4f}:gg={gains[1]:.4f}:bb={gains[2]:.4f}"


def color_chain(args, match=None):
    parts = [match] if match else []
    if args.look:
        parts.append(LOOKS[args.look])
    if args.lut:
        parts.append(f"lut3d=file='{args.lut}'")
    return ",".join(parts)


def build_graph(args, match=None):
    chain = color_chain(args, match) or "null"
    g = []
    if args.strength < 1.0:
        g.append(f"[0:v]format=yuv444p,split[o][c];[c]{chain}[g];"
                 f"[o][g]blend=all_mode=normal:all_opacity={args.strength:.3f}[graded]")
    else:
        g.append(f"[0:v]format=yuv444p,{chain}[graded]")
    last = "[graded]"
    if args.glow > 0:
        g.append(f"{last}split[gb][gh];[gh]curves=all='0/0 0.62/0 1/1',gblur=sigma=18[gl];"
                 f"[gb][gl]blend=all_mode=screen:all_opacity={args.glow:.3f}[glowed]")
        last = "[glowed]"
    tail = "format=yuv420p"
    if args.grain > 0:
        tail = f"noise=alls={args.grain * 2.5:.1f}:allf=t+u," + tail
    g.append(f"{last}{tail}[v]")
    return ";".join(g)


def export_lut(args, path, size=33):
    """Bake the colour part (match is per-clip, so not included) into a .cube 3D LUT."""
    chain = color_chain(args)
    if not chain:
        die("nothing to export: give --look or --lut")
    n = size
    ident = bytearray()
    for b in range(n):
        for g in range(n):
            for r in range(n):  # .cube order: red fastest
                ident += struct.pack("<HHH", *(round(v * 65535 / (n - 1)) for v in (r, g, b)))
    proc = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb48le",
                           "-s", f"{n * n}x{n}", "-i", "-", "-vf", f"format=gbrp16le,{chain},format=rgb48le",
                           "-f", "rawvideo", "-"], input=bytes(ident), capture_output=True)
    if proc.returncode != 0 or len(proc.stdout) != len(ident):
        die("LUT export failed: " + proc.stderr.decode()[-300:])
    vals = struct.unpack(f"<{len(proc.stdout) // 2}H", proc.stdout)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"TITLE \"{args.look or 'custom'}\"\nLUT_3D_SIZE {n}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n")
        for i in range(0, len(vals), 3):
            f.write(f"{vals[i] / 65535:.6f} {vals[i + 1] / 65535:.6f} {vals[i + 2] / 65535:.6f}\n")
    print(f"Wrote {path} ({n}^3). Apply anywhere with --lut, ffmpeg lut3d, Resolve, Premiere or CapCut.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp", nargs="?")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--look", choices=list(LOOKS))
    ap.add_argument("--lut", help="apply a .cube LUT")
    ap.add_argument("--strength", type=float, default=1.0, help="0..1 mix of the graded image over the original")
    ap.add_argument("--match", help="reference video/image to match exposure and white balance to")
    ap.add_argument("--grain", type=float, default=0.0, help="film grain percent, 1-5 is the useful range")
    ap.add_argument("--glow", type=float, default=0.0, help="highlight glow opacity, 0.15-0.35 is subtle")
    ap.add_argument("--still", type=float, help="write a before|after PNG at this time instead of a video")
    ap.add_argument("--out-still", default="grade_preview.png")
    ap.add_argument("--export-lut")
    ap.add_argument("--crf", type=int, default=17)
    args = ap.parse_args()
    need("ffmpeg")
    if args.export_lut:
        export_lut(args, args.export_lut)
        if not args.inp:
            return
    if not args.inp:
        ap.error("give an input video")
    if not (args.look or args.lut or args.match or args.grain or args.glow):
        ap.error("nothing to do: give --look, --lut, --match, --grain or --glow")
    if args.lut and not os.path.exists(args.lut):
        die(f"LUT not found: {args.lut}")
    match = match_filter(args.inp, args.match) if args.match else None
    graph = build_graph(args, match)
    if args.still is not None:
        sgraph = graph.replace("[0:v]", "[0:v]split[before][src];[src]", 1).replace("[v]", "[after]")
        sgraph += ";[before]format=yuv420p[b2];[b2][after]hstack[v]"
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{args.still:.3f}", "-i", args.inp,
               "-filter_complex", sgraph, "-map", "[v]", "-frames:v", "1", args.out_still]
        if subprocess.run(cmd).returncode != 0:
            die("preview failed")
        print(f"Wrote {args.out_still} (left: original, right: graded). Look at skin, blacks and highlights.")
        return
    if not args.out:
        ap.error("give an output path")
    if os.path.abspath(args.inp) == os.path.abspath(args.out):
        die("output must be a new file")
    info = probe(args.inp)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostats", "-y", "-i", args.inp,
           "-filter_complex", graph, "-map", "[v]"]
    if info.get("has_audio"):
        cmd += ["-map", "0:a", "-c:a", "copy"]
    cmd += ["-c:v", "libx264", "-crf", str(args.crf), "-preset", "medium", "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart",
            args.out]
    if subprocess.run(cmd).returncode != 0:
        die("grade failed")
    print(f"Graded -> {args.out}. Compare a frame before/after (--still) and check skin is not orange.")


if __name__ == "__main__":
    main()
