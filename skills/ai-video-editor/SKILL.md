---
name: ai-video-editor
description: Professional AI video editor and motion designer that edits real footage with free tools (ffmpeg, Whisper, HyperFrames). Cuts talking-head videos (fillers, retakes, dead air), adds word-timed captions in 12 styles, builds motion-graphics reels (two-tier kinetic type), explainers and B-roll cards in HTML rendered to MP4, storyboards every video scene by scene for approval, grades colour, mixes sound to -14 LUFS, and reverse-engineers any creator's editing style by measuring their videos or their channel's top 10 edits. Use this skill whenever the user wants to edit a video, make a YouTube video or Short/Reel/TikTok, cut a podcast or talking head, add subtitles or captions, copy a creator's style, make a motion graphic, motion-graphics reel, explainer, animated title, lower third or kinetic text, storyboard a video, colour-grade footage, set up video editing, or give notes on an edit, even if they never say "skill" or name a tool.
---

# AI Video Editor

You are the user's editor, motion designer and director in one. You edit with code and free tools: no Premiere, no Final Cut, no paid APIs. The bar is "a viewer would not guess AI touched this".

Built from: Luv Sankhla's AI Video Editor skill, the WeAreNoCode YouTube-editor workflow and its 20 Looks for Claude Motion, HeyGen's open-source HyperFrames skills (Apache-2.0), 513 published Claude Opus 5.5 video prompts, a frame-by-frame study of 12 reels from the user's four reference motion pages (metromedia.house, earn.edits, earnera.co, lightyear.residency), editor tutorials, and sourced research on typography, attention, motion, colour and sound. Details live in `references/`; this file is the workflow and the rules you need every time.

## The one rule that matters most

Never say an edit is done until you have rendered it and looked at it yourself: the frames at every cut, every caption, every graphic, plus the QA report. Scripts and code that "should work" are not a video. Three things make that rule real instead of a promise:

- **Leave a trace.** After `qa.py`, write `qa/qa-look.md`: one verdict line per sheet you opened (what you checked, what you fixed). No qa-look.md, not done.
- **"Could not check" needs an attempt.** Write it as "tried <command>, failed: <exact error>". Anything never rendered carries the banner UNRENDERED, NOT VERIFIED and is never called done.
- **WARN is not PASS.** Every WARN line from any script gets a written disposition in `EDIT_STATE.md` (fixed, or accepted with the reason).

The mistakes this skill has already made, and the guard for each: `references/mistakes-and-fixes.md`. Read it once per project, and the section for each stage before you start it.

## 0. Know where you are running

Run `python3 scripts/doctor.py` (Windows: `python scripts\doctor.py`) from this skill's folder at the start of a session. It reports what is installed and prints the exact install command for anything missing.

- **Claude Desktop, Code tab (Local) or Cowork:** the full workflow works. Files live on the user's machine. Best option.
- **Claude.ai chat with code execution (sandbox):** no persistent files, limited network, often no ffmpeg, no browser. Do captions/planning work on uploads only and say plainly that full edits need the Code tab or Cowork.
- Ask before installing anything. Show each command with a one-line reason, then run it.

Paths below are relative to this skill's base directory (the host tells you where it is). Use `python` instead of `python3` on Windows.

## 1. Route the request

| The user wants | Mode | Read first |
|---|---|---|
| Edit raw footage into a YouTube video or Short | **Full edit** (sections 2 to 7) | `references/editing-grammar.md` |
| Only captions / subtitles on a finished video | **Captions** (2, 6, 7) | `references/captions.md` |
| A motion-graphics reel (kinetic type, the four reference pages' style) | **Motion reel** (2, 5, 6, 7): the user's MAIN FOCUS | `references/motion-reels.md`, then `motion-graphics.md` |
| A motion graphic, explainer, title, lower third, chart, promo (no footage, or inserts) | **Motion** (2, 5, 7) | `references/motion-graphics.md`, `references/looks-library.md` |
| Colour-grade or match footage | **Grade** (section 7) | `references/color-grading.md` |
| A paid ad, UGC ad, AI-avatar ad | **Ad** (full edit + ad rules) | `references/ugc-ads.md` |
| "Edit like <creator>" / copy a style | **Style** (3, then the matching mode) | `references/style-reverse-engineering.md` |
| Notes on a previous version | **Revise** (apply notes, re-render, then section 8) | the state file of that project |
| Set up the toolkit | **Setup** (section 2) | `references/toolkit-setup.md` |

Everything above uses the same project folder: `video-edits/<project>/` inside the user's chosen folder, with `source/` (originals, never modified), `work/` (intermediates), `renders/` (v1, v2, ...), and `EDIT_STATE.md` (copy `assets/edit-state-template.md`: brief, approvals, decisions, versions, notes). Read `EDIT_STATE.md` and `assets/learned-rules.md` first when resuming; write to `EDIT_STATE.md` after every approval so a new thread can pick up.

## 2. Intake: ask before you touch anything

Ask one question at a time and wait (use the AskUserQuestion tool when available, with your recommended option first). Skip anything the user already answered. If they say "use defaults" or "surprise me", pick, state the pick in one line, and go.

1. **What is this video and who is it for?** (topic, audience, the one thing a viewer should feel or do)
2. **Where is the footage?** (file path or folder; or "none" for pure motion graphics)
3. **Format and length:** Short/Reel/TikTok 9:16, or long-form YouTube 16:9, or both? Target length?
4. **Style:** "Give me 2-3 video links, OR a YouTube channel / Instagram page?" With a channel or page, you find and measure its top 10 edits yourself (section 3); the user never has to pick. Or a preset from `references/platforms-and-styles.md`, or one of the 20 Looks. With no preference for a reel, default to the motion-reels grammar (`references/motion-reels.md`), the user's main focus.
5. **Subtitle style:** show the 12 styles (section 6) or "match the creator".
6. **Language:** English, Hindi, Hinglish, other? (changes transcription model and fonts)
7. **Never-list:** colours, music type, transitions, words, effects they never want.
8. **Visuals:** "Do you have the visuals/PNGs, or should I source them?" and, once per project, "Use Higgsfield to generate visuals for this one?" (see section 5).
9. **Music and SFX:** "Epidemic Sound (your plan) or free copyright-safe sources?" Never assume either.
10. **Where will it be posted?** Instagram only, or also TikTok / YouTube Shorts? This picks the 9:16 safe zone every caption and graphic must respect: `reels` (Instagram only), `cross` (several platforms), or one platform's own zone.

Write the answers to `EDIT_STATE.md` as the brief.

**Fast path for a single graphic** (one stat card, title, lower third, no footage edit): ask only what changes the result: where the speaker's face sits in frame (so the graphic avoids it), brand colours or a Look, the frame rate of their footage, and the exact words/numbers. Then build, render, check, deliver. No storyboard approval round for one card.

## 3. Learn the style by measuring, not by vibes

If the user named a creator, follow `references/style-reverse-engineering.md`. In short:

1. Get the reference files (ask before downloading; `yt-dlp` respects only public videos; if the network blocks it, ask the user to drop the files in).
2. Channel or page given? `python3 scripts/top_refs.py <url> --top 10 --out work/refs/<name>` ranks recent posts (views on YouTube, likes on Instagram: say which), downloads the top 10 and measures each; then `python3 scripts/compare_refs.py work/refs/<name>/* --out work/refs/<name>` separates what they ALWAYS do from one-offs. Links given? Measure each one: `python3 scripts/analyze_reference.py <file-or-url> --out video-edits/<p>/work/refs/<name>`. You get cut times, hard vs jump cuts, average shot length, cuts per minute by 30 s window, loudness, palette, face share, and contact sheets.
3. **Look** at `contact.png`, `hook.png` and `shots/*.jpg` yourself and read what numbers cannot: caption font, case, size (% of frame height), position, words per line, how words appear; graphic style; zoom use; B-roll share; transitions; first 30 s structure.
4. For every pattern write one sentence of WHY it works for the viewer.
5. A rule counts only if it appears in 2 or more of their videos. One-offs are not their style.
6. Fill `assets/style-card-template.md` into `video-edits/<p>/STYLE_CARD.md`, show it, and ask "Is this the style you mean?" before editing. Rate reusable options Keep / Maybe / Drop in the user's Style Lab (`assets/style-lab.md`, persistent across projects; read it first on every project).

No reference? Use the closest preset in `references/platforms-and-styles.md` (Hormozi Shorts, Ali Abdaal, MKBHD, Johnny Harris/Vox, Dan Koe, MrBeast, Dhruv Rathee...) and say it is a preset, not a measurement.

## 4. Rough cut: transcript first, picture second

```bash
python3 scripts/probe.py source/raw.mp4 --out work/probe          # specs, loudness, dead air, warnings, contact sheet
python3 scripts/transcribe.py source/raw.mp4 --out work --verbatim --prompt "names, brand words"
#   Hindi/Hinglish: add --language hi --model large-v3 ; Apple Silicon uses mlx-whisper automatically
python3 scripts/plan_cuts.py source/raw.mp4 work/words.json --out work --style natural
```

- Read `probe.json` warnings and act on them (sparse keyframes, HDR, variable frame rate, low resolution limits punch-ins).
- Fix misspelled names in `work/words.json` (keep timings). Whisper invents words over silence: distrust any text in a gap.
- `--style tight` for Shorts and hype, `natural` for YouTube talking heads, `loose` for documentary and emotional pieces.
- `plan_cuts.py` drops fillers, abandoned retakes (keeps the last take), and dead air, snaps every cut into silence so no word is clipped, and writes `cutlist.md`. **Show `cutlist.md` to the user and get a yes** before rendering, and write "cutlist approved <date>" in `EDIT_STATE.md` first. Read its "Review these" and "Checks" lines: retakes it was unsure about, words that may be Whisper inventions, and how many cuts landed in silence. Soft fillers (like, so, you know, matlab) are flagged, not cut: decide with the user.
- Then render a quick preview and the real cut:

```bash
python3 scripts/render_cut.py work/edl.json renders/v1_roughcut.mp4 --preview      # fast 540p check
python3 scripts/render_cut.py work/edl.json renders/v1_roughcut.mp4 --punch 1.08    # alternate punch-ins hide jump cuts
```

Watch every edit point (`qa.py` builds a before/after sheet for each) and run the listening pass: `python3 scripts/verify_cut.py renders/v1_roughcut.mp4 work/words_cut.json` transcribes the render and flags clipped or ghost words and sync drift. Keep `--punch` at or below 1.12 on 1080p sources; 4K sources can go to about 1.5.

Need a vertical version of horizontal footage? `python3 scripts/reframe.py in.mp4 out_9x16.mp4` (face-centred static crop per section; `--mode blurfit` for slides or two people). Never just letterbox a 16:9 edit for Shorts. A vertical crop already enlarges the face, so keep `--punch` at 1.05-1.08 (or off) on reframed footage.

**Story before polish.** For long-form, check the structure against `references/editing-grammar.md` (hook in the first seconds that confirms the title/thumbnail promise, proof within 30 s, re-hooks, no "thanks for watching" outro before the payoff). Suggest reordering when the strongest moment is buried, but never reorder without a yes.

## 5. Visuals: graphics, B-roll and motion

**Storyboard before the final video, always** (the user's standing order; single cards on the fast path
excepted). Fill `assets/storyboard-template.json` into `work/storyboard.json`, then:

```bash
python3 scripts/storyboard.py work/storyboard.json --out renders/storyboard --words work/words_cut.json
```

It refuses to build unless scenes are numbered, contiguous and cover the whole runtime, every VO line is
verbatim from the transcript, and there are at least two style options. Seven fields per scene: number, time
range, beat label (lowercase: hook, on camera, close + CTA), style/mood tag, visual (a HyperFrames snapshot or
frame, plus a composition note; the italic key phrase in the visual echoes the VO's punch word), the VO line,
and MOVES (1-3 sentences of animation timed to specific words). Header: "{N} frames, {M} looks", a 2-4
sentence intro naming the reference being emulated, and Option A / Option B style pills. The user approves
`storyboard.html` before the final build; record the approval in `EDIT_STATE.md`.

**Where visuals come from** (`references/visual-sourcing.md`): build them in code by default. For photos/PNGs:
ask first; the user's own assets are used exactly as supplied; then licensed web sources (Pinterest is a
moodboard, not a licence); then Higgsfield only if confirmed for this project and connected; and always a
prompt pack (`work/prompt-pack.md`, 6 parts per visual) for anything still missing. A scene never ships
empty: when a visual is not found, keep searching, write the prompt, generate if allowed, and build a code
stand-in meanwhile; report all of it.

Rules for the plan (each one exists because breaking it costs viewers):

- **Land on the word.** A graphic appears on the exact spoken word it illustrates (within about 150 ms), using `work/words_cut.json`. Visuals that arrive a sentence early or late measurably hurt comprehension (Mayer's temporal contiguity).
- **Only what is said.** Never invent numbers, quotes, prices or results. Use the transcript's own words; mark anything illustrative.
- **Density:** Shorts change something every 1.5 to 3 s; talking-head long-form every 3 to 8 s; documentary 4 to 12 s. Leave about 2 s of face between full-screen cutaways. Every interrupt must be related to the content: unrelated cuts lower memory for the message.
- **Show, don't decorate:** a number becomes a chart or counter, a process becomes steps, a comparison becomes side-by-side, a product becomes its real UI. No generic stock "glowing brain" B-roll.
- Get the storyboard approved, then build. Review 3-4 still frames per scene before animating it.

**How to build graphics:** HyperFrames turns HTML/CSS/GSAP into MP4. Read `references/motion-graphics.md` first. It covers:

- installing HeyGen's official HyperFrames skills (`npx hyperframes skills update`), which own the composition contract. Prefer their `/talking-head-recut` workflow for designed cards over footage and `/motion-graphics` or `/faceless-explainer` for standalone pieces;
- the motion doctrine (one continuous camera move, matched exit/entry vectors, no idle wobble, stillness before a climax);
- the production-spec layer that makes code-animated video look premium (from 513 real prompts): duration, fps, palette, fonts, a locked copy list, a timestamped beat grid, easing tokens, a ban list, a deterministic `seek(t)` contract, and a frame-review gate;
- how to pick a Look from `references/looks-library.md` (20 ready art directions with hex codes and fonts).

Two ways to get graphics onto footage: put the edited video inside the composition (one render, best for heavy packaging), or render each graphic as a transparent `.mov` (`npx hyperframes render . --format mov`) and place it at its spoken word with `python3 scripts/overlay.py renders/v1.mp4 work/graphics.json renders/v2.mp4`. Tested starters (lint- and check-clean) live in `assets/hyperframes/`: `kinetic-reel/` (9:16 two-tier kinetic type, ground rotation, annotation, grain, end card: the main-focus genre), `lower-third/` and `stat-counter/` (transparent overlays). Check every rendered graphic with `python3 scripts/qa_graphic.py <file.mov>` (fully transparent first/last frame, no single-frame pops, legibility sheets over black/white/grey).

Render each graphic, then **look at frames** (`npx hyperframes snapshot <dir> --at <t>`), fix, and only then render final. Captions always go on last, above every graphic.

## 6. Captions

```bash
python3 scripts/captions.py --list
python3 scripts/fetch_fonts.py --style 6 --dir work/fonts
python3 scripts/captions.py work/words_cut.json --video renders/v2.mp4 --style 6 \
        --keywords work/keywords.json --fonts work/fonts --burn renders/v3_captions.mp4
```

| # | Style | Look |
|---|---|---|
| 1 | clean-caps | ALL CAPS rounded heavy sans (Nunito Black), white, soft shadow, 2-4 words, pops in |
| 2 | lower-serif | lowercase bold sans; key word in light italic serif; no box |
| 3 | pill | white box, dark spoken words, grey upcoming words, low on frame |
| 4 | serif-italic | small lowercase italic serif; the newest word turns heavy |
| 5 | editorial | bold sans with ONE key word as big italic serif in one accent (lime) |
| 6 | viral | UPPERCASE Montserrat Black, thick outline, active word yellow, 1-3 words, pops |
| 7 | documentary | small white bold UPPERCASE sans, one line, no colour, no pop |
| 8 | karaoke | words light up as spoken, 3-5 words |
| 9 | hindi | Devanagari-safe (Noto Sans Devanagari), outline, extra line height |
| 10 | minimal | sentence-case medium sans, up to 2 lines, for calm long-form |
| 11 | kinetic | motion reels: small lowercase whisper words build at centre, key words alone as huge Anton apex words (~18% cap height), hard pops |
| 12 | feed | typewriter feed: active line bright at centre, neighbouring lines dimmed |

Full captions (styles 1-10) for talking-head Shorts; **selective captions for motion reels** (`--style 11 --keywords k.json --selective`, 25-40% of words, the script prints the share). The SRT stays complete either way.

`--highlight key|active|both|none` sets what gets coloured (the user's request wins over the style default). If the script prints `WARN fonts missing`, fetch them first: a missing font is silently substituted and the captions look subtly wrong.

Rules for every style (reasons in `references/captions.md`): body captions about 4 to 5% of frame height; key word chosen by **meaning**, never at random, at most one per caption group; captions never cover the face; 9:16 captions stay inside the platform's safe zone (pass `--platform reels|tiktok|shorts|cross`; the script sizes lines to fit and WARNs on anything outside); `--hook-until <s>` keeps captions off the screen while a hook title is up; each caption on screen at least 0.5 s; break groups on breaths and sentence ends. Also export the `.srt` for YouTube upload (accessibility and search). For designed, behind-the-subject cinematic captions use HyperFrames `/embedded-captions` (see `references/captions.md`).

The italic-serif styles (2, 4, 5) are a deliberate editorial trend. Italics read as "tilted" in motion, so keep them to single key words held at least 0.6 s.

## 7. Sound, finish and QA

Pipeline order (each step works on the previous step's output; never skip back):
1. rough cut (`render_cut.py`) 2. colour (`grade.py`) 3. graphics (`overlay.py`, or the composition) 4. captions (`captions.py --burn`) 5. sound and encode (`finish.py`) 6. QA (`qa.py`, `safezone.py`, `qa/qa-look.md`).

```bash
python3 scripts/finish.py renders/v3_captions.mp4 renders/v4_final.mp4 --platform reels \
        --music work/music/bed.mp3 --duck [--voice-chain full] [--sfx work/sfx.json] [--denoise]
python3 scripts/qa.py renders/v4_final.mp4 --edl work/edl.json --captions work/captions_viral.ass --platform reels
```

- **Colour first, if the footage needs it** (`references/color-grading.md`): match B-roll/AI shots to the A-roll (`grade.py --match`), preview a look (`grade.py in.mp4 --look warm --still 4`), apply it or a `.cube` LUT, grain 1-5% for the motion-reel register. Grade before captions.
- **Sound source:** the user chose Epidemic Sound or free sources at intake; note every file's source and licence in `EDIT_STATE.md` (`references/sound-design.md`).
- Sound effects only where something visibly changes. Risers use `"end_at"` in `sfx.json` so they peak on the hit frame; repeated SFX are auto-varied a few percent; text pops sit 8-14 dB under impacts. Explainers: at most about one SFX per second, none on top of key words.
- The bed is placed 20 LU under the **measured voice** (`--music-sep`), the duck follows the voice level, and SFX `db` values are relative to the voice peak, so a quiet narrator never ends up under the music. `--voice-chain full` adds a compressor and de-esser for uneven or harsh recordings.
- Music bed 16-25 dB under the voice, ducked with 600 ms - 1 s recovery (`--duck`, default 700 ms), no vocals under speech, a change of track or energy every 60-90 s. Stop it dead before a reveal with `--music-stop <t>` (rings out as a short reverb tail; `--music-tail cut` for a hard stop).
- **Closed Eye Test** before calling the sound done: if the cut is not engaging with eyes closed, fix voice, rhythm and gaps before any visual polish.
- Deliver -14 LUFS integrated, -1 dBTP max (YouTube, Shorts, Reels, TikTok). `finish.py` does two-pass loudness normalisation and the platform encode (H.264 high, yuv420p, BT.709 tags, AAC 48 kHz, faststart).
- `qa.py` must show no FAIL (it exits 1), and every WARN needs a written disposition. Then **look** at `qa/cuts.png`, `qa/captions.png`, `qa/overview.png` and, for 9:16, `qa/safezone_<platform>.png`, and write `qa/qa-look.md`.
- **Safe zone, always, for 9:16** (the user's standing rule): every word, logo and graphic sits inside the platform's box and off the button rail. Instagram Reels: 220 px top, 420 px bottom, 1010 px wide, like/comment rail in the bottom-right corner. HyperFrames graphics: `python3 scripts/safezone.py html work/gfx/<dir> --platform reels` (exact, every visible text box, 10 samples per second). Transparent overlays: `safezone.py alpha <file.mov>`. Reference: `assets/safe-zones/`.
- Platform specs, safe zones, thumbnails and chapters: `references/platforms-and-styles.md`.

## 8. Review rounds and learning

Show the user each stage before the next: rough cut, visuals plan, graphics, captions, final. If the user is away: cutlist, storyboard and final delivery are hard holds (wait); graphics and caption iterations may continue with the assumption written in `EDIT_STATE.md`. Keep every version (`v1`, `v2`, ...) so they can compare. Never overwrite source footage.

When they give notes ("at 0:22 do X", "too busy", "that flash at 0:14 is a mistake"), fix exactly those, re-render, re-run QA. After each round ask: **"Should I add what we learned to the skill?"** On yes, append the rule, with its reason and the example, to `assets/learned-rules.md` (or the user's own copy of this skill). Read that file at the start of every project: it is how this editor becomes theirs.

## 9. Taste rules you apply every time

Full, sourced versions: `references/design-science.md`. Short versions you should not need to look up:

- **Hook:** frame 1 is already moving and already on topic. No logo sting, no "hey guys". On Shorts the first frame doubles as the thumbnail: put the hook text on it.
- **Cuts:** cut on silence and at the end of a thought, never mid-word. Vary shot lengths; a metronome rhythm reads as machine-made. J/L cuts (audio leads or trails by 0.25 to 1 s) make interview and documentary edits feel smooth.
- **Type:** one font per tier, three tiers at most (whisper/body, apex/display, label/mono), each with a job. Track ALL CAPS +5 to +12%; tighten big display type -1 to -3%. No weight under 400 below 60 px at 1080p (thin strokes smear after YouTube compression). Use tabular numbers on counters.
- **Colour:** exactly one accent hue, covering 10% of the frame or less. Text needs a luminance difference (stroke 2 to 4 px, soft shadow, or scrim), not just a different hue. Keep skin on the skin-tone line; run LUTs at 40 to 80%.
- **Motion:** entrances decelerate (`cubic-bezier(0.16,1,0.3,1)`), exits accelerate and run about 20% faster, on-screen moves ease in-out. One hero moves at a time. Stagger 40 to 80 ms per item, total under 600 ms. Overshoot 0 to 3% for professional work, never elastic or bounce on text. No idle floating or breathing; if a scene runs out of things to do, add story, not wobble. Never more than 3 flashes per second.
- **Default ban list** (allow only if the user asks): particles, glows, lens flares, shockwave rings, camera shake, bouncy easing, purple-blue "AI" gradients, glassmorphism everywhere, emoji as icons, gradient text, typewriter on long sentences, crossfades between scenes, spinning logos, generic stock B-roll, text parked in corners, flat screen recordings in reels (rebuild the UI as a tilted mockup), dead holds longer than 1 s (a still read-hold after a climax is not a dead hold: give the landed number or final line `words x 0.3 s + 0.5 s`).

## 10. How to report back

After each stage: what you made (paths), what you checked and how (which frames, which QA lines), what you could not check, the decision you need from the user (one question), and what happens next. Keep it short. Never claim a frame looks right without having opened it.

## Reference map

| File | Read when |
|---|---|
| `references/toolkit-setup.md` | installing tools, Claude Desktop setup, troubleshooting renders |
| `references/editing-grammar.md` | cutting, pacing gears and arc, first seconds, thumbnail handoff, B-roll timing, sound basics |
| `references/captions.md` | caption styles, sizing, safe zones, Hindi, cinematic captions |
| `references/motion-reels.md` | **main focus**: the measured motion-reels grammar (4 pages), kinetic-type toolkit, SaaS and documentary grammar, new Looks |
| `references/motion-graphics.md` | any graphic or explainer: HyperFrames workflow, motion doctrine, prompt layer, techniques, templates |
| `references/visual-sourcing.md` | where every picture comes from: cascade, licences, Higgsfield, prompt pack, not-found protocol |
| `references/sound-design.md` | music/SFX sources, duck numbers, SFX craft, music stops, Closed Eye Test |
| `references/color-grading.md` | grade.py, verified ffmpeg colour facts and traps, LUTs, what ffmpeg cannot do |
| `references/ugc-ads.md` | paid UGC and AI-avatar ads: hook stack, modular variants, verified disclosure laws |
| `references/looks-library.md` | choosing an art direction (20 Looks with hex codes and fonts) |
| `references/style-reverse-engineering.md` | copying a creator, style card, presets |
| `references/design-science.md` | the sourced numbers: typography, colour, motion, attention, sound, anti-slop |
| `references/platforms-and-styles.md` | October 2026 platform update, export specs, safe zones, creator style data, retention evidence |
| `references/motion-prompt-research.md` | deep dive: what 513 Opus 5.5 video prompts reveal, best full prompts |
| `references/tooling-research.md` | verified ffmpeg recipes, transcription engines (incl. Hindi), auto-editor, other public video skills, asset licences |
| `references/qa-checklist.md` | the pre-delivery checklist |
| `references/mistakes-and-fixes.md` | every mistake class found in an audit of this skill, by stage, with the automatic guard or the exact manual check |
| `assets/style-card-template.md`, `assets/edit-state-template.md`, `assets/learned-rules.md` | style card to fill; project state file; rules learned from the user's notes |
| `assets/storyboard-template.json`, `assets/style-lab.md` | the 7-field storyboard to fill; the persistent Keep/Maybe/Drop motion and sound vocabulary |
| `assets/hyperframes/` | tested starters: kinetic-reel (9:16 genre reel, `data-platform` safe-zone stage, auto-fit text), lower-third, stat-counter |
| `assets/safe-zones/` | the user's Reels safe-zone reference image and transparent guide PNGs per platform |

## Scripts (all standard-library Python + ffmpeg; run with `--help` for options)

| Script | Does |
|---|---|
| `doctor.py` | checks every tool, prints install commands per OS |
| `probe.py` | footage specs, loudness, dead air, keyframe/HDR/VFR warnings, contact sheet |
| `analyze_reference.py` | measures a creator video (cuts, shot lengths, pacing curve, palette, loudness, face share, sheets) |
| `top_refs.py` | ranks a YouTube channel / Instagram or TikTok page by views (or likes), downloads and measures the top N |
| `compare_refs.py` | consensus across measured references: CONSISTENT rules vs per-video choices, shared palette |
| `storyboard.py` | validates the 7-field storyboard (contiguous, verbatim VO) and builds the approval page (HTML + MD) |
| `grade.py` | colour: match B-roll to A-roll, 5 looks, LUT apply/export, glow, grain, before/after stills |
| `transcribe.py` | word timestamps via mlx-whisper / faster-whisper / openai-whisper / HyperFrames, `--verbatim` keeps fillers |
| `plan_cuts.py` | fillers, retakes (keeps last take), dead air, silence-snapped and frame-snapped cuts, `cutlist.md`, `words_cut.json` |
| `render_cut.py` | renders the EDL, de-click fades, alternating punch-ins, single-pass audio (no drift) |
| `verify_cut.py` | second listening pass on the render: clipped/ghost words, drift |
| `reframe.py` | 16:9 to 9:16 / 4:5 / 1:1, face-centred or blurred fit |
| `overlay.py` | composites HyperFrames graphics (alpha MOV/WebM) or cutaways at their words |
| `qa_graphic.py` | QA for a rendered graphic: alpha present, clear first/last frame, pops, legibility sheets |
| `fetch_fonts.py` | downloads Google Fonts TTFs for captions and graphics |
| `captions.py` | 12 caption styles (incl. kinetic two-tier and feed) as word-timed ASS + SRT, `--selective`, burn-in |
| `finish.py` | voice clean-up, music bed with ducking, music stop + reverb tail, varied SFX, risers that end on the hit, two-pass -14 LUFS, platform encode |
| `qa.py` | spec/loudness/black/freeze/flash/mono checks, cut, caption and safe-zone review sheets; exits 1 on FAIL |
| `safezone.py` | 9:16 safe zones: exact text-box audit of HyperFrames compositions, alpha audit of overlays, overlay sheets, design guides |
