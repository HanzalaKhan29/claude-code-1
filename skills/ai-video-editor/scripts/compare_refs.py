#!/usr/bin/env python3
"""Turn several measured reference videos into one consensus style (what the creator ALWAYS does vs once).

Usage:
  python3 compare_refs.py work/refs/creator/* --out work/refs/creator
Reads each folder's measurements.json (from analyze_reference.py / top_refs.py) and writes
consensus.json + consensus.md: median, range and agreement count per metric, plus the shared palette.
A rule is CONSISTENT when at least 60% of the videos sit within +/-25% of the median (or share the palette
colour). Anything else is VARIES: do not put it in the style card as a rule; note it as a per-video choice.
"""
import argparse
import glob
import json
import os
import statistics
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, write_json  # noqa: E402

METRICS = [  # (key or callable, label, unit)
    ("duration", "Duration", "s"),
    ("avg_shot_len_s", "Average shot length", "s"),
    ("median_shot_len_s", "Median shot length", "s"),
    ("cuts_per_min_total", "Cuts per minute (whole)", "/min"),
    ("cuts_per_min_first_30s", "Cuts per minute (first 30 s)", "/min"),
    ("jump_share", "Share of cuts that are jump cuts / punch-ins", ""),
    ("lufs", "Integrated loudness", "LUFS"),
    ("lra", "Loudness range", "LU"),
    ("pauses_per_min", "Pauses >0.4 s per minute", "/min"),
    ("face_share", "Face on screen", "%"),
]


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def close(a, b, tol=48):
    return sum((x - y) ** 2 for x, y in zip(hex_rgb(a), hex_rgb(b))) ** 0.5 <= tol


def flatten(m):
    dur = (m.get("spec") or {}).get("duration") or 0
    cuts = (m.get("hard_cuts") or 0) + (m.get("jump_cuts_or_punch_ins") or 0)
    face = m.get("face") or {}
    return {
        "duration": dur or None,
        "avg_shot_len_s": m.get("avg_shot_len_s"),
        "median_shot_len_s": m.get("median_shot_len_s"),
        "cuts_per_min_total": m.get("cuts_per_min_total"),
        "cuts_per_min_first_30s": m.get("cuts_per_min_first_30s"),
        "jump_share": round(m["jump_cuts_or_punch_ins"] / cuts, 2) if cuts else None,
        "lufs": (m.get("loudness") or {}).get("integrated_lufs"),
        "lra": (m.get("loudness") or {}).get("lra_lu"),
        "pauses_per_min": round(len(m.get("silences_over_0_4s") or []) / (dur / 60), 1) if dur else None,
        "face_share": face.get("face_on_screen_pct") if isinstance(face, dict) else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folders", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--agree", type=float, default=0.6, help="share of videos that must agree for CONSISTENT")
    args = ap.parse_args()
    files = []
    for f in args.folders:
        files += glob.glob(os.path.join(f, "measurements.json")) if os.path.isdir(f) else []
    if len(files) < 2:
        die("need measurements from at least 2 videos (one video cannot separate style from a one-off choice)")
    data = []
    for f in sorted(files):
        with open(f, encoding="utf-8") as fh:
            m = json.load(fh)
        data.append((os.path.basename(os.path.dirname(f)), m, flatten(m)))
    n = len(data)
    need_n = max(2, -(-int(args.agree * n * 100) // 100))

    rows = []
    for key, label, unit in METRICS:
        vals = [(name, flat[key]) for name, _, flat in data if flat.get(key) is not None]
        if len(vals) < 2:
            continue
        nums = [v for _, v in vals]
        med = statistics.median(nums)
        tol = max(abs(med) * 0.25, 0.05 if unit == "" else 0.5)
        agree = sum(1 for v in nums if abs(v - med) <= tol)
        rows.append({"metric": label, "unit": unit, "median": round(med, 2), "min": round(min(nums), 2),
                     "max": round(max(nums), 2), "videos": len(nums), "agree": agree,
                     "verdict": "CONSISTENT" if agree >= need_n else "VARIES"})

    # palette: a colour counts when it appears (within tolerance) in the top 4 of enough videos
    tops = [[p["hex"] for p in (m.get("palette_time_weighted") or [])[:4]] for _, m, _ in data]
    shared = []
    for hexes in tops:
        for h in hexes:
            if any(close(h, s["hex"]) for s in shared):
                continue
            count = sum(1 for other in tops if any(close(h, o) for o in other))
            if count >= need_n:
                shared.append({"hex": h, "videos": count})
    shared.sort(key=lambda s: -s["videos"])

    os.makedirs(args.out, exist_ok=True)
    write_json({"videos": [name for name, _, _ in data], "agreement_needed": need_n, "metrics": rows,
                "shared_palette": shared}, os.path.join(args.out, "consensus.json"))
    lines = [f"# Consensus across {n} reference videos", "",
             f"A rule is CONSISTENT when at least {need_n} of {n} videos sit within 25% of the median.", "",
             "| Metric | Median | Range | Agree | Verdict |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['metric']} | {r['median']} {r['unit']} | {r['min']} - {r['max']} | "
                     f"{r['agree']}/{r['videos']} | {r['verdict']} |")
    lines += ["", "Shared palette (in the top 4 colours of enough videos): " +
              (", ".join(f"{s['hex']} ({s['videos']}/{n})" for s in shared) or "none: colour varies per video"),
              "", "Numbers cannot read captions, fonts, graphics or hooks. Open each video's hook.png and "
              "shots/ and check those by eye across the set: same rule (2+ videos) or a one-off."]
    with open(os.path.join(args.out, "consensus.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
