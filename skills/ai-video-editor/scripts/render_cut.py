#!/usr/bin/env python3
"""Render an EDL (from plan_cuts.py) to a new video. Never touches the original file.

Usage:
  python3 render_cut.py <edl.json> <out.mp4> [--punch 1.08] [--punch-center 0.5,0.4]
                        [--fade-ms 20] [--crf 18] [--preview]
--punch      alternate segments get a punch-in (scale factor) to disguise jump cuts.
             Keep <=1.12 on 1080p sources, up to ~1.5 on 4K.
--punch-center  focus point as fractions of width,height (usually the face; default 0.5,0.4)
--preview    fast 540p render for review rounds
Audio gets a few-ms fade at every boundary so cuts never click. Video keyframes every 1s
(-g = fps) so HyperFrames and editors can seek it frame-accurately.
"""
import argparse
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, need, probe, read_json, run  # noqa: E402

CHUNK = 60  # segments per filtergraph chunk (keeps ffmpeg graphs small on long videos)


def snap(segs, fps):
    """Snap boundaries to the frame grid so video (whole frames) and audio (samples) stay the same length.
    Without this every segment rounds differently and A/V drift accumulates over hundreds of cuts."""
    out = []
    for s in segs:
        a, b = round(s["start"] * fps) / fps, round(s["end"] * fps) / fps
        if b - a >= 1 / fps:
            out.append({**s, "start": a, "end": b})
    return out


def build_graph(segs, info, punch, center, fade_s, scale_to, index_offset=0, video=True, audio=True):
    w, h = info["width"], info["height"]
    tw, th = scale_to
    parts, labels = [], []
    has_a = info.get("has_audio") and audio
    for i, s in enumerate(segs):
        a, b = s["start"], s["end"]
        lab = ""
        if not video:
            pass
        else:
            v = f"[0:v]trim=start={a:.6f}:end={b:.6f},setpts=PTS-STARTPTS"
            if punch and punch > 1.0 and (i + index_offset) % 2 == 1:
                cw, ch = int(w / punch) // 2 * 2, int(h / punch) // 2 * 2
                cx = min(max(0, int(w * center[0] - cw / 2)), w - cw)
                cy = min(max(0, int(h * center[1] - ch / 2)), h - ch)
                v += f",crop={cw}:{ch}:{cx}:{cy}"
            v += f",scale={tw}:{th}:flags=lanczos,setsar=1,format=yuv420p[v{i}]"
            parts.append(v)
            lab = f"[v{i}]"
        if has_a:
            d = b - a
            fd = min(fade_s, d / 4)
            parts.append(f"[0:a]atrim=start={a:.6f}:end={b:.6f},asetpts=PTS-STARTPTS,"
                         f"afade=t=in:st=0:d={fd:.3f},afade=t=out:st={max(0, d - fd):.3f}:d={fd:.3f}[a{i}]")
            lab += f"[a{i}]"
        labels.append(lab)
    n = len(segs)
    outs = ("[v]" if video else "") + ("[a]" if has_a else "")
    parts.append("".join(labels) + f"concat=n={n}:v={1 if video else 0}:a={1 if has_a else 0}" + outs)
    return ";".join(parts)


def encode(src, graph, out, info, crf, preview, has_a):
    fps = round(info["fps"]) or 30
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostats", "-y", "-i", src,
           "-filter_complex", graph, "-map", "[v]", "-fps_mode", "cfr"]
    if has_a:
        cmd += ["-map", "[a]", "-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast" if preview else "medium", "-crf", str(28 if preview else crf),
            "-g", str(fps), "-keyint_min", str(fps), "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            "-movflags", "+faststart", out]
    proc = subprocess.run(cmd)
    if proc.returncode != 0:
        die("ffmpeg render failed (see log above)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edl")
    ap.add_argument("out")
    ap.add_argument("--punch", type=float, default=0.0)
    ap.add_argument("--punch-center", default="0.5,0.4")
    ap.add_argument("--fade-ms", type=float, default=20)
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()
    need("ffmpeg")

    edl = read_json(args.edl)
    src = edl["source"]
    if os.path.abspath(args.out) == os.path.abspath(src):
        die("refusing to overwrite the source footage; pick a new output name (v1, v2, ...)")
    info = probe(src)
    segs = snap(edl["segments"], info["fps"] or 30)
    if not segs:
        die("EDL has no segments")
    center = tuple(float(x) for x in args.punch_center.split(","))
    w, h = info["width"], info["height"]
    scale_to = (w, h)
    if args.preview:
        f = 540 / min(w, h)
        scale_to = (int(w * f) // 2 * 2, int(h * f) // 2 * 2)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)

    if len(segs) <= CHUNK:
        encode(src, build_graph(segs, info, args.punch, center, args.fade_ms / 1000, scale_to),
               args.out, info, args.crf, args.preview, info.get("has_audio"))
    else:
        # Long edits: video in chunks (small graphs), audio in ONE pass. Concatenating separately encoded
        # AAC chunks adds priming samples at every join (measured ~10 ms per join), so audio is never chunked.
        tmpdir = tempfile.mkdtemp(prefix="cut_")
        parts = []
        for k in range(0, len(segs), CHUNK):
            chunk = segs[k:k + CHUNK]
            p = os.path.join(tmpdir, f"part_{k // CHUNK:03d}.mp4")
            graph = build_graph(chunk, info, args.punch, center, args.fade_ms / 1000, scale_to, index_offset=k,
                                audio=False)
            encode(src, graph, p, info, args.crf, args.preview, False)
            parts.append(p)
        lst = os.path.join(tmpdir, "list.txt")
        with open(lst, "w") as f:
            for p in parts:
                f.write(f"file '{p}'\n")
        video_only = os.path.join(tmpdir, "video.mp4")
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
             "-c", "copy", video_only])
        if info.get("has_audio"):
            wav = os.path.join(tmpdir, "audio.wav")
            agraph = build_graph(segs, info, 0, center, args.fade_ms / 1000, scale_to, video=False)
            run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-filter_complex", agraph,
                 "-map", "[a]", "-c:a", "pcm_s16le", "-ar", "48000", wav])
            run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", video_only, "-i", wav, "-map", "0:v",
                 "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", args.out])
        else:
            run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", video_only, "-c", "copy",
                 "-movflags", "+faststart", args.out])
    out_info = probe(args.out)
    print(f"Rendered {args.out}: {out_info['duration']:.2f}s (EDL expected {edl['edited_duration']:.2f}s), "
          f"{out_info.get('width')}x{out_info.get('height')}")
    drift = abs(out_info["duration"] - edl["edited_duration"])
    if drift > 0.25:
        print(f"WARN: duration drift {drift:.2f}s vs EDL; check captions sync (re-time from the render).")


if __name__ == "__main__":
    main()
