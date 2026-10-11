#!/usr/bin/env python3
"""Measure a reference creator video so the style card is built from numbers, not vibes.

Usage:
  python3 analyze_reference.py <video-file-or-URL> [--out work/refs/<name>] [--threshold 0.27]
  (URLs are downloaded with yt-dlp at <=1080p; ask the user before downloading.)

Outputs in --out:
  measurements.json   cut times, shot lengths, cuts/min (whole, first 30s, rest), pacing curve,
                      loudness, per-second audio level, silences, palette, optional face share
  contact.png         one frame every 2 s (whole video)
  hook.png            one frame every 0.5 s for the first 15 s (the hook in detail)
  shots/shot_XXX.jpg  one mid-frame per shot (look at these for captions, graphics, framing)
  measurements.md     human summary to paste into the style card
The agent still LOOKS at the images to read caption style, fonts, graphics and framing.
"""
import argparse
import glob
import importlib.util
import os
import shutil
import statistics
import subprocess
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (contact_sheet, detect_cuts, die, dominant_colors, fmt_tc, frame_at, loudness,  # noqa: E402
                     need, probe, run, silences, write_json)


def download(url, out_dir):
    if not shutil.which("yt-dlp"):
        die("yt-dlp not installed. Install it (see doctor.py) or download the video manually.")
    os.makedirs(out_dir, exist_ok=True)
    tmpl = os.path.join(out_dir, "source.%(ext)s")
    run(["yt-dlp", "-f", "bv*[height<=1080]+ba/b[height<=1080]/b", "--merge-output-format", "mp4",
         "-o", tmpl, "--no-playlist", url], capture=False)
    files = glob.glob(os.path.join(out_dir, "source.*"))
    if not files:
        die("download failed")
    return files[0]


def audio_levels(path, dur):
    """Approximate per-second RMS level in dBFS (talking vs music vs silence pattern)."""
    proc = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn", "-af",
                "aresample=48000,asetnsamples=n=48000,astats=metadata=1:reset=1,"
                "ametadata=print:key=lavfi.astats.Overall.RMS_level", "-f", "null", "-"], check=False)
    levels = []
    for line in proc.stderr.splitlines():
        if "RMS_level=" in line:
            v = line.split("RMS_level=")[1].strip()
            try:
                levels.append(round(float(v), 1) if v not in ("-inf", "inf") else -90.0)
            except ValueError:
                levels.append(-90.0)
    return levels[: int(dur) + 1]


def face_share(path, dur, step=1.0):
    """Optional (needs opencv-python): % of sampled frames with a face, and median face height % of frame."""
    if importlib.util.find_spec("cv2") is None:
        return None
    import cv2  # noqa: WPS433
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(path)
    hits, heights, n, t = 0, [], 0, 0.0
    while t < dur:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
        faces = cascade.detectMultiScale(small, 1.1, 5, minSize=(24, 24))
        n += 1
        if len(faces):
            hits += 1
            heights.append(max(f[3] for f in faces) / small.shape[0])
        t += step
    cap.release()
    if not n:
        return None
    return {"face_on_screen_pct": round(100 * hits / n, 1),
            "median_face_height_pct": round(100 * statistics.median(heights), 1) if heights else None,
            "samples": n, "method": "OpenCV Haar frontal face, 1 sample/s (misses profiles; treat as estimate)"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--out", default=None)
    ap.add_argument("--threshold", type=float, default=0.3,
                    help="scene score for a HARD cut; jump cuts/punch-ins are found separately as local spikes")
    args = ap.parse_args()
    need("ffmpeg")

    is_url = args.src.startswith(("http://", "https://"))
    name = "ref" if is_url else os.path.splitext(os.path.basename(args.src))[0]
    out = args.out or os.path.join("work", "refs", name)
    os.makedirs(os.path.join(out, "shots"), exist_ok=True)
    path = download(args.src, out) if is_url else args.src

    info = probe(path)
    dur = info["duration"]
    found = [c for c in detect_cuts(path, hard=args.threshold) if 0.2 < c["t"] < dur - 0.2]
    cuts = [c["t"] for c in found]
    kinds = {c["t"]: c["kind"] for c in found}
    # merge cuts closer than 4 frames (flash frames / transitions count once)
    merged = []
    for c in cuts:
        if not merged or c - merged[-1] > 4 / max(info.get("fps", 30), 1):
            merged.append(c)
    bounds = [0.0] + merged + [dur]
    shots = [round(b - a, 3) for a, b in zip(bounds, bounds[1:]) if b - a > 0.05]

    def cpm(lo, hi):
        n = len([c for c in merged if lo <= c < hi])
        span = max(0.001, min(hi, dur) - lo)
        return round(n / span * 60, 1)

    pacing = [{"from_s": s, "to_s": min(s + 30, round(dur)), "cuts_per_min": cpm(s, s + 30)}
              for s in range(0, int(dur), 30)]

    m = {
        "source": args.src, "file": path, "spec": {k: info.get(k) for k in
                                                   ("width", "height", "fps", "duration", "orientation")},
        "cut_threshold": args.threshold,
        "cuts": merged,
        "hard_cuts": len([c for c in merged if kinds.get(c) == "hard"]),
        "jump_cuts_or_punch_ins": len([c for c in merged if kinds.get(c) == "jump"]),
        "shot_count": len(shots),
        "avg_shot_len_s": round(statistics.mean(shots), 2) if shots else None,
        "median_shot_len_s": round(statistics.median(shots), 2) if shots else None,
        "shortest_shot_s": min(shots) if shots else None,
        "longest_shot_s": max(shots) if shots else None,
        "cuts_per_min_total": cpm(0, dur),
        "cuts_per_min_first_30s": cpm(0, 30),
        "cuts_per_min_after_30s": cpm(30, dur) if dur > 35 else None,
        "pacing_by_30s": pacing,
    }
    if info.get("has_audio"):
        m["loudness"] = loudness(path)
        m["silences_over_0_4s"] = [[round(a, 2), round(b, 2)] for a, b in silences(path, -40, 0.4)]
        m["audio_level_dbfs_per_second"] = audio_levels(path, dur)

    # palette: mid-frame of every shot, aggregated
    agg = {}
    for i, (a, b) in enumerate(zip(bounds, bounds[1:])):
        mid = (a + b) / 2
        if i < 400:
            frame_at(path, mid, os.path.join(out, "shots", f"shot_{i:03d}_{mid:07.2f}s.jpg"), width=480)
        for c in dominant_colors(path, mid, k=4):
            agg[c["hex"]] = agg.get(c["hex"], 0) + c["share"] * (b - a)
    total = sum(agg.values()) or 1
    m["palette_time_weighted"] = [{"hex": h, "share": round(v / total, 3)}
                                  for h, v in sorted(agg.items(), key=lambda kv: -kv[1])[:10]]
    m["face"] = face_share(path, dur)

    contact_sheet(path, os.path.join(out, "contact.png"), every=2.0)
    contact_sheet(path, os.path.join(out, "hook.png"), every=0.5, cols=6, width=360, end=min(15, dur))
    write_json(m, os.path.join(out, "measurements.json"))

    lines = [
        f"# Measurements: {name}", "",
        f"- Spec: {info.get('width')}x{info.get('height')} @ {info.get('fps')} fps, {dur:.1f}s ({info.get('orientation')})",
        f"- Shots: {m['shot_count']} | avg {m['avg_shot_len_s']}s | median {m['median_shot_len_s']}s "
        f"| shortest {m['shortest_shot_s']}s | longest {m['longest_shot_s']}s",
        f"- Cuts/min: total {m['cuts_per_min_total']} | first 30s {m['cuts_per_min_first_30s']} "
        f"| after 30s {m['cuts_per_min_after_30s']}",
        f"- Cut types: {m['hard_cuts']} hard cuts, {m['jump_cuts_or_punch_ins']} jump cuts / punch-ins",
        "- Pacing curve: " + ", ".join(f"{p['from_s']}-{p['to_s']}s={p['cuts_per_min']}" for p in pacing),
    ]
    if "loudness" in m:
        L = m["loudness"]
        lines.append(f"- Loudness: {L.get('integrated_lufs')} LUFS integrated, peak {L.get('true_peak_dbtp')} dBTP, "
                     f"LRA {L.get('lra_lu')} LU; silences >0.4s: {len(m['silences_over_0_4s'])}")
    lines.append("- Palette (time-weighted): " + " ".join(f"{p['hex']}({int(p['share'] * 100)}%)"
                                                         for p in m["palette_time_weighted"][:6]))
    if m["face"]:
        lines.append(f"- Face on screen: {m['face']['face_on_screen_pct']}% of samples, median face height "
                     f"{m['face']['median_face_height_pct']}% of frame")
    lines += ["", "First cuts: " + ", ".join(fmt_tc(c)[3:] for c in merged[:20]), "",
              "NEXT: open contact.png, hook.png and shots/*.jpg. Read caption font/case/size/position/words-per-line,",
              "graphic style, zoom/punch-in use, B-roll share and transitions. Then fill assets/style-card-template.md."]
    with open(os.path.join(out, "measurements.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
