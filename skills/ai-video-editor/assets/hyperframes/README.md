# HyperFrames starters

`kinetic-reel/` (1080x1920, 8 s, full-frame) is the motion-reels genre grammar from `references/motion-reels.md`:
whisper tier (italic serif ~4.5%) + apex tier (Anton caps ~16-19% cap height), hard word pops on the spoken
word, the ground colour rotating ink -> accent -> cream between beats instead of transitions, one accent, a
hand-drawn annotation ellipse, a soft 3 s end card, and seek-safe film grain (`grain.png`, ~2.5%). The copy is
EXAMPLE text: replace the words in the HTML and the times in `BEATS` with the user's VO and `words_cut.json`
times. Fonts: `fetch_fonts.py "Anton:400" "Instrument Serif:i400" "JetBrains Mono:700" --dir <dir>/fonts`.
Render with `npx hyperframes render . --crf 20 -o reel.mp4` (grain defeats compression; CRF 18-22 keeps the
file sane, the platform re-encodes anyway). Lint- and check-clean with HyperFrames 0.8.147.
Gotchas learned building it: SVG `feTurbulence` grain renders blank in headless capture (use the PNG tile);
`vector-effect: non-scaling-stroke` breaks `pathLength` draw-on math (use a thin stroke in viewBox units);
an opacity tween is a fade, not a pop (use `tl.set` for visibility, tween only the scale settle); text under
the grain layer needs `data-layout-allow-occlusion` on each text node or `check` reports text_occluded.

`stat-counter/index.html` is a transparent stat card with a seek-safe counter and fixed-width digits (example numbers: replace them). Fonts: `fetch_fonts.py "Manrope:500,800" --dir <project>/fonts`. Same workflow as below.

`lower-third/index.html` is a transparent lower-third overlay (1920x1080, 5 s) that follows the HyperFrames
core contract and the motion rules in `references/motion-graphics.md`. Both pass `hyperframes lint` and `check` and were render-tested with
HyperFrames 0.8.147.

Use:
```bash
mkdir -p work/gfx/lower-third/fonts && cp -r assets/hyperframes/lower-third/* work/gfx/lower-third/
python3 scripts/fetch_fonts.py "Inter:500,800" --dir work/gfx/lower-third/fonts
# GSAP offline: npm pack gsap@3.14.2 && tar -xzf gsap-3.14.2.tgz && cp package/dist/gsap.min.js work/gfx/lower-third/
cd work/gfx/lower-third && npx hyperframes lint . && npx hyperframes snapshot . --at 0.8,2.5,4.7
npx hyperframes render . --format mov -o ../lower-third.mov
cd - && echo '[{"file":"work/gfx/lower-third.mov","at":3.2}]' > work/graphics.json
python3 scripts/overlay.py renders/v1.mp4 work/graphics.json renders/v2_graphics.mp4
```

Edit the CONTENT block (real name and role only) and the BRAND variables (one accent). For 9:16, change
`data-width`/`data-height` and the viewport to 1080x1920, scale type x1.3, and move the block inside the safe
box (bottom at least 672 px from the bottom edge).

For anything bigger than a single card, install the official skills (`npx hyperframes skills update`) and use
`/talking-head-recut`, `/motion-graphics` or `/faceless-explainer`.
