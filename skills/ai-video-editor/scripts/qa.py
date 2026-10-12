#!/usr/bin/env python3
"""Pre-delivery QA. Prints PASS/WARN/FAIL lines and builds review sheets the agent must LOOK at.

Usage:
  python3 qa.py <final.mp4> [--edl edl.json] [--captions captions.ass] [--platform youtube|shorts|...]
                [--out work/x/qa]
Checks: spec (codec, pix_fmt, fps, resolution, faststart), loudness vs target, true peak, black frames,
frozen frames, dead air, flash frames (very short shots), and builds:
  cuts.png      the frame just before and just after every edit point (jump-cut / flash check)
  captions.png  one frame in the middle of every 3rd caption group (legibility, face overlap, safe zone)
  overview.png  one frame every N seconds
"""
import argparse
import os
import re
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import contact_sheet, detect_cuts, frame_at, loudness, probe, read_json, run, safe_zone, silences  # noqa: E402,E501

TARGET = {"youtube": (-14, -1.0), "shorts": (-14, -1.0), "reels": (-14, -1.0), "tiktok": (-14, -1.0),
          "linkedin": (-14, -1.0), "x": (-14, -1.0), "master": (-14, -1.0)}


def tile(pngs, out, cols=4):
    if not pngs:
        return None
    lst = out + ".txt"
    with open(lst, "w") as f:
        for p in pngs:
            f.write(f"file '{os.path.abspath(p)}'\n")
    rows = -(-len(pngs) // cols)
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-vf", f"scale=360:-2,tile={cols}x{rows}:padding=4:margin=4", "-frames:v", "1", out])
    os.remove(lst)
    for p in pngs:
        os.remove(p)
    return out


def moov_first(path):
    """Walk top-level MP4 atoms (headers only): True when moov comes before mdat (faststart)."""
    import struct
    try:
        with open(path, "rb") as f:
            size_total = os.path.getsize(path)
            pos = 0
            while pos < size_total:
                f.seek(pos)
                hdr = f.read(16)
                if len(hdr) < 8:
                    return None
                size, kind = struct.unpack(">I4s", hdr[:8])
                if size == 1:
                    size = struct.unpack(">Q", hdr[8:16])[0]
                elif size == 0:
                    size = size_total - pos
                if kind == b"moov":
                    return True
                if kind == b"mdat":
                    return False
                if size < 8:
                    return None
                pos += size
    except OSError:
        return None
    return None


def window_loudness(path, t, length):
    """Integrated loudness of a short window, or None when the whole window is below the -70 LUFS gate."""
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{max(0.0, t):.3f}", "-t", f"{max(length, 0.4):.3f}",
               "-i", path, "-vn", "-af", "ebur128", "-f", "null", "-"], check=False).stderr
    m = re.findall(r"I:\s+(-?[\d.]+|-inf) LUFS", err)
    if not m or m[-1] == "-inf" or float(m[-1]) <= -69.9:
        return None
    return float(m[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--edl")
    ap.add_argument("--captions")
    ap.add_argument("--platform", default="youtube", choices=list(TARGET))
    ap.add_argument("--out")
    ap.add_argument("--every", type=float, default=5.0)
    ap.add_argument("--safe", default=None, help="9:16 safe zone to draw: reels, reels-ad, tiktok, shorts, cross "
                    "(default: the --platform's zone, cross for youtube)")
    ap.add_argument("--silence-at", default="",
                    help="times (s) of deliberate dead stops where the WHOLE mix pauses (music stopped and the voice silent), "
                         "e.g. '41.2,58'. Each 0.5 s window after them must sit "
                         "at least --silence-lu below the programme loudness (catches long SFX/reverb tails)")
    ap.add_argument("--silence-len", type=float, default=0.5)
    ap.add_argument("--silence-lu", type=float, default=14.0)
    args = ap.parse_args()
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.video)), "qa")
    os.makedirs(out, exist_ok=True)
    res = []

    def report(level, msg):
        res.append((level, msg))
        print(f"{level:<4} {msg}")

    info = probe(args.video)
    report("PASS" if info.get("vcodec") in ("h264", "hevc", "av1", "prores") else "WARN",
           f"video codec {info.get('vcodec')}")
    report("PASS" if info.get("pix_fmt") in ("yuv420p", "yuvj420p") else "FAIL",
           f"pixel format {info.get('pix_fmt')} (yuv420p needed for every player)")
    report("PASS" if info.get("acodec") == "aac" else "WARN", f"audio codec {info.get('acodec')}")
    report("PASS" if info.get("sample_rate") in (48000, 44100) else "WARN", f"sample rate {info.get('sample_rate')}")
    vert = info.get("height", 0) > info.get("width", 0)
    if args.platform in ("shorts", "reels", "tiktok") and not vert:
        report("FAIL", f"{args.platform} needs vertical 9:16; file is {info.get('width')}x{info.get('height')}")
    if min(info.get("width", 0), info.get("height", 0)) < 1080:
        report("WARN", f"below 1080p ({info.get('width')}x{info.get('height')})")
    size_mb = os.path.getsize(args.video) / 1e6
    mbps = size_mb * 8 / max(info.get("duration") or 1, 0.1)
    cap = 40 if min(info.get("width", 0), info.get("height", 0)) > 1440 else 16
    report("PASS" if mbps <= cap else "WARN",
           f"file {size_mb:.0f} MB, {mbps:.1f} Mbps overall (cap {cap} at this size"
           + ("" if mbps <= cap else "; grain or noise is eating bits: re-encode with finish.py --crf 21-23, the "
              "platform re-encodes anyway and a huge upload stalls or gets rejected)") + ")")
    mf = moov_first(args.video)
    report("PASS" if mf else "WARN", "faststart (moov atom before media data, plays before full download)"
           + ("" if mf is not None else ": could not read the atom layout"))

    if info.get("has_audio"):
        L = loudness(args.video)
        tgt, tp = TARGET[args.platform]
        i_l, p = L.get("integrated_lufs"), L.get("true_peak_dbtp")
        if i_l is not None:
            report("PASS" if abs(i_l - tgt) <= 1.0 else "FAIL", f"loudness {i_l} LUFS (target {tgt} +/-1)")
        else:
            report("WARN", f"loudness could not be measured: the {tgt} LUFS target is NOT verified")
        if p is not None:
            report("PASS" if p <= tp + 0.3 else "FAIL", f"true peak {p} dBTP (max {tp})")
        else:
            report("WARN", "true peak could not be measured: NOT verified")
        if info.get("channels") == 1:
            report("WARN", "mono audio: fine for voice-only, but a stereo music bed was collapsed if one was used")
        for t in [float(x) for x in args.silence_at.split(",") if x.strip()]:
            w = window_loudness(args.video, t, args.silence_len)
            if i_l is None:
                report("WARN", f"dead stop at {t:.2f}s not verified (programme loudness unknown)")
            elif w is None:
                report("PASS", f"dead stop at {t:.2f}s: window below the gate (true silence)")
            else:
                gap = i_l - w
                report("PASS" if gap >= args.silence_lu else "FAIL",
                       f"dead stop at {t:.2f}s: window {w:.1f} LUFS, {gap:.1f} LU under the programme "
                       f"(need {args.silence_lu:.0f})" + ("" if gap >= args.silence_lu else
                       ": a long hit or reverb tail is filling the silence; shorten or fade the SFX before the stop"))
        gaps = [s for s in silences(args.video, -45, 1.2) if s[0] > 0.5 and s[1] < info["duration"] - 0.5]
        report("PASS" if not gaps else "WARN", f"dead air >1.2s: {len(gaps)}"
               + (" at " + ", ".join(f"{a:.1f}s" for a, _ in gaps[:10]) if gaps else ""))

    bl = run(["ffmpeg", "-hide_banner", "-nostats", "-i", args.video, "-an", "-vf",
              "blackdetect=d=0.08:pix_th=0.06", "-f", "null", "-"], check=False).stderr
    blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", bl)
    blacks = [(float(a), float(b)) for a, b in blacks if not (float(a) < 0.05 and float(b) < 1.0)]
    report("PASS" if not blacks else "WARN", f"black frames: {len(blacks)}"
           + (" at " + ", ".join(f"{float(a):.2f}s" for a, _ in blacks[:10]) if blacks else ""))
    fz = run(["ffmpeg", "-hide_banner", "-nostats", "-i", args.video, "-an", "-vf",
              "scale=320:-2,freezedetect=n=0.002:d=2.5", "-f", "null", "-"], check=False).stderr
    freezes = re.findall(r"freeze_start: ([\d.]+)", fz)
    report("PASS" if not freezes else "WARN", f"frozen picture >2.5s: {len(freezes)}"
           + (" at " + ", ".join(f"{float(a):.1f}s" for a in freezes[:10]) if freezes else "")
           + " (fine for slides/holds; a bug if it is supposed to be live footage)")

    cuts = [c["t"] for c in detect_cuts(args.video)]
    fps = info.get("fps") or 30
    shots = [b - a for a, b in zip([0.0] + cuts, cuts + [info["duration"]])]
    flash = [round(c, 2) for c, s in zip([0.0] + cuts, shots) if s < 3 / fps and c > 0]
    report("PASS" if not flash else "FAIL", f"flash frames (shots < 3 frames): {len(flash)}"
           + (f" at {flash[:10]}" if flash else ""))

    edit_points = []
    if args.edl:
        t = 0.0
        for s in read_json(args.edl)["segments"][:-1]:
            t += s["end"] - s["start"]
            edit_points.append(t)
    else:
        edit_points = cuts
    pngs = []
    if len(edit_points) > 40:  # sample across the whole video, not just the first 40 cuts
        step = len(edit_points) / 40.0
        edit_points = [edit_points[int(i * step)] for i in range(40)]
    for i, t in enumerate(edit_points):
        pngs.append(frame_at(args.video, max(0, t - 1.5 / fps), os.path.join(out, f"_c{i:03d}a.png"), 480))
        pngs.append(frame_at(args.video, t + 1.5 / fps, os.path.join(out, f"_c{i:03d}b.png"), 480))
    if pngs:
        tile(pngs, os.path.join(out, "cuts.png"), cols=4)
        report("LOOK", f"cuts.png: before/after pairs for {len(edit_points)} edit points (sampled across the video)")

    if args.captions and os.path.exists(args.captions):
        times = []
        for line in open(args.captions, encoding="utf-8"):
            if line.startswith("Dialogue:"):
                p = line.split(",")
                h, m, s = p[1].split(":")
                h2, m2, s2 = p[2].split(":")
                a = int(h) * 3600 + int(m) * 60 + float(s)
                b = int(h2) * 3600 + int(m2) * 60 + float(s2)
                times.append((a + b) / 2)
        last = info["duration"] - 0.05  # never sample past the end (ffmpeg returns no frame)
        sample = sorted(set(round(t, 1) for t in times if t < last))[::3][:24]
        cp = [frame_at(args.video, t, os.path.join(out, f"_k{i:03d}.png"), 480) for i, t in enumerate(sample)]
        if cp:
            tile(cp, os.path.join(out, "captions.png"), cols=4)
            report("LOOK", "captions.png: check legibility, face overlap, platform UI safe zones, spelling")

    contact_sheet(args.video, os.path.join(out, "overview.png"), every=args.every)
    report("LOOK", "overview.png: whole-video rhythm, colour consistency, nothing broken")

    zone_name = args.safe or {"reels": "reels", "tiktok": "tiktok", "shorts": "shorts"}.get(args.platform, "cross")
    zone = safe_zone(zone_name, info.get("width", 0), info.get("height", 0)) if vert else None
    if zone:
        from safezone import draw_filters  # noqa: WPS433
        W, H = info["width"], info["height"]
        n = max(1, min(24, int(info["duration"] // 1.5) + 1))
        step = max(info["duration"] / n, 0.1)
        sz = os.path.join(out, f"safezone_{zone['name']}.png")
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", args.video, "-vf",
             f"fps=1/{step:.3f},{draw_filters(zone, W, H)},scale=270:-2,tile=6x{-(-n // 6)}:padding=6:color=0x202020",
             "-frames:v", "1", sz])
        report("LOOK", f"safezone_{zone['name']}.png: no text, logo or graphic in a dimmed band or on the red rail "
                       f"(graphics: scripts/safezone.py html|alpha checks them exactly)")

    fails = [m for lv, m in res if lv == "FAIL"]
    warns = [m for lv, m in res if lv == "WARN"]
    with open(os.path.join(out, "qa.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(f"{lv} {m}" for lv, m in res) + "\n")
    if fails:
        print("\nRESULT: FAIL (fix before delivery)")
    elif warns:
        print(f"\nRESULT: no FAIL, but {len(warns)} WARN line(s). Each one needs a written disposition in EDIT_STATE.md "
              "(fixed, or accepted with the reason) before delivery. Then LOOK at every sheet and write qa/qa-look.md.")
    else:
        print("\nRESULT: no automatic failures. Now LOOK at every sheet and write qa/qa-look.md (one verdict line "
              "per sheet) before calling it done.")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
