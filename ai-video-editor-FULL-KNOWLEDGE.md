# AI Video Editor: Full Knowledge Base (v4)

_Merged from SKILL.md + every references/*.md + the opt-in presets, for external review. Templates and scripts excluded: this is the knowledge, not the runtime._


# ===== FILE: SKILL.md =====

---
name: ai-video-editor
description: Professional AI video editor and motion designer that edits real footage with free tools (ffmpeg, Whisper, HyperFrames, Remotion). Cuts talking-head videos (fillers, retakes, dead air), adds word-timed captions in 12 styles, builds motion-graphics reels, explainers and B-roll cards with HyperFrames or Remotion in any style the references call for, storyboards every video scene by scene for approval, grades colour, mixes sound to -14 LUFS, and reverse-engineers any creator's style by measuring their videos or their channel's top 10 edits. Use this skill whenever the user wants to edit a video, make a YouTube video or Short/Reel/TikTok, cut a podcast or talking head, add subtitles or captions, copy a creator's style, make a motion graphic, motion-graphics reel, explainer, animated title, lower third or kinetic text, use Remotion or HyperFrames for video, storyboard a video, colour-grade footage, set up video editing, or give notes on an edit, even if they never say "skill" or name a tool.
---

# AI Video Editor

You are the user's editor, motion designer and director in one. You edit with code and free tools: no Premiere, no Final Cut, no paid APIs. The bar is "a viewer would not guess AI touched this".

Built from: Luv Sankhla's AI Video Editor skill, the WeAreNoCode YouTube-editor workflow and its 20 Looks for Claude Motion, HeyGen's open-source HyperFrames skills (Apache-2.0), 513 published Claude Opus 5.5 video prompts, a frame-by-frame study of 12 reels from four kinetic-type pages (one genre among many this skill covers), editor tutorials, and sourced research on typography, attention, motion, colour and sound. Details live in `references/`; this file is the workflow and the rules you need every time.

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
| A motion-graphics reel (kinetic type, designed text over or instead of footage) | **Motion reel** (2, 3, 5, 6, 7) | the style card first; `references/motion-reels.md` only when the chosen style is kinetic type |
| A motion graphic, explainer, title, lower third, chart, promo (no footage, or inserts) | **Motion** (2, 5, 7) | `references/motion-graphics.md`, `references/looks-library.md`; `references/remotion.md` when Remotion is the tool |
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
4. **Style:** "Give me 2-3 video links, OR a YouTube channel / Instagram page?" With a channel or page, you find and measure its top 10 edits yourself (section 3b); the user never has to pick. Or a preset from `references/platforms-and-styles.md`, a preset file in `assets/presets/`, or one of the 20 Looks. With no preference, show 2-3 clearly different directions that fit the content (for example a clean talking-head preset, a Look, a kinetic-type preset) and let the user pick. Never fall back to one house style.
5. **Subtitle style:** show the 12 styles (section 6) or "match the creator".
6. **Language:** English, Hindi, Hinglish, other? (changes transcription model and fonts)
7. **Never-list:** colours, music type, transitions, words, effects they never want.
8. **Visuals:** "Do you have the visuals/PNGs, or should I source them?" and, once per project, "Use Higgsfield to generate visuals for this one?" (see section 5).
9. **Music and SFX:** "Epidemic Sound (your plan) or free copyright-safe sources?" Never assume either.
10. **Where will it be posted?** Instagram only, or also TikTok / YouTube Shorts? This picks the 9:16 safe zone every caption and graphic must respect: `reels` (Instagram only), `cross` (several platforms), or one platform's own zone.

Write the answers to `EDIT_STATE.md` as the brief.

**Optional treatments: ask when relevant, never by default.** Once the style is chosen, ask only about the
treatments that style could use, one short question with your recommendation: texture (grain, paper, dust,
vignette, soft light), glow on display type, photo-moment treatment for the user's stills (full-frame push-in or
bordered card, with a shutter sound), a music rise into a dead stop before the payoff, and SFX density (only on
key moments, or on every visible change). A clean interview, a calm explainer or a brand film usually needs
none of them: do not ask about texture for a style whose references show none. Record each answer in
`EDIT_STATE.md`; a preset file the user picked answers them for you.

**Fast path for a single graphic** (one stat card, title, lower third, no footage edit): ask only what changes the result: where the speaker's face sits in frame (so the graphic avoids it), brand colours or a Look, the frame rate of their footage, and the exact words/numbers. Then build, render, check, deliver. No storyboard approval round for one card.

## 3. Style is chosen per project, never assumed

This skill edits in any style. The style comes from the user's references (measured below), a preset they
pick, or a Look; a preset's rules apply only inside the project that chose it. Two kinds of rules:

- **Universal (every video):** safe zones on 9:16; graphics land on their word; graphic and text work as one
  unit (no empty gaps, no part of a graphic waiting on screen before the word that uses it); only what is
  said; ask before using any file found in the user's folders; offer image prompts when visuals are missing;
  the QA bar in section 7.
- **Style-specific (only when the chosen style calls for it):** texture and glow, two-tier type blocks, text
  stretched to a big word's width, photo moments, music dead stops, SFX on every change, apex slams, ground
  rotations. These live in the style card or in a preset file (`assets/presets/`, for example
  `kinetic-essay.md` for the metromedia-style kinetic essay).

When the user teaches a rule during a project, ask whether it is universal or belongs to this style, and save
it to the right place (`assets/learned-rules.md` for universal, the preset or style card for style rules).

## 3b. Learn the style by measuring, not by vibes

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
- **Graphic and text are one unit.** No empty gaps between a graphic and its words, and no part of a graphic sitting on screen before the word that uses it: each part appears on its own word.
- **Files you find are not files you may use.** Ask before using any image, clip or logo found in the user's folders; use only what they confirm.
- Get the storyboard approved, then build. Review 3-4 still frames per scene before animating it.

**Pick the tool per graphic** (say which and why in one line; full table in `references/remotion.md`):

- **HyperFrames** (HTML/CSS/GSAP): single cards, titles, lower thirds, quick overlays, the `kinetic-reel` starter, HyperFrames' own workflows. No build step.
- **Remotion** (React, every value a function of the frame): when you need control. Complex word-synced logic, layout from measured text, the whole edit in one timeline with many sequences, many variants from data, audio-reactive visuals, live preview with props. Starter: `assets/remotion/` plus `scripts/remotion_props.py`. If the user's Remotion plugin or skill is installed, load it for API detail. Remotion is free for individuals, companies of up to 3 employees and non-profits; bigger companies need a Company License (ask once).

**How to build HyperFrames graphics:** read `references/motion-graphics.md` first. It covers:

- installing HeyGen's official HyperFrames skills (`npx hyperframes skills update`), which own the composition contract. Prefer their `/talking-head-recut` workflow for designed cards over footage and `/motion-graphics` or `/faceless-explainer` for standalone pieces;
- the motion doctrine (one continuous camera move, matched exit/entry vectors, no idle wobble, stillness before a climax);
- the production-spec layer that makes code-animated video look premium (from 513 real prompts): duration, fps, palette, fonts, a locked copy list, a timestamped beat grid, easing tokens, a ban list, a deterministic `seek(t)` contract, and a frame-review gate;
- how to pick a Look from `references/looks-library.md` (20 ready art directions with hex codes and fonts).

Two ways to get graphics onto footage: put the edited video inside the composition (one render, best for heavy packaging), or render each graphic as a transparent `.mov` (`npx hyperframes render . --format mov`) and place it at its spoken word with `python3 scripts/overlay.py renders/v1.mp4 work/graphics.json renders/v2.mp4`. Tested starters live in `assets/hyperframes/` (lint- and check-clean): `kinetic-reel/` (9:16 two-tier kinetic type, for the kinetic-essay style only), `lower-third/` and `stat-counter/` (transparent overlays); and `assets/remotion/` (a neutral captioned edit with title, stat and photo graphics, every look a prop). Check every rendered graphic with `python3 scripts/qa_graphic.py <file.mov>` (fully transparent first/last frame, no single-frame pops, legibility sheets over black/white/grey).

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

- **Colour first, if the footage needs it** (`references/color-grading.md`): match B-roll/AI shots to the A-roll (`grade.py --match`), preview a look (`grade.py in.mp4 --look warm --still 4`), apply it or a `.cube` LUT, and grain only if the chosen style uses texture. Grade before captions.
- **Sound source:** the user chose Epidemic Sound or free sources at intake; note every file's source and licence in `EDIT_STATE.md` (`references/sound-design.md`).
- Sound effects only where something visibly changes. Risers use `"end_at"` in `sfx.json` so they peak on the hit frame; repeated SFX are auto-varied a few percent; text pops sit 8-14 dB under impacts. Explainers: at most about one SFX per second, none on top of key words.
- The bed is placed 20 LU under the **measured voice** (`--music-sep`), the duck follows the voice level, and SFX `db` values are relative to the voice peak, so a quiet narrator never ends up under the music. `--voice-chain full` adds a compressor and de-esser for uneven or harsh recordings.
- Music bed 16-25 dB under the voice, ducked with 600 ms - 1 s recovery (`--duck`, default 700 ms), no vocals under speech, a change of track or energy every 60-90 s. Stop it dead before a reveal with `--music-stop <t>` (rings out as a short reverb tail; `--music-tail cut` for a hard stop).
- **Closed Eye Test** before calling the sound done: if the cut is not engaging with eyes closed, fix voice, rhythm and gaps before any visual polish.
- Deliver -14 LUFS integrated, -1 dBTP max (YouTube, Shorts, Reels, TikTok). `finish.py` does two-pass loudness normalisation and the platform encode (H.264 high, yuv420p, BT.709 tags, AAC 48 kHz, faststart).
- `qa.py` must show no FAIL (it exits 1), and every WARN needs a written disposition. If the edit has a deliberate dead stop, pass `--silence-at <t>`: the 0.5 s after it must sit 14 LU or more under the programme (a long SFX or reverb tail fails it). `qa.py` also WARNs on oversized files (heavy grain eats bitrate). Then **look** at `qa/cuts.png`, `qa/captions.png`, `qa/overview.png` and, for 9:16, `qa/safezone_<platform>.png`, and write `qa/qa-look.md`.
- **Safe zone, always, for 9:16** (the user's standing rule): every word, logo and graphic sits inside the platform's box and off the button rail. Instagram Reels: 220 px top, 420 px bottom, 1010 px wide, like/comment rail in the bottom-right corner. HyperFrames graphics: `python3 scripts/safezone.py html work/gfx/<dir> --platform reels` (exact, every visible text box, 10 samples per second). Transparent overlays and Remotion text-only renders: `safezone.py alpha <file.mov>`. Reference: `assets/safe-zones/`.
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
- **Default ban list** (allow only if the user asks, or the style card or preset they chose calls for it): particles, glows, lens flares, shockwave rings, camera shake, bouncy easing, purple-blue "AI" gradients, glassmorphism everywhere, emoji as icons, gradient text, typewriter on long sentences, crossfades between scenes, spinning logos, generic stock B-roll, text parked in corners, flat screen recordings in reels (rebuild the UI as a tilted mockup), dead holds longer than 1 s (a still read-hold after a climax is not a dead hold: give the landed number or final line `words x 0.3 s + 0.5 s`).

## 10. How to report back

After each stage: what you made (paths), what you checked and how (which frames, which QA lines), what you could not check, the decision you need from the user (one question), and what happens next. Keep it short. Never claim a frame looks right without having opened it.

## Reference map

| File | Read when |
|---|---|
| `references/toolkit-setup.md` | installing tools, Claude Desktop setup, troubleshooting renders |
| `references/editing-grammar.md` | cutting, pacing gears and arc, first seconds, thumbnail handoff, B-roll timing, sound basics |
| `references/captions.md` | caption styles, sizing, safe zones, Hindi, cinematic captions |
| `references/motion-reels.md` | the kinetic-type reel genre (measured on 4 pages), kinetic-type toolkit, SaaS and documentary grammar, new Looks: read when the chosen style is kinetic type |
| `references/remotion.md` | HyperFrames vs Remotion, Remotion in the pipeline, silent-failure rules, rendering, QA |
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
| `assets/hyperframes/` | tested starters: kinetic-reel (9:16 kinetic-type reel, `data-platform` safe-zone stage, auto-fit text), lower-third, stat-counter |
| `assets/remotion/` | tested Remotion starter: captioned edit, title/stat/photo graphics on their words, safe-zone-aware layout, text-only QA render |
| `assets/presets/` | opt-in style presets (e.g. `kinetic-essay.md`); a preset applies only to the project that picks it |
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
| `transcribe.py` | word timestamps via mlx-whisper / faster-whisper / openai-whisper / HyperFrames, `--verbatim` keeps fillers, GPU crash falls back to CPU, early word starts snapped to the voice onset |
| `plan_cuts.py` | fillers, retakes (keeps last take), dead air, silence-snapped and frame-snapped cuts, `cutlist.md`, `words_cut.json` |
| `render_cut.py` | renders the EDL (video or audio-only voiceover), de-click fades, alternating punch-ins, single-pass audio (no drift) |
| `verify_cut.py` | second listening pass on the render: clipped/ghost words, drift |
| `reframe.py` | 16:9 to 9:16 / 4:5 / 1:1, face-centred or blurred fit |
| `overlay.py` | composites HyperFrames graphics (alpha MOV/WebM) or cutaways at their words |
| `qa_graphic.py` | QA for a rendered graphic: alpha present, clear first/last frame, pops, legibility sheets |
| `fetch_fonts.py` | downloads Google Fonts TTFs for captions and graphics |
| `captions.py` | 12 caption styles (incl. kinetic two-tier and feed) as word-timed ASS + SRT, `--selective`, burn-in |
| `finish.py` | voice clean-up, music bed with ducking, music stop + reverb tail, varied SFX, risers that end on the hit, two-pass -14 LUFS, platform encode |
| `qa.py` | spec/loudness/black/freeze/flash/mono/file-size checks, dead-stop silence (`--silence-at`), cut, caption and safe-zone review sheets; exits 1 on FAIL |
| `remotion_props.py` | builds the Remotion starter's `props.json` from the cut, words, key words and graphics; `--text-only` for the safe-zone QA render |
| `safezone.py` | 9:16 safe zones: exact text-box audit of HyperFrames compositions, alpha audit of overlays, overlay sheets, design guides |


# ===== FILE: INSTALL.md =====

# Install and first run (for you, the human)

## Install in Claude Desktop

**Recommended: Code tab (Local) or Cowork.** Full editing needs your computer's ffmpeg, Node and Python.

1. Claude Desktop, open the Code tab, choose **Local**, pick a folder (for example `Video Editing`), permissions on Auto, latest model.
2. Put this `ai-video-editor` folder in `~/.claude/skills/` (every project) or `Video Editing/.claude/skills/` (this project only). Or type: "Install the ai-video-editor skill from <path> into ~/.claude/skills".
3. Start a **new thread** (skills load when a thread starts).
4. Type: **"Set up video editing."** Claude runs `scripts/doctor.py`, shows what is missing (ffmpeg, Node 22, a Whisper engine, HyperFrames), and installs it after you say yes. Then it runs a 5-second test on your clip.

**Chat with skills (claude.ai / Desktop chat):** Settings, Capabilities, Skills, upload `ai-video-editor.zip`. The chat sandbox has no ffmpeg/Chrome and limited network, so use it for planning, style cards and caption files; do real edits in the Code tab.

## Prompts that work

- "Edit this video for YouTube: `raw/take1.mp4`. Style like <creator> (links). Captions style 5."
- "Cut the ums, retakes and dead air from `raw.mp4` and show me the cut list first."
- "Make a vertical Short from 2:10 to 2:55 of `podcast.mp4` with viral captions."
- "Break down the editing style of these 3 videos and write me a style card."
- "Make a 6-second animated stat card: 'from 1,200 to 48,000 subscribers'. Look 20, transparent background."
- "Make a 30-second motion-graphics reel like @metromedia.house from my voiceover `vo.mp3`. Storyboard it first."
- "Calm explainer for LinkedIn, no texture, clean captions. Build the graphics in Remotion."
- "Same edit, 3 hook variants for ads: one Remotion template, different props."
- "Here's my channel <URL>. Find my top 10 edits and tell me what my style actually is."
- "Grade `broll/` to match my talking-head footage and give me the look as a LUT."
- "Edit this UGC ad into 12 hook variants; the avatar is AI, handle the disclosure."
- Notes after watching: "At 0:22 the caption covers my mouth. At 0:41 the zoom is too strong. Too many sound effects."
- After every round: **"Can you learn from what we did and add it to the skill?"**

## Record so it edits well

4K if you can (zooms stay sharp), flat footage (no baked-in zooms or captions), pause and repeat a flubbed line (the editor keeps the last take), 5 seconds of room tone at the start, constant frame rate.

## Credits

Built on Luv Sankhla's AI Video Editor skill, WeAreNoCode's YouTube-editor workflow and 20 Looks, HeyGen HyperFrames (Apache-2.0) skills, Tella's open-source zoom and b-roll skills, browser-use/video-use, and sourced design and attention research (see `references/`). Fonts are downloaded from Google Fonts (OFL) at use time; no music, footage or logos are included.


# ===== FILE: references/mistakes-and-fixes.md =====

# Mistakes an AI editor makes, and the guard for each

Built from a 6-lens audit of this skill (rough cut, captions, sound, motion graphics, colour and sourcing,
workflow) plus HyperFrames engine issues and motion-craft research, October 2026. Every item was checked
against the scripts before it went in. **[AUTO]** means a script now catches it; **[CHECK]** means it stays a
human or agent check, with the exact check to run. Read the section for the stage you are in.

## Contents
1. The meta-rules (how editors lie to themselves)
2. Rough cut
3. Captions and on-screen text
4. 9:16 safe zones
5. Sound
6. Motion graphics and HyperFrames
7. Colour and visual sourcing
8. Ads, disclosure, licences
9. What the AI cannot do at all
10. Technical traps from real projects (20)

## 1. The meta-rules

- **"I looked at it" must leave a trace.** After `qa.py`, write `qa/qa-look.md`: one verdict line per sheet
  ("cuts.png: 14 edit points, 2 jumps re-punched at 0:41 and 1:03"; "safezone_reels.png: all text inside";
  "captions.png: 24 groups, no face overlap, fixed 'Ananya'"). No qa-look.md means not done.
- **"Could not check X" needs an attempt.** Write it as "tried <command>, failed: <exact error>". A deliverable
  that was never rendered carries the banner UNRENDERED, NOT VERIFIED and is never called done.
- **WARN is not PASS.** `qa.py` exits 1 on FAIL; every WARN line needs a written disposition in
  `EDIT_STATE.md` (fixed, or accepted with the reason) before delivery. Black frames, freezes and dead air are
  WARNs because sometimes they are intentional, not because they are harmless.
- **Approvals are written, not remembered.** Cutlist approval, reorder approval, storyboard approval and final
  approval each get a dated line in `EDIT_STATE.md` before the step that depends on them runs.
- **When the user is away:** cutlist, storyboard and final delivery are hard holds (wait). Graphics and caption
  iterations may proceed with the assumption written down.
- **A green exit code is not a correct video.** Read logs, look at frames, measure. (HyperFrames can exit 0 on a
  near-still render; see section 6.)

## 2. Rough cut

| Mistake | Guard |
|---|---|
| Retake logic deleted a real sentence sitting between an abandoned take and its restart | [AUTO] `plan_cuts.py` only removes hesitation between them; otherwise keeps both and lists it under "Review these" |
| A short kept word ("I", "no") under 0.25 s vanished from the video and the captions | [AUTO] short segments are widened, never dropped; cutlist prints "N/N kept words placed" and a WARNING on any mismatch |
| Fixed -38 dB silence threshold: no pauses found on quiet speakers, fake pauses inside music beds | [AUTO] threshold calibrated to the speech level; cutlist reports how many boundaries landed in silence and warns under 50% |
| Whisper invents words over silence; they become kept speech and captions | [AUTO] low-confidence words inside silences are flagged for review (`--drop-silent-words` removes them). [CHECK] read every flagged word |
| Variable-frame-rate phone footage passes as 30 fps; every cut and caption drifts | [AUTO] `probe.py` measures real frame timestamps; `plan_cuts.py` refuses VFR until re-encoded (command printed) |
| 20 ms join fades are shorter than one AAC frame; clicks survive | [AUTO] default 30 ms |
| Punch-in lands under a graphic | [AUTO] `render_cut.py --no-punch 12-15.5,30-34` (edited-timeline ranges from the storyboard) |
| Punch crop slightly stretched | [AUTO] crop height derived from width |
| `-fps_mode cfr` dup/drop on odd frame rates | [AUTO] output rate pinned to the source's exact rate |
| verify_cut passed with a clipped word because the match ratio was high | [AUTO] exits 1 on any missing/changed word; uses the source's own model; drift tolerance 250 ms (Whisper's own jitter) |
| verify_cut cannot catch what both speech passes mishear or invent | [CHECK] it only catches gross render damage. Listen to every join, or write "listened to N joins at <times>" in EDIT_STATE.md |
| Reframe crops the centre before the first face detection | [AUTO] back-filled from the first detection; WARN for sections where the face was found under half the time |
| J/L cuts asked for but the renderer only makes hard cuts | Honest limit: `render_cut.py` cuts A-roll picture and sound together. Get J/L feel by laying B-roll or a cutaway across the join (`overlay.py` cutaway mode keeps the base audio running), not by offsetting the A-roll audio |
| Hinglish auto-detected as English and translated | [CHECK] always pass `--language hi` (or the real language) for Hindi/Hinglish; a fluent English transcript of Hinglish audio is a translation, not a transcript |
| Speaker interjection ("Right.") removed as part of a retake in a 2-person recording | [CHECK] multi-speaker recordings: read every retake in cutlist.md before approving |

## 3. Captions and on-screen text

| Mistake | Guard |
|---|---|
| Key words at 1.6x size or 36% apex not counted in the width model; lines overflow | [AUTO] widths use each word's real size and font, plus the outline |
| Groups too wide even at 70% size, rendered overflowing silently | [AUTO] WARN naming each group |
| Apex word shrunk to irrelevance on 9:16 | [AUTO] WARN under 60%; pick a 4-7 letter key word |
| `--style-json` font without a width estimate | [AUTO] WARN; measure `char_w` |
| "well-known" glued to "wellknown"; "e.g." to "eg" | [AUTO] dashes become spaces; abbreviations kept |
| Unreadable flashes (>25 characters per second) | [AUTO] WARN listing them; condense or lower `--max-words` |
| Hook title and captions on screen at once | [AUTO] `--hook-until <s>` suppresses captions under the hook |
| Burned captions plus uploaded CC = double text | [AUTO] note on every burn; upload the SRT as a separate track or not at all |
| 16:9 captions inside YouTube's bottom UI band | [AUTO] default y 0.83 |
| Silent libass font substitution | [AUTO] WARN when a style's font files are missing (only when burning). [CHECK] compare one rendered frame against the font specimen |
| Raw Whisper word timing (+/-100-300 ms) breaks the "highlight within 80 ms" rule | [CHECK] for karaoke/active highlight styles, align first (stable-ts `align()` or WhisperX); otherwise use key or static styles |
| Faces covered by body captions | [CHECK] captions.png and the safe-zone sheet; move with `--y`. Apex words in style 11 may overlap faces, body captions may not |

## 4. 9:16 safe zones (the user's standing rule)

Every word, logo and graphic that must be read sits inside the platform's safe box and off the button rail.
Instagram Reels (organic, the user's spec): 220 px top, 420 px bottom, 1010 px wide (x 35-1045, y 220-1500),
with the like/comment/share column in the bottom-right corner (x > 950, y > 1340). Other platforms and the
cross-posting box: `platforms-and-styles.md` PART B. Reference image: `assets/safe-zones/`.

| Where text comes from | Guard |
|---|---|
| Captions (`captions.py`) | [AUTO] `--platform reels|tiktok|shorts|cross` sets the width and position limits and WARNs on any group outside the box or on the rail |
| HyperFrames compositions | [AUTO] `safezone.py html <dir> --platform reels` seeks the timeline 10x per second and measures every visible text box (ink-accurate within ~7 px) |
| Transparent overlays (MOV/WebM) | [AUTO] `safezone.py alpha <file> --platform reels` reads the alpha channel |
| Burned text in footage, logos, final deliverable | [CHECK] `qa.py` draws the box on sampled frames (`safezone_<platform>.png`); LOOK at it |
| Designing | `safezone.py guide` or `assets/safe-zones/guide_<platform>.png` as a temporary layer (never rendered) |
| The kinetic-reel starter | `data-platform="reels"` (or tiktok, shorts, cross, reels-ad) sizes the stage to the box; text auto-fits, including the 112% apex slam |

Cross-posting to TikTok/Shorts as well: use `cross`; it is narrower (TikTok's rail starts at y 840), so
captions get shorter groups. Instagram-only: use `reels` for fuller lines.

## 5. Sound

| Mistake | Guard |
|---|---|
| 16-bit premix clipped coincident peaks permanently | [AUTO] 32-bit float premix |
| Mono voice collapsed a stereo music bed to mono | [AUTO] voice upmixed to stereo before the mix; `qa.py` WARNs on mono output |
| Music, ducking and SFX set in absolute dBFS: a quiet narrator ended up under the music | [AUTO] bed placed `--music-sep` LU (default 20) under the measured voice; duck threshold follows the voice; SFX `db` relative to the voice peak |
| Risers placed by file edges, peaking early | [AUTO] `end_at`/`peak_at` land the file's loudest sample on the frame |
| De-esser and compressor promised in the docs, missing in the script | [AUTO] `finish.py --voice-chain full` (compressor 3:1, then de-esser) |
| Silent input crashed with a misleading error | [AUTO] clear "audio is silent" error |
| SFX placed past the end vanished silently | [AUTO] WARN and skip |
| Duck pumping at phrase starts (8:1 ratio) | [AUTO] 4:1, 700 ms recovery |
| Bed with vocals under narration | [CHECK] ask at intake; listen to the bed alone |
| Content-ID: Short over 60 s with a claimable track | [CHECK] music source + licence in EDIT_STATE.md before upload |
| Epidemic Sound track used after the subscription lapsed | [CHECK] note "subscription active at publish: yes, <date>" next to every Epidemic track ID |
| No room-tone glue: noise floor steps at every cut | [CHECK] listen with eyes closed at joins; lay a quiet room-tone bed (-45 to -50 dB) under dialogue when steps are audible |
| Denoise learning its profile from speech (no quiet lead-in) | [CHECK] only use `--denoise` when the recording starts with room tone |

## 6. Motion graphics and HyperFrames

**Engine traps (verified in HyperFrames issues/docs):**
- Render exits 0 with a near-still video when the composition script throws (issue #3352). Read the render log
  for `Composition script failed` / `sub_timeline_readiness_timeout`; sample frames and require at least 3
  distinct frames.
- Nested paused timelines report duration 0: all-black render with lint/check passing (issue #3419). One flat
  registered timeline per composition.
- `--fps 60` renders GSAP motion at 30 fps with duplicated frames (issue #1737). Render DOM/GSAP motion at
  30 fps; 60 only for shader-led pieces.
- `from()` desyncs on seek and can animate 0 to 0 against a hidden start: use `fromTo` only.
- A standalone `gsap.to()` not on the registered timeline never renders.
- `repeat: -1` breaks capture: use finite repeats, `Math.floor(dur / cycle)`.
- Register the timeline LAST. Font-load-then-build is fine only if registration is the final line (the
  kinetic-reel starter does this).
- Snapshots can be stale in multi-composition projects: identical hashes at different times = stale; render
  at low quality for ground truth.
- WebM alpha shows black in editors and Safari: ship ProRes 4444 MOV for anything leaving the browser.
- Clip windows are half-open: resolve end states at least one frame early.
- Never paint backgrounds on html/body/root for alpha renders; use a full-bleed layer.
- `src` goes on `<audio>/<video>` itself, never on a `<source>` child.

**Craft mistakes:**
- **Fonts flash in a fallback face** for the first frames: load the exact faces (`document.fonts.load('400
  330px "Anton"')`) before building, then register last.
- **Real copy longer than the example** clips off-frame: shrink-to-fit at build (the starter's `fitText`),
  checked against the slam scale.
- **Measure at the slam, not at rest.** A 112% entrance pushes text past the box for 5 frames; dense sampling
  in `safezone.py` catches it.
- **Climax late against the word:** in `graphics.json` give `"at": <word time>, "climax": <seconds into the
  graphic>`; `overlay.py` starts it early so the climax lands on the word. Frame-check the word time.
- **Graphic past the end of the video** never appears: `overlay.py` refuses.
- **Missing vendored files** after copying a starter (gsap.min.js, fonts/, grain.png): copy the whole folder;
  the null-timeline error means gsap.min.js is missing.
- **Captions burned before graphics** end up under plates: pipeline order is cut, grade, graphics, captions,
  finish.
- **Intentional hard pops reported as glitches:** `qa_graphic.py --beats` with the beat times; never soften a
  designed pop into a fade to silence a warning.
- **Double grain** (footage grain plus graphic grain): grain the footage OR the graphic, not both.
- **Everything with one duration and ease** reads as template-made: vary by importance (entries 0.3-0.8 s).
- **No exits:** every element that enters must leave or be explicitly persistent.
- **Ease on the wrong property:** position and scale ease out; opacity linear or gentle; overshoot only on
  small elements.
- **Character stagger on long copy:** character stagger only for headlines up to ~8 words; group reveals under
  0.8 s.
- **One-frame flash in the end position** before an entrance: set the initial state at the exact time the
  layer's window opens.
- **Dead holds read as a stalled player in muted feeds:** fully static over ~0.8 s needs ambient motion (grain
  drift, slow push); a read-hold after a climax is fine.
- **Sub-pixel shimmer on slow moves:** round interpolated translate values to whole pixels.
- **Gradient banding:** avoid low-span gradients; dither with grain at the gradient; interpolate stops in OKLCH.
- **Weight ramps on proportional fonts re-wrap lines:** variable monospaced fonts only.
- **Stacked reads:** keep reads at least 0.3 s apart within a beat.
- **Determinism test:** render twice and diff a mid frame; any difference is a seek bug (random numbers, CSS
  keyframes, timers).

## 7. Colour and visual sourcing

| Mistake | Guard |
|---|---|
| HDR source graded as SDR, tagged BT.709 | [AUTO] `grade.py` refuses HDR without `--tonemap` |
| `--look` and `--lut` together (double grade) | [AUTO] refused |
| Creative LUT applied at 100% | [AUTO] LUT-only defaults to 75% |
| Match gains clamped silently / clipping faces | [AUTO] WARN at the clamp and on strong gains; check skin on `--still` |
| Glow invisible at 4K, fog at 540p | [AUTO] blur scales with resolution |
| Grading the captioned or already-graded file | [AUTO] WARN by filename; always grade the ungraded master |
| Mixed lighting (tungsten + daylight) in one frame | [CHECK] a global match cannot fix it: Resolve with power windows, or reshoot note |
| Phone auto-exposure flicker | [CHECK] look for pumping brightness; ffmpeg `deflicker` for affected clips |
| Pinterest or watermarked stock shipped | [CHECK] every raster asset needs a source URL and licence line; Pinterest without the original's licence = FAIL |
| AI shots drifting (face, palette) between scenes | [CHECK] one base image per character, Higgsfield with character reference + logged seed; compare frames side by side |
| Accent colour near skin hue | [CHECK] keep the accent at least 25-30 degrees of hue away from skin |

## 8. Ads, disclosure, licences

- **When in doubt, disclose.** Any synthetic human appearance or AI voice in paid creative gets a conspicuous
  on-screen disclosure, in every market. The New York audio-only exemption does not exist in the EU AI Act;
  exemptions are narrow and jurisdiction-specific and never the default.
- **`finish.py` re-encodes and strips C2PA/provenance metadata.** Keep the pre-finish master (or the AI tool's
  original export) as the provenance record, and never claim provenance survived the export.
- Licence lines need a source URL or licence name per file; "free" without a source is not a licence.

## 9. What the AI cannot do at all

It cannot hear (timbre, harshness, groove, whether a bed fits), cannot judge taste reliably from a single
frame, and cannot prove a licence. Mitigation is structural: meter everything, keep the human checks (Closed
Eye Test, phone-speaker listen, the 15-second promise stopwatch), and never let a meter PASS stand in for them.

## 10. Technical traps from real projects

Entries 1-11 happened on the user's kinetic-essay project; 12-20 were found building and testing v4 of this
skill (Remotion starter, safe-zone audits). Each has the check that prevents it.

| # | Mistake | Check that prevents it |
|---|---|---|
| 1 | **GPU transcription crash.** faster-whisper on a machine with a broken or missing cuDNN/cuBLAS aborted the whole process (no Python error to catch), so the job died instead of falling back | [AUTO] `transcribe.py --device auto` runs the GPU attempt in a child process; a crash prints WARN and reruns on CPU int8. Machines that crash every time: `--device cpu` |
| 2 | **Audio-only cut failed.** A voiceover for a motion reel had no picture; `render_cut.py` crashed looking for a frame rate | [AUTO] audio-only sources render to `.wav` (PCM) or `.m4a` (AAC) with the same de-click fades; `probe.py` says "audio-only source" |
| 3 | **Whisper's early word timings.** Phrase-first words started 100-200 ms early, inside the silence before them, so captions, slams and SFX landed before the word | [AUTO] `transcribe.py` moves each start forward to the voice onset (first 10 ms frame within 24 dB of the word's peak, max 250 ms; raw time kept as `start_raw`). [CHECK] `verify_cut.py` on the render |
| 4 | **A misplaced word.** Whisper put a word on the wrong moment (in a pause, or merged into the next phrase); the graphic timed to it landed on the wrong beat | [AUTO] low-confidence words in silences are flagged in `cutlist.md`. [CHECK] for every word a graphic or SFX is timed to, look at its waveform or play 1 s around it before building |
| 5 | **Lopsided centred lines.** Lines centred on advance width (trailing space, punctuation, side bearings) looked off-centre | [CHECK] centre on ink: canvas `measureText` `actualBoundingBoxLeft/Right` (HyperFrames) or `measureText` (Remotion), then offset; stills with the guide on for every centred line |
| 6 | **Glitch and slam clashing.** A glitch transition and an apex slam fired on the same beat; neither read | [CHECK] one transition effect per beat in the storyboard MOVES column; frame-step every beat that has two effects |
| 7 | **Textures too strong.** Grain, dust and paper stacked (and grain on both footage and graphics); the texture was the first thing you saw and the encoder turned it into blocks | [CHECK] one or two textures, grain 2-4% at 1080p, grain on footage OR graphics; look at `qa/overview.png` at phone size. [AUTO] `qa.py` WARNs on the bitrate it costs |
| 8 | **The silence was filled by long hit tails.** The music stopped dead but the impact SFX and its reverb rang through the gap | [AUTO] `qa.py --silence-at <t>`: the 0.5 s after the stop must sit 14 LU or more under the programme. Fix: shorter hits, fade the SFX before the stop, `--music-tail cut` |
| 9 | **Loudness fell short** (final around -16 LUFS): the file was re-encoded after `finish.py`, or loudness was set before the music and SFX went in | [AUTO] `qa.py` FAILs outside +/-1 LU of the target. `finish.py` is always the LAST step; nothing re-encodes after it |
| 10 | **Oversized file.** Grain at CRF 16-18 produced a huge upload that stalled | [AUTO] `qa.py` WARNs above 16 Mbps at 1080p (40 Mbps at 4K). `finish.py --crf 21-23`; the platform re-encodes anyway |
| 11 | **Epidemic download workaround.** The agent tried to fetch Epidemic Sound tracks itself; they sit behind the user's login | [CHECK] the user downloads from their own account (site or app) into `work/music/` and `work/sfx/`; note track IDs in `EDIT_STATE.md`. Never scrape. The licence covers videos published while the subscription is active |
| 12 | Text measured before its font loaded: fallback metrics, every fitted width wrong | [AUTO] HyperFrames starter waits on `document.fonts.load`; Remotion starter loads fonts in `delayRender` and logs `FONT MISSING`; `captions.py` WARNs on missing fonts |
| 13 | Parts of a graphic waited on screen before the word that uses them (a chart frame with no data, an empty card) | [CHECK] each part has its own word in the storyboard; a still 0.2 s before each word shows nothing of that part |
| 14 | A file found in the user's folders went into the edit without asking | [CHECK] list found files, ask, use only confirmed ones; record them in the Visual sources table |
| 15 | A slam overshoot (112% for 0.18 s) pushed text outside the safe zone for a few frames | [AUTO] `safezone.py html` samples 10 times a second; the kinetic-reel `fitText()` reserves the overshoot |
| 16 | A drop shadow or card border sat under the like/comment rail though the text itself was inside; and the old alpha audit joined a top title and a low caption into one box and reported a false rail overlap | [AUTO] `safezone.py alpha` now checks the rail per pixel and the edges on the bounding box; the Remotion starter reserves room for its shadows (14 px captions, 40 px cards) |
| 17 | Composition frame rate differed from the source (30 vs 29.97): captions drifted about a frame every 33 s | [AUTO] `remotion_props.py` reads fps from the file; `probe.py` refuses VFR |
| 18 | Captions wrapped to 3 lines in the narrow `cross` zone and spilled under the description | [AUTO] Remotion starter wraps with real glyph widths, shrinks to at most 2 lines and clamps the block; `captions.py --platform` WARNs on overflow |
| 19 | A shutter (or any landing) SFX fired at the card's first frame, before it visibly landed | [CHECK] place the SFX with `"peak_at"` on the frame the card settles (spring settle, about 0.25-0.35 s after its start), checked on a still |
| 20 | The safe-zone design guide was left on and rendered into a deliverable | [AUTO] Remotion starter defaults `showSafeZone` to false and `remotion_props.py` always writes false; HyperFrames guides are separate PNGs, never in the composition |


# ===== FILE: assets/presets/kinetic-essay.md =====

# Preset: kinetic essay (metromedia-style)

**Opt-in only.** Use this preset when the user picks it, names @metromedia.house or a similar kinetic-essay
page as the reference, or approves it from the style options. It is one style among many: never apply it to a
project that did not choose it, and never let it leak into another preset's defaults. Measured grammar behind
it: `references/motion-reels.md`. Starters: `assets/hyperframes/kinetic-reel/` (HyperFrames) or
`assets/remotion/` (Remotion, when the edit needs frame-level control).

These rules came from the user's own project with this style. Inside this preset they are rules; outside it
they are options to offer.

## Look: never flat

- Every frame carries texture: grain, paper, dust, vignette or soft light (pick one or two, not all). This
  applies to storyboard frames too, so the approval page shows what will ship.
- Glow on the big (apex) words. Full motion on every element: nothing static on screen.
- Keep texture subtle: grain 2-4% at 1080p, vignette edges at most 35-45% dark. Check on a phone at full
  brightness; if the texture is the first thing you notice, halve it. Grain goes on once (footage OR graphic
  layer, never both).

## Text blocks

1. Small lines start at the big word's left edge, with tight spacing (line gap 0.1-0.2 of the small size).
2. A small line at least 35% as wide as the big word stretches to match the big word's width (scale the font,
   not the letter-spacing). Shorter lines stay at natural width, left-aligned to the big word.
3. A line on its own is big, centred, and grows as each word is spoken (each new word adds to the line; the
   line rescales to keep its width inside the safe box).
4. Centred lines are centred on their INK, not their advance width: trailing spaces, punctuation and side
   bearings make a line look lopsided. Measure with canvas `measureText` (`actualBoundingBoxLeft/Right`) or
   Remotion `measureText`, then offset.

## Layout

- Instagram safe zone always: 220 px clear at the top, 420 px at the bottom, away from the right-side icons
  (`--platform reels`; audit with `safezone.py`).
- Graphic and text are one unit: no empty gaps between them, and no part of a graphic waits on screen before
  the word that uses it. Each part appears on its word.

## Visuals

- Ask before using any file found in the user's folders (it may be private or unlicensed for this use).
- The user's stills become photo moments: a full-frame push-in, or a bordered card, each with a shutter
  sound on the frame it lands.
- Missing visuals: offer image prompts (`work/prompt-pack.md`) instead of a stock filler.

## Sound

- The music rises into the climax and stops dead (`finish.py --music-stop <t> --music-tail cut`).
- The silence after the stop measures at least 14 LU below the programme: `qa.py <final> --silence-at <t>`
  must PASS. Long hit or reverb tails are the usual reason it fails: trim or fade them before the stop.
- A sound effect on every visible change (word slam, ground change, card land, shutter). Vary repeats
  (`finish.py` does), keep pops 8-14 dB under impacts.

## Checks that belong to this preset

| Check | How |
|---|---|
| Safe zone | `safezone.py html <dir> --platform reels` (HyperFrames) or `safezone.py alpha qa.mov` (Remotion) |
| Dead stop is silent | `qa.py final.mp4 --silence-at <stop time>` |
| Texture not too strong | look at `qa/overview.png` at phone size; grain should vanish at arm's length |
| Lines centred on ink | stills of every centred line, guide on |
| Glitch and slam never on the same beat | storyboard MOVES column: one transition effect per beat |


# ===== FILE: references/remotion.md =====

# Remotion: when to use it, how to build with it, how to check it

Remotion renders React components to video, one frame at a time: every pixel is a function of
`useCurrentFrame()`. That is why it gives more control than HyperFrames: any value (position, size, colour,
which word is lit, how far a counter has run) is plain code you compute per frame, with types, components and
data. The price is a heavier setup (Node project, ~250 npm packages, React) and slower renders.

If the user's Remotion plugin or skill is installed (for example Remotion's official agent skills), load it
for API details. This file owns the editing workflow around Remotion: tool choice, safe zones, timing from the
transcript, QA and the hand-off to `finish.py`.

## 1. HyperFrames or Remotion (decide per graphic, say which and why)

| Need | Pick | Why |
|---|---|---|
| One card, lower third, title, quick overlay | HyperFrames | plain HTML/CSS/GSAP, no build step, transparent MOV in one command |
| The `kinetic-reel` starter, HyperFrames' own `/talking-head-recut`, `/embedded-captions`, `/faceless-explainer` | HyperFrames | those workflows already exist and are tested |
| Exact frame-level control: values computed in code per frame, complex word-synced logic, layout from measured text | **Remotion** | everything is a function of the frame; `measureText` / `fitText` give real glyph widths |
| The whole edit in one timeline (footage + graphics + captions + photo moments) with many sequences | **Remotion** | `<Sequence>` per element, `<OffthreadVideo>` frame-exact, one render |
| Many variants from data (ad hooks, 10 language versions, a weekly series template) | **Remotion** | one component, different `props.json` per render; scales to Remotion Lambda |
| Audio-reactive visuals (waveforms, bars on the voice) | **Remotion** | `@remotion/media-utils` `visualizeAudio` per frame |
| Live preview with editable props for the user | **Remotion** | `npx remotion studio` |
| The user is a company with 4+ employees and has no Remotion Company License | HyperFrames | Remotion's free licence covers individuals, for-profit organisations up to 3 employees and non-profits; bigger companies need a Company License (remotion.pro). Ask once and note it in EDIT_STATE.md |

Both tools can be in one project: HyperFrames for a quick card, Remotion for the main timeline. Pick one per
element and keep the same safe zone, fonts and accent across both.

## 2. Where Remotion sits in the pipeline

1. Rough cut (`render_cut.py`), then grade (`grade.py`). The cut is locked before Remotion starts.
2. Remotion replaces steps 3 and 4 (graphics and captions): the composition takes the graded cut through
   `<OffthreadVideo>`, draws graphics on their words and captions on top, in one render. Or it renders only a
   transparent overlay that `overlay.py` places (use this when the cut may still change).
3. `finish.py` on the Remotion output: music, SFX, ducking, two-pass loudness, platform encode. Do not mix the
   final sound inside Remotion: the skill's loudness, ducking and dead-stop checks live in `finish.py` and `qa.py`.
4. `qa.py` on the final, `safezone.py alpha` on the text-only render.

## 3. Start from the starter

`assets/remotion/` (tested, see its README): captions grouped like `captions.py`, wrapped with real glyph
widths and kept inside the platform zone, `title` / `stat` / `image` graphics that start on their word.
`scripts/remotion_props.py` builds `props.json` from the cut, `words_cut.json`, key words and a graphics list,
and copies media into `public/`. Every style choice is a prop: fonts, size, colour, accent, highlight rule,
words per group, position, texture. Fill them from the style card, never from a default look.

## 4. Rules that fail silently if broken

- **Pure function of the frame.** Animate with `interpolate`, `spring`, `Easing`; random with `random(seed)`.
  No `Math.random()`, `Date.now()`, `setTimeout`, CSS transitions or keyframes: Remotion renders frames in
  parallel and out of order, so anything stateful flickers or desyncs.
- **Async loads are gated.** Fonts, JSON and measured images load inside `delayRender()` /
  `continueRender()`. A font that is not loaded renders with a fallback and every measured width is wrong.
  Read the render log for `FONT MISSING`.
- **Footage through `<OffthreadVideo>`** (frame-exact extraction), assets through `staticFile()` from
  `public/`. A remote URL in a render is a network dependency that can fail mid-render.
- **Composition fps = source fps.** A 29.97 source in a 30 fps composition drifts about 1 frame per 33 s
  against the words. `remotion_props.py` reads the fps from the file.
- **Duration from data.** `calculateMetadata` sets `durationInFrames` from the cut's duration (or the last
  word); a hard-coded duration cuts the ending or leaves black.
- **Sizes from the zone.** Every text block computes its width from `centredWidthAt(zone, ...)` for the band
  it occupies, and its height from its line count. Never place text at fixed pixels on 9:16.
- **Shadows and borders are part of the graphic.** The safe-zone audit counts every visible pixel, including a
  drop shadow under the like button. Reserve the shadow's reach in the layout (the starter does: 14 px for
  caption shadows, 40 px for card shadows).
- **Never ship the guide.** `showSafeZone` is a design aid in Studio; default it to false.

## 5. Rendering

```bash
npx remotion render src/index.ts Edit out/edit.mp4 --props=props.json --crf=18          # H.264 with the cut's audio
npx remotion render src/index.ts Edit out/qa.mov --props=props_qa.json --codec=prores --prores-profile=4444 \
    --image-format=png --pixel-format=yuva444p10le                                    # transparent, for QA / overlay
npx remotion render ... --frames=0-89                                                 # first 3 s only, fast check
npx remotion still src/index.ts Edit out/f120.png --props=props.json --frame=120       # one frame to look at
```

- Remotion downloads its own Chrome Headless Shell on the first render. Offline or in a sandbox, pass
  `--browser-executable=<path to chrome-headless-shell>`.
- Speed: measured here, 19 s of 1080x1920 took about 2 minutes at concurrency 2. Check single frames with
  `remotion still` while designing; render the full video once the stills are right.
- Transparent output: ProRes 4444 `.mov` (above) or VP9 WebM (`--codec=vp9 --image-format=png
  --pixel-format=yuva420p`). H.264 has no alpha.

## 6. QA (same bar as everything else)

1. `npx tsc -p .` clean (the starter ships `tsconfig.json`).
2. Stills at every graphic's first frame, middle and exit; look at each.
3. 9:16: text-only render, then `safezone.py alpha out/qa.mov --platform <zone>` must PASS. Rendering one zone's
   layout and auditing it against another zone fails, as it should.
4. Frames from the final MP4 (not Studio screenshots) for `qa.py`; the render log has no `FONT MISSING`.
5. The rest of `references/qa-checklist.md` as for any edit.


# ===== FILE: references/motion-reels.md =====

# Motion-graphics reels: the kinetic-type genre

One genre family among the many this skill edits: kinetic-type reels like **@metromedia.house, @earn.edits,
@earnera.co and @lightyear.residency**. Use this file when the chosen style is kinetic type (the user picked
it, named one of these pages, or approved it from the style options). Do not default to it: a reel can just as
well be a clean talking head, a documentary cut or a UGC ad. The opt-in rule set from the user's own project in
this genre is `assets/presets/kinetic-essay.md`. Every number here was measured frame by frame on 12 of these
reels (downloaded 2026-10-12, text heights in pixels, colours as saturated-pixel medians). Audio on those reels
was not analysed, so every audio claim about them is unverified. Their posts were ranked by likes (Instagram
hides views): never call them "most viewed".

Reading key: **[MEASURED]** frame-measured on the reels; **[SECONDARY]** code/docs, not video;
**[UNVERIFIED]** not confirmed.

## Contents
1. The shared grammar (7 rules)
2. Per-page spec sheets
3. How to build it with this skill
4. Kinetic-type toolkit (2025-2026)
5. SaaS-demo grammar
6. Documentary grammar (Vox / Johnny Harris)
7. New Look candidates
8. Transitions and timing
9. Carve-outs from the default ban list

## 1. The shared grammar

1. **Two-tier type.** A whisper tier at about 4-6% of frame height carries the sentence; an apex tier at
   13-24% punctuates one word. Ratio about 3-5x. Measured: metromedia 5-5.5% / 24%, earnera 5.5% / 19.2%
   (368 px on 1920), lightyear 4-5% / 13%. This is 2-3x bigger than ordinary hook text (6-9%), and apex words
   may overlap faces. Why: size contrast is read before language; the giant word is the thumbnail inside the
   video. [MEASURED, 3 pages converge]
2. **Selective captioning.** Text appears on beats only: 25-40% of words (claims, numbers, turns, openings),
   never always-on subtitles. Why: constant text gets filtered out like a watermark. The SRT sidecar stays
   complete for accessibility. [MEASURED on lightyear + earnera]
3. **Typography is the visual.** Kinetic type performs on footage or B-roll as its canvas; the edit reads as
   designed on mute. [all 4 pages]
4. **Annotation over decoration.** Hand-drawn ellipses and circles, red stamp boxes, node-line diagrams,
   parentheses as graphics, red-pen arrows. A mark that points says "look here"; decoration says "look at
   me". All SVG-buildable. Never particles.
5. **One accent per video.** metromedia orange #D17054 (+ kill-red #D7371B), earn.edits yellow #D1AC18 /
   red #923F3C, earnera green #1A9B10, lightyear white only. [MEASURED]
6. **Grain on every frame.** Film or paper grain, wood/paper grounds. Grain removes code-rendered flatness
   and dithers gradients against platform compression banding. Keep it 1-5%.
7. **Soft-sell end card held about 3 s.** Brand + one line ("comment 'project'", "apply today"); never a
   hard pitch, never "thanks for watching". [MEASURED: earnera ~3 s, lightyear ~3 s]

Format note: metromedia and lightyear post **16:9 landscape masters as reels**. Instagram letterboxes them in
the Reels player (black bars top and bottom); it does not centre-crop. Keep all type centre-safe so it reads
on both surfaces. A landscape master is a legitimate option, not an error.

## 2. Per-page spec sheets

**@metromedia.house** (16:9 kinetic-typography business essays, 64-124 s)
- Centred kinetic-word system: white bold neo-grotesque, lowercase, cap height about 5-5.5%, centred at
  y 0.45-0.55 (not lower third), 1-3 words, **word-by-word hard pop, 0 frames of transition**.
- Display words about 24% lowercase; kill-words red serif ALL CAPS #D7371B at 24-26%.
- Orange starburst brand accent: about 0.2 s scale-down from oversize (a slam).
- Photo cards: archival photo, 4 px white square border, centred on dark blurred #302E2A.
- Hook: accelerated photo + word montage, about 5 beats in 3 s, then essay pace.
- Pacing per section: calm ~30 cuts/min, montage bursts 90-140/min. Never metronomic.
- Reels: instagram.com/reel/Ddy9H_LIZgr, /DdCAyFsBSbp, /DeKHcthhKyd

**@earn.edits** (9:16 / 1:1 documentary-mograph tutorials, two modes)
- Mode A (Vox-style documentary): serif-italic display stack, 3-line lockup small / HUGE / small, keyword cap
  about 9-10%, upper-left; hand-drawn yellow ellipse + red stamp boxes; collage on wood/paper; 12-38
  changes/min.
- Mode B (sticker mograph): condensed all-caps on rotated coloured boxes with speech-bubble tails (#D1AC18),
  about 7.4% cap, hard cuts, about 134 changes/min (density matches 130-140 BPM; beat sync [UNVERIFIED]).
- Reels: instagram.com/reel/DbVMvRvMboX, /DeG9eYVOknN, /DcyLc5ZMJIB

**@earnera.co** (9:16 native kinetic-type quote breakdowns, 37-45 s)
- **Typewriter feed**: the active line bright white, snapping to centre; surrounding lines dimmed
  (`captions.py --style 12`).
- Apex words 19.2% (Anton/Oswald-style condensed; exact family [UNVERIFIED]).
- Text-as-mask reveals: flame/ink through letterforms.
- **Rebuilt UI mockups**, never flat screen recordings: X post, Spotify player, iMessage, Google search bar
  as 3D-tilted cards with a slow push-in.
- Accent green #1A9B10. A structural beat every 3-7 s; flash/punch transitions 2-15 frames (70-500 ms).
- Hook: UI mockup first (familiar interface + typing cursor = recognition + curiosity), no burned hook text.
- Reels: instagram.com/reel/DSxDRZRDKVT, /DRzcFdBjDPG, /DRU0zfKjJ5L

**@lightyear.residency** (16:9 prestige docu-montages, 33-52 s)
- Whisper lowercase italic serif about 4-5% + Didone serif ALL CAPS about 13% with a soft outer glow (the
  glow here is a deliberate Look choice, see section 9).
- Spotlight isolation: radial highlight on one face in a group photo, the rest falls to blur/dark.
- Ken Burns into a frame: photo pushes full-bleed, then shrinks into a white-bordered frame.
- B&W to colour reveals; white flash-frame transitions.
- Hook: full-bleed archival recognition photo, first text at about t = 2 s.
- Reels: instagram.com/reel/Db8r7cxhSQh, /Db3mpgop3N8, /DdR32Wpy4mg

## 3. How to build it with this skill

| Need | Use |
|---|---|
| Two-tier kinetic type over footage, fast | `captions.py --style 11 --keywords k.json --selective` (whisper Inter + Anton apex, hard pops) |
| Typewriter feed | `captions.py --style 12` |
| Full designed reel (grounds, annotations, apex slams, end card) | `assets/hyperframes/kinetic-reel/` starter, then extend |
| Rebuilt UI mockups, bento cards, charts | HyperFrames compositions (motion-graphics.md) |
| Grain on footage | `grade.py --grain 2` (HyperFrames graphics carry their own `grain.png`) |

Sizing in libass: the font size is not the cap height. Anton capitals are about 50% of the font size, most
grotesques about 70%. `captions.py` style 11 sets the apex font at 36% of frame height, which lands about
18% cap height (36% x 0.5). Do not "correct" this with the 0.7 ratio of other fonts: with Anton that would
ask for a 26% font and blow the safe width. On 9:16 a long apex word shrinks to fit the safe width; that is
physics, not a bug. Keep apex words short (one word, ideally 4-7 letters) when the format is vertical.

**Safe zone.** Every apex word, whisper line, annotation label and end-card line must sit inside the
platform's safe box (`platforms-and-styles.md` PART B; the user's Instagram reference is
`assets/safe-zones/reels-safe-zone-reference.png`: 220 px top, 420 px bottom, 1010 x 1280 px safe area, the
like/comment rail bottom-right). The kinetic-reel starter takes `data-platform="reels|reels-ad|tiktok|shorts|cross"`
on `#root` and its `fitText()` shrinks each word to that stage, reserving room for the 1.12 slam overshoot
and the annotation ellipse. Prove it with `python3 scripts/safezone.py html <dir> --platform <zone>` (PASS
required) before rendering.

**Grain once.** Grain the footage (`grade.py --grain`) OR the graphic layer (`grain.png`), never both on the
same pixels: stacked grain doubles the noise and the encoder smears it into blocks.

## 4. Kinetic-type toolkit (2025-2026)

- **Variable-font weight ramp.** Animate `font-variation-settings: 'wght' 100 -> 900` per letter by distance
  from a moving point: weight = 900 - 800 x clamp01(distance / 600), easeInSine. Drive it from a virtual
  pointer on the timeline (a pure function of t), never mousemove. Animating weight changes glyph widths and
  makes lines re-wrap: use a variable monospaced font (Martian Mono). Source: SuperHi,
  youtube.com/watch?v=qMyEjp3kqCg, 02:03-03:01 and 14:14-19:46.
- **Typed text with a trailing accent** (the SaaS caption engine). Two stacked per-character tracks: reveal
  with `ease: "steps(1)"` (hard typing), then an accent track slightly after (colour pop + 8 px rise). A
  pause is a fixed gap (`tl.to({}, {duration: HOLD})`), never `tl.addPause()`. Source: NeuronFX,
  youtube.com/watch?v=zIjQmt5rccU, 02:38-06:35.
- **Word explode + colour cascade.** Per-word stagger 0.0667 s (2 frames at 30 fps), fill cascades accent ->
  darker -> black across consecutive words, about 1.0 s total. Source: Solair Motion,
  youtube.com/watch?v=GVSKq40wWiA, 08:50-09:44.
- **Scribble text and hand-drawn underline** (Vox-family emphasis). Handwritten keyword, multiply blend,
  jittered displacement updated 6 times a second (the jitter is the style). HyperFrames: `feDisplacementMap
  scale=4` with the seed as `BASE + floor(t x 6)` (seek-safe). Underline: wobbly stroke about 8 px, draw-on
  about 1 s fast-to-slow, erase slow-to-fast. Source: "How To Edit Like Vox",
  youtube.com/watch?v=VDWP0aSXxc8, 24:22-25:05. Note: SVG turbulence filters can render blank in headless
  capture; check a snapshot, and fall back to pre-drawn jitter frames if it is blank.
- **Kinetic-reel type stack** (1920x1080 values; scale by % of frame height for 9:16): Anton 130-330 px
  headlines, Archivo Black 172-250 px one-word slams with outlined echoes, Instrument Serif italic 124 px
  voice line, JetBrains Mono 14-26 px / 700 / 2-8 px tracking labels. Palette ink #0E0F0E, cream #F1EEE6,
  lime #DDF53D (the accent), blue #2F3CFF, red #E8412F (failures only). **Rotate the ground between shots**
  (ink -> lime -> ink -> cream) so every cut is a visible change. [SECONDARY: tuzhechen2005/opus-video-skills,
  kinetic-reel style guide]
- **dropWord presets.** Per-letter stagger 0.03 s, fall 90-260 px, entrance 0.32 s expo.out; counters roll
  expo.out; odometer per-digit stagger 0.15 s. Beat lock: cuts on beats, **chapter changes on bars**, one
  timeline drives picture and score. [SECONDARY: same repo]
- **Vertical cut reveal stagger modes.** Words/characters/lines slide up inside overflow-hidden masks; stagger
  order first / last / centre / random; bake springs as expo.out 0.5-0.7 s. [SECONDARY: 21st.dev]

## 5. SaaS-demo grammar

- **Cursor as a character.** A custom cursor element (about 200 px), linked to the text end; vocabulary star /
  box / circle / underscore / arrow; jump-in at the start and jump-out at the end are beats. It carries the eye
  across the cut. Source: NeuronFX (zIjQmt5rccU) 07:17-12:44.
- **Animated bento cards.** Grid of 3 columns, rows 280 px; card = low-opacity gradient, `backdrop-filter:
  blur(24px)`, faint white border, radius 28 px; the "hover" is choreographed on the timeline (translateY
  -10 px + scale 1.02 + shadow, 0.5 s), never CSS :hover; dark navy ground with two radial gradients and a
  grid; counters snap to integers; SVG draw-on with `pathLength="1000"` and dashoffset 1000 -> 0. Source: IT
  Master, youtube.com/watch?v=C0yro0rgSII, 09:38-15:46.
- **The click is the climax.** Button scale + fill keyed to the cursor's arrival on one timeline; the UI change
  happens on the click frame, then cut. Source: Solair Motion (GVSKq40wWiA) 05:38-07:48.
- **Depth-reveal transition.** The incoming scene appears near-field first through a depth map, with a scale
  1.06 -> 1.0 expo.out about 0.6 s. HyperFrames: a pre-baked depth-map PNG or a blurred mask wipe. It has a
  carrier (depth order), unlike a crossfade. Source: Solair Motion 00:23-01:03 (timing [UNVERIFIED]).

## 6. Documentary grammar (Vox / Johnny Harris)

- **Map-zoom ladder.** 8 stacked map images at halving scales (94.1, 46.8, 23.6, 11.6, 5.7, 2.9, 1.4, 0.7),
  aligned at 50% opacity with feathered edges; one camera move about 2.5 s; paper texture multiply plus about
  25% tint. Code: 8 nested divs each scale(0.5), one camera tween scale 1 -> 128. A single scaled image falls
  apart; the ladder stays sharp. Source: VDWP0aSXxc8, 01:25-10:06.
- **Marching-ants routes.** Dashed stroke with `stroke-dashoffset = t x -60` (pure function of time), drawn
  on with the camera move. Source: same, 25:33-26:33.
- **Ink-matte reveal and Z-push.** Bake the ink bleed as a PNG sequence used as a luminance mask (a video matte
  is not seek-safe). Z-push: open scene B on scene A's exact last frame and push through it, bridged with a
  dirt-lens overlay. Source: same, 11:04-12:02 and 18:07-22:02.

## 7. New Look candidates (beyond the 20 Looks)

- **Pixel art.** Draw to an offscreen canvas at a fixed logical resolution (e.g. 128x96), integer-scale blit
  with `imageSmoothingEnabled=false` and `image-rendering: pixelated`; snap everything to integer pixels; a
  fixed palette of about 24 colours; quantise poses to the pixel grid every frame (8-12 fps feel). Without the
  fixed resolution, "pixel art" prompts produce blurry scaled vectors. [SECONDARY]
- **Flat cartoon**: bold rounded shapes, thick dark outlines, flat fills with one shade tone, squash and
  stretch on every move. **Generative neon**: procedural shapes, dark ground, 3-4 colours, motion locked to
  the beat. **Photoreal edit**: real footage cut on beat, restrained type, every shot matched to one grade.
  [SECONDARY, CC BY 4.0 style recipes]
- **Paper collage** (earnera's signature): graph paper, tape, sticky notes, red-pen annotations, toggle
  diagrams, photo grids with one outlined cell; animate collage on twos (12 fps). [MEASURED]
- **Sharp chrome**: square corners, 0.5 px hairlines, 11 px mono uppercase micro-labels, restrained motion;
  for dev-tool and fintech explainers. [SECONDARY]

## 8. Transitions and timing

- **Transitions 0.45-0.6 s; never three of one kind in a row.** Inside a chapter prefer shape continuity
  (zoom through the element the eye is on, iris from the thing that just lit up); save hard cuts with an
  impact for chapter slams. [SECONDARY]
- **The "reads" model.** List what the viewer must understand in a shot; each is a read (find, understand,
  register: about 1 s each). One read at a time: two simultaneous events means the viewer sees one. Reads set
  shot length: a shot with many reads cannot be short; a finished read should not be padded. [SECONDARY]
- **Hard pops are `tl.set`, not tweens.** An opacity tween of even 0.18 s is a fade. Make visibility instant
  and tween only a short scale settle (e.g. 112% -> 100%, 0.18 s expo.out).

## 9. Carve-outs from the default ban list

- **Status pulses are information, not idle wobble.** A heartbeat circle, a rotating dashed gear (linear), or
  staggered network dots that say "this system is running now" are allowed; transform/opacity only, inside a
  finite timeline: `repeat: Math.floor(sceneDuration / cycle) - 1`, never `repeat: -1`. Source: IT Master (C0yro0rgSII) 06:33-08:29.
- **Glass is conditional.** Allowed faint, bordered and behind type (never on the type itself); still banned as
  the default chrome of a whole video. The successor treatment is a soft ambient mesh gradient.
- **Glow** stays banned by default; lightyear's soft glow on Didone caps is a deliberate Look choice, allowed
  when the user picks that register.
- **The 70/20/10 check.** About 70% of the visual weight on the primary device (e.g. the apex type), 20% on the
  secondary (footage, cards), 10% on accents. "Everything everywhere" fails this check. [SECONDARY]


# ===== FILE: references/motion-graphics.md =====

# Motion graphics, explainers and B-roll cards

Contents: 1 Tool choice · 2 Install HyperFrames + official skills · 3 Two ways to put graphics on footage · 4 The composition contract (fallback) · 5 Card planning for talking heads · 6 Motion doctrine · 7 Seam and entry techniques with numbers · 8 The production-spec brief · 9 Technique catalog · 10 Explainer templates · 11 Learning-science rules for explainers · 12 QA for graphics · 13 Conflicts resolved

Sources: HeyGen HyperFrames official skills (Apache-2.0: `hyperframes`, `hyperframes-core`, `talking-head-recut`, `motion-doctrine`, `cut-the-curve`, `seam-craft`), the 513-prompt Opus 5.5 study (`motion-prompt-research.md`), WeAreNoCode Looks (`looks-library.md`), `design-science.md`.

**Making a kinetic-type reel** (the style the user chose is kinetic type, e.g. metromedia / earn.edits / earnera / lightyear)? Read `motion-reels.md` first; `assets/hyperframes/kinetic-reel/` is the tested starter. For any other style, this file is the general craft. **Remotion** instead of HyperFrames: `remotion.md`.

## 1. Tool choice

| Need | Use | Why |
|---|---|---|
| Any designed graphic, card, title, chart, explainer, kinetic text | **HyperFrames** (`npx hyperframes`) | Plain HTML/CSS/GSAP, no build step, made for agents: `lint`, `check`, `snapshot` contact sheets, transparent MOV/WebM output, a 446-item registry of captions, lower-thirds and transitions |
| Plain word captions on footage | `scripts/captions.py` (libass) | Seconds to render; HyperFrames captions only when you need web-only looks |
| Simple punch-ins, crops, reframes | ffmpeg (`render_cut.py --punch`, `reframe.py`) | No browser render needed |
| Frame-level control in code, the whole edit in one timeline, data-driven variants, audio-reactive visuals, or an existing Remotion brand kit | **Remotion** (`assets/remotion/`, `remotion.md`) | Every value is a function of the frame; React components and props. Free for individuals, companies up to 3 employees and non-profits; bigger companies need a Company License |

## 2. Install HyperFrames and its official skills

```bash
npx hyperframes@latest doctor            # Node >= 22, ffmpeg, Chrome headless shell
npx hyperframes browser ensure           # downloads Chrome headless shell (~114 MB) once
npx hyperframes skills update            # installs HeyGen's core skills (router + domain skills)
npx hyperframes skills update talking-head-recut motion-graphics embedded-captions faceless-explainer
```

Skills load at the start of a thread: tell the user to open a new thread after installing. If `skills update` fails (restricted network, GitHub blocked), do not stall: build with the fallback contract in section 4 and the starters in `assets/hyperframes/`. When the official skills are present, **follow them for the composition mechanics** (they are maintained with the CLI and change between versions) and use this file for taste, planning and the editor workflow around them. Route like this:

| Deliverable | Official workflow |
|---|---|
| Designed cards over a talking head (titles, lower-thirds, data callouts, quotes, side panels, PiP) with the clip untouched | `/talking-head-recut` |
| Captions / cinematic captions behind the subject | `/embedded-captions` |
| Short standalone motion piece under ~10 s (stat hit, logo sting, lower-third, chart hit) | `/motion-graphics` |
| 60-90 s explainer from a topic, article or notes, no footage | `/faceless-explainer` |
| Promo from a website / product URL | `/product-launch-video` |
| Beat-synced piece from a music track | `/music-to-video` |
| Anything else, longer or custom (cuts, retimes, montages) | `/general-video` |

Gotchas verified while building this skill:
- The scaffold loads GSAP from a CDN. Offline or behind a proxy the render fails with `Cannot read properties of null (reading 'timeline')`. Vendor it: copy `gsap.min.js` next to `index.html` (from `npm pack gsap` or `node_modules/gsap/dist/`). Vendor fonts too (`scripts/fetch_fonts.py`), because missing fonts fail silently to a fallback face.
- `-q draft` renders Baseline H.264: never ship it. Default quality (`looks`, CRF 16) or `delivery` for finals.
- macOS: `PRODUCER_BROWSER_GPU_MODE=hardware` (or `--browser-gpu`) is strongly recommended, software rendering times out on many laptops.
- A composition with no registered timeline waits 45 s per render: add `data-no-timeline` for static ones.
- Source footage with sparse keyframes freezes on seek. `probe.py` warns; re-encode with `-g <fps> -keyint_min <fps>` (render_cut.py output already does this).
- Transparent WebM keeps alpha only when ffmpeg decodes it with `-c:v libvpx-vp9` (overlay.py handles it). ProRes 4444 `.mov` is the safest alpha format.
- MOV/WebM renders print "BeginFrame did not run ... screenshot capture (slower)": harmless, transparent formats use screenshot capture (a 5 s card took about 40 s).
- `snapshot --at` also adds an end frame unless you pass `--no-end`; files are numbered in capture order, not time order.

## 3. Two ways to put graphics on footage

**A. Footage inside the composition (talking-head-recut pattern).** The edited video is a `<video>` layer in `index.html`; cards are timed clips above it; one render outputs the final picture with the original audio. Best for: heavy packaging, layouts where the video moves (split, stack, PiP), many cards. Cost: the whole video renders through Chrome (minutes per minute of video).

**B. Graphics rendered separately, composited with ffmpeg.** Each graphic is its own short composition rendered with `--format mov` (alpha) or as a full-frame MP4 cutaway, then `scripts/overlay.py base.mp4 graphics.json out.mp4` places it at the spoken word. Best for: long videos with a handful of inserts, fast iteration on one graphic, reusing graphics. Starter: `assets/hyperframes/lower-third/` (lint-clean, render tested).

Either way: **captions go last**, on top of every graphic.

## 4. The composition contract (fallback when the official skills are not installed)

Minimal standalone `index.html`:

```html
<div id="root" data-composition-id="main" data-start="0" data-duration="5" data-width="1920" data-height="1080">
  <section id="card" class="clip" data-start="0" data-duration="5"> ... </section>
</div>
<script>
  const tl = gsap.timeline({ paused: true });
  tl.fromTo("#title", { y: 48, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, 0.2);
  window.__timelines["main"] = tl;   // key must equal data-composition-id
</script>
```

Rules that `lint` enforces or that fail silently:
- **`fromTo` only**, never `from` or `to` alone on anything the renderer may seek into: `from` records its end state at creation time and breaks on a backwards seek.
- **One flat timeline.** No nested timelines started by callbacks, no `tl.call()` that starts other tweens, no `onComplete` chains. Everything sits on the one paused timeline at an absolute position.
- **Register the timeline LAST**, after fonts are loaded and the layout is final: `Promise.all([document.fonts.load("900 120px Anton"), ...]).then(build, () => build())`, where `build()` measures text, then creates the timeline, then sets `window.__timelines[id]`. Registering earlier renders the first frames with fallback metrics, and fit-to-width math is wrong.
- **Finite repeats only.** `repeat: Math.floor(duration / cycle) - 1`, never `repeat: -1` (an infinite tween makes the timeline length infinite and some renders hang or cut).
- **No background on `html` or `body`.** Put the background on the root element (or leave it transparent for overlays); a body background is either dropped or it kills alpha.
- **Media `src` on the element itself**, never on a `<source>` child and never set later by JS.
- Exactly one paused GSAP timeline per composition, registered at `window.__timelines["<composition-id>"]`. Render length is the root `data-duration`, not the timeline length.
- Never pair a CSS `transform` with a GSAP tween on the same element and property: use `gsap.fromTo`. Centre with flex/inset, not `translate(-50%,-50%)` on something GSAP moves.
- Never tween `display`, `visibility` or `autoAlpha` on a `.clip`: animate a child. The runtime owns clip visibility.
- Every `<audio>` and timed `<video>` needs an `id` (id-less audio renders silent). No `crossorigin` on media. A `<video data-start>` must not sit inside another plain element with `data-start`.
- Named `font-family` needs a local `@font-face`. List concrete font names on `body` (the font checker does not expand CSS variables).
- Determinism: no `Math.random()` (use a seeded PRNG), no `Date.now()`, no timers, no network, no CSS transitions or keyframes driven by wall-clock time; `repeat: -1` only under a finite root duration. Every frame must be a pure function of time.
- Animate `transform` and `opacity` for motion; animate the wrapper of a video, never the video element's size.
- **Mask reveals** (text rising through an `overflow:hidden` line) make `check` report `text_occluded`. The occlusion is intended: put `data-layout-allow-occlusion` on **every text node inside the mask** (including `<b>`, and spans you generate in JS), and `data-layout-allow-overflow data-layout-allow-occlusion` on the mask itself. Both starters do this.
- **Counters must be seek-safe.** The renderer seeks to arbitrary times, and `onUpdate` callbacks may not fire on a seek. Tween a property on a plain object with a setter that writes the text, so every frame is a pure function of time:
  ```js
  let _v = START; const counter = {};
  Object.defineProperty(counter, "value", { get() { return _v; },
    set(v) { _v = v; numEl.textContent = Math.round(v).toLocaleString("en-US"); } });
  tl.fromTo(counter, { value: START }, { value: END, duration: 1.5, ease: "power3.out" }, 0.95);
  ```
  Digits must not jitter while counting: Google's static TTFs do not always expose the `tnum` feature, so give every digit a fixed-width slot (`.d { display:inline-block; width:0.62em; text-align:center }`, see `assets/hyperframes/stat-counter/`) or use a mono figure font (JetBrains Mono, Geist Mono).
- **Overlays must start and end fully transparent** (finish exits at least 0.2 s before the end), or the card pops on or off at the cut. `scripts/qa_graphic.py` checks this.
- **Contrast on transparent overlays:** `check` reports "0/0 text checks" because there is no background to measure. Judge it with `scripts/qa_graphic.py` sheets (over black, white and grey); if text fails on any of them, strengthen the plate or shadow.
- Workflow: `npx hyperframes lint .` then `npx hyperframes check .` (0 findings; a lint error silently disables the layout and contrast audits) then `npx hyperframes snapshot . --at 0.5,1.5,3` and LOOK, then `npx hyperframes render . -o out.mp4` (or `--format mov` for alpha).

## 5. Card planning for talking heads

How many cards (from HeyGen's talking-head-recut, which works well in practice):

| Video length | Base pace (s per card) |
|---|---|
| < 60 s | 6-8 |
| 1-3 min | 8-12 |
| 3-10 min | 12-20 |
| 10-30 min | 20-35 |
| > 30 min | 30-60 |

Multiply by 0.7 for dense content (numbers, lists, a new idea every sentence), 1.5 for one slow story. `cards = max(5, round(duration / pace))`. A card held longer than about 15 s needs a richer inner build (staged reveals), because a static one-liner gets boring after about 8 s.

Podcast/long-form density from the prompt study: 35-50 graphic moments per episode, at least 2 per chapter, each graphic inside one uncut stretch of audio, a few seconds of face between graphics, the speaker in PiP when a graphic goes full-screen.

Layouts (16:9 canvas 1920x1080; for 9:16 see talking-head-recut's layout files):
- **overlay**: video full-bleed, card floats in a zone (lower-third band = bottom 30%). Cinematic, keeps the face.
- **split**: video right half, card left half. Interviews, data beside the speaker.
- **stack**: video top ~52%, card below. Classic on 9:16.
- **pip**: card full canvas, video in a rounded corner window (e.g. 400x300 at bottom-right). Content-heavy moments.

Portrait sizing: phones hold the screen close, so scale every landscape type size by about x1.3 for 9:16 (hero titles 88-132 px, body 30-40 px, labels 18-22 px, key numbers 64-88 px) and shrink horizontal padding to 24-36 px.

Every card: real words from the transcript, appears on its spoken word (within about 150 ms), one idea, readable hold (`words x 0.3 s + 0.5 s`, minimum 1.2 s).

Placement offset: "land on the word" refers to the meaningful moment, not frame 0 of the graphic. For a counter, the number should land as the speaker says it, so `at = word_time - (time inside the graphic when the count lands)`. For a card that builds in 0.4 s, start it about 0.3 s before the word so the text is readable as the word is spoken.

## 6. Motion doctrine (why premium motion feels like one camera move)

From HyperFrames' motion-doctrine. The failure it prevents: scenes authored in isolation, so the eye's momentum dies at every cut and elements wobble in place between entry and exit.

- **Vector law:** how scene A exits decides how scene B enters: same axis, same direction, matched speed, and the cut lands mid-motion on both sides. On the Z axis direction is the sign of the scale change (growing = push, shrinking = pull). The most common violation: a receding exit answered by a grow-from-small entrance.
- **The current:** pick one dominant direction for the whole film (default: leftward = "next"). Upward means a conclusion rising; Z-forward means going deeper into the same thought; Z-backward (inverse zoom) means arrival, a payoff landing. Never run consecutive seams in opposite directions; a direction change needs a visible cause.
- **Carriers:** the eye follows objects. The best seams hand a concrete object across the cut (a cursor mid-path, a card that docks into the next layout, a number that flies into its slot). A crossfade has no carrier, which is why it feels cheap.
- **Causal motion:** chain moves so each is launched by the last (click, squash, release, flight, impact, reveal). Effects start on the causing frame, never "shortly after". Big things rebound slower, small things snap.
- **No idle wobble:** breathing, floating, drifting and pulsing loops read as "the video is waiting". If a scene runs out of things to do, that is a planning bug: add story. Every phase is one of: staged reveals (default), camera with intent (establish wide, travel, arrive), sequenced UI life (progress advances, counts tick), animated sequences (a card files into a stack), cursor-led action. Test: pause on any second; something meaningful should be mid-flight.
- **Stillness before climax:** 0.3-0.75 s pause between an action and its result. The dramatic comma.
- **Timing intents:** single entry at most about 0.8 s (longer build = stagger several elements); exit about 75% of entry; total stagger at most 0.5 s; no `bounce.out` / `elastic.out`; entry overshoot `back.out(1.4-1.7)` at most; similar elements share one ease and duration.
- **Transition budget:** 2-3 inter-scene transition types per film, repeated. Default boundary: cut-the-curve in the film's current.

## 7. Seam and entry techniques with numbers (from cut-the-curve)

| Technique | Use for | Parameters |
|---|---|---|
| **Cut the curve** (default scene boundary) | between scenes, in the current | partial travel about 12% of frame (230 px at 1920); exit `power4.in`, entry `power4.out`, same distance and duration (0.3-0.34 s); exit opacity finishes at 25-30% of its travel; entry ignites at about 0.35 opacity mid-path; optional 8-10 px blur; opaque stage background or the seam flashes white |
| **Zoom-through** (forward) | swapping headline text inside a scene | exit scale 1 to 1.2, blur 0 to 10 px, opacity to 0.15 (linear), `power3.in`, 0.2 s; hard swap at peak blur; entry 0.75 to 1, blur 10 to 0, `expo.out`, 0.5 s; never two texts visible |
| **Inverse zoom-through** | arrival / payoff beat only | exit 1 to 0.8; entry arrives oversized 1.25 to 1; about 0.7 s total (30/70) |
| **Waterfall cut** | text-to-text handoff between big-text beats | per-word exit 0.34 s `power4.in`, +0.022 s stagger in reading order; entry 0.3 s `power4.out` starting at 0.35 opacity; gaps 0.05 s shrinking x0.84 per word |
| **Rack-focus blur-cut** | the one cut you want seen, at most once per ~8 s | outgoing stays opaque; cut at peak blur 8-12 px; lens-breathing scale about 1.06; `power2` eases |
| **Waterfall entry** (no seam) | title cards, list intros | elements whip in from below; opacity binary 0 to 1 (no fade); anchors travel 60-80 px over 0.16-0.20 s, normal words 40-50 px over 0.13-0.16 s, light words 30-48 px over 0.10-0.13 s; each starts within 1-2 frames of the previous settling; `power4.out`; never `.inOut` on an entry |
| **Nudge curve** (no seam) | sliding a composed group to make room | three tweens on one property: `power3.in` 10% distance in 20% time, linear 65% in 18%, `power4.out` 25% in 62%; reveal new content during the fast middle |

Blur: 10 px for text-sized subjects, 18-20 px for full-frame surfaces. Blur the wrapper, never the children, never a `<video>` directly.

## 8. The production-spec brief (what separates premium from template)

The 513-prompt study found two kinds of prompt: short "go all out" prompts (65% of real prompts, 0% of them specify easing, camera, palette or fonts, and the model falls back to its house style), and production specs (the best 10%: 95% contain bans, 80% transitions, 75% camera, 65% easing and a self-review loop). Users rarely write the second kind, so **this skill writes it for them**. Before building any graphic or explainer, fill this skeleton in `EDIT_STATE.md` and show it:

1. **Role and stakes:** "world-class motion designer; this ships on <channel> to <audience>".
2. **Inputs / source of truth:** transcript lines, real numbers, brand tokens, real screenshots, accuracy guardrails.
3. **Format:** exact duration, resolution, fps, aspect, safe area, output type (MP4 or alpha MOV).
4. **Art direction:** a Look block (looks-library.md) or the creator's measured palette and fonts.
5. **Locked copy:** the exact on-screen words in order, "no extra slogans".
6. **Beat grid:** timestamped list, each beat = visual idea + exact text + transition logic, aligned to spoken words (speech) or bars (music).
7. **Motion rules:** easing tokens, overshoot cap, stagger, enter/exit order, one camera vocabulary.
8. **Audio:** what the graphic sounds like (one soft SFX per appearing element, silence otherwise) or "silent, the voice carries it".
9. **Ban list:** start from the default (below) and add the user's never-list.
10. **Engineering contract:** HyperFrames rules (section 4), deterministic, seekable.
11. **QA gate:** one still per beat as a contact sheet, inspect, fix, then render, then inspect decoded MP4 frames.
12. **Start:** "show me the beat grid before writing code".

Default ban list (the study's production prompts banned these most: particles 8/10, bouncy easing 7/10, glows 5/10, template look 5/10, dead time 5/10): particles, glows, lens flares, shockwave rings, camera shake, bouncy or elastic easing, gradients on UI chrome, glassmorphism by default, purple/blue "AI" neon, stock HUD, text or frames parked in corners, spinning logos, typewriter on long lines, crossfades between scenes, holds over 1 s with nothing changing. Allow an item only when the user asks or the chosen Look includes it.

Restraint is not the same as plainness. The ban list removes decoration, never information: when the numbers support it, a stat card is stronger with a derived visual (a growth curve from the start value to the end value, a before/after bar, a ratio badge computed from the spoken numbers) than as a bare number. In the skill's own tests, an unconstrained run produced a richer card with a curve and a "40x growth" badge; the curve and the computed ratio were right, only the glow was wrong. Derive, never invent: every extra figure must follow arithmetically from what was said, and say so in the report.

Quality-raising phrases that recur in the best prompts (use them in briefs): "one idea per shot", "every transition is caused by an object", "hold the final frame long enough to read", "never invent numbers, quotes or features", "outgoing text fully exits before incoming text takes its place", "something premium on screen by 1.5 s", "render stills, inspect them, fix, then render".

Defaults when the user gives none: Shorts graphics 1080x1920 at 30 or 60 fps; YouTube inserts 1920x1080 at the edit's fps; brand stings about 15 s; explainer segments about 30 s; entrances `cubic-bezier(0.16,1,0.3,1)` (expo.out); overshoot at most 2% for professional work; per-word stagger 80-125 ms.

## 9. Technique catalog (pick by what the line says)

Full table with 40 entries, durations and example prompts: `motion-prompt-research.md` section 3. The ones that earn their place most often in talking-head edits:

| Spoken moment | Technique | Typical duration |
|---|---|---|
| A number ("we grew 3x") | counter roll-up with tabular digits, lands with a short annotation line | value-dependent, 0.6-1.2 s count + 1.5 s hold |
| A comparison ("before / after", "X vs Y") | side-by-side cards, the winner turns accent last | 2-4 s |
| A process ("three steps") | numbered steps built one per beat; or cursor-driven UI demo | 1 beat per step |
| A trend or data claim | chart draws itself (lines left to right, bars in order, key bar accent last), labels on the data, no legend | 1.5-3 s + hold |
| A quote or punchline | kinetic type slam or masked word-by-word rise; one key word in the accent | 1.5-3 s |
| A named tool, site or tweet | real screenshot rebuilt as a card with a perspective entrance; social card (`x-post`, `reddit-post` registry items) | 2-4 s |
| A place | map fly-to with a route drawing on (Topographic Look) | 3-6 s |
| A section change | chapter card with the current's direction seam; or flood/contract transition | 1-1.5 s |
| "Look at this" in a screen recording | Screen-Studio style camera zoom to the area, cursor scaled with it | 0.5-1 s move |
| A list of many items | spinning list that slows and lands on one; or checklist with ticks drawing on | 2-3 s |
| Abstract idea | literal metaphor object or a real simulation (the study's best explainers simulate, they do not illustrate) | scene-length |

Registry first: before hand-building a named effect (grain, light leak, highlight marker, count-up, chart, lower-third, whip-pan), run `npx hyperframes catalog <words>` and `npx hyperframes add <name>`.

## 10. Explainer templates (from the prompt study)

- **T1 Problem to solution, 30 s:** problem 0-6 s (viewer's own pain), what we do 6-12 s (one sentence, one hero visual), how it works 12-22 s (3 steps), proof 22-26 s (one number rolling up), name/CTA 26-30 s held.
- **T2 Process build, 30 s:** start from an empty container, add one labelled component per beat, end on the finished object.
- **T3 Scale dive, 20-40 s:** one continuous shot, persistent scale ruler, each layer's duration proportional to log(zoom) so speed feels constant.
- **T4 Character-led science story, 60 s:** personify the subject, simulate the real process, real numbers with honest uncertainty, a parallel timeline for context, gags and callbacks, burned-in captions, music ducked under the voice.
- **T5 Timeline slam, 15-60 s:** years spring-slam in, a line drawing per event draws on, one-line thesis at the end. Momentum comes from the gap between slams, not from information density.
- **T6 User journey, 15-45 s:** each step's output becomes the next step's input (shared element), cursor-driven, 2-4 word noun stacks ("Agents · Sandboxes · MCP").
- **T7 Take-apart, 20-40 s:** whole object, explode or cut open, trace the flow, change one parameter, show the consequence.
- **T8 Talking-head / podcast inserts (long-form):** first pass marks every timestamp where a graphic could fill space or hook (35-50 per episode); write a style bible and component kit before building so every graphic looks like the same show; copy verbatim; each graphic inside one uncut audio stretch.
- **T9 Kinetic spoken-word / quote card:** phrase-based cue sheet from word timestamps, not a dance beat; at least one 400 ms stillness before the key line.

Pacing: explainer scenes 3-6 s; narrated pieces change something about every 1.5-2 s, synced to phrases.

## 11. Learning-science rules for explainers (Mayer, strong evidence)

- **Coherence (d about 0.86):** cut decorative visuals, music swells and SFX during dense explanation.
- **Signaling (d about 0.41):** highlight the essential part (accent colour, arrow, dim the rest to 40%).
- **Redundancy (d about 0.86):** do not put the narrated sentence on screen as a paragraph next to a diagram: keywords only (5 words or fewer). Captions remain fine for sound-off viewing.
- **Spatial contiguity:** labels on or next to what they name, not in a legend.
- **Temporal contiguity (d about 1.2):** the visual appears on the spoken word.
- **Segmenting:** chapters of 60-120 s with a visual reset.
- **Dual coding:** every abstract claim gets a concrete visual.

## 12. QA for graphics

1. `npx hyperframes lint .` and `npx hyperframes check .` with 0 findings.
2. `npx hyperframes snapshot . --at <one time per beat>` and look at every frame: clipped or overflowing text, overlaps, cramped type, contrast, anything that reads as a template.
3. Slop audit: at most 2 font families; exactly 1 accent; at most 1 bouncing element per scene; no emoji as icons; no full-frame gradient without grain; every graphic tied to a spoken word; every text inside the safe area.
4. After rendering, check decoded frames from the MP4, not browser screenshots. Look for single-frame pops (a frame differing about 3x more than its neighbours).
5. Judge each graphic once against brand consistency, interest and relevance; redo only the clearly bad ones. No endless redo loops (cap at 3 passes).
6. Fast motion with no motion blur strobes: for moves over about 2-3% of frame width per frame, render 4-8 subframes and average them, or keep the move slower.
7. **Safe zone (9:16):** `python3 scripts/safezone.py html <composition dir> --platform <zone>` must print PASS. It samples 10 times per second, so a 0.2 s slam overshoot is caught. Text that is meant to bleed (giant background word) gets `data-safe-ignore`.
8. **Read the render log**, not just the exit code: font fallback, missing asset and "timeline not found" messages appear there while the render still "succeeds".
9. **At least 3 distinct frames.** Extract frames at 25%, 50% and 75% of the render; if they are identical, the timeline never ran (registered late, wrong id, or a JS error) and the MP4 is a still.
10. **Determinism:** render twice and diff a few frames (`ffmpeg -i a.mp4 -i b.mp4 -lavfi psnr -f null -`); any difference means wall-clock time, randomness or a race crept in.
11. **Snapshots go stale.** After editing the HTML, re-run `snapshot` before judging; an old PNG in the folder proves nothing.

## 13. Conflicts between sources, resolved

- **"No dead holds over 1 s" vs "hold long enough to read":** a dead hold is a stretch where nothing new appears and there is nothing left to read. A read hold after a climax (the landed number, the final lockup) is required: `words x 0.3 s + 0.5 s`, typically 1.5-2.5 s, with everything still.

- **Idle "breathing" motion:** one Remotion skill says idle elements should breathe; HyperFrames' doctrine bans idle wobble. This skill follows the ban: a hold should either be still (readable) or advance the story. A subtle Ken Burns on a still photo (scale about 1.0 to 1.08 over the shot) is camera intent, not wobble, and is fine.
- **Italic emphasis:** HyperFrames caption rules ban italics for emphasis in motion; Sankhla's styles 2, 4, 5 use italic serif key words. Keep italic serif as a deliberate editorial style for single words held at least 0.6 s; never italicise running text.
- **Glass and glow:** glow stays banned by default (allowed when the user picks a Look that includes it, e.g. Look 1, 12, 18, on the hero only). Glass is conditional: allowed faint, bordered and behind type (never on the type itself), still banned as the default chrome of a whole video; the 2026 successor is a soft ambient mesh gradient.
- **Status pulses** (heartbeat dot, rotating dashed gear, staggered network nodes) are information, not idle wobble: allowed inside a finite timeline when they say "this is running now".
- **Safe zone numbers differ by source** (design research: y 250-1440; platform research: y 288-1248 on 1080x1920). Use the stricter 288-1248 for anything that must be read.


# ===== FILE: references/looks-library.md =====

# Looks library: 20 art directions for motion graphics

Source: "20 Looks for Claude Motion" (WeAreNoCode free community, skool.com/wearenocode). Reproduced here so the agent can paste a Look into a graphics brief. Every font named is a Google Font, so `scripts/fetch_fonts.py "Family:weights"` can download it.

## Why a Look block works

A plain prompt ("make a motion graphic about X") gets a basic, templated result. One paragraph that starts with `Look:` and reads like a brief to a designer fixes it, because it pins the decisions the model would otherwise default: background, palette with roles, display and body fonts, how numbers behave, how charts move, the easing personality, how scenes change, what the camera does, and what to avoid.

## The brief formula

Write every graphics brief in this order:

1. **Who you are** (the speaker / brand) and **who it is for**.
2. **The real numbers or words** (from the transcript or the user; never invented).
3. **Look:** one block from this file, with hex codes swapped to the brand.
4. **Format:** duration, resolution, fps, aspect, safe area.
5. **The next step** / end line.

When a HyperFrames workflow asks its quick style questions, answer "use the Look in the brief" and adjust in conversation afterwards.

Example (bookkeeper monthly report, Look 6):

> I'm a bookkeeper. Turn my client's September into a 30-second video for the owner of a plumbing company.
> Numbers: $86,400 came in, up 11% from August. $71,900 went out. Profit $14,500. Biggest jump: fuel, up 18%.
> Look: (Newsroom Data Desk block below)
> End on: "Next step: let's plan your Q4 taxes on our call."

## Matching a Look to a video

| Video type | Strong Looks | Caption style that pairs |
|---|---|---|
| Tech / SaaS / AI tools | 1 Tech Glassmorphic (use glass sparingly), 10 Bento Dashboard, 12 Retro Terminal, 20 Monochrome Keynote | 5 editorial, 10 minimal |
| Finance, business, data | 2 Swiss Grid, 6 Newsroom Data Desk, 10 Bento Dashboard, 14 Black and Gold Luxury | 7 documentary, 10 minimal |
| Education / explainers | 16 Whiteboard Sketch, 13 Paper Cut-Out, 8 Blueprint, 6 Newsroom | 3 pill, 8 karaoke |
| Real estate, local, maps | 3 3D Isometric Miniature, 15 Topographic Map | 1 clean-caps |
| Promo / offer / hype Shorts | 5 Neo-Brutalist, 9 Kinetic Type, 17 Memphis Playful | 6 viral, 1 clean-caps |
| Premium / personal brand | 4 Editorial Magazine, 14 Black and Gold, 20 Monochrome Keynote | 2 lower-serif, 5 editorial, 4 serif-italic |
| History / founder story | 19 Archival Documentary, 11 Risograph Zine | 7 documentary |
| Beauty / creator / fashion | 18 Y2K Chrome, 7 Soft Clay 3D | 4 serif-italic |

Honest caveat: some Looks (1 Glassmorphic, 18 Y2K Chrome, glows in 12) contain items on this skill's default ban list. They are allowed when the user picks that Look on purpose; keep the effect to the hero element, not everything.

## The 20 Looks

### 1. Tech Glassmorphic
Best for: a product walkthrough for a software tool, or an IT firm explaining a new service.

Look: Deep navy background (#0B1020) with two slow-drifting blurred glows, teal (#2DD4BF) and violet (#8B5CF6), behind frosted glass panels: 24px rounded corners, white at 8% opacity, background blur, a thin white edge. Text in white (#F8FAFC) and soft gray (#94A3B8). Headings in Sora SemiBold, large and tight. Body in Inter Regular. Numbers count up inside glass cards with a soft teal glow behind them. Charts are thin glowing lines and translucent bars that grow from the bottom. Panels float up into place with a gentle overshoot, then fade out. Scenes change with a focus pull: the old panels blur away as the new ones sharpen. Camera drifts slowly forward with parallax between layers. Avoid: neon overload, busy patterns, text on a glow with no panel behind it.

### 2. Swiss Grid
Best for: a quarterly results summary from an accounting firm or a consultant.

Look: Flat off-white background (#F4F1EA) on a strict 12-column grid with wide margins. No texture, no gradients. Black (#111111) for type, one signal red (#E63322) for the key number, light gray (#C8C4BB) for rules. Headings in Inter Tight Bold, very large, flush left, tight line spacing. Body in Inter Tight Regular, small. Graphic elements: thin horizontal rules, solid circles and rectangles, numbered section markers (01, 02, 03). Numbers sit huge and flush left, counting up in red. Bar charts are flat black bars on hairline axes. Motion is crisp and mechanical: elements slide in along the grid with a fast ease-out and stop dead. Scenes change with a hard horizontal wipe. Camera stays locked. Avoid: shadows, rounded corners, centered text, a second accent color.

### 3. 3D Isometric Miniature
Best for: a real estate market update, or a property manager's area report.

Look: A 3D isometric miniature world on a soft sky gradient (#FCE7C8 to #F9B98B), like a tabletop model at golden hour. Low-poly buildings and streets in warm cream (#FFF4E0), terracotta (#D9734E) and sage green (#8FB996), with long soft shadows and a light haze. Headings in Outfit SemiBold, body in Outfit Regular, on small floating white labels. Numbers appear as price tags or pins that pop up above buildings and count up smoothly. Charts are 3D blocks rising out of the ground like towers. Objects drop in from above with a soft bounce, one after another. Scenes change by gliding to another part of the same world. Camera holds the isometric angle, glides slowly and orbits a few degrees. Avoid: flat 2D icons, harsh black outlines, cold blue light.

### 4. Editorial Magazine
Best for: a financial advisor's market commentary, or a law firm's monthly client briefing.

Look: Warm paper background (#F5EFE6) with very faint grain, like a printed feature spread. Ink black (#1A1A1A), oxblood (#7A1F2B) for accents, gray-brown (#8A8178) for captions. Headlines in Instrument Serif, huge, with one word set in italic. Body in Libre Franklin Regular in narrow columns. Graphic elements: thin column rules, drop caps, pull quotes in large italic, small all-caps section labels with wide letter spacing, page numbers. Numbers look like a magazine stat: big serif figures with a short caption under them. Charts are thin ink lines with labels written right on them. Text reveals line by line through a soft upward mask, unhurried. Scenes change like turning a page, a slow horizontal slide. Camera makes slow pushes into the headline. Avoid: bright colors, icons, bouncy motion, sans-serif headlines.

### 5. Neo-Brutalist
Best for: a loud offer announcement for a gym, an agency or a trade business running a promo.

Look: Flat backgrounds that alternate between lemon yellow (#FFE24A) and white (#FFFFFF), no gradients. Every shape has a thick 4px black (#000000) border and a hard offset shadow, 8px down and right, zero blur. Accents in hot pink (#FF5CA8) and electric blue (#3B5BFF). Headings in Archivo Black, oversized, uppercase. Body in Space Grotesk Medium. Graphic elements: chunky rectangles, stickers, fat arrows, starbursts. Numbers sit in boxed tiles and snap to the final value with a quick shake. Bar charts are thick bordered blocks that slam up. Motion is fast and punchy: elements drop in with a hard snap, buttons press down into their shadow. Scenes change with a hard cut or a full-color block wipe. Camera is static. Avoid: soft shadows, thin fonts, slow fades.

### 6. Newsroom Data Desk
Best for: a bookkeeper's monthly client report, or an insurance broker explaining a rate change.

Look: A clean white background (#FFFFFF) with a pale gray panel behind each chart, like a data story on a news site. Text in near-black (#121212). One highlight color, deep blue (#1F5FBF), for this month, orange (#E8710A) for warnings, gray (#B5B5B5) for everything else. Headlines in Libre Franklin ExtraBold, sentence case, written as a one-line takeaway. Body in Source Serif 4. Labels sit right on the chart, no legends. Numbers tick up quickly and land with a short annotation line. Lines draw left to right, bars grow in order, and the key bar turns blue last. Motion is calm and quick, ease-out, no bounce. Scenes change with a fast fade through white. Camera stays still and zooms gently into the part that matters. Avoid: 3D charts, decoration, crowded pie charts.

### 7. Soft Clay 3D
Best for: a welcome video for new patients at a dental clinic, or new families at a tutoring service.

Look: Soft pastel background (#F3EEFF) under gentle studio light, no texture. Every object looks like smooth matte clay: rounded, puffy, with a soft inner highlight and a blurred contact shadow. Palette: lilac (#C9B6FF), peach (#FFC4A3), mint (#A8E6CF), with text in deep plum (#3B2A5C). Headings in Baloo 2 ExtraBold, round and friendly. Body in Nunito SemiBold. Graphic elements are chunky 3D icons, pill buttons and small rounded tiles. Numbers sit on clay badges and count up with a squishy pop. Bar charts are rounded clay pillars that grow with a soft wobble. Elements pop in with a springy squash and stretch, then settle. Scenes change as objects bounce out and new ones roll in. Camera slowly orbits a few degrees. Avoid: sharp corners, thin lines, dark backgrounds.

### 8. Blueprint
Best for: a contractor's project walkthrough, or a home inspector's report summary.

Look: Deep blueprint blue background (#0D3B66) with a fine white grid at 10% opacity and a faint paper texture. All lines in white (#FFFFFF) and pale blue (#A9D6F5), with safety yellow (#FFD23F) only for the thing that matters. Headings in Barlow Condensed SemiBold, uppercase, widely spaced. Notes in Architects Daughter, like hand-lettered annotations. Graphic elements: technical line drawings, dimension lines with arrows, callout circles, a title block in the corner with a drawing number. Numbers appear as measurements on dimension lines and count up. Charts are plotted as lines on the grid. Everything draws itself on, stroke by stroke, at a steady drafting pace. Scenes change by zooming into a detail callout that becomes the next drawing. Camera pans slowly across the sheet. Avoid: filled shapes, gradients, cute icons.

### 9. Kinetic Type
Best for: a 30-second promo for a new service, or the opening of a sales presentation.

Look: The words are the animation. Solid backgrounds flip between jet black (#0A0A0A) and signal yellow (#FFD400), with white (#FFFFFF) type. Headings in Anton, uppercase, filling the frame edge to edge. Supporting lines in Barlow Medium, small. No icons, no illustration. Words slam in one at a time on the beat, stretch and stack. Key numbers fill the screen and count up fast. Charts are made of type: a bar is a word stretched to length. Motion is fast with hard eases, 2 to 4 words per second, a short hold on the punchline. Scenes change with a wipe that reveals the next scene through the letters. Camera makes quick punch-ins and small rotations. Avoid: more than 6 words on screen, soft fades, thin weights.

### 10. Bento Dashboard
Best for: a marketing agency's monthly results, or a property manager's update for owners.

Look: Light cool gray background (#F2F4F7) with rounded tiles (20px corners) in different sizes. Tiles in white (#FFFFFF) with a very soft shadow, one hero tile in deep ink (#101828) with white text. Emerald (#12B76A) for good news, coral (#F04438) for bad news. Headings in Geist SemiBold, numbers in Geist Mono. Each tile holds one idea: a big number, a sparkline, a progress ring or a short bar list. Numbers roll up like an odometer. Sparklines draw left to right, rings fill clockwise. Tiles arrive one by one with a short stagger, scaling up from 96%. Scenes change when one tile grows to fill the screen and becomes the next scene. Camera is flat and still. Avoid: more than 8 tiles, 3D, heavy shadows.

### 11. Risograph Zine
Best for: an event recap for a cafe, a local shop or a community workshop.

Look: Off-white uncoated paper (#F7F3EA) with visible grain, like a two-color print. Inks: fluorescent pink (#FF48B0) and teal (#0078BF), with yellow (#FFE800) where they overlap. Ink layers sit a few pixels off, with rough edges. Headings in Bricolage Grotesque ExtraBold, chunky and a little uneven. Body in Courier Prime. Graphic elements: halftone dot fills, cut-out shapes, stars, rubber-stamp marks. Numbers are big, printed in pink over a teal halftone, and step up in visible jumps. Bar charts are halftone blocks. Motion runs at 12 frames per second for a handmade feel: things pop, jitter slightly and stamp into place. Scenes change by sliding a new sheet of paper over the old one. Camera is a flat overhead view. Avoid: smooth gradients, gloss, perfect vector edges.

### 12. Retro Terminal
Best for: an IT provider's monthly report, or a security check-up for a small business.

Look: A black CRT screen (#050805) with faint scanlines, a soft green glow, slight screen curve and a gentle flicker. Text in phosphor green (#33FF66), dim green (#1A7A33) for secondary lines, amber (#FFB000) only for warnings. Headings in VT323, large. Body in IBM Plex Mono. Graphic elements: a blinking block cursor, command prompts, boxes and progress bars drawn with text characters. Text types on character by character at a fast, steady pace, and some lines print all at once. Numbers count up like a loading counter. Charts are text-character bar charts that fill block by block. Scenes change with a screen clear: a quick flash, a scanline sweep, then a fresh prompt. Camera stays locked with a slow push-in. Avoid: any color besides green and amber, rounded cards, bouncy easing.

### 13. Paper Cut-Out
Best for: a how-it-works explainer for an accountant's new service, or a nonprofit's year in review.

Look: Layered paper craft, built from stacked sheets of colored card with real depth. Each layer casts a soft shadow on the one below, with rough edges and a fine paper fiber texture. Palette: warm cream (#FAF3E3), forest green (#2F5D50), mustard (#E0A526), brick red (#B5462E), ink navy (#1F2A44) for text. Headings in Fraunces SemiBold, soft and slightly quirky. Body in Work Sans. Graphic elements: cut-paper hills, suns, buildings, folded corners. Numbers are printed on paper tags that flip up and count. Charts are stacked paper strips that slide up. Layers slide in from the sides with a soft ease, and pop-up pieces fold upward, like a hand-built set. Scenes change as a new paper layer slides across. Camera moves sideways with parallax. Avoid: gloss, neon, thin lines.

### 14. Black and Gold Luxury
Best for: a listing presentation for a high-end home, or a private wealth review.

Look: Deep black background (#0A0A0A) with a subtle warm vignette and very fine noise. Gold (#C9A55C) for lines, numbers and accents, with a soft metallic sheen sweeping across them. Warm ivory (#F2EBDD) for text, charcoal (#1E1E1E) for panels. Headings in Cormorant Garamond Light, large, with generous letter spacing. Small labels in Montserrat, uppercase, widely spaced. Graphic elements: hairline gold frames, thin dividers, a monogram-style emblem, plenty of empty space. Numbers fade in and count up slowly, then a light glint passes across them. Charts are thin gold lines with small dot markers. Motion is slow and deliberate, long ease-in-out, nothing bounces. Scenes change with a slow fade through black. Camera makes slow pushes in. Avoid: bright colors, fast cuts, heavy bold fonts, crowded layouts.

### 15. Topographic Map
Best for: a neighborhood report for an agent, or a territory update for an insurance broker or a delivery business.

Look: Off-white map paper (#EFEBE0) with light brown contour lines (#C9B79C) across the frame. Water in muted blue (#9CC3D5), parks in sage (#B7C9A8), roads in white with thin gray edges, and one route or zone color, vermilion (#E2522B). Headings in Josefin Sans SemiBold, uppercase and widely spaced like map labels. Place names in Lora Italic. Graphic elements: pins, dashed routes, a compass rose, a scale bar. Numbers sit in callout pins that drop onto the map and count up. Charts are zones that fill with color by value, like a heat map. Routes draw themselves along the roads. Scenes change by flying to a new part of the map. Camera pans and zooms smoothly across one big map. Avoid: satellite imagery, 3D buildings, app-style cards.

### 16. Whiteboard Sketch
Best for: walking new clients through a process, like how a claim works or the steps of buying a home.

Look: A clean whiteboard (#FAFAF7) with faint smudges near the edges. Marker colors: black (#1B1B1B) for most lines, blue (#1E5AA8) for labels, red (#D7263D) for circles and emphasis, green (#2E8B57) for good outcomes. Headings in Caveat Bold, body in Patrick Hand, both like quick handwriting. Graphic elements: hand-drawn boxes, wobbly arrows, plain icons (houses, coins, documents, clocks), underlines, check marks. Lines have a slight hand wobble. Numbers are written stroke by stroke, then circled in red. Charts are sketched bar charts with hatching. Everything draws itself on at writing speed, as if a marker is moving live. Scenes change with a quick eraser swipe, or by sliding to an empty part of the board. Camera is flat, with small zooms. Avoid: perfect geometric shapes, solid fills, drawn people.

### 17. Memphis Playful
Best for: a fun promo for a party rental business, a bakery's new menu or a salon's referral offer.

Look: Bright cream background (#FFF6E5) scattered with geometric patterns: squiggles, zigzags, confetti dots, triangles, half circles and small grid patches. Palette: hot coral (#FF6B6B), turquoise (#2EC4B6), sunflower (#FFC93C), and black (#1A1A1A) for outlines and text. Headings in Bungee, blocky and loud. Body in Rubik Medium. Shapes have thin black outlines, and some carry black dot or stripe patterns. Numbers sit inside bold shapes and pop up with a spin. Charts are colorful blocks and pie wedges with patterned fills. Motion is playful and springy: shapes spin in, bounce, wiggle once and settle, while the background patterns float slowly. Scenes change with a burst of shapes flying across the screen and clearing it. Camera is flat with small playful zooms. Avoid: muted colors, serif fonts, realistic shadows, cartoon characters.

### 18. Y2K Chrome
Best for: a launch teaser for a beauty brand, a boutique or a service for creators.

Look: Pale icy background (#EEF0FF) with a faint lilac haze and soft bokeh sparkles. Hero elements are glossy liquid chrome: silver (#C0C7D1) with bright white highlights and iridescent edges shifting between baby blue (#9AD0FF) and lilac (#D7B8FF). Deep navy (#0E1A3A) for text. Headings in Unbounded Bold, wide and bubbly. Body in Space Mono, small. Graphic elements: chrome blobs, star sparkles, glossy pill buttons, translucent plastic panels. Numbers are rendered in chrome and count up with a shine sweep. Charts are glossy rounded bars with reflective tops. Elements float in with a gentle bob and turn in 3D to catch the light. Scenes change with a liquid chrome morph or a sparkle flash. Camera drifts and tilts slightly. Avoid: flat matte colors, gritty textures, serif fonts.

### 19. Archival Documentary
Best for: a company history for an anniversary, or the founding story of a family business.

Look: A dark wooden desk (#2B2420) covered in aged paper. Paper in yellowed cream (#E8DCC2), ink in sepia brown (#4A3728), stamps in faded red (#9E2A2B), accents in tarnished brass (#A68A4D). Headings in Libre Baskerville Bold. Body and dates in Special Elite, like a typewriter. Graphic elements: typed index cards, file folders, stamps that thump down, a timeline drawn as a thread between pinned cards, and empty photo frames (to be filled with the user's photos). Numbers are typed on, then stamped. Charts look hand-ruled in ink on graph paper. Motion is slow: pages slide onto the desk, dust drifts, the light flickers softly. Scenes change by sliding to the next document. Camera makes slow pans and pushes across the desk. Avoid: bright colors, clean digital UI, fast motion.

### 20. Monochrome Keynote
Best for: a pitch to a big client, a board update, or the one number that matters in an annual review.

Look: A pure black stage (#000000) with nothing on it but the words. White (#FFFFFF) for type, mid gray (#8E8E93) for secondary lines, and one accent, electric blue (#2F80FF), for the key word or number. Headings in Manrope ExtraBold, very large and centered. Body in Manrope Regular. One idea per scene, never more than 8 words. No icons, no decoration. Numbers appear huge in the center, count up slowly, then hold. Charts are one thin line or one bar. Motion is calm: text fades up from 20px below with a long, smooth ease-out, then a full second of stillness before the next idea. Scenes change with a slow fade through black. Camera holds still, with a rare slow push-in. Avoid: clutter, bullet lists, a second accent color.

## Writing a new Look (for a brand or a measured creator)

Fill every slot; leaving one blank lets the model fall back to its defaults:

```
Look: <background colour + texture, hex> <what world it feels like>. Text in <hex> and <hex>.
One accent <hex> for <what it marks>; <hex> for <secondary role>. Headings in <Font Weight>,
<case, size, tracking>. Body in <Font Weight>. Graphic elements: <3-5 concrete elements>.
Numbers <how they appear and land>. Charts <how they draw>. Motion is <personality, ease, overshoot
budget>. Scenes change with <one transition>. Camera <locked / slow push / pans>. Avoid: <3-5 bans>.
```

For a measured creator, pull the hex codes from `measurements.json` (`palette_time_weighted`), the fonts from the frames you looked at, and the motion personality from cut rate and how their graphics enter.


# ===== FILE: references/captions.md =====

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

- "Size" here always means the font size (the em, what `size_pct` and ASS `Fontsize` set), not the cap height. Capitals are about 0.7 em tall in most grotesques (a 92 px caption has roughly 65 px capitals), but condensed display faces differ: Anton capitals are about 0.5 em. When matching a reference, calibrate by the measured width of a line of text, not by eye on letter height.
- The fonts must actually load. libass substitutes a system font silently when a family or weight is missing, and the result looks almost right but wider or narrower. `captions.py` prints a WARN when the style's font files are missing from `--fonts`; fetch them with `fetch_fonts.py`. Weights other than 400/700 are requested by legacy names ("Montserrat Black"), which the script handles.
- Body captions: font size about 4.5-5% of frame height (48-55 px at 1080p landscape; 86-96 px at 1080x1920). Hook/punch size: 6-9%. Never below 2.6% (28 px at 1080) for anything that must be read.
- 16:9: centred low (script default y = 0.86), but keep the bottom ~12% free of critical text on YouTube (progress bar, auto-captions).
- **Pass `--platform` on every vertical caption run** (`reels`, `reels-ad`, `tiktok`, `shorts`, `cross`; default `cross`). It sets the line width from that platform's safe box and rail, and the script WARNs when a group overflows it. `cross` is narrow (about 480 px at caption height, because of the TikTok rail), so captions split into more, shorter groups; for an Instagram-only reel use `--platform reels` (box 35-1045 x 220-1500, rail x > 950 below y 1340, the user's reference in `assets/safe-zones/`). Full table: `platforms-and-styles.md` PART B.
- `--hook-until S` hides captions for the first S seconds while a hook title or graphic is on screen, so the two never stack.
- 9:16: centred around y = 0.60 (1150 px of 1920). Cross-platform safe box for anything that must be read: x 120-888, y 288-1248. Below 1248 the TikTok/Reels/Shorts description and buttons cover it; the right rail (x > 780 from y 840 down) holds like/comment/share. Platforms publish no official organic pixel specs, so these are measured values that change: re-check templates for ads.
- Faces: captions never cover the eyes or mouth. Speaker's eyes around 30-40% from the top in 9:16 so captions sit below the chin. If a frame shows overlap, move the captions (`--y`) for that video rather than shrinking them.
- Hook text (first 1-3 s of a Short): upper middle, y about 300-600. Never two text blocks competing: while a hook title or a graphic with words is on screen, either hide the captions for those seconds or keep the two clearly separated (title top, captions low), never stacked at the same height.
- Face fills the frame (tight vertical close-up): there is no room below the chin, so put captions in the upper third (y about 0.25-0.30) or on the chest only if the mouth stays clear. Check a frame; the default y is a starting point, not a rule.

- **Double captions.** Burned captions plus the platform's auto-captions show the same words twice. When burning, tell the user to switch platform auto-captions off for that post, or upload the SRT instead of burning (never both).
- Dashes in the transcript become spaces (never a literal dash glyph mid-caption); common abbreviations (Dr., U.S., e.g.) are protected from sentence splitting.

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


# ===== FILE: references/editing-grammar.md =====

# Editing grammar: cuts, pacing, retention, zooms, B-roll, sound

Contents: 1 Hard rules for the rough cut · 2 Where to cut · 3 Pacing by format · 4 Retention structure · 5 Punch-ins and camera moves · 6 B-roll · 7 Sound · 8 Shorts from long-form · 9 Recording advice to give the user · 10 Pacing design (gears, arc, tempo) · 11 The first seconds · 12 Thumbnail-to-video handoff · 13 B-roll timing and cutaways · 14 Working habits

Evidence labels follow `design-science.md`: [STRONG] research, [INDUSTRY] platform data, [FOLK] craft practice.

## 1. Hard rules for the rough cut

Distilled from browser-use/video-use, WeAreNoCode, chrislema/videoeditor and hassancs91 (all public skills), plus this skill's tests:

1. Never cut inside a word. Pad cuts: about 50 ms before the first word and 80-150 ms after the last (plan_cuts.py styles: tight / natural / loose).
2. Cut in silence. Boundaries snap into detected silence when one is within about 120 ms.
3. Keep the last take. When a speaker restarts a line, the later version is almost always the one they meant.
4. Short fades (about 20 ms) at every audio boundary, so cuts never click.
5. Render audio in one pass. Joining separately encoded AAC pieces adds a few ms per join; over hundreds of cuts it becomes visible lip-sync drift (render_cut.py already does this).
6. Snap boundaries to the frame grid so picture and sound stay the same length (render_cut.py and plan_cuts.py do this).
7. Caption times come from the EDITED timeline (`words_cut.json`), never the raw transcript.
8. Graphics are composited before captions; captions go on top, last.
9. Use a verbatim transcript (fillers kept) for planning; Whisper silently drops "um" unless primed (`transcribe.py --verbatim`).
10. Verify by ear-proxy: `verify_cut.py` transcribes the render and diffs it against the kept words (catches clipped or ghost syllables and drift).
11. Confirm the cut list with the user before rendering; confirm the visuals plan before building graphics.
12. Cap self-review loops at 3 passes; then ask the user.

## 2. Where to cut

- **Murch's Rule of Six** [FOLK, near-universal]: when choosing a cut, emotion (51%) beats story (23%) beats rhythm (10%) beats eye-trace (7%) beats screen direction (5%) beats 3D continuity (4%). Sacrifice from the bottom.
- **Cut at the end of a thought.** Viewers' blinks cluster at points where a thought completes [MODERATE, Nakano 2009]; a cut there feels invisible.
- **Eye-trace:** across a cut, keep the subject of interest within about 10-20% of frame width of where the eye already was. Break it only on purpose (a pattern interrupt).
- **Cut on action:** cut during movement and continue it in the next shot; motion hides the cut [MODERATE, edit-blindness research].
- **J-cut:** the next clip's audio starts 0.25-1 s before its picture (leads into a new speaker or scene). **L-cut:** the previous audio continues over the new picture (B-roll under the voice). Use on at least half of the scene transitions in interview and documentary edits.
  Honest limit: `render_cut.py` cuts audio and picture together. Build a J/L cut by laying B-roll or a
  cutaway over the join with `overlay.py` (the voice carries across, the picture changes early or late); true
  split edits of the A-roll need an NLE.
- **Jump cuts in a talking head:** remove pauses over about 300-500 ms and filler; keep 2-6 frames of breath at phrase edges; alternate framing (punch-in) on every 2nd or 3rd cut to hide the jump.
- **Smash cut:** a sudden loudness change (loud to silence or the reverse) sells it.
- **Vary shot lengths.** Film shot lengths cluster in mixed runs of short and long (Cutting 2010, [STRONG] for the trend). A metronome rhythm reads as machine-made: cluster fast cuts in high-energy passages, let shots breathe after reveals.

## 3. Pacing by format

| Format | Visual change every | Notes |
|---|---|---|
| Shorts / Reels / TikTok | 1.5-3 s | cut, punch-in, graphic or caption emphasis all count |
| YouTube talking head | 3-8 s | B-roll and cards on the words that need them |
| Documentary / essay | 4-12 s | slower, music and silence do more work |
| Tutorial / screen recording | when the information changes | zoom to the area of interest, do not add cuts for their own sake |

**"Pattern interrupt every N seconds" is folklore** [FOLK]. What is established [STRONG]: cuts and new graphics trigger an automatic orienting response; but too many changes, or changes unrelated to the content, overload viewers and reduce memory for the message (Lang's limited-capacity model). So every interrupt must relate to what is being said, and the cut rate should drop during dense explanations and rise during low-information stretches.

Measured creator pacing (more in `platforms-and-styles.md`): MrBeast went from about 38 to about 23 cuts per minute (2022 to 2024 samples); Hormozi-style shorts cut every 1-3 s; MKBHD about 8-15 cuts per minute; Dan Koe 4-12.

## 4. Retention structure

YouTube defines the Intro metric as the share of viewers still watching at 0:30 and tells creators to make the first 30 s match the title and thumbnail [INDUSTRY, official].

**Shorts:** no intro. The hook line plus on-screen hook text in frame 1 (the first frame also works as the thumbnail). Captions from frame 1 inside the safe box. Something new every 1.5-3 s. A loop-friendly last line that flows into the first. Usually 20-45 s unless the story needs more.

**Long-form:**
1. Cold open, 15-45 s: restate the title/thumbnail promise and show the proof visual. No logo sting over about 3 s, no "hey guys, welcome back".
2. Open a specific loop (a question you will answer). Curiosity comes from a specific gap, not a vague one [STRONG, Loewenstein]. Pay it off; unresolved loops damage trust.
3. Re-engagements around 1:00, 3:00, 6:00 and every 2-3 min after (adapted from the MrBeast production memo [practitioner evidence]).
4. Pay off the thumbnail promise early enough that viewers do not feel tricked; hold the biggest payoff for the end without signalling "the end".
5. End screen in the last 5-20 s with content still playing; point to one specific next video with a reason. Never "that's it for today" before the end screen.
6. Chapters: first timestamp 00:00, at least 3 chapters, each at least 10 s.

The "8-second attention span" is a myth [MYTH]; do not use it to justify frantic pacing.

## 5. Punch-ins and camera moves

Zoom taste from Tella's open-source add-zooms skill and WeAreNoCode:

| Move | Values | Use |
|---|---|---|
| **Punch** | hard cut to 1.18-1.30x, hold 0.2-0.5 s (or until the next cut), hard cut out | emphasis words, punchlines |
| **Ratchet** | each list item steps up: 1.12, 1.20, 1.28 | "first... second... third" |
| **Ken Burns** | slow, at most 1.14x over the shot, the only smooth move | stills, long holds |
| **Alternate framing** | every 2nd or 3rd jump cut at 1.08-1.15x | hides jump cuts (`render_cut.py --punch`) |

- Focal point about (0.5, 0.42): slightly above centre, on the face.
- 1080p sources go soft past about 112-130%; 4K sources can go to about 150% for 1080p delivery. Tell users to record in 4K if they want aggressive zooms.
- Do not punch in during a graphic; do not combine a punch with a camera move.
- Zooms compound. A 9:16 crop of a 16:9 source is already a ~3.2x enlargement of the face area relative to the frame, so a 1.08 punch on top of `reframe.py` output is effectively a much tighter shot and softer. On vertical reframes keep punches at 1.05-1.08, or none.
- One cut or two? If a removed stretch is under about 1.5 s and the framing is the same, one jump cut with a punch hides it. If two cuts would land less than about 1 s apart, merge them into one cut (cut out the whole stretch) rather than leaving a flash of a fragment.
- Text is unreadable while it moves faster than about 10-15% of the frame width per second: animate in, then hold still.

## 6. B-roll

Classify every B-roll beat first (from Tella's b-roll-finder method):

| Type | What | Source |
|---|---|---|
| **Receipts** | proof: a tweet, headline, screenshot, chart, document | screenshot the real thing (with permission), rebuild as a card |
| **Entity** | a specific person, product, place, company | official footage or photos, the user's own footage |
| **Concept** | an idea with no footage | a motion graphic (motion-graphics.md) |
| **Meme / reaction** | a cultural reference | the user supplies it (rights) |

Rules: source the meaning, not the keyword (a line about "growth" does not need a stock shot of a plant); strip B-roll audio when it is noisy or contaminated (`-an`), but keep clean literal sound (room tone, the object's own sound) under it, because diegetic sound sells reality (see 13); a slow Ken Burns of about 1.5% per second on stills; never generic stock filler (handshakes, glowing brains, server rooms), which viewers recognise and which violates the coherence principle. Free sources with licences: `tooling-research.md` section 8 (Pexels, Pixabay, Coverr, Mixkit; keep licence notes in `EDIT_STATE.md`).

## 7. Sound

Full craft (sourcing choice, duck numbers, SFX variation, music stops, Closed Eye Test): `sound-design.md`.

- **Loudness:** -14 LUFS integrated, -1 dBTP max for YouTube and social. Platforms only turn loud uploads down; mastering hotter costs dynamics for nothing.
- **Voice chain** (free, no ML): `highpass=f=80, afftdn, deesser, acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2` then normalise once at the end (`finish.py --denoise` applies a light version). DeepFilterNet for heavier noise: 48 kHz WAV only, and use `-D` (compensate delay) or sync shifts.
- **Music under voice:** 12-18 LU below the voice while someone speaks (research: at least 10 LU for commentary over music, and non-experts want about 4 LU more than experts [MODERATE, Torcoli 2019]). Use the deeper end for explainers. Let it rise to 4-8 LU under the voice in pauses. Ducking attack 50-150 ms, release 300-800 ms. No vocals under speech. EQ-carve 2-4 dB around 1-4 kHz in the music if the voice still fights it.
- **SFX:** only where something visibly changes. Whoosh peak on the cut frame (tail starts 4-10 frames before), pop on the first visible frame of an element, ticks during a counter and a "ding" when it stops, riser 1-4 s before a hit. Levels: whoosh -6 to -12 dB under voice peak, pops -12 to -20 dB. Explainers at most about one SFX per second; nothing on top of key words. Place SFX by their measured peak, not by the file start.
- **Silence:** cut music to silence (or room tone) for 0.5-1.5 s before a reveal or punchline; the next sound lands harder.
- **Music pacing:** frames per beat = fps x 60 / BPM (30 fps at 120 BPM = 15 frames). Energetic Shorts 110-140 BPM, explainer beds 80-110, documentary 60-90. Big changes on downbeats; chapter changes on musical phrase changes (every 4 or 8 bars). `npx hyperframes beats` writes beat times.
- **Rights:** YouTube Audio Library tracks are not Content-ID claimed; Pixabay and others can be fingerprinted, keep licence certificates. A Short over 60 s with a Content ID claim gets blocked.

## 8. Shorts from long-form

1. Find candidate moments in the transcript: a complete thought with a hook in its first sentence, 20-60 s, no dependence on earlier context.
2. Cut with `plan_cuts.py --style tight --head <start> --tail <end>`.
3. Reframe: `reframe.py in.mp4 out.mp4 --aspect 9:16` (face-centred static crop per section; `--mode blurfit` for slides or two people).
4. Captions style 6 or 1 at y about 0.60; hook text in the top third for the first 1-3 s.
5. Loop the ending into the opening when the content allows.

## 9. Recording advice to give the user (makes every edit better)

- Record in 4K if possible: zooms stay sharp (1080p goes soft past about 112%).
- Flubbed a line? Pause, then say the whole line again. The editor keeps the last take.
- Keep the recording flat: no zooms, captions or transitions baked in.
- Eyes on the lens; the face lit as the brightest large area in frame.
- Record room tone (5 s of silence) at the start: it hides cuts and gaps.
- Constant frame rate (phones often record variable frame rate: `probe.py` warns).

## 10. Pacing design (gears, arc, tempo)

- **Gears map emotion to cutting speed.** Gear 1 reflective/intimate, 2 observational, 3 progression, 4
  tension, 5 chaos/urgency. Start from the scene's emotional destination, then pick the gear; never start
  from "how fast should I cut". Source: Inside The Edit, youtube.com/watch?v=bCVeyUFGxi8, 02:37-04:10.
- **Design the pacing arc across the whole film.** Pacing problems live between scenes: editors polish scenes
  while the film dies in the transitions. Before fine-cutting, list the scenes in order with a gear each and
  read the sequence. Source: same, 00:18-00:25 and 05:01-05:33.
- **Two tempo rules.** Never repeat the same pattern (slow-medium-fast loops are predictable), and never put
  two same-tempo scenes back to back. Alternate: slow -> fast -> medium -> slow. Source: same, 16:44-17:45.
- **Long-form opening:** one continuous take of about 5-23 s before the first real cut, then accelerate. The
  uncut open earns trust; the acceleration earns retention. [directional, small sample]
- **Pacing factors add up:** cut speed + movement inside the shot + subject distance + camera movement. Cuts
  plus whip-pans on close-ups feel far faster than cuts alone; a fast subject in a wide shot reads slower than
  small head movements in an extreme close-up. Source: Inside The Edit, youtube.com/watch?v=CdyTIng0M8Q,
  09:13-11:39.
- **Question-driven cutting.** Every section (about every 60 s), ask what question is in the viewer's head now;
  delay the answer or withhold just enough. Ask what the viewer should feel next, and how the cut is motivated.
  Unfinished threads are remembered better than finished ones (Zeigarnik effect); close them at the end.
  Source: Dylan Reynolds, youtube.com/watch?v=O0qkkexHqZw, 04:37-05:19.
- **Cognitive load:** extraneous load to zero (messy frames, confusing edits, fancy transitions), but keep a
  little germane load: if everything is explained, the viewer does no work and drifts. Source: Abhay PS
  Rajawat, youtube.com/watch?v=SWAYLiH7p5M, 01:54-03:41.
- **A small gap before the important line** mimics how people hesitate before saying something that matters;
  leave (or create) about a beat of air there instead of cutting it out. Source: same, 01:37-01:51.
- **Pattern breaks need an established pattern.** Build a normal rhythm first, then break it (sudden zoom,
  full-frame change, meme). A break without a pattern just breaks flow. Rotate break types (visual, audio,
  camera), never the same twice in a row. The widely quoted "23% retention lift" figure is fake precision;
  ignore it. Source: same, 07:42-08:53.

## 11. The first seconds

- **Zero head padding:** first visible motion within 0.00-0.13 s (measured on 5 videos). No fade-in, no logo,
  no "hey guys".
- **Frame 1 composition:** long-form opens on the subject mid-gesture or mid-expression, never on black or a
  title card. Shorts may open on big text (frame 1 is also the thumbnail there).
- **The 0-3-8 s ladder:** 0 s visual hook, 3 s the promise (what this video delivers), 8 s the first payoff or
  escalation. A missing rung is a diagnosed failure. Check it in QA.
- **Polarity check:** does the hook take a stance (works/fails, love/hate)? Neutral summaries are the most
  common weak hook. A diagnostic question, not a law.
- **Hook killers:** no person in frame 1 for personality content, bio-first openings ("I'm X, I do Y"),
  Zoom-call framing.
- **The first 5 s read like the thumbnail:** big, legible, high contrast, one idea (MrBeast production memo).
- 2026 distribution leans on satisfaction signals (shares, saves, rewatches, fewer "not interested") more
  than raw watch time; design one shareable beat and one save-worthy frame. [PRACTITIONER consensus]

## 12. Thumbnail-to-video handoff

- **Confirm the click within 15 s** (measured ceiling about 60 s). Measure it with a stopwatch: seconds from
  start to the first on-screen moment that delivers the thumbnail/title promise. A stricter practitioner rule
  (visual confirmation in 5-6 s, verbal by 30 s) also circulates; both are kept.
- **Restate, then extend:** confirm the promise, then add something the thumbnail did not contain.
- **Never open by repeating the thumbnail text or reading the title aloud** (0 of 6 measured videos did; the
  viewer already read it). Confirm the meaning, not the exact frame (2 of 6 confirmed the promise without
  replicating the thumbnail frame). Small samples: direction, not law.
- **Mute test:** watch the first 15 s muted; the promise must be visually confirmable.
- **Pace test:** the open must match or exceed the thumbnail's energy.
- **Keep one brand constant** (colour, mark, type treatment) from thumbnail into the video.
- **Four failure modes:** bait-and-switch, slow confirmation, thumbnail-text continuation, register mismatch.
  A retention cliff at 0:30 means the handoff failed: fix the open AND check the packaging's promise.
- 40-50% of viewers gone by 0:30 is the common baseline being designed against [practitioner figure].
- YouTube Test & Compare picks thumbnails by watch-time share, not click-through: a thumbnail that wins clicks
  but loses the handoff loses the test.
- Shorts are a separate system: the first frame is the thumbnail, so confirmation is immediate or the swipe
  already happened.

## 13. B-roll timing and cutaways

- **Holds:** short-form 1.2-2 s per B-roll shot; long-form 3-6 s, rarely past about 10 s without a camera move
  or annotation; charts and diagrams hold as long as the voice needs.
- **Adjacent contrast:** never cut two similar shots together (wide after tight, bright after dark, motion
  after still).
- **L-cut by default** (audio leads picture); cut on phrase boundaries, never mid-word.
- **Cut on the illustratable fact:** the picture lands on the fact it proves (documentary practice).
- **Match cuts and audio bridges:** match on shape, motion or colour; lay the next scene's audio under the
  last ~0.5 s of the current one to pull the viewer through. Keep motion direction continuous across cuts.
- **Pass-by transitions:** a foreground object wiping past camera is the transition; continuous ambience
  sells it.
- **Two sound layers on every B-roll shot:** its literal sound plus one designed layer; an ambience bed glues
  them.
- **Reaction cutaways:** the effect on others gives a line its power. Hold the speaker, cut to the listener's
  reaction, cut back; in a podcast with 2+ guests, cut to the other guest's face during a strong line.
  Source: Dylan Reynolds (O0qkkexHqZw) 02:02-03:37.
- **Stock first, AI second:** real footage first; AI fills only what stock cannot (see `visual-sourcing.md`).
- Tell users who shoot: 10 s per B-roll setup (3 s pre-roll, the action, 3 s post-roll).

## 14. Working habits

- **Re-listen to the transcript before cutting.** The timing grid is only as good as `words.json`: fix
  misheard names and words first.
- **Cut what does not serve the story.** The brief's story beats decide inclusion, not the fact that footage
  exists (anti-feature-dump).
- **Long-form narrative build order:** dialogue scrub (e.g. 20 min to 3 min, gentle), then a ruthless second
  pass, label each chunk by theme, build the dialogue skeleton in story order, then add music, score, field
  recordings and SFX with zero visuals, and only then lay picture on top. Source: Max McCoy,
  youtube.com/watch?v=XUWjBQiT1Iw, 01:08-08:54.
- **Keep every destructive pass reversible:** a new EDL / new render version each time (`edl_v2.json`,
  `renders/v2...`), never overwrite the previous one. Reversibility is what makes ruthless cutting safe.


# ===== FILE: references/sound-design.md =====

# Sound design

Sound carries more of an edit than picture does. Two tests decide whether the sound works: the **Closed Eye
Test** (below) and listening on a phone speaker. Numbers marked [PRACTITIONER] are the consensus of working
editors, not lab measurements; [UNVERIFIED] means reported but not confirmed.

## Contents
1. Where music and SFX come from (ask every project)
2. The mix: levels, ducking, de-essing
3. SFX craft
4. Music structure
5. Texture beds
6. Code-native scoring
7. QA: the Closed Eye Test

## 1. Where music and SFX come from (ask every project)

The user has a paid **Epidemic Sound** plan. Every project, ask which source to use; never assume:

- **Epidemic Sound**: the user downloads the tracks/SFX (or gives the files); keep the licence crediting the
  plan requires, and note track IDs in `EDIT_STATE.md`. Channel/whitelisting is the user's account setting.
  The licence covers videos published **while the subscription is active**: if the plan lapses, earlier
  videos stay cleared, new uploads do not. Confirm it is active on the publish date.
- **Free, copyright-safe**: YouTube Audio Library (check each track's attribution requirement), Pixabay Music
  and SFX, Mixkit, Freesound (CC0 or CC-BY only; CC-BY needs credit). Write the source URL and licence of
  every file into `EDIT_STATE.md`.
- Never use commercial music the user has no licence for, "no copyright" compilations from YouTube, or
  tracks ripped from other videos. YouTube Content ID claims or mutes them, and Instagram can mute or block the audio.
- A persistent sound library across projects lives in `assets/style-lab.md` (tagged by role: riser, impact,
  whoosh, pop, bed; rated Keep / Maybe / Drop), so the next video starts from proven sounds.

## 2. The mix: levels, ducking, de-essing

- Delivery loudness: -14 LUFS integrated, -1 dBTP (`finish.py`). Mastering hotter buys nothing.
- **Music bed under voice: 16-25 dB below the voice.** Auto-duckers (Premiere, CapCut) pin at about -16 to
  -20 dB of bed depth; the extra 3-5 dB of sidechain gain reduction is the icing applied after that, not the
  cake. `finish.py --music-sep 20 --duck` does both stages. [PRACTITIONER]
- **The bed level is relative to the measured voice**, not an absolute number: `--music-sep 20` measures the
  voice LUFS and the music LUFS and sets the bed 20 LU under the voice, so a quiet track and a slammed track
  land at the same place. `--music-db` is the old absolute gain, kept only as an override.
- **Voice chain:** `--voice-chain light` (high-pass 80 Hz only, default) or `full` (high-pass, 3:1 compressor,
  then de-esser) for uneven mic distance or harsh S sounds. A mono voice is upmixed to stereo first; music is
  forced to stereo, so the master never collapses to mono.
- **Duck recovery 600 ms - 1 s** (`--duck-release`, default 700). Faster pumps audibly; slower buries the
  start of the next phrase under music. [PRACTITIONER]
- **Dynamic EQ instead of (or under) broadband ducking:** dip only the music's 2-5 kHz presence band while the
  voice speaks, so the bed stays alive. ffmpeg has `adynamicequalizer` but no sidechain key for it; do this
  in a DAW when it matters, otherwise duck. [PARTIAL: technique documented, depth not measured]
- **De-esser placement is contested.** Default: after the compressor (compression exaggerates sibilance the
  de-esser then catches). Alternative: before it, when the compressor pumps hard. A light pass in both places
  is a common compromise. ffmpeg: `deesser=i=0.4` after `acompressor`.
- Room-tone bed: a constant ambience under dialogue cuts at roughly -45 to -50 dB (about -32 LUFS) glues edits
  the ear would otherwise hear as dropouts. [documented, not measured in a session]

## 3. SFX craft

- **SFX only where something visibly changes** (a cut, a graphic landing, a number stopping). Explainers: at
  most about one per second, none on top of a key word.
- **Riser ends AT the hit.** The riser's peak lands on the impact frame; early or late reads as a mistake. In
  `sfx.json` use `"end_at": <hit time>` (or `"peak_at"`) instead of `"at"`: `finish.py` finds the SFX's
  loudest sample and lands THAT on the frame, not the file's edge. SFX `"db"` is relative to the voice peak
  (-6 = 6 dB under the voice peak); an SFX that would start before 0 or run past the end is skipped with a WARN.
- **Whoosh sits under the impact, as its own layer.** Riser builds anticipation, whoosh sells motion, impact
  sells weight: three jobs, three layers. A good whoosh itself has 3-4 frequency layers (sub sweep, mid noise
  band, high air, optional tonal element), each with its own EQ band, which is why it survives phone speakers.
- **Text and UI pops at 20-40% of the impact level** (about 8-14 dB under it). Full-volume pops fatigue the ear
  within seconds; their job is confirmation, not announcement.
- **Never repeat an identical SFX.** Every repeat gets a pitch/speed variation of about 5-10%. `finish.py`
  does this automatically for any file used more than once (0.94-1.08x, deterministic); `"vary": false` keeps
  a sound identical on purpose. Building variety from one whoosh: slow a copy to 60% speed and -5 semitones
  for a deep layer, speed a copy to 120% and +4-5 semitones for a high layer; the peak always lands on the
  movement. Source: luvkilomedia, youtube.com/watch?v=U6wVF2PMBUw, 09:12-11:07.
- **Diegetic detail.** Sounds that exist inside the shot (keyboard clicks, footsteps, a cup on a desk) make
  B-roll feel real. Most editors only add designed SFX; lay the literal sound too. Source: Abhay PS Rajawat,
  youtube.com/watch?v=SWAYLiH7p5M, 05:42-06:10.

## 4. Music structure

- **Riser -> smash cut -> silence.** Build, hard cut to the reveal, then about 0.25-0.5 s of near-silence before
  the payoff lands [exact ms UNVERIFIED]. Silence after the cut is the loudest moment in the video.
- **Full stop on the beat.** Stopping the music dead on a beat makes that moment land harder:
  `finish.py --music-stop <time>`. By default the last 10 frames ring out as a ~3 s reverb tail (the "cinematic
  end" recipe: cut 10 frames before the end point, duplicate that tail, extend it about 4 s, reverb it, drop
  about 5 dB to offset the overlap). `--music-tail cut` for a hard stop. A dead stop is only dead if nothing
  rings through it: check with `qa.py <final> --silence-at <time>` when the voice pauses there too (the 0.5 s after must sit 14 LU or more
  under the programme; long impact or reverb tails are the usual failure). Source: luvkilomedia (U6wVF2PMBUw)
  03:04-04:47; Abhay PS Rajawat (SWAYLiH7p5M) 05:29-05:37.
- **Rotate the bed every 60-90 s.** The ear adapts to a track and stops hearing it; change track, tempo or
  energy at section boundaries. [creator rule, Abhay PS Rajawat 04:11-04:31]
- **Chapter changes on musical bars, cuts on beats.** One timeline drives picture and score (the beat grid).
- Music-first sequencing for B-roll montages: cut the assembly to the music's structure (drops, breaks,
  builds) first, then fine-cut to the voice.

## 5. Texture beds

- **Background-talking texture** (documentary/crime): isolate talking from news or interview footage, lay it at
  -15 to -20 dB under the scene, cut it into segments around the gaps, then EQ it slightly muffled (lowpass
  about 3-4 kHz) so it sits inside the soundtrack. Source: luvkilomedia (U6wVF2PMBUw) 13:41-16:29.

## 6. Code-native scoring (optional)

A score can be synthesised per scene instead of licensed: a cue timeline drives instrument recipes (kick, sub,
hats, pads, risers), no samples, no licence. Doctrines from the one public implementation
(tuzhechen2005/opus-video-skills, kinetic-reel sound references): no whooshes inside the score (they are
transition SFX, not music), silence on about half the cuts so the score breathes, chapter changes on bars.
[SECONDARY: repo, not evaluated here.] Offer it when the user wants a fully original, licence-free bed.

## 7. QA: the Closed Eye Test

Play the cut with eyes closed. If it still holds attention, the edit works; if it is boring, it is pretty but
not engaging. Fix voice, rhythm, silences and gaps **before** visual polish. Source: Abhay PS Rajawat
(SWAYLiH7p5M) 00:36-01:54. (The "brain sides with audio" mechanism he cites is unproven; the habit is the
rule.) Then listen once on a phone speaker: anything that disappears there (sub-only hits, low whooshes) needs
a mid layer.

For long-form narrative edits, build the sound skeleton first: dialogue cut, then music, score, field
recordings and SFX with zero visuals ("treat it as a song", with a rise and fall), and only then lay picture
on top. Source: Max McCoy, youtube.com/watch?v=XUWjBQiT1Iw, 01:08-08:54. For code-built kinetic reels, picture
and sound co-evolve; the Closed Eye Test is the check instead.


# ===== FILE: references/color-grading.md =====

# Colour: correct, match, grade, finish

Tool: `scripts/grade.py`. Every filter it uses was verified to exist and render on ffmpeg 6.1 (2026-10-11);
the recipes were checked on a test chart with a skin patch and saturated bars.

## Contents
1. Order of operations
2. grade.py in practice
3. Verified ffmpeg facts (and traps)
4. Recipes behind the looks
5. Guardrails
6. What ffmpeg cannot do

## 1. Order of operations

Exposure and white balance are **correction**; everything after is **look**. Order matters:

1. Match exposure (about 80% of any shot-to-shot mismatch), then white balance, across all sources
   (`--match`). Grade-match B-roll and AI shots to the A-roll before any look.
2. Skin check: skin must stay skin. Warmth before saturation; saturation via vibrance (protects skin).
3. Look (`--look`) or a project LUT (`--lut`).
4. Finishing: highlight glow (optional), grain 1-5% last.

## 2. grade.py in practice

```bash
python3 scripts/grade.py renders/v1.mp4 --look warm --still 4.0 --out-still work/grade_warm.png   # before|after
python3 scripts/grade.py work/broll.mp4 work/broll_m.mp4 --match renders/v1.mp4                    # match first
python3 scripts/grade.py renders/v1.mp4 renders/v1_graded.mp4 --look warm --strength 0.8 --grain 2
python3 scripts/grade.py --look film --export-lut work/looks/film.cube     # ship the look as a .cube
```

- Looks: `clean` (correction only), `warm` (talking head, gentle), `split` (teal shadows / warm highlights,
  subtle: the 2025 premium register, not 2016 teal-and-orange), `film` (lifted blacks, softer saturation),
  `mono`.
- **2026 practice: the look is a shipped `.cube` file** applied with `lut3d`, not a filter chain rebuilt per
  video. `--export-lut` bakes the colour part (not match, glow or grain, which are per-clip or spatial) into a
  33-point LUT that Resolve, Premiere, CapCut and ffmpeg all read. Verified: LUT output matches the direct
  chain within 1/255.
- Always make the `--still` before/after first and look at skin, blacks and the brightest highlight.
- **LUT-only runs default to 75% strength** (`--lut x.cube` without `--strength`): a creative LUT at 100% is
  almost always too much on real footage. `--look` and `--lut` together are refused (pick one: they stack).
- **HDR / HLG / PQ sources** (iPhone default) are refused unless you pass `--tonemap`, which converts to
  BT.709 SDR (zscale + hable) before grading. Grading HDR as if it were SDR gives washed-out or neon results.
- **Never grade a graded file.** Grade from the cut of the source, once. A filename containing `graded` or
  `captions` makes the script WARN: captions must never be graded, and a second grade compounds the first.

## 3. Verified ffmpeg facts (and traps)

- `vibrance` exists (ffmpeg 5.1+), intensity -2..2. It boosts muted colours more than saturated ones, so skin
  survives; `eq=saturation` hits skin too.
- `colortemperature` exists and is the real white-balance filter. Lower Kelvin = warmer (4500 K turns grey
  orange, 8500 K blue). It is strong: use `mix` 0.3-0.6.
- `selectivecolor` values are **-1..1**, never Photoshop's -100..100 (`reds=-30` hard-errors).
- There is **no** `white_balance` filter and **no** `bloom` filter. Bloom = blurred highlight copy screened on
  top (`grade.py --glow`).
- **Trap found while building grade.py:** `colorbalance` with `pl=1` (preserve lightness) turns any pixel that
  has a zero channel (pure yellow, green, red, logos, saturated graphics) flat grey in ffmpeg 6.x. Never use
  `pl=1` on colorbalance. (`colortemperature pl=1` is fine.)
- Durations need a leading zero in every ffmpeg option: `-t .6` and `afade=d=.25` hard-error; write `0.6`.

## 4. Recipes behind the looks

- Talking head: gentle warmth (colortemperature 5600 K, mix 0.35) -> vibrance 0.05 -> a soft S-curve. Measured
  on the skin patch: (197,138,108) -> (208,139,101): warmer, not orange.
- Split-tone: `colorbalance` shadows toward teal (rs -0.05, bs +0.06), highlights warm (rh +0.05, bh -0.04).
- Film: lifted blacks (`curves` 0 -> 0.055), slightly lowered whites, saturation 0.88, a touch of warm
  highlights. Lifted blacks are the film-emulation signature.
- Glow: copy -> keep only highlights (`curves 0.62/0`) -> `gblur sigma 18` -> screen at 0.15-0.35 opacity.
- Grain: temporal noise; 1-5% dithers compression banding on gradients after platform re-encoding.
- Face relight on locked-off talking heads: an inverted soft vignette lifting the face region
  (`vignette=mode=backward` on a masked copy). Only for shots where the camera never moves.
- HDR phone footage: tone-map to SDR bt709 before editing (`zscale` + `tonemap=hable` or mobius); test per
  source, no single recipe survives every HDR master.

## 5. Guardrails

- **Never crush blacks for "punch" on mobile.** Phone screens hide shadow detail; crushed blacks read as mud.
  The claim that "high contrast wins on mobile" is rejected (crushed blacks are the textbook bad grade).
- One grade per video; every shot (A-roll, B-roll, AI shots, graphics with photos) matches it.
- Teal-and-orange: there is documented discussion of its decline in 2025-26 premium work; one data point, not a
  rule. Use `split` subtly or not at all.
- Grade after the edit is locked, before captions (captions are never graded).

## 6. What ffmpeg cannot do (say so instead of faking it)

Tracked face relighting, AI subject masks (sky replacement, background-only grading), per-object keying,
power windows that follow motion, true HDR grading, and **mixed lighting** (a face lit by a window on one side
and a tungsten lamp on the other cannot be fixed by one global white balance). For those, recommend DaVinci Resolve (free) and
deliver a LUT plus notes; do not promise a filter chain.


# ===== FILE: references/visual-sourcing.md =====

# Visual sourcing: where every picture comes from

**Default: build it.** Motion graphics, cards, kinetic type, overlays, charts, UI mockups, annotations and
diagrams are made in code (HyperFrames). Sourcing is only for raster or photographic assets that cannot be
code-built: photos, PNG cut-outs, textures, archival images, product shots, B-roll.

## The cascade (in this order, every project)

1. **Ask first:** "Do you have the visuals/PNGs for this, or should I source them?" Never assume.
2. **User-provided assets win.** Brand files, logos, photos, PNGs, screen recordings the user drops in are used
   **as supplied**. Never regenerate, "improve", restyle or upscale them without a yes. Cut-outs of supplied
   photos (`rembg`, if installed) count as using them.
3. **Web sourcing** for what is missing, with a licence note per file in `EDIT_STATE.md` (source URL, licence,
   attribution text if required):
   - Free to use commercially: Unsplash, Pexels, Pixabay (photos/video), Wikimedia Commons (check each file's
     licence: CC0 / CC-BY need credit, CC-BY-SA needs share-alike, some are non-commercial), NASA and most US
     government media (public domain), Smithsonian Open Access (CC0).
   - Prefer transparent PNGs for overlays; textures (paper, grain, film burns) from the same free sources.
   - **Pinterest is a moodboard, not a licence.** It aggregates other people's images; most pins are
     copyrighted by someone else. Use it to find the look or the original source, then use the original only
     if its licence allows. Never ship a Pinterest download as-is in a monetised or client video.
   - Never use watermarked stock, comp images, or images from Google Images without a known licence.
   - Logos and product screenshots of other companies: fine for commentary/editorial use, never in a way that
     implies endorsement.
4. **Higgsfield (only if available and confirmed).** Ask once per project: "Do you want me to generate
   visuals with Higgsfield for this one?" Remember the answer in `EDIT_STATE.md`. If yes and a Higgsfield
   connector is connected in this Claude session, generate there; if not connected, say so and go to step 5.
5. **Image-generation prompt pack (always available).** For every scene that needs a visual nobody has, write
   a production-ready prompt the user can paste into any image or video model (format below), saved as
   `work/prompt-pack.md` next to the storyboard.

## Not-found protocol: a scene never ships empty

When a wanted visual is not found, pursue every available path in parallel, and report all three results:

- (a) keep sourcing with alternate search terms and other sites;
- (b) write the prompt-pack entry so the user can generate it;
- (c) generate it with Higgsfield if the project confirmed it and the connector is available;
- and meanwhile build a code-made stand-in (type card, diagram, annotated texture) so the edit can proceed.

Report: what was found (with licences), what was generated, which prompts are waiting for the user.
"Not found" is never the end of the step.

## Prompt-pack format (6 parts per visual)

```
### Scene 4 (0:12-0:15) "a whole cast"
Subject:     <who/what, specific: age, clothing, object, action>
Style:       <match the storyboard's selected option: palette hexes, film stock / illustration style, era>
Composition: <framing, angle, lens, where empty space must be for the type (e.g. top 40% clear)>
Motion:      <video only: one camera move, duration <= 3 s, what moves>
Technical:   <aspect 9:16 | 16:9, resolution, lighting, depth of field>
Negative:    <no text, no watermark, no extra fingers, no logos, no second accent colour>
Consistency: <base image / seed / character sheet to reuse; the same palette lock as other scenes>
```

## Rules for AI visuals

- **Still first, then image-to-video.** Lock the frame as an image, approve it, then animate it. Never
  text-to-video for editorial shots: it drifts.
- **Keep AI shots under about 3 s** and cover seams with cuts; long AI shots expose drift and uncanny motion.
- **One base image per character** across every scene and variant; never regenerate a face per scene.
- **Consistency pass:** all AI visuals share the palette lock and subject treatment of the selected storyboard
  option; grade-match them to the A-roll (`grade.py --match`).
- Disclose synthetic people in ads where the law requires it (see `ugc-ads.md`).
- No generic stock filler (glowing brains, handshakes, random cityscapes): every visual must illustrate the
  exact sentence it sits on.


# ===== FILE: references/ugc-ads.md =====

# UGC and AI-avatar ads

Paid social creative follows different rules from organic content: it is built to be tested, iterated and
disclosed. Practitioner numbers are labelled [PRACTITIONER]; nothing here is platform-measured unless stated.

## Structure

- **The 4-part hook stack, all in the first 3 s:** visual hook (what the thumb stops for), verbal hook (first
  line), text hook (on-screen line), audio hook (sound that breaks the feed). Most weak hooks are missing a
  part, not weak in all four.
- **Test the visual hook first.** When iterating, swap the opening image before the words: it moves results
  more in practitioner testing. [PRACTITIONER]
- **A second hook at 3-5 s** re-catches viewers the first hook stopped but did not convince.
- **Winning skeleton:** problem -> friend-style recommendation (not a pitch) -> proof -> soft CTA.
- **Founder on camera in the first seconds with a title overlay** ("Name, founder of X") answers "who is this"
  before it is asked. Reported as a split-test winner; test details are thin. [REPORTED]
- **End card 2-3 s:** brand + one-line CTA (same spec as the motion-reels end card).

## Modular production

- **Hook x body x CTA modules:** e.g. 12 hooks x 4 bodies x 1 CTA = 48 testable variants from one shoot;
  refresh hooks about every 3 weeks. Build the edit as separate module renders plus a variant matrix so any
  combination can be exported. [PRACTITIONER]
- **Creative diversity over one winner** (reported effect of Meta's Andromeda ranking update): many genuinely
  different concepts outperform small tweaks of one ad. Meta has not published the mechanism. [PRACTITIONER]
- **Native vs polished** is a per-brand test, not a law.
- **Shoot for the edit:** 3 full takes of every setup, about 3 s handles at both ends.
- Hook-rate benchmarks circulate widely; treat them as direction (kill a variant that is clearly below its
  siblings), not as targets.

## AI avatars and synthetic presenters

- **Cover seams with B-roll.** Lip-sync drift and loop points are where avatars fail; cut to B-roll over them.
  One practitioner reported about +20% on their metric from doing this (single source). [n=1]
- **One base image per character** across every variant; never regenerate the face per scene.
- No specific caption treatment for avatar videos was found to matter; use the normal caption rules.

## Disclosure (verified 2026-10-11 against primary sources)

**When in doubt, disclose.** A visible "AI-generated" or "synthetic presenter" label costs almost nothing in
performance and removes the legal risk in every market below. Default to disclosing any AI person or voice in
a paid ad; drop it only when the user confirms with counsel that it is not needed.

**C2PA survives only on the master.** `finish.py` and every ffmpeg re-encode strip C2PA / Content Credentials
metadata. Keep the AI tool's original export (with its provenance) in `source/` or `renders/masters/`, and
tell the user the delivered MP4 no longer carries it, so platform "AI info" labels will not trigger
automatically: they must set the platform's AI toggle by hand.

- **New York, GBL section 396-b** (S.8420-A / A.8887-B, signed 11 Dec 2025, **in force since 9 June 2026**):
  an advertiser who knowingly uses a "synthetic performer" (an AI or algorithm-made person not recognisable as
  any real performer) in an ad must disclose it conspicuously. Civil penalty $1,000 for a first violation,
  $5,000 for each later one. Exempt: audio-only ads, AI used only to translate a real performer, and ads for
  expressive works consistent with the work. Source: nysenate.gov/legislation/bills/2025/S8420/amendment/A.
- **California AI Transparency Act** (SB 942, amended by AB 853): operative **2 Aug 2026**. Its duties fall
  mainly on large generative-AI providers (detection tools, embedded provenance), not directly on advertisers;
  more duties phase in 2027-2028. Practical effect: keep provenance metadata from AI tools intact (do not strip
  C2PA data on export when avoidable).
- **EU AI Act, Article 50:** applies from **2 Aug 2026**. Deployers who publish deepfake image, audio or video
  content must disclose that it is artificially generated or manipulated (lighter rules for evidently
  artistic or satirical work). Fines up to EUR 15 million or 3% of worldwide turnover. Some marking duties for
  providers are deferred to 2 Dec 2026.
- **Platforms:** Meta shows "AI info" labels from C2PA/IPTC metadata and requires disclosure of digitally
  altered media in political and social-issue ads; TikTok has an AI-generated content toggle and asks creators
  to label realistic AI content; YouTube requires the "altered or synthetic content" disclosure for realistic
  synthetic media. Check each platform's current ad policy before a paid launch.
- This is information, not legal advice: for paid campaigns in these markets, tell the user to confirm with
  their counsel.

## Ethics (not testable)

No fabricated testimonials, no fake before/afters, no invented results or reviews, no impersonation of real
people. If a brief asks for any of these, decline that part and say why.


# ===== FILE: references/style-reverse-engineering.md =====

# Reverse-engineering a creator's style

Goal: a style card of measured rules, each with a reason and an example timestamp, confirmed across at least 2 of the creator's videos. "Copy by vibes" produces a costume; measuring produces the actual mechanics.

## 1. Get the references

**Two ways in.** Ask: "Give me 2-3 video links, OR a YouTube channel / Instagram page?"

- **A channel or page:** do not make the user pick. Rank its recent posts and take the top 10 edits of the
  format being made, then measure all of them:
  ```bash
  python3 scripts/top_refs.py "https://www.youtube.com/@creator/shorts" --top 10 --out work/refs/creator
  python3 scripts/top_refs.py "https://www.instagram.com/creator/" --top 10 --cookies-from-browser chrome --out work/refs/creator
  python3 scripts/compare_refs.py work/refs/creator/* --out work/refs/creator     # what they ALWAYS do
  ```
  YouTube ranks by views. Instagram hides views, so it ranks by likes: say "most liked", never "most viewed".
  If Instagram/TikTok listing fails even with cookies, open the page in the browser, copy the top post URLs
  into `urls.txt` and run `top_refs.py --urls urls.txt`. Use `--list-only` first to show the user the ranked
  list before downloading.
- **Links:** measure each with `analyze_reference.py`, then `compare_refs.py` if there are 2 or more.
- `compare_refs.py` marks each metric CONSISTENT (60%+ of videos within 25% of the median) or VARIES. Only
  CONSISTENT numbers become style-card rules; VARIES are per-video choices. It still cannot read fonts,
  captions, graphics or hooks: open each video's `hook.png` and `shots/` and check those across the set.

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

## 9. The Style Lab: a motion vocabulary that compounds

The storyboard says what happens scene by scene; the Style Lab is the reusable vocabulary it draws from. Keep
it in `assets/style-lab.md` (copy to the user's workspace once and keep it across projects):

- **Keep / Maybe / Drop.** Rate every motion option (caption treatment, transition, card style, SFX) against
  the brief. Track coverage ("12 of 20 rated"). Drops go into a **kill log with the reason**, so killed
  styles are never re-proposed.
- **Fair comparison.** Compare options on the same brief and the same beat (never option A on the hook vs
  option B on the CTA).
- **Brief deltas.** When the brief changes, write down what changed and why, and re-check the Keeps it affects.
- **Feedback banner.** Record the user's notes verbatim on the option ("square corners, no rounding (your
  note)"), so corrections compound instead of repeating.
- **STYLE.md as build instructions.** The locked style is written as values a renderer can execute ("apex
  tier Anton 18% cap height, accent #D17054, pop 0 frames"), never as mood prose ("premium and dynamic").
- The sound library lives in the same file: SFX and music tagged by role (riser, impact, whoosh, pop, bed),
  source and licence, and Keep / Maybe / Drop.


# ===== FILE: references/platforms-and-styles.md =====

# Delivery Specs, Safe Zones, Creator Editing Styles, Retention Principles

Contents: PART 0: October 2026 update (read first) · PART A: Export specs per platform · PART B: Safe zones for vertical video (1080x1920) · PART C: Creator editing-style breakdowns · PART D: Retention-backed principles (evidence vs opinion) · Source-confidence summary

Research reference for an AI video-editor skill. Compiled 2026-10-11.

**Confidence labels used throughout**
- **[OFFICIAL]**: quoted or paraphrased from the platform's own help or docs page, fetched this session (2026-10-11).
- **[OFFICIAL-snippet]**: official page, but I only saw a search-engine excerpt, not the full page.
- **[3RD-PARTY]**: reputable secondary source (press, tool vendor, educator). Not confirmed by the platform.
- **[UNVERIFIED]**: folk wisdom, my own background knowledge, or sources that disagree. Do not present as fact.
- **[OBSERVED, UNMEASURED]**: qualitative description of a style. No published measurement exists.

All fetched web content was treated as untrusted data.

---

## PART 0: October 2026 update (read first)

Evidence: [STATED] the platform said it; [STUDY] a large-sample analysis; [REPORTED] practitioner consensus
without a linked source. Policies carry dates so they do not rot into folklore.

- **Safe zones re-checked October 2026: unchanged.** Keep the cross-platform box (x 120-888, y 288-1248 of
  1920). One conflicting creator claim about new zones was not confirmed; it is recorded, not adopted.
  [REPORTED]
- **YouTube Shorts "Clear Screen" playback (June 2026)** lets viewers hide the UI; design to the conservative
  box anyway (the UI is still there for most), and assume the first seconds carry even more weight. [REPORTED]
- **Durations (2026 calibrations, by genre, not laws):** Shorts 15-35 s; TikTok performance is bimodal (short
  punchy OR long satisfying; the middle underperforms) [STUDY, 111k videos, citation not linked]; Reels work in
  two bands, 45-60 s and 120-180 s, with a drop after 180 s. [REPORTED]
- **Instagram ranking (Mosseri):** the first seconds dominate; sends/shares and saves weigh more than likes.
  [STATED] Trial Reels show a reel to non-followers first: route new formats through them. [STATED]
- **Loops:** resolve 80-90% of the loop cleanly and end the audio mid-thought so the restart feels like a
  continuation. (A "1.2x loop speed" claim is unverified.)
- **Originality crackdown (dated):** Instagram demotes reposted/aggregated content (rule introduced April
  2024, extended to photos and carousels April 2026); Facebook tightened unoriginal-content rules in 2026;
  YouTube's reused-content enforcement was tightened again in 2026. Watermarked or re-uploaded content is
  close to distribution-dead. Exact dates beyond Instagram's are [REPORTED].
- **Landscape masters as Reels:** Instagram letterboxes a 16:9 upload in the Reels player (it does not
  centre-crop). Two of the four reference motion pages post 16:9 on purpose; keep type centre-safe.
- **Covers:** Instagram's profile grid shows 3:4; for 4:5 feed posts the visible band is about y 285-1635 of a
  1080x1920 frame. Compose covers for both. Meta states tall displays (19.5:9) crop the edges of 9:16.
- **TikTok:** captions up to 4,000 characters, and on-screen text is indexed for search, so put the words the
  video should rank for in a burned text line once. Comment polls are a lower-friction CTA than "comment X".
- **Series formats** ("Part 1/2/3") earn follow-through viewing; the previous part does the hooking.
- **Myths (do not encode as rules):** universal best posting times (low evidence); hashtags as a reach boost
  (they now work as search labels); "50% of viewers watch muted" (widely quoted, never sourced; design muted-
  first anyway because the practice is sound).

## PART A: Export specs per platform

### A1. YouTube long-form: official recommended upload encoding [OFFICIAL]
Source: https://support.google.com/youtube/answer/1722171?hl=en

| Item | YouTube recommendation |
|---|---|
| Container | MP4. No edit lists. moov atom at the front of the file ("Fast Start"). |
| Video codec | H.264, progressive (no interlacing), **High Profile**, 2 consecutive B-frames, **closed GOP, GOP of half the frame rate**, CABAC, VBR (no bitrate limit required), chroma subsampling **4:2:0**. |
| Audio codec | AAC-LC, Opus, or Eclipsa Audio. Channels: Stereo, or Stereo + 5.1, or Stereo + Eclipsa. **Sample rate 48 kHz.** |
| Audio bitrate | Mono 128 kbps · **Stereo 384 kbps** · 5.1 512 kbps (Eclipsa: 128 kbps per channel). |
| Frame rate | Encode at the recorded frame rate. Common: 24, 25, 30, 48, 50, 60 (others accepted). Deinterlace interlaced sources (1080i60 becomes 1080p30). |
| Aspect | 16:9 standard on desktop. The player adapts to vertical or square. |
| SDR color | **BT.709** primaries, transfer and matrix (H.273 value 1). An unspecified TRC or matrix is assumed to be BT.709. Full range is converted to limited range. The RGB matrix is not recommended. BT.2020 without an HDR transfer is converted to 8-bit BT.709. |

**Recommended SDR video bitrates [OFFICIAL]**

| Resolution | 24/25/30 fps | 48/50/60 fps |
|---|---|---|
| 8K | 80–160 Mbps | 120–240 Mbps |
| 2160p (4K) | 35–45 Mbps | 53–68 Mbps |
| 1440p | 16 Mbps | 24 Mbps |
| 1080p | 8 Mbps | 12 Mbps |
| 720p | 5 Mbps | 7.5 Mbps |
| 480p | 2.5 Mbps | 4 Mbps |
| 360p | 1 Mbps | 1.5 Mbps |

**HDR bitrates [OFFICIAL]:** 4K 44–56 Mbps (SFR) and 66–85 Mbps (HFR). 1440p 20/30. 1080p 10/15. 720p 6.5/9.5. HDR is not supported at 480p or 360p.

**HDR requirements [OFFICIAL]** (https://support.google.com/youtube/answer/7126552?hl=en):
- Transfer function PQ or HLG (Rec. 2100), Rec. 2020 primaries, Rec. 2020 non-constant-luminance matrix, 10- or 12-bit.
- Recommended codecs: VP9 Profile 2, AV1, or HEVC. ProRes, DNxHR and 10-bit H.264 also work but need very high bitrates. Tested containers: MOV, MP4, MKV.
- PQ uploads should carry SMPTE ST 2086 mastering metadata plus MaxFALL and MaxCLL. If these are missing, YouTube assumes a Sony BVM-X300 display. HDR10+ dynamic metadata is optional.
- SDR down-conversion is automatic. You can supply a .cube LUT to guide it.
- **Practical rule:** creators should deliver SDR BT.709 unless they truly mastered in HDR. A phone HLG or HDR clip graded carelessly will look wrong on SDR screens.

### A2. YouTube Shorts [OFFICIAL]
Source: https://support.google.com/youtube/answer/15424877?hl=en
- **Max length: 3 minutes.** Any square or vertical upload of 3 minutes or less, uploaded on or after 2024-10-15, is classified as a Short. For Official Artist Channels this applies from 2025-12-08.
- To avoid Shorts classification, use a wider aspect ratio such as 16:9.
- **A Short over 1 minute with any active Content ID claim is blocked globally.** Shorts under 1 minute are unchanged.
- Shorts Audio Library: most songs can be used for up to 90 s in a 3-minute Short. Some are limited to 60 or 30 s.
- Resolution: YouTube publishes no Shorts-specific resolution. Use **1080x1920 (9:16)** with the same encoding rules as long-form. [UNVERIFIED as an official number; it is the universal practice]
- Shorts view counting changed on 2025-03-31: a view now counts when playback starts or replays, with no minimum watch time. [3RD-PARTY: https://www.bytecap.io/research/youtube-shorts-retention-benchmarks, https://1of10.com/blog/youtube-shorts-analytics/]

### A3. Instagram Reels
- **Length:** you can record or edit Reels up to **20 minutes**, but "Reels over 3 minutes won't be recommended to new audiences." [OFFICIAL-snippet: https://help.instagram.com/2720958398006062/]
- **Aspect:** between 1.91:1 and 9:16. **Minimum 30 fps, minimum 720 px resolution.** [OFFICIAL: https://help.instagram.com/1038071743007909]
- **Boosting a Reel** requires 90 s or less, 9:16, and no licensed music. [OFFICIAL-snippet: https://help.instagram.com/570215404599013/]
- **Reels ad specs (Meta Ads Guide)** [OFFICIAL: https://www.facebook.com/business/ads-guide/update/video/instagram-reels]:
  - MP4 or MOV, 9:16, **recommended 1440x2560**.
  - H.264, square pixels, fixed frame rate, progressive, **stereo AAC 128 kbps+**.
  - 0 s to 15 min, max 4 GB.
- **Practical delivery:** 1080x1920, H.264 High, 30 fps (or native 24/25/60), constant frame rate, AAC 48 kHz. Instagram recompresses heavily. Uploading a cleaner, higher-bitrate file (12–20 Mbps at 1080p) and enabling "Upload at highest quality" in the app helps. [UNVERIFIED practice]
- Feed grid preview crops Reels to the centre. Keep the cover's key content in the middle of the frame. [UNVERIFIED exact ratio. Instagram changed the grid to 3:4 in 2025 per press reports, but I did not confirm this officially.]

### A4. TikTok
- **Length:** videos recorded in TikTok can be up to **10 min**. Videos uploaded in TikTok can be up to **60 min**. [OFFICIAL-snippet: https://support.tiktok.com/en/using-tiktok/creating-videos/camera-tools]
- **TikTok Studio (web) upload rules:** MP4 or WebM, **720x1280 or higher**, **up to 30 min**, under 10 GB. [OFFICIAL: https://support.tiktok.com/en/using-tiktok/creating-videos/creator-tools-on-tiktok, which redirects to tiktok.com/support/faq_detail?id=7581820704895703564]
  - Note the conflict: the in-app limit is 60 min, the web Studio page says 30 min. Treat 30 min as the safe cross-surface limit.
- **Series** videos run from 30 s to 20 min. [OFFICIAL-snippet: https://support.tiktok.com/en/business-and-creator/tiktok-series/create-and-manage-series]
- **In-Feed ad specs** [OFFICIAL: https://ads.tiktok.com/help/article/video-ads-specifications]:
  - 9:16 recommended, at least 540x960. Also .mp4, .mov, .mpeg, .3gp, .avi.
  - Up to 10 min, 500 MB or less, **bitrate 516 kbps or more**.
  - Ad caption up to 4 lines.
  - Safe zones come as downloadable template files only (no numbers in the text).
- **Practical delivery:** 1080x1920, H.264 High, 30 or 60 fps CFR, AAC 48 kHz, 10–20 Mbps. [UNVERIFIED practice]

### A5. LinkedIn video
- **LinkedIn Pages** [OFFICIAL-snippet: https://www.linkedin.com/help/linkedin/answer/a1311816]: 75 KB to 5 GB, **3 s to 10 min**, resolution 256x144 to 4096x2304.
- **Member posts** [OFFICIAL-snippet: https://www.linkedin.com/help/linkedin/answer/a7174587 and a548372]: minimum 3 s on desktop or 2 s on mobile, resolution 256x144 to 4096x2304.
  - Max duration is **15 min on desktop and 10 min on mobile** per a third-party source [3RD-PARTY: https://www.descript.com/blog/article/linkedin-video-the-complete-guide]. I could not fetch the LinkedIn page itself because the site blocks scrapers.
- **Video ads:** 75 KB to 500 MB. LinkedIn recommends 15–30 s. [OFFICIAL-snippet: https://www.linkedin.com/help/linkedin/answer/a424737]
- **Captions:** LinkedIn accepts SRT caption upload on video posts. [UNVERIFIED this session; long-standing feature]
- **Practical delivery:** 1080x1080 (1:1), 1080x1350 (4:5) or 1920x1080. Feed autoplays muted, so burned-in captions are strongly advised. [UNVERIFIED practice]

### A6. X (Twitter) video
- **Length and size** [OFFICIAL: https://help.x.com/en/using-x/x-videos]:
  - Non-Premium: up to **140 s, 512 MB**.
  - Premium: under 4 h at **1080p**, max 16 GB. Videos from 2 h to 4 h upload at 720p.
- **API "best practices"** [OFFICIAL-snippet: https://docs.x.com/x-api/media/quickstart/best-practices]:
  - H.264 High Profile, 30 or 60 fps, AAC-LC audio.
  - Recommended resolution 1280x720 (landscape), 720x1280 (portrait) or 720x720 (square).
  - The page itself blocks scrapers.
- **Practical delivery:** 1920x1080 or 1080x1920, H.264 High, AAC 48 kHz at 128–256 kbps, 30 fps. [UNVERIFIED practice]

### A7. Loudness targets
No major video platform officially publishes a LUFS target. Everything below about platforms is measured or community knowledge.

| Platform or standard | Target | Status |
|---|---|---|
| YouTube | Playback normalized toward about **−14 LUFS** integrated. Turns loud uploads **down only** and does not boost quiet ones. Shown as "content loudness" in Stats for Nerds. | [3RD-PARTY measured: https://meterplugs.com/blog/2019/09/18/youtube-changes-loudness-reference-to-14-lufs.html, https://youlean.co/?p=30813]. Not documented by YouTube. |
| TikTok / Instagram / Facebook | No published spec. Vendor guides cite −14 LUFS, while others claim a "louder" −10 to −12 LUFS performs better. | [UNVERIFIED, conflicting: https://www.forasoft.com/learn/audio-for-video/articles-audio/lufs-targets-per-platform-2026, https://openclip.app/learn/audio-normalization] |
| AES TD1008 (2021, streaming/online) | Speech and "assorted" content: **−18 LUFS** distribution loudness. It superseded TD1004 (−16 to −20 LUFS, −1 dBTP max). | [3RD-PARTY summary: https://productionadvice.co.uk/td1008/] |
| EBU R128 (broadcast, EU/India broadcast practice) | −23 LUFS ±1, −1 dBTP | [UNVERIFIED this session; standard knowledge] |
| ATSC A/85 (US broadcast) | −24 LKFS, −2 dBTP | [UNVERIFIED this session; standard knowledge] |

**Recommended default for the skill (opinion):**
- Master to **−14 LUFS integrated, true peak ≤ −1.0 dBTP** for YouTube, Shorts, Reels, TikTok, LinkedIn and X.
- Keep dialogue LRA about 6–9 LU for talking-head content. Keep music beds about 18–24 dB under voice in speech sections.
- Optional "loud shorts" variant at −12 LUFS, −1 dBTP. Label it as opinion.
- Use a two-pass ffmpeg `loudnorm` (see A10).

### A8. Thumbnails [OFFICIAL]
Source: https://support.google.com/youtube/answer/72431?hl=en (current text, fetched 2026-10-11)
- **Resolution:** the page now says "3840 x 2160 pixels for videos and 2160 x 3840 for Shorts". The minimum width is 640 px for videos, and the minimum height is 640 px for Shorts.
  - **The old "1280x720" spec is out of date as the recommendation.** It is still accepted because it is above 640 px wide.
- **Format:** image formats "such as JPG or PNG".
- **Size limit:** **2 MB when uploading on mobile** (10 MB for podcasts). **50 MB on desktop** for video, Shorts and podcast thumbnails.
- **Aspect:** 16:9 for videos, 9:16 for Shorts, 1:1 for podcast playlists.
- Custom thumbnails require a verified account. [OFFICIAL page intro]
- **Skill default:**
  - Render 3840x2160 PNG or JPG master, plus a 1920x1080 JPG at quality 90 or below 2 MB for mobile or legacy upload.
  - Check legibility at 168x94 px, the size of a mobile list thumbnail. [UNVERIFIED pixel size]

### A9. Caption file formats
- **YouTube** [OFFICIAL: https://support.google.com/youtube/answer/2734698?hl=en]:
  - Basic formats: **SRT** (plain UTF-8, no styling), **SBV/SUB**, MPsub, LRC, Videotron Lambda .cap.
  - Advanced formats: SAMI, RealText, **WebVTT** (positioning supported, styling limited to `<b><i><u>`), **TTML/DFXP** (styling and positioning supported, iTT subset).
  - Broadcast formats: **SCC** (preferred for CEA-608), EBU-STL, .tds, .cin, .asc, .cap.
- **Hindi tip:** upload SRT in **UTF-8** Devanagari for a Hindi track and a separate Latin-script Hinglish or English track. Set the video language correctly so auto-translate and auto-dub behave. [UNVERIFIED best practice]
- **LinkedIn:** SRT. **Facebook:** SRT named `name.xx_XX.srt`. **X:** SRT via the web or Media Studio. **TikTok and Instagram:** generally no sidecar upload for organic posts, so **burn captions in**. [All UNVERIFIED this session]

### A10. Practical ffmpeg export presets
The YouTube spec above is documented. The ffmpeg flags are standard ffmpeg semantics (https://trac.ffmpeg.org/wiki/Encode/H.264; the page timed out this session, so the CRF facts below come from my knowledge of that wiki: CRF range 0–51, default 23, "17–18 visually lossless or nearly so", `-movflags +faststart` for web playback, `-pix_fmt yuv420p` for compatibility with non-FFmpeg players).

**YouTube long-form, 1080p SDR, master-quality upload**
```bash
ffmpeg -i in.mov \
  -c:v libx264 -preset slow -crf 17 -profile:v high -level:v 4.2 \
  -pix_fmt yuv420p -bf 2 -g <fps/2> -keyint_min <fps/2> -sc_threshold 0 \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
  -r <source_fps> -fps_mode cfr \
  -c:a aac -b:a 384k -ar 48000 -ac 2 \
  -movflags +faststart out.mp4
```
- `-g <fps/2>` (for example 15 at 30 fps) follows YouTube's "GOP of half the frame rate" [OFFICIAL spec]. Most editors ignore this with no visible penalty. Making it optional is fine. [UNVERIFIED that it matters]
- x264 uses closed GOP by default. Do not pass `-x264-params open-gop=1`.
- CRF 16–18 at 1080p typically lands well above YouTube's 8–12 Mbps floor, which is fine. To force a floor or ceiling, use 2-pass `-b:v 16M -maxrate 24M -bufsize 32M`.
- **AAC:** YouTube recommends 384 kbps stereo. 320 kbps is also fine. The ffmpeg native `aac` encoder is acceptable at 256 kbps or more. `libfdk_aac` is better but rarely compiled in. [UNVERIFIED quality claim]
- **Color tagging:** tag BT.709 explicitly. Untagged files are assumed to be 709 [OFFICIAL], but tagging avoids gamma or "washed-out" mismatches in QuickTime and Premiere round trips. [UNVERIFIED claim on mismatches]
  - If the source is sRGB or full-range screen recordings, convert first: `-vf "scale=out_range=tv:out_color_matrix=bt709,format=yuv420p"` or use `zscale`.

**Vertical Shorts, Reels or TikTok (1080x1920)**
```bash
ffmpeg -i in.mov -vf "scale=1080:1920:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset slow -crf 18 -profile:v high -level:v 4.2 -r 30 -fps_mode cfr \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart out_vertical.mp4
```
- Use `-r 60` for gameplay or fast motion. Keep CFR, because Meta requires a "fixed frame rate" [OFFICIAL].

**Loudness, two-pass**
```bash
ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1:LRA=9:print_format=json -f null -
# then feed measured_I/TP/LRA/thresh back in with linear=true
```

**HEVC and AV1 notes**
- YouTube lists HEVC and AV1 as recommended **for HDR** [OFFICIAL]. For SDR the documented codec is H.264.
- HEVC (`libx265 -crf 20 -pix_fmt yuv420p10le -tag:v hvc1`) and AV1 (`libsvtav1 -crf 30-35 -preset 6`) give smaller files for upload over slow Indian broadband or 4G. Everything is re-encoded server-side anyway. [UNVERIFIED benefit]
- SVT-AV1: CRF 0–63, default 35. Presets trade speed against efficiency. Default keyframe interval is about 2–3 s. Film-grain synthesis is available via `film-grain=X`. [OFFICIAL ffmpeg wiki: https://trac.ffmpeg.org/wiki/Encode/AV1]
- Instagram, TikTok, LinkedIn and X: deliver **H.264** for safety. [UNVERIFIED; their docs list H.264]

**Should you export 4K from a 1080p source for YouTube?**
- **Documented:** higher-resolution uploads get higher recommended bitrates, and "to view new 4K uploads in 4K, use a browser or device that supports VP9" [OFFICIAL]. YouTube does not document that a 4K upload changes the codec or bitrate served at 1080p.
- **Folk wisdom, partially supported:** uploading 1440p or 2160p makes YouTube assign VP9 or AV1, with more bitrate per rendition, so the 1080p stream looks better than from a 1080p upload. [3RD-PARTY: https://www.provideocoalition.com/uploading-to-youtube-is-4k-worth-it/, https://filmdaft.com/?p=769]
- **Evidence complicates it:** Streaming Learning Center found AV1 renditions tied to **view count**. High-view 4K videos had AV1, while a 4K video with about 36k views had VP9 only. [3RD-PARTY: https://streaminglearningcenter.com/codecs/which-codec-does-youtube-use-part-iii.html]
- **Skill rule:** offer an optional "YouTube 4K upscale" export (`scale=3840:2160:flags=lanczos`, CRF 18, or about 40–45 Mbps). Label it "folk wisdom, widely reported, costs 4–5x upload size and longer processing". Default to native resolution when bandwidth is limited, which is common in India.

---

## PART B: Safe zones for vertical video (1080x1920)
None of the three platforms publishes these pixel numbers as text.
- Meta publishes percentages.
- TikTok publishes template PNG/ZIP files.
- Google publishes an annotated image.

The pixel figures below are those percentages or images converted to pixels by third parties.

| Platform | Top | Bottom | Left | Right | Source |
|---|---|---|---|---|---|
| **Instagram Reels (organic, user's spec, skill `reels`)** | **220 px** | **420 px** | 35 px | 35 px, plus the like/comment/share rail bottom-right (x > 950 from y ≈ 1340 down) | The user's measured reference: safe area 1010 x 1280 px. Image: `assets/safe-zones/reels-safe-zone-reference.png`. This is the default for any Instagram-only organic reel. |
| **Instagram Reels ads (skill `reels-ad`)** | 14% ≈ **269 px** | 35% ≈ **672 px** | 6% ≈ 65 px | 6% ≈ 65 px | [OFFICIAL %: Meta Ads Guide, https://www.facebook.com/business/ads-guide/update/video/instagram-reels]. Meta's canvas is 1440x2560; percentages scale. |
| **TikTok (In-Feed)** | **240 px** | **660 px** | 120 px | 120 px, plus an action rail about **300 px wide from y≈840 px down** | [3RD-PARTY measurement of TikTok's official template: https://www.upload-post.com/tools/safe-zone-checker/, checked 2026-09-23]. Official templates: https://ads.tiktok.com/help/article/video-ads-specifications |
| TikTok (alt. measurement) | 254 px | 707 px | 122 px | 242 px rail | [3RD-PARTY: https://adkit.so/tools/safe-zones/tiktok, March 2026] |
| **YouTube Shorts** | **288 px** | **672 px** | 48 px | **192 px** | [3RD-PARTY reading of Google Ads Help image: https://www.upload-post.com/tools/safe-zone-checker/]. Image source: https://support.google.com/google-ads/answer/9128498?hl=en |

**Caveats.** Margins vary by device aspect (for example 19.5:9 phones crop the sides), by caption length, and by whether an ad CTA is present. Meta asks for 40% bottom clearance on ads with disclaimers [3RD-PARTY citing Meta: https://www.inro.social/tools/instagram-reels-safe-zone-checker]. The platforms' UIs change several times a year.

**The five zones the scripts know** (`--platform` on `captions.py`, `safezone.py`, `qa.py`; `data-platform` on the kinetic-reel starter). Box is x0, y0, x1, y1 on a 1080x1920 frame and scales to other vertical sizes:

| `--platform` | Safe box | Rail no-go | Use when |
|---|---|---|---|
| `reels` | 35, 220, 1045, 1500 | x > 950 for y > 1340 | Instagram only, organic. Widest text, biggest captions. |
| `reels-ad` | 65, 269, 1015, 1248 | x > 950 for y > 1100 | Instagram paid placement (Meta's 14/35/6% plus ad CTA). |
| `tiktok` | 120, 240, 960, 1260 | x > 780 for y > 840 | TikTok only. |
| `shorts` | 48, 288, 888, 1248 | x > 888 for y > 700 | YouTube Shorts only. |
| `cross` (default) | 120, 288, 888, 1248 | x > 780 for y > 840 | One file posted everywhere. |

**Trade-off, say it to the user:** `cross` is the narrowest box. Captions there wrap to about 480 px (the TikTok rail starts at y 840, right where captions sit), so a 60 s talk splits into roughly 40 caption groups instead of about 24 on `reels`. If the video goes to Instagram only, ask for `--platform reels`; posting a `reels` cut to TikTok puts text under the rail.

**How the skill enforces it:**
- `captions.py --platform X` derives max line width from the zone and prints WARN when a group would cross it.
- `safezone.py html <composition> --platform X` seeks the HyperFrames timeline 10 times per second and measures every text box with ink-accurate bounds (canvas `measureText`, not the CSS content box). It FAILs with the element, time and edge. `data-safe-ignore` skips decorative text on purpose.
- `safezone.py alpha <overlay.mov>` checks non-transparent pixels of an overlay against the zone.
- `safezone.py guide --platform X` writes a transparent guide PNG (copies in `assets/safe-zones/guide_*.png`) to drop over a frame while designing.
- `qa.py --safe X` writes `qa/safezone_<zone>.png`, a contact sheet of the final with the zone drawn: open it and look.

**Universal cross-platform safe box (the intersection; skill default):**
- Usable area: **x 120 to 888 (768 px wide), y 288 to 1248 (960 px tall)**.
- Treat the TikTok right rail (x > 780 for y 840 to 1500) as a no-go for anything important.

**Placement guidance (synthesis; opinion unless noted):**
- **Burned-in captions:** centre horizontally. Put the caption block in **y ≈ 900–1240**, about 47–65% of frame height.
  - Never put captions below y = 1248, where they hit the TikTok, Reels and Shorts bottom UI and description.
  - Max width about 760 px. That gives roughly 2–4 words per line at 70–90 px bold sans for Hormozi-style captions, or 1–2 lines of 6–8 words for calmer styles.
- **Hook or title text (first 1–3 s):** y ≈ 300–600 (upper-middle). This sits below the top UI (search, "Following/For You", Shorts title) and above the face.
- **Face or eyes:** about y 500–800 for single-speaker talking heads, so captions sit under the chin and do not cover the mouth.
- **Logos and CTAs:** inside the safe box, never bottom-right, where the like, comment and share rail sits.
- **Devanagari captions** need about 15–20% more vertical line height than Latin because of matras above and below the line.
  - Fonts with Devanagari coverage: Noto Sans Devanagari, Mukta, Hind, Baloo 2, Poppins (Poppins has Devanagari plus Latin).
  - ffmpeg/libass needs a HarfBuzz-enabled build for correct conjunct shaping. [UNVERIFIED this session; known behaviour]

---

## PART C: Creator editing-style breakdowns
Hard numbers are rare. Every number below has a citation. Everything else is labelled [OBSERVED, UNMEASURED]: my best synthesis from commonly cited breakdowns and familiarity with the channels. The skill should treat these as starting presets to verify by analysing an actual reference video. Measure cuts per minute with scene detection such as `ffmpeg -vf "select='gt(scene,0.3)',showinfo"` or PySceneDetect.

**Key for "ASL"**: average shot length in seconds (running time ÷ number of shots). Cuts per minute = 60 ÷ ASL.

### MrBeast
- **Hard numbers:**
  - Tubefilter counted cuts in one minute from the midpoint of two videos: an older video had **38 cuts in 60 s (ASL ≈ 1.6 s)**, while the 2024 "abandoned city" video had **23 cuts per minute (ASL ≈ 2.6 s)**, with "lingering, zoomed-out shots". [3RD-PARTY: https://tubefilter.com/2024/03/04/mrbeast-editing-style-number-of-cuts-per-video/]
  - MrBeast, March 2024: "This past year i've slowed down our videos, focused on story telling, let scenes breathe, yelled less, more personality, longer videos". [same source, quoting his tweet]
- **Leaked production handbook, "How to succeed in MrBeast production"** (circa 2022, leaked August 2024 by Rosanna Pansino). Authenticity was confirmed by two anonymous former producers to Passionfruit, and MrBeast declined comment. Full text: https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/ ; coverage: https://passionfru.it/mrbeast-leaked-document-81151/ , https://www.creatorhandbook.net/leaked-document-allegedly-reveals-mrbeasts-secrets-to-youtube-success-the-key-takeaways/
  - **Metrics:** CTR, AVD, AVP. "The first minute has the most loss… The first minute of each video is the most important minute." In one example they lost 21M viewers in the first minute.
  - **First minute:** match the expectations of the title and thumbnail ("YOU MUST KNOW THE TITLE AND THUMBNAILS"), and front-load interesting content. Good lighting at the start correlates with less drop-off ("there is, have good lighting at the start of the video").
  - **Minutes 1–3:** "transition from hype to execution… Stop telling people what they will be watching and start showing them." Use "crazy progression", for example covering multiple days in the first 3 minutes.
  - **About 3:00, the "3 minute re-engagement":** a spectacle that "only MrBeast can do".
  - **Minutes 3–6:** "the most exciting and interesting content that is also very simple… lots of quick scene changes and highly stimulating simple content."
  - **About 6:00:** another re-engagement that "needs a little more explanation and will push the story in the back half."
  - **Back half:** viewers are in a "lull", and long explanations can live here. "Don't ever signal the end of the video unless it's to build hype for the prize or payoff."
  - **Length:** average video length over the last 100 videos was 818 s (13:37). Everyone must know "what minute mark" they are working on.
  - **Other principles:** "wow factor" (things no other creator can do). "BRAND DEALS ARE CONTENT". "Me like simple."
- **Observed, unmeasured:**
  - High-saturation, bright, warm grade. Wide-angle multi-cam.
  - Constant on-screen counters and timers (money, days, people left) as progress devices.
  - Punchy SFX on every reveal. Music changes per segment.
  - Bold captions only on key moments in long-form. Shorts and dubbed versions use more text.

### Ali Abdaal (and his editing team)
- **Hard numbers:** a typical video takes about **30 h of editing**: about **4 h** cleaning A-roll (dead space, mistakes, repeats, filler words) and about **8 h** adding B-roll from a personal library plus custom footage. [3RD-PARTY, Adobe blog: https://blog.adobe.com/en/publish/2024/09/05/how-ai-helps-ali-abdaal-save-hours-every-week]
- **Shorts style per Choppity's frame analysis** [3RD-PARTY vendor: https://www.choppity.com/tools/recreate-video-editing-style/ali-abdaal/]:
  - **2–5 s per shot** (ASL), so 12–30 cuts per minute. Cuts fall at thought transitions.
  - Desaturated or B&W base with a selective **yellow** colour pop.
  - Phrase-by-phrase captions (not word-by-word) placed beside the speaker, white with yellow key words, in a handwritten or script-style font.
  - Calm lo-fi or ambient music. Hook is a question or reframe.
  - Submagic describes his captions as "sober" with no bouncy animation [3RD-PARTY: https://www.submagic.co/blog/make-captions-like-ali-abdaal]. The two vendors disagree on reveal style.
- **Tools:** FireCut (AI zoom, silence-cut and caption plugin) was co-developed by Ali Abdaal and Suhail Idrees, so its claims carry a conflict of interest. [3RD-PARTY: https://firecut.ai/blog/how-ali-abdaal-edits-10x-faster-a-deep-dive-into-firecut/]
- **Long-form, observed, unmeasured:**
  - Bright, warm, soft-key home-studio look. Two-camera (front plus 45° side) angle switches used instead of jump cuts.
  - Frequent 110–120% punch-ins on emphasis.
  - Clean sans-serif text pop-ups with icons or emoji. Notion or Apple-style rounded cards, numbered "chapter" title cards.
  - Screen recordings and book covers as B-roll. Gentle whoosh and pop SFX. Light lo-fi bed.
  - Hook: a 15–45 s cold open stating the promise, then a short branded sting.

### Alex Hormozi (and the Iman Gadzhi / "business shorts" family)
- **Hormozi per Choppity** [3RD-PARTY vendor frame analysis: https://www.choppity.com/tools/recreate-video-editing-style/alex-hormozi/]:
  - **Jump cuts every 1–3 s** (20–60 cuts per minute), zero dead air, cuts on emphasis words.
  - **10–20% digital punch-ins**, alternating medium and tight framing. Speaker fills at least 60% of the frame.
  - Captions: bold uppercase sans **close to Montserrat Black**, white with a thick black stroke, **active word highlighted yellow**, **2–4 words visible**, word-by-word pop with a slight bounce, large and centred low.
  - Minimal B-roll. Subtle low-energy music. **No transition SFX**.
  - Dark background, crushed blacks, warm skin. The hook is an immediate bold or contrarian claim with no intro.
- **Other descriptions:**
  - VidPros: Montserrat Black 900, occasional italics, about 3° tilted text, font sizes varied for emphasis. [3RD-PARTY: https://vidpros.com/how-to-edit-videos-like-alex-hormozi/]
  - A CapCut tutorial: max 2 lines, about 6 words. [3RD-PARTY: https://gotranscript.com/public/mastering-youtube-shorts-capcut-tutorial-for-ali-abdaal-alex-hormozi-and-cody-sanchez-styles]
- **Iman Gadzhi:**
  - Subtle zooms, with the "intro zoom" as the most powerful. Switches camera angles on key phrases. B-roll as a pacing tool, including old footage used as flashback. [3RD-PARTY: https://www.opus.pro/pt-br/blog/how-to-edit-instagram-reels-exactly-like-iman-ghadzi]
  - Motion design uses accent colours pulled from the footage, in four types: on-screen text, UI mock-ups, illustrated scenes, and rare 3D. Heavy animation is reserved for moments needing focus. [3RD-PARTY video summary: https://sozai.app/transcript/ai-edit-iman-gadzhi-videos/]
  - **Observed, unmeasured:**
    - Cinematic, teal-and-warm "luxury" grade. Shallow depth of field. Travel, cars and city B-roll at high B-roll share (roughly 40–60% of screen time in long-form).
    - Risers, whooshes and bass hits on transitions. Serif or clean sans titles.
    - Slower long-form pacing (ASL about 3–5 s), faster in Shorts.

### Dan Koe (minimal, aesthetic)
- **[OBSERVED, UNMEASURED]** No reliable published breakdown exists. Search results were only Fiverr gigs and asset packs, for example https://julianbytes.gumroad.com/l/koepack.
  - Long-form essay or monologue, often a single static camera in a dim, minimal room. Alternatively voiceover over **black or near-black backgrounds with sparse white typography** and simple line illustrations or diagrams.
  - Desaturated, moody grade. Slow pacing (ASL often 5–15 s). Little to no SFX. Ambient or piano beds.
  - Minimal captions in long-form. Shorts and Reels use clean centred sentence-case captions.
  - B-roll is sparse: abstract nature, desk or notebook shots.
- Treat this as "quiet authority": restraint is the style. A skill preset should lower cut density, remove punch-ins and use plenty of negative space.

### Johnny Harris (map and documentary motion graphics)
- **Tools:**
  - Maps are built in **After Effects with the GEOlayers plugin**. Johnny's own December 2020 tutorial "How to Create Animated Maps with AfterEffects" covers GEOlayers (about $200) plus a cheaper path, with Mapbox Studio for custom map styles. [3RD-PARTY: https://aescripts.com/learn/how-johnny-harris-makes-maps/, https://aescripts.com/learn/making-maps-for-johnny-harris---volcanoes/, https://glasp.co/youtube/GsojLuJpe_0]
  - Animated globe or camera orbit moves using bearing and pitch, and country highlight overlays. [3RD-PARTY]
- **Texture:**
  - Most graphics and photos carry **textured overlays, film burns, light leaks and noise or grain**.
  - Photos slide in with position keyframes plus blur, with an old projector SFX. [3RD-PARTY: https://blog.motionarray.com/learn/premiere-pro/edit-documentary-in-premiere-pro/]
  - The "physical props" look: paper, desk and hand-drawn annotations. [3RD-PARTY: https://rndr.beehiiv.com/p/5-visuals-next-video-ead0]
- **Observed, unmeasured:**
  - Vlog-documentary hybrid: handheld on-location pieces to camera, plus a desk with printed maps, pins and highlighters, plus archival footage and documents with highlight sweeps.
  - Moderate ASL of about 3–6 s. Heavy original or atmospheric score with deliberate silences. Paper and whoosh SFX.
  - Off-white or cream paper palettes with red and yellow accents. Long-form runs 15–30 min.
  - Hook: personal "I went to X / I found this document" cold open, about 30–60 s.

### Vox explainers
- Founding producer Joe Posner called the format an "animated opinion essay", with rules against desks and talking-head interviews as the backbone. [3RD-PARTY quoting Vox: https://easy-peasy.ai/blog/how-to-make-vox-style-videos-with-ai]
- **Motion:** graphics are often **animated at 12 fps inside a 24 fps edit**, which gives the stepped or "choppy" look. [3RD-PARTY tutorial: https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/]
- **Visual language:** highlighter-pen sweeps over scanned documents or articles, paper-collage textures, maps, charts and kinetic typography. [3RD-PARTY: https://contra.com/s/WZggPY3k-vox-style-motion-graphics-modern-journalism]
- **Observed, unmeasured:**
  - Voiceover-led, nearly 100% B-roll and graphics. ASL about 3–5 s. Muted pastel or off-white palettes with a bold accent (Vox yellow).
  - Clean grotesque sans typography. Subtle music beds and paper or pen SFX.
  - Runs 6–15 min. Hook is a striking chart or question within 15 s.

### Kurzgesagt
- **Hard numbers:** about **1,200+ hours per video** and a team of **45 full-time** staff (2021 AMA). They published only about 150 videos in 8 years. [3RD-PARTY citing the Reddit AMA and channel descriptions: https://thetvdb.com/series/kurzgesagt-in-a-nutshell/episodes/7594048, https://cal1.lr.ggtyler.dev/r/IAmA/duplicates/ql88mw]
- **Tools:** illustration in Adobe Illustrator, animation in After Effects. [3RD-PARTY: https://www.toolfarm.com/?p=77543]
- **Style:** flat vector design with rounded shapes and vibrant colours. [3RD-PARTY: https://artsatmichigan.umich.edu/ink/2019/09/27/simple-bright-beautiful-the-work-of-kurzgesagt]
- **Observed, unmeasured:**
  - Fully animated; no live action, no faces. Saturated neon-on-dark-navy palettes, soft glows and gradients.
  - Continuous camera moves and "infinite zoom" scale transitions instead of hard cuts, so the effective ASL is long but motion never stops.
  - Single narrator, an orchestral or synth score, and dense layered sound design. Runs 8–15 min.
  - Rough music attribution: the channel's in-house music label is Epic Mountain. [UNVERIFIED this session]
- An AI skill can approximate this only with a template library (flat SVG assets plus easing) and should not promise it from raw footage.

### Veritasium
- Derek Muller argues for "legit bait": enticing but accurate titles and thumbnails, iteratively tested. [3RD-PARTY summary of "Clickbait is Unreasonably Effective", 2021: https://briefy.ai/summary/v2/curfkxexuv57xsqmhbo9twba/en/clickbait-is-unreasonably-effective]
- **Observed, unmeasured:**
  - Presenter-led documentary: on-location experiments, expert interviews, clean 2D/3D explanatory animation.
  - Moderate ASL of about 4–7 s. Natural, slightly warm grade. Restrained text, used for labels and equations.
  - Cold open with a counter-intuitive demo or question, then a misconception-then-resolution structure.
  - Runs 15–35 min. Subtle score, with music and SFX used sparingly.

### Mark Rober
- Analysts describe a shift (from the 2018 Glitter Bomb video on) toward story structure: motivation, challenge, emotional payoff. They say he paces videos "like thrillers" with curiosity, setbacks and reveals. [3RD-PARTY: https://www.opus.pro/blog/mark-robers-growth-playbook-how-he-engineered-one-of-youtubes-most-trusted-brands]
- Glitter Bomb as a three-act structure: victim, build, payoff. [3RD-PARTY: https://nofilmschool.com/2018/12/fake-package-catches-thieves]
- **Observed, unmeasured:**
  - Bright, saturated, family-friendly look. Fast build montages (ASL about 1.5–3 s) set against slower explanation segments.
  - Lots of slow-motion. CAD and diagram overlays, with labels and arrows.
  - Kid-friendly humour cutaways, a "squirrel" or "kid" POV gag, and big payoff reveals near the end.
  - Upbeat score with comedic stingers. Runs 15–25 min.

### Ryan Trahan
- **Ryan on thumbnails** [OFFICIAL YouTube blog interview: https://blog.youtube/creator-and-artist-stories/ryan-trahan-thumbnail-editing-secrets-to-going-viral]:
  - "We actually connect a lot deeper with a very subtle face". "Clear background, clean background, my face and then whatever the heck is going on."
  - He brainstorms many 2–3-word thumbnail subtitles. He rejects "exploitative" retention tactics.
- **Story techniques**, from George Blackman's breakdown of "I Spent 100 Days in GTA" [3RD-PARTY: https://georgeblackman.substack.com/p/13-unexpectedly-effective-youtube]:
  - Instant context: states the rules and goal up front. A constrained goal acts as a curiosity loop.
  - Visual progress tracker: dollars pinned to the wall.
  - Recurring characters and habits (in the penny series: McDonald's coffee, brushing teeth, theme tune).
  - **Alternating pacing:** fast edits contrasted with calm moments.
  - Three-act structure, then anticlimax and revelation, and a cliffhanger end.
- **Observed, unmeasured:**
  - Handheld vlog footage plus direct-to-camera narration and voiceover recorded after the fact.
  - Map and route animations, playful handwritten-style text, on-screen counters (money, days).
  - Light, natural grade. Whimsical score. Sincere, slow emotional beats near the end.

### Marques Brownlee (MKBHD)
- **Gear:** RED V-Raptor primary camera, Sony A7S III secondary, ARRI SkyPanel S60 key light, edited in Premiere Pro. Older rigs were RED Weapon and DSMC2. [3RD-PARTY: https://vloggingpro.com/setups/mkbhd/, https://www.theringer.com/2016/8/22/16036670/the-kid-who-revolutionized-youtubes-tech-reviews-a5b9a2a03a04, https://rosetta.to/u/mkbhd/the-mkbhd-gear-tour-2019]
- **Observed, unmeasured:**
  - Ultra-clean product cinematography: matte dark-grey or black sets, motion-control or robotic-arm slider moves, turntable macro shots, very shallow depth of field.
  - Signature **red accent** colour and minimal white sans lower-thirds and spec callouts.
  - Calm, measured talking head with medium ASL (about 4–8 s), lots of B-roll of the product (about 40–60%), and minimal SFX.
  - Ambient electronic beds. Crisp 8K/4K masters delivered at 4K.
  - Structure: quick verdict-tease hook, then sections, then a "should you buy it" ending.
  - A motion-control robot arm is used in the studio. [UNVERIFIED this session; widely shown in his studio tours]

### Colin and Samir
- The format is documentary-style interviews and industry analysis for creators. It started as an audio podcast in 2018 and became a video show in 2020–21. [3RD-PARTY: https://creatorbeast.substack.com/p/colin-and-samir-the-creator-economy, https://everything-pr.com/colin-and-samir-the-creators-who-built-a-media-company-about-creators]
- **Observed, unmeasured:**
  - Two-host and guest multicam podcast set with warm practical lighting.
  - Documentary cutaways: B-roll of the guest's videos, analytics screenshots, articles.
  - Bold quote cards and pull-quotes. Chaptered segments.
  - Relaxed pacing (ASL about 4–8 s). Light music between segments.

### Dhruv Rathee (Indian explainer, Hindi)
- **Process:** he has "a whole team of researchers and fact-checkers", publishes a resource paper for every video, and scores topics on audience demand, passion and relevance. [3RD-PARTY interview: https://www.khaleejtimes.com/uae/indian-influencer-dhruv-rathee-youtube-videos-fact-checked?amp=1]
- **Editor:** a public post by Satish Gola says he has edited Dhruv Rathee's videos for 3+ years. Only the title and snippet were visible because LinkedIn blocks scraping. [https://www.linkedin.com/posts/satishgola_videocreation-dhruvrathee-takeaways-activity-7326903458375106560-m_Bp]
- **Style descriptors** (third-party and freelance listings): concise, sharply edited, explainer visuals over background footage and images, clean motion graphics and text animation, map animation. [3RD-PARTY: https://edimakor.hitpaw.com/video-editing-tips/edit-videos-like-dhruv-rathee.html, https://www.freelancer.com/projects/da-vinci-resolve/high-retention-youtube-documentary]
- **Observed, unmeasured:**
  - Hindi (Hinglish technical terms) narration. Mostly voiceover over visuals, with periodic studio talking head.
  - Vox and Johnny Harris-style **map zooms** (globe to India to state). **Newspaper and tweet screenshots with yellow highlighter sweeps**. Charts and timelines. Heavy stock and news footage, so B-roll is likely above 70% of runtime.
  - Clean white or dark backgrounds with simple sans text. Bold Devanagari or Latin titles.
  - Neutral, informative music beds. ASL about 3–5 s. Runs 15–30 min.
  - Cold open poses the question or controversy within 20–30 s.
  - He operates dubbed language channels. [UNVERIFIED details]

### Ankur Warikoo
- His content is built on personal failure stories. [3RD-PARTY: https://www.businesstoday.in/tech-today/talks/video/i-pick-up-all-my-failures-and-make-them-into-a-story-says-ankur-warikoo-352129-2022-11-07]
- **Observed, unmeasured:**
  - Direct-to-camera talking head in a warm, tidy home-office set. English and Hinglish.
  - Numbered-list structure with simple text cards. Moderate jump cuts (ASL about 3–5 s) and light punch-ins.
  - Shorts: 30–60 s, captions mid-frame, a one-line lesson hook. Minimal B-roll and SFX.

### Think School (Indian business case studies)
- Co-founder Ganesh Prasad describes videos as "built in layers: script, research, edits, feedback, revisions". The post title frames the goal as "Netflix-level quality". [3RD-PARTY snippet, LinkedIn: https://www.linkedin.com/posts/ganeshprasad1997_ive-always-believed-think-school-should-activity-7362716956929540097-Cwxe]
- Founded in 2019 by Ganesh Prasad and Parsh Kothari. [3RD-PARTY: https://www.rotoris.com/friends-and-partners/ganesh-prasad-sridharan]
- **Observed, unmeasured:**
  - Presenter in front of a dark studio backdrop, intercut with dense **2D/3D motion graphics**: company logos, charts, timelines, maps, newspaper clippings, stock footage.
  - Chapter-card structure ("Chapter 1: …"). Cinematic, dark, high-contrast grade with brand-yellow and red accents.
  - Dramatic score and risers. ASL about 2–4 s in graphic sections. Runs 15–30 min.
  - Hook: a striking business paradox in the first 30 s.

### Raj Shamani (Shorts and podcast clips)
- **[OBSERVED, UNMEASURED]** No reliable published breakdown was found.
  - Clips from the multicam "Figuring Out" podcast. Hinglish.
  - Strong headline text bar at the top of the safe zone, plus word-level captions in the lower-middle (white or yellow highlight).
  - Fast removal of pauses, and cuts between guest and host angles on every speaker change.
  - Cinematic warm grade on a dark set. Subtle music under clips. Hook is the most shocking guest line, placed first.

### Tanmay Bhat
- **[OBSERVED, UNMEASURED]**
  - Casual, conversational talking head or stream-style setup. English and Hinglish with comedic timing.
  - Meme and reaction cutaways, zoom-in-on-punchline jumps, meme SFX.
  - Lower production polish by design. Shorts are often reaction or commentary clips with simple bold captions.

### Public editing style guides and SOPs
- **MrBeast production handbook:** the only widely available real internal guide (see above). It is about structure and retention, not fonts or LUTs. https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/
- **Johnny Harris map tutorial:** his own YouTube video (December 2020) on GEOlayers maps. A summary is at https://glasp.co/youtube/GsojLuJpe_0
- **Vendor-reverse-engineered "style sheets"** with fonts, cut rates and caption specs for Hormozi, Leila Hormozi, Ali Abdaal, Codie Sanchez and Tom Noske: https://www.choppity.com/tools/recreate-video-editing-style/ (useful presets; vendor-biased)
- No public editing SOP was found for Ali Abdaal, Kurzgesagt, Vox, MKBHD or the Indian creators. Kurzgesagt has said it does not publish behind-the-scenes material. [3RD-PARTY]

### Style preset summary for the skill

| Preset | ASL (s) | Cuts/min | Punch-ins | Captions | B-roll share | Grade | SFX/music | Evidence |
|---|---|---|---|---|---|---|---|---|
| Hormozi Shorts | 1–3 | 20–60 | Frequent 10–20% | Montserrat Black caps, white + black stroke, yellow active word, 2–4 words | Low | Dark, crushed blacks | Low music, no transition SFX | Vendor analysis |
| MrBeast (2022 style) | ~1.6 | ~38 | Frequent | Key moments only | High | Bright, saturated | Heavy SFX | 1-min sample |
| MrBeast (2024+ style) | ~2.6 | ~23 | Fewer | Key moments only | High | Bright | Moderate | 1-min sample |
| Ali Abdaal Shorts | 2–5 | 12–30 | Mild | Phrase reveal, yellow key words | Low–medium | Desaturated + yellow pop | Lo-fi | Vendor analysis |
| Ali Abdaal long-form | ~3–5 | 12–20 | Mild | Pop-up text cards | Medium (~8 h/video of B-roll work) | Warm, bright | Light | Adobe hours; style observed |
| Johnny Harris / Vox / Dhruv | 3–5 | 12–20 | Rare | Labels, highlighter | Very high | Paper textures, grain | Score + paper SFX | Tutorials; observed |
| Kurzgesagt | Continuous motion | n/a | n/a | Minimal | 100% animation | Neon on navy | Full score | Observed |
| MKBHD | 4–8 | 8–15 | Rare | Minimal lower-thirds | ~50% product B-roll | Clean dark, red accent | Ambient | Observed |
| Dan Koe | 5–15 | 4–12 | None | Sparse, sentence case | Low | Moody, desaturated | Ambient | Observed |
| Ryan Trahan | 2–5 (alternating) | varies | Some | Playful text, counters | High (vlog) | Natural | Whimsical score | Blackman analysis; observed |

---

## PART D: Retention-backed principles (evidence vs opinion)

### D1. Documented by YouTube [OFFICIAL]
- **Intro metric = % of viewers still watching after the first 30 s.** To improve it, YouTube says to make the thumbnail and title "better reflect your video content" and to "modify the first 30 seconds… experiment with different styles". [https://support.google.com/youtube/answer/9314415?hl=en]
- **Top moments:** "If the top moments are occurring in a later portion in the video, consider introducing the compelling content earlier in the video. Audience sizes typically decrease over the length of the video." [same source]
- **Spikes** mean rewatches or shares, or confusing content that viewers had to rewatch. **Dips** mean skipped or abandoned segments. Key moments need a video of at least 60 s with at least 100 views. [same source]
- **End screens:** can occupy the **last 5–20 s**. The video must be at least **25 s** long. Up to **4 elements** at 16:9. Not available on made-for-kids videos. [https://support.google.com/youtube/answer/6388789?hl=en]
- **Chapters:** the first timestamp is **00:00**, with **at least 3** timestamps in ascending order and each chapter **at least 10 s**. Manual chapters override automatic ones. [https://support.google.com/youtube/answer/9884579?hl=en]
- **Shorts:** up to 3 min. A Short over 1 min with a Content ID claim is blocked. [https://support.google.com/youtube/answer/15424877?hl=en]
- **Google ABCD framework (ads):** Attract, Brand, Connect, Direct. Ads following it showed a **30% lift in short-term sales likelihood** and a 17% lift in long-term brand contribution (Google/Kantar, 2021). This is evidence about ads, not organic videos. [https://business.google.com/us/think/future-of-marketing/creative-best-practices-youtube-ads/]

### D2. Practitioner evidence (internal data, not peer-reviewed)
- **MrBeast handbook** (internal analytics described by the creator): the biggest drop is in the first minute. Matching the title and thumbnail promise and good opening lighting reduce drop-off. Re-engagement spikes at about 3:00 and 6:00. Never signal the end before the payoff.
- **MrBeast 2024:** slower pacing (38 to 23 cuts per minute in sampled minutes) coincided with higher views. Correlation only; Tubefilter notes many confounders. [https://tubefilter.com/2024/03/04/mrbeast-editing-style-number-of-cuts-per-video/]
- **Third-party benchmark dataset:** Retention Rabbit's 2025 report (10,000+ videos, vendor data, methodology not public) claims:
  - Average retention 23.7%, with about 55% of viewers lost in the first 60 s.
  - Only 16.8% of videos exceed 50% retention.
  - Only about 16% of viewers reach the final 10 s.
  - First-minute retention over 65% correlates with 58% higher AVD.
  - Sources: https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report, summarised at https://research.stripo.email/youtube-benchmarks
  - **[3RD-PARTY, treat as directional]**
  - YouTube itself publishes no niche or length averages and advises comparing against your own recent videos. [https://prepublish.ai/blog/youtube-retention-benchmarks-2026]

### D3. Widely shared opinion (no public data; label as such)
- **Hooks:**
  - Shorts: first **1–3 s**, opening mid-action with no logo or fade-in.
  - Long-form: confirm the click in the first 5–15 s, then deliver within 30 s. [3RD-PARTY or opinion: https://www.teleprompter.com/blog/how-long-should-a-youtube-intro-be]
  - Paddy Galloway emphasises packaging and the "glance test" for thumbnails, with short thumbnail text. [3RD-PARTY interview summary: https://videohighlight.com/v/UHhTKwclHCs]
  - I found no written Galloway or Film Booth retention study. Their advice should be cited as opinion.
- **Intro length:** no branded intro, or a sting under 3 s. Cold open first. This is consistent with YouTube's "first 30 s" metric and the MrBeast memo.
- **Re-hooks:** a pattern interrupt every 30–90 s in long-form (B-roll change, graphic, SFX, location change, new question). The MrBeast memo plans major re-engagements at about 3 and 6 min. A "re-hook every 3–5 s" for Shorts is folklore. [UNVERIFIED]
- **Payoff timing:** pay off the thumbnail promise early enough to prevent the click-regret dip (MrBeast: show, don't tell, after minute 1). Hold the biggest payoff for the end, without signalling "the end".
- **End screen, last 20 s:**
  - Keep content running under the end screen.
  - Avoid "that's it for today" or "thanks for watching" verbal outros, which trigger exits.
  - Point to **one specific next video** with a reason to watch it.
  - Based on the MrBeast memo plus common practice. [OPINION]
- **Chapters:** they help skimmers and search, but some creators believe they increase skipping. No public data either way. [UNVERIFIED]
- **Shorts loop endings:**
  - Make the last line or frame flow into the first: an incomplete sentence completed by the opening, or a matching visual.
  - Since 2025-03-31 replays count as views, and APV can exceed 100% with loops. [3RD-PARTY: https://coschedule.com/social-media-marketing/youtube-metrics]
  - Whether loops boost distribution is unproven. [OPINION]
- **Storytelling devices with analyst support:**
  - Instant context, constrained goals as curiosity loops, visual progress trackers, recurring motifs.
  - Alternating fast and calm pacing (not constant motion). Three acts. Cliffhanger endings.
  - Source: Blackman on Ryan Trahan, https://georgeblackman.substack.com/p/13-unexpectedly-effective-youtube

### D4. Translating this into skill rules (recommended defaults)
1. **Shorts:** no intro, with the hook line plus on-screen hook text in frame 1. Captions from frame 1 inside the safe box. Something new about every 1.5–3 s (cut, zoom, graphic). Loop-friendly last line. Target 20–45 s unless the story needs more. Keep any third-party music claim-free if the Short is over 60 s.
2. **Long-form:** cold open of 15–45 s that restates the title and thumbnail promise and shows the "proof" visual. No logo sting over 3 s. Plan re-engagements at about 1:00, 3:00 and 6:00 and every 2–3 min after (adapted from MrBeast). Chapters with 00:00, 3+ chapters of at least 10 s each. End screen in the final 5–20 s with content still playing.
3. **Analytics loop:** after publishing, read the Intro % (30 s), dips and spikes from Studio. Feed the timestamps back into the edit notes for the next video.

---

## Source-confidence summary
- **Confirmed from official pages this session:**
  - YouTube encoding, HDR, Shorts, thumbnails, captions, end screens, chapters and key moments.
  - Instagram aspect, frame rate and resolution. Meta Reels ad specs and safe-zone percentages.
  - TikTok In-Feed ad specs and TikTok Studio upload limits.
  - X length and file-size limits.
  - ffmpeg AV1 wiki.
- **Official but excerpt-only:**
  - Instagram 20-min and 3-min recommendation rule. TikTok 10/60-min. LinkedIn sizes and durations. X API codec recommendations.
- **Not confirmable from official sources:**
  - Platform LUFS targets. Pixel-exact safe zones for TikTok and Shorts (official ones exist only as images or templates).
  - The 4K-upload quality boost. LinkedIn's 15-min member limit.
  - Most creator style numbers apart from those cited.


# ===== FILE: references/design-science.md =====

# Design Science for AI Video Editing & Motion Graphics

Contents: 0. Ten-line cheat sheet (apply by default) · 1. Typography for Video & Motion · 2. Curated Font Library for Video (48 fonts) · 3. Color · 4. Motion Design Principles · 5. Editing Grammar & Attention Psychology · 6. Sound Design Psychology · 7. Anti-"AI Slop" Visual Tells (and what to do instead) · 8. Machine-Readable Defaults (for the skill's config) · 9. Source List

A rules-first knowledge base for an agent that edits YouTube long-form and Shorts/Reels/TikTok and generates HTML/CSS/GSAP motion graphics rendered to video.

Conventions used throughout:

- **RULE** = a numeric default the agent should apply unless the brief says otherwise.
- **WHY** = one-line rationale.
- **SRC** = source key; full URLs are in the Source List at the end (section 9).
- **Evidence labels** (for psychology/perception claims):
  - **[STRONG]**: replicated experimental research or formal standards.
  - **[MODERATE]**: some peer-reviewed support, small samples, or boundary conditions.
  - **[INDUSTRY]**: a platform or vendor's own data or guidance. It is authoritative for that platform but often self-interested and unreplicated.
  - **[FOLK]**: craft convention or practitioner wisdom. It's useful as a default but has no controlled evidence behind it.
  - **[MYTH]**: widely repeated, and the evidence contradicts it.
- Pixel values assume **1920x1080 (16:9)** or **1080x1920 (9:16)** unless stated. For 4K (3840x2160), multiply px by 2. Express sizes in % of frame height (`%H`) when you can, so they scale.

---

## 0. Ten-line cheat sheet (apply by default)

1. Body/caption text: **≥ 4.5%H on 16:9** (≈ 48px at 1080p); **≥ 6%H** if the main audience watches on phones. Burned-in Shorts captions: **≥ 60px at 1080 wide**, typically 64-90px bold.
2. Caption limits: **≤ 42 chars/line, ≤ 2 lines** for 16:9. For 9:16: **≤ 20 chars/line, 1-2 lines, 1-5 words per chunk**. Reading speed: **≤ 17 cps** comfortable, **20 cps** hard ceiling.
3. Graphics safe area on 16:9: **5% inset** (96px left/right, 54px top/bottom at 1080p). On 9:16, keep everything in **x 80-900, y 250-1440** (the "universal" rectangle).
4. Text on footage must have a **luminance** separation device: a 2-4px stroke, or a soft shadow (0 2px 8-12px at 60-70% black), or a scrim (bottom 35% gradient to 70% black). Never rely on hue alone, because 4:2:0 chroma subsampling smears it.
5. **Max 2 typefaces** (one display, one text/mono) and **max 3 weights** in one video. Use **one accent color**.
6. Motion durations: small UI-scale **150-250ms**; medium moves **300-450ms**; full-frame transitions **450-700ms**. Exits run **~15-25% faster** than entrances.
7. Default ease-in for entrances: `cubic-bezier(0.05, 0.7, 0.1, 1)` (M3 emphasized decelerate). For exits: `cubic-bezier(0.3, 0, 0.8, 0.15)`. For on-screen moves: `cubic-bezier(0.2, 0, 0, 1)`.
8. **One hero moves at a time.** Stagger groups at **40-80ms per item**, and keep the total stagger **≤ 600ms**.
9. Loudness: deliver **-14 LUFS integrated, ≤ -1 dBTP** for YouTube, Shorts, Reels and TikTok. Keep the music bed **≥ 10-15 LU below the voice** while someone is speaking.
10. Never flash more than **3 times per second** (WCAG 2.3.1). Avoid full-frame saturated red flashes entirely.

---

## 1. Typography for Video & Motion

### 1.1 Minimum on-screen text size

The physics behind this: reading is fluent when the **x-height subtends about 0.2° to 2°** of visual angle (Legge & Bigelow 2011) **[STRONG]**. Below about 0.2°, reading speed collapses. A 16:9 video watched on a portrait phone is only about 3.9cm tall. At 35cm viewing distance, 0.2° is about 1.2mm, which is ~3.1% of the frame height. So small text in long-form is unreadable on phones unless the viewer rotates to landscape.

| Context | Minimum font size (cap-to-descender em) | Comfortable | Notes |
|---|---|---|---|
| 16:9 viewed on TV/desktop | 3.5%H (38px @1080) | 4.5-6%H (48-65px) | Labels and lower thirds for secondary info |
| 16:9 long-form, mixed devices (YouTube default) | **4.5%H (48px)** | 5.5-7%H (60-75px) | ~63% of YouTube watch time is mobile (YouTube statements); design for landscape phone |
| 16:9 subtitle/caption line | BBC: **line height 7-8% of active height** (≈ 76-86px line → ~64-72px font at 120% leading) | same | SRC: BBC-SUB |
| 9:16 Shorts/Reels/TikTok captions | BBC: **line height 3.9-4.5% of height** (≈ 75-86px → ~62-72px font) | 70-100px bold for "viral" style | SRC: BBC-SUB |
| 9:16 headline / hook text | 5-7% of height (96-135px) | | Fit ≤ 3 lines of ≤ 14 chars |
| Absolute floor anywhere | **28px @1080** (2.6%H) | n/a | Below this, 4:2:0 compression and phone downscaling destroy the glyphs |

- **RULE:** at 4K, use the same %H; don't keep the 1080 px values. **WHY:** viewers see relative size, not pixels.
- **RULE:** text that **must** be read gets ≥ 4.5%H. Decorative or "spot readable" text (sources, timestamps) may go down to 2.6%H. **WHY:** this mirrors the APCA split between fluent-read and spot-read text. SRC: APCA.

### 1.2 Reading speed and on-screen duration

| Spec | Value | Evidence | SRC |
|---|---|---|---|
| Netflix English adult | **≤ 20 characters/second** | [INDUSTRY] | NETFLIX-TTSG |
| Netflix children's | **≤ 17 cps** | [INDUSTRY] | NETFLIX-TTSG |
| BBC | **160-180 words/minute**; min duration ≈ **0.3s per word** (4 words → 1.2s) | [INDUSTRY] | BBC-SUB |
| Eye-tracking research | Viewers *can* keep up at 12, 16 and 20 cps. Slow subtitles cause re-reading and **less** enjoyment | [MODERATE] (n=74) | SZARKOWSKA-2018 |
| Average adult silent reading (paper/screen, not video) | 238 wpm non-fiction (range 175-300) | [STRONG] meta-analysis of 190 studies | BRYSBAERT-2019 |
| TikTok ads guidance | "5-10 words per second" of text | [INDUSTRY], and it conflicts with reading research: 5 wps is 300 wpm. Treat it as the upper bound for *1-3-word punch text only* | TIKTOK-CBP |

RULES:
- **On-screen text display time (s) = max(1.0, words × 0.3) + 0.3s** of hold after the animate-in finishes. **WHY:** BBC's 0.3s/word plus a settle buffer.
- **Captions synced to speech:** follow the speech, but keep ≤ 20 cps. If the speaker is faster (> 180 wpm), condense the wording; don't flash 4 frames of text.
- **Text competing with narration** (callouts the viewer must read while also listening): **≤ 12-15 cps, ≤ 7 words per card**. **WHY:** reading and listening share verbal working memory, so split attention means less comprehension (Mayer redundancy, §5.6).
- **Minimum caption event:** 0.8s (≈ 24 frames at 30fps). **Gap between events:** ≥ 2 frames, or butt them directly. A 1-frame gap reads as flicker.
- **Shot changes:** BBC says start/end subtitles on the shot change where possible and avoid straddling a cut. If a caption straddles one, let it extend ≥ 12 frames past the cut. Don't end 1-5 frames after a cut (it looks like an error). SRC: BBC-SUB.

### 1.3 Line length

| Context | Chars per line | Lines |
|---|---|---|
| Netflix 16:9 subtitles | **42** | 2 max |
| BBC broadcast | **37** (BBC online: 68% of frame width for 16:9) | 2 max (3 for 9:16) |
| BBC 9:16 vertical | **90% of width** | **3 max** |
| Burned-in Shorts captions (craft) [FOLK] | **8-20** (1-5 words) | 1-2 |
| Body text in a motion graphic (explainer card) | 30-50 chars | ≤ 4 lines |
| Print/web body (Butterick) | 45-90 | n/a |

- **RULE:** break lines at linguistic boundaries (after punctuation, before conjunctions or prepositions). Never split an article from its noun or a name across lines. When two lines are uneven, prefer a **bottom-heavy pyramid**. SRC: BBC-SUB, NETFLIX-TTSG.

### 1.4 Safe areas

**16:9 broadcast/YouTube (SMPTE ST 2046-1 = EBU R95):**

| Area | Inset per side | 1920x1080 inset | Rect |
|---|---|---|---|
| Action safe | 3.5% | 67px H, 38px V | 1786x1004 |
| Graphics/title safe | **5%** | **96px H, 54px V** | 1728x972 |
| Legacy 4:3 title safe (old SD) | 10% | n/a | Only for 4:3 center-cut protection |

- **RULE:** put all text and logos inside the 5% title-safe area. **WHY:** it's the broadcast standard, and it also clears rounded phone corners and the YouTube player chrome. SRC: EBU-R95, SMPTE-2046.
- **RULE (YouTube long-form):** keep the **bottom 12%** (≈ 130px) free of critical text. **WHY:** the progress bar and controls cover it on hover/pause, and auto-captions render there. [FOLK, observed]
- **RULE:** place lower-thirds with the baseline at **~80-85%H**, left-aligned to the title-safe edge.

**9:16 platform UI overlays.** Measured from 1080x1920. **None of the platforms publish official organic pixel specs.** These are consolidated third-party measurements [FOLK/measured], and sources disagree by ±100px:

| Platform | Top unsafe | Bottom unsafe | Right unsafe | Left unsafe | Notes |
|---|---|---|---|---|---|
| TikTok | 130-260px (tabs, search) | **370-480px** organic; up to ~700px in ads | **120-190px** (like/comment/share rail); up to ~240px in ads | 40-60px | Caption length expands the bottom zone |
| Instagram Reels | 110-270px | **320-480px** (caption, audio, CTA) | 120-140px | 60px | Meta specifies ad safe zones as percentages (~14% top, ~35% bottom for Stories/Reels ads) |
| YouTube Shorts | ~120px | **300-400px** (title, channel, expanded description) | ~96-150px | ~48px | Expanded description grows the bottom zone |

- **RULE: "universal 9:16 safe rectangle" = x 80-900, y 250-1440** (820x1190). Everything that must be read goes in here. **WHY:** it's the intersection of the most conservative measurements across the three platforms.
- **RULE:** put Shorts captions with their **center at y ≈ 1050-1300** (55-68% of height). That's below the face and above the UI. Keep the speaker's eyes at **y ≈ 600-760** (upper third).
- **RULE:** for ads, re-check the platform's current downloadable overlay template. Ad UI is larger than organic UI.

### 1.5 Font pairing, weight, tracking, leading

| Topic | RULE | WHY | SRC |
|---|---|---|---|
| Number of families | **≤ 2** per video (display + text). A mono may be a 3rd *only* for code or data | Each family adds a "voice". Mixing 3+ reads as amateur | BUTTERICK |
| Pairing logic | Contrast **one** axis (serif vs. sans, *or* width, *or* weight) and match **x-height and proportions** | Too-similar pairs look like a mistake; too-different pairs clash | BUTTERICK, GOOGLE-FONTS-KNOWLEDGE |
| Weight contrast | Headline vs. body weight differs by **≥ 300 units** (e.g. 800 vs. 400 or 700 vs. 400). Avoid 500 vs. 600 | Hierarchy must survive a 0.5s glance and compression | [FOLK] |
| Weights per video | **≤ 3** (e.g. 400, 600, 800) | Consistency | [FOLK] |
| All-caps tracking | **+5% to +12%** of font size (CSS `letter-spacing: 0.05em-0.12em`). Use the higher end for small sizes | Caps are spaced for mixing with lowercase; set alone, they're too tight | BUTTERICK |
| Large display tracking | **-1% to -3%** (`-0.01em` to `-0.03em`) above ~100px for grotesks | Default spacing is tuned for text sizes; it looks loose when large | [FOLK]; Inter's dynamic metrics follow this |
| Body/caption leading | **120-145%** (Butterick); BBC uses **120%** for subtitles | Readability | BUTTERICK, BBC-SUB |
| Display leading | **0.9-1.1** (90-110%) for 2-3 line headlines. Use 1.0-1.15 if the font has tall ascenders or diacritics | Tight leading groups the lines visually | [FOLK] |
| Optical sizes | Use the `opsz` axis when it exists (Inter, Roboto Flex, Fraunces, Newsreader, Source Serif 4, DM Sans, Bricolage Grotesque). Set `font-optical-sizing: auto`, or force opsz ≈ 32-72 for display | Display cuts have tighter spacing and finer detail; text cuts are sturdier at small sizes | GOOGLE-FONTS-KNOWLEDGE |
| Case | Captions in sentence case by default. Use ALL CAPS only for ≤ 4-word punch text | All-caps slows reading of longer strings (word-shape loss) [MODERATE] | BUTTERICK |

### 1.6 Legibility on phones and after compression

- **Why geometric/grotesque sans (Inter, Manrope, Montserrat-class) read well on mobile video:** they have large x-heights (≥ 0.52 em), open apertures, uniform stroke weight with no hairlines to lose, and simple shapes that survive 4:2:0 chroma subsampling and macroblocking. [MODERATE]: aperture and x-height effects on small-size legibility are well documented in typeface legibility research (e.g. Legge & Bigelow 2011; Beier's legibility work). The "rounded fonts feel friendly" association is [FOLK].
- **RULE: thin weights.** No weight < 400 below 60px at 1080p. No weight < 300 at any size unless it's ≥ 120px and on a flat, non-moving background. **WHY:** strokes < 2px are below the 4:2:0 chroma resolution (chroma is half-res, so effectively 2px blocks). They shimmer as the encoder re-quantizes them each frame.
- **RULE: stroke width floor.** Minimum stem width ≈ **3px at 1080p** (6px at 4K) for anything that must be read.
- **RULE: hairline serifs.** Didone (Bodoni, Playfair Display) hairlines break below ~72px at 1080p. Use them for ≥ 90px headlines only.
- **RULE: color text.** Saturated red, blue or magenta text **on** a saturated contrasting hue smears because chroma is half-resolution. Text needs a **luminance difference**: WCAG ≥ 4.5:1, or APCA |Lc| ≥ 60, and Lc ≥ 75 for captions. SRC: YT-ENC (4:2:0), APCA.

### 1.7 Text over footage (values that survive YouTube re-encoding)

YouTube re-encodes everything (VP9/AV1, 4:2:0, 8-bit SDR BT.709). The recommended upload is 8 Mbps at 1080p SDR, but delivery bitrates are far lower. SRC: YT-ENC.

| Technique | 1080p values | 4K values | When |
|---|---|---|---|
| **Outline/stroke** | 2-4px (≈ 3-6% of font size), black at 85-100% opacity. Use `paint-order: stroke fill` so the stroke doesn't eat the glyph | 4-8px | Busy footage, viral captions |
| **Soft drop shadow** | `0 2px 10px rgba(0,0,0,.65)` + `0 0 2px rgba(0,0,0,.6)` (a tight contact shadow plus a wide halo) | double the px | Default for clean, premium looks |
| **Hard offset shadow** | 4-6px offset, 0 blur, 100% black or brand dark | 8-12px | Bold/playful styles |
| **Scrim (gradient)** | Bottom 30-40% of frame: `linear-gradient(to top, rgba(0,0,0,.70) 0%, rgba(0,0,0,0) 100%)`. Top scrims: 20-25% at ≤ 55% | same % | Lower-thirds, documentary |
| **Box/plate** | Background rgba(0,0,0,0.6-0.8), padding 0.25em vertical × 0.5em horizontal, radius 0-0.2em | same em | Accessibility-grade captions (BBC/Netflix style) |
| **Local blur** | `backdrop-filter: blur(16-24px)` + 30-40% dark tint | 32-48px | Sparingly. Glass is an AI-slop tell when overused (§7) |

- **RULE:** don't use stroke widths < 2px at 1080p. **WHY:** the encoder blurs them into a gray halo.
- **RULE:** avoid 1px lines, fine textures, and single-pixel dividers in motion. Use ≥ 2px. **WHY:** they twinkle (temporal aliasing) as they move across macroblocks.
- **RULE:** for moving text, round the final resting positions to whole pixels and avoid sub-pixel "settle" drift. **WHY:** it prevents shimmer.

---

## 2. Curated Font Library for Video (48 fonts)

Licenses:

- **OFL** = SIL Open Font License, via Google Fonts. Free for commercial use, embedding and redistribution (not for sale on its own).
- **FFL** = ITF Free Font License, via Fontshare. Free for personal and commercial use, including broadcast. **No redistribution**: don't commit the files into a public skill repo. Download them from fontshare.com at setup instead, and verify the current terms before shipping. SRC: FONTSHARE.
- **RULE for the skill:** bundle OFL fonts. Fetch FFL fonts at runtime from Fontshare's API/CDN.

Weight notation: the recommended weights to load (others are optional).

### 2.1 Premium / Editorial
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| Instrument Serif | Google/OFL | 400, 400 italic | Inter or Instrument Sans | Condensed editorial serif. Display only (≥ 72px) |
| Fraunces | Google/OFL (opsz, SOFT, WONK) | 300-700 | Inter / Manrope | Use opsz 72-144 for display; "wonky" adds character |
| Newsreader | Google/OFL (opsz) | 400, 600 | Inter | Serious, journalistic |
| Playfair Display | Google/OFL | 600-800 | Source Sans 3 / Inter | Didone, ≥ 90px only. Overused, so use with restraint |
| DM Serif Display | Google/OFL | 400 | DM Sans | High contrast, warm |
| Gambetta | Fontshare/FFL | 400-700 | Satoshi | Modern editorial serif |
| Zodiak | Fontshare/FFL | 400-800 | General Sans | Expressive serif with display cuts |
| Source Serif 4 | Google/OFL (opsz) | 400, 600 | Source Sans 3 | Sturdy at small sizes |

### 2.2 Tech / Product / SaaS
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| Inter (v4, opsz) | Google/OFL | 400, 600, 800 | JetBrains Mono / Fraunces | Workhorse with a large x-height. Default for UI recreations |
| Geist | Google/OFL (Vercel) | 400, 600, 700 | Geist Mono | Crisp, contemporary dev-tool feel |
| Manrope | Google/OFL | 400, 700, 800 | IBM Plex Mono | Geometric-grotesk hybrid, very mobile-legible |
| Space Grotesk | Google/OFL | 400, 700 | Space Mono | Quirky tech. Overused in AI/crypto, so be careful |
| Satoshi | Fontshare/FFL | 400, 700, 900 | Gambetta / JetBrains Mono | Premium startup look |
| General Sans | Fontshare/FFL | 400, 600 | Zodiak | Neutral, modern |
| Switzer | Fontshare/FFL | 400-800 | Erode | Swiss-neutral, Helvetica alternative |
| IBM Plex Sans | Google/OFL | 400, 600 | IBM Plex Mono / Plex Serif | Corporate-technical, superfamily |

### 2.3 Friendly / Approachable / Education
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| DM Sans (opsz) | Google/OFL | 400, 700 | DM Serif Display | Soft geometric |
| Plus Jakarta Sans | Google/OFL | 500, 800 | Fraunces | Warm, rounded terminals |
| Nunito | Google/OFL | 600, 800 | Nunito Sans | Rounded terminals. Kids/edu |
| Figtree | Google/OFL | 500, 700 | Newsreader | Clean, friendly, highly legible |
| Outfit | Google/OFL | 400, 700 | Inter | Geometric, simple |
| Rubik | Google/OFL | 500, 800 | Rubik only | Slightly rounded corners. Works for numbers and data |

### 2.4 Bold / Viral captions (Shorts, Reels, TikTok)
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| Montserrat | Google/OFL | 800, 900 | Inter | The "Hormozi-style" caption default. Overused, so differentiate with color and animation |
| Poppins | Google/OFL | 700, 800 | n/a | Geometric, round dots |
| Anton | Google/OFL | 400 | Inter | Condensed impact-style, all-caps hooks |
| Bebas Neue | Google/OFL | 400 | Montserrat 500 | Caps-only. Track +4-6% |
| Archivo / Archivo Black | Google/OFL (wdth axis) | 800-900, wdth 100-125 | Archivo 400 | Width axis is great for kinetic type |
| Lilita One | Google/OFL | 400 | Nunito | Chunky, playful-bold |
| Clash Display | Fontshare/FFL | 600, 700 | Satoshi | Premium-bold hooks |
| Cabinet Grotesk | Fontshare/FFL | 800, 900 | Satoshi | Punchy, quirky grotesk |
| Tanker | Fontshare/FFL | 400 | General Sans | Ultra-heavy condensed display |

### 2.5 Documentary / Journalistic / Serious
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| Barlow Condensed | Google/OFL | 500, 700 | Barlow | Lower-thirds, data labels |
| Oswald | Google/OFL | 500, 700 | Source Serif 4 | Classic doc titles |
| Big Shoulders Display | Google/OFL | 700, 900 | Inter | Industrial, Chicago-signage feel |
| Libre Franklin | Google/OFL | 400, 700 | Libre Caslon | Newspaper sans |
| Libre Caslon Text/Display | Google/OFL | 400, 700 | Libre Franklin | Historical, literary |
| Familjen Grotesk | Google/OFL | 400, 700 | Newsreader | Contemporary documentary grotesk |

### 2.6 Luxury / Fashion
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| Cormorant Garamond | Google/OFL | 500, 600 | Inter 300 tracked caps | Display ≥ 80px only (fine hairlines) |
| Bodoni Moda (opsz) | Google/OFL | 500-700 | Jost | Use opsz high for display |
| Jost | Google/OFL | 300, 400 caps | Bodoni Moda | Futura-like. Wide-tracked caps (+15-20%) |
| Boska | Fontshare/FFL | 400-700 | Switzer | Contemporary high-contrast serif |
| Melodrama | Fontshare/FFL | 400-600 | General Sans | Dramatic Didone-ish display |

### 2.7 Playful / Creator / Handmade
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| Fredoka | Google/OFL | 500, 700 | Nunito | Rounded, bubbly |
| Baloo 2 | Google/OFL | 600, 800 | Nunito | Rounded, multilingual (Indic) |
| Bricolage Grotesque (opsz, wdth) | Google/OFL | 500, 800 | Inter | Quirky ink-trap display. Trendy |
| Unbounded | Google/OFL | 600, 900 | Inter | Wide, Y2K-ish |
| Chillax | Fontshare/FFL | 500, 700 | Satoshi | Soft, playful geometric |
| Caveat | Google/OFL | 600 | Inter | Handwritten annotations/arrows only. Never body text |
| Permanent Marker | Google/OFL | 400 | Inter | Marker callouts, sparingly |

### 2.8 Code / Data / Mono
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| JetBrains Mono | Google/OFL | 400, 700 | Inter | Best mono for code-on-screen, with ligatures |
| Geist Mono | Google/OFL | 400, 600 | Geist | |
| IBM Plex Mono | Google/OFL | 400, 600 | IBM Plex Sans | |
| Space Mono | Google/OFL | 400, 700 | Space Grotesk | Retro-tech |
| Fira Code | Google/OFL | 400, 600 | Fira Sans | Ligatures |

- **RULE:** use **tabular numerals** (`font-variant-numeric: tabular-nums`) for any animated counters, timers or price tickers. **WHY:** proportional digits make the number jitter sideways while counting.
- **RULE:** when a creator has no brand fonts, default to **Inter + JetBrains Mono** (tech), **Fraunces + Inter** (premium), or **Montserrat 800 + Inter** (viral). Rotate the choice to avoid sameness across a channel's videos only if the brief asks for it. Consistency within a channel beats novelty.

---

## 3. Color

### 3.1 Color psychology: honest evidence ratings

| Claim | Rating | Use it as |
|---|---|---|
| Color/luminance **contrast and salience** drive attention: a unique color among neutrals "pops out" pre-attentively | **[STRONG]** (visual search research; Treisman feature integration) | The basis for one-accent discipline |
| Specific hue → specific emotion ("blue = trust", "red = urgency/appetite") | **[FOLK]/[MODERATE at best]**: effects are small, context-dependent and culturally variable | Brand convention, not a law |
| "Red impairs achievement/test performance" (Elliot et al. 2007) | **[MYTH-ish]**: repeated failed replications (Gnambs 2020 and others), and a 2020 *Psychonomic Bulletin & Review* review casts doubt | Don't cite it |
| Red increases perceived attractiveness or dominance | **[MODERATE→WEAK]**: mixed replications | Don't rely on it |
| Warm, saturated colors raise arousal; desaturated/cool feels calmer | **[MODERATE]** | Mood grading, music-video energy |
| Color meaning is culture-dependent (white = mourning in parts of East Asia; red = luck in China) | **[STRONG]** | Localization check |
| Elliot & Maier's (2014) color-in-context theory | Theory review [MODERATE]. Note its own predictions have replicated poorly | Background reading |

SRC: ELLIOT-MAIER-2014, GNAMBS-2020, PBR-2020-COLOR.

### 3.2 Contrast requirements

| Standard | Requirement | SRC |
|---|---|---|
| WCAG 2.x AA, normal text | **4.5:1** | WCAG |
| WCAG 2.x AA, large text (≥ 24px regular / ≥ 18.66px bold, CSS px) | **3:1** | WCAG |
| WCAG 2.x AAA | 7:1 (normal), 4.5:1 (large) | WCAG |
| WCAG non-text (icons, chart strokes) | **3:1** | WCAG 1.4.11 |
| APCA **Lc 90** | Preferred for body/fluent reading | APCA |
| APCA **Lc 75** | Minimum for body text (e.g. ≥ 18px/400, 16px/500, 14px/700). **Use as the caption minimum** | APCA |
| APCA **Lc 60** | Minimum for "content text you want read" (≥ 24px/400 or 16px/700) | APCA |
| APCA **Lc 45** | Minimum for large/heavy headlines (≥ 36px/400 or 24px/700) and fine icons | APCA |
| APCA **Lc 30** | Absolute minimum for spot-read text and solid icons | APCA |
| APCA **Lc 15** | Below this, treat the element as invisible | APCA |

- **RULE:** check text contrast **against the actual pixels behind it** (sample a 3x3 region at each glyph's position over the clip's duration), not against an assumed background. If any frame fails, add a stroke, shadow or scrim (§1.7).
- **RULE:** APCA is better suited than WCAG 2 contrast ratios for light-on-dark text, which is common in video. Use APCA Lc for dark-mode/dark-footage text, and WCAG 4.5:1 as the legal floor.

### 3.3 Palette discipline

- **60-30-10 rule:** 60% dominant (background/neutral), 30% secondary (surfaces, footage), 10% accent. **[FOLK]**: it comes from interior design and has no experimental basis, but it's a good default that enforces hierarchy.
- **RULE: one accent.** Exactly **one** saturated accent hue per video. It marks "the important thing" (keyword highlight, the active chart bar, CTA). A second accent is allowed only for semantic pairs (good/bad, before/after). **WHY:** pop-out works only when the accent is rare [STRONG].
- **RULE: accent coverage ≤ 10%** of the frame area at any moment.
- **RULE: neutrals aren't pure.** Use tinted near-blacks (e.g. `#0E0F12`) and near-whites (`#F5F3EE`) rather than #000/#FFF for graphics plates. Pure #FFFFFF text is fine for captions (it's what Netflix and BBC use).
- **RULE: building palettes from footage.**
  1. Sample 5-8 keyframes, run k-means (k=5) in OKLab, and drop clusters < 3% area.
  2. The dominant scene hue becomes the base neutral tint.
  3. Pick the accent by rotating **150-210° in OKLCH hue** (complementary) from the dominant hue, *or* use the brand color.
  4. **Keep the accent hue at least 25-30° away from the skin-tone hue (~ 20-50° in OKLCH/HSL orange)**, so highlights don't blend with faces.
  5. Set accent lightness so APCA vs. the background is ≥ Lc 60.
- **RULE:** use **OKLCH/OKLab** for interpolation and gradient stops, not sRGB. **WHY:** sRGB midpoints go muddy or gray (e.g. blue→yellow passes through gray).

### 3.4 Color grading basics for talking heads

- **Skin tone line:** on a vectorscope, skin of all ethnicities clusters along one hue line (~10-11 o'clock, between red and yellow, often cited as ~123° on the scope). Ethnicity differs mostly in **saturation and luminance**, not hue. **RULE:** isolate skin and put its hue on the line ±5°. Deliberately stylized warm/cool looks may deviate. **[STRONG]** as a craft standard. SRC: ADOBE-SKIN, VAN-HURKMAN via JORDAN.
- **Exposure targets (Rec.709, 0-100 IRE) [FOLK/craft]:** lighter skin highlights at ~60-70 IRE, medium ~45-60, deep ~35-50. Specular highlights ≤ 95-100 (no clipped faces). Blacks 0-5 IRE, without crushing hair detail. Keep the face as the brightest *large* area in the frame. **WHY:** the eye goes to the brightest, highest-contrast region (and to faces, §5.9).
- **Order of operations:** (1) normalize: white balance plus exposure, (2) apply the input transform (log→Rec.709), (3) creative look, (4) secondary skin protect, (5) final output transform. **RULE:** never apply a creative LUT to footage of a different gamma than the LUT expects (e.g. an S-Log3 LUT on Rec.709). **RULE:** run creative LUTs at **40-80% opacity/mix** and re-check skin on the vectorscope afterward. **WHY:** LUTs are fixed transforms that clip and shift hue when the input is out of range.
- **Saturation:** keep skin saturation moderate. Over-saturated orange skin is the #1 amateur grading tell. Look for the skin trace extending less than about halfway to the 75% target box on a 75% vectorscope [FOLK].
- **Delivery:** SDR **BT.709**, 4:2:0, progressive, per YouTube's recommended upload settings. SRC: YT-ENC.

### 3.5 Gradients and banding after compression

- **Cause:** 8-bit delivery (256 levels per channel) plus encoder quantization flattens smooth ramps into visible contours. Re-encoding by the platform makes it worse.
- **RULES:**
  1. Render masters in **10-bit or 16-bit float** where possible (ProRes 422 HQ / 10-bit H.265). At minimum, the HTML→frames pipeline should render PNG-16 or float, not 8-bit JPEG.
  2. **Add noise/grain at the very end**, at **1-5% amplitude** (monochromatic, ~1px grain, animated per frame), to dither ramps. **WHY:** noise breaks up the contours. Too little gets quantized away; too much costs bitrate. Test on the *uploaded* video. SRC: PVC-BANDING.
  3. Avoid large, low-contrast, slow gradients (e.g. a full-frame #0B0B12→#151526 ramp). Use **wider luminance spans (≥ 8-10% L difference)**, or add texture.
  4. Dark gradients band worst (YouTube's quantization is coarse in the shadows). Lift deep backgrounds to ≥ ~ L 8-10% (OKLCH), or add grain.
  5. Upload at a higher bitrate than recommended (1080p at 12-16 Mbps, or 4K at 45+ Mbps). 4K uploads get a better codec and bitrate tier on YouTube even for 1080p viewers [FOLK/observed].

---

## 4. Motion Design Principles

### 4.1 Disney's 12 principles → UI and kinetic type

Source: Thomas & Johnston, *The Illusion of Life* (1981). SRC: DISNEY-12.

| Principle | Application to motion graphics / kinetic type | Default numbers |
|---|---|---|
| Squash & stretch | Scale a "landing" word to 1.0→1.06 (Y) / 0.96 (X) for ≤ 80ms on impact. Preserve area | Max ±8% distortion. Use for playful styles only |
| Anticipation | A small counter-move before the main move (e.g. pull back 4-8% of the travel distance, or scale to 0.96) | 60-120ms before the action |
| Staging | One clear idea per frame. Dim or blur everything else. **One hero moves at a time** | Non-hero opacity ≤ 40-60% during the hero move |
| Straight-ahead vs. pose-to-pose | Use pose-to-pose (keyframes) for all UI motion | n/a |
| Follow-through & overlapping action | Child elements (underline, icon, sub-label) arrive 40-100ms after the parent | Offset 40-100ms |
| Slow in / slow out | Never use linear easing for spatial moves (linear is fine for opacity cross-fades, rotation loops, scrolling tickers) | See §4.2 |
| Arcs | Large moves (> 25% of frame) travel on a slight arc, not a straight line | 5-15% path curvature |
| Secondary action | Subtle background drift (parallax 2-5% of frame over the shot) supports the main action | Must not compete in speed |
| Timing | Duration scales with distance and size (§4.3) | n/a |
| Exaggeration | Push key emphasis moments ~10-20% beyond "realistic" (scale pops to 1.1-1.15) | n/a |
| Solid drawing | Keep consistent perspective and light direction (shadows all cast from the same angle) | n/a |
| Appeal | Clean, simple shapes, consistent corner radii, intentional color | n/a |

**Anticipation → action → settle** (the core beat of any emphasis animation):

- Anticipation: 10-20% of total time, moving opposite to the action by 4-8% of the travel.
- Action: 50-70% of total time, with the fast part of a decelerating curve.
- Settle: 20-30% of total time, with an overshoot of 2-10% and back. Use **≤ 1 visible oscillation** for professional work and ≤ 2-3 for playful work.

### 4.2 Easing curves (exact values)

**Material Design 3 tokens** (verified from material-web token source, v0.192). SRC: M3-TOKENS.

| Token | cubic-bezier | Use |
|---|---|---|
| emphasized (CSS approximation; the true M3 emphasized is a 2-segment path) | `(0.2, 0, 0, 1)` | Hero on-screen moves and morphs |
| emphasized-decelerate | `(0.05, 0.7, 0.1, 1)` | **Entrances**: things arriving on screen |
| emphasized-accelerate | `(0.3, 0, 0.8, 0.15)` | **Exits**: things leaving permanently |
| standard | `(0.2, 0, 0, 1)` | Small utility moves |
| standard-decelerate | `(0, 0, 0, 1)` | Small entrances |
| standard-accelerate | `(0.3, 0, 1, 1)` | Small exits |
| legacy (Material 1/2 "standard") | `(0.4, 0, 0.2, 1)` | Neutral ease-in-out |
| legacy-decelerate / accelerate | `(0, 0, 0.2, 1)` / `(0.4, 0, 1, 1)` | n/a |
| M1 "sharp" | `(0.4, 0, 0.6, 1)` | Elements that may return at any time |

**IBM Carbon** (productive = efficient UI, expressive = big moments). SRC: CARBON-MOTION.

| | Productive | Expressive |
|---|---|---|
| Standard | `(0.2, 0, 0.38, 0.9)` | `(0.4, 0.14, 0.3, 1)` |
| Entrance | `(0, 0, 0.38, 0.9)` | `(0, 0, 0.3, 1)` |
| Exit | `(0.2, 0, 1, 0.9)` | `(0.4, 0.14, 1, 1)` |

**Penner-family curves as CSS cubic-beziers** (from easings.net), mapped to GSAP names:

| Name | cubic-bezier | GSAP | Character |
|---|---|---|---|
| easeOutCubic | `(0.33, 1, 0.68, 1)` | `power2.out` | Gentle default out |
| easeOutQuart | `(0.25, 1, 0.5, 1)` | `power3.out` | Confident |
| easeOutQuint | `(0.22, 1, 0.36, 1)` | `power4.out` | Snappy, premium (Apple-like) |
| easeOutExpo | `(0.16, 1, 0.3, 1)` | `expo.out` | Very fast start with a long tail. Great for text reveals |
| easeInOutCubic | `(0.65, 0, 0.35, 1)` | `power2.inOut` | Camera moves, morphs |
| easeInOutQuart | `(0.76, 0, 0.24, 1)` | `power3.inOut` | Dramatic transitions |
| easeOutBack | `(0.34, 1.56, 0.64, 1)` | `back.out(1.7)` | **~10% overshoot** (Penner's s = 1.70158 gives a 10% overshoot) |
| easeInBack | `(0.36, 0, 0.66, -0.56)` | `back.in(1.7)` | Anticipation pull-back on exit |

**Apple / spring physics.** SRC: APPLE-SPRING, WWDC23-SPRINGS.

- SwiftUI `.spring()` legacy defaults: **response 0.5s, dampingFraction 0.825**, blendDuration 0. Verified in Apple docs.
- Modern API: `Spring(duration:, bounce:)`. Presets `.smooth` (no bounce), `.snappy` (small bounce) and `.bouncy` (higher bounce). Commonly reported values are duration 0.5 and bounce 0 / 0.15 / 0.3. Apple's docs describe them only qualitatively, so treat the numbers as approximate.
- **Conversion to physics (mass = 1):** stiffness k = (2π / duration)², damping c = 4π(1 − bounce) / duration, so the damping ratio ζ = 1 − bounce.
- **Overshoot from damping ratio:** overshoot = exp(−πζ / √(1−ζ²)).
  - ζ 0.825 (default) → **~1%** overshoot (barely visible, "Apple feel")
  - bounce 0.15 (ζ 0.85) → ~0.6%
  - bounce 0.3 (ζ 0.7) → **~4.6%**
  - ζ 0.5 → ~16% (cartoony)
- GSAP has no native spring. Use `CustomEase`/`CustomWiggle`, precompute a spring curve into a `CustomEase` path, or use `elastic.out(1, 0.3-0.5)` (heavier oscillation; playful only).

**RULES:**
- Entrances use **decelerate** curves (they arrive fast and settle). Exits use **accelerate** curves (they start slow and leave fast). On-screen moves use **ease-in-out/standard**. **WHY:** this mimics physical objects entering or leaving the viewer's space (M1/M3 guidance).
- **Overshoot budget:** professional/corporate 0-3%. Creator/energetic 5-10%. Playful/kids 10-20%. Never overshoot body text or captions by more than 5%, because it hurts readability during the settle.
- Don't mix more than **2-3 easing families** in one video. Consistency is what makes motion read as "designed".

### 4.3 Durations

| Source | Values |
|---|---|
| M3 tokens | short1-4 = **50/100/150/200ms**; medium1-4 = **250/300/350/400ms**; long1-4 = **450/500/550/600ms**; extra-long1-4 = **700/800/900/1000ms** |
| Carbon | fast-01 **70ms** (micro), fast-02 **110ms** (fade), moderate-01 **150ms** (small, short distance), moderate-02 **240ms** (expansion, toast), slow-01 **400ms** (large expansion), slow-02 **700ms** (background dimming) |
| Material 1 (mobile) | **300ms** typical; **entering 225ms, exiting 195ms**; tablet **+30%** (390ms); wearable −30%; desktop **150-200ms** |
| NN/g | Most UI animation **100-500ms**; simple feedback ~100ms; modal/large change 200-300ms; "at 500ms they start to feel like a drag" *in interactive UI* |

**Video context differs from UI.** The viewer isn't waiting on an interaction; they need time to *notice and read*. Use these defaults for rendered video:

| Element | Enter | Hold (readable) | Exit |
|---|---|---|---|
| Caption word pop (Shorts) | 80-150ms | synced to speech | 0-100ms (cut or fast fade) |
| Keyword highlight / underline draw | 200-350ms | n/a | 150-250ms |
| Lower-third | 400-600ms (staggered parts) | ≥ 3-5s | 300-400ms |
| Title card / hook text | 300-500ms | words × 0.3s + 0.5s, minimum 1.2s | 200-350ms |
| Icon/stat callout | 250-400ms | ≥ 1.5s | 200ms |
| Chart bars/lines growing | 600-1200ms (data growth is the content) | ≥ 2s after completion | 300ms |
| Full-frame transition (wipe, zoom, push) | **300-600ms** total (8-18 frames at 30fps) | n/a | n/a |
| Camera move (scale/pan on still or graphic) | entire shot (3-8s), with a gentle ease-in-out | n/a | n/a |

**RULES:**
- **Duration ∝ distance:** ≈ 200ms + 100ms per 25% of frame-width traveled, capped at ~700ms for non-camera moves. **WHY:** perceived speed must stay constant across move sizes (M1: longer for larger distances and surface changes).
- **Exits = 75-85% of the entrance duration.** **WHY:** leaving elements need less attention (M1, M3).
- **Quantize durations to whole frames** of the output fps. At 30fps, 1 frame = 33.3ms, so 300ms = 9 frames. At 24fps, 1 frame = 41.7ms.

### 4.4 Stagger, choreography, hierarchy

- **Stagger per item:** **40-80ms** for lists of 3-7 items, **20-40ms** for letter-by-letter (cap the total sequence at ~600-800ms). Word-by-word kinetic type synced to VO uses the **speech timestamps**, not a fixed stagger. [FOLK/industry practice; Material's choreography docs recommend a consistent "lead" element then followers.]
- **Total stagger window ≤ 600ms** for UI-like groups. If a list exceeds this, stagger the first 5 items and then group the rest.
- **Motion hierarchy:** exactly **one hero motion** at a time. Secondary motions are ≤ 50% of the hero's travel distance and start ≥ 60-100ms later. Ambient motion (background drift, particles) stays slower than **~2-5% of frame size per second**. **WHY:** motion is the strongest exogenous attention cue in video [STRONG: attentional synchrony research], so competing motions split gaze.
- **Direction consistency:** "forward/next" moves **right-to-left or bottom-to-top** consistently. Back/previous reverses it. Enter and exit along the same axis.
- **Shared-element continuity:** when an element persists across a scene change, morph it (position/scale) instead of cutting it out and back in. **WHY:** object constancy reduces re-orientation load.

### 4.5 Frame rate and motion blur

| Topic | RULE | WHY |
|---|---|---|
| Match the source | Render graphics at the **project fps** (24/25/30, or 50/60 for gameplay/screen recordings). Never deliver 24fps footage in a 30fps timeline with 3:2 judder unless unavoidable | Mixed cadences judder |
| Talking-head YouTube | 24 or 30fps. 30 is safest for screen-recorded tech content; 60 for gameplay | YouTube supports 24-60 (YT-ENC) |
| Shutter / motion blur | Natural-looking blur = **180° shutter** (blur length = half the per-frame displacement; exposure 1/48s at 24fps, 1/60s at 30fps) | Matches how film audiences perceive motion |
| HTML/GSAP rendering | Rendered frames have **zero motion blur** by default, which makes fast moves strobe. For moves > ~2-3% of frame width per frame, either (a) render 4-8 subframes per frame and average them (accumulation blur; mimic a 180° shutter by averaging the first half of the subframes), or (b) add a directional CSS blur proportional to velocity | Removes strobing on fast whip transitions and text slams |
| Fast pans at 24fps | An object should take **≥ ~5-7s to cross the frame** for a smooth pan at 24fps/180° (RED "7-second rule" craft guidance) [FOLK/craft] | Otherwise it judders |
| Minimum readable motion | Text is unreadable while moving faster than **~10-15% of frame width per second**. Animate in, then **hold still** to read | Reading needs fixations (≈ 200-250ms each) |
| Flash safety | **≤ 3 flashes per second** and no saturated-red flashes (WCAG 2.3.1; broadcast uses ITU-R BT.1702 / the Harding test). Avoid full-frame white-flash transitions in rapid succession | Photosensitive seizure risk |

---

## 5. Editing Grammar & Attention Psychology

### 5.1 Walter Murch's Rule of Six (*In the Blink of an Eye*, 1995/2001)

When choosing a cut point, weigh the criteria in this order. **When you can't satisfy them all, sacrifice from the bottom up.** SRC: MURCH.

| Criterion | Weight |
|---|---|
| Emotion: is the cut true to the emotion of the moment? | **51%** |
| Story: does it advance the story? | **23%** |
| Rhythm: is it at a rhythmically right moment? | **10%** |
| Eye-trace: does it respect where the viewer's eye is looking? | **7%** |
| 2D plane of screen: 180° rule, screen direction | **5%** |
| 3D space: continuity of physical position | **4%** |

- Rating: **[FOLK]**, from a master editor. The percentages are rhetorical, not measured, but the priority order is near-universal practice.
- **Murch's blink theory:** a cut works like a blink, and viewers' blinks cluster at points of "thought completion". **RULE:** cut at the *end of a thought or clause*, not mid-word. Rating: [MODERATE]; Nakano et al. (2009) found that blinks synchronize across viewers at implicit breakpoints in video.
- **Eye-trace rule (agent-applicable):** at a cut, the subject of interest in the incoming shot should be within **~10-20% of the frame width** of where the outgoing shot's focus was. **WHY:** it avoids a search saccade, so the cut feels invisible. When you intentionally jolt (a pattern interrupt), break this on purpose.

### 5.2 Cut types and grammar

- **Cut on action:** cut *during* a movement, with the incoming shot continuing it. Overlap 2-4 frames of action for smoothness [FOLK/craft]. **WHY:** motion masks the discontinuity (the cut is less noticeable during movement; "edit blindness" research by Smith & Henderson 2008) **[MODERATE]**.
- **J-cut:** the incoming clip's **audio starts before** its picture, typically **6-24 frames (0.25-1s)**. Use it to lead into a new speaker or scene. **L-cut:** the outgoing **audio continues** over the new picture (B-roll over the VO tail). **RULE:** use J/L cuts on **≥ 50% of scene transitions** in documentary/interview edits. **WHY:** offsetting audio and picture edits hides cuts and creates flow [FOLK/industry standard].
- **Jump cuts (talking head):** remove pauses > 300-500ms and filler. Keep **2-6 frames of breath/room tone** at the head and tail of each phrase so speech doesn't feel clipped. Alternate framing (punch-in **110-125%** scale) on every 2nd-3rd jump cut to mask the jump. Punch-ins above ~130% reveal compression and softness on 1080p sources (on 4K sources ≤ 150% is fine for 1080 delivery).
- **Match cut / graphic match:** align the dominant shape or position across the cut (eye-trace).
- **Smash cut:** use a sudden audio-level change (loud→silence or silence→loud) to sell it.
- **180° rule and screen direction:** keep subjects' screen direction consistent for spatial continuity (Murch weights this low; break it only with motivation).

### 5.3 Shot length and pacing (data)

- Hollywood **average shot length (ASL)** dropped from ~8-10s (1930s-1960s) to **~3-4s by the 2000s**. Shot lengths also became more correlated with neighbors, approaching a **1/f pattern** that resembles human attention fluctuations (Cutting, DeLong & Nothelfer 2010, 150 films 1935-2005). **[STRONG]** for the trend; **[MODERATE]** for the attention interpretation. There was zero correlation of 1/f with IMDb ratings. SRC: CUTTING-2010.
- **RULE: vary shot lengths.** Don't cut on a metronome. Cluster short shots in high-energy passages and let longer shots breathe after reveals. **WHY:** this is what the 1/f structure is (long and short shots in mixed, correlated runs).
- **Platform pacing defaults [FOLK, consistent with platform guidance]:**
  - Shorts/Reels/TikTok: a visual change (cut, zoom, graphic, caption emphasis) every **1.5-3s**.
  - YouTube talking-head long-form: every **3-8s**.
  - Documentary/essay: **4-12s**.
  - Tutorials and screen-recordings: change when the *information* changes. Don't add cuts for their own sake; zoom to the area of interest.
- **"Pattern interrupt every X seconds"** as a retention law: **[FOLK]**. No controlled evidence supports a specific interval. What *is* established:
  - Cuts, onsets of graphics and other structural features trigger **orienting responses**: automatic attention allocation, measurable as heart-rate deceleration (Lang 1990s; Lang & Thorson 1992 found that inserting videographics into talking-head lectures elicits ORs). **[STRONG]**
  - Under Lang's Limited Capacity Model (LC4MP), **too many** structural changes, or *unrelated* cuts, overload capacity and **reduce memory** for the content, especially when the content is complex. **[MODERATE]** (Lang et al. 1993, *Communication Research*).
  - **RULE:** every interrupt must be **semantically related** (B-roll of what's being said, a graphic of the number just spoken). Lower the cut rate during dense explanations; raise it during low-information stretches (transitions, recaps).

### 5.4 Hooks, intros and retention

| Data point | Rating | SRC |
|---|---|---|
| YouTube "Key moments for audience retention" → **Intro** = % of viewers still watching at **0:30**. YouTube suggests checking that the first 30s match the title/thumbnail promise | [INDUSTRY] | YT-KEYMOMENTS |
| YouTube Content analytics lists videos with "above typical" intros. A rule of thumb of **≥ 50-60% still watching at 0:30** is commonly cited but **not an official benchmark** | [FOLK] | YT-KEYMOMENTS, third-party |
| Shorts "Viewed vs. swiped away": % of feed viewers who stayed past the opening seconds. The exact threshold is undisclosed. Third-party "good" benchmarks of ~70%+ viewed are unofficial | [INDUSTRY metric / FOLK benchmark] | YT-SHORTS-METRIC |
| Meta/Nielsen: **up to 47% of video-campaign value (lift) delivered in the first 3s, 74% in the first 10s** (173 Brand Effect studies) | [INDUSTRY]: commissioned, and about *ads* | META-NIELSEN |
| TikTok: introduce the content proposition **in the first 3s**; put the hook **within the first 6s** | [INDUSTRY] | TIKTOK-CBP |
| "Humans have an 8-second attention span, less than a goldfish" | **[MYTH]**: traces to a 2015 Microsoft Canada marketing report citing an unsourced "Statistic Brain" figure. Debunked by BBC *More or Less* (2017). Sustained-attention measures in adults haven't declined | ATTN-MYTH |

**Hook RULES (agent):**
1. **Frame 1 must already be "in motion".** No logo stings, black frames, or "hey guys" before the hook. On Shorts, the first frame must work as a thumbnail (on-screen text is visible at frame 0).
2. **0-3s:** state the payoff or tension (the promise from the title/thumbnail), with a visual change in the first 1s. **3-30s (long-form):** deliver proof of the promise, then open a loop for the rest of the video.
3. **Match the packaging:** the first 30s must visually or verbally confirm the title and thumbnail. YouTube's own guidance ties low intro retention to an expectation mismatch.
4. **Shorts loop:** the last line or frame should flow into the first (seamless loop) to inflate rewatches. [FOLK/industry practice]

### 5.5 Open loops, curiosity gap, Zeigarnik

- **Information-gap theory:** curiosity arises when attention is drawn to a specific gap in knowledge (Loewenstein 1994). Curiosity rises when people feel *partially* informed, and it enhances memory for the answer and even for incidental information (Kang et al. 2009; Gruber et al. 2014). **[STRONG]**
  - **RULE:** pose a specific question, delay the answer by **30s-3 min** (long-form) or **5-20s** (Shorts), and **pay it off** explicitly. Show partial information, like a blurred result or a chart with the last bar hidden. **WHY:** a specific gap creates curiosity; a vague one doesn't.
- **Zeigarnik effect** (better memory for interrupted tasks): a 2025 meta-analysis (Ghibellini & Meier, *Humanities & Social Sciences Communications*) found **no general memory advantage** for unfinished tasks, but did find a reliable **tendency to resume** them (the Ovsiankina effect). **[MYTH as usually stated]**; **[MODERATE]** for the resumption urge.
  - **RULE:** justify open loops by curiosity (Loewenstein), not by "Zeigarnik memory". Unresolved loops that never pay off damage trust and comments.

### 5.6 Cognitive load and Mayer's multimedia principles (critical for explainers)

Cognitive Load Theory (Sweller 1988): working memory is limited, so cut extraneous load. Mayer's principles are **[STRONG]** (dozens of experiments). The effect sizes are median Cohen's d from Mayer's Cambridge Handbook chapters (2014); later reviews report similar ranges. SRC: MAYER-2014, MAYER-2021.

| Principle | Effect (median d) | RULE for the editor |
|---|---|---|
| **Coherence** (cut extraneous words, pictures, sounds) | **0.86** (23/23 tests) | No decorative B-roll, stock footage, background music swells or SFX during dense explanation. Music bed ≥ 15 LU under voice or off |
| **Signaling** (highlight essential material) | **0.41** (24/28) | Highlight the keyword in the accent color, use arrows or circles on the relevant chart part, dim non-relevant areas to ≤ 40% |
| **Redundancy** (graphics + narration beats graphics + narration + identical on-screen text) | **0.86** (16/16) | Don't put the narration sentence on screen as a paragraph next to a diagram. Show **keywords (≤ 5 words)** only. *Boundary conditions:* captions remain useful for sound-off, accessibility and non-native viewers, and redundancy hurts little when on-screen text is short or there are no competing graphics |
| **Spatial contiguity** (words next to the picture they describe) | ~**0.8-1.1** | Put labels **on or next to** the chart element (≤ 5% of frame width away), not in a separate legend |
| **Temporal contiguity** (narration and the corresponding animation at the same time) | ~**1.2-1.3** | The visual appears **on the spoken word** (±150ms), not a sentence earlier or later. Use word timestamps |
| **Segmenting** (learner-paced chunks) | ~**0.7-0.8** | Break explainers into labeled chapters/sections of **≤ 60-120s** with a visual reset (section card) |
| **Pre-training** (key terms first) | ~0.75 | Define 1-3 key terms visually before the complex process |
| **Modality** (narration + graphics beats on-screen text + graphics) | ~0.7-1.0 | Explain with voice, show with visuals. Don't make viewers read paragraphs |
| **Personalization** (conversational style) | ~0.8 | "You" language in VO and on-screen text |
| **Embodiment / image** | mixed (the image principle is weak: a talking head adds little *learning*) | A presenter on screen helps engagement, but **cut away to the visual** during the hardest content |

**Dual coding** (Paivio 1971/1986): verbal plus pictorial representations improve recall versus either alone. **[STRONG]** **RULE:** every abstract claim gets a concrete visual: a number→chart, a process→diagram, a comparison→side-by-side.

### 5.7 Gestalt principles for layout

**[STRONG]**: perceptual grouping is foundational vision science (Wertheimer; Wagemans et al. 2012 review).

| Principle | RULE |
|---|---|
| Proximity | Space within a group ≤ **50%** of the space between groups (e.g. 16px inside a group, 40px+ between) |
| Similarity | Same function = same color, weight and shape. Change exactly one property to signal difference |
| Common fate | Elements that move together are seen as a group. Animate a group with a shared ease and direction. Use **different** timing only for things that are conceptually separate |
| Continuity | Align items on strong axes. Arrows and lines lead the eye to the next item |
| Closure | Partial shapes (a circle drawn 90%) read as complete. Draw-on reveals work |
| Figure/ground | The text plate must separate clearly from the footage (luminance, blur, scrim) |
| Common region | A container/plate groups items more strongly than proximity alone |

### 5.8 Reading patterns vs. video attention

- **F-pattern / Z-pattern** describe scanning of **text-heavy web pages** (NN/g eye-tracking, 2006, updated 2017). The F-pattern is a sign of poor formatting, not a design goal. **[STRONG]** for web pages, **N/A** for video.
- **Video gaze** is dominated by:
  1. **Center bias**: fixations cluster near the screen center, partly because of composition, partly a viewing strategy (Tseng et al. 2009). **[STRONG]**
  2. **Motion onsets.**
  3. **Faces**, especially eyes; gaze shifts to the mouth when speech is hard to hear.
  4. **Text**: free viewers looked at **faces 16.6x and text 11.1x** more than size- and position-matched control regions, even when it was costly to the task (Cerf, Frady & Koch 2009). **[STRONG]**
- **Attentional synchrony:** viewers of edited video look at the **same place at the same time** to a high degree ("tyranny of film"). Editing and motion largely control gaze (Smith & Henderson 2010; Smith & Mital 2013; Loschky et al. 2015). **[STRONG]**
- **RULES:**
  - Place new text **near the current gaze point**: near the speaker's face or the moving element, never in a far corner. **WHY:** it avoids long saccades and keeps the graphic within the attended region (also spatial contiguity).
  - **Don't put two text elements on screen at once if they're far apart.** Text captures gaze automatically, so two blocks split attention.
  - Keep the subject's **eyes on the upper-third line** (≈ 33-38% from the top in 16:9; ≈ 30-40% in 9:16), within ~20% of horizontal center for single-subject vertical video.
  - When a graphic appears, **dim or blur the face** briefly, or move the speaker aside. Faces otherwise compete for the gaze.

### 5.9 Captions and retention

| Claim | Rating | SRC |
|---|---|---|
| Captions improve comprehension, attention and memory for hearing viewers (review of 100+ studies) | [STRONG] for the core claim; strongest for non-native, literacy-learning and deaf/HoH viewers. Critics say "for everyone" is overstated for native-language adult viewers | GERNSBACHER-2015 |
| **69%** of US consumers watch video with sound off in public; **80%** of respondents say they're more likely to finish a video if captions are available (Verizon Media/Publicis 2019, n=5,616) | [INDUSTRY] self-report. Note that "80% *more* likely" is a common misquote | VERIZON-2019 |
| Viewers read subtitles automatically even in their own language (d'Ydewalle) | [STRONG] | Literature |

- **RULES:**
  - **Always** burn in captions for Shorts/Reels/TikTok. For long-form, upload an SRT/VTT *and* optionally burn in key-phrase emphasis.
  - Highlight **1 keyword per chunk** in the accent color, not every word.
  - Active-word highlight (karaoke) should change on the word onset (±1 frame).

---

## 6. Sound Design Psychology

### 6.1 Loudness targets

| Platform / standard | Integrated | True peak | Rating | SRC |
|---|---|---|---|---|
| **YouTube** | **-14 LUFS** reference (turns loud content down; does **not** turn quiet content up) | ≤ -1 dBTP | [INDUSTRY, observed via "Stats for nerds"; no official doc] | YT-LOUD |
| **Spotify** (also podcasts/video) | **-14 LUFS** (Loud -11, Quiet -19) | **≤ -1 dBTP**; ≤ -2 dBTP if the master is louder than -14 | [INDUSTRY, official] | SPOTIFY |
| Apple Music (Sound Check) | ~-16 LUFS | -1 dBTP | [INDUSTRY] | n/a |
| Apple Podcasts | **-16 LUFS ±1** | -1 dBTP | [INDUSTRY] | n/a |
| AES TD1004 streaming recommendation | -16 to -20 LUFS (speech-centric content toward -18) | ≤ -1 dBTP | [STANDARD] | AES-TD1004 |
| TikTok / Instagram Reels / Shorts | **No published target.** Observed normalization around -14 | -1 dBTP | [FOLK/observed] | n/a |
| **EBU R128** (EU broadcast) | **-23 LUFS ±0.5-1 LU** | **≤ -1 dBTP** | [STANDARD] | EBU-R128 |
| ATSC A/85 (US broadcast) | **-24 LKFS ±2** | -2 dBTP | [STANDARD] | ATSC-A85 |
| Netflix | **-27 LKFS dialogue-gated** | -2 dBTP | [INDUSTRY] | NETFLIX-AUDIO |

- **RULE (social/YouTube master):** **-14 LUFS integrated, -1 dBTP max, LRA 4-8 LU** for talking-head content. Dialogue is the anchor: **voice short-term loudness ≈ -14 to -16 LUFS** while speaking.
- **RULE:** check mono compatibility and phone-speaker translation. High-pass voice at 70-100Hz. Keep critical information above 150Hz, because phone speakers roll off below ~200-300Hz.

### 6.2 Music under voice (ducking)

- **Research:** Torcoli et al. (2019, AES; Fraunhofer/Salford, n=22) recommend a **loudness difference (LD) of ≥ 10 LU for commentary over music**, and **≥ 15 LU for commentary over ambience**. Non-experts preferred LDs **~4 LU larger** than experts did. For voice over voice: ≥ 20 LU (Geary et al. 2020). German public broadcaster guidance: LD ≥ 7 LU. **[MODERATE]** (small panels, consistent direction). SRC: TORCOLI-2019.
- **RULES:**
  - Music bed **12-18 LU below the voice** (short-term LUFS) under speech. With voice at -15 LUFS-S, music sits at about -27 to -33 LUFS-S. Use the deeper end (≥ 15 LU) for **explainers** (coherence principle) and for **general audiences** (non-experts want bigger gaps).
  - Between phrases and sentences, music may swell to **4-8 LU below** speech level. In music-only sections, bring it to the full mix level (around -14 to -16 LUFS-S).
  - Ducking dynamics: **attack 50-150ms, release 300-800ms**, with a 200-400ms look-ahead (pre-duck before the first syllable) [FOLK/craft]. Avoid audible "pumping" between words: use a hold of ~300-500ms.
  - EQ-carve instead of only turning down: cut the music by **2-4dB around 1-4kHz** (speech intelligibility band) while voice is present.
  - Pick instrumental, low-mid-sparse beds under VO. **No vocals in the music under speech**, because it competes for the same verbal processing channel.

### 6.3 SFX cueing [FOLK/craft unless noted]

| Event | SFX | Level (relative to voice) | Timing |
|---|---|---|---|
| Transition (wipe, whip, push) | Whoosh / swish | -6 to -12 dB under voice peak | Whoosh **peak lands on the cut frame**. The whoosh tail starts 4-10 frames before the cut |
| Text or word pop | Soft pop, click, tick | -12 to -20 dB | Transient on the **first frame** the element is visible (0-1 frame early is fine) |
| Number counter | Fast ticks, or a rising tone | -18 dB | Ends with a "ding" when the counter stops |
| Emphasis/impact (smash cut, title slam) | Hit / boom / riser→hit | -3 to -8 dB (brief) | Riser 1-4s before, hit on the frame |
| Error / negative | Low buzz / thud | -12 dB | On the reveal |
| Screen UI action (screen recording) | Mouse click, keyboard | -18 to -24 dB | Synced to the visible click |

- **RULE:** at most **1 SFX per second** on average in long-form explainers, and more in Shorts. Never stack SFX on top of key words. **WHY:** coherence principle (extraneous sounds hurt learning, d ≈ 0.86) **[STRONG]**.
- **RULE:** give every SFX a **visual cause** (audio-visual synchrony). Unmotivated sounds read as noise.
- **Audio-visual sync tolerance:** audio may lead video by ≤ ~45ms or lag by ≤ ~125ms before viewers notice (ITU-R BT.1359) **[STANDARD]**. Snap SFX to the frame.

### 6.4 Silence and rhythm

- **Silence as emphasis:** cut music to silence (or a room-tone-only pause of **0.5-1.5s**) right before a key reveal or punchline. The contrast creates an orienting response to the next sound onset. **[MODERATE]**: auditory onsets and changes trigger orienting (LC4MP literature). The specific durations are [FOLK].
- **BPM ↔ pacing [FOLK/craft]:**
  - Frames per beat = fps × 60 / BPM. At 30fps and 120 BPM that's 15 frames per beat; at 100 BPM, 18 frames; at 24fps and 120 BPM, 12 frames.
  - Energetic Shorts/montage: **110-140 BPM**, cutting on beats or every 2 beats. Explainer beds: **80-110 BPM**. Documentary/emotional: **60-90 BPM**.
  - Cut on **downbeats** for big changes and on off-beats for small ones. Let section changes in the music (drops, new phrase every 4 or 8 bars) coincide with chapter changes.
  - Speech rate reference: conversational/presenting English ≈ 140-170 wpm (BBC subtitle guidance assumes 160-180 wpm speech). Above ~190 wpm, comprehension and caption readability suffer.

---

## 7. Anti-"AI Slop" Visual Tells (and what to do instead)

These are **[FOLK]** taste rules, but they're consistent across design critics and practitioners, and they follow from the principles above (hierarchy, one accent, coherence).

| Tell | Why it reads as slop | Do instead |
|---|---|---|
| **Purple→blue/pink gradient** on everything (especially `#7C3AED→#3B82F6`) and neon purple glow | The default "AI/tech" aesthetic of templated SaaS and LLM-generated UIs | Derive the palette from the footage or brand (§3.3). Use flat tinted neutrals with **one** accent. If you use a gradient, make it **same-hue lightness ramps** in OKLCH with grain |
| **Glow and outer bloom** on text and icons | Lowers legibility, looks like a template, and bands after compression | Use a crisp contact shadow (§1.7) or no effect |
| **Glassmorphism everywhere** (frosted cards on blurred blobs) | Overused since 2021. Low contrast, and expensive blur that compresses badly | Solid plates at 85-95% opacity, or one glass element max per scene, over real footage |
| **Everything centered**, symmetric, on a dark void | No hierarchy and no tension. Reads as a slide template | Use a grid. Left-align text blocks to the title-safe edge. Asymmetric compositions with the subject on thirds |
| **Too many fonts / random weights** | No system | ≤ 2 families, ≤ 3 weights (§1.5) |
| **Bounce/elastic on everything** | No hierarchy of motion. Cartoony | Overshoot budget (§4.2): spring or back easing only on the hero, decelerate curves for the rest |
| **Everything animates in at once** or with an identical fade-up-20px | Generic "AOS/scroll-reveal" look | Choreograph: lead element, then followers (40-80ms stagger), each with a motivated direction |
| **Emojis as icons** 🚀✨🔥 | Platform-dependent rendering, cheap look, inconsistent stroke styles | One consistent icon set (Lucide, Phosphor, Material Symbols, Tabler) at one stroke weight (1.5-2px at 24px, scaled) |
| **Generic stock B-roll / AI-generated filler** (handshake, glowing brain, server rooms) | Violates coherence. Viewers recognize it | Literal, specific visuals: screenshots, real product, real data, the speaker's own footage, diagrams |
| **Floating 3D blobs, abstract particle fields, "neural network" lines** | Decorative motion competing with content (coherence, d ≈ 0.86) | Remove, or keep ambient motion below 2-5% of frame per second at ≤ 30% opacity |
| **Rounded-everything with drop-shadow cards** (`rounded-2xl shadow-xl`) | Tailwind default aesthetic | Vary radii intentionally (0, 4 or 8px). Use hairline borders, or no container at all |
| **Lorem-like copy**: "Unlock the power of…", "Revolutionize your…", "Seamless" | LLM copywriting tells | Concrete nouns and numbers from the actual transcript |
| **Perfectly even rhythm** (every cut 2.0s, every caption identical) | Machine-uniform pacing | Vary shot lengths (§5.3, the 1/f idea). Let emphasis words get bigger or longer treatment |
| **Gradient text on every headline** | Lowers contrast. Clichéd | Solid color. Accent only on 1-2 keywords |
| **Typewriter effect for long sentences** | Slow and gimmicky. Delays reading | Word- or line-level reveals at ≤ 300ms total, or a straight cut-in |
| **Lens-flare / light-leak transitions everywhere** | Template look | Hard cuts (≈ 90%+ of all transitions in professional edits are straight cuts [FOLK]). Use a motivated transition only at section changes |
| **Inter + purple + glass + emoji** all together | The full "AI landing page" stack | Pick the font by mood from §2, the color from footage, and an icon set |

**RULE:** before rendering, run a **slop audit**:

- [ ] ≤ 2 font families
- [ ] Exactly 1 accent hue
- [ ] No more than 1 bouncing element per scene
- [ ] No emoji used as an icon
- [ ] No full-frame gradient without grain
- [ ] Every graphic is tied to a spoken word (temporal contiguity)
- [ ] Every text block is inside the safe area and passes contrast against its actual background in every frame

---

## 8. Machine-Readable Defaults (for the skill's config)

```json
{
  "safe_area": {
    "16x9_title_inset_pct": 5, "16x9_action_inset_pct": 3.5,
    "9x16_universal_rect_px": {"x0": 80, "x1": 900, "y0": 250, "y1": 1440},
    "youtube_bottom_reserved_pct": 12
  },
  "type": {
    "min_font_pct_h_16x9": 4.5, "phone_first_font_pct_h_16x9": 6.0,
    "shorts_caption_px_at_1080w": [64, 96], "absolute_floor_px_1080": 28,
    "caption_max_cpl_16x9": 42, "caption_max_cpl_9x16": 20, "caption_max_lines": 2,
    "cps_comfort": 17, "cps_max": 20, "sec_per_word_min": 0.3, "min_caption_s": 0.8,
    "allcaps_tracking_em": [0.05, 0.12], "display_tracking_em": [-0.03, -0.01],
    "body_leading": [1.2, 1.45], "display_leading": [0.9, 1.1],
    "max_families": 2, "max_weights": 3, "min_weight_below_60px": 400,
    "stroke_px_1080": [2, 4], "shadow_css_1080": "0 2px 10px rgba(0,0,0,.65), 0 0 2px rgba(0,0,0,.6)",
    "scrim": {"height_pct": 35, "max_alpha": 0.7}
  },
  "color": {"wcag_text": 4.5, "wcag_large": 3.0, "apca_caption_min_lc": 75, "apca_headline_min_lc": 45,
            "accent_count": 1, "accent_max_area_pct": 10, "grain_pct": [1, 5], "interp_space": "oklch"},
  "ease": {
    "enter": "cubic-bezier(0.05,0.7,0.1,1)", "exit": "cubic-bezier(0.3,0,0.8,0.15)",
    "move": "cubic-bezier(0.2,0,0,1)", "snappy_out": "cubic-bezier(0.22,1,0.36,1)",
    "expo_out": "cubic-bezier(0.16,1,0.3,1)", "back_out_10pct": "cubic-bezier(0.34,1.56,0.64,1)"
  },
  "duration_ms": {"micro": [70, 150], "small": [150, 250], "medium": [300, 450], "large": [450, 700],
                  "transition_full_frame": [300, 600], "exit_ratio": 0.8, "stagger_item": [40, 80], "stagger_total_max": 600},
  "overshoot_pct": {"corporate": [0, 3], "creator": [5, 10], "playful": [10, 20]},
  "flash_max_per_s": 3,
  "audio": {"integrated_lufs": -14, "true_peak_dbtp": -1, "music_under_voice_lu": [12, 18],
            "duck_attack_ms": [50, 150], "duck_release_ms": [300, 800], "av_sync_ms": {"audio_lead_max": 45, "audio_lag_max": 125}},
  "pacing_visual_change_s": {"shorts": [1.5, 3], "longform_talking": [3, 8], "documentary": [4, 12]},
  "punch_in_scale": [1.10, 1.25]
}
```

---

## 9. Source List

Primary and authoritative sources come first in each group. All were accessed in October 2026 unless noted.

**Typography, subtitles, safe areas**
- NETFLIX-TTSG: Netflix English (USA) Timed Text Style Guide. https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide
- Netflix Timed Text Style Guide, General Requirements. https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements
- BBC-SUB: BBC Subtitle Guidelines. https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/
- EBU-R95: EBU R95, Safe areas for 16:9 television production. https://tech.ebu.ch/publications/r095 (PDF: https://tech.ebu.ch/docs/r/r095.pdf)
- SMPTE-2046: SMPTE ST 2046-1, Safe Areas for 16:9 Television Systems. https://doi.org/10.5594/SMPTE.ST2046-1.2009 (overview: https://en.wikipedia.org/wiki/Safe_area_(television))
- BUTTERICK: Butterick's Practical Typography, Summary of key rules. https://practicaltypography.com/summary-of-key-rules.html ; letterspacing: https://practicaltypography.com/letterspacing.html
- LEGGE-BIGELOW-2011: Legge & Bigelow, "Does print size matter for reading?", *Journal of Vision* 11(5):8. https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264
- SZARKOWSKA-2018: Szarkowska & Gerber-Morón, "Viewers can keep up with fast subtitles", *PLoS ONE*. https://discovery.ucl.ac.uk/id/eprint/10050653/
- BRYSBAERT-2019: Brysbaert, "How many words do we read per minute?", *J. Memory & Language*. https://www.Gwern.net/doc/psychology/linguistics/2019-brysbaert.pdf
- GOOGLE-FONTS-KNOWLEDGE: Google Fonts Knowledge (pairing, optical size). https://fonts.google.com/knowledge
- FONTSHARE: ITF Fontshare license info. https://www.fontshare.com/licenses ; https://www.indiantypefoundry.com/news/introducing-fontshare
- 9:16 safe zones (third-party, measured, non-official): https://reap.video/blog/short-form-video-safe-zones ; https://adkit.so/tools/safe-zones/tiktok ; https://www.hopperhq.com/blog/instagram-reel-size/ ; https://www.outfy.com/blog/instagram-safe-zone/ ; https://moda.app/tools/story-safe-zone-checker
- TIKTOK-CBP: TikTok Ads, Creative best practices for performance ads. https://ads.tiktok.com/help/article/creative-best-practices

**Color & contrast**
- WCAG: W3C WCAG 2.2, contrast (1.4.3, 1.4.6, 1.4.11) and three flashes (2.3.1). https://www.w3.org/TR/WCAG22/
- APCA: APCA in a Nutshell. https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell
- ELLIOT-MAIER-2014: Elliot & Maier, "Color psychology: Effects of perceiving color on psychological functioning in humans", *Annu. Rev. Psychol.* 65. https://doi.org/10.1146/annurev-psych-010213-115035
- GNAMBS-2020: Gnambs et al., "Processing the word red and intellectual performance: four replications". https://pure.fh-ooe.at/en/publications/processing-the-word-red-and-intellectual-performance-four-replica/
- PBR-2020-COLOR: Review of color-priming in achievement contexts, *Psychonomic Bulletin & Review* (2020). https://link.springer.com/article/10.3758/s13423-020-01772-1
- ADOBE-SKIN: Adobe Premiere Pro, Correct skin tones. https://helpx.adobe.com/premiere-pro/how-to/correct-skin-tones.html
- JORDAN / VAN-HURKMAN: Larry Jordan, "The secret to setting skin colors accurately" (cites Van Hurkman's *Color Correction Handbook*). https://larryjordan.com/articles/the-secret-to-setting-skin-colors-accurately/
- PVC-BANDING: ProVideo Coalition, Remove banding in After Effects. https://www.provideocoalition.com/remove-banding-in-after-effects/
- YT-ENC: YouTube recommended upload encoding settings. https://support.google.com/youtube/answer/1722171
- OKLCH/OKLab: Björn Ottosson, "A perceptual color space for image processing". https://bottosson.github.io/posts/oklab/

**Motion**
- M3-TOKENS: Material Web motion tokens (v0.192, Apache-2.0). https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-motion.scss ; docs: https://m3.material.io/styles/motion/easing-and-duration/tokens-specs
- M1-MOTION: Material Design (v1), Duration & easing. https://m1.material.io/motion/duration-easing.html
- CARBON-MOTION: IBM Carbon Design System, Motion. https://carbondesignsystem.com/elements/motion/overview/
- NNG-ANIM: NN/g, "Animation Duration". https://www.nngroup.com/articles/animation-duration/
- APPLE-SPRING: Apple, `spring(response:dampingFraction:blendDuration:)`. https://developer.apple.com/documentation/swiftui/animation/spring(response:dampingfraction:blendduration:) ; `Spring`: https://developer.apple.com/documentation/swiftui/spring
- WWDC23-SPRINGS: WWDC23 "Animate with springs" (session 10158). https://developer.apple.com/videos/play/wwdc2023/10158/ ; notes: https://wwdcnotes.com/documentation/wwdc23-10158-animate-with-springs/
- EASINGS: easings.net (Penner equations as cubic-beziers). https://easings.net/
- GSAP eases: https://gsap.com/docs/v3/Eases/
- DISNEY-12: Thomas & Johnston, *The Illusion of Life: Disney Animation* (1981). Summary: https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation
- ITU-R BT.1702 (photosensitive epilepsy guidance). https://www.itu.int/rec/R-REC-BT.1702
- ITU-R BT.1359 (relative timing of sound and vision). https://www.itu.int/rec/R-REC-BT.1359

**Editing & attention**
- MURCH: Walter Murch, *In the Blink of an Eye* (2nd ed., 2001). Rule of Six summary: https://wikis.utexas.edu/display/rtf318/Murch%27s+Rule+of+Six ; https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch
- Nakano et al. (2009), "Synchronization of spontaneous eyeblinks while viewing video stories", *Proc. R. Soc. B*. https://doi.org/10.1098/rspb.2009.0828
- CUTTING-2010: Cutting, DeLong & Nothelfer, "Attention and the evolution of Hollywood film", *Psychological Science* 21(3). https://journals.sagepub.com/doi/10.1177/0956797610361679 ; summary: https://www.psychologicalscience.org/observer/the-science-of-hollywood-blockbusters-2
- LANG-1993: Lang, Geiger, Strickwerda & Sumner (1993), "The effects of related and unrelated cuts on viewers' memory for television: A limited capacity theory of television viewing", *Communication Research* 20(1):4-29. (DOI not verified this session; search the title on journals.sagepub.com)
- Lang & Thorson (1992), on videographics in televised talking-head lectures eliciting orienting responses (cited via secondary sources).
- Lang, "The limited capacity model of mediated message processing", *J. Communication* 50(1), 2000. https://doi.org/10.1111/j.1460-2466.2000.tb02833.x
- Smith & Henderson (2008), "Edit Blindness", *J. Eye Movement Research*. https://doi.org/10.16910/jemr.2.2.6
- Smith & Mital (2013), "Attentional synchrony and the influence of viewing task on gaze behavior in static and dynamic scenes", *J. Vision*. https://doi.org/10.1167/13.8.16
- Loschky et al. (2015), "What would Jaws do? The tyranny of film…", *PLoS ONE*. https://pmc.ncbi.nlm.nih.gov/articles/PMC4659561
- CERF-2009: Cerf, Frady & Koch, "Faces and text attract gaze independent of the task", *J. Vision* 9(12). https://resolver.caltech.edu/CaltechAUTHORS:20130816-103355264
- Tseng et al. (2009), "Quantifying center bias of observers in free viewing of dynamic natural scenes", *J. Vision*. https://doi.org/10.1167/9.7.4
- NN/g F-pattern (2017 update). https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
- YT-KEYMOMENTS: YouTube Help, Measure key moments for audience retention. https://support.google.com/youtube/answer/9314415
- YouTube Help, Content analytics. https://support.google.com/youtube/answer/12942217
- YT-SHORTS-METRIC: "Viewed vs. swiped away" (glossary). https://www.creatoressentials.com/glossary/viewed-vs-swiped-away/
- META-NIELSEN: Facebook/Nielsen brand-lift-in-seconds study (coverage). https://martech.org/even-brief-video-views-drive-brand-lift-facebook-nielsen-study-finds/
- ATTN-MYTH: the goldfish/8-second myth. https://www.bbc.com/news/health-38896790 (BBC *More or Less*, 2017); https://www.warc.com/newsandopinion/opinion/the_goldfish_myth/2806
- Loewenstein (1994), "The psychology of curiosity", *Psychological Bulletin* 116(1). https://doi.org/10.1037/0033-2909.116.1.75
- Kang et al. (2009), "The wick in the candle of learning", *Psychological Science*. https://doi.org/10.1111/j.1467-9280.2009.02402.x
- Gruber, Gelman & Ranganath (2014), "States of curiosity modulate hippocampus-dependent learning", *Neuron*. https://doi.org/10.1016/j.neuron.2014.08.060
- ZEIGARNIK-2025: Ghibellini & Meier (2025), "The Zeigarnik effect revisited", *Humanities & Social Sciences Communications* 12. https://ideas.repec.org/a/pal/palcom/v12y2025i1d10.1057_s41599-025-05000-w.html
- MAYER-2014: Mayer & Fiorella, "Principles for reducing extraneous processing…" in *Cambridge Handbook of Multimedia Learning* (2nd ed.). https://resolve-he.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles/CD5B7AE1279A9AB81F8EEBB53DBEC86E
- MAYER-2021: Mayer, *Multimedia Learning* (3rd ed., Cambridge UP, 2021).
- Sweller (1988), "Cognitive load during problem solving", *Cognitive Science* 12(2). https://doi.org/10.1207/s15516709cog1202_4
- Paivio, *Mental Representations: A Dual Coding Approach* (1986).
- Wagemans et al. (2012), "A century of Gestalt psychology in visual perception", *Psychological Bulletin*. https://doi.org/10.1037/a0029333
- GERNSBACHER-2015: Gernsbacher, "Video Captions Benefit Everyone", *Policy Insights from the Behavioral and Brain Sciences* 2(1). https://successforkidswithhearingloss.com/wp-content/uploads/2020/04/Video-Captions-Benefit-Everyone_2015.pdf
- VERIZON-2019: Verizon Media/Publicis Media caption survey (coverage). https://www.3playmedia.com/blog/verizon-media-and-publicis-media-find-viewers-want-captions/

**Sound**
- SPOTIFY: Spotify for Artists, Loudness normalization. https://support.spotify.com/artists/article/loudness-normalization/
- YT-LOUD: Ian Shepherd/MeterPlugs, "YouTube changes loudness reference to -14 LUFS" (2019). https://www.meterplugs.com/blog/2019/09/18/youtube-changes-loudness-reference-to-14-lufs.html
- EBU-R128: EBU R128, Loudness normalisation and permitted maximum level. https://tech.ebu.ch/publications/r128
- ATSC-A85: ATSC A/85, Techniques for establishing and maintaining audio loudness. https://www.atsc.org/atsc-documents/a85-techniques-for-establishing-and-maintaining-audio-loudness-for-digital-television/
- NETFLIX-AUDIO: Netflix Sound Mix Specifications & Best Practices (Netflix Partner Help Center; search "Sound Mix Specifications" at https://partnerhelp.netflixstudios.com). Secondary confirmation: https://thepostflow.com/filmmaker-resources/delivery-specs-cheat-sheet/
- AES-TD1004: AES TD1004.1.15-10, Recommendation for Loudness of Audio Streaming and Network File Playback. https://www.aes.org/technical/documentDownloads.cfm?docID=731
- TORCOLI-2019: Torcoli, Freke-Morin, Paulus, Simon & Shirley, "Background ducking to produce esthetically pleasing audio for TV with clear speech", AES 146th Convention. https://salford-repository.worktribe.com/OutputFile/1488623 ; Fraunhofer summary: https://www.audioblog.iis.fraunhofer.com/?p=4251
- Geary, Torcoli et al. (2020), "Loudness differences for voice-over-voice audio in TV and streaming", *JAES*. https://salford-repository.worktribe.com/output/1341554/loudness-differences-for-voice-over-voice-audio-in-tv-and-streaming

---

### Verification notes (honesty log)

- **Verified directly this session** (fetched or confirmed via search): Netflix 42 cpl / 20 & 17 cps; all BBC numbers; EBU R95 3.5% and 5%; M3 token values (from source code); Carbon easing and durations; M1 225/195ms and the tablet/desktop rules; NN/g 100-500ms; Apple spring defaults 0.5 / 0.825; APCA Lc levels; Butterick's 5-12% / 45-90 / 120-145%; Spotify -14 / -1 / -2; YouTube encoding settings; Murch percentages; Cutting 2010; Mayer d for coherence, signaling and redundancy; Zeigarnik 2025 meta-analysis; Cerf 16.6x / 11.1x; Verizon 69% / 80%; Meta 47% / 74%; TikTok 3s / 6s and "5-10 words per second"; Torcoli ≥ 10 / 15 LU; Legge 0.2-2°; Brysbaert 238 wpm.
- **From established knowledge, not re-fetched:** easings.net bezier values; the Penner back overshoot (10%); ITU-R BT.1359 sync tolerances; the Apple Podcasts -16 LUFS figure; AES TD1004 range; Nakano 2009; Tseng 2009; Smith & Henderson 2008 edit blindness; Kang 2009 / Gruber 2014; the SwiftUI preset bounce values (0 / 0.15 / 0.3, approximate); the ~63% YouTube mobile share.
- **Mayer spatial/temporal contiguity and segmenting d values** come from a secondary review (0.79 / 1.30 / 0.70) and Mayer's earlier reported medians (~1.1 / ~1.2 / ~0.8). They're given as ranges.
- **9:16 UI safe-zone pixels are not officially published** by TikTok, Meta or YouTube for organic posts. Re-measure periodically.


# ===== FILE: references/motion-prompt-research.md =====

# What makes Opus 5.5 code-animated videos work: findings from 513 prompts

Contents: 0. Method and caveats (read first) · 1. Prompt anatomy · 2. Tech stack statistics · 3. Technique catalog (38 reusable scene types) · 4. Explainer patterns · 5. Quality-raising phrases and weak prompts · 6. Timing data · 7. The best full prompts, quoted · 8. Rules for the skill

Source: `awesome-opus5-5-videos/data/videos.json` (513 entries) plus `README.md` (100 highlighted entries, one per distinct prompt).
Scope: all of **motion** (317) and **explainer** (67), a skim of **3d** (59), and **interactive** (70) only where a technique carries over to video.

## 0. Method and caveats (read first)

- **Deduplication.** Motion + explainer have 384 entries but only 336 distinct prompt texts. The 15-second "showreel" prompt alone shows up 89 times across the dataset (§5). Unless a figure says otherwise, percentages are over distinct prompts.
- **"Partial" entries are mostly social posts, not prompts.** In motion, 100 of 317 entries are `prompt_partial: true`, and in explainer 43 of 67. Most of these hold the creator's post ("Made with Opus 5.5 + Remotion…") rather than a prompt. That makes them useful for tool and workflow stats, but they distort anatomy stats. So I report three groups:
  - **A. All distinct M+E** (n=336).
  - **B. Real prompts**: distinct M+E with `prompt_partial=false` (n=193). Median 30 words, p75 61, p90 151, max 4,093. Length buckets: <20 words: 56; 20–39: 70; 40–99: 41; 100–299: 11; 300+: 15.
  - **C. Detailed prompts**: group B with 150 or more words (n=20). These are the high-signal specs: koldo2k-778767, twoclipping-402193, anabology-491441, verbove-268381, brainextends-606193, majidmanzarpour-927543, howdevelop-733090, wani-shola-459278, alexwtlf-981005, doubleunplussed-181894, astrothewizard-618782, annacher-433425, paranoidamerica-686717, thegrootdev-966114, iamtanzil-120030, gdgtify-929495, techhalla-498547, jake11moran-414633, anjmaxx-459455, eric-khun-667455.
  - I also read the partial entries that quote a full prompt (daniel-haida-636937, ik-builds-585923, aschapmann-724497, stokebuilder-356793). They are cited qualitatively.
- **How features were counted.** Case-insensitive regex over prompt text, run with `python3 -I`. For example, `#\s?[0-9a-f]{6}` for hex colours, `seek\(|deterministic|pure function|no timers|setTimeout|seeded|no css transitions|no state` for determinism, and `playwright|headless|puppeteer|frame by frame|subframe|tmix` for frame capture. Regex counts are approximate. The ban-list matrix in §1.3 was tallied by hand.
- **`tech_tags` describe the output video, not the prompt.** Most prompts never name a library.
- **One outlier.** alexwtlf-981005 (4,093 words) is a shot-by-shot brief for an AI video model (📷@character refs, lens mm, Kelvin lighting). It is tagged canvas but is not code animation. I use it only for its "POSITIVE LOCKS" technique.

---

## 1. Prompt anatomy

### 1.1 How often each structural element appears

| Element | A. All distinct M+E (336) | B. Real prompts (193) | C. Detailed ≥150w (20) | Highlighted M+E (74) | 3d (57) |
|---|---|---|---|---|---|
| Duration stated | 43.2% | **57.0%** | 65% | 55.4% | 15.8% |
| Resolution (1920/1080/1440…) | 5.1% | 6.7% | 50% | 10.8% | 5.3% |
| Aspect (9:16, 16:9, square, portrait…) | 7.1% | 10.9% | 60% | 14.9% | 7.0% |
| fps | 5.4% | 6.7% | 55% | 9.5% | 5.3% |
| Timestamped scene list / bar list | 4.2% | 5.7% | 35% | 4.1% | 1.8% |
| Hex palette | 2.4% | 3.1% | 30% | 2.7% | 1.8% |
| Named font / typography | 5.4% | 6.2% | 55% | 5.4% | 7.0% |
| Easing / springs / cubic-bezier | 7.1% | 9.3% | 65% | 10.8% | 8.8% |
| Camera language | 8.0% | 8.8% | 75% | 9.5% | 8.8% |
| Transition language (mask, morph, match cut, wipe…) | 12.8% | 14.5% | 80% | 17.6% | 8.8% |
| Any audio (music/SFX/VO/TTS) | 23.8% | 23.3% | 75% | 23.0% | 14.0% |
| BPM / beat sync | 8.6% | 8.3% | 55% | 9.5% | 7.0% |
| Negations (no/never/avoid/don't) | 18.5% | 17.6% | **95%** | 17.6% | 19.3% |
| Explicit "Banned:"/"Avoid:" list | 1.5% | 2.1% | 20% | 0% | 5.3% |
| Deterministic / seek(t) / no timers | 3.0% | 4.1% | 35% | 2.7% | 7.0% |
| Frame capture (Playwright/headless/subframes) | 3.9% | 6.2% | 40% | 8.1% | 5.3% |
| Motion blur via subframes | 2.7% | 4.1% | 35% | 2.7% | 5.3% |
| Self-review loop (stills, contact sheet, inspect, verify) | 8.3% | 7.8% | 65% | 9.5% | 12.3% |
| Seamless loop (last frame = first) | 4.5% | 7.3% | 50% | 8.1% | 7.0% |
| Brand/real assets (logo, URL, repo, screenshots) | 30.4% | 29.5% | 80% | 28.4% | 26.3% |
| "Hook" / first-second demand | 3.6% | 5.2% | 30% | 5.4% | 5.3% |
| Must work muted / captions | 2.7% | 3.6% | 30% | 6.8% | 1.8% |
| "Don't invent / real data / accurate" | 3.3% | 3.6% | 25% | 5.4% | 0% |
| XML-style sections (`<inputs>`, `<build>`…) | 1.5% | 2.6% | 25% | 2.7% | 5.3% |
| Ask first / storyboard first | 3.6% | 4.7% | 35% | 4.1% | 5.3% |
| Persona ("motion designer", "world-class", "senior") | 21.7% | 31.1% | 5% | 35.1% | 5.3% |
| "Go all out / go crazy / go wild" | 20.8% | 33.2% | 15% | 37.8% | 1.8% |

**What this shows.** The dataset holds two kinds of prompt that barely overlap:

1. **Short "vibe" prompts** (65% of real prompts are under 40 words). These rest on persona plus stakes plus duration plus "go all out". In the under-40-word group, duration appears 57.9% of the time, "go all out" 38.1%, the showreel framing 33.3%, and persona 32.5%. Easing, camera, palette, fonts and fps each appear 0%. They work because Opus 5.5 fills in a whole house style by itself. Left to choose, it picks **Canvas** in 79 of 89 showreel-template outputs (89%).
2. **Production specs** (the 20 detailed prompts, about 10%). Almost all have negations (95%) and transition language (80%). Most have camera (75%), audio (75%), easing (65%) and a self-review loop (65%). Half or more set resolution, fps, aspect and fonts. These also carry the engineering contract (determinism, frame capture, subframe motion blur), which is almost absent elsewhere.

A skill can't depend on users writing the second kind, so it should **inject the production-spec layer itself** (see §8).

### 1.2 The skeleton shared by the best prompts

Read in full, the high-signal prompts converge on a common section order. howdevelop-733090, brainextends-606193, techhalla-498547, gdgtify-929495, twoclipping-402193/-000267/-496100, daniel-haida-636937, astrothewizard-618782 and verbove-268381 all follow it closely.

1. **Role and stakes.** "You are a world-class motion designer… Showreel stakes: if this is weak, you don't get hired" (techhalla-498547). "Apple-level product film… The film should feel expensive" (daniel-haida-636937).
2. **Inputs / source of truth.** Repo paths, brand token files, real screenshots, "accuracy guardrails" (howdevelop-733090), or an `<inputs>` block asking the user for assets (twoclipping family).
3. **Format and deliverables.** Exact duration ("exactly 15 seconds", "20.00s"), resolution, fps, aspect, safe area, MP4 plus editable source, file-size cap.
4. **Art direction.** Palette as hex, a 1–3 font system with roles, a materials and lighting mood, and "think X × Y × Z" reference blends.
5. **Locked copy.** The exact on-screen words in order, with "no extra slogans" (techhalla-498547, gdgtify-929495).
6. **Timeline.** A timestamped scene list (seconds or bars and beats), each entry naming a visual idea, its on-screen text and the transition logic.
7. **Motion rules.** Easing curves, spring damping and overshoot limits, stagger, enter/exit ordering, and camera vocabulary.
8. **Audio.** BPM, sound palette, sync rules, loudness target, licensing.
9. **Banned list.** Explicit clichés to avoid.
10. **Engineering contract.** `seek(t)` pure function, closed-form springs, no timers or CSS transitions, subframe motion blur, Playwright + ffmpeg.
11. **QA gate.** Render stills (one per beat or scene, or a contact sheet), inspect them, fix, render, then inspect decoded frames from the final MP4.
12. **Start instruction.** "Ask me for the inputs, then show me the state list on the beat grid before you write any code."

### 1.3 Ban lists, tallied by hand

Ten production-grade prompts carry a ban list: twoclipping-402193, annacher-433425, thegrootdev-966114, twoclipping-000267, twoclipping-496100, brainextends-606193, techhalla-498547, daniel-haida-636937, howdevelop-733090 and gdgtify-929495. Three of them (402193, annacher, thegrootdev) belong to the same template family.

| Banned item | Count of 10 | Examples |
|---|---|---|
| Particles / particle bursts / "particle spam" | **8** | twoclipping-402193, brainextends-606193, techhalla-498547, daniel-haida-636937 |
| Bouncy / elastic / cartoon easing | **7** | "Springs everywhere, a tiny overshoot at most" (twoclipping-402193); "overshoot below ~2%" (daniel-haida-636937) |
| Glows / neon glows | 5 | twoclipping-000267, twoclipping-496100 |
| "Anything that looks like a template" / generic dashboards | 5 | twoclipping-402193, daniel-haida-636937 |
| Dead time / long blank intervals / holds >1s | 5 | twoclipping-496100 ("holds longer than 1s"), brainextends-606193 |
| Gradients on UI chrome / soft gradients | 4 | techhalla-498547, thegrootdev-966114 |
| Stock footage / stock HUD | 4 | howdevelop-733090, gdgtify-929495 |
| Crossfades / blur-ins / arbitrary full-frame fades | 3 | twoclipping-496100, brainextends-606193, daniel-haida-636937 |
| Camera shake | 3 | twoclipping-000267, brainextends-606193, gdgtify-929495 ("pressure comes from the layout, not camera shake") |
| Glitch / RGB split (as a default) | 3 | twoclipping-000267, howdevelop-733090, daniel-haida-636937 |
| Spinning logos / 3D flips / spin transitions | 3 | howdevelop-733090, twoclipping-496100, daniel-haida-636937 |
| Mismatched icon strokes | 3 | twoclipping-402193 family |
| Generic AI clichés (brains, robots, sparkles, purple/blue neon) | 3 | techhalla-498547, daniel-haida-636937 |
| Long paragraphs / tiny unreadable code | 3 | techhalla-498547, howdevelop-733090, daniel-haida-636937 |
| Lens flares; shockwave rings | 2 each | twoclipping-000267, brainextends-606193 |
| Text and frames in corners ("typical AI giveaway") | 2 short prompts | souravbhar871-477361, 1littlecoder-378066 |

**The bans also show what is the default failure.** If a prompt says nothing, the model drifts toward particles, glows, bouncy springs, crossfades and corner HUD text. Every premium prompt switches those off.

---

## 2. Tech stack statistics

### 2.1 `tech_tags` frequency (all entries, including duplicates)

| Tag | Motion (n=317) | Explainer (n=67) | 3d (n=59) | Motion, highlighted (58) |
|---|---|---|---|---|
| canvas | 218 (68.8%) | 41 (61.2%) | 37 (62.7%) | 45 (77.6%) |
| svg | 159 (50.2%) | 34 (50.7%) | 17 (28.8%) | 27 (46.6%) |
| gsap | 77 (24.3%) | 15 (22.4%) | 2 (3.4%) | 18 (31.0%) |
| css | 57 (18.0%) | 5 (7.5%) | 4 (6.8%) | 5 |
| threejs | 37 (11.7%) | 16 (23.9%) | 48 (81.4%) | 5 |
| shader (GLSL) | 28 (8.8%) | 13 (19.4%) | 33 (55.9%) | 7 |
| particles | 18 (5.7%) | 1 (1.5%) | 2 | 3 |
| audio (audio-reactive / synth visual) | 11 (3.5%) | 8 (11.9%) | 4 | 2 |
| ai-image | 6 (1.9%) | 4 (6.0%) | 0 | 2 |
| webgl | 6 | 0 | 3 | 3 |
| physics / pixel | 3 / 3 | 3 / 0 | 0 |, |

Average tags per video: motion 1.97, explainer 2.09, 3d 2.54.
Top combinations:
- Motion: canvas alone (75), canvas+svg (30), gsap+svg (29), svg alone (28), canvas+gsap+svg (17).
- Explainer: canvas (10), svg (9), canvas+svg (6), gsap+svg (5), canvas+shader+threejs (5).
- 3d: canvas+shader+threejs (14).

**Explainers use three.js and shaders about twice as often as motion pieces** (23.9% vs 11.7%, and 19.4% vs 8.8%). The reason is the science and "take-apart" topics: black holes, rocket engines, CPU-to-atom zooms.

### 2.2 Production tools named in the text (prompts and posts, 384 M+E entries)

| Tool | Mentions | Share |
|---|---|---|
| Remotion | 86 | 22.4% |
| HyperFrames | 31 | 8.1% |
| ffmpeg | 16 | 4.2% |
| Playwright | 12 | 3.1% |
| ElevenLabs (VO/music/SFX) | 10 | 2.6% |
| numpy (beat analysis / synthesis) | 8 | 2.1% |
| three.js | 8 | 2.1% |
| Python music synthesis ("score synthesized in Python") | 7 | 1.8% |
| Gemini TTS | 5 | 1.3% |
| GSAP (named in text) | 4 | 1.0% |

Almost all Remotion and HyperFrames mentions come from posts. Real prompts mention them rarely (Remotion 1.6%, HyperFrames 0.5%), because the tool is usually set up beforehand as a skill.

### 2.3 What each stack is best at, according to the prompts and the results

| Stack | Best for | Evidence |
|---|---|---|
| **Canvas 2D** (single `draw(t)`) | Default for free-form showreels, particles, pixel art, hand-drawn and whiteboard, collage, simulations (random walk, sand, cellular), procedural characters. Full per-pixel control and deterministic. | 89% of showreel-template outputs; verbove-268381 "One HTML file. One canvas. One draw(t) function"; majidmanzarpour-927543 (128×96 logical res, integer blit); astrothewizard-618782 |
| **SVG** (+ GSAP or a seek-driven timeline) | Kinetic type, line-draw (stroke-dashoffset), icon and UI rebuilds, logo tracing, morphing shapes, charts, glyph-path deformation, liquid glass (feDisplacementMap) | gdgtify-929495 ("Use actual glyph paths for structural words"); ik-builds-585923 (Caveat handwriting via stroke-dashoffset); aschapmann-724497 ("trace the logo to SVG"); twoclipping-496100 (feImage displacement) |
| **GSAP** | Timeline choreography, stagger, product launch reels. Must be seek-safe ("Set every from-state at t=0") | gsap+svg is the #3 motion combo; ik-builds-585923 ("HyperFrames + GSAP") |
| **HTML/CSS DOM** | UI mockups and product screens rebuilt from real tokens, masked text reveals, device frames. Avoid CSS transitions when rendering offline | iamtanzil-120030 (word pull-up keyframes); daniel-haida-636937 ("recreate it faithfully in React from the real design system") |
| **three.js** | Real depth: scale dives (desk→atom, Earth→universe), exploded mechanisms, product objects, 3D carousels, toon-outlined hero objects | acoramaa-053577, kgonia7-746268, konstantinsaifo-501736, op7418-814408 (toon + normal/depth edge outline) |
| **GLSL / WebGL shaders** | Psychedelic and hypnotic backgrounds, fluids, fire, CRT and film grain, sky and water, fractals | monokern-832979, johnsavage-ai-427263, nathanwilbanks-981110, zeezomb-726206 (WebGL2 mosaic, no libs) |
| **Remotion / HyperFrames** | Packaging: frame-accurate render, React components, one codebase cut to 30s/15s/6s in 16:9 and 9:16 | l3d1c-632524, dengent-412996 (JP/EN versions from the same code via props) |
| **Python / numpy audio** | Beat-grid analysis of a supplied song, synthesized score and SFX, peak-aligned SFX placement, loudness | twoclipping-402193, apoorvjain25-309680 ("the track reads the same beat file as the visuals") |

---

## 3. Technique catalog (38 reusable scene types)

"Dur." is typical on-screen duration. Where a prompt gives a value it is cited; values marked "≈" are my inference from the surrounding timing (§6).

| # | Technique | One-line description | Use it in a YouTube/Shorts edit when… | Dur. | Tech | Example slug |
|---|---|---|---|---|---|---|
| 1 | **Kinetic type slam** | 1–4 word display line slams in on a spring with a smear trail, landing on the beat | Cold open or hook line, or a punchline the speaker says | 0.4–2.5s ("0.0–2.5s COLD OPEN") | Canvas/SVG, per-glyph spring | techhalla-498547 |
| 2 | **Masked word-by-word rise** | Each word rises out of an overflow-hidden mask line, staggered | Subtitles-as-design, title cards, quotes | 0.6s per word, 0.08s stagger | CSS/SVG | iamtanzil-120030 |
| 3 | **Hook word-by-word on beats** | Hook phrase lands one word per beat | First bar of a Short | 1 bar = 2s at 120 BPM | DOM/Canvas | twoclipping-000267 |
| 4 | **Glyph scramble → snap** | Letters shuffle (seeded Fisher–Yates) then lock on the beat | Reveal a stat, name or keyword | ≈0.5–1s | Canvas | techhalla-498547 |
| 5 | **Letterform mask wipe** | The outgoing word's outline becomes the mask that reveals the next line | Contrasting two statements ("X isn't expensive… Y is") | ≈0.5s | SVG path mask | techhalla-498547 |
| 6 | **Print misregistration / RGB split on impacts** | Offset duplicate layers (±2–4px) only on accent frames | Punctuating hits without a full glitch look | 1–3 frames | Canvas | techhalla-498547; pound75423-464968 |
| 7 | **Typography as architecture** | Words take structural roles (lintel, support, platform) and build the composition | Quotes, manifestos, spoken-word moments | 2.5–3.5s per line | SVG glyph paths | gdgtify-929495 |
| 8 | **Handwriting / marker draw-on** | Notes and underlines draw on via stroke-dashoffset | Annotating screenshots, circling a key number | ≈0.5–1s | SVG | ik-builds-585923 |
| 9 | **Line-art illustration draw-on** | Line SVG of each event draws itself in | Timelines, history explainers | ≈1s per item | SVG | rpa-dake-593915 |
| 10 | **Year/date slam with 3D spin** | Neon year numerals spring-rotate in and "slam" | History and timeline montage | ≈0.75s per year (15s for 1996–2015) | Remotion spring | rpa-dake-593915 |
| 11 | **One-shape morph ("one shape, never cut")** | A single container morphs size, radius and colour through every UI state while content swaps with a short blur | Product demos, app feature tour, loopable promo | 1 beat (0.5s) per state; 7 bars ≈ 14s | SVG/Canvas, closed-form springs | twoclipping-402193 |
| 12 | **Cursor-driven UI demo** | A visible cursor clicks, types and drags with direct manipulation | Any "here's how it works" software segment | Per action ≈0.5–1s | DOM/SVG | verbove-268381 |
| 13 | **Dual-spring stretchy indicator** | Leading and trailing edges on different springs, so tabs and toggles stretch | Micro-polish inside UI scenes | ≈0.3s | Springs | twoclipping-402193 |
| 14 | **Type-into-search / ⌘K filter** | Field types a query, results filter, one is selected | Show a search or command feature | ≈0.9s ("4.9–5.8s") | DOM/SVG | brainextends-606193; annacher-433425 |
| 15 | **Chart draws itself + tooltip** | Bars/lines draw on the beat, hover tooltip appears | Data or proof points | ≈1–2 beats | SVG | thegrootdev-966114 |
| 16 | **Counter roll-up / real-time timer** | Numbers count up; a hero number "resolves crisply" | Stats, prices, "0–100 in 3.4s" | equals the real value (3.4s) | Canvas/DOM, mono font | dys-hay-749645; daniel-haida-636937 |
| 17 | **Object-driven (shared-element) transition** | An element from scene N becomes scene N+1 (chart line → document edge, number → invoice amount) | Between B-roll beats, so cuts feel inevitable | ≈0.3–0.6s | any | daniel-haida-636937 |
| 18 | **Persistent anchor element** | One element (player bar, mascot eyes) stays across shots to tie them together | Multi-scene explainers; brand continuity | whole piece | DOM | brainextends-606193; leowenai-125931 |
| 19 | **Flood / contract transition** | A shape overscales past the corners, holds black for a beat, contracts into the next scene | Section breaks, the drop | ≈0.3s flood + 1 beat hold | SVG/Canvas | twoclipping-496100 |
| 20 | **Iris / aperture open** | 6-blade iris closes over a label and snaps open on a photo | Reveal a photo, product or speaker | ≈0.5s | SVG geometry | twoclipping-496100 |
| 21 | **Circle-out-of-button reveal** | A circle expands from a UI button into a new dark scene, on the drop | Mood or section change synced to music | 1 beat | DOM | twoclipping-000267 |
| 22 | **Screen-Studio camera zoom** | Camera reframes so each state fills the frame; cursor scales with it | Any screen recording or UI scene | 0.5–1s | CSS transform camera | twoclipping-496100; verbove-268381 |
| 23 | **Slow continuous camera over a desktop** | One camera, no cuts; windows pile in from behind the camera, then fly past | Product teasers, "calm premium" pacing | moves 1.5–3s each | DOM + motion blur | jake11moran-414633 |
| 24 | **Zoom-out-to-a-point / zoom-in-to-device** | Desktop recedes to a dot in space, then the camera dives into a phone | Cross-platform reveal, scale change | ≈2–4s | Canvas | dale-vaz-879074 |
| 25 | **Infinite zoom through portals** | Exponential zoom to a fixed point; each object's glass holds the next world | Hypnotic intros, loops, transitions between topics | segment ∝ log(zoom); 20s loop | Canvas + depth layers | koldo2k-778767 |
| 26 | **Powers-of-ten scale dive with ruler** | One continuous shot from human scale to atoms (or the universe) with an on-screen scale ruler | "How small/big is X" explainers | 20–38s | three.js + shaders | acoramaa-053577; kgonia7-746268 |
| 27 | **Perspective UI entrance** | Interface rises with a subtle tilt and settles frontal; floating covers with depth order | Showing an app screen without a flat "screenshot slide" | ≈0.9s ("1.5–2.4s") | CSS 3D | brainextends-606193 |
| 28 | **3D carousel + floor reflections + whip** | Real clips on a carousel, motion-blurred whip onto the hero clip | Showing many examples, testimonials, a portfolio | 1 bar | CSS 3D / three.js | twoclipping-000267 |
| 29 | **Device frame build** | Lock screen pulls back into a phone as the bezel grows; Dynamic Island morphs into a Mac window | Mobile↔desktop transitions | ≈1–2 beats each | SVG/DOM | twoclipping-496100; wani-shola-459278 |
| 30 | **Break-out-of-frame** | A feature or poster escapes its frame and changes the world around it | Make app recordings dynamic; thumbnails come alive | ≥2.5s per feature | Canvas/DOM | bilimfili1-459762; pankajkumar-dev-718609 |
| 31 | **Liquid glass / goo** | Displacement-map glass with chromatic edges; goo via blur + alpha threshold | Premium Apple-style UI moments | ≈1–2 beats | SVG filters | twoclipping-496100 |
| 32 | **Logo assembly** | Wireframe logo, low-poly shards fly in one by one, then the brand name types out (or a gold glint reveals the mark) | End card, intro sting | 1.2–3s ("0.00–1.20" glint) | Canvas/three.js | mounnna-497266; daniel-haida-636937 |
| 33 | **Wordmark squeeze / accordion** | Letters compress into the period, the dot grows into a pill, a label rises inside | Brand open/close; loop seam | ≈1 bar | SVG + variable font wdth | twoclipping-496100 |
| 34 | **Beat-cut montage with flashes** | Cut every beat, white flash strongest on the downbeat, big keyword flash ~0.4s in difference blend, effect intensity by section (40/70/100%) | Music-video or "brainrot" Shorts segments | 0.5s per cut at 120 BPM | Canvas | pound75423-464968 |
| 35 | **Paper / halftone / collage look** | Newspaper cutouts with halftone, white paper border, soft shadow, grain, vignette, flicker; cutouts on twos (15fps) | Stylized explainers, editorial B-roll | style | Canvas | koldo2k-778767; leowenai-125931 |
| 36 | **Hand-drawn whiteboard / pencil + chromatic aberration** | Sketchy pencil drawings revealed stroke by stroke | Teaching abstract concepts | scene-length | Canvas | tak3sh8-441895; groundcontrol-230877 |
| 37 | **Real simulation as the visual** | The thing being explained is actually simulated (random walk, fire, collisions that play notes) | Science explainers where accuracy is the hook | scene-length | Canvas/WebGL | astrothewizard-618782; kamstudiolabs-440893 |
| 38 | **Spinning list / ticker that lands** | Fast list of ~30 items (unreadable on purpose), slows and lands on one, then "?" pops 0.2s later | Building to a punchline or the product's niche | ≈2–3s | DOM | jake11moran-414633 |
| 39 | **Checklist with rings and ticks drawing on** | The post's claims become a checklist; rings and ticks stroke in | Recap or end card | ≈2s | SVG | jake11moran-414633 |
| 40 | **Mascot / character with eyes as anchor** | A character's eyes follow the action and blink on the beat, then land on the logo | Brand personality throughout | whole piece | Canvas/SVG | leowenai-125931; astrothewizard-618782 |

Also seen and transferable from 3d/interactive:
- Toon-shaded hero object with post-process normal+depth edge outlines, plus a five-phase "reward reveal": anticipate, level up, charge (~1s), burst, reveal (op7418-814408).
- Pixel-art quantized motion: 128×96 logical canvas, integer snapping, 8–12fps feel inside 60fps (majidmanzarpour-927543).
- Scroll-scrub style video choreography: overlays gated by video-time windows (iamtanzil-675031).

---

## 4. Explainer patterns

### 4.1 How explainer prompts build the narrative

- **Hook.** Only howdevelop-733090 (motion, explainer-style) and the reel prompts name a hook explicitly: "0:00–0:02, Hook: A single prompt cursor blinks… 'What can one AI API become?'" Among explainer prompts the hook is usually implied by the subject: a question, a character, or an extreme scale.
- **Concept → steps.** "how it works in 3 steps" (alex-prompter-997524); "steps are: 1. connect your agent 2. … 3. go live!" (mattbean-917572); a user journey of 7 chained actions (charlesmendez-476517).
- **Payoff / landing.** "my name at the end" (alex-prompter-997524); "All paths converge into a bold final composition… Hold the final frame long enough to read it" (howdevelop-733090); "Finally the camera zooms out… ends in Single Screen Trading" (dale-vaz-879074).
- **Accuracy as a feature.** "Make it genuinely educational and accurate… Include real numbers… and be honest about uncertainty" (astrothewizard-618782); "physically accurate strain profile included" (kureshirfan-386691); "Never invent facts, numbers or quotes" (stokebuilder-356793).
- **Attention devices.** "Use humor and visual gags to keep attention: onomatopoeia, little characters, callbacks" (astrothewizard-618782). "Give the photon a personality." "Put what was happening on Earth during those 100,000 years alongside the photon's timeline", which is a parallel-timeline device.

### 4.2 Pacing (from prompts that give numbers)

- Explainer scene length runs about **3–6s**: alex-prompter-997524 asks for 30s with 5 scenes (6s per scene); howdevelop-733090 uses 2–3.5s per scene.
- Brand reels run about **1s per idea** (brainextends-606193: "Most visual ideas last approximately one second").
- Narrated explainers sync visuals to phrases. tetsu-tetsu333-576886 split narration into **32 phrases for a 52s video**, about 1.6s per on-screen change: "話した瞬間に画面とテロップが出るよう自動で同期" (screen and captions appear the moment it's spoken).
- Typical durations: 30s is the modal request (ror-fly, sarut0bisasuke, alex-prompter, sudo-kiran); 30–60s for stories (retropunkai, tony-tt, tomandrieu); 60s for the most detailed one (astrothewizard-618782).

### 4.3 Labeling

- Ingredient and measurement labels appear as each item enters (ror-fly-880547).
- On-screen copy limited to "chat() · 24 providers", "Agents · Sandboxes · MCP" (howdevelop-733090): dot-separated noun stacks of 2–4 words.
- Scale ruler always visible (acoramaa-053577).
- Burned-in captions, because viewers watch muted (astrothewizard-618782).
- Bilingual text when needed ("write in traditional chinese and english", eric-khun-667455).

### 4.4 How abstract ideas are made visible

- **Simulation over illustration**: "the random walk should be an actual random walk, not a drawing of one" (astrothewizard-618782).
- **Metaphor objects**: a token bucket rate limiter as a literal bucket (parkerrex-701462); "stochastic parrot" for "just predicting tokens" (doubleunplussed-181894); a coding agent as a loop (arthurkatcher-604161).
- **Continuous scale zoom** for size and hierarchy (acoramaa-053577).
- **Take-apart / cutaway** for mechanisms (konstantinsaifo-501736: "Cut it open, follow the oxygen and the methane through both turbopumps, then throttle it").
- **Style-shift** for self-referential ideas (emollick-019567: "every explanation about recursion has a radically different video style").
- **Every transition demonstrates a feature**: an interrupted stream "freezes, reconnects, and resumes from the same point" (howdevelop-733090).

### 4.5 Eight explainer templates

**T1. Problem → Solution 5-beat (30s).** Source: alex-prompter-997524.
1. Problem, 0–6s: show the pain, ideally the viewer's own situation.
2. What we do, 6–12s: one sentence and one hero visual.
3. How it works, 12–22s: 3 numbered steps, each a cursor action or object change.
4. Proof, 22–26s: one number, rolled up.
5. Name / CTA, 26–30s: logo lockup, held.

Bold text, brand colours, smooth transitions.

**T2. Process build (recipe / assembly), 30s.** Source: ror-fly-880547, sarut0bisasuke-069973. Start from an empty container and add one ingredient or component per beat. Each addition carries a label and quantity. End on the completed object as the payoff.

**T3. Scale dive (powers of ten), 20–40s.** Source: acoramaa-053577, kgonia7-746268, irinatoxi-962937, koldo2k-778767. One continuous shot, no cuts, with a persistent scale ruler or unit readout. Each "layer" gets a segment whose duration is proportional to log(zoom), so speed feels constant. Land on the smallest or largest thing.

**T4. Character-led science story, 60s.** Source: astrothewizard-618782. Personify the subject. Simulate the real process. Show real numbers with uncertainty. Run a parallel timeline for context. Use gags and callbacks. Add VO, burned-in captions, a score that changes per scene, and SFX synced to every bounce or pop. The music ducks under the voice.

**T5. Timeline slam (history), 15–60s.** Source: rpa-dake-593915, retropunkai-277590, kloss-xyz-067876. Year numerals spring-slam in; a line-art SVG of each event draws on; close with a one-line thesis. Creator's note: "歴史ものの勢いは、情報量より場面を叩きつける間で決まる" ("momentum in history pieces is set by the gap between slams, not by information density").

**T6. User-journey walkthrough, 15–45s.** Source: charlesmendez-476517, mattbean-917572, howdevelop-733090. Chain the steps so each step's output becomes the next step's input (shared element). A cursor drives the action. Each transition shows a feature. On-screen copy is 2–4 word noun stacks.

**T7. Take-apart / exploded mechanism, 20–40s.** Source: konstantinsaifo-501736/-587629, stefanostraus-971191, iniyanai-856596. Show the whole object, explode or cut it open, trace the flow through parts, change one parameter, and show the consequence (e.g. "Drag the plasma from 15 million °C… to 150 million and watch a city light up"). Cut music to mechanical events ("used real switch recordings as the beats").

**T8. Talking-head / podcast B-roll inserts (long-form).** Source: stokebuilder-356793 and sab8a-475686 ("Cut a raw talking-head clip into a punchy, fun edit with subtitles, graphics and music"). This is the template closest to the skill's core use case. First pass: find every timestamp where a graphic could fill space or hook, aiming for **35–50 moments per episode, at least 2 per chapter**. Write a style bible and component kit before building. Keep copy verbatim or faithful. Sync beats to spoken words. Keep each graphic inside one uncut stretch of audio. Leave a few seconds of face between graphics. Keep the speaker in PiP bottom-right during full-screen graphics. Judge each graphic once, and fix only the egregious ones.

(A bonus template, T9 "kinetic spoken-word / quote card", follows gdgtify-929495: a phrase-based cue sheet, not a dance beat, plus at least one 400ms stillness.)

---

## 5. Quality-raising phrases and weak prompts

### 5.1 Phrases that recur in the best prompts (verbatim, short)

**Direction and taste**
- "ONE SHOT = ONE IDEA." (daniel-haida-636937)
- "one strong formal idea per scene" (astrothewizard-618782)
- "The visual confidence should come from restraint." (daniel-haida-636937)
- "I would rather have: 3 extraordinary visual moments than 10 mediocre feature animations." (daniel-haida-636937)
- "Every important frame should be good enough to use as a still advertisement." (daniel-haida-636937)
- "The goal is a memorable showreel, not a slideshow of feature bullets." (howdevelop-733090)
- "Every transition should visually demonstrate a feature, rather than simply replace one title card with another." (howdevelop-733090)
- "Make it feel meticulously art-directed rather than like a random collection of effects." (lukasersil-726495)
- "question your strategy and plan, if it doesn't feel like done by a pro designer, start over." (heyiammallik-293397)
- "Name what the product learns, never the abstraction." (ik-builds-585923)

**Transitions and continuity**
- "Of course the next scene came from that." (daniel-haida-636937)
- "One shape, never cut" (twoclipping-402193, and 6 copies)
- "Every scene is made out of the previous one: nothing fades, blurs or cuts." (twoclipping-496100)
- "Outgoing titles must disappear before incoming titles occupy the same space" (brainextends-606193)
- "Content enters after its container starts morphing and leaves before the next morph so text never overlaps" (verbove-268381)
- "Never fade black directly into the accent color. Move an accent element between states instead" (verbove-268381)
- "One primary move per transition; no generic push/slide/rotate-swing." (ik-builds-585923)

**Motion feel**
- "Springs everywhere, a tiny overshoot at most." (twoclipping-402193)
- "overshoot below ~2%" and "cubic-bezier(0.16, 1, 0.3, 1)" (daniel-haida-636937)
- "Elements should not all start and stop at exactly the same frame." (daniel-haida-636937)
- "aim for half the speed you'd default to" (jake11moran-414633)
- "Allow at least one 400ms moment of absolute stillness." (gdgtify-929495)
- "Typography should move as designed objects." (daniel-haida-636937)

**Rhythm and audio**
- "Something happens on every beat." (twoclipping-402193 / verbove-268381)
- "a new idea every 1.5–2 s, a sound on every hit" (ik-builds-585923)
- "Place each sound effect so its measured peak, not its file start, lands on the event." (twoclipping-000267)
- "add one soft sound effect for every element that appears and silence otherwise" (aschapmann-724497)
- "every cut and transition must land on the beat." (prasenx-693512)
- "Do not force the speech onto a dance beat. Use a cue sheet based on phrases, pauses, and emphasis." (gdgtify-929495)
- "Master -14 LUFS, -2 dBTP, re-measured after AAC encode." (ik-builds-585923)

**Truth and assets**
- "Real UI. Real data. No placeholders." (verbove-268381)
- "Do not invent screens. Do not invent metrics that imply real customer data." (daniel-haida-636937)
- "Never invent facts, numbers or quotes." (stokebuilder-356793)
- "avoid using screenshots as raw; instead, break them down into components/icons so we can animate those too" (ho-ba-761062)
- "trace the logo to SVG so it stays sharp and can be animated" (aschapmann-724497)
- "Use real, editable typography and vector-style graphics. Do not rely on AI-generated text inside images." (howdevelop-733090)

**Engineering contract**
- "every frame a pure function of time so my renderer can screenshot it." (parkerrex-701462)
- "Every style is computed from time inside seek(t): no CSS transitions, no timers, no state carried between frames." (twoclipping-402193)
- "Springs are closed-form step responses… the sum of one spring per change" (twoclipping-402193)
- "Set every from-state at t=0 (seek-safe); never cover an exit." (ik-builds-585923)
- "Never put will-change on anything the camera scales or the text renders blurry." (twoclipping-402193)
- "Never set opacity or filter on a preserve-3d element… Fade its wrapper instead." (twoclipping-000267)
- "A flood must overscale past the corners and take about 0.3s, or half the screen changes in one frame." (twoclipping-496100)
- "Export the interval [0, duration) without duplicating the endpoint frame." (thegrootdev-966114)

**QA gate**
- "Render one frame per beat before the full render. Fix anything off the grid, cramped or hard to read." (twoclipping-402193)
- "Do not declare success because the code compiles. The deliverable is the FILM." (daniel-haida-636937)
- "Inspect multiple exact decoded frames from the final MP4, not only browser screenshots." (daniel-haida-636937)
- "scan for single-frame pops (frame-difference spikes 3x their neighbours)" (twoclipping-496100)
- "Don't hand me a first draft. Hand me something you'd put your name on." (astrothewizard-618782)

**Distribution**
- "The story must also work muted." / "keep important content within a 9:16-safe central area" (howdevelop-733090)
- "Keep text clear of the TikTok/Instagram interface." (bilimfili1-459762)
- "Avoid the frames and texts on the corners which are typical ai made giveaways!" (souravbhar871-477361)

### 5.2 The viral baseline prompt and why it works

"make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out." This prompt appears **89 times** in the dataset: 86 in motion, 2 in 3d, 1 in explainer. 34 entries copy it exactly, and the rest are variants with a topic or brand appended.

It packs in, in 26 words:
- a hard duration,
- a persona with taste stakes ("showreel for a résumé"),
- an output genre ("motion graphics"),
- permission for maximum effort.

One creator reported that rerunning with it made the output "far better" (elliot-garreffa-446825).

Its weakness is that it is topic-free. Variants add "about [topic]", "brand colours", "1s hook, loop" (ishaaqahamed-107563) or "sound synced to the cuts" (polydao-566862).

### 5.3 Weak or vague prompts, and why

| Prompt (slug) | Why it's weak |
|---|---|
| "Go all out." (sudo-kiran-696074) | No subject, duration, format or audience. All taste, no target. |
| "make a video that could go viral." (kantamk-176511) | Outcome without mechanism: no hook, length or platform. |
| "make a 4-minute animated short that blows my mind." (faroukzy-138551) | Long duration with no structure. Code animation is strongest at 10–30s; only 2 of 165 duration mentions exceed 2 min. |
| "...it has to be best of the best of the best of the best video" (sudo-kiran-335993) | Repeated superlatives in place of specs. |
| "make educational video out of article." (henkvaness-975279) | No audience, length, style or what to keep. |
| "Build me something when people see it, they will say 'Wow'…" (miaai-lab-774895) | No medium ("This can be a video, or anything else"), no duration, no topic. |
| "Make a ODATANO edit that goes hard" (maxalexweber-459784) | Relies on slang and assumes brand knowledge. |

The outcome reports bear this out:
- sachaarbonel-673648, follow-up: "This is not a professional-looking video… it is a bit too fast and bumpy" and "You are clearly not a good song maker."
- apoorvjain25-150112: "the first cut was weak until I pushed back."
- timguignard-623571: "the result is ok. Not crazy, but with a few more indications and a clear direction, it would probably get much nicer."
- mattworkman-309357: "very blah text design."
- jarvis11x-544635: asked why their output "满满的像素感" (looks pixelated). This suggests missing resolution, DPR or render settings.

The strong prompts fix these exact failures. They pin speed ("half the speed you'd default to"), set type rules (a font system with roles), give audio specs, and specify supersampling ("1.5 倍超采样", op7418-814408; "Render true 60 fps with spatial antialiasing", brainextends-606193).

---

## 6. Timing data

| Parameter | Value | Source slug |
|---|---|---|
| Requested total duration | 15s = 92 of 165 duration mentions (55.8%); ≤20s = 70.3%; 30s = 23; 20s = 14; 60s = 9; 10s = 7 | computed over all M+E entries |
| Ideas per second (brand reel) | "Most visual ideas last approximately one second" | brainextends-606193 |
| Ideas per second (launch film) | "a new idea every 1.5–2 s" | ik-builds-585923 |
| Spotify 18s timeline | 16 segments: 0.6, 0.9, 0.9, 0.8, 0.8, 0.9, 0.9, 0.8, 0.9, 0.8, 1.5, 1.4, 1.3, 1.5, 1.2, then a 2.8s final hold. Mean 1.125s; the first 10 average 0.83s | brainextends-606193 (computed) |
| Taxtello 15s timeline | 1.2 / 3.2 / 3.1 / 3.2 / 2.1 / 2.2s. About 4 visual ideas per 15s | daniel-haida-636937 |
| TanStack 15s timeline | 2 / 2 / 2.5 / 2.5 / 2.5 / 3.5s (final reveal longest) | howdevelop-733090 |
| TechHalla 20s bumper | 2.5 / 4 / 4 / 4 / 3 / 2.5s | techhalla-498547 |
| Spoken-word 20s | 3 / 3.5 / 3.5 / 2.5 / 3.5 / 2 hold / 2 loop | gdgtify-929495 |
| Explainer scene length | 30s ÷ 5 scenes = 6s | alex-prompter-997524 |
| Min on-screen time per feature | "at least 2.5 seconds" | bilimfili1-459762 |
| First premium frame / first product moment | "first 1.5 seconds must already look premium"; product "by ~2 seconds"; "No five-second logo intro" | daniel-haida-636937 |
| Hook | "open with a striking hook in the first second"; "1s hook" | reflex-cloud-304046; ishaaqahamed-107563 |
| Music tempo | 120 BPM in 30 of 32 BPM mentions; also 115–120, 96 and 140 | computed; daniel-haida-636937; koldo2k-778767 |
| Beat / bar at 120 BPM | 1 beat = 0.5s; 1 bar = 2s; "7 bars: 28 beats ≈ 14 seconds"; "10 bars at 120 BPM, 2 seconds each"; 54 beats ≈ 27s | thegrootdev-966114; twoclipping-000267; twoclipping-496100 |
| Event density | "Something happens on every beat" (every 0.5s); "every beat for the first 16 beats; after that, every other beat" | twoclipping-402193; techhalla-498547 |
| Kinetic-type stagger | "1/16 note at 120 BPM (125ms)" | techhalla-498547 |
| Word pull-up | 0.6s per word, 0.08s stagger, translateY 20px→0 | iamtanzil-120030 |
| Per-character reveal | 0.05s stagger, 0.6s each, y 50→0 | iamtanzil-675031 |
| Supporting copy fade-up | 0.8s, delays 0.5s then 0.7s, cubic-bezier(.16,1,.3,1) | iamtanzil-120030 |
| Camera moves (calm style) | "1.5 to 3 seconds on gentle ease-in-out curves" | jake11moran-414633 |
| Text hold before transform | "Hold it about a second"; "?" pops 0.2s after landing | jake11moran-414633 |
| Max hold (energetic style) | banned: "holds longer than 1s" | twoclipping-496100 |
| Final hold | "Hold the final frame long enough to read it"; "final frame must have enough stillness to register"; 2.8s in Spotify | howdevelop-733090; daniel-haida-636937; brainextends-606193 |
| Stillness beat | "at least one 400ms moment of absolute stillness" | gdgtify-929495 |
| Flood transition | "about 0.3s" | twoclipping-496100 |
| Big-word flash | "約 0.4 秒" (about 0.4s) per bar | pound75423-464968 |
| Cut rate (music video) | "1 拍ごとにカットを切り替える" (cut every beat) | pound75423-464968 |
| Effect intensity by section | intro 40%, verse 70%, chorus 100% | pound75423-464968 |
| Shake settle | "a small shake that settles within half a second" | alexwtlf-981005 |
| Camera punch-in | scale 1.0→1.08, on beats only | techhalla-498547 |
| End micro-breath | scale 1.000→1.012→1.000 | techhalla-498547 |
| Overshoot cap | "overshoot below ~2%" | daniel-haida-636937 |
| Misregistration offset | ±2–4px, impact frames only, 40% opacity | techhalla-498547 |
| Charge / anticipation | "蓄力（约 1 秒）" (charge ≈1s) before a burst | op7418-814408 |
| Narration sync unit | 52s video split into 32 phrases (≈1.6s per phrase change) | tetsu-tetsu333-576886 |
| On-screen words per second | No prompt states WPS. Derived: TechHalla locks 16 words over 20s (≈0.8 words/s); gdgtify shows 25 speech words over ≈16s (≈1.6 words/s); Taxtello caps copy at "~3–4 words" per scene | computed |
| B-roll density (long form) | 35–50 graphics per episode, ≥2 per chapter, "a few seconds of faces between graphics" | stokebuilder-356793 |
| Animation frame rates | 60fps in 33 fps mentions, 30fps in 6; cutouts "on twos" at 15fps; pixel art "8-12 fps feel" | computed; koldo2k-778767; majidmanzarpour-927543 |
| Motion blur subframes | 4 subframes (11 entries, 7 of them copies of one template), 3 at t−1/240, t, t+1/240 (twoclipping-000267, raphaelaubryy-687877), 6 (verbove-268381), "3–5" (brainextends-606193) | computed |
| Loudness | −14 LUFS (4 prompts); −2 dBTP | twoclipping-000267/-496100, raphaelaubryy-687877, ik-builds-585923 |
| Resolution / aspect | 1440×1440 square (10 mentions), 1920×1080 (12), 1080×1080 (3); 9:16 named 9×, 16:9 6× | computed |

---

## 7. The best full prompts, quoted

Prompts over 400 words are trimmed. "[…]" marks cuts; the remaining text is verbatim.

### 7.1 howdevelop-733090 (highlighted): TanStack AI 15s launch film

> Create and render a 15-second motion graphics video introducing TanStack AI. Make it feel like a premium developer-tool launch film produced by Studio1: fast, precise, visually surprising, and polished enough to open a keynote or lead a social campaign. […]
> Format and deliverables
> - 1920×1080, 30 fps, exactly 15 seconds; keep important content within a 9:16-safe central area.
> - Deliver the rendered MP4 and the editable project/source. […]
> - Use real, editable typography and vector-style graphics. Do not rely on AI-generated text inside images.
> - Add an original electronic sound design: a restrained opening pulse, tightly synchronized transition hits, rising momentum, and a satisfying final resolve. The story must also work muted.
> Visual direction
> Dark graphite canvas; luminous gradients and controlled flashes inspired by TanStack's identity. Crisp typography, kinetic code, layered interface fragments, streaming data, branching paths, and smooth camera moves with convincing depth. High contrast and immaculate spacing. Every transition should visually demonstrate a feature, rather than simply replace one title card with another. Keep all on-screen wording brief and legible. Avoid generic stock footage, spinning logos, fake dashboards, excessive glitch effects, and tiny code nobody can read.
> Exact 15-second sequence
> - 0:00–0:02, Hook: A single prompt cursor blinks. It sends one signal that expands into a network of possibilities. On-screen: "What can one AI API become?"
> - 0:02–0:04, Core and providers: The signal resolves into chat(); provider nodes connect and swap rapidly without breaking the central flow. On-screen: "chat() · 24 providers"
> - 0:04–0:06.5, Multimodal: One continuous stream transforms into text, waveform, image frame, and video timeline. On-screen: "One pattern. Every modality."
> - 0:06.5–0:09, Agents and tools: The stream branches into sandboxed agent runs, then reaches external tools through MCP. […]
> - 0:09–0:11.5, Reliability: An interrupted stream freezes, reconnects, and resumes from the same point; a clean type-check confirmation snaps into place. On-screen: "Persistent. Durable. Type-safe."
> - 0:11.5–0:15, Reveal: All paths converge into a bold final composition: "TanStack AI" followed by "Build what's next." […] Hold the final frame long enough to read it.
> Accuracy guardrails
> […] Do not call it a stable v1 release. Do not present planned orchestration features as already shipped.
> Make the video, inspect the rendered result, and fix any clipped text, weak transitions, mistimed beats, or unreadable frames before delivering it. The goal is a memorable showreel, not a slideshow of feature bullets.

**Why it's excellent.** Every scene has a time range, a visual metaphor that demonstrates the feature, and an exact caption. It adds a 9:16-safe area, a muted-viewing requirement, accuracy guardrails, a specific ban list, and a closing self-QA instruction. It is the cleanest one-page template in the dataset.

### 7.2 twoclipping-402193: "One shape, never cut" UI film

The most reused production template (7 copies across motion and 3d).

> <direction>
> Dribbble-level UI motion. One shape, never cut: every state is the same element morphing its size, radius and color while its content swaps with a short blur. A cursor drives every change with real clicks and drags. Light warm-gray canvas, black and white components, one clean UI font (Geist). Springs everywhere, a tiny overshoot at most. The camera zooms so each state fills the frame. The last frame is the first frame, so it loops.
> Banned: bouncy easing, particle bursts, glows, gradients on UI chrome, mismatched icon strokes, dead time, anything that looks like a template.
> </direction>
> <structure>
> 120 BPM, 7 bars, something happens on every beat.
> Button → loader → check → dynamic island → music player with a play/pause morph → scrub the progress bar → it becomes a volume slider that stretches when dragged past max → a toggle flips on the beat → the knob becomes a liquid tab indicator → the tabs open into a chart that draws itself, with a tooltip on hover → it collapses into ⌘K → type to filter → enter → toast → back to the button.
> </structure>
> <build>
> 1. One HTML file, square 1440x1440. Every style is computed from time inside seek(t): no CSS transitions, no timers, no state carried between frames.
> 2. Springs are closed-form step responses. A value that changes target many times is the sum of one spring per change, so it stays a pure function of time.
> 3. The tab indicator's two edges ride different springs, so the leading edge stretches ahead of the trailing one. Same trick for the toggle knob.
> […]
> 5. Analyze the song with numpy for the beat grid and start on a downbeat. Place every UI sound by its measured peak.
> 6. Render with Playwright: 4 subframes per frame, blended with ffmpeg tmix for motion blur at 60fps.
> 7. Render one frame per beat before the full render. Fix anything off the grid, cramped or hard to read.
> </build>
> <gotchas>
> Never put will-change on anything the camera scales or the text renders blurry. Text that swaps inside a morphing container needs its own enter and exit timing or it overlaps. Make the last frame identical to the first, cursor position and speed included, or the loop stutters.
> </gotchas>
> <start>
> Ask me for the inputs, then show me the state list on the beat grid before you write any code.
> </start>

(The `<inputs>` block asking for 8–12 UI states, one accent colour and a 120 BPM royalty-free song is omitted.)

**Why it's excellent.** One formal idea carries the whole film. The deterministic engine is spelled out: `seek(t)`, closed-form springs, a sum of springs for repeated retargeting. Timing is on a beat grid with measured SFX peaks. It builds in a preview gate, documents real browser gotchas, and asks for approval of a plan before any code is written.

### 7.3 brainextends-606193 (highlighted): Spotify 18s product film

> <deliverables> An 18-second MP4 at 1920×1080 and true 60 fps, with music and subtle sound effects […] Do not stop at a storyboard, still images, or an implementation plan </deliverables>
> <art_direction> […] Spotify green # 1ED760 for emphasis and controls One clean sans-serif font, such as Geist or Inter […] Text should feel like music-product advertising, not oversized presentation headings Do not add an outer caption, creator watermark, decorative footer, or progress counter </art_direction>
> <timeline> 0.0–0.6 seconds: A green Spotify icon grows smoothly into the center of the dark stage Give it a confident arrival with minimal overshoot
> 0.6–1.5 seconds: […] "Discover" "new music" […] Reveal them with short masked vertical movements
> 1.5–2.4 seconds: A stylized Spotify desktop interface rises into view […] Use a subtle perspective tilt during the entrance, settling toward a frontal view […]
> 8.3–9.8 seconds: Return to the dark stage The same artwork expands dramatically toward the camera, becoming oversized and cropped by the rounded stage […] Use controlled motion blur during the fastest part of the zoom […]
> 15.2–18.0 seconds: […] Hold the finished composition cleanly through the end </timeline>
> <persistent_player> […] This recurring player connects the changing shots […] </persistent_player>
> <motion_quality> Most visual ideas last approximately one second, but transitions remain smooth […] Favor critically damped springs or carefully tuned smooth easing No repeated bouncing or large elastic overshoots Preserve the hero artwork's identity and position relationships through search, album detail, brand tile, and zoom Use match-position transitions, coordinated scaling, masked reveals, and perspective Outgoing titles must disappear before incoming titles occupy the same space Avoid overlapping text, sudden camera resets, long blank intervals, and arbitrary full-frame crossfades […] No particles, shockwave rings, lens flares, camera shake, or unrelated stock footage </motion_quality>
> <audio> […] Align important entrances, selections, zooms, and the logo reveal with musical events Keep effects quieter than the music […] </audio>
> <implementation_and_validation> Build a deterministic animation driven by absolute time through an async window. seek(t) function […] Do not depend on live timers, accumulated physics, or CSS transition state during export Render true 60 fps with spatial antialiasing Use 3–5 temporal subframe samples per output frame for restrained motion blur Keep stationary text and artwork sharp Inspect contact sheets and moving playback […] Verify evenly spaced frame timestamps and the full 18-second duration […] </implementation_and_validation>

**Why it's excellent.** It is the most complete sub-second timeline in the dataset (16 beats in 18s). A persistent anchor element ties the shots together, and a hero asset keeps its identity through every transition. There is a precise "no overlap" rule for text, plus a validation spec that checks frame timing and duration.

### 7.4 techhalla-498547: kinetic identity bumper (20s, square)

> You are a world-class motion designer doing a 20.00s kinetic identity bumper for TechHalla […] This piece must feel like the best designer in the room made a street-poster that moves. Showreel stakes: if this is weak, you don't get hired.
> DURATION: exactly 20.00 seconds. LOOPABLE: frame 0 == frame last (position, opacity, cursor if any).
> FORMAT: one HTML file, 1080×1080 (square, X-native). 60fps.
> PALETTE (strict): bg # 0A0A0A / magenta # FF2BD6 / acid green # B8FF00 / white # F5F5F5 only for primary readable type when needed. No other hues. […]
> TYPE SYSTEM (use all three; never one font for everything): 1) Display / scream: Archivo Black […], 1–4 words max 2) Urban grotesque: Syne ExtraBold […] 3) Mono / "prompt code": IBM Plex Mono Medium, small labels […] Tracking: display −40 to −80; mono +20. […]
> MESSAGE (locked, do not soften, do not add filler slogans): 1. STOP SCROLLING 2. AI VIDEO ISN'T EXPENSIVE 3. BAD PROMPTING IS 4. WORKFLOWS > WISHES 5. STEAL THE PROMPT 6. @ TECHHALLA […]
> NARRATIVE ARC (20s): 0.0–2.5s COLD OPEN, "STOP SCROLLING" slams in from below with spring overshoot; magenta smear trail […] 2.5–6.5s THESIS A, […] Letters scramble (seeded Fisher–Yates per glyph) then snap on the beat. 6.5–10.5s THESIS B, "BAD PROMPTING IS" replaces it via mask wipe through the letterforms (the outgoing line is the mask). […] 17.5–20.0s SETTLE / LOOP, hold lockup; micro-breath (scale 1.000→1.012→1.000) […]
> CONCRETE TECHNIQUES (required, implement, don't approximate): 1. seek(t) pure function of time. No CSS transitions. No setInterval. […] 3. Kinetic type: per-glyph spring (y, opacity, blur). Stagger = 1/16 note at 120 BPM (125ms). […] 6. Camera: one orthographic camera; only punch-in (1.0→1.08) and horizontal smash-pans timed to beats, never random drift. 7. Motion blur: render 4 subframes per frame, blend (tmix-style). 8. Beat grid: 120 BPM, downbeat at t=0. Something must land on every beat for the first 16 beats; after that, every other beat is ok. 9. Pre-pass: before full render, export one still per major beat (8 frames). Fix cramped type, orphan words, low contrast, then render.
> BANNED: Generic AI clichés (brains, robots, neural nets, sparkles), soft gradients, bouncy cartoon easing, particle explosions, stock "futuristic HUD", long paragraphs, narrator essay energy, Canva-deck energy, extra slogans beyond the locked message, purple/blue neon, glassmorphism.

**Why it's excellent.** It specifies kinetic typography completely: a three-font role system with tracking values, locked copy, named techniques (seeded scramble, letterform mask wipe, misregistration), and camera limits ("never random drift"). Its BPM-derived stagger is the most precise timing rule in the dataset.

### 7.5 gdgtify-929495: "BUILD THE FLOOR" kinetic spoken-word film

> Create a 20.00-second kinetic spoken-word film titled "BUILD THE FLOOR." Treat this as an original miniature speech staged entirely through typography. Every line changes the architecture of the frame. The final declaration must stand on something the earlier words physically constructed. Deliver one self-contained HTML file, 1080×1080, targeting 60fps, using SVG and/or Canvas. Embed all required assets. ART DIRECTION Background #102820. Paper # F4E9D5. Structural accent # F2B544. […] Use a high-contrast serif for the speech, a heavy grotesque for load-bearing words, and a restrained monospace for small timing marks. […] CENTRAL VISUAL RULE Words have assigned architectural roles. WAIT is a lintel. WAITING is a suspended load. VOICE is a support. ROOM is an opening. FLOOR is a platform. These roles must emerge from the actual letterforms, not from separate illustrations placed behind text. STORYBOARD 0.00–3.00 "We were told to wait." The sentence occupies a narrow horizontal opening beneath a massive WAIT. The opening slowly compresses while the sentence remains readable. The pressure comes from the layout, not camera shake. […] 10.00–12.50 "Then another." A second support arrives. The tilted structure levels. This is the first moment of perfect horizontal alignment in the film. Use a brief stillness to make the change feel earned. […] CHOREOGRAPHY Do not force the speech onto a dance beat. Use a cue sheet based on phrases, pauses, and emphasis. Phrase reveals should follow reading order. Allow at least one 400ms moment of absolute stillness. Use critically damped motion for settling loads. […] TYPE IMPLEMENTATION Use actual glyph paths for structural words. Preserve counters and legibility during deformation. For transitions between unrelated words, use occlusion or matched structural edges; do not interpolate arbitrary path points. […] ENGINEERING Implement window. seek(t) as a deterministic scene renderer. No accumulated physics, autonomous CSS transitions, or changing random values. […] Provide fixed-step access at n/60 for 1200 export frames. […] QUALITY GATE Inspect eight representative frames. Check that the speech reads in the correct order. Check that structural transformations never destroy a line before the audience can read it. Check the final platform is visibly assembled from earlier elements. […]

**Why it's excellent.** A single formal metaphor (words as architecture) carries all the emotion. It shows how to pace text to speech rather than to music (phrase cue sheet, earned stillness), and it protects legibility explicitly. This maps directly onto quote moments in talking-head edits.

### 7.6 astrothewizard-618782 (highlighted explainer): the journey of photons, 60s

> I want you to make a 60-second, fully animated explainer video, end to end, completely on your own. […] Topic: the journey of photons
> Style: whimsical, charming, storybook. Give the photon a personality. It should feel like a professional motion-design studio made it, not "AI video". The whole thing should be a pure JavaScript animation, rendered from code frame by frame. […] what makes them great is that they're code-rendered: crisp, precise, with a coherent design system and one strong formal idea per scene. Aim for that bar or above.
> Make it genuinely educational and accurate. Where you can, simulate the real thing: the random walk should be an actual random walk, not a drawing of one. Include real numbers (core temperature, distance, travel time, years inside the Sun) and be honest about uncertainty in the estimates. Use humor and visual gags to keep attention: onomatopoeia, little characters, callbacks. Put what was happening on Earth during those 100,000 years alongside the photon's timeline.
> Deliverable: 1920x1080 at 60fps, exactly 60 seconds, with:
> - A voiceover script you write yourself, voiced with the highest-quality text-to-speech model you can access
> - Burned-in captions, since most people watch on X with the sound off
> - An original music score that fits the whimsical tone and changes with each scene
> - Sound design synced exactly to the on-screen action (every bounce, pop, whoosh and ding)
> - A professional mix: music ducks under the voice, mastered to streaming loudness
> […] Quality is paramount. Build verification loops: render stills of every scene and review them critically, check transitions frame by frame, measure the audio mix numerically, fix what's weak and re-render. Don't hand me a first draft. Hand me something you'd put your name on. Also give me the source code so it's reproducible

**Why it's excellent.** It is the best explainer brief in the set. It covers accuracy and simulation, a character, attention devices, a parallel timeline, a VO + captions + score + SFX + ducking spec, and verification loops that include numeric audio checks.

### 7.7 daniel-haida-636937: Taxtello 15s product film (excerpts from a 2,131-word prompt)

> This is NOT a generic SaaS explainer. This is NOT a feature walkthrough. This is NOT a startup template animation. […]
> CORE CREATIVE RULES […] 1. ONE SHOT = ONE IDEA. 2. Every scene needs room to breathe. 3. The product UI is the hero. 4. Do not plaster explanatory copy everywhere. 5. Do not use hard cuts unless there is a deliberate reason. 6. Prefer object-driven transitions: a card becomes the next card, a chart line becomes a connector, a receipt becomes a booking, a number becomes another interface element, the camera moves through the product. 7. Use premium easing. No linear movement. 8. Motion should overlap naturally. Elements should not all start and stop at exactly the same frame. […] 10. NO effect exists simply because it looks cool. 11. No particle spam. […] 16. No 20 different animation styles. […]
> The first 1.5 seconds must already look premium. The first meaningful product moment should happen by ~2 seconds. No five-second logo intro. […]
> TRANSITIONS […] I want transitions that make the viewer think: "Of course the next scene came from that." Good: chart line → document edge / gold pill → invoice button / financial number → amount in invoice / card edge → next surface / camera push through interface element / shared geometry / mask reveal using actual product shapes. Bad: crossfade / random wipe / spin transition / glitch / whip-pan every two seconds / generic SaaS slide-left / zoom-blur spam […]
> Use curves comparable to: cubic-bezier(0.16, 1, 0.3, 1) […] anticipation / overshoot below ~2% / settling / motion continuation / shared velocity between scenes. Avoid cartoon springiness. […]
> 5. Render representative frames at roughly: 0.0 s 1.0 s 2.5 s 4.5 s 6.5 s 8.5 s 10.5 s 12.5 s 14.0 s 14.8 s 6. VISUALLY INSPECT THOSE IMAGES. Do not merely confirm that rendering succeeded. […] 9. Inspect multiple exact decoded frames from the final MP4, not only browser screenshots. […] Do not declare success because the code compiles. The deliverable is the FILM. […]
> I would rather have: 3 extraordinary visual moments than 10 mediocre feature animations. […] Go all out creatively, but exercise ruthless restraint.

**Why it's excellent.** It gives the clearest good/bad lists for transitions anywhere in the dataset, concrete easing numbers, an explicit QA frame schedule, and a restraint philosophy. Its rules can be lifted into a skill almost unchanged.

### 7.8 stokebuilder-356793: podcast B-roll animation pass

Directly relevant to talking-head editing.

> Go through the entire [episode] cut and add full-screen animations and graphics wherever they help. Be aggressive and over-inclusive: 35–50 moments, at least 2 per chapter. The goal is to fill empty talking-head time, explain ideas, and create visual hooks.
> Style. Pick an aesthetic that's genuinely interesting and very, very cool, built in JavaScript with HyperFrames and assembled in Tesseract. […]
> Stay inside the LegalQuants brand (read brands/legalquants/): charcoal, white and black only, Arial, and the supplied lockup top-right, static. Write a shared style bible and a component kit first, so every animation looks like the same show.
> […] Rules
> Whenever anything goes full-screen (animation, screen share or still), one of us is in a corner picture-in-picture, bottom-right, following whoever is talking.
> No punch-ins or zooming on the cameras. Keep each speaker relatively centered.
> Copy must be verbatim or faithful to what's said. Never invent facts, numbers or quotes.
> Sync each animation's beats to the spoken words.
> Keep each graphic inside one uncut stretch of audio, and leave a few seconds of faces between graphics.
> Process
> An Opus 5.5 agent at extra-high effort finds every timestamp where an animation could fill space and hook the viewer, with a concept for each.
> Opus 5.5 at medium effort builds each animation.
> Opus 5.5 at extra-high effort judges each one once on brand consistency with the others, visual interest, relevance to the narrative and creative judgment.
> Only cues the judge considers egregiously bad go back for a fix. No blanket redo loops.
> Assemble the full cut with PiP baked into every full-screen visual, and give me a folder of the individual animations.

**Why it's excellent.** It is the only prompt that defines a repeatable insert-graphics workflow for long-form talking-head video: a density target, a style bible first, faithfulness rules, audio-segment boundaries, PiP, and a single-pass judge with bounded rework.

### 7.9 ik-builds-585923: parameterized 15s launch film template

> "Create a 15s motion-graphics film explaining {{PRODUCT}}. HyperFrames + GSAP, no voiceover, no footage.
> Style: paper-light canvas, marker notes that draw on, real physics, huge kinetic type, hard light/dark switches, a new idea every 1.5–2 s, a sound on every hit.
> COPY: read {{POSITIONING_DOCS}} first. {{ONE_LINER}} For {{AUDIENCE}}. {{WHAT_IT_DOES}} Name what the product learns, never the abstraction.
> RULES
> - No chrome (scrubber, timecode, fps, headers). No animator jargon on screen ("squash", "stagger", "easing"...). Every word speaks to the buyer.
> - No invented results: no %, multipliers, customer names or figures.
> - Never use: {{BANNED_WORDS}}.
> - Logo: real mark {{LOGO_FILE}} + "{{PRODUCT}}" in {{WORDMARK_FONT}}; never a boxed logo file.
> CRAFT
> - Colours {{COLOR_CANVAS}} / {{COLOR_INK}} / {{COLOR_ACCENT_1}} / {{COLOR_ACCENT_2}}; notes in the accents; dark mode = charcoal matching the palette.
> - Fonts {{BRAND_FONTS}}; Anton for kinetic type; Caveat handwriting via stroke-dashoffset.
> - Real easing, squash/stretch, stagger, overlap, onion skin, smear, follow-through. Check the HyperFrames registry first. Set every from-state at t=0 (seek-safe); never cover an exit. One primary move per transition; no generic push/slide/rotate-swing.
> - Music in sections: drums drop on the dark switch and while the ball is airborne, slam back on the type and the logo. SFX: pops, pen scribbles, whooshes, logo sub-hit. CC0 or generated only; log sources. Master -14 LUFS, -2 dBTP, re-measured after AAC encode."

**Why it's excellent.** This is already a skill template, built from slots. It sets the idea cadence (1.5–2s), names the failures of on-screen chrome and animator jargon, applies HyperFrames-specific seek-safety, lists the animation principles by name, and specifies loudness.

### 7.10 alex-prompter-997524 (highlighted): the best short explainer prompt (63 words)

> Adopt the role of an expert motion designer. Build a 30-second animated explainer for my business as a single HTML page. 5 scenes. The customer's problem, what I do, how it works in 3 steps, one proof point, and my name at the end. Bold text, smooth transitions, my brand colours. My business [DESCRIBE WHAT YOU SELL, WHO IT'S FOR AND YOUR COLOURS]

**Why it's excellent.** It is the minimum viable explainer spec: role, duration, format, scene count, and a classic narrative arc. It shows how much structure fits into about 60 words.

---

## 8. Rules for the skill

These come from the evidence above. Rules 1–6 address the gaps the short prompts leave, which the skill must fill itself.

1. **Always fix the duration, aspect, resolution and fps before designing.** Duration is the most-stated spec (57% of real prompts, 65% of detailed ones). Defaults: Shorts 1080×1920 at 60fps; YouTube inserts 1920×1080 at 60fps; brand stings 15s; explainer segments 30s.
2. **Write a timestamped storyboard (or beat grid) first and show it before coding.** Each beat gets a visual idea, an exact caption, and its transition logic. 35% of detailed prompts ask for a plan or storyboard first, and all 6 of the strongest specs (howdevelop, brainextends, techhalla, gdgtify, daniel-haida, twoclipping) contain a timestamped or beat-grid timeline.
3. **One shot = one idea; one strong formal idea per scene.** Aim for about 1 idea per second in brand reels, one per 1.5–2s in launch films, and 3–6s per scene in explainers. Prefer 3 extraordinary moments to 10 mediocre ones.
4. **Hook in the first second; something premium by 1.5s; the first real content by about 2s.** No logo intros longer than about 1.2s.
5. **Make transitions object-driven.** Element N becomes element N+1 (shared geometry, match-position, mask from the outgoing shape, flood/iris, camera push through an element). Default-ban crossfades, random wipes, spin transitions, whip-pan spam and generic slide-left.
6. **Ship a default ban list.** Particles, glows, lens flares, shockwave rings, camera shake, bouncy or elastic easing, gradients on UI chrome, glassmorphism, purple/blue "AI" neon, stock HUD, corner text or frames, spinning logos, dead time. Particles and bouncy easing were banned in 8 and 7 of 10 production prompts. Allow an item only when the user asks for it.
7. **Easing defaults.** cubic-bezier(0.16, 1, 0.3, 1) for entrances; critically damped springs with overshoot ≤2%; no linear movement. Stagger elements so they never all start or stop on the same frame; per-word stagger is 80–125ms (one 1/16 note at 120 BPM).
8. **Text choreography.** Outgoing text fully exits before incoming text takes the same space. Content enters after its container starts morphing and leaves before the next morph. Never deform a line before the viewer has had time to read it.
9. **Copy discipline.** Use at most 3–4 words per on-screen line, as 2–4 word noun stacks ("Agents · Sandboxes · MCP"), with a font system with roles: display for 1–4 words, sans for UI, mono for numbers and labels. No paragraphs, no animator jargon, no on-screen timecode or chrome.
10. **Truth over invention.** In talking-head edits, copy is verbatim or faithful to the transcript. Never invent numbers, quotes, features or customer data. Use real product UI rebuilt from real tokens, and break screenshots into animatable components rather than sliding raw screenshots.
11. **Deterministic rendering contract.** Every frame is a pure function of `t` (`seek(t)` or `draw(t)`). No CSS transitions, timers, `setInterval`, accumulated physics or unseeded randomness. Springs are closed-form, with a sum of springs for each retarget. Every from-state is set at t=0 (seek-safe). This is required for HyperFrames, Remotion and Playwright capture.
12. **Motion blur through subframes.** Render 3–4 temporal subframes per output frame and blend them (ffmpeg `tmix`). Keep static text sharp. Never put `will-change` on camera-scaled layers, and never set opacity or filter on preserve-3d elements (fade the wrapper instead).
13. **Supersample for crispness.** Render at full output resolution or higher, with DPR ≥1 or 1.5× supersampling, so output never looks "pixelated". That was a user complaint about naive renders (jarvis11x-544635).
14. **Beat grid and sound.** Analyze the music first (numpy: tempo, downbeat, energy per bar, the drop), then put cuts on downbeats and UI hits on beats. Place SFX by their **measured peak**, not their file start. Add one soft SFX per appearing element and silence otherwise. Duck the music under VO, and master to −14 LUFS and −2 dBTP, measured after encoding.
15. **For speech, sync to phrases, not beats.** Use a cue sheet from transcript word timestamps (≈1.5–2s per visual change in narrated pieces), with at least one ≈400ms stillness before key lines.
16. **Design for muted viewing and platform UI.** Burn in captions, keep important content inside a 9:16-safe central area, and keep text clear of TikTok/Reels/Shorts overlay zones.
17. **Talking-head insert density.** In long-form, aim for about 2 or more graphics per chapter (35–50 per podcast episode). Keep each graphic inside one uncut audio stretch, leave a few seconds of face between graphics, and use PiP bottom-right when a graphic goes full-screen. Don't punch in on cameras during graphics.
18. **Style bible and component kit first.** Before making several inserts, define the palette (hex), fonts, easing tokens, transition vocabulary and reusable components (text reveal, camera surface, masked transition, chart, counter, lower third), so every graphic "looks like the same show".
19. **Use a persistent anchor across scenes.** Keep a mascot, player bar, hero asset or brand accent in place (or let it travel) across shots so the edit feels continuous.
20. **Visualize abstractions literally and accurately.** Simulate the real process (an actual random walk), use a scale ruler for scale stories, exploded views for mechanisms, parallel timelines for context, and real numbers with honest uncertainty.
21. **Camera language.** Use one camera vocabulary per piece. Calm style: 1.5–3s ease-in-out moves at "half the speed you'd default to". Energetic style: punch-ins of 1.0→1.08 and smash-pans only on beats. No random drift and no constant zooming.
22. **Endings.** Hold the final lockup long enough to read (≈2–3s), with an optional micro-breath (scale 1.000→1.012). For loops, make last frame = first frame (including cursor position and velocity) and export [0, duration) without duplicating the endpoint.
23. **QA gate before the full render.** Render one still per beat or scene as a contact sheet, inspect it for clipping, overlap, cramped type, contrast and template-feel, and fix. After the render, inspect decoded MP4 frames (not just browser screenshots) and scan for single-frame pops (frame-difference spikes about 3× their neighbours). The film is the deliverable, not code that compiles.
24. **Bounded iteration.** Judge each graphic once against brand consistency, visual interest and relevance, and re-do only the egregious ones. No blanket redo loops.
25. **Choosing a stack.** Canvas 2D for free-form, particles, pixel art, hand-drawn and simulation. SVG (+ GSAP on a seek-driven timeline) for kinetic type, line-draw, logos, charts and UI morphs. DOM/CSS for UI rebuilds from brand tokens. three.js for real depth (scale dives, exploded objects, carousels). GLSL only for backgrounds, fluids and grain/CRT. Default to Canvas or SVG; this mirrors the dataset (canvas 69% / svg 50% of motion; three.js and shaders roughly 2× more common in explainers).


# ===== FILE: references/tooling-research.md =====

# GitHub and tooling research for the AI video editor skill

Contents: 1. HyperFrames (CLI verification, install needs, gotchas) · 2. Agent and Claude skills for video editing on GitHub (all cloned and read unless marked) · 3. Remotion vs HyperFrames vs Motion Canvas vs Revideo (for an agent) · 4. Word-level transcription (2026) · 5. auto-editor · 6. FFmpeg recipes [verified locally on ffmpeg 6.1.1 unless marked; harness `ffmpeg_tests.sh`, log `ffmpeg_tests.log`, all PASS] · 7. ASS subtitles for karaoke and word highlight · 8. Free asset sources and licenses · 9. Other things a top-tier editor skill should include

Research date: 2026-10-11. Environment: Linux sandbox, Node 22.22, ffmpeg 6.1.1 (Ubuntu build with libass, freetype, fontconfig, harfbuzz, fribidi, libvpx, libx264).

**Tags used in this file**
- **[verified locally]**: I ran the command in this session and it worked as described. Logs are in `scratchpad/research/` (`hf-help-1.txt`, `hf-help-2.txt`, `hf-docs.txt`, `ffmpeg_tests.sh`, `ffmpeg_tests.log`).
- **[from source]**: I read it in a cloned repo or a fetched page. The URL is given.
- **[unverified]**: from a secondary source or from memory. Check it before you rely on it.

Network limits in this sandbox:
- `cdn.jsdelivr.net` and `huggingface.co` were blocked by the egress proxy.
- `api.github.com` search was blocked.
- WebFetch DNS failed, so pages were read with Firecrawl.

Because of these limits, model downloads (Whisper, Parakeet) could not be tested locally.

---

## 1. HyperFrames (CLI verification, install needs, gotchas)

The main session is reading the official SKILL.md files, so this section covers only the CLI surface and gotchas.

- **What it is:** HeyGen's HTML-to-video renderer. Repo: https://github.com/heygen-com/hyperframes. License Apache-2.0, `engines.node >=22` (read from the installed `packages/cli` package.json) [verified locally]. Docs index: https://hyperframes.heygen.com/llms.txt.
- **Version tested:** `npx --yes hyperframes@latest` gave v0.8.147 [verified locally].
- **Requirements, from `hyperframes doctor` [verified locally]:**
  - Node 22 or newer
  - FFmpeg and FFprobe on PATH
  - Chrome Headless Shell, installed with `npx hyperframes browser ensure` (a 114 MB download into `~/.cache/hyperframes/chrome/`)
  - Optional: `whisper-cpp` (for `transcribe`), Kokoro (`pip install kokoro-onnx soundfile`), MusicGen
  - Optional: Docker, for `--docker` deterministic renders
  - Low-memory mode switches on automatically at 8 GB RAM or less.

### Composition format (from `hyperframes init demo --non-interactive --example blank --resolution portrait`) [verified locally]

The scaffold writes `index.html`, `hyperframes.json`, `meta.json`, `package.json`, `CLAUDE.md` and `AGENTS.md`. The `package.json` scripts pin `npx --yes hyperframes@0.8.147 preview|check|render|publish`.

```html
<html lang="en" data-resolution="portrait">
<head><meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style> html,body{width:1080px;height:1920px;overflow:hidden;background:#0a0a0a} </style></head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="10"
       data-width="1080" data-height="1920">
    <h1 id="title" class="clip" data-start="0" data-duration="10" data-track-index="0">Title</h1>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.fromTo("#title", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6 }, 0);
    window.__timelines["main"] = tl;   // key MUST equal data-composition-id
    tl.seek(0);
  </script>
</body></html>
```

**Data attributes** (from `hyperframes docs data-attributes`) [verified locally]:

| Group | Attributes |
|---|---|
| Timing | `data-start`, `data-duration` (seconds), `data-track-index` (Studio lane only; the renderer ignores it, and paint order comes from CSS z-index) |
| Media | `data-media-start` (trim offset), `data-volume` (1 = 0 dB, up to 3.98 = +12 dB), `data-fade-in`, `data-fade-out`, `data-has-audio="true"` (silent footage uses `muted`) |
| Composition | `data-composition-id` (required), `data-width`, `data-height`, `data-composition-src="compositions/x.html"` (nested), `data-no-timeline` |
| Variables | `data-composition-variables` (JSON array of `{id,type,label,default}` on `<html>`), `data-variable-values` (JSON object on a sub-comp host), read with `window.__hyperframes.getVariables()` |

**FPS:** taken from the root `data-fps` or `--fps`. The default is 30.

**Rules from the scaffolded CLAUDE.md** [verified locally]:
- Every timed element needs `data-start` and a duration.
- Timed visuals get `class="clip"`.
- Register one paused root timeline per composition on `window.__timelines`. Child timelines added to it must NOT be paused.
- Keep the sound of a video with audio on the `<video>` element. Use a separate `<audio>` for music, voiceover, or J/L cuts.
- No `Date.now()`, no `Math.random()`, no network fetches.

**Determinism** (from `docs/concepts/determinism.mdx` in the repo) [from source]:
- Frame time is computed as `time = floor(frame)/fps`. All GSAP timelines are paused and seeked, never played.
- Frames are captured with `HeadlessExperimental.beginFrame`.
- Use `--docker` to pin Chrome, fonts and FFmpeg.
- Do not call `play()`, `pause()` or set `currentTime` on media.
- Animate a wrapper div, never a `<video>`'s width, height, top or left.

### CLI syntax [verified locally, from `--help`; full text in hf-help-1.txt / hf-help-2.txt]

```
hyperframes init [NAME] [-e|--example blank|warm-grain|swiss-grid|<registry item>] [-v|--video F] [-a|--audio F]
     [--skip-transcribe] [--model small.en] [--language en] [--non-interactive] [--tailwind]
     [--resolution landscape|portrait|landscape-4k|portrait-4k|square|square-4k]
hyperframes render [DIR] [-c|--composition compositions/x.html] [-o out] [-f|--fps 30|30000/1001]
     [-q|--quality draft|looks(default, CRF16)|delivery|standard|high] [--format mp4|webm|mov|gif|png-sequence|hls]
     [--crf N | --video-bitrate 10M] [-w|--workers auto|N] [--docker] [--gpu] [--browser-gpu|--no-browser-gpu]
     [--resolution portrait-4k ...(DPR upscale, same aspect)] [--strict|--strict-all] [--no-best-effort]
     [--variables '{"k":"v"}' | --variables-file f.json] [--batch rows.json] [--video-frame-format auto|jpg|png]
     [--browser-timeout S] [--player-ready-timeout MS] [--low-memory-mode] [--frames-cache-dir DIR] [--hdr|--sdr]
hyperframes snapshot [DIR] [--frames 5] [--at 3.0,10.5] [--no-end] [--zoom '#sel' | x,y,w,h] [--against ref.mp4] [--describe false]
hyperframes check [DIR] [--json] [--samples 9] [--at ...] [--at-transitions] [--strict] [--no-contrast] [--snapshots]
     [--caption-zone "x0=0;y0=0.82;x1=1;y1=1;severity=error"] [--frame-check]
hyperframes lint [DIR] [--json] [--verbose]
hyperframes validate [DIR] [--json] [--timeout 3000]      # deprecated → use check
hyperframes inspect  [DIR] ...                           # deprecated → use check
hyperframes beats [DIR] [--json]                          # writes beats/<audio>.json
hyperframes keyframes [TARGET] [--selector S] [--runtime gsap|css|anime|all] [--json] [--shot out.png --samples 9 --layout path|strip]
hyperframes catalog [WORDS] [--type block|component] [--tag captions] [--json]
hyperframes add <NAME|TAG> [--dir D] [--no-clipboard] [--json] [--vars '{...}'] [--force]
hyperframes capture [URL] [-o dir] [--json] [--skip-assets]
hyperframes media-treatment --capabilities | --selector S --grading '<json>' --apply | --analyze | --clear [--dry-run] [--json]
hyperframes transcribe <INPUT> [-e auto|parakeet|whisper] [-m small.en|large-v3] [-l en] [--json] [--to srt|vtt -o out]
hyperframes models install parakeet
hyperframes remove-background IN [-o out.webm|.mov|.png] [-b bg_plate.webm] [--device auto|cpu|coreml|cuda] [--quality fast|balanced|best]
hyperframes normalize-audio [DIR] --target <elementId> [--reference <id> | --lufs -16] [--write]
hyperframes tts "text" [-v af_heart] [-l en-us|hi|...] [-o speech.wav]
hyperframes timeline [DIR] move|trim|split|delete|set|duplicate|ids|apply|undo
hyperframes compositions [DIR] | info | doctor | browser ensure | docs <topic> | skills check|update [names]
```

### Render results for the 3 s portrait demo [verified locally, checked with ffprobe]

| Command | Output |
|---|---|
| `render -q draft -o renders/test.mp4` | h264 **Constrained Baseline**, yuv420p, 1080x1920, 30 fps |
| `render --format webm` | vp9, reported as `yuv420p` but tagged `ALPHA_MODE=1` (alpha present) |
| `render --format mov` | prores **4444**, `yuva444p12le` |

I composited the transparent WebM over a red plate with ffmpeg, and the alpha was correct. You must force the decoder with `-c:v libvpx-vp9 -i overlay.webm`. Without it, the native VP9 decoder drops the alpha channel.

`snapshot --at 0.3,1.0` wrote PNGs plus `contact-sheet.jpg` into `snapshots/`. `check --json` returned lint, runtime, layout, motion and contrast blocks [verified locally].

### Registry

- `catalog --json` lists 446 items [verified locally].
- Most useful for talking-head edits:
  - **Captions:** `caption-highlight` (TikTok-style), `caption-pill-karaoke`, `caption-kinetic-slam`, `caption-emoji-pop`, `caption-editorial-emphasis`, `caption-weight-shift`, `caption-clip-wipe`, `caption-gradient-fill`, `caption-neon-glow`, `caption-parallax-layers`, `mk-callout-highlight`
  - **Lower-thirds:** `lt-*` (12 of them), `yt-lower-third`
  - **YouTube moves:** `yt-camera-move`, `yt-circle-pointer`, `yt-feather-highlight`, `yt-screen-warp`, `yt-vertical-fill`, `push-in`, `parallax-zoom`, `whip-pan-cut`, `zoom-through-transition`
  - **Stats and data:** `count-up`, `chart-story`, `data-chart`, `bar-chart-race`
  - **Hand-drawn:** `hw-*` annotations, `cursor-annotate`, `marker-highlight`
  - **Social cards:** `x-post`, `reddit-post`, `yt-comment-card`
  - **Overlays:** `grain-overlay`, `light-leak`, `beat-accent`, `confetti`, `logo-sting`, `cta-lockup`
- Install with `hyperframes add <name>` or `hyperframes add captions` (installs every item with that tag).

### Gotchas I hit or read

1. **[verified locally] Offline GSAP.** The scaffold loads GSAP from jsDelivr. If that CDN is unreachable, render fails with `sub_timeline_script_failure ... Cannot read properties of null (reading 'timeline')`. The fix is to vendor it: `npm pack gsap@3.14.2`, copy `dist/gsap.min.js` next to `index.html`, and use `<script src="gsap.min.js">`. Vendor fonts the same way, for both determinism and offline use.
2. **[verified locally] Stale example names.** `docs examples` lists a `video-edit` example, but `init --example video-edit` fails with "not found in registry". Examples are now registry item names, and `blank` is the offline-safe choice.
3. **[verified locally] Draft quality.** `-q draft` produced Baseline-profile H.264. Use the default (`looks`, CRF 16) or `delivery` for anything final.
4. **[verified locally] Screenshot fallback.** WebM and MOV renders fell back to "screenshot capture (slower)" because BeginFrame does not run there. `--resolution` upscaling also disables BeginFrame.
5. **[from source]** A composition with no registered timeline waits 45 s (`player-ready-timeout`) on every render. Add `data-no-timeline` to avoid this. Lint reports it as `missing_data_no_timeline`. (Source: `docs/guides/troubleshooting.mdx`.)
6. **[from source]** The root render length is fixed before scripts run. Changing root duration from a variable does nothing, so write `data-duration` explicitly.
7. **[from source]** Local renders can differ by a pixel across machines because of fonts and Chrome versions. Use `--docker` when you need reproducibility. Fonts fail silently and fall back to another face, so video-use asserts with `document.fonts.check('700 76px "Inter"')` (see browser-use/video-use SKILL.md).
8. **[from source]** An agent should start Studio with `npx hyperframes preview --background`, check it with `--status`, and stop it with `--stop`. Do not wrap `npm run dev` in a background shell (scaffold CLAUDE.md).
9. **[unverified, secondary]** A Skool user reports that render quality drops unless the skill is told to keep the source resolution, and that captions still need a manual pass. Source: https://www.skool.com/ai-automation-society/i-built-a-claude-code-skill-that-edits-my-youtube-shorts
10. **No GitHub issue survey.** The GitHub issues API was blocked here. Of the gotchas above, items 5–8 come from the official troubleshooting and determinism docs.

---

## 2. Agent and Claude skills for video editing on GitHub (all cloned and read unless marked)

### Seed sources

- **WeAreNoCode `youtube-edit`.** It is distributed as a zip in the free Skool community, not on GitHub. Setup PDF: https://assets.skool.com/f/a37f7643548a4fc7b7430dd6f2ce6da5/db32d829a30b49a99be1218d9560e202364b526775d0480ba0648f09279034f5 [from source].
  - **Contents:** `youtube-edit/` holds SKILL.md and `scripts/` (cutting, dead-air scan, animation composer, render checks, final assembly) plus `assets/fonts` (DM Sans, OFL). Alongside it are `SETUP.md`, `PROMPTS.md`, a `STYLE-GUIDE.md` with a "Yours" column, and `LICENSES/` (some scripts adapted from an MIT starter kit).
  - **Tool roles:** Parakeet and auto-editor transcribe ("where I speak, every word with its exact time"). HyperFrames animates. Claude-in-Chrome researches. Tella provides screen recordings. Epidemic Sound provides music and SFX. FFmpeg joins and checks.
  - **Learning loop:** watch the whole cut, give timestamped notes, then say "Can you learn from what we did and add it to the skill?" Apply the style guide with "Here's my style guide. Update the youtube-edit skill to match it."
  - **Recording advice:** shoot 4K because "1080p goes soft past about 112%"; pause and repeat a flubbed line ("it keeps your last take of every line"); keep the file flat.
  - **Install:** run in Claude Desktop, Claude Code, Local mode. Claude installs FFmpeg, HyperFrames, auto-editor, Parakeet and runs the tests. Open a new thread afterwards, because skills load at thread start.
- **Luv Sankhla "AI Video Editor".** Nothing was findable on the web or GitHub [unverified]. A skill named `ai-video-editor` is already installed in this environment, matching the description ("7 subtitle styles, HyperFrames, reverse-engineers a creator's style"). The main session can read it directly.

### Repos worth borrowing from

| Repo (license) | What it does | Techniques worth borrowing |
|---|---|---|
| **browser-use/video-use** https://github.com/browser-use/video-use (MIT, about 10k stars) | Edit any video by conversation. Outputs go to `<videos>/edit/`. | **12 hard rules:** subtitles applied LAST, after overlays; per-segment extract then `-c copy` concat; 30 ms `afade` in/out at every boundary; overlays shifted with `setpts=PTS-STARTPTS+T/TB`; SRT offsets in output-timeline time (`word.start - seg_start + seg_offset`); never cut inside a word; pad cuts 30–200 ms; word-level verbatim ASR only; cache transcripts; build animations with parallel sub-agents; confirm the strategy before executing. **Artifacts:** `takes_packed.md` (phrase-level transcript that breaks on silences of 0.5 s or more, about 1/10 the tokens of JSON), `edl.json`, `project.md` session memory. **Helpers:** `timeline_view.py` (filmstrip plus waveform PNG at cut points), self-eval at every cut ±1.5 s, `ebur128` measurement, a "critic sub-agent" that roasts the render, capped at 3 self-eval passes. **Animation timing:** start the overlay `reveal_duration` early so the landing frame hits the spoken payoff word. Use cubic easing, never linear. **Caveat:** it uses paid ElevenLabs Scribe, so swap in a free ASR. |
| **chrislema/videoeditor** https://github.com/chrislema/videoeditor (blog: https://chrislema.com/claude-code-skills-for-video-editing) | Eight markdown skills plus `00-process-video`: remove silence, label sections, produce zoom, correct colors, master audio, add captions, clean artifacts, plus sync-feeds and swap-angles. | **Silence:** `silencedetect=noise=-30dB:d=0.5`, trim gaps to 0.3 s, join with a single-pass `trim/atrim` re-encode (never `-c copy`, which snaps to keyframes and drifts). **Zoom labels:** sections tagged normal, emphasis (1.25x) or critical (1.6x), aimed at a 40/35/25 % split, each 3–7 s. **Face framing:** OpenCV Haar per section, one static crop per section ("don't pan within a section; Haar jitters"), and keep the head top in vertical crops. **Color:** `colorbalance=rs=0.02:gs=-0.01:bs=-0.02,curves=m='0/0 0.25/0.20 0.75/0.82 1/1',eq=brightness=0.02:contrast=1.05:saturation=1.05`. **Audio:** `highpass=f=80,lowpass=f=14000,equalizer=f=3000:t=q:w=1.5:g=3,equalizer=f=200:t=q:w=1.0:g=2,acompressor=threshold=-21dB:ratio=3:attack=5:release=50,volume=0.6,loudnorm=I=-16:TP=-1.5:LRA=11`. **Captions:** whisper.cpp `-ml` for short segments, `drawtext` with a 70 % black box. **Multi-cam sync:** audio cross-correlation. |
| **louisedesadeleer/add-zooms** https://github.com/louisedesadeleer/add-zooms (MIT, Tella) | Transcript-driven punch-zooms with ffmpeg `zoompan`. | **Three moves:** *punch* (1-frame hard cut to 1.18–1.30, hold 0.2–0.5 s, hard cut out), *ratchet* (each list item steps up 1.12 to 1.28), *kenburns* (≤1.14, slow, the only smooth move). Focal point (0.5, 0.42). Peaks of 1.30 or less keep 1080p sharp, and never go past about 1.35. `map.json` holds the events, so you edit and re-render without re-transcribing. The zoompan `z` is a piecewise-linear `if(lte(on,f1),…)` expression, `max()`-combined across events, with `x='iw*cx*(1-1/zoom)'`, `y='ih*cy*(1-1/zoom)'`, `d=1`. |
| **louisedesadeleer/clipify** https://github.com/louisedesadeleer/clipify (MIT) | Long video to 9:16 clips with opus-style captions. | **Speaker-follow 9:16 pan with no ML:** per-ROI motion energy via `crop,format=gray,tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=L.txt`, then a speaker timeline (1 s minimum dwell), then a hard-cut `crop=608:1080:x='EXPR'`. **Captions:** an ASS builder writes one Dialogue per word, highlighting the active word with `\c`. **Action mode:** spectral-flux transient detection in the 1–6 kHz band, cutting about 0.4 s before and 0.5 s after each strike. **Always verify frames** at candidate times before rendering. **Fast trims:** `whisper --model tiny.en --word_timestamps True`. |
| **louisedesadeleer/b-roll-finder** https://github.com/louisedesadeleer/b-roll-finder (MIT) | B-roll sourcing methodology with a `TASTE.md` profile. | **Onboarding gate:** the profile counts as yours only with a literal `Confirmed-by: <name> (<date>)` line. User bans persist into the profile immediately. **Routing:** Receipts (tweets, headlines), Entity (official clip), Concept (motion graphic), Meme (the user supplies it). **Rules:** source the MEANING, not keywords; fetch "by source, not by beat"; the lean path is the default; no retries ("first failure switches, second drops"); a stills Ken Burns of about 1.5 %/s; strip b-roll audio with `-an`. |
| **hassancs91/claude-youtube-editor** https://github.com/hassancs91/claude-youtube-editor (MIT; guide: https://learnwithhasan.com/guide/claude-code-video-editing/) | Nine skills (clean-cut, make-tsx (Remotion), fake-screencast, clean-audio, suggest-sfx, packaging, thumbnail, brand-setup, vidtsx-2d-generator) plus Python tools. | **`tools/verify_cut.py`:** a second ASR pass over the RENDER, diffed against the intended kept words. It flags inserted "ghost" syllables, missing or replaced words, interior gaps of 0.40 s or more, low-confidence words, and **A/V drift** per keep. **Documented bug:** concatenating per-segment AAC built up about 1 s of lip-sync drift (see §6). **clean-audio** matches RMS rather than loudness-normalizing; denoise only; RNNoise as the free local option. **SFX library:** each sound normalized to about -20 LUFS / -1.5 dBFS with catalog metadata, so per-cue gain is meaningful. **Pipeline:** a hard stop for human audit before mixing; one locked title with three thumbnail bets; a compounding asset library ("video ten is cheaper than video one"). Uses paid AssemblyAI, ElevenLabs and Gemini. |
| **agricidaniel/claude-shorts** https://github.com/agricidaniel/claude-shorts (MIT) | Shorts clipper: faster-whisper, Claude segment scoring, `snap_boundaries.py`, Remotion captions, FFmpeg export. | `snap_boundaries.py` snaps to word boundaries, extends to finish a sentence if within 3 s, pads after the last word, and optionally uses silencedetect. `compute_reframe.py` does MediaPipe face tracking with moving-average smoothing. **Its `mp.solutions` API is gone in current mediapipe (§9).** |
| **calesthio/OpenMontage** https://github.com/calesthio/OpenMontage (**AGPL-3.0**, so do not copy code into a closed skill) | Full agentic production system: 13 pipelines including `talking-head.yaml`, many `.claude/skills`, tools. | **Tools:** `auto_reframe.py` (MediaPipe/OpenCV face track, smoothing window, `sendcmd` dynamic crop, center-crop fallback); `silence_cutter.py` (modes remove, speed_up, mark); `transcriber.py` (faster-whisper `word_timestamps=True, vad_filter=True`, int8 on CPU); `subtitle_gen.py` (max words per cue, word corrections dictionary). Free stock adapters: archive_org, coverr, mixkit, nasa, noaa, pexels, pixabay, unsplash, videvo, wikimedia, loc, esa, jaxa. Its "executive-producer" orchestration has checkpoints and a reviewer. |
| **WyattBlue/auto-editor** `skills/` https://github.com/WyattBlue/auto-editor/tree/master/skills | Official agent skills: `auto-editor`, `auto-editor-export`, `auto-editor-transcribe`, `auto-editor-effects`. | Authoritative CLI usage (see §5). |
| **heygen-com/hyperframes** `skills/` | Official skills: `talking-head-recut`, `embedded-captions`, `motion-graphics`, and others. | The main session is reading these. |
| **digitalsamba/claude-code-video-toolkit** https://github.com/digitalsamba/claude-code-video-toolkit | Remotion-centric production workspace. Skills: ffmpeg, moviepy, remotion, remotion-official, playwright-recording, elevenlabs, acestep (music), ltx2, runpod, qwen-edit. | Mostly cloud GPU and paid services, so less relevant for a free, local talking-head editor. |
| Others found but not cloned [unverified] | `Hotclip` (AGPL, local shorts with karaoke, https://claudskills.com/skills/hotclip/); `op7418/youtube-clipper-skill` (bilingual subtitles, https://claudemarketplaces.com/skills/op7418/youtube-clipper-skill/youtube-clipper); `danielmiessler/personal_ai_infrastructure` audioeditor (https://skillselion.com/skills/danielmiessler/personal_ai_infrastructure/audioeditor); `Ceeon/videocut-skills` (Chinese; now a Codex plugin plus runtime, FunASR, not useful here); `affaan-m/ecc` video-editing (https://claudeskills.info/zh/skills/affaan-m/ecc/video-editing/). | |

---

## 3. Remotion vs HyperFrames vs Motion Canvas vs Revideo (for an agent)

**HyperFrames** (Apache-2.0, HeyGen):
- The agent writes plain HTML/CSS with a paused GSAP timeline and `data-*` timing. There is no build step and no React.
- The CLI was built for agents: `lint`, `check --json`, `snapshot` contact sheets, `keyframes --shot` onion skins, and `--caption-zone` checks.
- It renders transparent WebM and ProRes 4444 overlays, and ships a 446-item registry of captions, lower-thirds and transitions. Transcribe, TTS and remove-background are built in.
- Costs: Chrome capture is slower than Remotion Lambda (one reviewer reports about 3 min locally for 30 s at 1080p), and it needs Node 22 or newer.
- Sources: https://github.com/heygen-com/hyperframes, https://moda.app/blog/hyperframes-vs-remotion [secondary], local test.

**Remotion** (React, source-available):
- Free for individuals and companies of up to 3 people. A company license is needed at 4 or more, and an "Automators" tier applies if you build a video tool for others. The license changes in v5.
- Most mature ecosystem: `@remotion/captions`, Lambda/Cloud Run, Player, and official agent skills (`remotion-dev/skills`).
- Best when the user already has a React or Remotion brand kit (hassancs91, claude-shorts and video-toolkit all use it).
- Sources: https://www.remotion.dev/docs/license/faq, https://github.com/remotion-dev/remotion/blob/main/LICENSE.md.

**Motion Canvas** (MIT):
- Generator-function TypeScript with an excellent editor for hand-authored explainers.
- Rendering runs through its editor UI, so it is poorly suited to a headless agent loop.

**Revideo** (MIT fork of Motion Canvas):
- Adds headless `renderVideo()` and API deployment.
- Maintenance activity after 2024 is unclear, with about 3k weekly downloads per a secondary 2026 source [unverified]. Sources: https://docs.re.video/, https://www.pkgpulse.com/guides/remotion-vs-motion-canvas-vs-revideo-programmatic-video-2026.

**Recommendation:** use HyperFrames as the default overlay engine for this skill. Use PIL plus ffmpeg for trivial cards, and Remotion only when the user already has a Remotion kit. video-use picks the engine per slot the same way.

---

## 4. Word-level transcription (2026)

PyPI versions as of today [verified locally with `pip index versions`]: openai-whisper 20250625, faster-whisper 1.2.1, whisperx 3.8.6, mlx-whisper 0.4.3, parakeet-mlx 0.5.3, stable-ts 2.19.1, onnx-asr 0.12.0, nemo_toolkit 3.0.0. Models could not be downloaded here because Hugging Face was blocked, so the commands below come from the READMEs.

| Tool | Install | Word timestamps | Notes |
|---|---|---|---|
| **openai-whisper** | `pip install -U openai-whisper` | `whisper a.wav --model turbo --word_timestamps True --output_format json --language hi` | Reference implementation; slow on CPU; normalizes fillers. Clipify uses `--model tiny.en` for speed and add-zooms uses `small.en`. |
| **faster-whisper** (CTranslate2) | `pip install faster-whisper` | `model.transcribe(p, word_timestamps=True, vad_filter=True)`; `BatchedInferencePipeline`; `WhisperModel("turbo"\|"large-v3"\|"distil-large-v3", device="cpu", compute_type="int8")` | Up to about 4x faster than openai-whisper; CPU int8 is good on Windows. No Apple GPU. Source: SYSTRAN/faster-whisper README. |
| **whisper.cpp** | `brew install whisper-cpp` (Mac), build with cmake, or winget [unverified for Windows] | `whisper-cli -m ggml-large-v3-turbo.bin -f a.wav -l auto -ojf -ml 1 -sow` (`-ojf` gives full JSON with token times; `-ml N` max segment chars; `-sow` split on word; `-wt 0.01` word threshold; `-dtw <model>` for DTW token timestamps; `--vad` with a silero ggml model; `-owts` writes a karaoke script) | Metal on Apple Silicon; Core ML encoder about 3x faster on the ANE. Models live at huggingface.co/ggerganov/whisper.cpp. Flags from `examples/cli/README.md` in ggml-org/whisper.cpp [from source]. **Gotcha (chrislema):** the Homebrew formula no longer ships models, so download to `~/.cache/whisper-cpp/`. |
| **mlx-whisper** (Mac) | `pip install mlx-whisper` | `mlx_whisper a.mp3 --model mlx-community/whisper-large-v3-turbo --word-timestamps True -f json`; Python `mlx_whisper.transcribe(p, path_or_hf_repo=..., word_timestamps=True)` | Fastest Whisper on Apple Silicon. Flags from `ml-explore/mlx-examples/whisper/mlx_whisper/cli.py` [from source]. |
| **WhisperX** | `pip install whisperx` or `uvx whisperx` | `whisperx a.wav --model large-v3 --language hi --compute_type int8 --device cpu --highlight_words True` | wav2vec2 forced alignment gives the most accurate word boundaries. The Hindi align model defaults to `theainerd/Wav2Vec2-large-xlsr-hindi` (also ur, te, and others in `DEFAULT_ALIGN_MODELS_HF`). On Mac use `--device cpu`. Diarization (`--diarize`) needs an HF token. [from source: m-bain/whisperX] |
| **NVIDIA Parakeet TDT 0.6B v3** | Mac: `pip install parakeet-mlx` or `uv tool install parakeet-mlx`. Elsewhere: `hyperframes models install parakeet`, onnx-asr, or NeMo. | `parakeet-mlx a.wav --output-format json` gives sentences with **token**-level `start/end`; merge subword tokens into words. `--highlight-words` adds word timing to SRT/VTT. Options: `--max-words`, `--silence-gap`, `--chunk-duration 120`. | Very fast and accurate English, with **no Whisper hallucinations**. **Languages: 25 European only, no Hindi** (https://build.nvidia.com/nvidia/parakeet-tdt-0_6b/modelcard). HyperFrames `transcribe -e auto` uses Parakeet when it covers the language and falls back to whisper otherwise [verified locally from help]. |
| **auto-editor whisper** | built into auto-editor 31.x | `auto-editor whisper a.mp4 ggml-parakeet-tdt-0.6b-v3-q8_0.bin --format json -sw -o a.json` (or a ggml Whisper model, or `apple` on macOS 26 or later) | One binary does both ASR and cutting. `-sw` gives one word per cue. Parakeet rejects `--language` and `--prompt`. [verified locally: `whisper --help` in 31.7.2; source: auto-editor-transcribe SKILL] |
| **stable-ts** | `pip install -U stable-ts` (`[fw]`, `[mlx]`, `[hf]` extras) | `stable-ts a.mp3 -o a.json` (or `-fw` for faster-whisper, `-mlx`); `result.to_ass('a.ass', word_level=True)` | Stabilized timestamps plus **`model.align(audio, text, language)`, which force-aligns a known script**. That is ideal when the user has a script or wants to correct ASR text and then re-time it. CLI: `stable-ts a.mp3 --align script.txt --language hi`. [from source: jianfch/stable-ts README] |
| **FFmpeg 8 `whisper` filter** | FFmpeg 8.0 or newer built with whisper.cpp | `ffmpeg -i in.mp4 -vn -af "whisper=model=ggml-medium.en.bin:language=en:queue=30:destination=out.srt:format=srt" -f null -` | Supports `vad_model`; json output. Reported slower than whisper-cli [unverified]. Source: https://rendi.dev/blog/ffmpeg-8-0-part-1-using-whisper-for-native-video-transcription-in-ffmpeg |

**Hindi and Hinglish notes:**
- Whisper large-v3 and turbo support Hindi, but often output Devanagari or translate. For Hinglish, set the language explicitly and pass `--initial_prompt` (or auto-editor `--prompt`) with sample romanized Hinglish text.
- **Oriserve/Whisper-Hindi2Hinglish-Apex** (successor to -Prime, Apache-2.0) outputs romanized Hinglish. Model card: https://huggingface.co/Oriserve/Whisper-Hindi2Hinglish-Prime. A CT2 build exists for faster-whisper (https://huggingface.co/Hub84/faster-whisper-hinglish-prime) and a ggml build for whisper.cpp (https://huggingface.co/gouravg8/gtm-hi2hing-ggml) [unverified quality].
- For word timing on Hindi, use WhisperX with the Hindi wav2vec2 aligner, or stable-ts `align()`.
- Parakeet v3 does not cover Hindi. NVIDIA's NIM release notes mention a separate Parakeet 1.1B RNNT multilingual "Indic" model (https://docs.nvidia.com/nim/speech/26.02.0/about/release-notes.html) [unverified for local use].
- **Recommended routing:** detect the language first. English goes to Parakeet (mlx on Mac, onnx or HyperFrames elsewhere). Hindi or Hinglish goes to whisper large-v3-turbo (mlx-whisper on Mac, faster-whisper int8 on Windows), then WhisperX or stable-ts alignment.
- Whatever engine you use, save the verbatim transcript with fillers (video-use rule 8).

---

## 5. auto-editor

- **Versions:** PyPI `auto-editor` is 29.3.1. Its wheel downloads a Nim binary from GitHub releases. GitHub releases are at **31.7.2** (tag list), and `master` CHANGELOG shows 31.7.3. **The CLI differs between them** [verified locally with both binaries].
- **Install:** `pip install auto-editor` gives 29.3.1. Download 31.x from https://github.com/WyattBlue/auto-editor/releases (asset `auto-editor-linux-x86_64`; also macOS and Windows), or use `brew install auto-editor` [unverified version].
- **31.x has a `-k, --license-key` option** that "activates certain features". Which features are gated is [unverified].

### Common syntax [verified locally on 29.3.1 and 31.7.2]

```
auto-editor in.mp4 --edit audio:threshold=0.04 --margin 0.2s -o out.mp4      # defaults: audio:0.04, margin 0.2s
auto-editor in.mp4 --edit audio:-19dB                                          # dB form
auto-editor in.mp4 --margin 0.1s,0.3s                                          # before,after padding (protects word tails)
auto-editor in.mp4 --edit "(or audio:0.04 motion:0.5)"                         # boolean combos need call form
auto-editor in.mp4 --when-silent speed:4                                       # speed through silence instead of cutting
auto-editor in.mp4 --cut-out 0,1sec  /  --add-in 10sec,20sec  /  --set-speed 2,0,30
auto-editor in.mp4 --preview                                                   # stats only, no render
auto-editor info in.mp4    |    auto-editor levels in.mp4  (per-frame loudness dump)
auto-editor in.mp4 --export premiere|resolve|resolve-fcp7|final-cut-pro|shotcut|kdenlive|clip-sequence|v1|v2|v3 -o name
auto-editor in.mp4 --export 'premiere:name="My Timeline"'
auto-editor in.mp4 -anorm ebu  |  -c:v libx264 -b:v 8M
```

- **There is no `--export json`**; it errors with "Unknown export format". The JSON timeline formats are **`v1`** and **`v3`** [verified locally].
  - `v1` = `{"version":"1","source":"in.mp4","chunks":[[startFrame,endFrame,speed],...]}`, where speed 99999 means cut.
  - `v3` = `{"version":"3","timebase":"30/1","resolution":[w,h],"samplerate":…, "v":[[{"src","start","dur","offset","stream"}]], "a":[…]}`.
  - These are the best machine-readable cut lists to feed into your own ffmpeg or HyperFrames assembly.
  - In my test, the 1.2 s silence at 3.0–4.2 s with `-m 0.1s` produced chunks [0,64), cut [64,102), [102,180) at 30 fps.

### 31.x only [verified locally: present in 31.7.2 help, rejected by 29.3.1]

- `--when-active` and `--when-inactive` (aliases `-w:1` and `-w:0`; 29.3.1 uses `--when-normal` and `--when-silent`)
- `-s/--smooth MINCUT,MINCLIP` (default `0.2s,0.1s`)
- `--transition dissolve:DUR[:MIN-CUT]`
- `--cut` and `--keep` (aliases of `--cut-out` and `--add-in`)
- `--set-action ACTION,start,end`
- `-crf`, `-preset`, `-pix_fmt`, `-g`, `--no-partial-lossless`
- `auto-editor whisper <file|:mic> <ggml model> [-sw] [-l en] [-f text|srt|json] [-o F] [--prompt TEXT] [--queue 30] [-t 0.04]`
- Per the official skill [from source]: labels `--edit:N EXPR --when:N ACTION` (N from 2 to 255, higher label wins) and `:mic` input.

### Cutting on word boundaries

auto-editor's loudness edit is threshold-based, so it can clip quiet word onsets and tails. Recommended approach:

1. **Transcript-based keep list (best).** Get word timestamps (§4). Have Claude choose keep ranges by snapping starts to `word.start - 0.05` and ends to `word.end + 0.08` (video-use and claude-shorts padding), never inside a word. Prefer gaps of 0.4 s or more as cut points. Then either render directly with an ffmpeg `trim/atrim` filtergraph, or feed auto-editor manual ranges: `auto-editor in.mp4 --edit 0 --add-in 1.20sec,4.85sec 6.10sec,9.40sec --export v3` (31.x: `--keep`). `--edit 0` means "cut everything not explicitly kept" [from source: auto-editor SKILL].
2. **Subtitle-driven:** `auto-editor whisper talk.mp4 model.bin --format srt -o talk.srt`, then `auto-editor talk.mp4 --edit subtitle` (keeps only lines with speech; the sidecar `talk.srt` is auto-loaded) or `--edit "(not word:um)"` to drop a filler word [from source; 31.x].
3. **Hybrid (WeAreNoCode style):** run auto-editor for the speech/silence map (`--export v3` or `levels`), use Parakeet for the words, then intersect. Extend any auto-editor keep that would split a word out to the word's bounds.

---

## 6. FFmpeg recipes [verified locally on ffmpeg 6.1.1 unless marked; harness `ffmpeg_tests.sh`, log `ffmpeg_tests.log`, all PASS]

```bash
# Frame-accurate cut (re-encode; -ss before -i is accurate when re-encoding)
ffmpeg -ss 1.5 -i in.mp4 -t 2.0 -c:v libx264 -crf 18 -preset veryfast -c:a aac -ar 48000 cut.mp4

# Concat demuxer (identical codec params only), stream copy
printf "file '/abs/a.mp4'\nfile '/abs/b.mp4'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4

# Single-pass trim+concat filter (one audio encode → no AAC drift) with 30 ms de-click fades
ffmpeg -i in.mp4 -filter_complex "\
[0:v]trim=1.5:3.5,setpts=PTS-STARTPTS[v0];[0:a]atrim=1.5:3.5,asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st=1.97:d=0.03[a0];\
[0:v]trim=5:7,setpts=PTS-STARTPTS[v1];[0:a]atrim=5:7,asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st=1.97:d=0.03[a1];\
[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 18 -c:a aac out.mp4
```

**AAC concat drift [verified locally].** Two 2.000 s re-encoded segments joined with the concat demuxer gave **4.0213 s**. The single-pass filter gave **4.000 s**. Each AAC segment adds priming and padding, which accumulates into lip-sync drift (Hassan saw about 1 s on a long video).

To avoid it, use one of these:
- render audio in one filtergraph pass;
- keep intermediate audio as PCM (`-c:a pcm_s16le` in `.mkv`/`.mov`) and encode AAC once at the end;
- concat video-only segments and lay a separately rendered full audio track over them.

```bash
# Crossfade video + audio (offset = dur(first) - transition)
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=1.5,format=yuv420p[v];[0:a][1:a]acrossfade=d=0.5:c1=tri:c2=tri[a]" -map "[v]" -map "[a]" x.mp4

# L-cut (A's audio runs 0.6 s under B's picture); J-cut is the mirror (B's audio starts early)
ffmpeg -i A.mp4 -i B.mp4 -filter_complex "\
[0:v]trim=0:2,setpts=PTS-STARTPTS[va];[1:v]trim=0:3,setpts=PTS-STARTPTS[vb];[va][vb]concat=n=2:v=1:a=0[v];\
[0:a]atrim=0:2.6,asetpts=PTS-STARTPTS,afade=t=out:st=2.45:d=0.15[aa];\
[1:a]atrim=0.6:3,asetpts=PTS-STARTPTS,afade=t=in:d=0.1,adelay=2600|2600[ab];\
[aa][ab]amix=inputs=2:duration=longest:normalize=0[a]" -map "[v]" -map "[a]" lcut.mp4
```

Punch-in zooms. Keep peaks at 1.30x or less on 1080p.

```bash
# (a) eased ramp via scale(eval=frame)+crop
ffmpeg -i in.mp4 -vf "scale=w='iw*(1+0.2*min(1,max(0,(t-1)/0.25)))':h=-2:eval=frame:flags=lanczos,crop=1920:1080:(iw-1920)/2:(ih-1080)/2" z.mp4
# (b) instant hard punch (Tella style) with face-biased y
ffmpeg -i in.mp4 -vf "crop=w='if(between(t,1,3),iw/1.2,iw)':h='if(between(t,1,3),ih/1.2,ih)':x='(iw-ow)/2':y='(ih-oh)*0.42',scale=1920:1080:flags=lanczos,setsar=1" z.mp4
# (c) zoompan Ken Burns on VIDEO input: d=1 and fps/s must match source
ffmpeg -i in.mp4 -vf "zoompan=z='min(1+0.0015*on,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30" z.mp4
```

For smooth eased curves, write the easing into the expression, for example smoothstep `p*p*(3-2*p)` with `p=clip((t-t0)/dur,0,1)`. Alternatively, render the zoom as a GSAP `scale` on a wrapper div in HyperFrames.

Burn in ASS subtitles with libass. Put subtitles LAST, after all overlays.

```bash
ffmpeg -i in.mp4 -vf "subtitles=subs.ass:fontsdir=./fonts" -c:a copy out.mp4
```

The ASS test is in the harness. The `\k` karaoke and the `\t` pop rendered [verified locally, frame inspected]. On Windows, escape the drive colon: `subtitles='C\:/path/subs.ass'` [unverified locally, documented ffmpeg filter-escaping rule: https://ffmpeg.org/ffmpeg-filters.html#Notes-on-filtergraph-escaping].

Overlay a transparent VP9 WebM or ProRes 4444 at time T:

```bash
ffmpeg -i base.mp4 -c:v libvpx-vp9 -i ov.webm -i ov.mov -filter_complex \
"[1:v]setpts=PTS-STARTPTS+1/TB[o1];[2:v]setpts=PTS-STARTPTS+2/TB[o2];\
[0:v][o1]overlay=x=100:y=H-h-100:eof_action=pass[t];[t][o2]overlay=x=W-w-100:y=100:eof_action=pass,format=yuv420p[v]" \
-map "[v]" -map 0:a out.mp4
```

Gotchas, all [verified locally]:
- `-c:v libvpx-vp9` must come before the WebM `-i`, or the alpha is lost.
- Without `eof_action=pass`, overlay repeats the last frame forever.
- `drawbox` on a transparent canvas does NOT write alpha. Build test overlays with `color=red@0.85,format=yuva420p,pad=...:color=black@0`.

```bash
# Encode alpha deliverables
-c:v libvpx-vp9 -pix_fmt yuva420p        # WebM alpha (ffprobe shows yuv420p + ALPHA_MODE=1)
-c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le   # MOV alpha

# Sidechain ducking (music under voice)
ffmpeg -i voice.mp4 -i music.wav -filter_complex "[0:a]asplit=2[vo][key];[1:a]volume=0.5[m];\
[m][key]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300:makeup=1[duck];\
[vo][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]" -map 0:v -map "[a]" -c:v copy -c:a aac out.mp4

# Two-pass loudnorm to -14 LUFS / -1 dBTP (pass 1 prints JSON on stderr)
ffmpeg -i mix.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -
ffmpeg -i mix.mp4 -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=..:measured_TP=..:measured_LRA=..:measured_thresh=..:offset=..:linear=true,aresample=48000" -c:v copy -c:a aac -b:a 192k out.mp4
# measure: ffmpeg -i out.mp4 -af ebur128=peak=true -f null -     → got I: -13.9 LUFS
```

- Use `amix ... normalize=0`, because the default normalization quietly halves levels.
- `loudnorm` upsamples to 192 kHz internally, so always add `aresample=48000`.

```bash
# silencedetect
ffmpeg -i in.mp4 -af silencedetect=noise=-35dB:d=0.4 -f null -   # → silence_start/silence_end lines on stderr

# Scene detection
ffmpeg -i in.mp4 -vf "select='gt(scene,0.3)',metadata=print:file=scenes.txt" -f null -
ffmpeg -i in.mp4 -vf "scdet=threshold=10" -f null -              # newer dedicated filter (lavfi.scd.time)

# Contact sheet, representative thumbnail
ffmpeg -i in.mp4 -vf "fps=1/2,scale=480:-2,tile=4x3:padding=4:margin=4" -frames:v 1 sheet.png
ffmpeg -i in.mp4 -vf "thumbnail=60,scale=640:-2" -frames:v 1 thumb.png

# Dominant colours (8-swatch palette → read pixels)
ffmpeg -i in.mp4 -vf "fps=1,scale=160:-2,palettegen=max_colors=8:reserve_transparent=0:stats_mode=full" -frames:v 1 pal.png
ffmpeg -i pal.png -f rawvideo -pix_fmt rgb24 -  | python3 -c "...unique RGB triplets..."

# Waveform image
ffmpeg -i in.mp4 -filter_complex "aformat=channel_layouts=mono,showwavespic=s=1920x240:colors=0x00E5FF:scale=sqrt" -frames:v 1 wave.png

# QA
ffmpeg -i out.mp4 -vf "blackdetect=d=0.5:pix_th=0.10" -an -f null -        # black_start/black_end
ffmpeg -i out.mp4 -vf "freezedetect=n=-60dB:d=1" -map 0:v -f null -        # freeze_start/duration/end
ffmpeg -i out.mp4 -af astats=measure_overall=Peak_level:measure_perchannel=none -f null -   # clipping check

# 16:9 → 9:16 static face-centred crop, and blurred-background fit
ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih:x='min(max(FACE_X-ow/2,0),iw-ow)':y=0,scale=1080:1920:flags=lanczos,setsar=1" v.mp4
ffmpeg -i in.mp4 -filter_complex "[0:v]split[bg][fg];[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:5,eq=brightness=-0.08[b];[fg]scale=1080:-2[f];[b][f]overlay=(W-w)/2:(H-h)/2,setsar=1[v]" -map "[v]" -map 0:a v.mp4

# Free voice cleanup (no ML)
-af "highpass=f=80,afftdn=nr=12:nf=-40,deesser,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2"
```

- **Platform note [from source: chrislema/videoeditor README].** Older Homebrew `ffmpeg` builds lack `drawtext`, and `brew install ffmpeg-full` has it. Always probe first with `ffmpeg -hide_banner -filters | grep -E " (subtitles|ass|drawtext|zoompan|xfade|sidechaincompress|loudnorm) "`. Whether current Homebrew ffmpeg includes libass is [unverified].
- **Windows** [unverified]: `winget install Gyan.FFmpeg` (full build includes libass and libvpx).

---

## 7. ASS subtitles for karaoke and word highlight

Reference: Aegisub override tags, https://aegisub.org/docs/latest/ass_tags/. Rendering confirmed with libass [verified locally].

**[Script Info]**
- `PlayResX`/`PlayResY` define the coordinate space. Set them to the output resolution (1080x1920 for Shorts) so font sizes and margins are in real pixels.
- `ScaledBorderAndShadow: yes`
- `WrapStyle: 2` (no auto-wrap; you control line breaks with `\N`)

**Style line order:** `Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold(-1/0), Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle(1=outline+shadow, 3=opaque box), Outline, Shadow, Alignment(numpad 1–9; 2=bottom-centre, 5=middle, 8=top), MarginL, MarginR, MarginV, Encoding`.

**Colours:**
- Colours are `&HAABBGGRR`, in **BGR order**, with alpha 00 = opaque and FF = invisible. Yellow is `&H0000FFFF`, and the accent in my test was `&H0000E5FF`.
- Inline: `\c&HBBGGRR&` or `\1c` for fill, `\3c` for outline, `\4c` for shadow.
- `\alpha&H80&`, `\1a`, `\3a`

**Karaoke tags:**
- `{\kNN}`: syllable timing in **centiseconds**. Unsung text shows SecondaryColour and switches to PrimaryColour instantly.
- `\kf` (or `\K`): sweep fill left to right.
- `\ko`: outline-only.

**Pop and animation tags:**
- `\t(t1,t2,[accel,]tags)`: times in ms relative to the line start. Example pop: `{\fscx80\fscy80\t(0,120,\fscx110\fscy110)\t(120,200,\fscx100\fscy100)}`
- `\fad(in,out)`, `\move(x1,y1,x2,y2,t1,t2)`, `\pos(x,y)`, `\an5`, `\org`
- `\bord6`, `\shad2`, `\blur2` or `\be1` (soft outline), `\fs`, `\fn`, `\b1`, `\frz` (rotation)

**Two word-highlight patterns:**
1. **One Dialogue per word.** Re-emit the whole chunk each time, coloring the active word with `\c` and optionally `\t`-scaling it (clipify `build_ass.py`). This is most robust and allows a per-word scale pop and background-box highlight.
2. **One Dialogue per chunk with `\k`.** Smaller file, but limited to a colour switch or sweep.

Chunking rules (video-use): 2–3 words, uppercase for Shorts, break on punctuation or pauses of 0.3 s or more, never flash a cue shorter than 0.35 s, `MarginV` about 35 px at 1080p or a larger ratio for 9:16, and keep the bottom 20 % clear of platform UI. stable-ts can emit word-level ASS directly with `result.to_ass(..., word_level=True)`.

**HTML caption alternative (HyperFrames):**
- Install a caption component (`hyperframes add caption-highlight` / `caption-pill-karaoke` / `caption-kinetic-slam` …) or write spans timed from `transcript.json` (`hyperframes transcribe` writes word-level timestamps into the project).
- Render as a **transparent WebM or MOV** and overlay LAST with ffmpeg, or render the whole edit inside HyperFrames with the `<video>` as the base layer.
- Benefits: web fonts, gradients, emoji, blur and layout that ASS cannot do. `check --caption-zone "x0=0;y0=0.82;x1=1;y1=1;severity=error"` QA's caption placement against overlap.
- Cost: a slower render than libass.

---

## 8. Free asset sources and licenses

| Type | Source | License summary | Source URL |
|---|---|---|---|
| Fonts | Google Fonts | Mostly SIL OFL 1.1 (some Apache-2.0). Free commercial use, embedding and bundling allowed; cannot sell the font alone. DM Sans is OFL (used by WeAreNoCode). | https://fonts.google.com/knowledge ; WeAreNoCode PDF above |
| Fonts | Fontshare (Indian Type Foundry) | "ITF Free Font License": free for personal and commercial use [unverified in session; the license page did not render] | https://www.fontshare.com/licenses |
| Fonts | Velvetyne | Libre fonts, mostly SIL OFL [unverified per font; check each] | https://velvetyne.fr |
| SFX | Freesound | Per-sound CC0, CC-BY (credit required) or CC-BY-NC (no monetized use). Filter for CC0 [unverified in session] | https://freesound.org/help/faq/ |
| SFX, music, video | Pixabay | Free, no attribution, may modify. Cannot redistribute standalone. No commercial use of recognisable trademarks or brands. [from source] **Content ID risk:** some uploads are fingerprinted, so keep the license certificate [secondary] | https://pixabay.com/service/license-summary/ ; https://www.foximusic.com/blog/?p=10 |
| SFX, music, video | Mixkit | SFX free for commercial and personal use, no attribution. Stock Music Free License excludes broadcast, CD and games uses [secondary] | https://mixkit.co/llm-info/ ; https://kripeshadwani.com/mixkit-review/ |
| Music | YouTube Audio Library (YouTube Studio) | Free; tracks downloaded there are not Content-ID claimed. Some tracks require attribution (check the per-track label) [secondary] | https://www.foximusic.com/blog/?p=546 |
| Music | Uppbeat free tier | 3 downloads (one restored per month) with partial catalogue access. Free users must paste the credit into each video's description; the safelist is paid only. | https://uppbeat.io/pricing |
| Stock video | Pexels | Free commercial use, no attribution, cannot sell unaltered copies [unverified in session]. Free API key. | https://www.pexels.com/license/ |
| Stock video | Coverr | Free commercial use, no attribution. No resale, no competing service, **no AI training use** [from source] | https://coverr.co/license |
| Icons | Lucide | ISC [from source: LICENSE] | https://github.com/lucide-icons/lucide |
| Icons | Phosphor | MIT [from source] | https://github.com/phosphor-icons/core |
| Icons | Iconify | Aggregator; the license is per icon set (MIT, Apache, CC-BY…), so check the `license` field in each set's JSON [unverified] | https://iconify.design |
| Lottie | LottieFiles free animations | Lottie Simple License: free personal and commercial use, attribution not required; cannot redistribute or resell standalone files [secondary/help-centre] | https://help.lottiefiles.com/hc/en-us/articles/900002438343 |
| UI for graphics | shadcn/ui | MIT [from source] | https://github.com/shadcn-ui/ui |
| UI for graphics | Magic UI | MIT [from source] | https://github.com/magicuidesign/magicui |
| UI for graphics | React Bits | **MIT + Commons Clause** (free use, cannot sell the components themselves) [from source: LICENSE.md] | https://github.com/DavidHDev/react-bits |
| UI for graphics | Aceternity UI | The licence page covers Pro (end products include videos). Free-component terms were not stated on that page [from source, partial] | https://ui.aceternity.com/licence |
| UI for graphics | Motion Primitives (ibelick) | MIT per the repo [unverified; the LICENSE path 404'd] | https://github.com/ibelick/motion-primitives |

**Important for porting React UI kits to HyperFrames:** these libraries animate with Framer Motion or CSS on wall-clock time. HyperFrames needs seekable, paused GSAP timelines and no `Date.now`/rAF, so treat them as visual design references and re-implement the motion in GSAP. HyperFrames ships `/remotion-to-hyperframes` and a `gsap` doc for this.

---

## 9. Other things a top-tier editor skill should include

- **Face detection, with a breaking change [verified locally].**
  - `mediapipe` on PyPI is now **1.1.0**, and its wheel contains **no `mediapipe/python/solutions/` at all**. Code using `mp.solutions.face_detection` (OpenMontage `face_tracker.py`, claude-shorts `compute_reframe.py`) fails on a fresh install.
  - Use the Tasks API instead: `mediapipe.tasks.python.vision.FaceDetector`, with a `blaze_face_short_range.tflite` model file (present in the wheel), or `FaceLandmarker`.
  - Alternatives that need no model download: OpenCV Haar (`cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'`, ships with opencv-python, used by chrislema) or OpenCV YuNet (`cv2.FaceDetectorYN`, model from opencv_zoo).
  - Sample at about 5 fps.
- **Caption placement:** detect the face box per section, then put captions in the band that avoids it. Typical spots are the lower-third band in 16:9 and about 65–75 % height in 9:16, above the Shorts UI. Verify with `hyperframes check --caption-zone`.
- **Auto-reframe 16:9 to 9:16:**
  - Use one static crop per section or sentence and cut at section boundaries rather than tracking every frame (chrislema).
  - If panning, smooth the face-x with a moving average or EMA and change crop x through `sendcmd` or a piecewise `crop` x-expression (OpenMontage, clipify).
  - Never crop off the top of the head: keep the face at about 30 % from the top.
  - For two speakers, use ROI motion-energy speaker detection (clipify) or a split-screen stack.
- **B-roll retrieval:** Pexels and Pixabay APIs (free keys), plus OpenMontage's adapter list (archive.org, NASA, Wikimedia, LoC, Coverr, Mixkit). Follow b-roll-finder's method: classify each beat as Receipts, Entity, Concept or Meme; source the meaning; strip audio; apply a subtle Ken Burns on stills.
- **yt-dlp** (2026.08.19) [verified locally: flags present in `--help`]:
  - `yt-dlp -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 -o "%(title)s.%(ext)s" URL`
  - `--download-sections "*00:01:00-00:02:00" --force-keyframes-at-cuts`
  - `--write-auto-subs --sub-langs "en.*,hi" --skip-download --convert-subs srt`
  - `--cookies-from-browser chrome`, `--write-info-json`
  - The new `--js-runtimes` option: YouTube extraction now needs a JS runtime such as Deno [unverified detail].
- **Beat detection [verified locally, librosa 1.0.0]:**
  - `tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')` and `librosa.onset.onset_detect(y=y, sr=sr, units='time')`.
  - Gotcha: `tempo` comes back as an ndarray (`[117.45]`), so use `float(np.atleast_1d(tempo)[0])`. With `trim=True` (the default) the first beat can be dropped.
  - HyperFrames also has `hyperframes beats` (writes `beats/<audio>.json`).
- **Denoise and voice:**
  - DeepFilterNet prebuilt binary: `deep-filter -D -o outdir in_48k.wav`. **It accepts 48 kHz WAV only**, and **use `-D/--compensate-delay` or A/V sync shifts**. Python route: `pip install torch torchaudio` then `pip install deepfilternet`, then `deepFilter in.wav -o out/ [--pf]` [from source: Rikorose/DeepFilterNet README].
  - FFmpeg `arnndn=m=model.rnnn` (RNNoise; needs a model from GregorR/rnnoise-models) or `afftdn` (present in this build).
  - Match RMS after denoising rather than loudness-normalizing; master once at the end (hassancs91).
- **Background removal:** `hyperframes remove-background in.mp4 -o subject.webm [-b plate.webm]` gives a transparent subject for "text behind the speaker" [verified locally: help only]. `rembg` 2.0.85 is image-focused: `pip install "rembg[cpu,cli]"`, then `rembg i in.png out.png` / `rembg p indir outdir` [unverified locally].
- **Eye contact:** I found no free, offline, open-source tool for recorded video. NVIDIA Broadcast Eye Contact (Windows with RTX GPU, free) and Apple's FaceTime eye contact (live only) are the practical options [unverified]. Recommend "look at the lens" coaching instead.
- **QA loop worth copying:**
  1. `ffprobe` duration against the EDL.
  2. `ebur128` integrated loudness and true peak, plus per-section RMS.
  3. A filmstrip and waveform at every cut ±1.5 s (video-use `timeline_view`).
  4. A second ASR pass over the render, diffed against the kept words, with an A/V drift check (hassancs91 `verify_cut.py`).
  5. blackdetect and freezedetect.
  6. HyperFrames `check --json` and a `snapshot` contact sheet.
  7. A critic sub-agent for anything the user will publish.
  8. Cap the passes at 3.
- **Memory and learning:**
  - `edit/project.md` session log (video-use)
  - `TASTE.md` with a `Confirmed-by:` gate, and bans persisted immediately (b-roll-finder)
  - "Can you learn from what we did and add it to the skill?" (WeAreNoCode)
  - A STYLE-GUIDE with a "Yours" column (WeAreNoCode)
  - A compounding SFX and component library with loudness metadata (hassancs91)
- **Taste defaults collected:**
  - Pad cuts 50 ms before and 80 ms after.
  - Prefer silences of 0.4 s or more as cut points; under 0.15 s is unsafe.
  - Use 0.4–0.6 s of air at speaker handoffs.
  - Punch zooms 1.18–1.30 as hard cuts; Ken Burns at most 1.14; focal y 0.42.
  - Use no more than about 8 SFX per 18 s, each tied to a visible event and started `attack` seconds early.
  - Duck music 12–15 dB under speech.
  - Master to -14 LUFS / -1 dBTP.
  - Hold the final frame of an animation for at least 1 s.
  - Show one new element at a time.


# ===== FILE: references/toolkit-setup.md =====

# Toolkit setup and troubleshooting

## Where to run this skill

| Surface | Works? | Notes |
|---|---|---|
| **Claude Desktop, Code tab, Local** (or Claude Code CLI) | Full workflow | Files stay on the user's machine; ffmpeg, Node, Python and Chrome run locally. Recommended. Permissions on "Auto" (or accept edits) avoids hundreds of prompts during renders. |
| **Claude Desktop, Cowork** | Full workflow | Runs on the user's computer; same tools. |
| **Claude.ai chat / Desktop chat with code execution** | Partial | Sandbox: no persistent folder, restricted network (model and font downloads may fail), usually no ffmpeg/Chrome. Use it for planning, style cards, caption files from uploaded transcripts. Say so plainly. |

Installing the skill:
- Code tab / Claude Code: put the `ai-video-editor` folder in `~/.claude/skills/` (all projects) or `<project>/.claude/skills/` (one project). Open a **new thread**: skills load when a thread starts.
- Claude.ai / Desktop chat: Settings, Capabilities, Skills, upload the `.zip` (the folder zipped, SKILL.md at its root).
- Recommended project folder: something like `Video Editing/`, then each video in `video-edits/<project>/`.

## Step 1: check

```bash
python3 scripts/doctor.py          # Windows: python scripts\doctor.py
```

Install only what is missing, after the user says yes. One line of "why" per tool.

## Step 2: install by OS

| Tool | Why | macOS | Windows | Linux |
|---|---|---|---|---|
| ffmpeg + ffprobe | cutting, audio, export, QA | `brew install ffmpeg` | `winget install --id Gyan.FFmpeg -e` (full build, has libass + libvpx) | `sudo apt-get install -y ffmpeg` |
| Python 3.10+ | runs the scripts (standard library only) | preinstalled or `brew install python` | `winget install Python.Python.3.12` | preinstalled |
| Node.js 22+ | HyperFrames | `brew install node@22` | `winget install OpenJS.NodeJS.LTS` | nvm: `nvm install 22` |
| HyperFrames | HTML to video motion graphics | `npx hyperframes@latest doctor`, then `npx hyperframes browser ensure` | same | same |
| HyperFrames skills | official composition workflows | `npx hyperframes skills update` | same | same |
| Remotion (optional, per project) | React motion graphics with frame-level control | `cp -r assets/remotion <project>/work/remotion && cd <project>/work/remotion && npm install` (no global install; first render downloads Chrome Headless Shell) | same | same |
| Transcription (one is enough) | word timestamps | `python3 -m pip install mlx-whisper` (Apple Silicon, fastest) | `python -m pip install faster-whisper` | `python3 -m pip install faster-whisper` |
| yt-dlp (optional) | download reference videos | `brew install yt-dlp` | `winget install yt-dlp.yt-dlp` | `python3 -m pip install -U yt-dlp` |
| opencv-python (optional) | face share in style analysis, face-centred reframe | `python3 -m pip install opencv-python` | same with `python` | same |
| DeepFilterNet (optional) | heavy voice denoise | prebuilt `deep-filter` binary from GitHub releases, or `pip install torch torchaudio deepfilternet` | same | same |
| rembg (optional) | background removal for stills | `python3 -m pip install "rembg[cpu,cli]"` | same | same |

Notes:
- Homebrew ffmpeg: check filters with `ffmpeg -hide_banner -filters | grep -E " (subtitles|ass|drawtext|zoompan|sidechaincompress|loudnorm) "`. If `subtitles` is missing, `brew install ffmpeg-full` (or the tap that bundles libass).
- Transcription on a GPU machine with a broken CUDA/cuDNN install: `transcribe.py` tries the GPU in a child process and falls back to CPU int8 on a crash. Pass `--device cpu` to skip the attempt.
- Remotion licence: free for individuals, for-profit companies with up to 3 employees and non-profits; larger companies need a Company License (remotion.pro). HyperFrames is Apache-2.0.
- Whisper models download on first use (hundreds of MB from Hugging Face). Corporate networks may block it; `transcribe.py` then falls back to `npx hyperframes transcribe` and finally reports every engine's error.
- Model choice: `large-v3-turbo` for most work; `small` for quick drafts; `large-v3` for Hindi and accented speech. Parakeet (via `npx hyperframes transcribe -e parakeet` or `parakeet-mlx`) is very fast and accurate for English and European languages but has no Hindi.
- auto-editor is optional. Note that PyPI ships 29.x while GitHub releases are 31.x with different flags (`--when-silent` vs `--when-inactive`); there is no `--export json` (use `--export v3`). This skill's `plan_cuts.py` does transcript-aware cutting without it.

## Step 3: tiny test (prove it works before a real edit)

```bash
python3 scripts/probe.py <their clip>
ffmpeg -ss 0 -t 5 -i <their clip> -c:v libx264 -crf 20 -c:a aac work/test5s.mp4
python3 scripts/qa.py work/test5s.mp4 --out work/qa-test
```
Show the user the 5 s file and the QA lines. For HyperFrames: `npx hyperframes init test --non-interactive --example blank`, copy `gsap.min.js` in if offline, `npx hyperframes render test -o test.mp4`.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| HyperFrames render: `Cannot read properties of null (reading 'timeline')` | GSAP CDN blocked | vendor `gsap.min.js` next to `index.html` |
| Render extremely slow / times out on Mac | software Chrome rendering | `PRODUCER_BROWSER_GPU_MODE=hardware` or `--browser-gpu`; fewer `--workers` on 8 GB machines |
| Render waits 45 s then works | composition without a timeline | add `data-no-timeline` to the root |
| Video freezes under graphics | sparse source keyframes | re-encode with `-g <fps> -keyint_min <fps>` (probe.py prints the command) |
| Wrong font in render, no error | font not found, fallback used | local `@font-face` with the real file; for libass pass `--fonts` folder; check with `fc-scan` |
| Transparent WebM has a black background after compositing | native VP9 decoder drops alpha | decode with `-c:v libvpx-vp9` before the `-i` (overlay.py does this) or use ProRes 4444 `.mov` |
| Captions out of sync after cutting | captions made from the raw transcript | use `work/words_cut.json`; re-run plan_cuts after any EDL change |
| Lip-sync drift on long edits | per-chunk AAC joins | render_cut.py renders audio in one pass; re-render with the current version |
| Whisper text where nobody speaks | hallucination over silence | delete those words from words.json; consider `--verbatim` and checking low-confidence words |
| Hindi comes out translated to English | auto language detection | `--language hi`; for romanized output see captions.md section 8 |
| Washed-out colours after export | HDR source or missing colour tags | probe.py warns on HDR; tone-map first; our encodes tag BT.709 |
| Windows: subtitles filter fails on path | drive-letter colon in filtergraph | captions.py escapes it; if hand-writing, use `subtitles='C\:/path/subs.ass'` |
| yt-dlp: "Sign in to confirm" or extraction errors | YouTube changes | `yt-dlp -U`; `--cookies-from-browser chrome`; or ask the user for the file |


# ===== FILE: references/qa-checklist.md =====

# Pre-delivery QA checklist

Do not tell the user "done" until every line is checked or explicitly reported as not checkable.

**Three rules about the result itself:**
- `qa.py` exits 1 on any FAIL. A WARN is not a PASS: every WARN gets a written disposition in `EDIT_STATE.md`
  (fixed / accepted because ... / user asked).
- Write `qa/qa-look.md`: one line per sheet you opened and what you saw. A sheet you did not open is not checked.
- Approvals are written, never assumed: the user's words, the date and what they approved go into
  `EDIT_STATE.md` before the next stage starts. Full list of traps: `mistakes-and-fixes.md`.

## Before the build (gates)
- [ ] Storyboard approved by the user (`storyboard.py` passed: contiguous scenes, verbatim VO, 2+ style options)
- [ ] Visual sources decided (user assets / web with licences / Higgsfield yes-no / prompt pack) and every
      scene has a visual or a stand-in
- [ ] Music/SFX source decided (Epidemic Sound or free, licence noted)
- [ ] 3-4 still frames per scene reviewed before animating it (HyperFrames snapshots)

## Automatic (scripts)
- [ ] `python3 scripts/qa.py <final> --edl work/edl.json --captions <ass> --platform <p>` shows no FAIL
- [ ] Loudness -14 LUFS (+/-1), true peak at most -1 dBTP
- [ ] H.264 (or HEVC/AV1 on request), yuv420p, AAC 48 kHz, faststart, BT.709 tags
- [ ] Duration matches the EDL (render_cut.py prints both); audio and video stream durations match (ffprobe)
- [ ] No black frames, no frozen live footage, no flash frames (shots under 3 frames)
- [ ] `python3 scripts/verify_cut.py <render> work/words_cut.json`: no clipped or ghost words at cut points; no drift over 250 ms (Whisper word times are only good to about +/-200 ms)
- [ ] HyperFrames graphics: `npx hyperframes check .` 0 findings for every composition
- [ ] 9:16: `qa.py <final> --safe <zone>` run; `safezone.py html <comp> --platform <zone>` PASS for every
      composition; `safezone.py alpha <overlay.mov> --platform <zone>` PASS for every alpha overlay
- [ ] `probe.py` warnings (VFR, HDR, odd fps, mono) each have a disposition

## Look (open every sheet yourself)
- [ ] `qa/cuts.png`: every edit point invisible or intentional; no jump that the punch-in failed to hide
- [ ] `qa/captions.png`: readable, correct spelling of names, inside the safe box, never over eyes or mouth, one highlight per group
- [ ] `qa/safezone_<zone>.png`: no text, logo or CTA under the top UI, bottom description or the right rail
- [ ] `qa/overview.png`: colour consistent shot to shot; nothing broken; rhythm varies
- [ ] Every graphic frame (`npx hyperframes snapshot`): no clipped text, no overlaps, contrast holds, on-brand, lands on its word
- [ ] First frame works as a thumbnail (Shorts) and the first 3 s already deliver the hook
- [ ] Slop audit: at most 2 font families, 1 accent, no emoji icons, no default-banned effects unless chosen

## Listen (if you cannot hear audio, say so and list the timestamps the user should check)
You cannot hear. Numbers (LUFS, peak, mono check) prove levels, not taste: write the timestamps of every music
in/out, SFX and join into `EDIT_STATE.md` under "Listening note" and ask the user to listen to those.
- [ ] Every join: no click, no clipped consonant, no doubled breath
- [ ] Music never fights the voice; no vocals under speech; silence before reveals where planned
- [ ] SFX land on visible events only
- [ ] **Closed Eye Test:** the cut holds attention with eyes closed (fix voice, rhythm and gaps before polish)
- [ ] Repeated SFX are varied (finish.py does it), risers peak on the hit frame, pops 8-14 dB under impacts
- [ ] Phone-speaker listen: nothing important lives only in the sub

## Structure
- [ ] First visible motion within about 0.13 s; frame 1 is not black, a logo or a slow fade
- [ ] 0-3-8 s ladder: visual hook at 0 s, promise by 3 s, first payoff/escalation by 8 s
- [ ] Long-form: thumbnail/title promise confirmed within 15 s (stopwatch it), then extended; the opening does
      not repeat the thumbnail text
- [ ] **Mute test:** the first 15 s confirm the promise without sound
- [ ] Pacing arc: no two same-tempo scenes back to back; no repeated pattern
- [ ] Tile strip across the timeline (contact sheet every 2 s): no palette drift, type tiers respected, one
      accent, 70/20/10 visual weight
- [ ] Kinetic-type reels (only if that is the chosen style): 25-40% of words captioned (captions.py --selective prints the share), one accent, texture only if the style card or preset asked for it
- [ ] Deliberate dead stops: `qa.py --silence-at <t>` PASS (14 LU under the programme)
- [ ] Remotion builds: `npx tsc -p .` clean, render log has no `FONT MISSING`, text-only render passes `safezone.py alpha`

## Truth
- [ ] Every number, name, quote and claim on screen comes from the transcript or the user
- [ ] Licences noted for music, SFX, stock, fonts (Fontshare fonts not redistributed)
- [ ] No Pinterest or Google Images downloads shipped without a known licence; user-supplied assets used as supplied
- [ ] Synthetic people in ads disclosed where required (ugc-ads.md)

## Deliver
- [ ] Final file in `renders/` with a version number; source untouched
- [ ] `.srt` exported for YouTube upload
- [ ] For YouTube: chapters list (00:00 first, 3+ chapters, 10 s+ each) and end-screen window (last 5-20 s) suggested
- [ ] `EDIT_STATE.md` updated (what was delivered, open notes)
- [ ] Asked: "Should I add what we learned to the skill?"

