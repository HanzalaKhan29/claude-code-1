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
