#!/usr/bin/env python3
"""Plan the rough cut from a word-level transcript: drop fillers, abandoned retakes and dead air.

Usage:
  python3 plan_cuts.py <video> <words.json> [--out work/x] [--style tight|natural|loose]
                       [--keep-soft-fillers] [--no-retakes] [--drop "12.4-15.9" ...]
Writes:
  edl.json          keep-segments (source times) + everything removed with a reason
  cutlist.md        human review list: what stays, what goes and why (show this to the user)
  words_cut.json    words re-timed onto the edited timeline (feed this to captions.py)

Rules (from editors' practice):
  * cut on silence, never inside a word: boundaries snap into detected silence when possible
  * keep the LAST take of a repeated line (creators re-say a line after a mistake)
  * leave a short breath between thoughts so the edit does not feel machine-gunned
"""
import argparse
import os
import re
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, fmt_tc, loudness, probe, read_json, silences, vfr_check, write_json  # noqa: E402

HESITATION = {"sorry", "wait", "again", "redo", "restart", "hold", "on", "let", "me", "start", "over", "okay", "ok",
              "no", "actually", "uh", "um", "hmm", "one", "more", "time", "take"}
HARD_FILLERS = {"um", "umm", "uh", "uhh", "uhm", "er", "erm", "ah", "ahh", "hmm", "hm", "mm", "mmm", "eh"}
SOFT_FILLERS = {"like", "basically", "actually", "literally", "right", "okay", "so", "matlab", "toh", "na",
                "haan", "accha", "yaani", "bas"}
SOFT_PHRASES = [("you", "know"), ("i", "mean"), ("kind", "of"), ("sort", "of"), ("you", "see")]

STYLES = {  # pad_before, pad_after, max_pause, keep_pause
    "tight": (0.05, 0.08, 0.25, 0.10),     # Shorts / hype: Hormozi-style
    "natural": (0.08, 0.14, 0.40, 0.18),   # default YouTube talking head
    "loose": (0.12, 0.25, 0.80, 0.35),     # documentary / reflective
}


def norm(t):
    return re.sub(r"[^\w']+", "", t.lower())


def phrases(words, gap=0.45):
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if nxt is None or w["text"].endswith((".", "?", "!", "।")) or nxt["start"] - w["end"] >= gap:
            out.append(cur)
            cur = []
    return out


def similar_start(a_tokens, b_tokens, k=3):
    """True if phrase B restarts phrase A (same opening words, or heavy overlap)."""
    a, b = [t for t in a_tokens if t], [t for t in b_tokens if t]
    if len(a) < 2 or len(b) < 2:
        return False
    n = min(k, len(a), len(b))
    if a[:n] == b[:n]:
        return True
    head_a = a[: max(4, len(a))]
    overlap = len(set(head_a) & set(b[: len(head_a) + 3])) / len(set(head_a))
    return overlap >= 0.75 and len(head_a) >= 4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("words")
    ap.add_argument("--out", default=None)
    ap.add_argument("--style", default="natural", choices=list(STYLES))
    ap.add_argument("--keep-soft-fillers", action="store_true", default=True,
                    help="default: soft fillers (like, so, you know) are only flagged, not cut")
    ap.add_argument("--cut-soft-fillers", action="store_true", help="also cut soft fillers when isolated by pauses")
    ap.add_argument("--no-retakes", action="store_true")
    ap.add_argument("--allow-vfr", action="store_true", help="proceed on variable-frame-rate footage (drift risk)")
    ap.add_argument("--drop-silent-words", action="store_true",
                    help="drop low-confidence words that sit inside a silence (likely Whisper hallucinations)")
    ap.add_argument("--drop", action="append", default=[], help="extra source ranges to remove, e.g. 12.4-15.9")
    ap.add_argument("--pad-before", type=float, help="override the style's lead-in before each kept word (s)")
    ap.add_argument("--pad-after", type=float, help="override the style's tail after each kept word (s)")
    ap.add_argument("--max-pause", type=float, help="override the longest pause left in (s)")
    ap.add_argument("--head", type=float, default=None, help="force start time (cut everything before)")
    ap.add_argument("--tail", type=float, default=None, help="force end time (cut everything after)")
    args = ap.parse_args()

    pad_b, pad_a, max_pause, keep_pause = STYLES[args.style]
    pad_b = pad_b if args.pad_before is None else args.pad_before
    pad_a = pad_a if args.pad_after is None else args.pad_after
    max_pause = max_pause if args.max_pause is None else args.max_pause
    keep_pause = min(keep_pause, max_pause)
    out = args.out or os.path.dirname(os.path.abspath(args.words))
    os.makedirs(out, exist_ok=True)
    words = read_json(args.words)
    if isinstance(words, dict):
        words = words.get("words", [])
    pinfo = probe(args.video)
    if not args.allow_vfr and vfr_check(args.video):
        die("variable frame rate source: every frame-grid snap would drift. Re-encode first: ffmpeg -i in -vf "
            f"fps={round(pinfo.get('r_fps') or pinfo.get('fps') or 30)} -c:v libx264 -crf 16 -c:a aac cfr.mp4 "
            "(or --allow-vfr to proceed anyway)")
    dur, fps = pinfo["duration"], (pinfo.get("fps") or 30)
    # Silence threshold calibrated to this recording: about 22 dB under the speech level (a fixed -38 dB misses
    # every pause on a quiet speaker and "finds" pauses inside a music bed).
    speech = (loudness(args.video) or {}).get("integrated_lufs")
    noise_db = max(-55.0, min(-30.0, speech - 22.0)) if speech is not None else -38.0
    sil = silences(args.video, noise_db=noise_db, min_dur=0.12)

    drop = {}  # word index -> reason
    toks = [norm(w["text"]) for w in words]
    for i, t in enumerate(toks):
        if t in HARD_FILLERS:
            drop[i] = "filler"
    soft_flags = []
    for i, t in enumerate(toks):
        isolated = (i == 0 or words[i]["start"] - words[i - 1]["end"] > 0.25) and \
                   (i == len(words) - 1 or words[i + 1]["start"] - words[i]["end"] > 0.25)
        if t in SOFT_FILLERS:
            soft_flags.append(i)
            if args.cut_soft_fillers and isolated:
                drop[i] = "soft filler (isolated)"
        for a, b in SOFT_PHRASES:
            if t == a and i + 1 < len(toks) and toks[i + 1] == b:
                soft_flags += [i, i + 1]

    retakes, suspect = [], []
    if not args.no_retakes:
        ph = phrases(words)
        for pi, p in enumerate(ph):
            a = [toks[i] for i in p if i not in drop]
            for qj in range(pi + 1, min(pi + 4, len(ph))):
                b = [toks[i] for i in ph[qj] if i not in drop]
                if similar_start(a, b):
                    # The abandoned take is phrase p. Anything between it and the restart is only removed when it is
                    # hesitation ("sorry, let me redo that"); a real sentence in between means this is probably not
                    # a retake at all, so keep everything and flag it for a human instead.
                    middle = [k for pk in range(pi + 1, qj) for k in ph[pk] if k not in drop]
                    if any(toks[k] not in HESITATION and toks[k] not in SOFT_FILLERS for k in middle):
                        suspect.append({"text": " ".join(words[k]["text"] for k in p), "at": words[p[0]]["start"],
                                        "why": "looks like a restart, but real speech sits between: kept both"})
                        break
                    for pk in range(pi, qj):
                        for i in ph[pk]:
                            drop.setdefault(i, "retake (kept the later take)")
                    retakes.append({"dropped": " ".join(words[i]["text"] for i in p),
                                    "kept": " ".join(words[i]["text"] for i in ph[qj]),
                                    "at": words[p[0]]["start"]})
                    break

    for r in args.drop:
        lo, hi = (float(x) for x in r.split("-"))
        for i, w in enumerate(words):
            if w["start"] >= lo - 0.01 and w["end"] <= hi + 0.01:
                drop[i] = "manual drop"
    if args.head is not None:
        for i, w in enumerate(words):
            if w["end"] <= args.head:
                drop[i] = "before head"
    if args.tail is not None:
        for i, w in enumerate(words):
            if w["start"] >= args.tail:
                drop[i] = "after tail"

    keep_idx = [i for i in range(len(words)) if i not in drop]
    if not keep_idx:
        die("nothing left to keep: every word was dropped (check --drop/--head/--tail)")
    # Whisper invents words over silence. A low-confidence word sitting entirely inside a detected silence is a
    # hallucination suspect: flagged in cutlist.md for review (dropped only with --drop-silent-words).
    for i in keep_idx:
        w = words[i]
        if w.get("prob", 1.0) < 0.45 and any(a <= w["start"] and w["end"] <= b for a, b in sil):
            suspect.append({"text": w["text"], "at": w["start"], "why": "low-confidence word over silence (hallucination?)"})
            if args.drop_silent_words:
                drop[i] = "hallucination suspect (over silence)"
    keep_idx = [i for i in range(len(words)) if i not in drop]

    snap_stats = {"total": 0, "snapped": 0}

    def snap(t, direction):
        """Move a boundary into a nearby silence so we never clip a breath or consonant."""
        snap_stats["total"] += 1
        for a, b in sil:
            if a - 0.02 <= t <= b + 0.02:
                snap_stats["snapped"] += 1
                return t
        best = None
        for a, b in sil:
            cand = b - 0.03 if direction == "start" else a + 0.03
            if abs(cand - t) <= 0.12 and (best is None or abs(cand - t) < abs(best - t)):
                best = cand
        if best is not None:
            snap_stats["snapped"] += 1
        return best if best is not None else t

    # group kept words into runs; split a run where the pause is too long (pause compression)
    segs = []
    run_start = keep_idx[0]
    prev = keep_idx[0]
    for i in keep_idx[1:] + [None]:
        contiguous = i is not None and all(j not in drop for j in range(prev + 1, i))
        gap = (words[i]["start"] - words[prev]["end"]) if i is not None else None
        if i is not None and contiguous and gap <= max_pause:
            prev = i
            continue
        segs.append([run_start, prev])
        if i is not None:
            run_start = prev = i

    segments = []
    for k, (a, b) in enumerate(segs):
        lo_limit = words[a - 1]["end"] if a > 0 else 0.0
        hi_limit = words[b + 1]["start"] if b + 1 < len(words) else dur
        start = max(lo_limit, words[a]["start"] - pad_b)
        end = min(hi_limit, words[b]["end"] + pad_a)
        # long pause inside a thought: keep a breath (keep_pause split across both sides)
        start = max(lo_limit, min(start, words[a]["start"] - keep_pause / 2))
        end = min(hi_limit, max(end, words[b]["end"] + keep_pause / 2))
        start, end = snap(start, "start"), snap(end, "end")
        start = max(lo_limit, start)
        end = min(hi_limit, end)
        segments.append({"start": round(max(0.0, start), 3), "end": round(min(dur, end), 3),
                         "first_word": a, "last_word": b,
                         "text": " ".join(words[j]["text"] for j in range(a, b + 1) if j not in drop)})

    # merge overlaps; a short segment that holds kept words is widened to 0.25 s, never dropped (a lone "I" or
    # "no" is still speech, and dropping it would delete it from the video AND the captions)
    merged = []
    for s in segments:
        if merged and s["start"] <= merged[-1]["end"] + 0.02:
            merged[-1]["end"] = max(merged[-1]["end"], s["end"])
            merged[-1]["last_word"] = s["last_word"]
            merged[-1]["text"] += " " + s["text"]
            continue
        if s["end"] - s["start"] < 0.25:
            lo = words[s["first_word"] - 1]["end"] if s["first_word"] > 0 else 0.0
            hi = words[s["last_word"] + 1]["start"] if s["last_word"] + 1 < len(words) else dur
            need = 0.25 - (s["end"] - s["start"])
            s["start"] = max(lo, s["start"] - need / 2)
            s["end"] = min(hi, s["start"] + 0.25)
        if merged and s["start"] <= merged[-1]["end"] + 0.02:
            merged[-1]["end"] = max(merged[-1]["end"], s["end"])
            merged[-1]["last_word"] = s["last_word"]
            merged[-1]["text"] += " " + s["text"]
        else:
            merged.append(s)
    # snap to the frame grid (render_cut.py does the same), so caption times match the render exactly
    snapped = []
    for s in merged:
        a, b = round(s["start"] * fps) / fps, round(s["end"] * fps) / fps
        if b - a >= 1 / fps:
            snapped.append({**s, "start": round(a, 6), "end": round(b, 6)})
    segments = snapped

    # remap words to the edited timeline
    words_cut, offset = [], 0.0
    for s in segments:
        for j in range(s["first_word"], s["last_word"] + 1):
            if j in drop:
                continue
            w = words[j]
            words_cut.append({"text": w["text"], "start": round(offset + max(0, w["start"] - s["start"]), 3),
                              "end": round(offset + min(s["end"], w["end"]) - s["start"], 3),
                              "prob": w.get("prob", 1.0), "src_start": w["start"]})
        offset += s["end"] - s["start"]

    removed = []
    cursor = 0.0
    for s in segments + [{"start": dur, "end": dur}]:
        if s["start"] - cursor > 0.05:
            txt = " ".join(f"{words[i]['text']}" for i, w in enumerate(words)
                           if w["start"] >= cursor - 0.01 and w["end"] <= s["start"] + 0.01)
            reasons = sorted({drop[i] for i, w in enumerate(words)
                              if i in drop and w["start"] >= cursor - 0.01 and w["end"] <= s["start"] + 0.01})
            removed.append({"start": round(cursor, 3), "end": round(s["start"], 3),
                            "reason": ", ".join(reasons) or "silence / dead air", "text": txt})
        cursor = s["end"]

    new_dur = round(sum(s["end"] - s["start"] for s in segments), 2)
    edl = {"source": os.path.abspath(args.video), "style": args.style, "source_duration": round(dur, 2),
           "edited_duration": new_dur, "removed_seconds": round(dur - new_dur, 2),
           "segments": [{"start": s["start"], "end": s["end"], "text": s["text"]} for s in segments],
           "removed": removed, "retakes": retakes, "review": suspect,
           "silence_threshold_db": round(noise_db, 1), "boundaries_snapped": snap_stats,
           "soft_fillers_flagged": sorted({words[i]["start"] for i in soft_flags})}
    write_json(edl, os.path.join(out, "edl.json"))
    write_json(words_cut, os.path.join(out, "words_cut.json"))

    lines = [f"# Rough cut plan ({args.style})", "",
             f"Source {dur:.1f}s -> edit {new_dur:.1f}s (removed {dur - new_dur:.1f}s, "
             f"{len(segments)} segments, {len(retakes)} retakes, "
             f"{sum(1 for r in drop.values() if r == 'filler')} fillers)", "", "## Removed (review these)"]
    for r in removed:
        lines.append(f"- {fmt_tc(r['start'])[3:]}-{fmt_tc(r['end'])[3:]} ({r['end'] - r['start']:.2f}s) "
                     f"[{r['reason']}] {r['text'][:120]}")
    if retakes:
        lines += ["", "## Retakes (kept the later version)"]
        for r in retakes:
            lines.append(f"- @{r['at']:.1f}s dropped: \"{r['dropped'][:90]}\" -> kept: \"{r['kept'][:90]}\"")
    if soft_flags:
        lines += ["", f"## Soft fillers flagged but kept ({len(set(soft_flags))}): decide per case "
                      "(`--cut-soft-fillers` or `--drop a-b`)"]
    if suspect:
        lines += ["", "## Review these (not decided automatically)"]
        for r in suspect:
            lines.append(f"- @{r['at']:.1f}s \"{r['text'][:90]}\": {r['why']}")
    kept_words = len([i for i in range(len(words)) if i not in drop])
    lines += ["", f"Checks: silence threshold {noise_db:.0f} dB (calibrated to speech), "
                  f"{snap_stats['snapped']}/{snap_stats['total']} boundaries landed in silence, "
                  f"{len(words_cut)}/{kept_words} kept words placed on the edited timeline."]
    if kept_words != len(words_cut):
        lines.append(f"WARNING: {kept_words - len(words_cut)} kept word(s) are missing from words_cut.json. "
                     "Do not render: report this as a bug.")
    if snap_stats["total"] and snap_stats["snapped"] / snap_stats["total"] < 0.5:
        lines.append("WARNING: under half the cut points found a silence (music bed, noisy room or wrong threshold). "
                     "Cuts may clip breaths or consonants: listen to every join, consider --style loose.")
    with open(os.path.join(out, "cutlist.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines[:4]))
    for ln in lines:
        if ln.startswith(("WARNING", "Checks")):
            print(ln)
    print(f"Wrote {out}/edl.json, cutlist.md, words_cut.json")


if __name__ == "__main__":
    main()
