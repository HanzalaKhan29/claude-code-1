#!/usr/bin/env python3
"""Pre-delivery QA. Prints PASS/WARN/FAIL lines and builds review sheets the agent must LOOK at.

Usage:
  python3 qa.py <final.mp4> [--edl edl.json] [--captions captions.ass] [--platform youtube|shorts|...]
                [--out work/x/qa]
Checks: spec (codec, pix_fmt, fps, resolution, faststart), loudness vs target, true peak, black frames,
frozen frames, dead air, flash frames (very short shots), and builds:
  cuts.png      the frame just before and just after every edit point (jump-cut / flash check)
  captions.png  one frame in the middle of every 3rd caption group (legibility, face overlap, safe zone)
  overview.png  one frame every N seconds
"""
import argparse
import os
import re
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import contact_sheet, detect_cuts, frame_at, loudness, probe, read_json, run, silences  # noqa: E402

TARGET = {"youtube": (-14, -1.0), "shorts": (-14, -1.0), "reels": (-14, -1.0), "tiktok": (-14, -1.0),
          "linkedin": (-14, -1.0), "x": (-14, -1.0), "master": (-14, -1.0)}


def tile(pngs, out, cols=4):
    if not pngs:
        return None
    lst = out + ".txt"
    with open(lst, "w") as f:
        for p in pngs:
            f.write(f"file '{os.path.abspath(p)}'\n")
    rows = -(-len(pngs) // cols)
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-vf", f"scale=360:-2,tile={cols}x{rows}:padding=4:margin=4", "-frames:v", "1", out])
    os.remove(lst)
    for p in pngs:
        os.remove(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--edl")
    ap.add_argument("--captions")
    ap.add_argument("--platform", default="youtube", choices=list(TARGET))
    ap.add_argument("--out")
    ap.add_argument("--every", type=float, default=5.0)
    args = ap.parse_args()
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.video)), "qa")
    os.makedirs(out, exist_ok=True)
    res = []

    def report(level, msg):
        res.append((level, msg))
        print(f"{level:<4} {msg}")

    info = probe(args.video)
    report("PASS" if info.get("vcodec") in ("h264", "hevc", "av1", "prores") else "WARN",
           f"video codec {info.get('vcodec')}")
    report("PASS" if info.get("pix_fmt") in ("yuv420p", "yuvj420p") else "FAIL",
           f"pixel format {info.get('pix_fmt')} (yuv420p needed for every player)")
    report("PASS" if info.get("acodec") == "aac" else "WARN", f"audio codec {info.get('acodec')}")
    report("PASS" if info.get("sample_rate") in (48000, 44100) else "WARN", f"sample rate {info.get('sample_rate')}")
    vert = info.get("height", 0) > info.get("width", 0)
    if args.platform in ("shorts", "reels", "tiktok") and not vert:
        report("FAIL", f"{args.platform} needs vertical 9:16; file is {info.get('width')}x{info.get('height')}")
    if min(info.get("width", 0), info.get("height", 0)) < 1080:
        report("WARN", f"below 1080p ({info.get('width')}x{info.get('height')})")
    with open(args.video, "rb") as f:
        head = f.read(64 * 1024)
    report("PASS" if head.find(b"moov") != -1 and (head.find(b"mdat") == -1 or head.find(b"moov") < head.find(b"mdat"))
           else "WARN", "faststart (moov atom at start, plays before full download)")

    if info.get("has_audio"):
        L = loudness(args.video)
        tgt, tp = TARGET[args.platform]
        i_l, p = L.get("integrated_lufs"), L.get("true_peak_dbtp")
        if i_l is not None:
            report("PASS" if abs(i_l - tgt) <= 1.0 else "FAIL", f"loudness {i_l} LUFS (target {tgt} +/-1)")
        if p is not None:
            report("PASS" if p <= tp + 0.3 else "FAIL", f"true peak {p} dBTP (max {tp})")
        gaps = [s for s in silences(args.video, -45, 1.2) if s[0] > 0.5 and s[1] < info["duration"] - 0.5]
        report("PASS" if not gaps else "WARN", f"dead air >1.2s: {len(gaps)}"
               + (" at " + ", ".join(f"{a:.1f}s" for a, _ in gaps[:10]) if gaps else ""))

    bl = run(["ffmpeg", "-hide_banner", "-nostats", "-i", args.video, "-an", "-vf",
              "blackdetect=d=0.08:pix_th=0.06", "-f", "null", "-"], check=False).stderr
    blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", bl)
    blacks = [(float(a), float(b)) for a, b in blacks if not (float(a) < 0.05 and float(b) < 1.0)]
    report("PASS" if not blacks else "WARN", f"black frames: {len(blacks)}"
           + (" at " + ", ".join(f"{float(a):.2f}s" for a, _ in blacks[:10]) if blacks else ""))
    fz = run(["ffmpeg", "-hide_banner", "-nostats", "-i", args.video, "-an", "-vf",
              "scale=320:-2,freezedetect=n=0.002:d=2.5", "-f", "null", "-"], check=False).stderr
    freezes = re.findall(r"freeze_start: ([\d.]+)", fz)
    report("PASS" if not freezes else "WARN", f"frozen picture >2.5s: {len(freezes)}"
           + (" at " + ", ".join(f"{float(a):.1f}s" for a in freezes[:10]) if freezes else "")
           + " (fine for slides/holds; a bug if it is supposed to be live footage)")

    cuts = [c["t"] for c in detect_cuts(args.video)]
    fps = info.get("fps") or 30
    shots = [b - a for a, b in zip([0.0] + cuts, cuts + [info["duration"]])]
    flash = [round(c, 2) for c, s in zip([0.0] + cuts, shots) if s < 3 / fps and c > 0]
    report("PASS" if not flash else "FAIL", f"flash frames (shots < 3 frames): {len(flash)}"
           + (f" at {flash[:10]}" if flash else ""))

    edit_points = []
    if args.edl:
        t = 0.0
        for s in read_json(args.edl)["segments"][:-1]:
            t += s["end"] - s["start"]
            edit_points.append(t)
    else:
        edit_points = cuts
    pngs = []
    for i, t in enumerate(edit_points[:40]):
        pngs.append(frame_at(args.video, max(0, t - 1.5 / fps), os.path.join(out, f"_c{i:03d}a.png"), 480))
        pngs.append(frame_at(args.video, t + 1.5 / fps, os.path.join(out, f"_c{i:03d}b.png"), 480))
    if pngs:
        tile(pngs, os.path.join(out, "cuts.png"), cols=4)
        report("LOOK", f"cuts.png: before/after pairs for {min(40, len(edit_points))} edit points")

    if args.captions and os.path.exists(args.captions):
        times = []
        for line in open(args.captions, encoding="utf-8"):
            if line.startswith("Dialogue:"):
                p = line.split(",")
                h, m, s = p[1].split(":")
                h2, m2, s2 = p[2].split(":")
                a = int(h) * 3600 + int(m) * 60 + float(s)
                b = int(h2) * 3600 + int(m2) * 60 + float(s2)
                times.append((a + b) / 2)
        sample = sorted(set(round(t, 1) for t in times))[::3][:24]
        cp = [frame_at(args.video, t, os.path.join(out, f"_k{i:03d}.png"), 480) for i, t in enumerate(sample)]
        if cp:
            tile(cp, os.path.join(out, "captions.png"), cols=4)
            report("LOOK", "captions.png: check legibility, face overlap, platform UI safe zones, spelling")

    contact_sheet(args.video, os.path.join(out, "overview.png"), every=args.every)
    report("LOOK", "overview.png: whole-video rhythm, colour consistency, nothing broken")

    fails = [m for lv, m in res if lv == "FAIL"]
    with open(os.path.join(out, "qa.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(f"{lv} {m}" for lv, m in res) + "\n")
    print("\nRESULT:", "FAIL (fix before delivery)" if fails else "no automatic failures. Now LOOK at the sheets "
          "and listen to every join before calling it done.")


if __name__ == "__main__":
    main()
