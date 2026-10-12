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
