# Motion graphics, explainers and B-roll cards

Contents: 1 Tool choice · 2 Install HyperFrames + official skills · 3 Two ways to put graphics on footage · 4 The composition contract (fallback) · 5 Card planning for talking heads · 6 Motion doctrine · 7 Seam and entry techniques with numbers · 8 The production-spec brief · 9 Technique catalog · 10 Explainer templates · 11 Learning-science rules for explainers · 12 QA for graphics · 13 Conflicts resolved

Sources: HeyGen HyperFrames official skills (Apache-2.0: `hyperframes`, `hyperframes-core`, `talking-head-recut`, `motion-doctrine`, `cut-the-curve`, `seam-craft`), the 513-prompt Opus 5.5 study (`motion-prompt-research.md`), WeAreNoCode Looks (`looks-library.md`), `design-science.md`.

**Making a motion-graphics REEL** (the user's main focus: metromedia / earn.edits / earnera / lightyear style)? Read `motion-reels.md` first: it holds the measured genre grammar, and `assets/hyperframes/kinetic-reel/` is the tested starter. This file is the general HyperFrames craft underneath it.

## 1. Tool choice

| Need | Use | Why |
|---|---|---|
| Any designed graphic, card, title, chart, explainer, kinetic text | **HyperFrames** (`npx hyperframes`) | Plain HTML/CSS/GSAP, no build step, made for agents: `lint`, `check`, `snapshot` contact sheets, transparent MOV/WebM output, a 446-item registry of captions, lower-thirds and transitions |
| Plain word captions on footage | `scripts/captions.py` (libass) | Seconds to render; HyperFrames captions only when you need web-only looks |
| Simple punch-ins, crops, reframes | ffmpeg (`render_cut.py --punch`, `reframe.py`) | No browser render needed |
| The user already has a Remotion brand kit | Remotion | Respect existing work; Remotion needs a paid license for companies of 4+ people |

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
