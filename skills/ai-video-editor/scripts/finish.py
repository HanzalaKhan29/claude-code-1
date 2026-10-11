#!/usr/bin/env python3
"""Final mix + export: optional music bed with sidechain ducking, two-pass loudness normalisation,
platform encode presets. Writes a new file; never overwrites the input.

Usage:
  python3 finish.py <in.mp4> <out.mp4> [--platform youtube|shorts|reels|tiktok|linkedin|x|master]
                    [--music bed.mp3 --music-db -20 --duck] [--sfx sfx.json] [--denoise] [--res 2160]
                    [--music-stop 41.2 [--music-tail reverb|cut]]
--music-stop kills the music dead at that time (on the beat before a reveal); by default the last 10 frames
ring out as a ~3 s reverb tail (multi-tap echo + lowpass, -5 dB) instead of a hard stop.
sfx.json: [{"file": "whoosh.wav", "at": 12.40, "db": -6},             (starts at 12.40 s)
           {"file": "riser.wav", "end_at": 20.00, "db": -8},           (riser PEAKS on the hit frame)
           {"file": "pop.wav", "at": 21.1, "db": -14, "vary": false}]  (times on the edited timeline)
A file used more than once is pitch/speed-shifted a few percent per hit (0.94-1.08x) so repeats never sound
pasted; "vary": false keeps it identical. Text/UI pops sit 8-14 dB under impacts (20-40% level).

Loudness targets (integrated LUFS / true peak): YouTube & social -14 / -1 dBTP. Platforms normalise
down louder uploads, so mastering hotter buys nothing and costs dynamics. Speech-first content keeps music
roughly 16-25 dB under the voice; --duck lets music swell back in the gaps. Duck recovery defaults to 700 ms:
faster than ~600 ms pumps audibly, slower than ~1 s buries the start of the next phrase.
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
    ap.add_argument("--duck-release", type=int, default=700, help="duck recovery in ms (600-1000 sounds natural)")
    ap.add_argument("--music-stop", type=float, help="stop the music dead at this time (s), e.g. on the beat before "
                    "a reveal; silence is the loudest moment in the video")
    ap.add_argument("--music-tail", choices=["cut", "reverb"], default="reverb",
                    help="with --music-stop: hard cut, or a ~4 s reverb tail ringing out of the last 10 frames")
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
        if args.music_stop:
            stop = min(args.music_stop, info["duration"])
            fps = info.get("fps") or 30
            tail_start = max(0.0, stop - 10 / fps)  # the reverb is fed by the last 10 frames before the stop
            base = (f"[{m}:a]volume={args.music_db}dB,atrim=0:{stop:.3f},afade=t=in:d=1.5,"
                    f"afade=t=out:st={max(0.0, stop - 0.02):.3f}:d=0.02")
            if args.music_tail == "reverb":
                # multi-tap echo + lowpass approximates a small-room reverb (ffmpeg has no reverb filter);
                # -5 dB compensates the loudness bump of dry + wet overlapping
                chains.append(base + ",asplit=2[mdry][msrc]")
                chains.append(f"[msrc]atrim=start={tail_start:.3f},asetpts=PTS-STARTPTS,apad=pad_dur=4,"
                              "aecho=0.8:0.8:43|89|149|233|347|509|727|1013|1409|1931|2609|3407:0.55|0.47|0.41|0.35|0.3|0.26|0.22|0.18|0.14|0.1|0.07|0.04,"
                              f"lowpass=f=5000,volume=-5dB,afade=t=out:st=0.6:d=3.6,"
                              f"adelay={int(tail_start * 1000)}|{int(tail_start * 1000)}[mtail]")
                chains.append("[mdry][mtail]amix=inputs=2:normalize=0:duration=longest,"
                              f"atrim=0:{info['duration']:.3f}[mus]")
            else:
                chains.append(base + "[mus]")
        else:
            chains.append(f"[{m}:a]volume={args.music_db}dB,atrim=0:{info['duration']:.3f},"
                          f"afade=t=in:d=1.5,afade=t=out:st={max(0, info['duration'] - 2.5):.3f}:d=2.5[mus]")
        if args.duck:
            chains[0] = voice.replace("[voice]", "[v0]")
            chains.append("[v0]asplit=2[voice][sc]")
            chains.append(f"[mus][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release={args.duck_release}:makeup=1[musd]")
            mix_labels.append("[musd]")
        else:
            mix_labels.append("[mus]")
    if args.sfx:
        variations = [1.0, 0.94, 1.06, 0.97, 1.08, 0.95, 1.03]  # deterministic, so re-renders match
        seen = {}
        for k, s in enumerate(read_json(args.sfx)):
            if not os.path.exists(s["file"]):
                die(f"missing sfx file: {s['file']}")
            inputs += ["-i", s["file"]]
            n = seen.get(s["file"], 0)
            seen[s["file"]] = n + 1
            rate = variations[n % len(variations)] if s.get("vary", True) else 1.0
            sfx_dur = probe(s["file"])["duration"] / rate
            start = float(s["end_at"]) - sfx_dur if "end_at" in s else float(s["at"])
            ms = max(0, int(round(start * 1000)))
            shift = f"aresample=48000,asetrate={48000 * rate:.0f},aresample=48000," if rate != 1.0 else ""
            chains.append(f"[{n_in}:a]{shift}volume={s.get('db', -6)}dB,adelay={ms}|{ms}[sfx{k}]")
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
