#!/usr/bin/env python3
"""9:16 safe-zone tools: every piece of text and every graphic that must be read stays inside the platform's
safe box and out of the button rail. Platforms: reels (organic Instagram, the user's spec: 220 px top, 420 px
bottom, 1010 px wide), reels-ad, tiktok, shorts, cross (all of them; default when cross-posting).

Usage:
  python3 safezone.py html work/gfx/reel --platform reels [--samples 24] [--at 0.8,2.4]
        Opens a HyperFrames composition in headless Chrome, seeks the timeline at each sample time and
        measures every VISIBLE text box. FAIL when any text leaves the safe box or touches the rail.
        Mark deliberate bleed (a giant background word) with data-safe-ignore on the element.
  python3 safezone.py alpha work/gfx/lower-third.mov --platform reels
        For transparent overlays (MOV/WebM): the alpha channel is exactly where the graphic is.
        FAIL when visible pixels fall outside the box or on the rail.
  python3 safezone.py sheet renders/v3.mp4 --platform reels [--every 1.5]
        Contact sheet with the safe box drawn on each frame (green box, dimmed UI bands, red rail):
        the visual check for burned-in footage text that no script can read.
  python3 safezone.py guide --platform reels --out work/safe_reels.png
        Transparent 1080x1920 guide PNG to drop into a composition while designing (remove before render).
Exit code 1 on any FAIL, so it can gate delivery.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import SAFE_ZONES, die, need, probe, safe_zone, zone_violations  # noqa: E402


def find_chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    if shutil.which("npx"):
        p = subprocess.run(["npx", "--yes", "hyperframes", "browser", "path"], capture_output=True, text=True)
        cand = (p.stdout.strip().splitlines() or [""])[-1].strip()
        if cand and os.path.exists(cand):
            return cand
    for c in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe"] + \
             [shutil.which(n) or "" for n in ("google-chrome", "chromium", "chromium-browser", "chrome")]:
        if c and os.path.exists(c):
            return c
    die("no Chrome found. Run `npx hyperframes browser ensure`, or set CHROME=/path/to/chrome")


AUDIT_JS = r"""
<script>
(async () => {
  const out = {boxes: [], error: null};
  try {
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    const ids = Object.keys(window.__timelines || {});
    if (!ids.length) throw new Error("no timeline registered in window.__timelines");
    const tl = window.__timelines[ids[0]];
    for (const t of __TIMES__) {
      tl.seek(t, false);
      const els = [...document.querySelectorAll('body *')].filter(e =>
        e.id !== '__safe_audit' && !e.closest('[data-safe-ignore]') &&
        [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
      for (const e of els) {
        let op = 1, n = e;
        while (n && n.nodeType === 1) {
          const cs = getComputedStyle(n);
          if (cs.display === 'none' || cs.visibility === 'hidden') { op = 0; break; }
          op *= parseFloat(cs.opacity || '1'); n = n.parentElement;
        }
        if (op < 0.05) continue;
        const r = document.createRange(); r.selectNodeContents(e);
        const b = r.getBoundingClientRect();
        if (b.width < 1 || b.height < 1) continue;
        let y0 = b.top, y1 = b.bottom;
        // Single-line text with no child elements: use the glyphs' real ink height, not the font's content box
        // (display faces like Anton have a content box ~1.5x the font size; that would flag phantom overlaps).
        if (e.children.length === 0 && r.getClientRects().length === 1) {
          const cs = getComputedStyle(e);
          const ctx = (window.__szc = window.__szc || document.createElement('canvas').getContext('2d'));
          ctx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
          const m = ctx.measureText(e.textContent.trim());
          const fA = m.fontBoundingBoxAscent, fD = m.fontBoundingBoxDescent;
          if (fA + fD > 0 && m.actualBoundingBoxAscent > 0) {
            const k = b.height / (fA + fD);
            y0 = b.top + (fA - m.actualBoundingBoxAscent) * k;
            y1 = b.top + (fA + m.actualBoundingBoxDescent) * k;
          }
        }
        out.boxes.push({t, text: e.textContent.trim().replace(/\s+/g, ' ').slice(0, 40),
                        x0: b.left, y0, x1: b.right, y1});
      }
    }
  } catch (err) { out.error = String(err); }
  const pre = document.createElement('pre'); pre.id = '__safe_audit';
  pre.textContent = JSON.stringify(out); document.body.appendChild(pre);
})();
</script>
"""


def audit_html(args):
    d = os.path.abspath(args.target)
    page = os.path.join(d, "index.html") if os.path.isdir(d) else d
    if not os.path.exists(page):
        die(f"no index.html in {args.target}")
    html = open(page, encoding="utf-8").read()
    m = re.search(r'data-composition-id="[^"]+"[^>]*', html)
    attrs = m.group(0) if m else ""
    num = lambda k, dflt: float(re.search(rf'{k}="([\d.]+)"', attrs).group(1)) if re.search(rf'{k}="([\d.]+)"', attrs) else dflt  # noqa: E731,E501
    W, H, dur = int(num("data-width", 1080)), int(num("data-height", 1920)), num("data-duration", 5)
    zone = safe_zone(args.platform, W, H)
    if zone is None:
        die(f"composition is {W}x{H}: safe zones apply to vertical (9:16) frames only")
    # dense sampling (default 10 per second): a 0.18 s slam at 112% scale is exactly what sparse samples miss
    n = max(2, args.samples or int(round(dur * 10)))
    times = [round(dur * (i + 0.5) / n, 3) for i in range(n)]
    times += [float(x) for x in args.at.split(",")] if args.at else []
    inj = AUDIT_JS.replace("__TIMES__", json.dumps(sorted(set(times))))
    html2 = re.sub(r"<head>", lambda _m: "<head><script>window.__timelines = window.__timelines || {};</script>", html,
                   count=1, flags=re.I)
    html2 = re.sub(r"</body>", lambda _m: inj + "</body>", html2, count=1, flags=re.I)
    tmp = os.path.join(os.path.dirname(page), "_safezone_audit.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html2)
    try:
        chrome = find_chrome()
        prof = tempfile.mkdtemp(prefix="sz-")
        p = subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                            f"--user-data-dir={prof}", f"--window-size={W},{H}", "--force-device-scale-factor=1",
                            "--allow-file-access-from-files", "--virtual-time-budget=20000", "--dump-dom",
                            "file://" + tmp], capture_output=True, text=True, timeout=180)
        shutil.rmtree(prof, ignore_errors=True)
    finally:
        os.remove(tmp)
    mm = re.search(r'<pre id="__safe_audit">(.*?)</pre>', p.stdout, re.S)
    if not mm:
        die("audit produced no result (page script failed to run). Check the composition loads: npx hyperframes lint")
    data = json.loads(mm.group(1).replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<")
                      .replace("&gt;", ">"))
    if data.get("error"):
        die("audit error in page: " + data["error"])
    return report(zone, [(b["t"], b["text"], (b["x0"], b["y0"], b["x1"], b["y1"])) for b in data["boxes"]],
                  f"{len(set(times))} sample times, {len(data['boxes'])} visible text boxes")


def audit_alpha(args):
    need("ffmpeg")
    info = probe(args.target)
    W, H = info["width"], info["height"]
    zone = safe_zone(args.platform, W, H)
    if zone is None:
        die(f"graphic is {W}x{H}: safe zones apply to vertical (9:16) frames only")
    sw, sh = 270, int(270 * H / W)
    pre = ["-c:v", "libvpx-vp9"] if args.target.lower().endswith(".webm") else []
    raw = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error"] + pre + ["-i", args.target, "-vf",
                          f"fps=4,format=rgba,alphaextract,scale={sw}:{sh}:flags=area,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    if not raw:
        die("could not read an alpha channel (is this a transparent MOV/WebM? MP4 has no alpha)")
    fsz = sw * sh
    hits = []
    for k in range(len(raw) // fsz):
        fr = raw[k * fsz:(k + 1) * fsz]
        xs = [i % sw for i in range(fsz) if fr[i] > 40]
        if not xs:
            continue
        ys = [i // sw for i in range(fsz) if fr[i] > 40]
        sx, sy = W / sw, H / sh
        rect = (min(xs) * sx, min(ys) * sy, (max(xs) + 1) * sx, (max(ys) + 1) * sy)
        hits.append((round(k / 4, 2), "graphic pixels", rect))
    if not hits:
        die("graphic is fully transparent in every sampled frame")
    return report(zone, hits, f"{len(raw) // fsz} frames at 4 fps")


def report(zone, items, what):
    fails = []
    for t, text, rect in items:
        for v in zone_violations(rect, zone):
            fails.append(f"t={t:>6.2f}s  '{text}'  {v}")
    seen, uniq = set(), []
    for f in fails:
        key = f.split("  ", 1)[1]
        if key not in seen:
            seen.add(key)
            uniq.append(f)
    bx = ", ".join(f"{v:.0f}" for v in zone["box"])
    print(f"Safe zone '{zone['name']}' box ({bx}), {what}.")
    if uniq:
        for f in uniq[:40]:
            print("FAIL", f)
        print(f"RESULT: FAIL ({len(uniq)} problem(s)). Move or shrink the text; keep it inside the box and out "
              "of the rail. Deliberate bleed: data-safe-ignore.")
        return 1
    print("RESULT: PASS: every visible text box stays inside the safe zone.")
    return 0


def draw_filters(zone, W, H, dim=0.45):
    x0, y0, x1, y1 = (int(v) for v in zone["box"])
    f = [f"drawbox=x=0:y=0:w={W}:h={y0}:color=black@{dim}:t=fill",
         f"drawbox=x=0:y={y1}:w={W}:h={H - y1}:color=black@{dim}:t=fill",
         f"drawbox=x=0:y={y0}:w={x0}:h={y1 - y0}:color=black@{dim}:t=fill",
         f"drawbox=x={x1}:y={y0}:w={W - x1}:h={y1 - y0}:color=black@{dim}:t=fill"]
    for rx0, ry0, rx1, ry1 in zone["rails"]:
        f.append(f"drawbox=x={int(rx0)}:y={int(ry0)}:w={int(rx1 - rx0)}:h={int(ry1 - ry0)}:color=red@0.35:t=fill")
    f.append(f"drawbox=x={x0}:y={y0}:w={x1 - x0}:h={y1 - y0}:color=0xC8E61E@1:t=4")
    return ",".join(f)


def sheet(args):
    need("ffmpeg")
    info = probe(args.target)
    W, H = info["width"], info["height"]
    zone = safe_zone(args.platform, W, H)
    if zone is None:
        die("sheet needs a vertical (9:16) video")
    out = args.out or os.path.splitext(args.target)[0] + f".safezone_{zone['name']}.png"
    n = max(1, -(-int(info["duration"] * 1000) // int(args.every * 1000)))
    cols = min(6, n)
    rows = -(-n // cols)
    vf = (f"fps=1/{args.every},{draw_filters(zone, W, H)},scale=270:-2,"
          f"tile={cols}x{rows}:padding=6:color=0x202020")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", args.target, "-vf", vf,
                    "-frames:v", "1", out], check=True)
    print(f"Wrote {out}: {n} frames with the '{zone['name']}' safe box. LOOK: no text or logo may sit in a "
          "dimmed band or on the red rail.")
    return 0


def guide(args):
    need("ffmpeg")
    W, H = (int(v) for v in args.size.split("x"))
    zone = safe_zone(args.platform, W, H)
    out = args.out or f"safe_{zone['name']}_{W}x{H}.png"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    f"color=black@0.0:s={W}x{H}:d=0.04,format=rgba", "-vf", draw_filters(zone, W, H, dim=0.35),
                    "-frames:v", "1", out], check=True)
    print(f"Wrote {out}: transparent guide. Use it while designing; never render it into the final.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["html", "alpha", "sheet", "guide"])
    ap.add_argument("target", nargs="?")
    ap.add_argument("--platform", default="cross", help="reels | reels-ad | tiktok | shorts | cross ("
                    + ", ".join(SAFE_ZONES) + ")")
    ap.add_argument("--samples", type=int, default=0, help="sample count (default: 10 per second of timeline)")
    ap.add_argument("--at", help="extra sample times, e.g. the apex word times")
    ap.add_argument("--every", type=float, default=1.5)
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--out")
    args = ap.parse_args()
    if args.mode != "guide" and not args.target:
        ap.error("give a target")
    if args.mode != "guide" and not os.path.exists(args.target):
        die(f"not found: {args.target}")
    sys.exit({"html": audit_html, "alpha": audit_alpha, "sheet": sheet, "guide": guide}[args.mode](args))


if __name__ == "__main__":
    main()
