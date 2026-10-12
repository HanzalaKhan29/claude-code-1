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
