# Mistakes an AI editor makes, and the guard for each

Built from a 6-lens audit of this skill (rough cut, captions, sound, motion graphics, colour and sourcing,
workflow) plus HyperFrames engine issues and motion-craft research, October 2026. Every item was checked
against the scripts before it went in. **[AUTO]** means a script now catches it; **[CHECK]** means it stays a
human or agent check, with the exact check to run. Read the section for the stage you are in.

## Contents
1. The meta-rules (how editors lie to themselves)
2. Rough cut
3. Captions and on-screen text
4. 9:16 safe zones
5. Sound
6. Motion graphics and HyperFrames
7. Colour and visual sourcing
8. Ads, disclosure, licences
9. What the AI cannot do at all

## 1. The meta-rules

- **"I looked at it" must leave a trace.** After `qa.py`, write `qa/qa-look.md`: one verdict line per sheet
  ("cuts.png: 14 edit points, 2 jumps re-punched at 0:41 and 1:03"; "safezone_reels.png: all text inside";
  "captions.png: 24 groups, no face overlap, fixed 'Ananya'"). No qa-look.md means not done.
- **"Could not check X" needs an attempt.** Write it as "tried <command>, failed: <exact error>". A deliverable
  that was never rendered carries the banner UNRENDERED, NOT VERIFIED and is never called done.
- **WARN is not PASS.** `qa.py` exits 1 on FAIL; every WARN line needs a written disposition in
  `EDIT_STATE.md` (fixed, or accepted with the reason) before delivery. Black frames, freezes and dead air are
  WARNs because sometimes they are intentional, not because they are harmless.
- **Approvals are written, not remembered.** Cutlist approval, reorder approval, storyboard approval and final
  approval each get a dated line in `EDIT_STATE.md` before the step that depends on them runs.
- **When the user is away:** cutlist, storyboard and final delivery are hard holds (wait). Graphics and caption
  iterations may proceed with the assumption written down.
- **A green exit code is not a correct video.** Read logs, look at frames, measure. (HyperFrames can exit 0 on a
  near-still render; see section 6.)

## 2. Rough cut

| Mistake | Guard |
|---|---|
| Retake logic deleted a real sentence sitting between an abandoned take and its restart | [AUTO] `plan_cuts.py` only removes hesitation between them; otherwise keeps both and lists it under "Review these" |
| A short kept word ("I", "no") under 0.25 s vanished from the video and the captions | [AUTO] short segments are widened, never dropped; cutlist prints "N/N kept words placed" and a WARNING on any mismatch |
| Fixed -38 dB silence threshold: no pauses found on quiet speakers, fake pauses inside music beds | [AUTO] threshold calibrated to the speech level; cutlist reports how many boundaries landed in silence and warns under 50% |
| Whisper invents words over silence; they become kept speech and captions | [AUTO] low-confidence words inside silences are flagged for review (`--drop-silent-words` removes them). [CHECK] read every flagged word |
| Variable-frame-rate phone footage passes as 30 fps; every cut and caption drifts | [AUTO] `probe.py` measures real frame timestamps; `plan_cuts.py` refuses VFR until re-encoded (command printed) |
| 20 ms join fades are shorter than one AAC frame; clicks survive | [AUTO] default 30 ms |
| Punch-in lands under a graphic | [AUTO] `render_cut.py --no-punch 12-15.5,30-34` (edited-timeline ranges from the storyboard) |
| Punch crop slightly stretched | [AUTO] crop height derived from width |
| `-fps_mode cfr` dup/drop on odd frame rates | [AUTO] output rate pinned to the source's exact rate |
| verify_cut passed with a clipped word because the match ratio was high | [AUTO] exits 1 on any missing/changed word; uses the source's own model; drift tolerance 250 ms (Whisper's own jitter) |
| verify_cut cannot catch what both speech passes mishear or invent | [CHECK] it only catches gross render damage. Listen to every join, or write "listened to N joins at <times>" in EDIT_STATE.md |
| Reframe crops the centre before the first face detection | [AUTO] back-filled from the first detection; WARN for sections where the face was found under half the time |
| J/L cuts asked for but the renderer only makes hard cuts | Honest limit: `render_cut.py` cuts A-roll picture and sound together. Get J/L feel by laying B-roll or a cutaway across the join (`overlay.py` cutaway mode keeps the base audio running), not by offsetting the A-roll audio |
| Hinglish auto-detected as English and translated | [CHECK] always pass `--language hi` (or the real language) for Hindi/Hinglish; a fluent English transcript of Hinglish audio is a translation, not a transcript |
| Speaker interjection ("Right.") removed as part of a retake in a 2-person recording | [CHECK] multi-speaker recordings: read every retake in cutlist.md before approving |

## 3. Captions and on-screen text

| Mistake | Guard |
|---|---|
| Key words at 1.6x size or 36% apex not counted in the width model; lines overflow | [AUTO] widths use each word's real size and font, plus the outline |
| Groups too wide even at 70% size, rendered overflowing silently | [AUTO] WARN naming each group |
| Apex word shrunk to irrelevance on 9:16 | [AUTO] WARN under 60%; pick a 4-7 letter key word |
| `--style-json` font without a width estimate | [AUTO] WARN; measure `char_w` |
| "well-known" glued to "wellknown"; "e.g." to "eg" | [AUTO] dashes become spaces; abbreviations kept |
| Unreadable flashes (>25 characters per second) | [AUTO] WARN listing them; condense or lower `--max-words` |
| Hook title and captions on screen at once | [AUTO] `--hook-until <s>` suppresses captions under the hook |
| Burned captions plus uploaded CC = double text | [AUTO] note on every burn; upload the SRT as a separate track or not at all |
| 16:9 captions inside YouTube's bottom UI band | [AUTO] default y 0.83 |
| Silent libass font substitution | [AUTO] WARN when a style's font files are missing (only when burning). [CHECK] compare one rendered frame against the font specimen |
| Raw Whisper word timing (+/-100-300 ms) breaks the "highlight within 80 ms" rule | [CHECK] for karaoke/active highlight styles, align first (stable-ts `align()` or WhisperX); otherwise use key or static styles |
| Faces covered by body captions | [CHECK] captions.png and the safe-zone sheet; move with `--y`. Apex words in style 11 may overlap faces, body captions may not |

## 4. 9:16 safe zones (the user's standing rule)

Every word, logo and graphic that must be read sits inside the platform's safe box and off the button rail.
Instagram Reels (organic, the user's spec): 220 px top, 420 px bottom, 1010 px wide (x 35-1045, y 220-1500),
with the like/comment/share column in the bottom-right corner (x > 950, y > 1340). Other platforms and the
cross-posting box: `platforms-and-styles.md` PART B. Reference image: `assets/safe-zones/`.

| Where text comes from | Guard |
|---|---|
| Captions (`captions.py`) | [AUTO] `--platform reels|tiktok|shorts|cross` sets the width and position limits and WARNs on any group outside the box or on the rail |
| HyperFrames compositions | [AUTO] `safezone.py html <dir> --platform reels` seeks the timeline 10x per second and measures every visible text box (ink-accurate within ~7 px) |
| Transparent overlays (MOV/WebM) | [AUTO] `safezone.py alpha <file> --platform reels` reads the alpha channel |
| Burned text in footage, logos, final deliverable | [CHECK] `qa.py` draws the box on sampled frames (`safezone_<platform>.png`); LOOK at it |
| Designing | `safezone.py guide` or `assets/safe-zones/guide_<platform>.png` as a temporary layer (never rendered) |
| The kinetic-reel starter | `data-platform="reels"` (or tiktok, shorts, cross, reels-ad) sizes the stage to the box; text auto-fits, including the 112% apex slam |

Cross-posting to TikTok/Shorts as well: use `cross`; it is narrower (TikTok's rail starts at y 840), so
captions get shorter groups. Instagram-only: use `reels` for fuller lines.

## 5. Sound

| Mistake | Guard |
|---|---|
| 16-bit premix clipped coincident peaks permanently | [AUTO] 32-bit float premix |
| Mono voice collapsed a stereo music bed to mono | [AUTO] voice upmixed to stereo before the mix; `qa.py` WARNs on mono output |
| Music, ducking and SFX set in absolute dBFS: a quiet narrator ended up under the music | [AUTO] bed placed `--music-sep` LU (default 20) under the measured voice; duck threshold follows the voice; SFX `db` relative to the voice peak |
| Risers placed by file edges, peaking early | [AUTO] `end_at`/`peak_at` land the file's loudest sample on the frame |
| De-esser and compressor promised in the docs, missing in the script | [AUTO] `finish.py --voice-chain full` (compressor 3:1, then de-esser) |
| Silent input crashed with a misleading error | [AUTO] clear "audio is silent" error |
| SFX placed past the end vanished silently | [AUTO] WARN and skip |
| Duck pumping at phrase starts (8:1 ratio) | [AUTO] 4:1, 700 ms recovery |
| Bed with vocals under narration | [CHECK] ask at intake; listen to the bed alone |
| Content-ID: Short over 60 s with a claimable track | [CHECK] music source + licence in EDIT_STATE.md before upload |
| Epidemic Sound track used after the subscription lapsed | [CHECK] note "subscription active at publish: yes, <date>" next to every Epidemic track ID |
| No room-tone glue: noise floor steps at every cut | [CHECK] listen with eyes closed at joins; lay a quiet room-tone bed (-45 to -50 dB) under dialogue when steps are audible |
| Denoise learning its profile from speech (no quiet lead-in) | [CHECK] only use `--denoise` when the recording starts with room tone |

## 6. Motion graphics and HyperFrames

**Engine traps (verified in HyperFrames issues/docs):**
- Render exits 0 with a near-still video when the composition script throws (issue #3352). Read the render log
  for `Composition script failed` / `sub_timeline_readiness_timeout`; sample frames and require at least 3
  distinct frames.
- Nested paused timelines report duration 0: all-black render with lint/check passing (issue #3419). One flat
  registered timeline per composition.
- `--fps 60` renders GSAP motion at 30 fps with duplicated frames (issue #1737). Render DOM/GSAP motion at
  30 fps; 60 only for shader-led pieces.
- `from()` desyncs on seek and can animate 0 to 0 against a hidden start: use `fromTo` only.
- A standalone `gsap.to()` not on the registered timeline never renders.
- `repeat: -1` breaks capture: use finite repeats, `Math.floor(dur / cycle)`.
- Register the timeline LAST. Font-load-then-build is fine only if registration is the final line (the
  kinetic-reel starter does this).
- Snapshots can be stale in multi-composition projects: identical hashes at different times = stale; render
  at low quality for ground truth.
- WebM alpha shows black in editors and Safari: ship ProRes 4444 MOV for anything leaving the browser.
- Clip windows are half-open: resolve end states at least one frame early.
- Never paint backgrounds on html/body/root for alpha renders; use a full-bleed layer.
- `src` goes on `<audio>/<video>` itself, never on a `<source>` child.

**Craft mistakes:**
- **Fonts flash in a fallback face** for the first frames: load the exact faces (`document.fonts.load('400
  330px "Anton"')`) before building, then register last.
- **Real copy longer than the example** clips off-frame: shrink-to-fit at build (the starter's `fitText`),
  checked against the slam scale.
- **Measure at the slam, not at rest.** A 112% entrance pushes text past the box for 5 frames; dense sampling
  in `safezone.py` catches it.
- **Climax late against the word:** in `graphics.json` give `"at": <word time>, "climax": <seconds into the
  graphic>`; `overlay.py` starts it early so the climax lands on the word. Frame-check the word time.
- **Graphic past the end of the video** never appears: `overlay.py` refuses.
- **Missing vendored files** after copying a starter (gsap.min.js, fonts/, grain.png): copy the whole folder;
  the null-timeline error means gsap.min.js is missing.
- **Captions burned before graphics** end up under plates: pipeline order is cut, grade, graphics, captions,
  finish.
- **Intentional hard pops reported as glitches:** `qa_graphic.py --beats` with the beat times; never soften a
  designed pop into a fade to silence a warning.
- **Double grain** (footage grain plus graphic grain): grain the footage OR the graphic, not both.
- **Everything with one duration and ease** reads as template-made: vary by importance (entries 0.3-0.8 s).
- **No exits:** every element that enters must leave or be explicitly persistent.
- **Ease on the wrong property:** position and scale ease out; opacity linear or gentle; overshoot only on
  small elements.
- **Character stagger on long copy:** character stagger only for headlines up to ~8 words; group reveals under
  0.8 s.
- **One-frame flash in the end position** before an entrance: set the initial state at the exact time the
  layer's window opens.
- **Dead holds read as a stalled player in muted feeds:** fully static over ~0.8 s needs ambient motion (grain
  drift, slow push); a read-hold after a climax is fine.
- **Sub-pixel shimmer on slow moves:** round interpolated translate values to whole pixels.
- **Gradient banding:** avoid low-span gradients; dither with grain at the gradient; interpolate stops in OKLCH.
- **Weight ramps on proportional fonts re-wrap lines:** variable monospaced fonts only.
- **Stacked reads:** keep reads at least 0.3 s apart within a beat.
- **Determinism test:** render twice and diff a mid frame; any difference is a seek bug (random numbers, CSS
  keyframes, timers).

## 7. Colour and visual sourcing

| Mistake | Guard |
|---|---|
| HDR source graded as SDR, tagged BT.709 | [AUTO] `grade.py` refuses HDR without `--tonemap` |
| `--look` and `--lut` together (double grade) | [AUTO] refused |
| Creative LUT applied at 100% | [AUTO] LUT-only defaults to 75% |
| Match gains clamped silently / clipping faces | [AUTO] WARN at the clamp and on strong gains; check skin on `--still` |
| Glow invisible at 4K, fog at 540p | [AUTO] blur scales with resolution |
| Grading the captioned or already-graded file | [AUTO] WARN by filename; always grade the ungraded master |
| Mixed lighting (tungsten + daylight) in one frame | [CHECK] a global match cannot fix it: Resolve with power windows, or reshoot note |
| Phone auto-exposure flicker | [CHECK] look for pumping brightness; ffmpeg `deflicker` for affected clips |
| Pinterest or watermarked stock shipped | [CHECK] every raster asset needs a source URL and licence line; Pinterest without the original's licence = FAIL |
| AI shots drifting (face, palette) between scenes | [CHECK] one base image per character, Higgsfield with character reference + logged seed; compare frames side by side |
| Accent colour near skin hue | [CHECK] keep the accent at least 25-30 degrees of hue away from skin |

## 8. Ads, disclosure, licences

- **When in doubt, disclose.** Any synthetic human appearance or AI voice in paid creative gets a conspicuous
  on-screen disclosure, in every market. The New York audio-only exemption does not exist in the EU AI Act;
  exemptions are narrow and jurisdiction-specific and never the default.
- **`finish.py` re-encodes and strips C2PA/provenance metadata.** Keep the pre-finish master (or the AI tool's
  original export) as the provenance record, and never claim provenance survived the export.
- Licence lines need a source URL or licence name per file; "free" without a source is not a licence.

## 9. What the AI cannot do at all

It cannot hear (timbre, harshness, groove, whether a bed fits), cannot judge taste reliably from a single
frame, and cannot prove a licence. Mitigation is structural: meter everything, keep the human checks (Closed
Eye Test, phone-speaker listen, the 15-second promise stopwatch), and never let a meter PASS stand in for them.
