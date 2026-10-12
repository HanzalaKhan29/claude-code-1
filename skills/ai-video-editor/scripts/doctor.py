#!/usr/bin/env python3
"""Check the editing toolkit and print the exact install command for anything missing.

Usage: python3 doctor.py [--json]
Never installs anything itself: the agent shows the commands and asks before running them.
"""
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys

OS = platform.system()  # Darwin / Windows / Linux
ARM_MAC = OS == "Darwin" and platform.machine() == "arm64"


def ver(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return (out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr) else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def install_hint(name):
    mac, win, lin = {
        "ffmpeg": ("brew install ffmpeg", "winget install --id Gyan.FFmpeg -e", "sudo apt-get install -y ffmpeg"),
        "node": ("brew install node@22", "winget install OpenJS.NodeJS.LTS", "use nvm: nvm install 22"),
        "yt-dlp": ("brew install yt-dlp", "winget install yt-dlp.yt-dlp", "python3 -m pip install -U yt-dlp"),
        "auto-editor": ("python3 -m pip install -U auto-editor", "python -m pip install -U auto-editor",
                        "python3 -m pip install -U auto-editor"),
    }.get(name, ("", "", ""))
    return {"Darwin": mac, "Windows": win}.get(OS, lin)


def check_bin(name, version_args):
    path = shutil.which(name)
    return {"name": name, "ok": bool(path), "path": path,
            "version": ver([name] + version_args) if path else "", "install": "" if path else install_hint(name)}


def check_py(module, pip_name, why):
    ok = importlib.util.find_spec(module) is not None
    py = "python" if OS == "Windows" else "python3"
    return {"name": pip_name, "ok": ok, "why": why, "install": "" if ok else f"{py} -m pip install -U {pip_name}"}


def main():
    as_json = "--json" in sys.argv
    report = {"os": OS, "arch": platform.machine(), "python": sys.version.split()[0], "required": [], "optional": []}

    report["required"].append(check_bin("ffmpeg", ["-version"]))
    report["required"].append(check_bin("ffprobe", ["-version"]))
    node = check_bin("node", ["--version"])
    if node["ok"]:
        try:
            major = int(node["version"].lstrip("v").split(".")[0])
            if major < 22:
                node["ok"] = False
                node["install"] = "HyperFrames needs Node >= 22. " + install_hint("node")
        except ValueError:
            pass
    report["required"].append(node)
    npx = shutil.which("npx")
    report["required"].append({"name": "hyperframes (via npx)", "ok": bool(npx),
                               "install": "" if npx else "comes with Node 22+",
                               "note": "First run: npx hyperframes@latest doctor"})

    # transcription: any one engine is enough
    engines = []
    if ARM_MAC:
        engines.append(check_py("mlx_whisper", "mlx-whisper", "fastest on Apple Silicon"))
    engines.append(check_py("faster_whisper", "faster-whisper", "fast on CPU/NVIDIA, word timestamps"))
    engines.append(check_py("whisper", "openai-whisper", "reference Whisper, slower"))
    hf_ok = False
    if npx and not any(e["ok"] for e in engines):  # the fallback only counts if it actually runs
        try:
            hf_ok = subprocess.run(["npx", "--yes", "hyperframes", "--version"], capture_output=True,
                                   timeout=90).returncode == 0
        except (subprocess.TimeoutExpired, OSError):
            hf_ok = False
    have_engine = any(e["ok"] for e in engines) or hf_ok
    # Engines download their model on first use. A sandbox or firewall that blocks Hugging Face makes an
    # "installed" engine fail late, so check reachability now (skip if a model is already cached).
    cache = os.path.expanduser("~/.cache/huggingface/hub")
    cached = os.path.isdir(cache) and any("whisper" in d.lower() for d in os.listdir(cache))
    hf_ok = cached
    if not cached:
        try:
            import urllib.request  # noqa: WPS433
            urllib.request.urlopen(urllib.request.Request("https://huggingface.co", method="HEAD"), timeout=6)
            hf_ok = True
        except Exception:  # noqa: BLE001 - any failure means models cannot download
            hf_ok = False
    report["model_download"] = {"ok": hf_ok, "cached": cached}
    report["transcription"] = {"ok": have_engine, "engines": engines,
                               "fallback": "npx hyperframes transcribe <audio> --json (bundled local Whisper)"}

    report["optional"].append(check_bin("yt-dlp", ["--version"]))
    report["optional"].append(check_bin("auto-editor", ["--version"]))
    report["optional"].append(check_py("rembg", "rembg", "background removal for cut-outs"))
    report["optional"].append(check_py("df", "deepfilternet", "voice clean-up / denoise"))
    report["optional"].append(check_py("cv2", "opencv-python", "face detection for caption placement and reframing"))

    missing_req = [r for r in report["required"] if not r["ok"]]
    report["ready"] = not missing_req and have_engine

    if as_json:
        print(json.dumps(report, indent=2))
        return
    print(f"System: {OS} {platform.machine()} · Python {report['python']}")
    for r in report["required"]:
        mark = "OK " if r["ok"] else "MISSING"
        print(f"  [{mark}] {r['name']:<22} {r.get('version', '')[:60]}")
        if not r["ok"] and r.get("install"):
            print(f"           install: {r['install']}")
    print(f"  [{'OK ' if have_engine else 'MISSING'}] transcription engine")
    for e in engines:
        print(f"           {'yes' if e['ok'] else 'no '} {e['name']:<16} {e['why']}"
              + ("" if e["ok"] else f"  ->  {e['install']}"))
    if not report["model_download"]["ok"]:
        print("  [WARN] huggingface.co unreachable and no cached Whisper model: transcription will fail on first\n"
              "         use. Allow the host, or copy a model into ~/.cache/huggingface/hub, or transcribe elsewhere\n"
              "         and hand over words.json.")
    print("Optional:")
    for r in report["optional"]:
        print(f"  [{'yes' if r['ok'] else 'no '}] {r['name']:<16}" + ("" if r["ok"] else f"  ->  {r['install']}"))
    print("\nREADY" if report["ready"] else "\nNOT READY: install the MISSING items above (ask the user first).")


if __name__ == "__main__":
    main()
