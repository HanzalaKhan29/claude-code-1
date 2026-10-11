# Captions and subtitles

Contents: 1 Two kinds of caption · 2 The caption model (drop / rail / embed) · 3 The 12 styles · 4 Sizing and placement · 5 Grouping and timing · 6 Key words · 7 Legibility on footage · 8 Hindi and Hinglish · 9 Designed captions with HyperFrames · 10 Self-check · 11 Selective captioning and type tiers (2026)

## 1. Two kinds of caption

- **Accessibility subtitles** (`.srt` / `.vtt` uploaded to YouTube): complete, verbatim enough to follow, readable at 17-20 characters per second, at most 2 lines of 42 characters (Netflix/BBC). Always export one (`captions.py` writes it next to the `.ass`): it helps deaf and hard-of-hearing viewers, non-native viewers, and search.
- **Design captions** (burned into the picture): part of the edit's style. Short groups, word-timed, one highlighted word. Mandatory for Shorts/Reels/TikTok because most phone viewing starts muted (69% of US viewers watch with sound off in public, self-reported [INDUSTRY, Verizon 2019]).

## 2. The caption model: drop / rail / embed

From HeyGen's embedded-captions skill (Apache-2.0). Every spoken phrase is one of:

| Role | What | Shown as |
|---|---|---|
| **drop** | filler: um, uh, stutters, self-corrections | not shown |
| **rail** | ordinary speech (most of it) | clean caption in front, readable; one punch word may get an inline highlight |
| **embed** | the rare headline beat | one big word composited behind the speaker (needs a matte) |

The rail carries most of the text. Embedding is earned: at most one per thought, never two on screen together, a beat of air between them, at most one "apex" per section. Embedding every word is the classic mistake.

## 3. The 12 styles (`scripts/captions.py --list`)

Sankhla's 7, plus 3 additions, plus 2 measured from the motion-reels pages (`motion-reels.md`). Fonts are Google Fonts (OFL), fetched with `fetch_fonts.py --style N`.

| # | Name | Font | Look | Best for |
|---|---|---|---|---|
| 1 | clean-caps | Nunito 900 | ALL CAPS rounded heavy sans, white, soft shadow, 2-4 words, pops in | friendly Shorts, education |
| 2 | lower-serif | Inter 800 + Instrument Serif italic | lowercase bold sans, key word in light italic serif, no box | aesthetic, lifestyle, personal brand |
| 3 | pill | Inter 700 | white box, dark spoken words, grey upcoming words, low on frame | tutorials, calm explainers |
| 4 | serif-italic | Playfair Display italic 400/800 | small lowercase italic serif, the newest word turns heavy | poetic, reflective, fashion |
| 5 | editorial | Inter 800 + Instrument Serif italic | bold sans, ONE key word as big italic serif in lime #C6FF3D | premium creators, commentary |
| 6 | viral | Montserrat 900 | UPPERCASE, thick black outline, active word yellow #FFE600, 1-3 words, pops | hype Shorts, business clips (Hormozi family) |
| 7 | documentary | Inter 700 | small white bold UPPERCASE, tracked, one line, no colour, no pop | serious, documentary, calm premium |
| 8 | karaoke | Inter 800 | words light up in the accent as spoken, 3-5 words | music, fast talkers, engagement |
| 9 | hindi | Noto Sans Devanagari 700 | Devanagari-safe, outline, extra line height | Hindi videos |
| 10 | minimal | Inter 600 | sentence case, up to 2 lines, soft shadow | long-form YouTube |
| 11 | kinetic | Inter 700 + Anton | two-tier: small lowercase whisper words revealed one by one at centre, key words ALONE as apex words (Anton caps ~18% of frame height, lime #DDF53D), hard pops | motion reels (metromedia / earnera grammar); use `--selective` |
| 12 | feed | Inter 800 | typewriter feed: active line bright at centre, previous and next lines dimmed above/below | quote breakdowns, earnera-style reels |

Override anything with `--style-json`, for example a measured creator style:
`{"font": "Satoshi", "weight": 900, "case": "upper", "size_pct": 5.2, "active": "#00E676", "max_words": 2, "fonts": []}`
(Fontshare fonts like Satoshi cannot be redistributed; the user downloads them from fontshare.com into the fonts folder.)

ASS limits to know: the pill box has square corners (libass cannot round them); per-word background boxes, gradients, blur and glows need the HyperFrames route (section 9).

## 4. Sizing and placement

- "Size" here always means the font size (the em, what `size_pct` and ASS `Fontsize` set), not the cap height. Capitals are about 0.7 em tall, so a 92 px caption has roughly 65 px capitals. When matching a reference, calibrate by the measured width of a line of text, not by eye on letter height.
- The fonts must actually load. libass substitutes a system font silently when a family or weight is missing, and the result looks almost right but wider or narrower. `captions.py` prints a WARN when the style's font files are missing from `--fonts`; fetch them with `fetch_fonts.py`. Weights other than 400/700 are requested by legacy names ("Montserrat Black"), which the script handles.
- Body captions: font size about 4.5-5% of frame height (48-55 px at 1080p landscape; 86-96 px at 1080x1920). Hook/punch size: 6-9%. Never below 2.6% (28 px at 1080) for anything that must be read.
- 16:9: centred low (script default y = 0.86), but keep the bottom ~12% free of critical text on YouTube (progress bar, auto-captions).
- 9:16: centred around y = 0.60 (1150 px of 1920). Cross-platform safe box for anything that must be read: x 120-888, y 288-1248. Below 1248 the TikTok/Reels/Shorts description and buttons cover it; the right rail (x > 780 from y 840 down) holds like/comment/share. Platforms publish no official organic pixel specs, so these are measured values that change: re-check templates for ads.
- Faces: captions never cover the eyes or mouth. Speaker's eyes around 30-40% from the top in 9:16 so captions sit below the chin. If a frame shows overlap, move the captions (`--y`) for that video rather than shrinking them.
- Hook text (first 1-3 s of a Short): upper middle, y about 300-600. Never two text blocks competing: while a hook title or a graphic with words is on screen, either hide the captions for those seconds or keep the two clearly separated (title top, captions low), never stacked at the same height.
- Face fills the frame (tight vertical close-up): there is no room below the chin, so put captions in the upper third (y about 0.25-0.30) or on the chest only if the mouth stays clear. Check a frame; the default y is a starting point, not a rule.

## 5. Grouping and timing

- Break groups at pauses of 250 ms or more, at sentence ends, at commas followed by a pause, and at the style's word limit. Never span a breath.
- Each group on screen at least 0.5 s (0.8 s preferred); merge shorter ones.
- Enter about 50 ms before the first word; leave at most 0.5-0.6 s after the last word or when the next group starts.
- Reading speed: at most 17-20 characters per second; if the speaker is faster than about 180 words per minute, condense rather than flash.
- Word highlight changes on the word onset (within 1 frame); timing must stay within about 80 ms of the transcript.
- Honour silence: during a rhetorical pause of 1.5 s or more, do not keep the old caption lingering.
- Do not caption filler; fold self-corrections to the final version. Do not show "[laughs]" in design captions.

## 6. Key words (choose by meaning)

The highlight works only because it is rare (pop-out needs one unique element among neutrals [STRONG]).

- The user's explicit request wins over these defaults ("highlight every word as it is spoken" means `--highlight active`). Modes: `key` (only keywords.json words), `active` (the word being spoken), `both`, `none`; `auto` picks from the style.
- At most one highlighted word per caption group; roughly 70% of groups plain, 20% with a slight lift, 8% a full highlight, 2% a climax.
- Pick the word that carries the meaning of the sentence: the number, the outcome, the surprising noun, the contrast word. Not the loudest word, not a random word, not every noun.
- Write them to `work/keywords.json`, either as plain words (`["3x", "profit"]`, matches every occurrence) or with times (`[{"text": "profit", "start": 12.3}]`, exact occurrence, edited timeline).
- Same accent colour as the rest of the edit's graphics.

Two subtitle files come out of every run. `--srt-mode access` (default) writes a proper accessibility SRT: up to 42 characters x 2 lines, at most 20 characters per second, sentence case, for YouTube upload and search. `--srt-mode design` writes the same short groups that are burned in (useful when a platform wants a sidecar that matches the picture).

## 7. Legibility on footage

- Text needs a luminance difference from the pixels behind it, not just a different hue: compression halves colour resolution.
- Options in order of elegance: soft shadow (`0 2px 10px rgba(0,0,0,.65)` + tight contact shadow), 2-4 px outline at 1080p, a narrow gradient scrim, a box. Never strokes under 2 px (they blur into a grey halo after YouTube re-encoding).
- Brightness probe from embedded-captions: sample the caption region; average luma under 60 = light text as is; 60-180 = add shadow or scrim; over 180 (bright walls, sky) = dark text or an opaque plate.
- No weight under 400 below 60 px at 1080p; Didone hairline serifs (Playfair, Bodoni) only at large sizes.
- Italics in motion read as "tilted", so italic styles use italics for single key words, held at least 0.6 s.

## 8. Hindi and Hinglish

- Transcribe Hindi with `--language hi --model large-v3` (or large-v3-turbo); Parakeet does not support Hindi. Whisper may output Devanagari or translate: decide with the user which script the captions use.
- Hinglish (romanized Hindi + English): prime with `--prompt` containing a few lines of the user's own romanized phrasing; or use Oriserve's Whisper-Hindi2Hinglish model for romanized output (see `tooling-research.md`). For the most accurate word timing in Hindi, WhisperX with the Hindi wav2vec2 aligner, or stable-ts `align()` against a corrected script.
- Devanagari needs about 15-20% more line height (matras above and below). Fonts with coverage: Noto Sans Devanagari, Mukta, Hind, Baloo 2, Poppins.
- Mixed-script captions: pick one script per video; switching scripts mid-video slows reading.
- libass needs HarfBuzz shaping for correct conjuncts (standard in current ffmpeg builds): check a conjunct-heavy frame visually.

## 9. Designed captions with HyperFrames

When the style needs web-only looks (rounded pills per word, gradients, behind-the-subject text, per-letter physics):
- Plain designed captions: registry items `caption-highlight`, `caption-pill-karaoke`, `caption-kinetic-slam`, `caption-editorial-emphasis`, `caption-weight-shift` (`npx hyperframes catalog captions`, `npx hyperframes add <name>`), driven by `words_cut.json`, rendered as a transparent MOV and composited last with `overlay.py`.
- Cinematic captions behind the speaker: the official `/embedded-captions` workflow (35 identities, subject matting, safe zones, timing gates). Refuses clips with multiple speakers, burned-in text or garbage transcripts, which is the right call.
- `npx hyperframes check --caption-zone "x0=0;y0=0.82;x1=1;y1=1;severity=error"` tests captions against a zone.

## 10. Self-check before rendering (from embedded-captions' 18 rules)

- Does the face or the caption read first? The face should.
- More than one font family or two weights? More than one accent colour?
- Letter-spacing or blur animating on entrance? (causes line jumps; animate transform/opacity only)
- Same stagger for a calm documentary and a hype Short? (40 ms reads urgent, 80 ms conversational, 150 ms deliberate, 250 ms+ ceremonial)
- Every group emphasised? Then nothing is.
- 30 s or more with no change of rhythm? Plant one rhythm break (a word at 2x, a beat of silence with no caption).
- Any caption inside a platform UI zone or over the face? Check `qa.py --captions` sheet.

## 11. Selective captioning and type tiers (2026)

- **Genre decides full vs selective.** Talking-head Shorts and Reels keep full word captions (styles 1-10):
  people start muted, and the speech is the content. **Motion-graphics reels caption 25-40% of words**, only on
  beats (claims, numbers, turns, openings), measured on all four reference pages: constant text gets filtered
  like a watermark. `captions.py --style 11 --keywords k.json --selective` keeps groups with a key word or a
  number plus the setup words leading into a solo apex word, and prints the share (target 25-40%). The SRT
  sidecar stays complete either way.
- **One font per tier, three tiers max** (whisper/body, apex/display, label/mono), each with a job. This
  replaces the old "one font only" rule: 2026 premium work is tiered (serif-italic display + grotesque body +
  mono labels in one video).
- **Emphasis budget: at most about 10% of words get premium emphasis** (box, gradient, underline bar,
  blur-reveal); the rest pop or stay plain. Hero words up to about 2.4x body size, one or two per beat, never
  three in a row, at most about 15 characters.
- **2025-26 emphasis treatments** (build in HyperFrames; ASS cannot do them well):
  underline-bar highlight (solid accent bar behind/below the active word, the word flips to the ground colour:
  two independent codebases converge, so ship it); gradient-fill active word with tight tracking (-20 to -25)
  at large sizes only (it reads broken under ~60 px); word box (solid box behind the active word); blur-reveal
  on a Difference blend (blur is the transition, the word resolves sharp: allowed, unlike blur as a style);
  traveling highlight (the highlight slides from word to word: two staggered timelines, one hides word A's
  bar while word B's expands).
- **Karaoke has three distinct mechanics; do not blend them:** (a) fill sweep inside each word's bounds,
  (b) active word bright with neighbours dimmed (style 12 is the line-level version), (c) pun strike-and-
  replace (the word strikes through and swaps).
- **Placement ruling:** the default stays y = 0.60 on 9:16 (inside the safe box, floor at y 1248 of 1920). A
  2026 claim that UGC captions now sit at y 0.70-0.78 comes from a single source and collides with TikTok's
  bottom UI; use it only as an opt-in (`--y 0.72`) after checking the frame, never silently.
- **Stroke units:** the 2-4 px outline rule is libass outline units at 1080p; caption-code guides quote 8-12 px
  strokes at 74 px type in CSS pixels. Different units, same physics: stroke first, then fill.
- **Bilingual captions** (CapCut / Edits auto-translate, July 2026): two-line bilingual captions are now a
  native option. QC rule: the translation reads what the speech model heard, so a misheard word ships in both
  languages. Fix `words.json` first, then translate.
