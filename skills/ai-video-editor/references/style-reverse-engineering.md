# Reverse-engineering a creator's style

Goal: a style card of measured rules, each with a reason and an example timestamp, confirmed across at least 2 of the creator's videos. "Copy by vibes" produces a costume; measuring produces the actual mechanics.

## 1. Get the references

- Store everything under `work/refs/<name>/` in the project folder so later sessions can reuse the measurements.
- Only one reference video? Measure it anyway, but mark every rule "seen once" and tell the user which rules may be one-off choices (a single punch-in, a one-time colour). Ask for a second video before treating them as the creator's style.
- The user only wants a breakdown ("what makes this editing style work?") and no edit: skip the intake questions and go straight to measuring and explaining.
- Ask for 1-3 videos of the same format the user is making (a creator's Shorts and long-form are different styles).
- Download only with the user's go-ahead: `python3 scripts/analyze_reference.py "<url>"` (yt-dlp, at most 1080p). Respect the platform's terms; this is for private analysis, not re-upload. If YouTube blocks yt-dlp (it now sometimes needs a JS runtime or cookies: `--cookies-from-browser chrome`), ask the user to download the file and drop it in.
- Long videos: analyse the first 3 minutes plus one middle chunk; the opening is where styles differ most. `yt-dlp --download-sections "*00:00-03:00"`.

## 2. Measure (the script does the numbers)

`python3 scripts/analyze_reference.py <file> --out work/refs/<name>` produces:

| Measurement | Field | What it tells you |
|---|---|---|
| Cut times, split into hard cuts and jump cuts/punch-ins | `cuts`, `hard_cuts`, `jump_cuts_or_punch_ins` | edit density and how they hide jump cuts |
| Average / median / shortest / longest shot | `avg_shot_len_s` ... | rhythm; a long tail of short shots = energetic |
| Cuts per minute: total, first 30 s, after 30 s, per 30 s window | `cuts_per_min_*`, `pacing_by_30s` | front-loaded hooks show as a high first-30 s rate |
| Loudness, true peak, LRA | `loudness` | mastering target and dynamics |
| Per-second audio level | `audio_level_dbfs_per_second` | music swells, silences used for emphasis |
| Silences | `silences_over_0_4s` | do they leave breaths or cut everything |
| Time-weighted palette | `palette_time_weighted` | brand colours, grade temperature |
| Face on screen %, face size | `face` (needs opencv) | talking head vs B-roll share, framing tightness |

Treat cut detection as an estimate: hard cuts are reliable; jump cuts are detected as frame-difference spikes and can include fast motion. Spot-check 5 detected cuts on the contact sheet.

## 3. Look (the agent does what numbers cannot)

Open `contact.png` (every 2 s), `hook.png` (every 0.5 s for the first 15 s) and `shots/*.jpg`. Write down:

- **Captions:** font family guess (match against the font library in `design-science.md` section 2), case, weight, size as % of frame height (measure pixel height of a capital / frame height), position (y as % of height), words per line, highlight colour and logic, how words appear (pop, fade, karaoke, none), outline/shadow/box.
- **Graphics:** recurring card types, colours (hex from the palette or a zoomed frame), fonts, how they enter and leave, how long they stay, where they sit.
- **Framing and camera:** face size and position, punch-in amounts and frequency, camera moves, aspect.
- **B-roll:** share of runtime, type (receipts, entity, concept, meme), how it is cut in (on the word? L-cuts?).
- **Transitions:** hard cuts vs effects; which effect, how often.
- **Sound (listen if you can, otherwise read the level curve):** music under voice? Changes at sections? SFX on what? Silences before punchlines?
- **First 30 seconds:** write a second-by-second beat list. What changes every few seconds to hold attention? When does the promise land? When does proof appear?
- **Colour:** warm/cool, contrast, saturation, skin treatment.

## 4. Explain each pattern

For every rule write one sentence on why it works for the viewer. Examples:
- "Music cuts out on the punchline so the joke lands in silence."
- "The first 3 s show the result before the explanation, so the viewer knows the payoff is real."
- "Key numbers turn yellow because yellow is the only saturated colour in the frame, so the eye jumps to it."
A rule without a reason gets copied badly, because the editor cannot judge when to break it.

## 5. Confirm across videos

A rule counts only if it shows up in 2 or more videos. Mark single-video observations as "seen once" and do not apply them by default.

## 6. Write the style card and confirm

Fill `assets/style-card-template.md` into `video-edits/<project>/STYLE_CARD.md`. Show it and ask: "Is this the style you mean?" Apply only after a yes. Then map it to tools:
- Cut style -> `plan_cuts.py --style tight|natural|loose` and `--punch` amount.
- Caption style -> nearest of the 10 styles plus a `--style-json` override with the measured font, size, colours and words per line.
- Graphics -> a custom Look block (`looks-library.md`, last section) using the measured palette and fonts.
- Music and loudness -> `finish.py` settings.

## 7. Presets when there is no reference

From `platforms-and-styles.md` Part C (mostly observed, some measured; say "preset" not "measured" to the user):

| Preset | Shot length | Cuts/min | Punch-ins | Captions (closest style) | B-roll | Grade | Sound |
|---|---|---|---|---|---|---|---|
| Hormozi Shorts | 1-3 s | 20-60 | frequent 10-20% | 6 viral | low | dark, crushed blacks | low music, no transition SFX |
| MrBeast (2024+) | ~2.6 s | ~23 | fewer | key moments only | high | bright, saturated | moderate SFX |
| Ali Abdaal Shorts | 2-5 s | 12-30 | mild | 1 clean-caps / phrase reveal, yellow key words | low-medium | desaturated + yellow pop | lo-fi |
| Ali Abdaal long-form | 3-5 s | 12-20 | mild | pop-up text cards | medium | warm, bright | light |
| Johnny Harris / Vox / Dhruv Rathee | 3-5 s | 12-20 | rare | labels, highlighter | very high (maps, paper) | paper textures, grain | score + paper SFX |
| Kurzgesagt | continuous animation | n/a | n/a | minimal | 100% animation | saturated on navy | full score |
| MKBHD | 4-8 s | 8-15 | rare | minimal lower thirds (10 minimal) | ~50% product B-roll | clean dark, red accent | ambient |
| Dan Koe | 5-15 s | 4-12 | none | 10 minimal / 7 documentary | low | moody, desaturated | ambient |
| Ryan Trahan | 2-5 s alternating | varies | some | playful text, counters | high (vlog) | natural | whimsical score |

## 8. Ethics and honesty

Learning a style is normal craft. Copying a creator's logo, intro, music, or exact graphics package is not: build the style from its mechanics and the user's own brand. If the user asks to clone protected assets, say so plainly and offer the mechanics instead.
