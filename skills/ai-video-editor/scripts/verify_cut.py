#!/usr/bin/env python3
"""Second listening pass: transcribe the RENDER and diff it against the words you meant to keep.

Catches what frame checks cannot: clipped word starts/ends, "ghost" syllables from a cut landing inside a
word, missing words, and audio drifting against the planned timeline (lip-sync or caption sync problems).

Usage:
  python3 verify_cut.py <render.mp4> <words_cut.json> [--render-words render_words.json] [--model small]
--render-words skips transcription if you already transcribed the render (transcribe.py --out ...).
Exit code 1 when problems are found, so it can gate delivery; 2 when no ASR engine is available.
"""
import argparse
import difflib
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_json, write_json  # noqa: E402


def norm(t):
    return re.sub(r"[^\w']+", "", t.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("render")
    ap.add_argument("planned")
    ap.add_argument("--render-words")
    ap.add_argument("--model", default=None, help="default: the model recorded in transcribe-meta.json next to "
                    "the planned words (same model both passes, or model disagreement looks like cut errors)")
    ap.add_argument("--language", default="auto")
    ap.add_argument("--drift-ms", type=float, default=250,
                    help="flag words whose timing moved more than this (Whisper's own word timing jitters ~200 ms)")
    args = ap.parse_args()

    planned = read_json(args.planned)
    if args.model is None:
        meta_dir = os.path.dirname(os.path.abspath(args.planned))
        for cand in (meta_dir, os.path.dirname(meta_dir)):
            mp = os.path.join(cand, "transcribe-meta.json")
            if os.path.exists(mp):
                args.model = read_json(mp).get("model")
                break
        args.model = args.model or "large-v3-turbo"
    if args.render_words:
        heard = read_json(args.render_words)
    else:
        out = os.path.join(os.path.dirname(os.path.abspath(args.render)), "verify")
        here = os.path.dirname(os.path.abspath(__file__))
        proc = subprocess.run([sys.executable, "-I", os.path.join(here, "transcribe.py"), args.render, "--out", out,
                               "--model", args.model, "--language", args.language, "--verbatim"])
        if proc.returncode != 0 or not os.path.exists(os.path.join(out, "words.json")):
            print("verify_cut: no transcription engine worked, so the ASR diff cannot run. Fall back to: "
                  "qa.py <render> --edl edl.json (cuts.png + click check), then LISTEN to every join. "
                  "Do not report the cut as verified.")
            sys.exit(2)
        heard = read_json(os.path.join(out, "words.json"))

    a = [norm(w["text"]) for w in planned]
    b = [norm(w["text"]) for w in heard]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    problems, drifts = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                d = (heard[j1 + k]["start"] - planned[i1 + k]["start"]) * 1000
                if abs(d) > args.drift_ms:
                    drifts.append({"word": planned[i1 + k]["text"], "planned": planned[i1 + k]["start"],
                                   "heard": heard[j1 + k]["start"], "drift_ms": round(d)})
            continue
        problems.append({
            "type": {"delete": "missing in render", "insert": "extra/ghost in render", "replace": "changed"}[tag],
            "planned": " ".join(w["text"] for w in planned[i1:i2]),
            "heard": " ".join(w["text"] for w in heard[j1:j2]),
            "at": round((heard[j1]["start"] if j1 < len(heard) else (planned[i1]["start"] if i1 < len(planned)
                                                                   else 0)), 2),
        })
    match = sm.ratio()
    report = {"match_ratio": round(match, 3), "problems": problems, "timing_drifts": drifts[:50]}
    write_json(report, os.path.splitext(args.render)[0] + ".verify.json")
    print(f"Word match {match:.1%}; {len(problems)} differences; {len(drifts)} words drifted > {args.drift_ms:.0f} ms")
    for p in problems[:25]:
        print(f"  @{p['at']}s {p['type']}: planned '{p['planned']}' heard '{p['heard']}'")
    if drifts:
        worst = max(drifts, key=lambda d: abs(d["drift_ms"]))
        print(f"  worst drift: '{worst['word']}' {worst['drift_ms']} ms (planned {worst['planned']}s)")
    print("ASR is imperfect: listen at each flagged time before re-cutting. Real clipped words usually show as "
          "'changed' or 'missing' right next to a cut point.")
    print("Note: this pass re-runs the same kind of speech model, so it cannot catch words both passes mishear or "
          "invent. It catches gross render damage (clipped, missing, doubled words). Still listen to every join.")
    sys.exit(1 if problems or len(drifts) > 3 else 0)


if __name__ == "__main__":
    main()
