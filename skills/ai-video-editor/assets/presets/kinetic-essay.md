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
