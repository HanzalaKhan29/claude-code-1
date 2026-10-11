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
