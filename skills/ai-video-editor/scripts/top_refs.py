#!/usr/bin/env python3
"""Find a creator's best-performing edits on a YouTube channel or Instagram/TikTok page, then measure them.

The user should not have to pick reference videos. Give a channel/page URL and this ranks its recent posts
by views (likes when the platform hides views, e.g. Instagram), keeps the top N, downloads them and runs
analyze_reference.py on each. Then run compare_refs.py on the results to get the consensus style.

Usage:
  python3 top_refs.py "https://www.youtube.com/@creator/shorts" --top 10 --out work/refs/creator
  python3 top_refs.py "https://www.instagram.com/creator/" --top 10 --cookies-from-browser chrome
  python3 top_refs.py --urls urls.txt --top 10            # you collected post URLs yourself (one per line)
  python3 top_refs.py ... --list-only                     # rank and print, download nothing

Notes:
- Ask the user before downloading. This is private style analysis, never re-upload.
- YouTube: point at the tab that matches the format being made (/shorts for Shorts, /videos for long-form).
- Instagram/TikTok usually need login cookies for profile listing (--cookies-from-browser chrome|safari|firefox).
  If listing still fails, open the page in a browser, copy the post URLs into urls.txt and use --urls.
- The ranking metric is printed and saved. Never call a likes ranking "most viewed".
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, write_json  # noqa: E402


def ytdlp(args, cookies):
    cmd = ["yt-dlp", "--ignore-errors", "--no-warnings"] + (["--cookies-from-browser", cookies] if cookies else [])
    proc = subprocess.run(cmd + args, capture_output=True, text=True)
    return proc


def list_entries(url, scan, cookies):
    proc = ytdlp(["--flat-playlist", "--playlist-end", str(scan), "-J", url], cookies)
    if proc.returncode != 0 and not proc.stdout.strip():
        die("could not list that page: " + (proc.stderr.strip().splitlines() or ["unknown error"])[-1] +
            "\nTry --cookies-from-browser, or collect post URLs into a file and use --urls.")
    data = json.loads(proc.stdout or "{}")
    out = []
    for e in data.get("entries") or []:
        link = e.get("url") or e.get("webpage_url")
        if link and not link.startswith("http"):
            link = f"https://www.youtube.com/watch?v={link}" if len(link) == 11 else link
        out.append({"url": link, "title": e.get("title"), "views": e.get("view_count"),
                    "likes": e.get("like_count"), "duration": e.get("duration")})
    return [e for e in out if e["url"]]


def fill_metrics(entries, cookies):
    """Flat listings often omit counts (Instagram, TikTok). Fetch per-post metadata for those."""
    for e in entries:
        if e["views"] is not None or e["likes"] is not None:
            continue
        proc = ytdlp(["--skip-download", "-J", "--no-playlist", e["url"]], cookies)
        try:
            meta = json.loads(proc.stdout)
        except json.JSONDecodeError:
            continue
        e["views"], e["likes"] = meta.get("view_count"), meta.get("like_count")
        e["title"] = e["title"] or meta.get("title") or meta.get("description", "")[:60]
        e["duration"] = e["duration"] or meta.get("duration")
    return entries


def rank(entries):
    with_views = [e for e in entries if e["views"] is not None]
    if len(with_views) >= max(3, len(entries) // 2):
        metric = "views"
    elif any(e["likes"] is not None for e in entries):
        metric = "likes"
    else:
        return "none (no counts available: recent order kept)", entries
    ranked = sorted(entries, key=lambda e: (e[metric] is None, -(e[metric] or 0)))
    return metric, ranked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?")
    ap.add_argument("--urls", help="text file of post URLs, one per line")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--scan", type=int, default=60, help="how many recent posts to consider")
    ap.add_argument("--out", default=None)
    ap.add_argument("--cookies-from-browser", dest="cookies")
    ap.add_argument("--list-only", action="store_true")
    ap.add_argument("--entries-json", help=argparse.SUPPRESS)  # offline testing: pre-fetched entries
    args = ap.parse_args()
    if not shutil.which("yt-dlp") and not args.entries_json:
        die("yt-dlp not installed (see doctor.py).")
    if args.entries_json:
        with open(args.entries_json, encoding="utf-8") as f:
            entries = json.load(f)
    elif args.urls:
        with open(args.urls, encoding="utf-8") as f:
            entries = [{"url": u.strip(), "title": None, "views": None, "likes": None, "duration": None}
                       for u in f if u.strip().startswith("http")]
        entries = fill_metrics(entries, args.cookies)
    elif args.url:
        entries = fill_metrics(list_entries(args.url, args.scan, args.cookies), args.cookies)
    else:
        ap.error("give a channel/page URL or --urls")
    if not entries:
        die("no posts found")

    metric, ranked = rank(entries)
    top = ranked[: args.top]
    name = args.out or os.path.join("work", "refs", "top")
    os.makedirs(name, exist_ok=True)
    write_json({"ranked_by": metric, "scanned": len(entries), "top": top}, os.path.join(name, "top_refs.json"))
    print(f"Scanned {len(entries)} posts, ranked by {metric}. Top {len(top)}:")
    for i, e in enumerate(top, 1):
        print(f"  {i:2d}. {e.get(metric) if metric in ('views', 'likes') else '-':>10}  "
              f"{(e.get('title') or '')[:50]:<50}  {e['url']}")
    if args.list_only:
        return
    here = os.path.dirname(os.path.abspath(__file__))
    done = []
    for i, e in enumerate(top, 1):
        out = os.path.join(name, f"{i:02d}")
        print(f"\n[{i}/{len(top)}] measuring {e['url']}")
        proc = subprocess.run([sys.executable, os.path.join(here, "analyze_reference.py"), e["url"], "--out", out])
        if proc.returncode == 0:
            done.append(out)
    print(f"\nMeasured {len(done)}/{len(top)}. Next: python3 {os.path.join(here, 'compare_refs.py')} "
          f"{os.path.join(name, '*')} --out {name}")


if __name__ == "__main__":
    main()
