# Looks library: 20 art directions for motion graphics

Source: "20 Looks for Claude Motion" (WeAreNoCode free community, skool.com/wearenocode). Reproduced here so the agent can paste a Look into a graphics brief. Every font named is a Google Font, so `scripts/fetch_fonts.py "Family:weights"` can download it.

## Why a Look block works

A plain prompt ("make a motion graphic about X") gets a basic, templated result. One paragraph that starts with `Look:` and reads like a brief to a designer fixes it, because it pins the decisions the model would otherwise default: background, palette with roles, display and body fonts, how numbers behave, how charts move, the easing personality, how scenes change, what the camera does, and what to avoid.

## The brief formula

Write every graphics brief in this order:

1. **Who you are** (the speaker / brand) and **who it is for**.
2. **The real numbers or words** (from the transcript or the user; never invented).
3. **Look:** one block from this file, with hex codes swapped to the brand.
4. **Format:** duration, resolution, fps, aspect, safe area.
5. **The next step** / end line.

When a HyperFrames workflow asks its quick style questions, answer "use the Look in the brief" and adjust in conversation afterwards.

Example (bookkeeper monthly report, Look 6):

> I'm a bookkeeper. Turn my client's September into a 30-second video for the owner of a plumbing company.
> Numbers: $86,400 came in, up 11% from August. $71,900 went out. Profit $14,500. Biggest jump: fuel, up 18%.
> Look: (Newsroom Data Desk block below)
> End on: "Next step: let's plan your Q4 taxes on our call."

## Matching a Look to a video

| Video type | Strong Looks | Caption style that pairs |
|---|---|---|
| Tech / SaaS / AI tools | 1 Tech Glassmorphic (use glass sparingly), 10 Bento Dashboard, 12 Retro Terminal, 20 Monochrome Keynote | 5 editorial, 10 minimal |
| Finance, business, data | 2 Swiss Grid, 6 Newsroom Data Desk, 10 Bento Dashboard, 14 Black and Gold Luxury | 7 documentary, 10 minimal |
| Education / explainers | 16 Whiteboard Sketch, 13 Paper Cut-Out, 8 Blueprint, 6 Newsroom | 3 pill, 8 karaoke |
| Real estate, local, maps | 3 3D Isometric Miniature, 15 Topographic Map | 1 clean-caps |
| Promo / offer / hype Shorts | 5 Neo-Brutalist, 9 Kinetic Type, 17 Memphis Playful | 6 viral, 1 clean-caps |
| Premium / personal brand | 4 Editorial Magazine, 14 Black and Gold, 20 Monochrome Keynote | 2 lower-serif, 5 editorial, 4 serif-italic |
| History / founder story | 19 Archival Documentary, 11 Risograph Zine | 7 documentary |
| Beauty / creator / fashion | 18 Y2K Chrome, 7 Soft Clay 3D | 4 serif-italic |

Honest caveat: some Looks (1 Glassmorphic, 18 Y2K Chrome, glows in 12) contain items on this skill's default ban list. They are allowed when the user picks that Look on purpose; keep the effect to the hero element, not everything.

## The 20 Looks

### 1. Tech Glassmorphic
Best for: a product walkthrough for a software tool, or an IT firm explaining a new service.

Look: Deep navy background (#0B1020) with two slow-drifting blurred glows, teal (#2DD4BF) and violet (#8B5CF6), behind frosted glass panels: 24px rounded corners, white at 8% opacity, background blur, a thin white edge. Text in white (#F8FAFC) and soft gray (#94A3B8). Headings in Sora SemiBold, large and tight. Body in Inter Regular. Numbers count up inside glass cards with a soft teal glow behind them. Charts are thin glowing lines and translucent bars that grow from the bottom. Panels float up into place with a gentle overshoot, then fade out. Scenes change with a focus pull: the old panels blur away as the new ones sharpen. Camera drifts slowly forward with parallax between layers. Avoid: neon overload, busy patterns, text on a glow with no panel behind it.

### 2. Swiss Grid
Best for: a quarterly results summary from an accounting firm or a consultant.

Look: Flat off-white background (#F4F1EA) on a strict 12-column grid with wide margins. No texture, no gradients. Black (#111111) for type, one signal red (#E63322) for the key number, light gray (#C8C4BB) for rules. Headings in Inter Tight Bold, very large, flush left, tight line spacing. Body in Inter Tight Regular, small. Graphic elements: thin horizontal rules, solid circles and rectangles, numbered section markers (01, 02, 03). Numbers sit huge and flush left, counting up in red. Bar charts are flat black bars on hairline axes. Motion is crisp and mechanical: elements slide in along the grid with a fast ease-out and stop dead. Scenes change with a hard horizontal wipe. Camera stays locked. Avoid: shadows, rounded corners, centered text, a second accent color.

### 3. 3D Isometric Miniature
Best for: a real estate market update, or a property manager's area report.

Look: A 3D isometric miniature world on a soft sky gradient (#FCE7C8 to #F9B98B), like a tabletop model at golden hour. Low-poly buildings and streets in warm cream (#FFF4E0), terracotta (#D9734E) and sage green (#8FB996), with long soft shadows and a light haze. Headings in Outfit SemiBold, body in Outfit Regular, on small floating white labels. Numbers appear as price tags or pins that pop up above buildings and count up smoothly. Charts are 3D blocks rising out of the ground like towers. Objects drop in from above with a soft bounce, one after another. Scenes change by gliding to another part of the same world. Camera holds the isometric angle, glides slowly and orbits a few degrees. Avoid: flat 2D icons, harsh black outlines, cold blue light.

### 4. Editorial Magazine
Best for: a financial advisor's market commentary, or a law firm's monthly client briefing.

Look: Warm paper background (#F5EFE6) with very faint grain, like a printed feature spread. Ink black (#1A1A1A), oxblood (#7A1F2B) for accents, gray-brown (#8A8178) for captions. Headlines in Instrument Serif, huge, with one word set in italic. Body in Libre Franklin Regular in narrow columns. Graphic elements: thin column rules, drop caps, pull quotes in large italic, small all-caps section labels with wide letter spacing, page numbers. Numbers look like a magazine stat: big serif figures with a short caption under them. Charts are thin ink lines with labels written right on them. Text reveals line by line through a soft upward mask, unhurried. Scenes change like turning a page, a slow horizontal slide. Camera makes slow pushes into the headline. Avoid: bright colors, icons, bouncy motion, sans-serif headlines.

### 5. Neo-Brutalist
Best for: a loud offer announcement for a gym, an agency or a trade business running a promo.

Look: Flat backgrounds that alternate between lemon yellow (#FFE24A) and white (#FFFFFF), no gradients. Every shape has a thick 4px black (#000000) border and a hard offset shadow, 8px down and right, zero blur. Accents in hot pink (#FF5CA8) and electric blue (#3B5BFF). Headings in Archivo Black, oversized, uppercase. Body in Space Grotesk Medium. Graphic elements: chunky rectangles, stickers, fat arrows, starbursts. Numbers sit in boxed tiles and snap to the final value with a quick shake. Bar charts are thick bordered blocks that slam up. Motion is fast and punchy: elements drop in with a hard snap, buttons press down into their shadow. Scenes change with a hard cut or a full-color block wipe. Camera is static. Avoid: soft shadows, thin fonts, slow fades.

### 6. Newsroom Data Desk
Best for: a bookkeeper's monthly client report, or an insurance broker explaining a rate change.

Look: A clean white background (#FFFFFF) with a pale gray panel behind each chart, like a data story on a news site. Text in near-black (#121212). One highlight color, deep blue (#1F5FBF), for this month, orange (#E8710A) for warnings, gray (#B5B5B5) for everything else. Headlines in Libre Franklin ExtraBold, sentence case, written as a one-line takeaway. Body in Source Serif 4. Labels sit right on the chart, no legends. Numbers tick up quickly and land with a short annotation line. Lines draw left to right, bars grow in order, and the key bar turns blue last. Motion is calm and quick, ease-out, no bounce. Scenes change with a fast fade through white. Camera stays still and zooms gently into the part that matters. Avoid: 3D charts, decoration, crowded pie charts.

### 7. Soft Clay 3D
Best for: a welcome video for new patients at a dental clinic, or new families at a tutoring service.

Look: Soft pastel background (#F3EEFF) under gentle studio light, no texture. Every object looks like smooth matte clay: rounded, puffy, with a soft inner highlight and a blurred contact shadow. Palette: lilac (#C9B6FF), peach (#FFC4A3), mint (#A8E6CF), with text in deep plum (#3B2A5C). Headings in Baloo 2 ExtraBold, round and friendly. Body in Nunito SemiBold. Graphic elements are chunky 3D icons, pill buttons and small rounded tiles. Numbers sit on clay badges and count up with a squishy pop. Bar charts are rounded clay pillars that grow with a soft wobble. Elements pop in with a springy squash and stretch, then settle. Scenes change as objects bounce out and new ones roll in. Camera slowly orbits a few degrees. Avoid: sharp corners, thin lines, dark backgrounds.

### 8. Blueprint
Best for: a contractor's project walkthrough, or a home inspector's report summary.

Look: Deep blueprint blue background (#0D3B66) with a fine white grid at 10% opacity and a faint paper texture. All lines in white (#FFFFFF) and pale blue (#A9D6F5), with safety yellow (#FFD23F) only for the thing that matters. Headings in Barlow Condensed SemiBold, uppercase, widely spaced. Notes in Architects Daughter, like hand-lettered annotations. Graphic elements: technical line drawings, dimension lines with arrows, callout circles, a title block in the corner with a drawing number. Numbers appear as measurements on dimension lines and count up. Charts are plotted as lines on the grid. Everything draws itself on, stroke by stroke, at a steady drafting pace. Scenes change by zooming into a detail callout that becomes the next drawing. Camera pans slowly across the sheet. Avoid: filled shapes, gradients, cute icons.

### 9. Kinetic Type
Best for: a 30-second promo for a new service, or the opening of a sales presentation.

Look: The words are the animation. Solid backgrounds flip between jet black (#0A0A0A) and signal yellow (#FFD400), with white (#FFFFFF) type. Headings in Anton, uppercase, filling the frame edge to edge. Supporting lines in Barlow Medium, small. No icons, no illustration. Words slam in one at a time on the beat, stretch and stack. Key numbers fill the screen and count up fast. Charts are made of type: a bar is a word stretched to length. Motion is fast with hard eases, 2 to 4 words per second, a short hold on the punchline. Scenes change with a wipe that reveals the next scene through the letters. Camera makes quick punch-ins and small rotations. Avoid: more than 6 words on screen, soft fades, thin weights.

### 10. Bento Dashboard
Best for: a marketing agency's monthly results, or a property manager's update for owners.

Look: Light cool gray background (#F2F4F7) with rounded tiles (20px corners) in different sizes. Tiles in white (#FFFFFF) with a very soft shadow, one hero tile in deep ink (#101828) with white text. Emerald (#12B76A) for good news, coral (#F04438) for bad news. Headings in Geist SemiBold, numbers in Geist Mono. Each tile holds one idea: a big number, a sparkline, a progress ring or a short bar list. Numbers roll up like an odometer. Sparklines draw left to right, rings fill clockwise. Tiles arrive one by one with a short stagger, scaling up from 96%. Scenes change when one tile grows to fill the screen and becomes the next scene. Camera is flat and still. Avoid: more than 8 tiles, 3D, heavy shadows.

### 11. Risograph Zine
Best for: an event recap for a cafe, a local shop or a community workshop.

Look: Off-white uncoated paper (#F7F3EA) with visible grain, like a two-color print. Inks: fluorescent pink (#FF48B0) and teal (#0078BF), with yellow (#FFE800) where they overlap. Ink layers sit a few pixels off, with rough edges. Headings in Bricolage Grotesque ExtraBold, chunky and a little uneven. Body in Courier Prime. Graphic elements: halftone dot fills, cut-out shapes, stars, rubber-stamp marks. Numbers are big, printed in pink over a teal halftone, and step up in visible jumps. Bar charts are halftone blocks. Motion runs at 12 frames per second for a handmade feel: things pop, jitter slightly and stamp into place. Scenes change by sliding a new sheet of paper over the old one. Camera is a flat overhead view. Avoid: smooth gradients, gloss, perfect vector edges.

### 12. Retro Terminal
Best for: an IT provider's monthly report, or a security check-up for a small business.

Look: A black CRT screen (#050805) with faint scanlines, a soft green glow, slight screen curve and a gentle flicker. Text in phosphor green (#33FF66), dim green (#1A7A33) for secondary lines, amber (#FFB000) only for warnings. Headings in VT323, large. Body in IBM Plex Mono. Graphic elements: a blinking block cursor, command prompts, boxes and progress bars drawn with text characters. Text types on character by character at a fast, steady pace, and some lines print all at once. Numbers count up like a loading counter. Charts are text-character bar charts that fill block by block. Scenes change with a screen clear: a quick flash, a scanline sweep, then a fresh prompt. Camera stays locked with a slow push-in. Avoid: any color besides green and amber, rounded cards, bouncy easing.

### 13. Paper Cut-Out
Best for: a how-it-works explainer for an accountant's new service, or a nonprofit's year in review.

Look: Layered paper craft, built from stacked sheets of colored card with real depth. Each layer casts a soft shadow on the one below, with rough edges and a fine paper fiber texture. Palette: warm cream (#FAF3E3), forest green (#2F5D50), mustard (#E0A526), brick red (#B5462E), ink navy (#1F2A44) for text. Headings in Fraunces SemiBold, soft and slightly quirky. Body in Work Sans. Graphic elements: cut-paper hills, suns, buildings, folded corners. Numbers are printed on paper tags that flip up and count. Charts are stacked paper strips that slide up. Layers slide in from the sides with a soft ease, and pop-up pieces fold upward, like a hand-built set. Scenes change as a new paper layer slides across. Camera moves sideways with parallax. Avoid: gloss, neon, thin lines.

### 14. Black and Gold Luxury
Best for: a listing presentation for a high-end home, or a private wealth review.

Look: Deep black background (#0A0A0A) with a subtle warm vignette and very fine noise. Gold (#C9A55C) for lines, numbers and accents, with a soft metallic sheen sweeping across them. Warm ivory (#F2EBDD) for text, charcoal (#1E1E1E) for panels. Headings in Cormorant Garamond Light, large, with generous letter spacing. Small labels in Montserrat, uppercase, widely spaced. Graphic elements: hairline gold frames, thin dividers, a monogram-style emblem, plenty of empty space. Numbers fade in and count up slowly, then a light glint passes across them. Charts are thin gold lines with small dot markers. Motion is slow and deliberate, long ease-in-out, nothing bounces. Scenes change with a slow fade through black. Camera makes slow pushes in. Avoid: bright colors, fast cuts, heavy bold fonts, crowded layouts.

### 15. Topographic Map
Best for: a neighborhood report for an agent, or a territory update for an insurance broker or a delivery business.

Look: Off-white map paper (#EFEBE0) with light brown contour lines (#C9B79C) across the frame. Water in muted blue (#9CC3D5), parks in sage (#B7C9A8), roads in white with thin gray edges, and one route or zone color, vermilion (#E2522B). Headings in Josefin Sans SemiBold, uppercase and widely spaced like map labels. Place names in Lora Italic. Graphic elements: pins, dashed routes, a compass rose, a scale bar. Numbers sit in callout pins that drop onto the map and count up. Charts are zones that fill with color by value, like a heat map. Routes draw themselves along the roads. Scenes change by flying to a new part of the map. Camera pans and zooms smoothly across one big map. Avoid: satellite imagery, 3D buildings, app-style cards.

### 16. Whiteboard Sketch
Best for: walking new clients through a process, like how a claim works or the steps of buying a home.

Look: A clean whiteboard (#FAFAF7) with faint smudges near the edges. Marker colors: black (#1B1B1B) for most lines, blue (#1E5AA8) for labels, red (#D7263D) for circles and emphasis, green (#2E8B57) for good outcomes. Headings in Caveat Bold, body in Patrick Hand, both like quick handwriting. Graphic elements: hand-drawn boxes, wobbly arrows, plain icons (houses, coins, documents, clocks), underlines, check marks. Lines have a slight hand wobble. Numbers are written stroke by stroke, then circled in red. Charts are sketched bar charts with hatching. Everything draws itself on at writing speed, as if a marker is moving live. Scenes change with a quick eraser swipe, or by sliding to an empty part of the board. Camera is flat, with small zooms. Avoid: perfect geometric shapes, solid fills, drawn people.

### 17. Memphis Playful
Best for: a fun promo for a party rental business, a bakery's new menu or a salon's referral offer.

Look: Bright cream background (#FFF6E5) scattered with geometric patterns: squiggles, zigzags, confetti dots, triangles, half circles and small grid patches. Palette: hot coral (#FF6B6B), turquoise (#2EC4B6), sunflower (#FFC93C), and black (#1A1A1A) for outlines and text. Headings in Bungee, blocky and loud. Body in Rubik Medium. Shapes have thin black outlines, and some carry black dot or stripe patterns. Numbers sit inside bold shapes and pop up with a spin. Charts are colorful blocks and pie wedges with patterned fills. Motion is playful and springy: shapes spin in, bounce, wiggle once and settle, while the background patterns float slowly. Scenes change with a burst of shapes flying across the screen and clearing it. Camera is flat with small playful zooms. Avoid: muted colors, serif fonts, realistic shadows, cartoon characters.

### 18. Y2K Chrome
Best for: a launch teaser for a beauty brand, a boutique or a service for creators.

Look: Pale icy background (#EEF0FF) with a faint lilac haze and soft bokeh sparkles. Hero elements are glossy liquid chrome: silver (#C0C7D1) with bright white highlights and iridescent edges shifting between baby blue (#9AD0FF) and lilac (#D7B8FF). Deep navy (#0E1A3A) for text. Headings in Unbounded Bold, wide and bubbly. Body in Space Mono, small. Graphic elements: chrome blobs, star sparkles, glossy pill buttons, translucent plastic panels. Numbers are rendered in chrome and count up with a shine sweep. Charts are glossy rounded bars with reflective tops. Elements float in with a gentle bob and turn in 3D to catch the light. Scenes change with a liquid chrome morph or a sparkle flash. Camera drifts and tilts slightly. Avoid: flat matte colors, gritty textures, serif fonts.

### 19. Archival Documentary
Best for: a company history for an anniversary, or the founding story of a family business.

Look: A dark wooden desk (#2B2420) covered in aged paper. Paper in yellowed cream (#E8DCC2), ink in sepia brown (#4A3728), stamps in faded red (#9E2A2B), accents in tarnished brass (#A68A4D). Headings in Libre Baskerville Bold. Body and dates in Special Elite, like a typewriter. Graphic elements: typed index cards, file folders, stamps that thump down, a timeline drawn as a thread between pinned cards, and empty photo frames (to be filled with the user's photos). Numbers are typed on, then stamped. Charts look hand-ruled in ink on graph paper. Motion is slow: pages slide onto the desk, dust drifts, the light flickers softly. Scenes change by sliding to the next document. Camera makes slow pans and pushes across the desk. Avoid: bright colors, clean digital UI, fast motion.

### 20. Monochrome Keynote
Best for: a pitch to a big client, a board update, or the one number that matters in an annual review.

Look: A pure black stage (#000000) with nothing on it but the words. White (#FFFFFF) for type, mid gray (#8E8E93) for secondary lines, and one accent, electric blue (#2F80FF), for the key word or number. Headings in Manrope ExtraBold, very large and centered. Body in Manrope Regular. One idea per scene, never more than 8 words. No icons, no decoration. Numbers appear huge in the center, count up slowly, then hold. Charts are one thin line or one bar. Motion is calm: text fades up from 20px below with a long, smooth ease-out, then a full second of stillness before the next idea. Scenes change with a slow fade through black. Camera holds still, with a rare slow push-in. Avoid: clutter, bullet lists, a second accent color.

## Writing a new Look (for a brand or a measured creator)

Fill every slot; leaving one blank lets the model fall back to its defaults:

```
Look: <background colour + texture, hex> <what world it feels like>. Text in <hex> and <hex>.
One accent <hex> for <what it marks>; <hex> for <secondary role>. Headings in <Font Weight>,
<case, size, tracking>. Body in <Font Weight>. Graphic elements: <3-5 concrete elements>.
Numbers <how they appear and land>. Charts <how they draw>. Motion is <personality, ease, overshoot
budget>. Scenes change with <one transition>. Camera <locked / slow push / pans>. Avoid: <3-5 bans>.
```

For a measured creator, pull the hex codes from `measurements.json` (`palette_time_weighted`), the fonts from the frames you looked at, and the motion personality from cut rate and how their graphics enter.
