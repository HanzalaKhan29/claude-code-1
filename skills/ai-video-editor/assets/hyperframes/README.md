# HyperFrames starters

`lower-third/index.html` is a transparent lower-third overlay (1920x1080, 5 s) that follows the HyperFrames
core contract and the motion rules in `references/motion-graphics.md`. Lint-clean and render-tested with
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
