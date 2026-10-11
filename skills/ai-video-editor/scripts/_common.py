"""Shared helpers for the ai-video-editor scripts. Standard library only + ffmpeg/ffprobe on PATH."""
import json
import os
import shutil
import subprocess
import sys
from fractions import Fraction


def die(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def need(tool):
    path = shutil.which(tool)
    if not path:
        die(f"'{tool}' not found on PATH. Run scripts/doctor.py for install commands.")
    return path


def run(cmd, capture=True, check=True):
    """Run a command list. Returns CompletedProcess. stderr is captured (ffmpeg logs there)."""
    proc = subprocess.run(cmd, capture_output=capture, text=True, errors="replace")
    if check and proc.returncode != 0:
        tail = (proc.stderr or "")[-2000:]
        die(f"command failed ({proc.returncode}): {' '.join(cmd[:6])} ...\n{tail}")
    return proc


def probe(path):
    """Return a dict with duration, width, height, fps, has_audio, codec info."""
    need("ffprobe")
    out = run([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", path,
    ]).stdout
    data = json.loads(out)
    v = next((s for s in data["streams"] if s.get("codec_type") == "video"), None)
    a = next((s for s in data["streams"] if s.get("codec_type") == "audio"), None)
    info = {
        "path": os.path.abspath(path),
        "duration": float(data["format"].get("duration", 0) or 0),
        "size_bytes": int(data["format"].get("size", 0) or 0),
        "bit_rate": int(data["format"].get("bit_rate", 0) or 0),
        "has_video": v is not None,
        "has_audio": a is not None,
    }
    if v:
        rate = v.get("avg_frame_rate") or v.get("r_frame_rate") or "30/1"
        try:
            fps = float(Fraction(rate)) if rate != "0/0" else 30.0
        except (ZeroDivisionError, ValueError):
            fps = 30.0
        rotation = 0
        for sd in v.get("side_data_list", []) or []:
            if "rotation" in sd:
                rotation = int(sd["rotation"])
        w, h = int(v.get("width", 0)), int(v.get("height", 0))
        if abs(rotation) in (90, 270):
            w, h = h, w
        info.update({
            "width": w, "height": h, "fps": round(fps, 3), "fps_fraction": rate,
            "vcodec": v.get("codec_name"), "pix_fmt": v.get("pix_fmt"),
            "color_transfer": v.get("color_transfer"), "rotation": rotation,
            "aspect": round(w / h, 4) if h else 0,
            "orientation": "vertical" if h > w else ("square" if h == w else "horizontal"),
        })
    if a:
        info.update({
            "acodec": a.get("codec_name"), "sample_rate": int(a.get("sample_rate", 0) or 0),
            "channels": a.get("channels"),
        })
    return info


def silences(path, noise_db=-35, min_dur=0.35):
    """Return list of (start, end) silence intervals via ffmpeg silencedetect."""
    need("ffmpeg")
    proc = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn",
        "-af", f"silencedetect=noise={noise_db}dB:d={min_dur}", "-f", "null", "-",
    ], check=False)
    out, cur = [], None
    for line in proc.stderr.splitlines():
        if "silence_start:" in line:
            cur = float(line.split("silence_start:")[1].split()[0])
        elif "silence_end:" in line and cur is not None:
            end = float(line.split("silence_end:")[1].split("|")[0].strip())
            out.append((max(0.0, cur), end))
            cur = None
    if cur is not None:
        out.append((cur, probe(path)["duration"]))
    return out


def loudness(path):
    """Integrated loudness (LUFS), true peak (dBTP) and LRA via ebur128. Returns dict."""
    proc = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn",
        "-af", "ebur128=peak=true", "-f", "null", "-",
    ], check=False)
    res = {}
    summary = proc.stderr.split("Summary:")[-1] if "Summary:" in proc.stderr else ""
    for line in summary.splitlines():
        line = line.strip()
        if line.startswith("I:"):
            res["integrated_lufs"] = _num(line)
        elif line.startswith("LRA:"):
            res["lra_lu"] = _num(line)
        elif line.startswith("Peak:"):
            res["true_peak_dbtp"] = _num(line)
    return res


def _num(line):
    try:
        return float(line.split(":")[1].split()[0])
    except (IndexError, ValueError):
        return None


def scene_cuts(path, threshold=0.3):
    """Timestamps where the picture changes (hard cuts) using the scene score."""
    proc = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", path, "-an",
        "-vf", f"scale=320:-2,select='gt(scene,{threshold})',showinfo", "-f", "null", "-",
    ], check=False)
    cuts = []
    for line in proc.stderr.splitlines():
        if "showinfo" in line and "pts_time:" in line:
            try:
                cuts.append(round(float(line.split("pts_time:")[1].split()[0]), 3))
            except ValueError:
                pass
    return cuts


def detect_cuts(path, hard=0.3, soft_floor=0.02, spike=4.0, window=15):
    """Hard cuts (scene score >= hard) PLUS jump cuts / punch-ins: frames whose score is a local spike
    (>= spike x the median of the surrounding window and >= soft_floor). Talking-head jump cuts score
    only 0.03-0.2, which a plain threshold misses or confuses with motion.
    Returns [{"t": seconds, "score": s, "kind": "hard"|"jump"}]."""
    proc = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", path, "-an",
        "-vf", "scale=320:-2,select='gte(scene,0)',metadata=print:key=lavfi.scene_score", "-f", "null", "-",
    ], check=False)
    times, scores, cur_t = [], [], None
    for line in proc.stderr.splitlines():
        if "pts_time:" in line:
            try:
                cur_t = float(line.split("pts_time:")[1].split()[0])
            except ValueError:
                cur_t = None
        elif "lavfi.scene_score=" in line and cur_t is not None:
            times.append(cur_t)
            scores.append(float(line.split("=")[1]))
    cuts = []
    for i, (t, s) in enumerate(zip(times, scores)):
        if t < 0.1:
            continue
        lo, hi = max(0, i - window), min(len(scores), i + window + 1)
        neigh = sorted(scores[lo:i] + scores[i + 1:hi]) or [0.0]
        med = neigh[len(neigh) // 2]
        is_peak = s >= max(scores[max(0, i - 2):i + 3])
        if s >= hard:
            cuts.append({"t": round(t, 3), "score": round(s, 3), "kind": "hard"})
        elif s >= soft_floor and is_peak and s >= spike * max(med, 0.002):
            cuts.append({"t": round(t, 3), "score": round(s, 3), "kind": "jump"})
    return cuts


def contact_sheet(path, out_png, every=2.0, cols=6, width=320, start=0.0, end=None):
    """Tile one frame every `every` seconds into a single PNG with timestamps burned in."""
    info = probe(path)
    dur = (end or info["duration"]) - start
    n = max(1, int(dur / every))
    rows = max(1, -(-n // cols))
    vf = (
        f"fps=1/{every},scale={width}:-2,"
        "drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,"
        f"tile={cols}x{rows}:padding=4:margin=4"
    )
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    if start:
        cmd += ["-ss", f"{start}"]
    cmd += ["-i", path]
    if end:
        cmd += ["-t", f"{dur}"]
    cmd += ["-vf", vf, "-frames:v", "1", out_png]
    proc = run(cmd, check=False)
    if proc.returncode != 0:
        # drawtext needs a font; retry without timestamps
        vf2 = f"fps=1/{every},scale={width}:-2,tile={cols}x{rows}:padding=4:margin=4"
        cmd[cmd.index("-vf") + 1] = vf2
        run(cmd)
    return out_png


def frame_at(path, t, out_png, width=None):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{max(0, t):.3f}", "-i", path,
           "-frames:v", "1"]
    if width:
        cmd += ["-vf", f"scale={width}:-2"]
    run(cmd + [out_png])
    return out_png


def dominant_colors(path, t, k=5):
    """Return k dominant hex colors of the frame at time t. Pure python: ffmpeg -> 64x36 raw RGB."""
    proc = subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", path,
        "-frames:v", "1", "-vf", "scale=64:36", "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ], capture_output=True)
    raw = proc.stdout
    if not raw:
        return []
    buckets = {}
    for i in range(0, len(raw) - 2, 3):
        r, g, b = raw[i] >> 4, raw[i + 1] >> 4, raw[i + 2] >> 4  # 16 levels per channel
        buckets[(r, g, b)] = buckets.get((r, g, b), 0) + 1
    top = sorted(buckets.items(), key=lambda kv: -kv[1])[:k]
    total = len(raw) // 3
    return [{"hex": "#%02X%02X%02X" % (r * 17, g * 17, b * 17), "share": round(c / total, 3)}
            for (r, g, b), c in top]


def write_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    return path


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fmt_tc(t):
    t = max(0.0, t)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"
