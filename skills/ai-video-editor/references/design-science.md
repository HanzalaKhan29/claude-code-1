# Design Science for AI Video Editing & Motion Graphics

Contents: 0. Ten-line cheat sheet (apply by default) · 1. Typography for Video & Motion · 2. Curated Font Library for Video (48 fonts) · 3. Color · 4. Motion Design Principles · 5. Editing Grammar & Attention Psychology · 6. Sound Design Psychology · 7. Anti-"AI Slop" Visual Tells (and what to do instead) · 8. Machine-Readable Defaults (for the skill's config) · 9. Source List

A rules-first knowledge base for an agent that edits YouTube long-form and Shorts/Reels/TikTok and generates HTML/CSS/GSAP motion graphics rendered to video.

Conventions used throughout:

- **RULE** = a numeric default the agent should apply unless the brief says otherwise.
- **WHY** = one-line rationale.
- **SRC** = source key; full URLs are in the Source List at the end (section 9).
- **Evidence labels** (for psychology/perception claims):
  - **[STRONG]**: replicated experimental research or formal standards.
  - **[MODERATE]**: some peer-reviewed support, small samples, or boundary conditions.
  - **[INDUSTRY]**: a platform or vendor's own data or guidance. It is authoritative for that platform but often self-interested and unreplicated.
  - **[FOLK]**: craft convention or practitioner wisdom. It's useful as a default but has no controlled evidence behind it.
  - **[MYTH]**: widely repeated, and the evidence contradicts it.
- Pixel values assume **1920x1080 (16:9)** or **1080x1920 (9:16)** unless stated. For 4K (3840x2160), multiply px by 2. Express sizes in % of frame height (`%H`) when you can, so they scale.

---

## 0. Ten-line cheat sheet (apply by default)

1. Body/caption text: **≥ 4.5%H on 16:9** (≈ 48px at 1080p); **≥ 6%H** if the main audience watches on phones. Burned-in Shorts captions: **≥ 60px at 1080 wide**, typically 64-90px bold.
2. Caption limits: **≤ 42 chars/line, ≤ 2 lines** for 16:9. For 9:16: **≤ 20 chars/line, 1-2 lines, 1-5 words per chunk**. Reading speed: **≤ 17 cps** comfortable, **20 cps** hard ceiling.
3. Graphics safe area on 16:9: **5% inset** (96px left/right, 54px top/bottom at 1080p). On 9:16, keep everything in **x 80-900, y 250-1440** (the "universal" rectangle).
4. Text on footage must have a **luminance** separation device: a 2-4px stroke, or a soft shadow (0 2px 8-12px at 60-70% black), or a scrim (bottom 35% gradient to 70% black). Never rely on hue alone, because 4:2:0 chroma subsampling smears it.
5. **Max 2 typefaces** (one display, one text/mono) and **max 3 weights** in one video. Use **one accent color**.
6. Motion durations: small UI-scale **150-250ms**; medium moves **300-450ms**; full-frame transitions **450-700ms**. Exits run **~15-25% faster** than entrances.
7. Default ease-in for entrances: `cubic-bezier(0.05, 0.7, 0.1, 1)` (M3 emphasized decelerate). For exits: `cubic-bezier(0.3, 0, 0.8, 0.15)`. For on-screen moves: `cubic-bezier(0.2, 0, 0, 1)`.
8. **One hero moves at a time.** Stagger groups at **40-80ms per item**, and keep the total stagger **≤ 600ms**.
9. Loudness: deliver **-14 LUFS integrated, ≤ -1 dBTP** for YouTube, Shorts, Reels and TikTok. Keep the music bed **≥ 10-15 LU below the voice** while someone is speaking.
10. Never flash more than **3 times per second** (WCAG 2.3.1). Avoid full-frame saturated red flashes entirely.

---

## 1. Typography for Video & Motion

### 1.1 Minimum on-screen text size

The physics behind this: reading is fluent when the **x-height subtends about 0.2° to 2°** of visual angle (Legge & Bigelow 2011) **[STRONG]**. Below about 0.2°, reading speed collapses. A 16:9 video watched on a portrait phone is only about 3.9cm tall. At 35cm viewing distance, 0.2° is about 1.2mm, which is ~31% of the frame height. So small text in long-form is unreadable on phones unless the viewer rotates to landscape.

| Context | Minimum font size (cap-to-descender em) | Comfortable | Notes |
|---|---|---|---|
| 16:9 viewed on TV/desktop | 3.5%H (38px @1080) | 4.5-6%H (48-65px) | Labels and lower thirds for secondary info |
| 16:9 long-form, mixed devices (YouTube default) | **4.5%H (48px)** | 5.5-7%H (60-75px) | ~63% of YouTube watch time is mobile (YouTube statements); design for landscape phone |
| 16:9 subtitle/caption line | BBC: **line height 7-8% of active height** (≈ 76-86px line → ~64-72px font at 120% leading) | same | SRC: BBC-SUB |
| 9:16 Shorts/Reels/TikTok captions | BBC: **line height 3.9-4.5% of height** (≈ 75-86px → ~62-72px font) | 70-100px bold for "viral" style | SRC: BBC-SUB |
| 9:16 headline / hook text | 5-7% of height (96-135px) | | Fit ≤ 3 lines of ≤ 14 chars |
| Absolute floor anywhere | **28px @1080** (2.6%H) | n/a | Below this, 4:2:0 compression and phone downscaling destroy the glyphs |

- **RULE:** at 4K, use the same %H; don't keep the 1080 px values. **WHY:** viewers see relative size, not pixels.
- **RULE:** text that **must** be read gets ≥ 4.5%H. Decorative or "spot readable" text (sources, timestamps) may go down to 2.6%H. **WHY:** this mirrors the APCA split between fluent-read and spot-read text. SRC: APCA.

### 1.2 Reading speed and on-screen duration

| Spec | Value | Evidence | SRC |
|---|---|---|---|
| Netflix English adult | **≤ 20 characters/second** | [INDUSTRY] | NETFLIX-TTSG |
| Netflix children's | **≤ 17 cps** | [INDUSTRY] | NETFLIX-TTSG |
| BBC | **160-180 words/minute**; min duration ≈ **0.3s per word** (4 words → 1.2s) | [INDUSTRY] | BBC-SUB |
| Eye-tracking research | Viewers *can* keep up at 12, 16 and 20 cps. Slow subtitles cause re-reading and **less** enjoyment | [MODERATE] (n=74) | SZARKOWSKA-2018 |
| Average adult silent reading (paper/screen, not video) | 238 wpm non-fiction (range 175-300) | [STRONG] meta-analysis of 190 studies | BRYSBAERT-2019 |
| TikTok ads guidance | "5-10 words per second" of text | [INDUSTRY], and it conflicts with reading research: 5 wps is 300 wpm. Treat it as the upper bound for *1-3-word punch text only* | TIKTOK-CBP |

RULES:
- **On-screen text display time (s) = max(1.0, words × 0.3) + 0.3s** of hold after the animate-in finishes. **WHY:** BBC's 0.3s/word plus a settle buffer.
- **Captions synced to speech:** follow the speech, but keep ≤ 20 cps. If the speaker is faster (> 180 wpm), condense the wording; don't flash 4 frames of text.
- **Text competing with narration** (callouts the viewer must read while also listening): **≤ 12-15 cps, ≤ 7 words per card**. **WHY:** reading and listening share verbal working memory, so split attention means less comprehension (Mayer redundancy, §5.6).
- **Minimum caption event:** 0.8s (≈ 24 frames at 30fps). **Gap between events:** ≥ 2 frames, or butt them directly. A 1-frame gap reads as flicker.
- **Shot changes:** BBC says start/end subtitles on the shot change where possible and avoid straddling a cut. If a caption straddles one, let it extend ≥ 12 frames past the cut. Don't end 1-5 frames after a cut (it looks like an error). SRC: BBC-SUB.

### 1.3 Line length

| Context | Chars per line | Lines |
|---|---|---|
| Netflix 16:9 subtitles | **42** | 2 max |
| BBC broadcast | **37** (BBC online: 68% of frame width for 16:9) | 2 max (3 for 9:16) |
| BBC 9:16 vertical | **90% of width** | **3 max** |
| Burned-in Shorts captions (craft) [FOLK] | **8-20** (1-5 words) | 1-2 |
| Body text in a motion graphic (explainer card) | 30-50 chars | ≤ 4 lines |
| Print/web body (Butterick) | 45-90 | n/a |

- **RULE:** break lines at linguistic boundaries (after punctuation, before conjunctions or prepositions). Never split an article from its noun or a name across lines. When two lines are uneven, prefer a **bottom-heavy pyramid**. SRC: BBC-SUB, NETFLIX-TTSG.

### 1.4 Safe areas

**16:9 broadcast/YouTube (SMPTE ST 2046-1 = EBU R95):**

| Area | Inset per side | 1920x1080 inset | Rect |
|---|---|---|---|
| Action safe | 3.5% | 67px H, 38px V | 1786x1004 |
| Graphics/title safe | **5%** | **96px H, 54px V** | 1728x972 |
| Legacy 4:3 title safe (old SD) | 10% | n/a | Only for 4:3 center-cut protection |

- **RULE:** put all text and logos inside the 5% title-safe area. **WHY:** it's the broadcast standard, and it also clears rounded phone corners and the YouTube player chrome. SRC: EBU-R95, SMPTE-2046.
- **RULE (YouTube long-form):** keep the **bottom 12%** (≈ 130px) free of critical text. **WHY:** the progress bar and controls cover it on hover/pause, and auto-captions render there. [FOLK, observed]
- **RULE:** place lower-thirds with the baseline at **~80-85%H**, left-aligned to the title-safe edge.

**9:16 platform UI overlays.** Measured from 1080x1920. **None of the platforms publish official organic pixel specs.** These are consolidated third-party measurements [FOLK/measured], and sources disagree by ±100px:

| Platform | Top unsafe | Bottom unsafe | Right unsafe | Left unsafe | Notes |
|---|---|---|---|---|---|
| TikTok | 130-260px (tabs, search) | **370-480px** organic; up to ~700px in ads | **120-190px** (like/comment/share rail); up to ~240px in ads | 40-60px | Caption length expands the bottom zone |
| Instagram Reels | 110-270px | **320-480px** (caption, audio, CTA) | 120-140px | 60px | Meta specifies ad safe zones as percentages (~14% top, ~35% bottom for Stories/Reels ads) |
| YouTube Shorts | ~120px | **300-400px** (title, channel, expanded description) | ~96-150px | ~48px | Expanded description grows the bottom zone |

- **RULE: "universal 9:16 safe rectangle" = x 80-900, y 250-1440** (820x1190). Everything that must be read goes in here. **WHY:** it's the intersection of the most conservative measurements across the three platforms.
- **RULE:** put Shorts captions with their **center at y ≈ 1050-1300** (55-68% of height). That's below the face and above the UI. Keep the speaker's eyes at **y ≈ 600-760** (upper third).
- **RULE:** for ads, re-check the platform's current downloadable overlay template. Ad UI is larger than organic UI.

### 1.5 Font pairing, weight, tracking, leading

| Topic | RULE | WHY | SRC |
|---|---|---|---|
| Number of families | **≤ 2** per video (display + text). A mono may be a 3rd *only* for code or data | Each family adds a "voice". Mixing 3+ reads as amateur | BUTTERICK |
| Pairing logic | Contrast **one** axis (serif vs. sans, *or* width, *or* weight) and match **x-height and proportions** | Too-similar pairs look like a mistake; too-different pairs clash | BUTTERICK, GOOGLE-FONTS-KNOWLEDGE |
| Weight contrast | Headline vs. body weight differs by **≥ 300 units** (e.g. 800 vs. 400 or 700 vs. 400). Avoid 500 vs. 600 | Hierarchy must survive a 0.5s glance and compression | [FOLK] |
| Weights per video | **≤ 3** (e.g. 400, 600, 800) | Consistency | [FOLK] |
| All-caps tracking | **+5% to +12%** of font size (CSS `letter-spacing: 0.05em-0.12em`). Use the higher end for small sizes | Caps are spaced for mixing with lowercase; set alone, they're too tight | BUTTERICK |
| Large display tracking | **-1% to -3%** (`-0.01em` to `-0.03em`) above ~100px for grotesks | Default spacing is tuned for text sizes; it looks loose when large | [FOLK]; Inter's dynamic metrics follow this |
| Body/caption leading | **120-145%** (Butterick); BBC uses **120%** for subtitles | Readability | BUTTERICK, BBC-SUB |
| Display leading | **0.9-1.1** (90-110%) for 2-3 line headlines. Use 1.0-1.15 if the font has tall ascenders or diacritics | Tight leading groups the lines visually | [FOLK] |
| Optical sizes | Use the `opsz` axis when it exists (Inter, Roboto Flex, Fraunces, Newsreader, Source Serif 4, DM Sans, Bricolage Grotesque). Set `font-optical-sizing: auto`, or force opsz ≈ 32-72 for display | Display cuts have tighter spacing and finer detail; text cuts are sturdier at small sizes | GOOGLE-FONTS-KNOWLEDGE |
| Case | Captions in sentence case by default. Use ALL CAPS only for ≤ 4-word punch text | All-caps slows reading of longer strings (word-shape loss) [MODERATE] | BUTTERICK |

### 1.6 Legibility on phones and after compression

- **Why geometric/grotesque sans (Inter, Manrope, Montserrat-class) read well on mobile video:** they have large x-heights (≥ 0.52 em), open apertures, uniform stroke weight with no hairlines to lose, and simple shapes that survive 4:2:0 chroma subsampling and macroblocking. [MODERATE]: aperture and x-height effects on small-size legibility are well documented in typeface legibility research (e.g. Legge & Bigelow 2011; Beier's legibility work). The "rounded fonts feel friendly" association is [FOLK].
- **RULE: thin weights.** No weight < 400 below 60px at 1080p. No weight < 300 at any size unless it's ≥ 120px and on a flat, non-moving background. **WHY:** strokes < 2px are below the 4:2:0 chroma resolution (chroma is half-res, so effectively 2px blocks). They shimmer as the encoder re-quantizes them each frame.
- **RULE: stroke width floor.** Minimum stem width ≈ **3px at 1080p** (6px at 4K) for anything that must be read.
- **RULE: hairline serifs.** Didone (Bodoni, Playfair Display) hairlines break below ~72px at 1080p. Use them for ≥ 90px headlines only.
- **RULE: color text.** Saturated red, blue or magenta text **on** a saturated contrasting hue smears because chroma is half-resolution. Text needs a **luminance difference**: WCAG ≥ 4.5:1, or APCA |Lc| ≥ 60, and Lc ≥ 75 for captions. SRC: YT-ENC (4:2:0), APCA.

### 1.7 Text over footage (values that survive YouTube re-encoding)

YouTube re-encodes everything (VP9/AV1, 4:2:0, 8-bit SDR BT.709). The recommended upload is 8 Mbps at 1080p SDR, but delivery bitrates are far lower. SRC: YT-ENC.

| Technique | 1080p values | 4K values | When |
|---|---|---|---|
| **Outline/stroke** | 2-4px (≈ 3-6% of font size), black at 85-100% opacity. Use `paint-order: stroke fill` so the stroke doesn't eat the glyph | 4-8px | Busy footage, viral captions |
| **Soft drop shadow** | `0 2px 10px rgba(0,0,0,.65)` + `0 0 2px rgba(0,0,0,.6)` (a tight contact shadow plus a wide halo) | double the px | Default for clean, premium looks |
| **Hard offset shadow** | 4-6px offset, 0 blur, 100% black or brand dark | 8-12px | Bold/playful styles |
| **Scrim (gradient)** | Bottom 30-40% of frame: `linear-gradient(to top, rgba(0,0,0,.70) 0%, rgba(0,0,0,0) 100%)`. Top scrims: 20-25% at ≤ 55% | same % | Lower-thirds, documentary |
| **Box/plate** | Background rgba(0,0,0,0.6-0.8), padding 0.25em vertical × 0.5em horizontal, radius 0-0.2em | same em | Accessibility-grade captions (BBC/Netflix style) |
| **Local blur** | `backdrop-filter: blur(16-24px)` + 30-40% dark tint | 32-48px | Sparingly. Glass is an AI-slop tell when overused (§7) |

- **RULE:** don't use stroke widths < 2px at 1080p. **WHY:** the encoder blurs them into a gray halo.
- **RULE:** avoid 1px lines, fine textures, and single-pixel dividers in motion. Use ≥ 2px. **WHY:** they twinkle (temporal aliasing) as they move across macroblocks.
- **RULE:** for moving text, round the final resting positions to whole pixels and avoid sub-pixel "settle" drift. **WHY:** it prevents shimmer.

---

## 2. Curated Font Library for Video (48 fonts)

Licenses:

- **OFL** = SIL Open Font License, via Google Fonts. Free for commercial use, embedding and redistribution (not for sale on its own).
- **FFL** = ITF Free Font License, via Fontshare. Free for personal and commercial use, including broadcast. **No redistribution**: don't commit the files into a public skill repo. Download them from fontshare.com at setup instead, and verify the current terms before shipping. SRC: FONTSHARE.
- **RULE for the skill:** bundle OFL fonts. Fetch FFL fonts at runtime from Fontshare's API/CDN.

Weight notation: the recommended weights to load (others are optional).

### 2.1 Premium / Editorial
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| Instrument Serif | Google/OFL | 400, 400 italic | Inter or Instrument Sans | Condensed editorial serif. Display only (≥ 72px) |
| Fraunces | Google/OFL (opsz, SOFT, WONK) | 300-700 | Inter / Manrope | Use opsz 72-144 for display; "wonky" adds character |
| Newsreader | Google/OFL (opsz) | 400, 600 | Inter | Serious, journalistic |
| Playfair Display | Google/OFL | 600-800 | Source Sans 3 / Inter | Didone, ≥ 90px only. Overused, so use with restraint |
| DM Serif Display | Google/OFL | 400 | DM Sans | High contrast, warm |
| Gambetta | Fontshare/FFL | 400-700 | Satoshi | Modern editorial serif |
| Zodiak | Fontshare/FFL | 400-800 | General Sans | Expressive serif with display cuts |
| Source Serif 4 | Google/OFL (opsz) | 400, 600 | Source Sans 3 | Sturdy at small sizes |

### 2.2 Tech / Product / SaaS
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| Inter (v4, opsz) | Google/OFL | 400, 600, 800 | JetBrains Mono / Fraunces | Workhorse with a large x-height. Default for UI recreations |
| Geist | Google/OFL (Vercel) | 400, 600, 700 | Geist Mono | Crisp, contemporary dev-tool feel |
| Manrope | Google/OFL | 400, 700, 800 | IBM Plex Mono | Geometric-grotesk hybrid, very mobile-legible |
| Space Grotesk | Google/OFL | 400, 700 | Space Mono | Quirky tech. Overused in AI/crypto, so be careful |
| Satoshi | Fontshare/FFL | 400, 700, 900 | Gambetta / JetBrains Mono | Premium startup look |
| General Sans | Fontshare/FFL | 400, 600 | Zodiak | Neutral, modern |
| Switzer | Fontshare/FFL | 400-800 | Erode | Swiss-neutral, Helvetica alternative |
| IBM Plex Sans | Google/OFL | 400, 600 | IBM Plex Mono / Plex Serif | Corporate-technical, superfamily |

### 2.3 Friendly / Approachable / Education
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| DM Sans (opsz) | Google/OFL | 400, 700 | DM Serif Display | Soft geometric |
| Plus Jakarta Sans | Google/OFL | 500, 800 | Fraunces | Warm, rounded terminals |
| Nunito | Google/OFL | 600, 800 | Nunito Sans | Rounded terminals. Kids/edu |
| Figtree | Google/OFL | 500, 700 | Newsreader | Clean, friendly, highly legible |
| Outfit | Google/OFL | 400, 700 | Inter | Geometric, simple |
| Rubik | Google/OFL | 500, 800 | Rubik only | Slightly rounded corners. Works for numbers and data |

### 2.4 Bold / Viral captions (Shorts, Reels, TikTok)
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| Montserrat | Google/OFL | 800, 900 | Inter | The "Hormozi-style" caption default. Overused, so differentiate with color and animation |
| Poppins | Google/OFL | 700, 800 | n/a | Geometric, round dots |
| Anton | Google/OFL | 400 | Inter | Condensed impact-style, all-caps hooks |
| Bebas Neue | Google/OFL | 400 | Montserrat 500 | Caps-only. Track +4-6% |
| Archivo / Archivo Black | Google/OFL (wdth axis) | 800-900, wdth 100-125 | Archivo 400 | Width axis is great for kinetic type |
| Lilita One | Google/OFL | 400 | Nunito | Chunky, playful-bold |
| Clash Display | Fontshare/FFL | 600, 700 | Satoshi | Premium-bold hooks |
| Cabinet Grotesk | Fontshare/FFL | 800, 900 | Satoshi | Punchy, quirky grotesk |
| Tanker | Fontshare/FFL | 400 | General Sans | Ultra-heavy condensed display |

### 2.5 Documentary / Journalistic / Serious
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| Barlow Condensed | Google/OFL | 500, 700 | Barlow | Lower-thirds, data labels |
| Oswald | Google/OFL | 500, 700 | Source Serif 4 | Classic doc titles |
| Big Shoulders Display | Google/OFL | 700, 900 | Inter | Industrial, Chicago-signage feel |
| Libre Franklin | Google/OFL | 400, 700 | Libre Caslon | Newspaper sans |
| Libre Caslon Text/Display | Google/OFL | 400, 700 | Libre Franklin | Historical, literary |
| Familjen Grotesk | Google/OFL | 400, 700 | Newsreader | Contemporary documentary grotesk |

### 2.6 Luxury / Fashion
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| Cormorant Garamond | Google/OFL | 500, 600 | Inter 300 tracked caps | Display ≥ 80px only (fine hairlines) |
| Bodoni Moda (opsz) | Google/OFL | 500-700 | Jost | Use opsz high for display |
| Jost | Google/OFL | 300, 400 caps | Bodoni Moda | Futura-like. Wide-tracked caps (+15-20%) |
| Boska | Fontshare/FFL | 400-700 | Switzer | Contemporary high-contrast serif |
| Melodrama | Fontshare/FFL | 400-600 | General Sans | Dramatic Didone-ish display |

### 2.7 Playful / Creator / Handmade
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| Fredoka | Google/OFL | 500, 700 | Nunito | Rounded, bubbly |
| Baloo 2 | Google/OFL | 600, 800 | Nunito | Rounded, multilingual (Indic) |
| Bricolage Grotesque (opsz, wdth) | Google/OFL | 500, 800 | Inter | Quirky ink-trap display. Trendy |
| Unbounded | Google/OFL | 600, 900 | Inter | Wide, Y2K-ish |
| Chillax | Fontshare/FFL | 500, 700 | Satoshi | Soft, playful geometric |
| Caveat | Google/OFL | 600 | Inter | Handwritten annotations/arrows only. Never body text |
| Permanent Marker | Google/OFL | 400 | Inter | Marker callouts, sparingly |

### 2.8 Code / Data / Mono
| Font | Source/License | Weights | Pair with | Notes |
|---|---|---|---|---|
| JetBrains Mono | Google/OFL | 400, 700 | Inter | Best mono for code-on-screen, with ligatures |
| Geist Mono | Google/OFL | 400, 600 | Geist | |
| IBM Plex Mono | Google/OFL | 400, 600 | IBM Plex Sans | |
| Space Mono | Google/OFL | 400, 700 | Space Grotesk | Retro-tech |
| Fira Code | Google/OFL | 400, 600 | Fira Sans | Ligatures |

- **RULE:** use **tabular numerals** (`font-variant-numeric: tabular-nums`) for any animated counters, timers or price tickers. **WHY:** proportional digits make the number jitter sideways while counting.
- **RULE:** when a creator has no brand fonts, default to **Inter + JetBrains Mono** (tech), **Fraunces + Inter** (premium), or **Montserrat 800 + Inter** (viral). Rotate the choice to avoid sameness across a channel's videos only if the brief asks for it. Consistency within a channel beats novelty.

---

## 3. Color

### 3.1 Color psychology: honest evidence ratings

| Claim | Rating | Use it as |
|---|---|---|
| Color/luminance **contrast and salience** drive attention: a unique color among neutrals "pops out" pre-attentively | **[STRONG]** (visual search research; Treisman feature integration) | The basis for one-accent discipline |
| Specific hue → specific emotion ("blue = trust", "red = urgency/appetite") | **[FOLK]/[MODERATE at best]**: effects are small, context-dependent and culturally variable | Brand convention, not a law |
| "Red impairs achievement/test performance" (Elliot et al. 2007) | **[MYTH-ish]**: repeated failed replications (Gnambs 2020 and others), and a 2020 *Psychonomic Bulletin & Review* review casts doubt | Don't cite it |
| Red increases perceived attractiveness or dominance | **[MODERATE→WEAK]**: mixed replications | Don't rely on it |
| Warm, saturated colors raise arousal; desaturated/cool feels calmer | **[MODERATE]** | Mood grading, music-video energy |
| Color meaning is culture-dependent (white = mourning in parts of East Asia; red = luck in China) | **[STRONG]** | Localization check |
| Elliot & Maier's (2014) color-in-context theory | Theory review [MODERATE]. Note its own predictions have replicated poorly | Background reading |

SRC: ELLIOT-MAIER-2014, GNAMBS-2020, PBR-2020-COLOR.

### 3.2 Contrast requirements

| Standard | Requirement | SRC |
|---|---|---|
| WCAG 2.x AA, normal text | **4.5:1** | WCAG |
| WCAG 2.x AA, large text (≥ 24px regular / ≥ 18.66px bold, CSS px) | **3:1** | WCAG |
| WCAG 2.x AAA | 7:1 (normal), 4.5:1 (large) | WCAG |
| WCAG non-text (icons, chart strokes) | **3:1** | WCAG 1.4.11 |
| APCA **Lc 90** | Preferred for body/fluent reading | APCA |
| APCA **Lc 75** | Minimum for body text (e.g. ≥ 18px/400, 16px/500, 14px/700). **Use as the caption minimum** | APCA |
| APCA **Lc 60** | Minimum for "content text you want read" (≥ 24px/400 or 16px/700) | APCA |
| APCA **Lc 45** | Minimum for large/heavy headlines (≥ 36px/400 or 24px/700) and fine icons | APCA |
| APCA **Lc 30** | Absolute minimum for spot-read text and solid icons | APCA |
| APCA **Lc 15** | Below this, treat the element as invisible | APCA |

- **RULE:** check text contrast **against the actual pixels behind it** (sample a 3x3 region at each glyph's position over the clip's duration), not against an assumed background. If any frame fails, add a stroke, shadow or scrim (§1.7).
- **RULE:** APCA is better suited than WCAG 2 contrast ratios for light-on-dark text, which is common in video. Use APCA Lc for dark-mode/dark-footage text, and WCAG 4.5:1 as the legal floor.

### 3.3 Palette discipline

- **60-30-10 rule:** 60% dominant (background/neutral), 30% secondary (surfaces, footage), 10% accent. **[FOLK]**: it comes from interior design and has no experimental basis, but it's a good default that enforces hierarchy.
- **RULE: one accent.** Exactly **one** saturated accent hue per video. It marks "the important thing" (keyword highlight, the active chart bar, CTA). A second accent is allowed only for semantic pairs (good/bad, before/after). **WHY:** pop-out works only when the accent is rare [STRONG].
- **RULE: accent coverage ≤ 10%** of the frame area at any moment.
- **RULE: neutrals aren't pure.** Use tinted near-blacks (e.g. `#0E0F12`) and near-whites (`#F5F3EE`) rather than #000/#FFF for graphics plates. Pure #FFFFFF text is fine for captions (it's what Netflix and BBC use).
- **RULE: building palettes from footage.**
  1. Sample 5-8 keyframes, run k-means (k=5) in OKLab, and drop clusters < 3% area.
  2. The dominant scene hue becomes the base neutral tint.
  3. Pick the accent by rotating **150-210° in OKLCH hue** (complementary) from the dominant hue, *or* use the brand color.
  4. **Keep the accent hue at least 25-30° away from the skin-tone hue (~ 20-50° in OKLCH/HSL orange)**, so highlights don't blend with faces.
  5. Set accent lightness so APCA vs. the background is ≥ Lc 60.
- **RULE:** use **OKLCH/OKLab** for interpolation and gradient stops, not sRGB. **WHY:** sRGB midpoints go muddy or gray (e.g. blue→yellow passes through gray).

### 3.4 Color grading basics for talking heads

- **Skin tone line:** on a vectorscope, skin of all ethnicities clusters along one hue line (~10-11 o'clock, between red and yellow, often cited as ~123° on the scope). Ethnicity differs mostly in **saturation and luminance**, not hue. **RULE:** isolate skin and put its hue on the line ±5°. Deliberately stylized warm/cool looks may deviate. **[STRONG]** as a craft standard. SRC: ADOBE-SKIN, VAN-HURKMAN via JORDAN.
- **Exposure targets (Rec.709, 0-100 IRE) [FOLK/craft]:** lighter skin highlights at ~60-70 IRE, medium ~45-60, deep ~35-50. Specular highlights ≤ 95-100 (no clipped faces). Blacks 0-5 IRE, without crushing hair detail. Keep the face as the brightest *large* area in the frame. **WHY:** the eye goes to the brightest, highest-contrast region (and to faces, §5.9).
- **Order of operations:** (1) normalize: white balance plus exposure, (2) apply the input transform (log→Rec.709), (3) creative look, (4) secondary skin protect, (5) final output transform. **RULE:** never apply a creative LUT to footage of a different gamma than the LUT expects (e.g. an S-Log3 LUT on Rec.709). **RULE:** run creative LUTs at **40-80% opacity/mix** and re-check skin on the vectorscope afterward. **WHY:** LUTs are fixed transforms that clip and shift hue when the input is out of range.
- **Saturation:** keep skin saturation moderate. Over-saturated orange skin is the #1 amateur grading tell. Look for the skin trace extending less than about halfway to the 75% target box on a 75% vectorscope [FOLK].
- **Delivery:** SDR **BT.709**, 4:2:0, progressive, per YouTube's recommended upload settings. SRC: YT-ENC.

### 3.5 Gradients and banding after compression

- **Cause:** 8-bit delivery (256 levels per channel) plus encoder quantization flattens smooth ramps into visible contours. Re-encoding by the platform makes it worse.
- **RULES:**
  1. Render masters in **10-bit or 16-bit float** where possible (ProRes 422 HQ / 10-bit H.265). At minimum, the HTML→frames pipeline should render PNG-16 or float, not 8-bit JPEG.
  2. **Add noise/grain at the very end**, at **1-5% amplitude** (monochromatic, ~1px grain, animated per frame), to dither ramps. **WHY:** noise breaks up the contours. Too little gets quantized away; too much costs bitrate. Test on the *uploaded* video. SRC: PVC-BANDING.
  3. Avoid large, low-contrast, slow gradients (e.g. a full-frame #0B0B12→#151526 ramp). Use **wider luminance spans (≥ 8-10% L difference)**, or add texture.
  4. Dark gradients band worst (YouTube's quantization is coarse in the shadows). Lift deep backgrounds to ≥ ~ L 8-10% (OKLCH), or add grain.
  5. Upload at a higher bitrate than recommended (1080p at 12-16 Mbps, or 4K at 45+ Mbps). 4K uploads get a better codec and bitrate tier on YouTube even for 1080p viewers [FOLK/observed].

---

## 4. Motion Design Principles

### 4.1 Disney's 12 principles → UI and kinetic type

Source: Thomas & Johnston, *The Illusion of Life* (1981). SRC: DISNEY-12.

| Principle | Application to motion graphics / kinetic type | Default numbers |
|---|---|---|
| Squash & stretch | Scale a "landing" word to 1.0→1.06 (Y) / 0.96 (X) for ≤ 80ms on impact. Preserve area | Max ±8% distortion. Use for playful styles only |
| Anticipation | A small counter-move before the main move (e.g. pull back 4-8% of the travel distance, or scale to 0.96) | 60-120ms before the action |
| Staging | One clear idea per frame. Dim or blur everything else. **One hero moves at a time** | Non-hero opacity ≤ 40-60% during the hero move |
| Straight-ahead vs. pose-to-pose | Use pose-to-pose (keyframes) for all UI motion | n/a |
| Follow-through & overlapping action | Child elements (underline, icon, sub-label) arrive 40-100ms after the parent | Offset 40-100ms |
| Slow in / slow out | Never use linear easing for spatial moves (linear is fine for opacity cross-fades, rotation loops, scrolling tickers) | See §4.2 |
| Arcs | Large moves (> 25% of frame) travel on a slight arc, not a straight line | 5-15% path curvature |
| Secondary action | Subtle background drift (parallax 2-5% of frame over the shot) supports the main action | Must not compete in speed |
| Timing | Duration scales with distance and size (§4.3) | n/a |
| Exaggeration | Push key emphasis moments ~10-20% beyond "realistic" (scale pops to 1.1-1.15) | n/a |
| Solid drawing | Keep consistent perspective and light direction (shadows all cast from the same angle) | n/a |
| Appeal | Clean, simple shapes, consistent corner radii, intentional color | n/a |

**Anticipation → action → settle** (the core beat of any emphasis animation):

- Anticipation: 10-20% of total time, moving opposite to the action by 4-8% of the travel.
- Action: 50-70% of total time, with the fast part of a decelerating curve.
- Settle: 20-30% of total time, with an overshoot of 2-10% and back. Use **≤ 1 visible oscillation** for professional work and ≤ 2-3 for playful work.

### 4.2 Easing curves (exact values)

**Material Design 3 tokens** (verified from material-web token source, v0.192). SRC: M3-TOKENS.

| Token | cubic-bezier | Use |
|---|---|---|
| emphasized (CSS approximation; the true M3 emphasized is a 2-segment path) | `(0.2, 0, 0, 1)` | Hero on-screen moves and morphs |
| emphasized-decelerate | `(0.05, 0.7, 0.1, 1)` | **Entrances**: things arriving on screen |
| emphasized-accelerate | `(0.3, 0, 0.8, 0.15)` | **Exits**: things leaving permanently |
| standard | `(0.2, 0, 0, 1)` | Small utility moves |
| standard-decelerate | `(0, 0, 0, 1)` | Small entrances |
| standard-accelerate | `(0.3, 0, 1, 1)` | Small exits |
| legacy (Material 1/2 "standard") | `(0.4, 0, 0.2, 1)` | Neutral ease-in-out |
| legacy-decelerate / accelerate | `(0, 0, 0.2, 1)` / `(0.4, 0, 1, 1)` | n/a |
| M1 "sharp" | `(0.4, 0, 0.6, 1)` | Elements that may return at any time |

**IBM Carbon** (productive = efficient UI, expressive = big moments). SRC: CARBON-MOTION.

| | Productive | Expressive |
|---|---|---|
| Standard | `(0.2, 0, 0.38, 0.9)` | `(0.4, 0.14, 0.3, 1)` |
| Entrance | `(0, 0, 0.38, 0.9)` | `(0, 0, 0.3, 1)` |
| Exit | `(0.2, 0, 1, 0.9)` | `(0.4, 0.14, 1, 1)` |

**Penner-family curves as CSS cubic-beziers** (from easings.net), mapped to GSAP names:

| Name | cubic-bezier | GSAP | Character |
|---|---|---|---|
| easeOutCubic | `(0.33, 1, 0.68, 1)` | `power2.out` | Gentle default out |
| easeOutQuart | `(0.25, 1, 0.5, 1)` | `power3.out` | Confident |
| easeOutQuint | `(0.22, 1, 0.36, 1)` | `power4.out` | Snappy, premium (Apple-like) |
| easeOutExpo | `(0.16, 1, 0.3, 1)` | `expo.out` | Very fast start with a long tail. Great for text reveals |
| easeInOutCubic | `(0.65, 0, 0.35, 1)` | `power2.inOut` | Camera moves, morphs |
| easeInOutQuart | `(0.76, 0, 0.24, 1)` | `power3.inOut` | Dramatic transitions |
| easeOutBack | `(0.34, 1.56, 0.64, 1)` | `back.out(1.7)` | **~10% overshoot** (Penner's s = 1.70158 gives a 10% overshoot) |
| easeInBack | `(0.36, 0, 0.66, -0.56)` | `back.in(1.7)` | Anticipation pull-back on exit |

**Apple / spring physics.** SRC: APPLE-SPRING, WWDC23-SPRINGS.

- SwiftUI `.spring()` legacy defaults: **response 0.5s, dampingFraction 0.825**, blendDuration 0. Verified in Apple docs.
- Modern API: `Spring(duration:, bounce:)`. Presets `.smooth` (no bounce), `.snappy` (small bounce) and `.bouncy` (higher bounce). Commonly reported values are duration 0.5 and bounce 0 / 0.15 / 0.3. Apple's docs describe them only qualitatively, so treat the numbers as approximate.
- **Conversion to physics (mass = 1):** stiffness k = (2π / duration)², damping c = 4π(1 − bounce) / duration, so the damping ratio ζ = 1 − bounce.
- **Overshoot from damping ratio:** overshoot = exp(−πζ / √(1−ζ²)).
  - ζ 0.825 (default) → **~1%** overshoot (barely visible, "Apple feel")
  - bounce 0.15 (ζ 0.85) → ~0.6%
  - bounce 0.3 (ζ 0.7) → **~4.6%**
  - ζ 0.5 → ~16% (cartoony)
- GSAP has no native spring. Use `CustomEase`/`CustomWiggle`, precompute a spring curve into a `CustomEase` path, or use `elastic.out(1, 0.3-0.5)` (heavier oscillation; playful only).

**RULES:**
- Entrances use **decelerate** curves (they arrive fast and settle). Exits use **accelerate** curves (they start slow and leave fast). On-screen moves use **ease-in-out/standard**. **WHY:** this mimics physical objects entering or leaving the viewer's space (M1/M3 guidance).
- **Overshoot budget:** professional/corporate 0-3%. Creator/energetic 5-10%. Playful/kids 10-20%. Never overshoot body text or captions by more than 5%, because it hurts readability during the settle.
- Don't mix more than **2-3 easing families** in one video. Consistency is what makes motion read as "designed".

### 4.3 Durations

| Source | Values |
|---|---|
| M3 tokens | short1-4 = **50/100/150/200ms**; medium1-4 = **250/300/350/400ms**; long1-4 = **450/500/550/600ms**; extra-long1-4 = **700/800/900/1000ms** |
| Carbon | fast-01 **70ms** (micro), fast-02 **110ms** (fade), moderate-01 **150ms** (small, short distance), moderate-02 **240ms** (expansion, toast), slow-01 **400ms** (large expansion), slow-02 **700ms** (background dimming) |
| Material 1 (mobile) | **300ms** typical; **entering 225ms, exiting 195ms**; tablet **+30%** (390ms); wearable −30%; desktop **150-200ms** |
| NN/g | Most UI animation **100-500ms**; simple feedback ~100ms; modal/large change 200-300ms; "at 500ms they start to feel like a drag" *in interactive UI* |

**Video context differs from UI.** The viewer isn't waiting on an interaction; they need time to *notice and read*. Use these defaults for rendered video:

| Element | Enter | Hold (readable) | Exit |
|---|---|---|---|
| Caption word pop (Shorts) | 80-150ms | synced to speech | 0-100ms (cut or fast fade) |
| Keyword highlight / underline draw | 200-350ms | n/a | 150-250ms |
| Lower-third | 400-600ms (staggered parts) | ≥ 3-5s | 300-400ms |
| Title card / hook text | 300-500ms | words × 0.3s + 0.5s, minimum 1.2s | 200-350ms |
| Icon/stat callout | 250-400ms | ≥ 1.5s | 200ms |
| Chart bars/lines growing | 600-1200ms (data growth is the content) | ≥ 2s after completion | 300ms |
| Full-frame transition (wipe, zoom, push) | **300-600ms** total (8-18 frames at 30fps) | n/a | n/a |
| Camera move (scale/pan on still or graphic) | entire shot (3-8s), with a gentle ease-in-out | n/a | n/a |

**RULES:**
- **Duration ∝ distance:** ≈ 200ms + 100ms per 25% of frame-width traveled, capped at ~700ms for non-camera moves. **WHY:** perceived speed must stay constant across move sizes (M1: longer for larger distances and surface changes).
- **Exits = 75-85% of the entrance duration.** **WHY:** leaving elements need less attention (M1, M3).
- **Quantize durations to whole frames** of the output fps. At 30fps, 1 frame = 33.3ms, so 300ms = 9 frames. At 24fps, 1 frame = 41.7ms.

### 4.4 Stagger, choreography, hierarchy

- **Stagger per item:** **40-80ms** for lists of 3-7 items, **20-40ms** for letter-by-letter (cap the total sequence at ~600-800ms). Word-by-word kinetic type synced to VO uses the **speech timestamps**, not a fixed stagger. [FOLK/industry practice; Material's choreography docs recommend a consistent "lead" element then followers.]
- **Total stagger window ≤ 600ms** for UI-like groups. If a list exceeds this, stagger the first 5 items and then group the rest.
- **Motion hierarchy:** exactly **one hero motion** at a time. Secondary motions are ≤ 50% of the hero's travel distance and start ≥ 60-100ms later. Ambient motion (background drift, particles) stays slower than **~2-5% of frame size per second**. **WHY:** motion is the strongest exogenous attention cue in video [STRONG: attentional synchrony research], so competing motions split gaze.
- **Direction consistency:** "forward/next" moves **right-to-left or bottom-to-top** consistently. Back/previous reverses it. Enter and exit along the same axis.
- **Shared-element continuity:** when an element persists across a scene change, morph it (position/scale) instead of cutting it out and back in. **WHY:** object constancy reduces re-orientation load.

### 4.5 Frame rate and motion blur

| Topic | RULE | WHY |
|---|---|---|
| Match the source | Render graphics at the **project fps** (24/25/30, or 50/60 for gameplay/screen recordings). Never deliver 24fps footage in a 30fps timeline with 3:2 judder unless unavoidable | Mixed cadences judder |
| Talking-head YouTube | 24 or 30fps. 30 is safest for screen-recorded tech content; 60 for gameplay | YouTube supports 24-60 (YT-ENC) |
| Shutter / motion blur | Natural-looking blur = **180° shutter** (blur length = half the per-frame displacement; exposure 1/48s at 24fps, 1/60s at 30fps) | Matches how film audiences perceive motion |
| HTML/GSAP rendering | Rendered frames have **zero motion blur** by default, which makes fast moves strobe. For moves > ~2-3% of frame width per frame, either (a) render 4-8 subframes per frame and average them (accumulation blur; mimic a 180° shutter by averaging the first half of the subframes), or (b) add a directional CSS blur proportional to velocity | Removes strobing on fast whip transitions and text slams |
| Fast pans at 24fps | An object should take **≥ ~5-7s to cross the frame** for a smooth pan at 24fps/180° (RED "7-second rule" craft guidance) [FOLK/craft] | Otherwise it judders |
| Minimum readable motion | Text is unreadable while moving faster than **~10-15% of frame width per second**. Animate in, then **hold still** to read | Reading needs fixations (≈ 200-250ms each) |
| Flash safety | **≤ 3 flashes per second** and no saturated-red flashes (WCAG 2.3.1; broadcast uses ITU-R BT.1702 / the Harding test). Avoid full-frame white-flash transitions in rapid succession | Photosensitive seizure risk |

---

## 5. Editing Grammar & Attention Psychology

### 5.1 Walter Murch's Rule of Six (*In the Blink of an Eye*, 1995/2001)

When choosing a cut point, weigh the criteria in this order. **When you can't satisfy them all, sacrifice from the bottom up.** SRC: MURCH.

| Criterion | Weight |
|---|---|
| Emotion: is the cut true to the emotion of the moment? | **51%** |
| Story: does it advance the story? | **23%** |
| Rhythm: is it at a rhythmically right moment? | **10%** |
| Eye-trace: does it respect where the viewer's eye is looking? | **7%** |
| 2D plane of screen: 180° rule, screen direction | **5%** |
| 3D space: continuity of physical position | **4%** |

- Rating: **[FOLK]**, from a master editor. The percentages are rhetorical, not measured, but the priority order is near-universal practice.
- **Murch's blink theory:** a cut works like a blink, and viewers' blinks cluster at points of "thought completion". **RULE:** cut at the *end of a thought or clause*, not mid-word. Rating: [MODERATE]; Nakano et al. (2009) found that blinks synchronize across viewers at implicit breakpoints in video.
- **Eye-trace rule (agent-applicable):** at a cut, the subject of interest in the incoming shot should be within **~10-20% of the frame width** of where the outgoing shot's focus was. **WHY:** it avoids a search saccade, so the cut feels invisible. When you intentionally jolt (a pattern interrupt), break this on purpose.

### 5.2 Cut types and grammar

- **Cut on action:** cut *during* a movement, with the incoming shot continuing it. Overlap 2-4 frames of action for smoothness [FOLK/craft]. **WHY:** motion masks the discontinuity (the cut is less noticeable during movement; "edit blindness" research by Smith & Henderson 2008) **[MODERATE]**.
- **J-cut:** the incoming clip's **audio starts before** its picture, typically **6-24 frames (0.25-1s)**. Use it to lead into a new speaker or scene. **L-cut:** the outgoing **audio continues** over the new picture (B-roll over the VO tail). **RULE:** use J/L cuts on **≥ 50% of scene transitions** in documentary/interview edits. **WHY:** offsetting audio and picture edits hides cuts and creates flow [FOLK/industry standard].
- **Jump cuts (talking head):** remove pauses > 300-500ms and filler. Keep **2-6 frames of breath/room tone** at the head and tail of each phrase so speech doesn't feel clipped. Alternate framing (punch-in **110-125%** scale) on every 2nd-3rd jump cut to mask the jump. Punch-ins above ~130% reveal compression and softness on 1080p sources (on 4K sources ≤ 150% is fine for 1080 delivery).
- **Match cut / graphic match:** align the dominant shape or position across the cut (eye-trace).
- **Smash cut:** use a sudden audio-level change (loud→silence or silence→loud) to sell it.
- **180° rule and screen direction:** keep subjects' screen direction consistent for spatial continuity (Murch weights this low; break it only with motivation).

### 5.3 Shot length and pacing (data)

- Hollywood **average shot length (ASL)** dropped from ~8-10s (1930s-1960s) to **~3-4s by the 2000s**. Shot lengths also became more correlated with neighbors, approaching a **1/f pattern** that resembles human attention fluctuations (Cutting, DeLong & Nothelfer 2010, 150 films 1935-2005). **[STRONG]** for the trend; **[MODERATE]** for the attention interpretation. There was zero correlation of 1/f with IMDb ratings. SRC: CUTTING-2010.
- **RULE: vary shot lengths.** Don't cut on a metronome. Cluster short shots in high-energy passages and let longer shots breathe after reveals. **WHY:** this is what the 1/f structure is (long and short shots in mixed, correlated runs).
- **Platform pacing defaults [FOLK, consistent with platform guidance]:**
  - Shorts/Reels/TikTok: a visual change (cut, zoom, graphic, caption emphasis) every **1.5-3s**.
  - YouTube talking-head long-form: every **3-8s**.
  - Documentary/essay: **4-12s**.
  - Tutorials and screen-recordings: change when the *information* changes. Don't add cuts for their own sake; zoom to the area of interest.
- **"Pattern interrupt every X seconds"** as a retention law: **[FOLK]**. No controlled evidence supports a specific interval. What *is* established:
  - Cuts, onsets of graphics and other structural features trigger **orienting responses**: automatic attention allocation, measurable as heart-rate deceleration (Lang 1990s; Lang & Thorson 1992 found that inserting videographics into talking-head lectures elicits ORs). **[STRONG]**
  - Under Lang's Limited Capacity Model (LC4MP), **too many** structural changes, or *unrelated* cuts, overload capacity and **reduce memory** for the content, especially when the content is complex. **[MODERATE]** (Lang et al. 1993, *Communication Research*).
  - **RULE:** every interrupt must be **semantically related** (B-roll of what's being said, a graphic of the number just spoken). Lower the cut rate during dense explanations; raise it during low-information stretches (transitions, recaps).

### 5.4 Hooks, intros and retention

| Data point | Rating | SRC |
|---|---|---|
| YouTube "Key moments for audience retention" → **Intro** = % of viewers still watching at **0:30**. YouTube suggests checking that the first 30s match the title/thumbnail promise | [INDUSTRY] | YT-KEYMOMENTS |
| YouTube Content analytics lists videos with "above typical" intros. A rule of thumb of **≥ 50-60% still watching at 0:30** is commonly cited but **not an official benchmark** | [FOLK] | YT-KEYMOMENTS, third-party |
| Shorts "Viewed vs. swiped away": % of feed viewers who stayed past the opening seconds. The exact threshold is undisclosed. Third-party "good" benchmarks of ~70%+ viewed are unofficial | [INDUSTRY metric / FOLK benchmark] | YT-SHORTS-METRIC |
| Meta/Nielsen: **up to 47% of video-campaign value (lift) delivered in the first 3s, 74% in the first 10s** (173 Brand Effect studies) | [INDUSTRY]: commissioned, and about *ads* | META-NIELSEN |
| TikTok: introduce the content proposition **in the first 3s**; put the hook **within the first 6s** | [INDUSTRY] | TIKTOK-CBP |
| "Humans have an 8-second attention span, less than a goldfish" | **[MYTH]**: traces to a 2015 Microsoft Canada marketing report citing an unsourced "Statistic Brain" figure. Debunked by BBC *More or Less* (2017). Sustained-attention measures in adults haven't declined | ATTN-MYTH |

**Hook RULES (agent):**
1. **Frame 1 must already be "in motion".** No logo stings, black frames, or "hey guys" before the hook. On Shorts, the first frame must work as a thumbnail (on-screen text is visible at frame 0).
2. **0-3s:** state the payoff or tension (the promise from the title/thumbnail), with a visual change in the first 1s. **3-30s (long-form):** deliver proof of the promise, then open a loop for the rest of the video.
3. **Match the packaging:** the first 30s must visually or verbally confirm the title and thumbnail. YouTube's own guidance ties low intro retention to an expectation mismatch.
4. **Shorts loop:** the last line or frame should flow into the first (seamless loop) to inflate rewatches. [FOLK/industry practice]

### 5.5 Open loops, curiosity gap, Zeigarnik

- **Information-gap theory:** curiosity arises when attention is drawn to a specific gap in knowledge (Loewenstein 1994). Curiosity rises when people feel *partially* informed, and it enhances memory for the answer and even for incidental information (Kang et al. 2009; Gruber et al. 2014). **[STRONG]**
  - **RULE:** pose a specific question, delay the answer by **30s-3 min** (long-form) or **5-20s** (Shorts), and **pay it off** explicitly. Show partial information, like a blurred result or a chart with the last bar hidden. **WHY:** a specific gap creates curiosity; a vague one doesn't.
- **Zeigarnik effect** (better memory for interrupted tasks): a 2025 meta-analysis (Ghibellini & Meier, *Humanities & Social Sciences Communications*) found **no general memory advantage** for unfinished tasks, but did find a reliable **tendency to resume** them (the Ovsiankina effect). **[MYTH as usually stated]**; **[MODERATE]** for the resumption urge.
  - **RULE:** justify open loops by curiosity (Loewenstein), not by "Zeigarnik memory". Unresolved loops that never pay off damage trust and comments.

### 5.6 Cognitive load and Mayer's multimedia principles (critical for explainers)

Cognitive Load Theory (Sweller 1988): working memory is limited, so cut extraneous load. Mayer's principles are **[STRONG]** (dozens of experiments). The effect sizes are median Cohen's d from Mayer's Cambridge Handbook chapters (2014); later reviews report similar ranges. SRC: MAYER-2014, MAYER-2021.

| Principle | Effect (median d) | RULE for the editor |
|---|---|---|
| **Coherence** (cut extraneous words, pictures, sounds) | **0.86** (23/23 tests) | No decorative B-roll, stock footage, background music swells or SFX during dense explanation. Music bed ≥ 15 LU under voice or off |
| **Signaling** (highlight essential material) | **0.41** (24/28) | Highlight the keyword in the accent color, use arrows or circles on the relevant chart part, dim non-relevant areas to ≤ 40% |
| **Redundancy** (graphics + narration beats graphics + narration + identical on-screen text) | **0.86** (16/16) | Don't put the narration sentence on screen as a paragraph next to a diagram. Show **keywords (≤ 5 words)** only. *Boundary conditions:* captions remain useful for sound-off, accessibility and non-native viewers, and redundancy hurts little when on-screen text is short or there are no competing graphics |
| **Spatial contiguity** (words next to the picture they describe) | ~**0.8-1.1** | Put labels **on or next to** the chart element (≤ 5% of frame width away), not in a separate legend |
| **Temporal contiguity** (narration and the corresponding animation at the same time) | ~**1.2-1.3** | The visual appears **on the spoken word** (±150ms), not a sentence earlier or later. Use word timestamps |
| **Segmenting** (learner-paced chunks) | ~**0.7-0.8** | Break explainers into labeled chapters/sections of **≤ 60-120s** with a visual reset (section card) |
| **Pre-training** (key terms first) | ~0.75 | Define 1-3 key terms visually before the complex process |
| **Modality** (narration + graphics beats on-screen text + graphics) | ~0.7-1.0 | Explain with voice, show with visuals. Don't make viewers read paragraphs |
| **Personalization** (conversational style) | ~0.8 | "You" language in VO and on-screen text |
| **Embodiment / image** | mixed (the image principle is weak: a talking head adds little *learning*) | A presenter on screen helps engagement, but **cut away to the visual** during the hardest content |

**Dual coding** (Paivio 1971/1986): verbal plus pictorial representations improve recall versus either alone. **[STRONG]** **RULE:** every abstract claim gets a concrete visual: a number→chart, a process→diagram, a comparison→side-by-side.

### 5.7 Gestalt principles for layout

**[STRONG]**: perceptual grouping is foundational vision science (Wertheimer; Wagemans et al. 2012 review).

| Principle | RULE |
|---|---|
| Proximity | Space within a group ≤ **50%** of the space between groups (e.g. 16px inside a group, 40px+ between) |
| Similarity | Same function = same color, weight and shape. Change exactly one property to signal difference |
| Common fate | Elements that move together are seen as a group. Animate a group with a shared ease and direction. Use **different** timing only for things that are conceptually separate |
| Continuity | Align items on strong axes. Arrows and lines lead the eye to the next item |
| Closure | Partial shapes (a circle drawn 90%) read as complete. Draw-on reveals work |
| Figure/ground | The text plate must separate clearly from the footage (luminance, blur, scrim) |
| Common region | A container/plate groups items more strongly than proximity alone |

### 5.8 Reading patterns vs. video attention

- **F-pattern / Z-pattern** describe scanning of **text-heavy web pages** (NN/g eye-tracking, 2006, updated 2017). The F-pattern is a sign of poor formatting, not a design goal. **[STRONG]** for web pages, **N/A** for video.
- **Video gaze** is dominated by:
  1. **Center bias**: fixations cluster near the screen center, partly because of composition, partly a viewing strategy (Tseng et al. 2009). **[STRONG]**
  2. **Motion onsets.**
  3. **Faces**, especially eyes; gaze shifts to the mouth when speech is hard to hear.
  4. **Text**: free viewers looked at **faces 16.6x and text 11.1x** more than size- and position-matched control regions, even when it was costly to the task (Cerf, Frady & Koch 2009). **[STRONG]**
- **Attentional synchrony:** viewers of edited video look at the **same place at the same time** to a high degree ("tyranny of film"). Editing and motion largely control gaze (Smith & Henderson 2010; Smith & Mital 2013; Loschky et al. 2015). **[STRONG]**
- **RULES:**
  - Place new text **near the current gaze point**: near the speaker's face or the moving element, never in a far corner. **WHY:** it avoids long saccades and keeps the graphic within the attended region (also spatial contiguity).
  - **Don't put two text elements on screen at once if they're far apart.** Text captures gaze automatically, so two blocks split attention.
  - Keep the subject's **eyes on the upper-third line** (≈ 33-38% from the top in 16:9; ≈ 30-40% in 9:16), within ~20% of horizontal center for single-subject vertical video.
  - When a graphic appears, **dim or blur the face** briefly, or move the speaker aside. Faces otherwise compete for the gaze.

### 5.9 Captions and retention

| Claim | Rating | SRC |
|---|---|---|
| Captions improve comprehension, attention and memory for hearing viewers (review of 100+ studies) | [STRONG] for the core claim; strongest for non-native, literacy-learning and deaf/HoH viewers. Critics say "for everyone" is overstated for native-language adult viewers | GERNSBACHER-2015 |
| **69%** of US consumers watch video with sound off in public; **80%** of respondents say they're more likely to finish a video if captions are available (Verizon Media/Publicis 2019, n=5,616) | [INDUSTRY] self-report. Note that "80% *more* likely" is a common misquote | VERIZON-2019 |
| Viewers read subtitles automatically even in their own language (d'Ydewalle) | [STRONG] | Literature |

- **RULES:**
  - **Always** burn in captions for Shorts/Reels/TikTok. For long-form, upload an SRT/VTT *and* optionally burn in key-phrase emphasis.
  - Highlight **1 keyword per chunk** in the accent color, not every word.
  - Active-word highlight (karaoke) should change on the word onset (±1 frame).

---

## 6. Sound Design Psychology

### 6.1 Loudness targets

| Platform / standard | Integrated | True peak | Rating | SRC |
|---|---|---|---|---|
| **YouTube** | **-14 LUFS** reference (turns loud content down; does **not** turn quiet content up) | ≤ -1 dBTP | [INDUSTRY, observed via "Stats for nerds"; no official doc] | YT-LOUD |
| **Spotify** (also podcasts/video) | **-14 LUFS** (Loud -11, Quiet -19) | **≤ -1 dBTP**; ≤ -2 dBTP if the master is louder than -14 | [INDUSTRY, official] | SPOTIFY |
| Apple Music (Sound Check) | ~-16 LUFS | -1 dBTP | [INDUSTRY] | n/a |
| Apple Podcasts | **-16 LUFS ±1** | -1 dBTP | [INDUSTRY] | n/a |
| AES TD1004 streaming recommendation | -16 to -20 LUFS (speech-centric content toward -18) | ≤ -1 dBTP | [STANDARD] | AES-TD1004 |
| TikTok / Instagram Reels / Shorts | **No published target.** Observed normalization around -14 | -1 dBTP | [FOLK/observed] | n/a |
| **EBU R128** (EU broadcast) | **-23 LUFS ±0.5-1 LU** | **≤ -1 dBTP** | [STANDARD] | EBU-R128 |
| ATSC A/85 (US broadcast) | **-24 LKFS ±2** | -2 dBTP | [STANDARD] | ATSC-A85 |
| Netflix | **-27 LKFS dialogue-gated** | -2 dBTP | [INDUSTRY] | NETFLIX-AUDIO |

- **RULE (social/YouTube master):** **-14 LUFS integrated, -1 dBTP max, LRA 4-8 LU** for talking-head content. Dialogue is the anchor: **voice short-term loudness ≈ -14 to -16 LUFS** while speaking.
- **RULE:** check mono compatibility and phone-speaker translation. High-pass voice at 70-100Hz. Keep critical information above 150Hz, because phone speakers roll off below ~200-300Hz.

### 6.2 Music under voice (ducking)

- **Research:** Torcoli et al. (2019, AES; Fraunhofer/Salford, n=22) recommend a **loudness difference (LD) of ≥ 10 LU for commentary over music**, and **≥ 15 LU for commentary over ambience**. Non-experts preferred LDs **~4 LU larger** than experts did. For voice over voice: ≥ 20 LU (Geary et al. 2020). German public broadcaster guidance: LD ≥ 7 LU. **[MODERATE]** (small panels, consistent direction). SRC: TORCOLI-2019.
- **RULES:**
  - Music bed **12-18 LU below the voice** (short-term LUFS) under speech. With voice at -15 LUFS-S, music sits at about -27 to -33 LUFS-S. Use the deeper end (≥ 15 LU) for **explainers** (coherence principle) and for **general audiences** (non-experts want bigger gaps).
  - Between phrases and sentences, music may swell to **4-8 LU below** speech level. In music-only sections, bring it to the full mix level (around -14 to -16 LUFS-S).
  - Ducking dynamics: **attack 50-150ms, release 300-800ms**, with a 200-400ms look-ahead (pre-duck before the first syllable) [FOLK/craft]. Avoid audible "pumping" between words: use a hold of ~300-500ms.
  - EQ-carve instead of only turning down: cut the music by **2-4dB around 1-4kHz** (speech intelligibility band) while voice is present.
  - Pick instrumental, low-mid-sparse beds under VO. **No vocals in the music under speech**, because it competes for the same verbal processing channel.

### 6.3 SFX cueing [FOLK/craft unless noted]

| Event | SFX | Level (relative to voice) | Timing |
|---|---|---|---|
| Transition (wipe, whip, push) | Whoosh / swish | -6 to -12 dB under voice peak | Whoosh **peak lands on the cut frame**. The whoosh tail starts 4-10 frames before the cut |
| Text or word pop | Soft pop, click, tick | -12 to -20 dB | Transient on the **first frame** the element is visible (0-1 frame early is fine) |
| Number counter | Fast ticks, or a rising tone | -18 dB | Ends with a "ding" when the counter stops |
| Emphasis/impact (smash cut, title slam) | Hit / boom / riser→hit | -3 to -8 dB (brief) | Riser 1-4s before, hit on the frame |
| Error / negative | Low buzz / thud | -12 dB | On the reveal |
| Screen UI action (screen recording) | Mouse click, keyboard | -18 to -24 dB | Synced to the visible click |

- **RULE:** at most **1 SFX per second** on average in long-form explainers, and more in Shorts. Never stack SFX on top of key words. **WHY:** coherence principle (extraneous sounds hurt learning, d ≈ 0.86) **[STRONG]**.
- **RULE:** give every SFX a **visual cause** (audio-visual synchrony). Unmotivated sounds read as noise.
- **Audio-visual sync tolerance:** audio may lead video by ≤ ~45ms or lag by ≤ ~125ms before viewers notice (ITU-R BT.1359) **[STANDARD]**. Snap SFX to the frame.

### 6.4 Silence and rhythm

- **Silence as emphasis:** cut music to silence (or a room-tone-only pause of **0.5-1.5s**) right before a key reveal or punchline. The contrast creates an orienting response to the next sound onset. **[MODERATE]**: auditory onsets and changes trigger orienting (LC4MP literature). The specific durations are [FOLK].
- **BPM ↔ pacing [FOLK/craft]:**
  - Frames per beat = fps × 60 / BPM. At 30fps and 120 BPM that's 15 frames per beat; at 100 BPM, 18 frames; at 24fps and 120 BPM, 12 frames.
  - Energetic Shorts/montage: **110-140 BPM**, cutting on beats or every 2 beats. Explainer beds: **80-110 BPM**. Documentary/emotional: **60-90 BPM**.
  - Cut on **downbeats** for big changes and on off-beats for small ones. Let section changes in the music (drops, new phrase every 4 or 8 bars) coincide with chapter changes.
  - Speech rate reference: conversational/presenting English ≈ 140-170 wpm (BBC subtitle guidance assumes 160-180 wpm speech). Above ~190 wpm, comprehension and caption readability suffer.

---

## 7. Anti-"AI Slop" Visual Tells (and what to do instead)

These are **[FOLK]** taste rules, but they're consistent across design critics and practitioners, and they follow from the principles above (hierarchy, one accent, coherence).

| Tell | Why it reads as slop | Do instead |
|---|---|---|
| **Purple→blue/pink gradient** on everything (especially `#7C3AED→#3B82F6`) and neon purple glow | The default "AI/tech" aesthetic of templated SaaS and LLM-generated UIs | Derive the palette from the footage or brand (§3.3). Use flat tinted neutrals with **one** accent. If you use a gradient, make it **same-hue lightness ramps** in OKLCH with grain |
| **Glow and outer bloom** on text and icons | Lowers legibility, looks like a template, and bands after compression | Use a crisp contact shadow (§1.7) or no effect |
| **Glassmorphism everywhere** (frosted cards on blurred blobs) | Overused since 2021. Low contrast, and expensive blur that compresses badly | Solid plates at 85-95% opacity, or one glass element max per scene, over real footage |
| **Everything centered**, symmetric, on a dark void | No hierarchy and no tension. Reads as a slide template | Use a grid. Left-align text blocks to the title-safe edge. Asymmetric compositions with the subject on thirds |
| **Too many fonts / random weights** | No system | ≤ 2 families, ≤ 3 weights (§1.5) |
| **Bounce/elastic on everything** | No hierarchy of motion. Cartoony | Overshoot budget (§4.2): spring or back easing only on the hero, decelerate curves for the rest |
| **Everything animates in at once** or with an identical fade-up-20px | Generic "AOS/scroll-reveal" look | Choreograph: lead element, then followers (40-80ms stagger), each with a motivated direction |
| **Emojis as icons** 🚀✨🔥 | Platform-dependent rendering, cheap look, inconsistent stroke styles | One consistent icon set (Lucide, Phosphor, Material Symbols, Tabler) at one stroke weight (1.5-2px at 24px, scaled) |
| **Generic stock B-roll / AI-generated filler** (handshake, glowing brain, server rooms) | Violates coherence. Viewers recognize it | Literal, specific visuals: screenshots, real product, real data, the speaker's own footage, diagrams |
| **Floating 3D blobs, abstract particle fields, "neural network" lines** | Decorative motion competing with content (coherence, d ≈ 0.86) | Remove, or keep ambient motion below 2-5% of frame per second at ≤ 30% opacity |
| **Rounded-everything with drop-shadow cards** (`rounded-2xl shadow-xl`) | Tailwind default aesthetic | Vary radii intentionally (0, 4 or 8px). Use hairline borders, or no container at all |
| **Lorem-like copy**: "Unlock the power of…", "Revolutionize your…", "Seamless" | LLM copywriting tells | Concrete nouns and numbers from the actual transcript |
| **Perfectly even rhythm** (every cut 2.0s, every caption identical) | Machine-uniform pacing | Vary shot lengths (§5.3, the 1/f idea). Let emphasis words get bigger or longer treatment |
| **Gradient text on every headline** | Lowers contrast. Clichéd | Solid color. Accent only on 1-2 keywords |
| **Typewriter effect for long sentences** | Slow and gimmicky. Delays reading | Word- or line-level reveals at ≤ 300ms total, or a straight cut-in |
| **Lens-flare / light-leak transitions everywhere** | Template look | Hard cuts (≈ 90%+ of all transitions in professional edits are straight cuts [FOLK]). Use a motivated transition only at section changes |
| **Inter + purple + glass + emoji** all together | The full "AI landing page" stack | Pick the font by mood from §2, the color from footage, and an icon set |

**RULE:** before rendering, run a **slop audit**:

- [ ] ≤ 2 font families
- [ ] Exactly 1 accent hue
- [ ] No more than 1 bouncing element per scene
- [ ] No emoji used as an icon
- [ ] No full-frame gradient without grain
- [ ] Every graphic is tied to a spoken word (temporal contiguity)
- [ ] Every text block is inside the safe area and passes contrast against its actual background in every frame

---

## 8. Machine-Readable Defaults (for the skill's config)

```json
{
  "safe_area": {
    "16x9_title_inset_pct": 5, "16x9_action_inset_pct": 3.5,
    "9x16_universal_rect_px": {"x0": 80, "x1": 900, "y0": 250, "y1": 1440},
    "youtube_bottom_reserved_pct": 12
  },
  "type": {
    "min_font_pct_h_16x9": 4.5, "phone_first_font_pct_h_16x9": 6.0,
    "shorts_caption_px_at_1080w": [64, 96], "absolute_floor_px_1080": 28,
    "caption_max_cpl_16x9": 42, "caption_max_cpl_9x16": 20, "caption_max_lines": 2,
    "cps_comfort": 17, "cps_max": 20, "sec_per_word_min": 0.3, "min_caption_s": 0.8,
    "allcaps_tracking_em": [0.05, 0.12], "display_tracking_em": [-0.03, -0.01],
    "body_leading": [1.2, 1.45], "display_leading": [0.9, 1.1],
    "max_families": 2, "max_weights": 3, "min_weight_below_60px": 400,
    "stroke_px_1080": [2, 4], "shadow_css_1080": "0 2px 10px rgba(0,0,0,.65), 0 0 2px rgba(0,0,0,.6)",
    "scrim": {"height_pct": 35, "max_alpha": 0.7}
  },
  "color": {"wcag_text": 4.5, "wcag_large": 3.0, "apca_caption_min_lc": 75, "apca_headline_min_lc": 45,
            "accent_count": 1, "accent_max_area_pct": 10, "grain_pct": [1, 5], "interp_space": "oklch"},
  "ease": {
    "enter": "cubic-bezier(0.05,0.7,0.1,1)", "exit": "cubic-bezier(0.3,0,0.8,0.15)",
    "move": "cubic-bezier(0.2,0,0,1)", "snappy_out": "cubic-bezier(0.22,1,0.36,1)",
    "expo_out": "cubic-bezier(0.16,1,0.3,1)", "back_out_10pct": "cubic-bezier(0.34,1.56,0.64,1)"
  },
  "duration_ms": {"micro": [70, 150], "small": [150, 250], "medium": [300, 450], "large": [450, 700],
                  "transition_full_frame": [300, 600], "exit_ratio": 0.8, "stagger_item": [40, 80], "stagger_total_max": 600},
  "overshoot_pct": {"corporate": [0, 3], "creator": [5, 10], "playful": [10, 20]},
  "flash_max_per_s": 3,
  "audio": {"integrated_lufs": -14, "true_peak_dbtp": -1, "music_under_voice_lu": [12, 18],
            "duck_attack_ms": [50, 150], "duck_release_ms": [300, 800], "av_sync_ms": {"audio_lead_max": 45, "audio_lag_max": 125}},
  "pacing_visual_change_s": {"shorts": [1.5, 3], "longform_talking": [3, 8], "documentary": [4, 12]},
  "punch_in_scale": [1.10, 1.25]
}
```

---

## 9. Source List

Primary and authoritative sources come first in each group. All were accessed in October 2026 unless noted.

**Typography, subtitles, safe areas**
- NETFLIX-TTSG: Netflix English (USA) Timed Text Style Guide. https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide
- Netflix Timed Text Style Guide, General Requirements. https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements
- BBC-SUB: BBC Subtitle Guidelines. https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/
- EBU-R95: EBU R95, Safe areas for 16:9 television production. https://tech.ebu.ch/publications/r095 (PDF: https://tech.ebu.ch/docs/r/r095.pdf)
- SMPTE-2046: SMPTE ST 2046-1, Safe Areas for 16:9 Television Systems. https://doi.org/10.5594/SMPTE.ST2046-1.2009 (overview: https://en.wikipedia.org/wiki/Safe_area_(television))
- BUTTERICK: Butterick's Practical Typography, Summary of key rules. https://practicaltypography.com/summary-of-key-rules.html ; letterspacing: https://practicaltypography.com/letterspacing.html
- LEGGE-BIGELOW-2011: Legge & Bigelow, "Does print size matter for reading?", *Journal of Vision* 11(5):8. https://pmc.ncbi.nlm.nih.gov/articles/PMC3428264
- SZARKOWSKA-2018: Szarkowska & Gerber-Morón, "Viewers can keep up with fast subtitles", *PLoS ONE*. https://discovery.ucl.ac.uk/id/eprint/10050653/
- BRYSBAERT-2019: Brysbaert, "How many words do we read per minute?", *J. Memory & Language*. https://www.Gwern.net/doc/psychology/linguistics/2019-brysbaert.pdf
- GOOGLE-FONTS-KNOWLEDGE: Google Fonts Knowledge (pairing, optical size). https://fonts.google.com/knowledge
- FONTSHARE: ITF Fontshare license info. https://www.fontshare.com/licenses ; https://www.indiantypefoundry.com/news/introducing-fontshare
- 9:16 safe zones (third-party, measured, non-official): https://reap.video/blog/short-form-video-safe-zones ; https://adkit.so/tools/safe-zones/tiktok ; https://www.hopperhq.com/blog/instagram-reel-size/ ; https://www.outfy.com/blog/instagram-safe-zone/ ; https://moda.app/tools/story-safe-zone-checker
- TIKTOK-CBP: TikTok Ads, Creative best practices for performance ads. https://ads.tiktok.com/help/article/creative-best-practices

**Color & contrast**
- WCAG: W3C WCAG 2.2, contrast (1.4.3, 1.4.6, 1.4.11) and three flashes (2.3.1). https://www.w3.org/TR/WCAG22/
- APCA: APCA in a Nutshell. https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell
- ELLIOT-MAIER-2014: Elliot & Maier, "Color psychology: Effects of perceiving color on psychological functioning in humans", *Annu. Rev. Psychol.* 65. https://doi.org/10.1146/annurev-psych-010213-115035
- GNAMBS-2020: Gnambs et al., "Processing the word red and intellectual performance: four replications". https://pure.fh-ooe.at/en/publications/processing-the-word-red-and-intellectual-performance-four-replica/
- PBR-2020-COLOR: Review of color-priming in achievement contexts, *Psychonomic Bulletin & Review* (2020). https://link.springer.com/article/10.3758/s13423-020-01772-1
- ADOBE-SKIN: Adobe Premiere Pro, Correct skin tones. https://helpx.adobe.com/premiere-pro/how-to/correct-skin-tones.html
- JORDAN / VAN-HURKMAN: Larry Jordan, "The secret to setting skin colors accurately" (cites Van Hurkman's *Color Correction Handbook*). https://larryjordan.com/articles/the-secret-to-setting-skin-colors-accurately/
- PVC-BANDING: ProVideo Coalition, Remove banding in After Effects. https://www.provideocoalition.com/remove-banding-in-after-effects/
- YT-ENC: YouTube recommended upload encoding settings. https://support.google.com/youtube/answer/1722171
- OKLCH/OKLab: Björn Ottosson, "A perceptual color space for image processing". https://bottosson.github.io/posts/oklab/

**Motion**
- M3-TOKENS: Material Web motion tokens (v0.192, Apache-2.0). https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-motion.scss ; docs: https://m3.material.io/styles/motion/easing-and-duration/tokens-specs
- M1-MOTION: Material Design (v1), Duration & easing. https://m1.material.io/motion/duration-easing.html
- CARBON-MOTION: IBM Carbon Design System, Motion. https://carbondesignsystem.com/elements/motion/overview/
- NNG-ANIM: NN/g, "Animation Duration". https://www.nngroup.com/articles/animation-duration/
- APPLE-SPRING: Apple, `spring(response:dampingFraction:blendDuration:)`. https://developer.apple.com/documentation/swiftui/animation/spring(response:dampingfraction:blendduration:) ; `Spring`: https://developer.apple.com/documentation/swiftui/spring
- WWDC23-SPRINGS: WWDC23 "Animate with springs" (session 10158). https://developer.apple.com/videos/play/wwdc2023/10158/ ; notes: https://wwdcnotes.com/documentation/wwdc23-10158-animate-with-springs/
- EASINGS: easings.net (Penner equations as cubic-beziers). https://easings.net/
- GSAP eases: https://gsap.com/docs/v3/Eases/
- DISNEY-12: Thomas & Johnston, *The Illusion of Life: Disney Animation* (1981). Summary: https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation
- ITU-R BT.1702 (photosensitive epilepsy guidance). https://www.itu.int/rec/R-REC-BT.1702
- ITU-R BT.1359 (relative timing of sound and vision). https://www.itu.int/rec/R-REC-BT.1359

**Editing & attention**
- MURCH: Walter Murch, *In the Blink of an Eye* (2nd ed., 2001). Rule of Six summary: https://wikis.utexas.edu/display/rtf318/Murch%27s+Rule+of+Six ; https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch
- Nakano et al. (2009), "Synchronization of spontaneous eyeblinks while viewing video stories", *Proc. R. Soc. B*. https://doi.org/10.1098/rspb.2009.0828
- CUTTING-2010: Cutting, DeLong & Nothelfer, "Attention and the evolution of Hollywood film", *Psychological Science* 21(3). https://journals.sagepub.com/doi/10.1177/0956797610361679 ; summary: https://www.psychologicalscience.org/observer/the-science-of-hollywood-blockbusters-2
- LANG-1993: Lang, Geiger, Strickwerda & Sumner (1993), "The effects of related and unrelated cuts on viewers' memory for television: A limited capacity theory of television viewing", *Communication Research* 20(1):4-29. (DOI not verified this session; search the title on journals.sagepub.com)
- Lang & Thorson (1992), on videographics in televised talking-head lectures eliciting orienting responses (cited via secondary sources).
- Lang, "The limited capacity model of mediated message processing", *J. Communication* 50(1), 2000. https://doi.org/10.1111/j.1460-2466.2000.tb02833.x
- Smith & Henderson (2008), "Edit Blindness", *J. Eye Movement Research*. https://doi.org/10.16910/jemr.2.2.6
- Smith & Mital (2013), "Attentional synchrony and the influence of viewing task on gaze behavior in static and dynamic scenes", *J. Vision*. https://doi.org/10.1167/13.8.16
- Loschky et al. (2015), "What would Jaws do? The tyranny of film…", *PLoS ONE*. https://pmc.ncbi.nlm.nih.gov/articles/PMC4659561
- CERF-2009: Cerf, Frady & Koch, "Faces and text attract gaze independent of the task", *J. Vision* 9(12). https://resolver.caltech.edu/CaltechAUTHORS:20130816-103355264
- Tseng et al. (2009), "Quantifying center bias of observers in free viewing of dynamic natural scenes", *J. Vision*. https://doi.org/10.1167/9.7.4
- NN/g F-pattern (2017 update). https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
- YT-KEYMOMENTS: YouTube Help, Measure key moments for audience retention. https://support.google.com/youtube/answer/9314415
- YouTube Help, Content analytics. https://support.google.com/youtube/answer/12942217
- YT-SHORTS-METRIC: "Viewed vs. swiped away" (glossary). https://www.creatoressentials.com/glossary/viewed-vs-swiped-away/
- META-NIELSEN: Facebook/Nielsen brand-lift-in-seconds study (coverage). https://martech.org/even-brief-video-views-drive-brand-lift-facebook-nielsen-study-finds/
- ATTN-MYTH: the goldfish/8-second myth. https://www.bbc.com/news/health-38896790 (BBC *More or Less*, 2017); https://www.warc.com/newsandopinion/opinion/the_goldfish_myth/2806
- Loewenstein (1994), "The psychology of curiosity", *Psychological Bulletin* 116(1). https://doi.org/10.1037/0033-2909.116.1.75
- Kang et al. (2009), "The wick in the candle of learning", *Psychological Science*. https://doi.org/10.1111/j.1467-9280.2009.02402.x
- Gruber, Gelman & Ranganath (2014), "States of curiosity modulate hippocampus-dependent learning", *Neuron*. https://doi.org/10.1016/j.neuron.2014.08.060
- ZEIGARNIK-2025: Ghibellini & Meier (2025), "The Zeigarnik effect revisited", *Humanities & Social Sciences Communications* 12. https://ideas.repec.org/a/pal/palcom/v12y2025i1d10.1057_s41599-025-05000-w.html
- MAYER-2014: Mayer & Fiorella, "Principles for reducing extraneous processing…" in *Cambridge Handbook of Multimedia Learning* (2nd ed.). https://resolve-he.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles/CD5B7AE1279A9AB81F8EEBB53DBEC86E
- MAYER-2021: Mayer, *Multimedia Learning* (3rd ed., Cambridge UP, 2021).
- Sweller (1988), "Cognitive load during problem solving", *Cognitive Science* 12(2). https://doi.org/10.1207/s15516709cog1202_4
- Paivio, *Mental Representations: A Dual Coding Approach* (1986).
- Wagemans et al. (2012), "A century of Gestalt psychology in visual perception", *Psychological Bulletin*. https://doi.org/10.1037/a0029333
- GERNSBACHER-2015: Gernsbacher, "Video Captions Benefit Everyone", *Policy Insights from the Behavioral and Brain Sciences* 2(1). https://successforkidswithhearingloss.com/wp-content/uploads/2020/04/Video-Captions-Benefit-Everyone_2015.pdf
- VERIZON-2019: Verizon Media/Publicis Media caption survey (coverage). https://www.3playmedia.com/blog/verizon-media-and-publicis-media-find-viewers-want-captions/

**Sound**
- SPOTIFY: Spotify for Artists, Loudness normalization. https://support.spotify.com/artists/article/loudness-normalization/
- YT-LOUD: Ian Shepherd/MeterPlugs, "YouTube changes loudness reference to -14 LUFS" (2019). https://www.meterplugs.com/blog/2019/09/18/youtube-changes-loudness-reference-to-14-lufs.html
- EBU-R128: EBU R128, Loudness normalisation and permitted maximum level. https://tech.ebu.ch/publications/r128
- ATSC-A85: ATSC A/85, Techniques for establishing and maintaining audio loudness. https://www.atsc.org/atsc-documents/a85-techniques-for-establishing-and-maintaining-audio-loudness-for-digital-television/
- NETFLIX-AUDIO: Netflix Sound Mix Specifications & Best Practices (Netflix Partner Help Center; search "Sound Mix Specifications" at https://partnerhelp.netflixstudios.com). Secondary confirmation: https://thepostflow.com/filmmaker-resources/delivery-specs-cheat-sheet/
- AES-TD1004: AES TD1004.1.15-10, Recommendation for Loudness of Audio Streaming and Network File Playback. https://www.aes.org/technical/documentDownloads.cfm?docID=731
- TORCOLI-2019: Torcoli, Freke-Morin, Paulus, Simon & Shirley, "Background ducking to produce esthetically pleasing audio for TV with clear speech", AES 146th Convention. https://salford-repository.worktribe.com/OutputFile/1488623 ; Fraunhofer summary: https://www.audioblog.iis.fraunhofer.com/?p=4251
- Geary, Torcoli et al. (2020), "Loudness differences for voice-over-voice audio in TV and streaming", *JAES*. https://salford-repository.worktribe.com/output/1341554/loudness-differences-for-voice-over-voice-audio-in-tv-and-streaming

---

### Verification notes (honesty log)

- **Verified directly this session** (fetched or confirmed via search): Netflix 42 cpl / 20 & 17 cps; all BBC numbers; EBU R95 3.5% and 5%; M3 token values (from source code); Carbon easing and durations; M1 225/195ms and the tablet/desktop rules; NN/g 100-500ms; Apple spring defaults 0.5 / 0.825; APCA Lc levels; Butterick's 5-12% / 45-90 / 120-145%; Spotify -14 / -1 / -2; YouTube encoding settings; Murch percentages; Cutting 2010; Mayer d for coherence, signaling and redundancy; Zeigarnik 2025 meta-analysis; Cerf 16.6x / 11.1x; Verizon 69% / 80%; Meta 47% / 74%; TikTok 3s / 6s and "5-10 words per second"; Torcoli ≥ 10 / 15 LU; Legge 0.2-2°; Brysbaert 238 wpm.
- **From established knowledge, not re-fetched:** easings.net bezier values; the Penner back overshoot (10%); ITU-R BT.1359 sync tolerances; the Apple Podcasts -16 LUFS figure; AES TD1004 range; Nakano 2009; Tseng 2009; Smith & Henderson 2008 edit blindness; Kang 2009 / Gruber 2014; the SwiftUI preset bounce values (0 / 0.15 / 0.3, approximate); the ~63% YouTube mobile share.
- **Mayer spatial/temporal contiguity and segmenting d values** come from a secondary review (0.79 / 1.30 / 0.70) and Mayer's earlier reported medians (~1.1 / ~1.2 / ~0.8). They're given as ranges.
- **9:16 UI safe-zone pixels are not officially published** by TikTok, Meta or YouTube for organic posts. Re-measure periodically.
