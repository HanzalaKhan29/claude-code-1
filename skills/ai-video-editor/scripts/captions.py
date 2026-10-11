#!/usr/bin/env python3
"""Word-timed caption files (ASS for burn-in, SRT for platform upload) in named styles.

Usage:
  python3 captions.py <words_cut.json> --video v1.mp4 --style 6 [--keywords keywords.json]
                      [--highlight key|active|both|none] [--y 0.60] [--burn out.mp4] [--fonts work/fonts]
  python3 captions.py --list                       # show the style catalog
keywords.json: ["profit", "3x", ...]  or  [{"text": "profit", "start": 12.3}, ...] (edited-timeline times).
The agent chooses keywords BY MEANING (max one per caption group).

Highlight modes:
  key     only the chosen key words get the accent, from the moment they are spoken (default when a
          keywords file is given: matches "the important word turns yellow")
  active  every word lights up as it is spoken (karaoke / Hormozi look; default without keywords for
          styles that have an active colour)
  both    key words in the accent + the active word highlighted
  none    plain
Styles (font size is % of frame height; body captions about 4-5%):
  1 clean-caps     ALL CAPS rounded heavy sans, white, soft shadow, 2-4 words, pop-in
  2 lower-serif    lowercase bold sans; key word in light italic serif; no box
  3 pill           white box, dark spoken words, grey upcoming words, low on frame
  4 serif-italic   small lowercase italic serif, soft shadow; the newest word turns heavy
  5 editorial      bold sans; ONE key word as big italic serif in a single accent (lime)
  6 viral          UPPERCASE Montserrat Black, thick outline, yellow highlight, 1-3 words, pops
  7 documentary    small white bold UPPERCASE sans, one line, no colour, no pop
  8 karaoke        bold sans, words light up as spoken (active = accent), 3-5 words
  9 hindi          Devanagari-safe bold sans (Noto Sans Devanagari), white + outline
 10 minimal        sentence case medium sans, 1-2 lines, soft shadow (long-form YouTube)
Any field can be overridden with --style-json card.json (e.g. the creator's measured style card).
Lines never exceed the safe width: groups break before a word that would overflow, then shrink to fit.
The SRT is accessibility-grade by default (sentence case, punctuation, <=42 chars x 2 lines, <=20 cps);
--srt-mode design writes the burned-in groups instead.
"""
import argparse
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import die, probe, read_json  # noqa: E402

BASE = {
    "font": "Inter", "weight": 800, "italic": False, "size_pct": 4.6, "case": "asis",
    "primary": "#FFFFFF", "upcoming": None, "active": None, "outline_pct": 0.0, "outline": "#000000",
    "shadow_pct": 0.25, "shadow": "#000000", "shadow_alpha": 0.55, "box": False, "box_color": "#FFFFFF",
    "box_pad_pct": 0.9, "max_words": 4, "max_chars_line": 22, "lines": 1, "anim": "fade", "tracking": 0.0,
    "key_font": None, "key_italic": False, "key_weight": None, "key_color": None, "key_size_mul": 1.0,
    "active_bold": False, "drop_punct": True, "char_w": 0.42, "fonts": ["Inter:800"],
}

# char_w = average glyph advance per ASS font-size unit, measured with libass on the real fonts
# (Inter ExtraBold mixed 0.38, Montserrat Black caps 0.455, Nunito Black caps 0.49, Inter Bold caps 0.46,
# Playfair italic 0.31, Devanagari 0.22 per codepoint) plus ~10% margin. Wrong fonts = wrong widths, so the
# fonts must actually load (pass --fonts); see ass_font().
STYLES = {
    "clean-caps": dict(font="Nunito", weight=900, case="upper", size_pct=4.8, shadow_pct=0.35, max_words=4,
                       anim="pop", tracking=0.5, char_w=0.53, key_color="#FFE14D", fonts=["Nunito:900"]),
    "lower-serif": dict(font="Inter", weight=800, case="lower", size_pct=4.6, max_words=4, anim="fade",
                        tracking=-0.5, key_font="Instrument Serif", key_italic=True, key_weight=400,
                        key_size_mul=1.15, fonts=["Inter:800", "Instrument Serif:i400"]),
    "pill": dict(font="Inter", weight=700, case="lower", size_pct=3.6, primary="#141414", upcoming="#9A9A9A",
                 box=True, box_color="#FFFFFF", shadow_pct=0.0, max_words=5, max_chars_line=26, anim="none",
                 fonts=["Inter:700"]),
    "serif-italic": dict(font="Playfair Display", weight=400, italic=True, case="lower", size_pct=4.2,
                         shadow_pct=0.3, max_words=5, anim="fade", active_bold=True, char_w=0.36,
                         fonts=["Playfair Display:i400,i800"]),
    "editorial": dict(font="Inter", weight=800, case="asis", size_pct=4.4, max_words=4, anim="fade", tracking=-0.6,
                      key_font="Instrument Serif", key_italic=True, key_weight=400, key_color="#C6FF3D",
                      key_size_mul=1.6, fonts=["Inter:800", "Instrument Serif:i400"]),
    "viral": dict(font="Montserrat", weight=900, case="upper", size_pct=4.8, outline_pct=0.55, shadow_pct=0.3,
                  active="#FFE600", key_color="#FFE600", max_words=3, max_chars_line=16, anim="pop", char_w=0.50,
                  fonts=["Montserrat:900"]),
    "documentary": dict(font="Inter", weight=700, case="upper", size_pct=3.0, shadow_pct=0.2, max_words=7,
                        max_chars_line=34, anim="none", tracking=1.5, char_w=0.50, fonts=["Inter:700"]),
    "karaoke": dict(font="Inter", weight=800, case="asis", size_pct=4.6, outline_pct=0.3, upcoming="#FFFFFF",
                    active="#FFD400", max_words=5, max_chars_line=22, anim="fade", fonts=["Inter:800"]),
    "hindi": dict(font="Noto Sans Devanagari", weight=700, case="asis", size_pct=4.8, outline_pct=0.4,
                  max_words=4, max_chars_line=20, anim="fade", char_w=0.34, fonts=["Noto Sans Devanagari:700"]),
    "minimal": dict(font="Inter", weight=600, case="asis", size_pct=3.6, shadow_pct=0.3, max_words=9,
                    max_chars_line=38, lines=2, anim="fade", drop_punct=False, fonts=["Inter:600"]),
}
IDS = {str(i + 1): k for i, k in enumerate(STYLES)}
FUNCTION_WORDS = {"a", "an", "the", "to", "of", "in", "on", "at", "for", "with", "and", "or", "but", "is", "are",
                  "my", "your", "our", "their", "his", "her", "its", "this", "that", "as", "by", "from", "if", "so"}
FILLERS = {"um", "uh", "umm", "uhh", "erm", "hmm", "uhm"}


def resolve_style(s):
    s = str(s).strip().lower()
    if s in IDS:
        return IDS[s]
    if s in STYLES:
        return s
    die(f"unknown style '{s}'. Use --list.")


WEIGHT_NAMES = {100: "Thin", 200: "ExtraLight", 300: "Light", 500: "Medium", 600: "SemiBold", 800: "ExtraBold",
                900: "Black"}


def ass_font(family, weight):
    """(name, bold flag) libass can actually match. Static font files (Google Fonts, most foundries) register
    their legacy family name: weights 400/700 live in the base family, every other weight is its own family
    ("Montserrat Black", "Inter ExtraBold"). Asking for "Montserrat" at weight 900 silently falls back to
    another installed font, so always request the legacy name."""
    weight = int(round(weight / 100.0) * 100)
    if weight in (400, 700):
        return family, (1 if weight == 700 else 0)
    if weight < 400 and weight not in WEIGHT_NAMES:
        return family, 0
    return f"{family} {WEIGHT_NAMES.get(weight, 'Bold')}", 0


def ass_color(hex_color, alpha=0.0):
    h = hex_color.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    a = int(round(alpha * 255))
    return f"&H{a:02X}{b}{g}{r}".upper()


def esc(t):
    return t.replace("\\", "\\\\").replace("{", "(").replace("}", ")")


def norm(t):
    return re.sub(r"\W", "", t.lower())


def clean_word(t, cfg):
    t = t.strip()
    if cfg["drop_punct"]:
        t = re.sub(r"[,.;:]+$", "", t)
        t = t.replace("—", "").replace("–", "")
    if cfg["case"] == "upper":
        t = t.upper()
    elif cfg["case"] == "lower":
        t = t.lower()
    return t


def text_width(texts, cfg, fs):
    """Rough rendered width in px: glyph count x font size x average advance, plus spaces and tracking."""
    chars = sum(len(t) for t in texts)
    return chars * fs * cfg["char_w"] + max(0, len(texts) - 1) * fs * 0.28 + chars * cfg["tracking"]


def group_words(words, cfg, fs, max_w):
    """Break on breaths (>=250 ms), sentence ends, comma pauses, and BEFORE a word that would exceed the word
    count or the safe width. Never leave a function word (a, the, to...) dangling at the end of a group."""
    groups, cur = [], []
    limit_w = max_w * cfg["lines"]
    for i, w in enumerate(words):
        t = clean_word(w["text"], cfg)
        if cur and (len(cur) + 1 > cfg["max_words"] or
                    text_width([clean_word(x["text"], cfg) for x in cur] + [t], cfg, fs) > limit_w or
                    sum(len(clean_word(x["text"], cfg)) + 1 for x in cur) + len(t) > cfg["max_chars_line"] * cfg["lines"]):
            carry = []
            if len(cur) >= 2 and norm(cur[-1]["text"]) in FUNCTION_WORDS:
                carry = [cur.pop()]
            groups.append(cur)
            cur = carry
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        raw = w["text"].rstrip()
        if (nxt is None or nxt["start"] - w["end"] >= 0.25 or raw.endswith((".", "?", "!", "।"))
                or (raw.endswith(",") and nxt["start"] - w["end"] >= 0.15)):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    merged = []
    for g in groups:
        if merged and (g[-1]["end"] - g[0]["start"] < 0.5) and len(merged[-1]) + len(g) <= cfg["max_words"] \
                and g[0]["start"] - merged[-1][-1]["end"] < 0.25 and \
                text_width([clean_word(x["text"], cfg) for x in merged[-1] + g], cfg, fs) <= limit_w:
            merged[-1].extend(g)
        else:
            merged.append(g)
    return merged


def load_keywords(path, words):
    if not path:
        return set()
    keys = set()
    for k in read_json(path):
        if isinstance(k, dict):
            t = float(k.get("start", -1))
            for i, w in enumerate(words):
                if abs(w["start"] - t) < 0.15 and norm(w["text"]) == norm(k["text"]):
                    keys.add(i)
        else:
            for i, w in enumerate(words):
                if norm(w["text"]) == norm(str(k)):
                    keys.add(i)
    return keys


def ts(t):
    cs = int(round(max(0.0, t) * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def srt_ts(t):
    ms = int(round(max(0.0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def word_markup(text, role, is_key, cfg, H, pop_in, mode, scale_fit):
    """Every word carries a complete tag set (no \\r resets, which would cancel line-level animation).
    role: spoken | active | upcoming (or 'static' when the group is not stepped word by word)."""
    color = cfg["primary"]
    if role == "upcoming" and cfg["upcoming"]:
        color = cfg["upcoming"]
    lit = False
    if mode in ("active", "both") and role == "active" and cfg["active"]:
        color, lit = cfg["active"], True
    if mode in ("key", "both") and is_key and cfg["key_color"] and role != "upcoming":
        color, lit = cfg["key_color"], True
    font, weight, italic = cfg["font"], cfg["weight"], cfg["italic"]
    if is_key and cfg["key_font"] and mode != "none":
        font, weight, italic = cfg["key_font"], cfg["key_weight"] or 400, cfg["key_italic"]
    if role == "active" and cfg["active_bold"]:
        weight = 800
    mul = cfg["key_size_mul"] if (is_key and mode != "none") else 1.0
    size = round(cfg["size_pct"] / 100 * H * mul * scale_fit)
    target = 110 if (lit and cfg["anim"] == "pop" and role == "active") else 100
    if pop_in:
        scale = (f"\\fscx{round(target * 0.82)}\\fscy{round(target * 0.82)}"
                 f"\\t(0,90,\\fscx{round(target * 1.06)}\\fscy{round(target * 1.06)})"
                 f"\\t(90,170,\\fscx{target}\\fscy{target})")
    else:
        scale = f"\\fscx{target}\\fscy{target}"
    fname, bold = ass_font(font, weight)
    return "{" + f"\\1c{ass_color(color)}\\fn{fname}\\b{bold}\\i{1 if italic else 0}\\fs{size}{scale}" + "}" + esc(text)


def split_lines(texts, cfg):
    if cfg["lines"] < 2:
        return [list(range(len(texts)))]
    total = sum(len(t) + 1 for t in texts)
    if total <= cfg["max_chars_line"] or len(texts) < 2:
        return [list(range(len(texts)))]
    best, best_diff = 1, 10 ** 9
    for k in range(1, len(texts)):
        a = sum(len(t) + 1 for t in texts[:k])
        diff = abs(total - 2 * a) + (6 if norm(texts[k - 1]) in FUNCTION_WORDS else 0)
        if diff < best_diff:
            best, best_diff = k, diff
    return [list(range(best)), list(range(best, len(texts)))]


def build(words, cfg, W, H, keys, y_frac, mode, duration):
    fs = round(cfg["size_pct"] / 100 * H)
    vertical = H > W * 1.2
    max_w = W * (0.71 if vertical else 0.80)
    outline = round(cfg["outline_pct"] / 100 * H, 1)
    shadow = round(cfg["shadow_pct"] / 100 * H, 1)
    border_style = 3 if cfg["box"] else 1
    if cfg["box"]:
        outline = round(cfg["box_pad_pct"] / 100 * H, 1)
    outc = cfg["box_color"] if cfg["box"] else cfg["outline"]
    base_name, base_bold = ass_font(cfg["font"], cfg["weight"])
    style_line = (f"Style: Cap,{base_name},{fs},{ass_color(cfg['primary'])},{ass_color(cfg['upcoming'] or cfg['primary'])},"
                  f"{ass_color(outc)},{ass_color(cfg['shadow'], 1 - cfg['shadow_alpha'])},"
                  f"{-1 if base_bold else 0},{-1 if cfg['italic'] else 0},0,0,100,100,"
                  f"{cfg['tracking']},0,{border_style},{outline},{shadow},5,{int(W * 0.08)},{int(W * 0.08)},0,1")
    header = "\n".join([
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2",
        "ScaledBorderAndShadow: yes", "YCbCr Matrix: TV.709", "", "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding",
        style_line, "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ])
    events, design_srt, fits = [], [], 0
    groups = group_words(words, cfg, fs, max_w)
    idx = {id(w): i for i, w in enumerate(words)}
    x, y = W // 2, int(H * y_frac)
    per_word = bool((mode in ("active", "both") and cfg["active"]) or cfg["upcoming"] or cfg["active_bold"]
                    or (mode in ("key", "both") and cfg["key_color"] and not cfg["key_font"]))
    prev_out = -1.0
    for gi, g in enumerate(groups):
        g_in = max(0.0, g[0]["start"] - 0.05, prev_out)
        nxt_in = groups[gi + 1][0]["start"] - 0.05 if gi + 1 < len(groups) else g[-1]["end"] + 0.6
        g_out = min(nxt_in, g[-1]["end"] + 0.5, duration)
        if g_out - g_in < 0.5:
            g_out = min(max(nxt_in, g_in + 0.3), g_in + 0.5, duration)
        if g_out <= g_in:
            continue
        gap_before = g_in - prev_out if prev_out >= 0 else 9.0
        gap_after = (nxt_in - g_out) if gi + 1 < len(groups) else 9.0
        prev_out = g_out
        texts = [clean_word(w["text"], cfg) for w in g]
        gkeys = [idx[id(w)] in keys for w in g]
        if sum(gkeys) > 1:
            first = gkeys.index(True)
            gkeys = [i == first for i in range(len(g))]
        design_srt.append((g_in, g_out, " ".join(texts)))
        lines = split_lines(texts, cfg)
        widest = max(text_width([texts[j] for j in line], cfg, fs) for line in lines)
        scale_fit = min(1.0, max_w / widest) if widest > 0 else 1.0
        scale_fit = max(scale_fit, 0.7)
        fits += scale_fit < 1.0
        steps = range(len(g)) if per_word else [None]
        for k in steps:
            t0 = g_in if (k is None or k == 0) else max(g_in, g[k]["start"])
            t1 = g_out if (k is None or k == len(g) - 1) else min(g_out, g[k + 1]["start"])
            if t1 - t0 < 0.02:
                continue
            first_step, last_step = (k is None or k == 0), (k is None or k == len(g) - 1)
            parts = []
            for line in lines:
                seg = []
                for j in line:
                    role = "static" if k is None else ("spoken" if j < k else ("active" if j == k else "upcoming"))
                    pop = first_step and cfg["anim"] == "pop"
                    seg.append(word_markup(texts[j], role, gkeys[j], cfg, H, pop, mode, scale_fit))
                parts.append(" ".join(seg))
            # fades only where there is real air around the group: a fade between back-to-back groups reads
            # as a grey flicker, and fading a short step dims the word entirely
            fin = 120 if (first_step and cfg["anim"] == "fade" and gap_before >= 0.2) else 0
            fout = 90 if (last_step and cfg["anim"] in ("fade", "pop") and gap_after >= 0.25 and t1 - t0 >= 0.3) else 0
            lead = f"{{\\an5\\pos({x},{y})" + (f"\\fad({fin},{fout})" if fin or fout else "") + "}"
            events.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},Cap,,0,0,0,,{lead}" + "\\N".join(parts))
    return header + "\n" + "\n".join(events) + "\n", design_srt, len(groups), fits


def access_srt(words, duration):
    """Accessibility subtitles: original case and punctuation, cues on sentences/pauses, <=42 chars x 2 lines,
    reading speed <=20 cps (extended into following silence when possible), 1-7 s per cue."""
    cues, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        text = " ".join(x["text"].strip() for x in cur)
        if (nxt is None or w["text"].rstrip().endswith((".", "?", "!", "।")) or nxt["start"] - w["end"] >= 0.6
                or len(text) >= 70 or w["end"] - cur[0]["start"] >= 6.5):
            cues.append(cur)
            cur = []
    out = []
    for ci, c in enumerate(cues):
        text = " ".join(x["text"].strip() for x in c)
        if len(text) > 42:
            words_t = text.split()
            best, bd = 1, 10 ** 9
            for k in range(1, len(words_t)):
                a, b = " ".join(words_t[:k]), " ".join(words_t[k:])
                d = abs(len(a) - len(b)) + (99 if max(len(a), len(b)) > 42 else 0) + \
                    (8 if norm(words_t[k - 1]) in FUNCTION_WORDS else 0)
                if d < bd:
                    best, bd = k, d
            text = " ".join(words_t[:best]) + "\n" + " ".join(words_t[best:])
        start = c[0]["start"]
        nxt = cues[ci + 1][0]["start"] if ci + 1 < len(cues) else duration
        end = max(c[-1]["end"] + 0.2, start + 1.0, start + len(text) / 20.0)
        end = min(end, nxt - 0.04, duration, start + 7.0)
        if end > start:
            out.append((start, end, text))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words", nargs="?")
    ap.add_argument("--video", help="edited video (for resolution and duration); or give --size")
    ap.add_argument("--size", help="WxH, e.g. 1080x1920")
    ap.add_argument("--style", default="1")
    ap.add_argument("--style-json", help="override fields, e.g. measured creator style")
    ap.add_argument("--keywords")
    ap.add_argument("--highlight", choices=["auto", "key", "active", "both", "none"], default="auto")
    ap.add_argument("--y", type=float, help="vertical centre of captions as fraction of height")
    ap.add_argument("--max-words", type=int)
    ap.add_argument("--accent", help="hex colour for the highlight")
    ap.add_argument("--srt-mode", choices=["access", "design"], default="access")
    ap.add_argument("--out", help="output .ass path (default next to words file)")
    ap.add_argument("--burn", help="also burn into this output video (needs --video)")
    ap.add_argument("--fonts", default="work/fonts", help="folder with .ttf files for burn-in")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        for i, (k, v) in enumerate(STYLES.items(), 1):
            print(f"{i:>2} {k:<13} font={v.get('font')} {v.get('weight')} case={v.get('case', 'asis')} "
                  f"size={v.get('size_pct')}%H max_words={v.get('max_words')} fonts={v.get('fonts')}")
        return
    if not args.words:
        ap.error("words json required")
    name = resolve_style(args.style)
    cfg = dict(BASE)
    cfg.update(STYLES[name])
    override = read_json(args.style_json) if args.style_json else {}
    cfg.update(override)
    if "font" in override and "fonts" not in override:
        cfg["fonts"] = [f"{cfg['font']}:{cfg['weight']}"]
    if args.max_words:
        cfg["max_words"] = args.max_words
    if args.accent:
        for f in ("active", "key_color"):
            if cfg[f]:
                cfg[f] = args.accent
        if not cfg["active"] and not cfg["key_color"]:
            cfg["key_color"] = args.accent

    duration = float("inf")
    if args.video:
        info = probe(args.video)
        W, H, duration = info["width"], info["height"], info["duration"]
    elif args.size:
        W, H = (int(v) for v in args.size.lower().split("x"))
    else:
        die("give --video or --size")
    # 9:16 default 0.60 keeps captions inside the cross-platform safe box (y 288-1248 of 1920): Meta reserves
    # the bottom 35%, TikTok/Shorts put description + buttons there. 16:9 sits low; 1:1/4:5 in between.
    y = args.y if args.y is not None else (0.60 if H > W * 1.2 else (0.78 if abs(H - W) < W * 0.3 else 0.86))

    words = read_json(args.words)
    if isinstance(words, dict):
        words = words.get("words", [])
    words = [w for w in words if norm(w["text"]) not in FILLERS and w["start"] < duration]
    keys = load_keywords(args.keywords, words)
    mode = args.highlight
    if mode == "auto":
        mode = "key" if (keys and (cfg["key_color"] or cfg["key_font"])) else ("active" if cfg["active"] else
                                                                              ("key" if keys else "none"))
    ass, design, n_groups, fits = build(words, cfg, W, H, keys, y, mode, duration)

    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.words)), f"captions_{name}.ass")
    with open(out, "w", encoding="utf-8") as f:
        f.write(ass)
    srt_rows = access_srt(words, duration) if args.srt_mode == "access" else design
    srt_path = os.path.splitext(out)[0] + ".srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, (a, b, t) in enumerate(srt_rows, 1):
            f.write(f"{i}\n{srt_ts(a)} --> {srt_ts(b)}\n{t}\n\n")
    print(f"Wrote {out} ({n_groups} caption groups, style {name}, highlight={mode}, {W}x{H}, y={y}; "
          f"{fits} group(s) shrunk to fit the safe width) and {srt_path} ({args.srt_mode} SRT)")
    if keys and mode in ("active", "none"):
        print("NOTE: keywords were given but highlight mode ignores them; use --highlight key or both.")
    have = {f.rsplit(".", 1)[0].lower() for f in os.listdir(args.fonts)} if os.path.isdir(args.fonts) else set()

    def font_files(spec):  # "Playfair Display:i400,i800" -> playfairdisplay-400italic, ... (fetch_fonts naming)
        fam, _, ws = spec.partition(":")
        fam = fam.replace(" ", "").lower()
        return [f"{fam}-{w.lstrip('i')}{'italic' if w.startswith('i') else ''}" for w in (ws or "400").split(",")]
    missing = [s for s in cfg["fonts"] if not all(n in have for n in font_files(s))]
    if missing:
        print("WARN fonts missing (libass will silently substitute a system font and widths will be off):",
              ", ".join(missing), "-> python3 fetch_fonts.py " + " ".join(f'"{s}"' for s in missing) +
              f" --dir {args.fonts}")

    if args.burn:
        if not args.video:
            die("--burn needs --video")
        sub = out.replace("\\", "/").replace(":", "\\:")
        fdir = os.path.abspath(args.fonts).replace("\\", "/").replace(":", "\\:")
        vf = f"subtitles='{sub}':fontsdir='{fdir}'" if os.path.isdir(args.fonts) else f"subtitles='{sub}'"
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostats", "-y", "-i", args.video, "-vf", vf,
               "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
               "-g", str(round(info["fps"])), "-c:a", "copy", "-movflags", "+faststart", args.burn]
        if subprocess.run(cmd).returncode != 0:
            die("burn-in failed")
        print(f"Burned captions -> {args.burn}. Check: python3 qa.py {args.burn} --captions {out}")


if __name__ == "__main__":
    main()
