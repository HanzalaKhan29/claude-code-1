#!/usr/bin/env python3
"""Reframe 16:9 footage to 9:16 (or 4:5 / 1:1) for Shorts, Reels and TikTok.

Usage:
  python3 reframe.py <in.mp4> <out.mp4> [--aspect 9:16] [--mode crop|blurfit] [--x 0.5] [--window 6]
crop     face-centred crop. With opencv-python installed, the face is found per section (default 6 s) and the
         crop holds still inside a section and hard-cuts between sections: a static frame per thought reads as
         intentional; slow auto-pans driven by noisy face detection look like a security camera.
         Without opencv, uses --x (0..1 horizontal centre; default 0.5).
blurfit  whole 16:9 frame centred on a blurred, darkened copy of itself (for slides, screen recordings,
         two-person shots where a crop would cut someone out).
Rule kept from editors: never cut off the top of the head; eyes land around 30-40% from the top.
"""
import argparse
import importlib.util
import os
import statistics
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, need, probe  # noqa: E402


def face_xs(path, dur, window, step=0.5):
    if importlib.util.find_spec("cv2") is None:
        return None
    import cv2  # noqa: WPS433
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(path)
    sections, t = [], 0.0
    while t < dur:
        xs = []
        s = t
        while s < min(t + window, dur):
            cap.set(cv2.CAP_PROP_POS_MSEC, s * 1000)
            ok, frame = cap.read()
            if ok:
                small = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (0, 0), fx=0.5, fy=0.5)
                faces = cascade.detectMultiScale(small, 1.1, 5, minSize=(30, 30))
                if len(faces):
                    fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])
                    xs.append((fx + fw / 2) / small.shape[1])
            s += step
        sections.append((t, statistics.median(xs) if xs else None))
        t += window
    cap.release()
    # fill gaps with the previous known position (or centre)
    last = 0.5
    out = []
    for t0, x in sections:
        last = x if x is not None else last
        out.append((t0, last))
    # ignore tiny moves: re-framing for a 3% shift is a visible jump with no benefit
    merged = []
    for t0, x in out:
        if merged and abs(x - merged[-1][1]) < 0.06:
            continue
        merged.append((t0, x))
    return merged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("out")
    ap.add_argument("--aspect", default="9:16")
    ap.add_argument("--mode", default="crop", choices=["crop", "blurfit"])
    ap.add_argument("--x", type=float, default=None, help="manual horizontal centre 0..1")
    ap.add_argument("--window", type=float, default=6.0)
    ap.add_argument("--crf", type=int, default=18)
    args = ap.parse_args()
    need("ffmpeg")
    info = probe(args.inp)
    aw, ah = (int(v) for v in args.aspect.split(":"))
    W, H = (1080, int(round(1080 * ah / aw / 2)) * 2)
    iw, ih = info["width"], info["height"]

    if args.mode == "blurfit":
        vf = (f"[0:v]split[bg][fg];[bg]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"boxblur=40:5,eq=brightness=-0.08[b];[fg]scale={W}:-2[f];[b][f]overlay=(W-w)/2:(H-h)/2,setsar=1[v]")
    else:
        cw = int(ih * aw / ah) // 2 * 2
        if cw > iw:
            die("source is already narrower than the target aspect; use --mode blurfit")
        if args.x is not None:
            plan = [(0.0, args.x)]
        else:
            plan = face_xs(args.inp, info["duration"], args.window) or [(0.0, 0.5)]
        def xpx(c):
            return int(min(max(c * iw - cw / 2, 0), iw - cw))
        expr = str(xpx(plan[-1][1]))
        for t0, c in reversed(plan[:-1]):
            nxt = plan[plan.index((t0, c)) + 1][0]
            expr = f"if(lt(t,{nxt:.2f}),{xpx(c)},{expr})"
        vf = f"[0:v]crop={cw}:{ih}:x='{expr}':y=0,scale={W}:{H}:flags=lanczos,setsar=1[v]"
        print(f"Reframe plan (section start s -> centre x): {[(round(t, 1), round(x, 2)) for t, x in plan]}")
    fps = round(info["fps"]) or 30
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostats", "-y", "-i", args.inp, "-filter_complex", vf,
           "-map", "[v]"]
    if info.get("has_audio"):
        cmd += ["-map", "0:a", "-c:a", "copy"]
    cmd += ["-c:v", "libx264", "-crf", str(args.crf), "-preset", "medium", "-pix_fmt", "yuv420p", "-g", str(fps),
            "-movflags", "+faststart", args.out]
    if subprocess.run(cmd).returncode != 0:
        die("reframe failed")
    print(f"Wrote {args.out} ({W}x{H}). Check the contact sheet: heads must not be cut off at any section.")


if __name__ == "__main__":
    main()
