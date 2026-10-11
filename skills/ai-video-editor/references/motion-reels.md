# Motion-graphics reels: the genre grammar (main focus)

The user's main focus is motion-graphics reels like **@metromedia.house, @earn.edits, @earnera.co and
@lightyear.residency**. When a brief says reel, Short, explainer or "edit like these pages" and nothing says
otherwise, default to this grammar. Every number here was measured frame by frame on 12 of their reels
(downloaded 2026-10-12, text heights in pixels, colours as saturated-pixel medians). Audio on those reels was
not analysed, so every audio claim about them is unverified. Their posts were ranked by likes (Instagram hides
views): never call them "most viewed".

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
18% cap height. On 9:16 a long apex word shrinks to fit the safe width; that is physics, not a bug. Keep apex
words short (one word, ideally 4-7 letters) when the format is vertical.

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
  finite timeline. Source: IT Master (C0yro0rgSII) 06:33-08:29.
- **Glass is conditional.** Allowed faint, bordered and behind type (never on the type itself); still banned as
  the default chrome of a whole video. The successor treatment is a soft ambient mesh gradient.
- **Glow** stays banned by default; lightyear's soft glow on Didone caps is a deliberate Look choice, allowed
  when the user picks that register.
- **The 70/20/10 check.** About 70% of the visual weight on the primary device (e.g. the apex type), 20% on the
  secondary (footage, cards), 10% on accents. "Everything everywhere" fails this check. [SECONDARY]
