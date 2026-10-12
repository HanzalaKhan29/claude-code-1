# Remotion starter: captioned edit with graphics on their words

A neutral template, not a house style. It puts the locked cut, word-timed captions, and graphics that land on
their spoken word into one React composition, sized to the platform's safe zone. Every look decision (fonts,
sizes, colours, highlight rule, texture) is a prop, so the same code serves a calm explainer, a Hormozi-style
short or a kinetic essay.

Tested with Remotion 4.0.535, React 19.1, on 1080x1920 at 30 fps: type-check clean, renders H.264, and the
transparent text-only render passes `safezone.py alpha` on all five zones (reels, reels-ad, tiktok, shorts, cross).

## Files

| File | Job |
|---|---|
| `src/Root.tsx` | registers the `Edit` composition; `calculateMetadata` sets size, fps and duration from props |
| `src/Edit.tsx` | layer order: footage, photo push-ins, texture, cards/titles/stats, captions, safe-zone guide |
| `src/Captions.tsx` | groups words (pause >= 250 ms, sentence end, word limit), wraps with real glyph widths, keeps the block inside the zone, max 2 lines |
| `src/Graphics.tsx` | `title`, `stat` (seek-safe counter, tabular digits), `image` (`push` full-frame or bordered `card` sized to clear the rail) |
| `src/safeZones.ts` | the same five zones as `scripts/_common.py` |
| `src/fonts.ts` | loads `public/fonts/*.ttf` before the first frame (`delayRender`), logs `FONT MISSING` otherwise |
| `props.example.json` | every prop with an example value |

## Use

```bash
cp -r <skill>/assets/remotion video-edits/<p>/work/remotion && cd video-edits/<p>/work/remotion
npm install
python3 <skill>/scripts/fetch_fonts.py "Inter:700,900" --dir public/fonts     # or the fonts the style card names
python3 <skill>/scripts/remotion_props.py --project . --video ../../renders/v2_graded.mp4 \
        --words ../words_cut.json --platform reels --keywords ../keywords.json --graphics ../graphics-remotion.json
npx remotion studio src/index.ts        # optional: preview, toggle showSafeZone in the props panel
npx remotion render src/index.ts Edit out/edit.mp4 --props=props.json --crf=18
```

No internet for Chrome? Remotion downloads its own headless shell on the first render. Point it at an existing
one instead: `--browser-executable=/path/to/chrome-headless-shell`.

Safe-zone QA (required for 9:16), a transparent render of only the text and graphics:

```bash
python3 <skill>/scripts/remotion_props.py ... --text-only --out props_qa.json
npx remotion render src/index.ts Edit out/qa.mov --props=props_qa.json --codec=prores --prores-profile=4444 \
        --image-format=png --pixel-format=yuva444p10le
python3 <skill>/scripts/safezone.py alpha out/qa.mov --platform reels      # PASS required
```

Then `finish.py` for the music, SFX and loudness, and `qa.py` on the final, as in the main pipeline.

## Graphics JSON

```json
[
  {"type": "title", "at": 0.1, "duration": 1.4, "text": "Hook title\nfrom the VO", "sub": "optional"},
  {"type": "stat", "at": 5.0, "duration": 2.5, "from": 0, "to": 1250, "suffix": "+", "label": "words from the VO"},
  {"type": "image", "at": 9.0, "duration": 2.0, "src": "work/stills/photo.jpg", "mode": "card", "aspect": 1.333},
  {"type": "image", "at": 12.0, "duration": 2.0, "src": "work/stills/photo.jpg", "mode": "push"}
]
```

`at` is the start time of the spoken word on the edited timeline (`words_cut.json`). Each graphic starts on
that word, enters with a decelerating spring and leaves 0.2 s before its end. Nothing appears before its word.

## Extending it

- New graphic type: add a member to `Graphic` in `types.ts` and a component in `Graphics.tsx` that takes `zone`
  and computes its own size from it (never a fixed pixel position).
- Animation must be a pure function of `useCurrentFrame()`: `interpolate`, `spring`, `random(seed)` from
  `remotion`. No `Math.random`, `Date.now`, timers or CSS transitions: frames render in parallel and out of order.
- Load anything async (fonts, JSON, images measured in JS) inside `delayRender` / `continueRender`.
- Footage goes in through `<OffthreadVideo>` (frame-exact), assets through `staticFile()` from `public/`.
