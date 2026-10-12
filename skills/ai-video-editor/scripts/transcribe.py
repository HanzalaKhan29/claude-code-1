#!/usr/bin/env python3
"""Word-level transcription with automatic engine fallback.

Order: mlx-whisper (Apple Silicon) -> faster-whisper -> openai-whisper -> `npx hyperframes transcribe`.
Output (HyperFrames-compatible): <out>/words.json = flat list [{"text","start","end","prob"}],
plus <out>/transcript.txt (one sentence per line with timecodes).

Usage:
  python3 transcribe.py <video-or-audio> [--out work/x] [--model large-v3-turbo] [--language en|hi|auto]
                        [--prompt "Names, jargon, brand words"] [--verbatim]
--verbatim primes Whisper to keep fillers (um, uh, like) so they can be cut. Without it Whisper
often silently drops disfluencies and the filler cut misses them.
--device auto runs the GPU attempt in a child process: a CUDA/cuDNN crash (which can kill the process outright)
falls back to CPU int8 instead of ending the job. --device cpu skips the GPU entirely.
Word starts are refined against the audio by default: Whisper often starts a word up to ~200 ms early (in the
silence before it), which makes captions and graphics land early. Each start moves forward to the first 10 ms
frame within 24 dB of that word's own peak (forward only, at most 250 ms). The raw time stays in "start_raw".
--no-refine turns it off.
"""
import argparse
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, fmt_tc, need, read_json, run, write_json  # noqa: E402

VERBATIM_PROMPT = "Umm, let me think like, hmm... Okay, so, uh, I mean, you know, it's like, basically, right?"


def extract_audio(src, wav):
    need("ffmpeg")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000",
         "-c:a", "pcm_s16le", wav])
    return wav


def norm_words(raw):
    words = []
    for w in raw:
        text = (w.get("word") or w.get("text") or "").strip()
        if not text:
            continue
        words.append({"text": text, "start": round(float(w["start"]), 3), "end": round(float(w["end"]), 3),
                      "prob": round(float(w.get("probability", w.get("prob", 1.0)) or 1.0), 3)})
    # enforce monotonic, non-overlapping timings
    for a, b in zip(words, words[1:]):
        if b["start"] < a["end"]:
            mid = round((a["end"] + b["start"]) / 2, 3)
            a["end"], b["start"] = mid, mid
    return words


def via_mlx(wav, model, language, prompt):
    import mlx_whisper  # noqa: WPS433
    repo = model if "/" in model else f"mlx-community/whisper-{model}"
    res = mlx_whisper.transcribe(wav, path_or_hf_repo=repo, word_timestamps=True,
                                 language=None if language == "auto" else language, initial_prompt=prompt)
    return norm_words([w for s in res.get("segments", []) for w in s.get("words", [])]), res.get("language")


def via_faster(wav, model, language, prompt, device="cpu"):
    from faster_whisper import WhisperModel  # noqa: WPS433
    m = WhisperModel(model, device=device, compute_type="int8" if device == "cpu" else "auto")
    segs, info = m.transcribe(wav, word_timestamps=True, language=None if language == "auto" else language,
                              initial_prompt=prompt, vad_filter=False, condition_on_previous_text=False)
    raw = [{"word": w.word, "start": w.start, "end": w.end, "probability": w.probability}
           for s in segs for w in (s.words or [])]
    return norm_words(raw), info.language


def cuda_devices():
    try:
        import ctranslate2  # noqa: WPS433
        return ctranslate2.get_cuda_device_count()
    except Exception:  # no ctranslate2 or a broken CUDA install
        return 0


def via_faster_safe(wav, args, prompt, out):
    """GPU first in a CHILD process (a cuDNN/cuBLAS crash can abort the whole interpreter), CPU int8 after."""
    if args.device == "cpu" or (args.device == "auto" and cuda_devices() == 0):
        return via_faster(wav, args.model, args.language, prompt, "cpu")
    if args.device == "cuda":
        return via_faster(wav, args.model, args.language, prompt, "cuda")
    child_out = os.path.join(out, "gpu-attempt")
    cmd = [sys.executable, os.path.abspath(__file__), wav, "--out", child_out, "--engine", "faster",
           "--device", "cuda", "--model", args.model, "--language", args.language, "--no-refine"]
    if prompt:
        cmd += ["--raw-prompt", prompt]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    words_file = os.path.join(child_out, "words.json")
    if proc.returncode == 0 and os.path.exists(words_file):
        meta = read_json(os.path.join(child_out, "transcribe-meta.json"))
        return read_json(words_file), meta.get("language")
    last = (proc.stderr.strip().splitlines() or [f"exit code {proc.returncode}"])[-1]
    print(f"WARN: GPU transcription crashed ({last[:160]}). Falling back to CPU int8 (slower, same words). "
          f"Use --device cpu next time on this machine.", file=sys.stderr)
    return via_faster(wav, args.model, args.language, prompt, "cpu")


def envelope(wav):
    """RMS level in dB for every 10 ms of a 16 kHz mono wav (one ffmpeg pass, no numpy)."""
    proc = run(["ffmpeg", "-hide_banner", "-nostats", "-i", wav, "-af",
                "asetnsamples=n=160:p=0,astats=metadata=1:reset=1,"
                "ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-", "-f", "null", "-"], check=False)
    env = []
    for line in proc.stdout.splitlines():
        if "RMS_level=" in line:
            v = line.split("=", 1)[1].strip()
            env.append(-120.0 if v in ("-inf", "nan") else float(v))
    return env


def refine_onsets(words, env, step=0.01, below_peak=24.0, max_shift=0.25):
    moved = 0
    for i, w in enumerate(words):
        a, b = int(w["start"] / step), int(w["end"] / step)
        seg = env[a:b + 1]
        if len(seg) < 3:
            continue
        peak = max(seg)
        lim = min(len(seg), int(max_shift / step) + 1)
        onset = next((k for k in range(lim) if seg[k] >= peak - below_peak), 0)
        new = round(max(w["start"], (a + onset) * step - 0.01), 3)
        if new - w["start"] >= 0.04 and new < w["end"] - 0.05:
            w["start_raw"], w["start"] = w["start"], new
            moved += 1
    return moved


def via_openai(wav, model, language, prompt):
    import whisper  # noqa: WPS433
    name = model.replace("large-v3-turbo", "turbo")
    m = whisper.load_model(name)
    res = m.transcribe(wav, word_timestamps=True, language=None if language == "auto" else language,
                       initial_prompt=prompt, condition_on_previous_text=False)
    return norm_words([w for s in res.get("segments", []) for w in s.get("words", [])]), res.get("language")


def via_hyperframes(wav, model, language, out):
    if not shutil.which("npx"):
        raise RuntimeError("npx not found")
    hf_model = "small.en" if language in ("en", "auto") and model.startswith(("small", "base", "tiny")) else "small"
    tmp = os.path.join(out, "hf-transcribe")
    os.makedirs(tmp, exist_ok=True)
    subprocess.run(["npx", "--yes", "hyperframes@latest", "transcribe", wav, "-d", tmp, "--json", "--model", hf_model],
                   check=True)
    data = read_json(os.path.join(tmp, "transcript.json"))
    if isinstance(data, dict):
        data = data.get("words", [])
    return norm_words([w for w in data if w.get("type", "word") == "word"]), language


def sentences(words, gap=0.6):
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_punct = w["text"].endswith((".", "?", "!", "।"))
        if nxt is None or end_punct or nxt["start"] - w["end"] > gap:
            out.append(cur)
            cur = []
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--out", default=None)
    ap.add_argument("--model", default="large-v3-turbo",
                    help="large-v3-turbo (best speed/quality), medium, small; use large-v3 for Hindi/Hinglish")
    ap.add_argument("--language", default="auto")
    ap.add_argument("--prompt", default="", help="names/jargon so Whisper spells them right")
    ap.add_argument("--verbatim", action="store_true", help="keep fillers (um/uh/like) for the filler cut")
    ap.add_argument("--engine", default="auto", choices=["auto", "mlx", "faster", "openai", "hyperframes"])
    ap.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"],
                    help="faster-whisper device; auto tries the GPU in a child process and falls back to CPU")
    ap.add_argument("--no-refine", action="store_true", help="keep Whisper's raw word start times")
    ap.add_argument("--raw-prompt", default=None, help=argparse.SUPPRESS)  # internal: GPU child process
    args = ap.parse_args()

    out = args.out or os.path.join("work", os.path.splitext(os.path.basename(args.src))[0])
    os.makedirs(out, exist_ok=True)
    wav = extract_audio(args.src, os.path.join(out, "audio16k.wav"))
    prompt = args.raw_prompt or " ".join(p for p in [VERBATIM_PROMPT if args.verbatim else "", args.prompt] if p) \
        or None

    order = []
    arm_mac = platform.system() == "Darwin" and platform.machine() == "arm64"
    if args.engine in ("auto", "mlx") and arm_mac and importlib.util.find_spec("mlx_whisper"):
        order.append(("mlx-whisper", lambda: via_mlx(wav, args.model, args.language, prompt)))
    if args.engine in ("auto", "faster") and importlib.util.find_spec("faster_whisper"):
        order.append(("faster-whisper", lambda: via_faster_safe(wav, args, prompt, out)))
    if args.engine in ("auto", "openai") and importlib.util.find_spec("whisper"):
        order.append(("openai-whisper", lambda: via_openai(wav, args.model, args.language, prompt)))
    if args.engine in ("auto", "hyperframes"):
        order.append(("hyperframes", lambda: via_hyperframes(wav, args.model, args.language, out)))

    words, lang, used, errors = None, None, None, []
    for name, fn in order:
        try:
            print(f"Transcribing with {name} ({args.model})...", file=sys.stderr)
            words, lang = fn()
            used = name
            break
        except Exception as e:  # engine missing model / runtime error -> try next
            errors.append(f"{name}: {e}")
            print(f"  {name} failed: {e}", file=sys.stderr)
    if not words:
        die("no transcription engine worked. Run doctor.py. Errors:\n" + "\n".join(errors))

    moved = 0 if args.no_refine else refine_onsets(words, envelope(wav))
    write_json(words, os.path.join(out, "words.json"))
    sents = sentences(words)
    with open(os.path.join(out, "transcript.txt"), "w", encoding="utf-8") as f:
        for s in sents:
            f.write(f"[{fmt_tc(s[0]['start'])} - {fmt_tc(s[-1]['end'])}] {' '.join(w['text'] for w in s)}\n")
    low = [w for w in words if w["prob"] < 0.5]
    meta = {"engine": used, "model": args.model, "language": lang, "words": len(words),
            "duration_spoken_s": round(words[-1]["end"] - words[0]["start"], 2),
            "wpm": round(len(words) / max(0.1, (words[-1]["end"] - words[0]["start"]) / 60), 1),
            "low_confidence_words": len(low), "onsets_refined": moved}
    write_json(meta, os.path.join(out, "transcribe-meta.json"))
    print(json.dumps(meta))
    if low:
        print("Check these low-confidence words (names/jargon?): " +
              ", ".join(f"{w['text']}@{w['start']}" for w in low[:25]), file=sys.stderr)
    print(f"Wrote {out}/words.json and transcript.txt. Fix misspelled names in words.json (keep timings).",
          file=sys.stderr)


if __name__ == "__main__":
    main()
