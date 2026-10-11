#!/usr/bin/env python3
"""Inspect raw footage before editing: specs, loudness, silences, keyframe spacing, contact sheet.

Usage: python3 probe.py <video> [--out work/probe] [--every 2]
Writes <out>/probe.json and <out>/contact.png and prints a short report with warnings.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import contact_sheet, loudness, need, probe, run, silences, write_json  # noqa: E402


def keyframe_gap(path, seconds=30):
    proc = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-skip_frame", "nokey",
                "-read_intervals", f"%+{seconds}", "-show_entries", "frame=pts_time",
                "-of", "csv=p=0", path], check=False)
    times = []
    for line in proc.stdout.splitlines():
        try:
            times.append(float(line.strip().strip(",")))
        except ValueError:
            pass
    if len(times) < 2:
        return None
    gaps = [b - a for a, b in zip(times, times[1:])]
    return round(max(gaps), 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default=None)
    ap.add_argument("--every", type=float, default=2.0, help="contact sheet: one frame every N seconds")
    args = ap.parse_args()
    need("ffmpeg")
    out = args.out or os.path.join("work", os.path.splitext(os.path.basename(args.video))[0], "probe")
    os.makedirs(out, exist_ok=True)

    info = probe(args.video)
    if not info["has_video"]:
        print("No video stream found.")
    warnings = []
    if info.get("has_audio"):
        info["loudness"] = loudness(args.video)
        sil = silences(args.video, noise_db=-35, min_dur=0.5)
        info["silences_over_0_5s"] = [[round(a, 3), round(b, 3)] for a, b in sil]
        info["dead_air_seconds"] = round(sum(b - a for a, b in sil), 2)
        lufs = info["loudness"].get("integrated_lufs")
        if lufs is not None and lufs < -30:
            warnings.append(f"Very quiet recording ({lufs} LUFS). Check the mic; normalize at the end.")
        tp = info["loudness"].get("true_peak_dbtp")
        if tp is not None and tp > -0.5:
            warnings.append(f"Audio peaks at {tp} dBTP: possible clipping. Listen to loud moments.")
    else:
        warnings.append("No audio stream: transcription and silence cutting are impossible.")
    if info["has_video"]:
        gap = keyframe_gap(args.video)
        info["max_keyframe_gap_s"] = gap
        if gap and gap > 1.0:
            warnings.append(f"Sparse keyframes (gap {gap}s). Re-encode before HyperFrames or it may freeze on seek: "
                            f"ffmpeg -i in -c:v libx264 -crf 18 -g {round(info['fps'])} -keyint_min {round(info['fps'])} "
                            "-pix_fmt yuv420p -c:a aac -movflags +faststart staged.mp4")
        if info.get("height", 0) < 1080 and info.get("width", 0) < 1080:
            warnings.append("Source below 1080p: punch-in zooms above ~105% will look soft.")
        elif min(info.get("width", 0), info.get("height", 0)) <= 1080:
            warnings.append("1080p source: keep punch-ins at or below ~112% (4K allows ~150%).")
        if info.get("color_transfer") in ("arib-std-b67", "smpte2084"):
            warnings.append("HDR source (HLG/PQ). Tone-map to SDR bt709 before editing or colors will wash out.")
        if info.get("rotation"):
            warnings.append(f"Phone rotation metadata {info['rotation']} deg: ffmpeg auto-rotates, HyperFrames may not. "
                            "Re-encode once to bake rotation in.")
        if abs(info["fps"] - round(info["fps"])) > 0.01 and info["fps"] not in (23.976, 29.97, 59.94):
            warnings.append(f"Unusual/variable frame rate {info['fps']}: re-encode to constant fps first.")
        info["contact_sheet"] = contact_sheet(args.video, os.path.join(out, "contact.png"), every=args.every)
    info["warnings"] = warnings
    write_json(info, os.path.join(out, "probe.json"))

    print(f"{os.path.basename(args.video)}: {info.get('width')}x{info.get('height')} @ {info.get('fps')} fps, "
          f"{info['duration']:.1f}s, {info.get('orientation')}, video={info.get('vcodec')} audio={info.get('acodec')}")
    if "loudness" in info:
        L = info["loudness"]
        print(f"Loudness: {L.get('integrated_lufs')} LUFS, peak {L.get('true_peak_dbtp')} dBTP, "
              f"dead air (>0.5s): {info['dead_air_seconds']}s across {len(info['silences_over_0_5s'])} gaps")
    for w in warnings:
        print("WARN:", w)
    print(f"Wrote {out}/probe.json and contact.png (look at the contact sheet).")


if __name__ == "__main__":
    main()
