#!/usr/bin/env python3
"""Final mix + export: optional music bed with sidechain ducking, two-pass loudness normalisation,
platform encode presets. Writes a new file; never overwrites the input.

Usage:
  python3 finish.py <in.mp4> <out.mp4> [--platform youtube|shorts|reels|tiktok|linkedin|x|master]
                    [--music bed.mp3 --music-db -20 --duck] [--sfx sfx.json] [--denoise] [--res 2160]
sfx.json: [{"file": "whoosh.wav", "at": 12.40, "db": -6}, ...]  (times on the edited timeline)

Loudness targets (integrated LUFS / true peak): YouTube & social -14 / -1 dBTP. Platforms normalise
down louder uploads, so mastering hotter buys nothing and costs dynamics. Speech-first content keeps music
roughly 18-25 dB under the voice; --duck lets music swell back in the gaps.
"""
import argparse
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, need, probe, read_json, run  # noqa: E402

PRESETS = {  # target LUFS, true peak, video bitrate hint (Mbps @1080p SDR), max fps
    "youtube": (-14, -1.0, 12), "shorts": (-14, -1.0, 12), "reels": (-14, -1.0, 10),
    "tiktok": (-14, -1.0, 10), "linkedin": (-14, -1.0, 8), "x": (-14, -1.0, 8), "master": (-14, -1.0, 20),
}


def measure(path, af_chain, target, tp):
    proc = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-filter_complex",
                f"{af_chain}loudnorm=I={target}:TP={tp}:LRA=11:print_format=json", "-f", "null", "-"], check=False)
    txt = proc.stderr
    j = txt[txt.rfind("{"): txt.rfind("}") + 1]
    try:
        return json.loads(j)
    except json.JSONDecodeError:
        die("loudness measurement failed:\n" + txt[-1500:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("out")
    ap.add_argument("--platform", default="youtube", choices=list(PRESETS))
    ap.add_argument("--music")
    ap.add_argument("--music-db", type=float, default=-20.0, help="music level before ducking")
    ap.add_argument("--duck", action="store_true", help="sidechain-duck music under the voice")
    ap.add_argument("--sfx", help="json list of sound effects to place")
    ap.add_argument("--denoise", action="store_true", help="light FFT denoise + high-pass on voice (afftdn)")
    ap.add_argument("--res", type=int, help="output height, e.g. 2160 to upload 4K (YouTube gives 4K uploads a "
                                            "higher-bitrate codec; helps 1080p detail on big screens)")
    ap.add_argument("--crf", type=int, default=17)
    args = ap.parse_args()
    need("ffmpeg")
    if os.path.abspath(args.inp) == os.path.abspath(args.out):
        die("output must be a new file")
    info = probe(args.inp)
    target, tp, _ = PRESETS[args.platform]

    inputs = ["-i", args.inp]
    voice = "[0:a]highpass=f=70" + (",afftdn=nf=-25" if args.denoise else "") + "[voice]"
    chains = [voice]
    mix_labels = ["[voice]"]
    n_in = 1
    if args.music:
        inputs += ["-stream_loop", "-1", "-i", args.music]
        m = n_in
        n_in += 1
        chains.append(f"[{m}:a]volume={args.music_db}dB,atrim=0:{info['duration']:.3f},"
                      f"afade=t=in:d=1.5,afade=t=out:st={max(0, info['duration'] - 2.5):.3f}:d=2.5[mus]")
        if args.duck:
            chains[0] = voice.replace("[voice]", "[v0]")
            chains.append("[v0]asplit=2[voice][sc]")
            chains.append("[mus][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350:makeup=1[musd]")
            mix_labels.append("[musd]")
        else:
            mix_labels.append("[mus]")
    if args.sfx:
        for k, s in enumerate(read_json(args.sfx)):
            inputs += ["-i", s["file"]]
            ms = int(float(s["at"]) * 1000)
            chains.append(f"[{n_in}:a]volume={s.get('db', -6)}dB,adelay={ms}|{ms}[sfx{k}]")
            mix_labels.append(f"[sfx{k}]")
            n_in += 1
    if len(mix_labels) > 1:
        chains.append("".join(mix_labels) + f"amix=inputs={len(mix_labels)}:normalize=0:duration=first[pre]")
    else:
        chains[-1] = chains[-1].replace("[voice]", "[pre]")
    graph = ";".join(chains)

    # pass 1: measure the mixed result; pass 2: linear normalisation with measured values
    pre_path = args.out + ".premix.wav"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"] + inputs +
        ["-filter_complex", graph, "-map", "[pre]", "-ar", "48000", pre_path])
    m = measure(pre_path, "", target, tp)
    ln = (f"loudnorm=I={target}:TP={tp}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:"
          "linear=true:print_format=summary")

    vf = []
    if args.res and args.res != info.get("height"):
        vf.append(f"scale=-2:{args.res}:flags=lanczos")
    fps = round(info["fps"]) or 30
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostats", "-y", "-i", args.inp, "-i", pre_path,
           "-map", "0:v", "-map", "1:a", "-af", f"{ln},aresample=48000"]
    if vf:
        cmd += ["-vf", ",".join(vf)]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", str(args.crf), "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-g", str(fps * 2), "-bf", "2", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", args.out]
    if subprocess.run(cmd).returncode != 0:
        die("final encode failed")
    os.remove(pre_path)
    print(f"Finished {args.out} for {args.platform}: target {target} LUFS / {tp} dBTP. "
          f"Verify with: python3 qa.py {args.out}")


if __name__ == "__main__":
    main()
