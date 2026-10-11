# GitHub and tooling research for the AI video editor skill

Contents: 1. HyperFrames (CLI verification, install needs, gotchas) · 2. Agent and Claude skills for video editing on GitHub (all cloned and read unless marked) · 3. Remotion vs HyperFrames vs Motion Canvas vs Revideo (for an agent) · 4. Word-level transcription (2026) · 5. auto-editor · 6. FFmpeg recipes [verified locally on ffmpeg 6.1.1 unless marked; harness `ffmpeg_tests.sh`, log `ffmpeg_tests.log`, all PASS] · 7. ASS subtitles for karaoke and word highlight · 8. Free asset sources and licenses · 9. Other things a top-tier editor skill should include

Research date: 2026-10-11. Environment: Linux sandbox, Node 22.22, ffmpeg 6.1.1 (Ubuntu build with libass, freetype, fontconfig, harfbuzz, fribidi, libvpx, libx264).

**Tags used in this file**
- **[verified locally]**: I ran the command in this session and it worked as described. Logs are in `scratchpad/research/` (`hf-help-1.txt`, `hf-help-2.txt`, `hf-docs.txt`, `ffmpeg_tests.sh`, `ffmpeg_tests.log`).
- **[from source]**: I read it in a cloned repo or a fetched page. The URL is given.
- **[unverified]**: from a secondary source or from memory. Check it before you rely on it.

Network limits in this sandbox:
- `cdn.jsdelivr.net` and `huggingface.co` were blocked by the egress proxy.
- `api.github.com` search was blocked.
- WebFetch DNS failed, so pages were read with Firecrawl.

Because of these limits, model downloads (Whisper, Parakeet) could not be tested locally.

---

## 1. HyperFrames (CLI verification, install needs, gotchas)

The main session is reading the official SKILL.md files, so this section covers only the CLI surface and gotchas.

- **What it is:** HeyGen's HTML-to-video renderer. Repo: https://github.com/heygen-com/hyperframes. License Apache-2.0, `engines.node >=22` (read from the installed `packages/cli` package.json) [verified locally]. Docs index: https://hyperframes.heygen.com/llms.txt.
- **Version tested:** `npx --yes hyperframes@latest` gave v0.8.147 [verified locally].
- **Requirements, from `hyperframes doctor` [verified locally]:**
  - Node 22 or newer
  - FFmpeg and FFprobe on PATH
  - Chrome Headless Shell, installed with `npx hyperframes browser ensure` (a 114 MB download into `~/.cache/hyperframes/chrome/`)
  - Optional: `whisper-cpp` (for `transcribe`), Kokoro (`pip install kokoro-onnx soundfile`), MusicGen
  - Optional: Docker, for `--docker` deterministic renders
  - Low-memory mode switches on automatically at 8 GB RAM or less.

### Composition format (from `hyperframes init demo --non-interactive --example blank --resolution portrait`) [verified locally]

The scaffold writes `index.html`, `hyperframes.json`, `meta.json`, `package.json`, `CLAUDE.md` and `AGENTS.md`. The `package.json` scripts pin `npx --yes hyperframes@0.8.147 preview|check|render|publish`.

```html
<html lang="en" data-resolution="portrait">
<head><meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style> html,body{width:1080px;height:1920px;overflow:hidden;background:#0a0a0a} </style></head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="10"
       data-width="1080" data-height="1920">
    <h1 id="title" class="clip" data-start="0" data-duration="10" data-track-index="0">Title</h1>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.fromTo("#title", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6 }, 0);
    window.__timelines["main"] = tl;   // key MUST equal data-composition-id
    tl.seek(0);
  </script>
</body></html>
```

**Data attributes** (from `hyperframes docs data-attributes`) [verified locally]:

| Group | Attributes |
|---|---|
| Timing | `data-start`, `data-duration` (seconds), `data-track-index` (Studio lane only; the renderer ignores it, and paint order comes from CSS z-index) |
| Media | `data-media-start` (trim offset), `data-volume` (1 = 0 dB, up to 3.98 = +12 dB), `data-fade-in`, `data-fade-out`, `data-has-audio="true"` (silent footage uses `muted`) |
| Composition | `data-composition-id` (required), `data-width`, `data-height`, `data-composition-src="compositions/x.html"` (nested), `data-no-timeline` |
| Variables | `data-composition-variables` (JSON array of `{id,type,label,default}` on `<html>`), `data-variable-values` (JSON object on a sub-comp host), read with `window.__hyperframes.getVariables()` |

**FPS:** taken from the root `data-fps` or `--fps`. The default is 30.

**Rules from the scaffolded CLAUDE.md** [verified locally]:
- Every timed element needs `data-start` and a duration.
- Timed visuals get `class="clip"`.
- Register one paused root timeline per composition on `window.__timelines`. Child timelines added to it must NOT be paused.
- Keep the sound of a video with audio on the `<video>` element. Use a separate `<audio>` for music, voiceover, or J/L cuts.
- No `Date.now()`, no `Math.random()`, no network fetches.

**Determinism** (from `docs/concepts/determinism.mdx` in the repo) [from source]:
- Frame time is computed as `time = floor(frame)/fps`. All GSAP timelines are paused and seeked, never played.
- Frames are captured with `HeadlessExperimental.beginFrame`.
- Use `--docker` to pin Chrome, fonts and FFmpeg.
- Do not call `play()`, `pause()` or set `currentTime` on media.
- Animate a wrapper div, never a `<video>`'s width, height, top or left.

### CLI syntax [verified locally, from `--help`; full text in hf-help-1.txt / hf-help-2.txt]

```
hyperframes init [NAME] [-e|--example blank|warm-grain|swiss-grid|<registry item>] [-v|--video F] [-a|--audio F]
     [--skip-transcribe] [--model small.en] [--language en] [--non-interactive] [--tailwind]
     [--resolution landscape|portrait|landscape-4k|portrait-4k|square|square-4k]
hyperframes render [DIR] [-c|--composition compositions/x.html] [-o out] [-f|--fps 30|30000/1001]
     [-q|--quality draft|looks(default, CRF16)|delivery|standard|high] [--format mp4|webm|mov|gif|png-sequence|hls]
     [--crf N | --video-bitrate 10M] [-w|--workers auto|N] [--docker] [--gpu] [--browser-gpu|--no-browser-gpu]
     [--resolution portrait-4k ...(DPR upscale, same aspect)] [--strict|--strict-all] [--no-best-effort]
     [--variables '{"k":"v"}' | --variables-file f.json] [--batch rows.json] [--video-frame-format auto|jpg|png]
     [--browser-timeout S] [--player-ready-timeout MS] [--low-memory-mode] [--frames-cache-dir DIR] [--hdr|--sdr]
hyperframes snapshot [DIR] [--frames 5] [--at 3.0,10.5] [--no-end] [--zoom '#sel' | x,y,w,h] [--against ref.mp4] [--describe false]
hyperframes check [DIR] [--json] [--samples 9] [--at ...] [--at-transitions] [--strict] [--no-contrast] [--snapshots]
     [--caption-zone "x0=0;y0=.82;x1=1;y1=1;severity=error"] [--frame-check]
hyperframes lint [DIR] [--json] [--verbose]
hyperframes validate [DIR] [--json] [--timeout 3000]      # deprecated → use check
hyperframes inspect  [DIR] ...                           # deprecated → use check
hyperframes beats [DIR] [--json]                          # writes beats/<audio>.json
hyperframes keyframes [TARGET] [--selector S] [--runtime gsap|css|anime|all] [--json] [--shot out.png --samples 9 --layout path|strip]
hyperframes catalog [WORDS] [--type block|component] [--tag captions] [--json]
hyperframes add <NAME|TAG> [--dir D] [--no-clipboard] [--json] [--vars '{...}'] [--force]
hyperframes capture [URL] [-o dir] [--json] [--skip-assets]
hyperframes media-treatment --capabilities | --selector S --grading '<json>' --apply | --analyze | --clear [--dry-run] [--json]
hyperframes transcribe <INPUT> [-e auto|parakeet|whisper] [-m small.en|large-v3] [-l en] [--json] [--to srt|vtt -o out]
hyperframes models install parakeet
hyperframes remove-background IN [-o out.webm|.mov|.png] [-b bg_plate.webm] [--device auto|cpu|coreml|cuda] [--quality fast|balanced|best]
hyperframes normalize-audio [DIR] --target <elementId> [--reference <id> | --lufs -16] [--write]
hyperframes tts "text" [-v af_heart] [-l en-us|hi|...] [-o speech.wav]
hyperframes timeline [DIR] move|trim|split|delete|set|duplicate|ids|apply|undo
hyperframes compositions [DIR] | info | doctor | browser ensure | docs <topic> | skills check|update [names]
```

### Render results for the 3 s portrait demo [verified locally, checked with ffprobe]

| Command | Output |
|---|---|
| `render -q draft -o renders/test.mp4` | h264 **Constrained Baseline**, yuv420p, 1080x1920, 30 fps |
| `render --format webm` | vp9, reported as `yuv420p` but tagged `ALPHA_MODE=1` (alpha present) |
| `render --format mov` | prores **4444**, `yuva444p12le` |

I composited the transparent WebM over a red plate with ffmpeg, and the alpha was correct. You must force the decoder with `-c:v libvpx-vp9 -i overlay.webm`. Without it, the native VP9 decoder drops the alpha channel.

`snapshot --at 0.3,1.0` wrote PNGs plus `contact-sheet.jpg` into `snapshots/`. `check --json` returned lint, runtime, layout, motion and contrast blocks [verified locally].

### Registry

- `catalog --json` lists 446 items [verified locally].
- Most useful for talking-head edits:
  - **Captions:** `caption-highlight` (TikTok-style), `caption-pill-karaoke`, `caption-kinetic-slam`, `caption-emoji-pop`, `caption-editorial-emphasis`, `caption-weight-shift`, `caption-clip-wipe`, `caption-gradient-fill`, `caption-neon-glow`, `caption-parallax-layers`, `mk-callout-highlight`
  - **Lower-thirds:** `lt-*` (12 of them), `yt-lower-third`
  - **YouTube moves:** `yt-camera-move`, `yt-circle-pointer`, `yt-feather-highlight`, `yt-screen-warp`, `yt-vertical-fill`, `push-in`, `parallax-zoom`, `whip-pan-cut`, `zoom-through-transition`
  - **Stats and data:** `count-up`, `chart-story`, `data-chart`, `bar-chart-race`
  - **Hand-drawn:** `hw-*` annotations, `cursor-annotate`, `marker-highlight`
  - **Social cards:** `x-post`, `reddit-post`, `yt-comment-card`
  - **Overlays:** `grain-overlay`, `light-leak`, `beat-accent`, `confetti`, `logo-sting`, `cta-lockup`
- Install with `hyperframes add <name>` or `hyperframes add captions` (installs every item with that tag).

### Gotchas I hit or read

1. **[verified locally] Offline GSAP.** The scaffold loads GSAP from jsDelivr. If that CDN is unreachable, render fails with `sub_timeline_script_failure ... Cannot read properties of null (reading 'timeline')`. The fix is to vendor it: `npm pack gsap@3.14.2`, copy `dist/gsap.min.js` next to `index.html`, and use `<script src="gsap.min.js">`. Vendor fonts the same way, for both determinism and offline use.
2. **[verified locally] Stale example names.** `docs examples` lists a `video-edit` example, but `init --example video-edit` fails with "not found in registry". Examples are now registry item names, and `blank` is the offline-safe choice.
3. **[verified locally] Draft quality.** `-q draft` produced Baseline-profile H.264. Use the default (`looks`, CRF 16) or `delivery` for anything final.
4. **[verified locally] Screenshot fallback.** WebM and MOV renders fell back to "screenshot capture (slower)" because BeginFrame does not run there. `--resolution` upscaling also disables BeginFrame.
5. **[from source]** A composition with no registered timeline waits 45 s (`player-ready-timeout`) on every render. Add `data-no-timeline` to avoid this. Lint reports it as `missing_data_no_timeline`. (Source: `docs/guides/troubleshooting.mdx`.)
6. **[from source]** The root render length is fixed before scripts run. Changing root duration from a variable does nothing, so write `data-duration` explicitly.
7. **[from source]** Local renders can differ by a pixel across machines because of fonts and Chrome versions. Use `--docker` when you need reproducibility. Fonts fail silently and fall back to another face, so video-use asserts with `document.fonts.check('700 76px "Inter"')` (see browser-use/video-use SKILL.md).
8. **[from source]** An agent should start Studio with `npx hyperframes preview --background`, check it with `--status`, and stop it with `--stop`. Do not wrap `npm run dev` in a background shell (scaffold CLAUDE.md).
9. **[unverified, secondary]** A Skool user reports that render quality drops unless the skill is told to keep the source resolution, and that captions still need a manual pass. Source: https://www.skool.com/ai-automation-society/i-built-a-claude-code-skill-that-edits-my-youtube-shorts
10. **No GitHub issue survey.** The GitHub issues API was blocked here. Of the gotchas above, items 5–8 come from the official troubleshooting and determinism docs.

---

## 2. Agent and Claude skills for video editing on GitHub (all cloned and read unless marked)

### Seed sources

- **WeAreNoCode `youtube-edit`.** It is distributed as a zip in the free Skool community, not on GitHub. Setup PDF: https://assets.skool.com/f/a37f7643548a4fc7b7430dd6f2ce6da5/db32d829a30b49a99be1218d9560e202364b526775d0480ba0648f09279034f5 [from source].
  - **Contents:** `youtube-edit/` holds SKILL.md and `scripts/` (cutting, dead-air scan, animation composer, render checks, final assembly) plus `assets/fonts` (DM Sans, OFL). Alongside it are `SETUP.md`, `PROMPTS.md`, a `STYLE-GUIDE.md` with a "Yours" column, and `LICENSES/` (some scripts adapted from an MIT starter kit).
  - **Tool roles:** Parakeet and auto-editor transcribe ("where I speak, every word with its exact time"). HyperFrames animates. Claude-in-Chrome researches. Tella provides screen recordings. Epidemic Sound provides music and SFX. FFmpeg joins and checks.
  - **Learning loop:** watch the whole cut, give timestamped notes, then say "Can you learn from what we did and add it to the skill?" Apply the style guide with "Here's my style guide. Update the youtube-edit skill to match it."
  - **Recording advice:** shoot 4K because "1080p goes soft past about 112%"; pause and repeat a flubbed line ("it keeps your last take of every line"); keep the file flat.
  - **Install:** run in Claude Desktop, Claude Code, Local mode. Claude installs FFmpeg, HyperFrames, auto-editor, Parakeet and runs the tests. Open a new thread afterwards, because skills load at thread start.
- **Luv Sankhla "AI Video Editor".** Nothing was findable on the web or GitHub [unverified]. A skill named `ai-video-editor` is already installed in this environment, matching the description ("7 subtitle styles, HyperFrames, reverse-engineers a creator's style"). The main session can read it directly.

### Repos worth borrowing from

| Repo (license) | What it does | Techniques worth borrowing |
|---|---|---|
| **browser-use/video-use** https://github.com/browser-use/video-use (MIT, about 10k stars) | Edit any video by conversation. Outputs go to `<videos>/edit/`. | **12 hard rules:** subtitles applied LAST, after overlays; per-segment extract then `-c copy` concat; 30 ms `afade` in/out at every boundary; overlays shifted with `setpts=PTS-STARTPTS+T/TB`; SRT offsets in output-timeline time (`word.start - seg_start + seg_offset`); never cut inside a word; pad cuts 30–200 ms; word-level verbatim ASR only; cache transcripts; build animations with parallel sub-agents; confirm the strategy before executing. **Artifacts:** `takes_packed.md` (phrase-level transcript that breaks on silences of 0.5 s or more, about 1/10 the tokens of JSON), `edl.json`, `project.md` session memory. **Helpers:** `timeline_view.py` (filmstrip plus waveform PNG at cut points), self-eval at every cut ±1.5 s, `ebur128` measurement, a "critic sub-agent" that roasts the render, capped at 3 self-eval passes. **Animation timing:** start the overlay `reveal_duration` early so the landing frame hits the spoken payoff word. Use cubic easing, never linear. **Caveat:** it uses paid ElevenLabs Scribe, so swap in a free ASR. |
| **chrislema/videoeditor** https://github.com/chrislema/videoeditor (blog: https://chrislema.com/claude-code-skills-for-video-editing) | Eight markdown skills plus `00-process-video`: remove silence, label sections, produce zoom, correct colors, master audio, add captions, clean artifacts, plus sync-feeds and swap-angles. | **Silence:** `silencedetect=noise=-30dB:d=0.5`, trim gaps to 0.3 s, join with a single-pass `trim/atrim` re-encode (never `-c copy`, which snaps to keyframes and drifts). **Zoom labels:** sections tagged normal, emphasis (1.25x) or critical (1.6x), aimed at a 40/35/25 % split, each 3–7 s. **Face framing:** OpenCV Haar per section, one static crop per section ("don't pan within a section; Haar jitters"), and keep the head top in vertical crops. **Color:** `colorbalance=rs=0.02:gs=-0.01:bs=-0.02,curves=m='0/0 0.25/0.20 0.75/0.82 1/1',eq=brightness=0.02:contrast=1.05:saturation=1.05`. **Audio:** `highpass=f=80,lowpass=f=14000,equalizer=f=3000:t=q:w=1.5:g=3,equalizer=f=200:t=q:w=1.0:g=2,acompressor=threshold=-21dB:ratio=3:attack=5:release=50,volume=0.6,loudnorm=I=-16:TP=-1.5:LRA=11`. **Captions:** whisper.cpp `-ml` for short segments, `drawtext` with a 70 % black box. **Multi-cam sync:** audio cross-correlation. |
| **louisedesadeleer/add-zooms** https://github.com/louisedesadeleer/add-zooms (MIT, Tella) | Transcript-driven punch-zooms with ffmpeg `zoompan`. | **Three moves:** *punch* (1-frame hard cut to 1.18–1.30, hold 0.2–0.5 s, hard cut out), *ratchet* (each list item steps up 1.12 to 1.28), *kenburns* (≤1.14, slow, the only smooth move). Focal point (0.5, 0.42). Peaks of 1.30 or less keep 1080p sharp, and never go past about 1.35. `map.json` holds the events, so you edit and re-render without re-transcribing. The zoompan `z` is a piecewise-linear `if(lte(on,f1),…)` expression, `max()`-combined across events, with `x='iw*cx*(1-1/zoom)'`, `y='ih*cy*(1-1/zoom)'`, `d=1`. |
| **louisedesadeleer/clipify** https://github.com/louisedesadeleer/clipify (MIT) | Long video to 9:16 clips with opus-style captions. | **Speaker-follow 9:16 pan with no ML:** per-ROI motion energy via `crop,format=gray,tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=L.txt`, then a speaker timeline (1 s minimum dwell), then a hard-cut `crop=608:1080:x='EXPR'`. **Captions:** an ASS builder writes one Dialogue per word, highlighting the active word with `\c`. **Action mode:** spectral-flux transient detection in the 1–6 kHz band, cutting about 0.4 s before and 0.5 s after each strike. **Always verify frames** at candidate times before rendering. **Fast trims:** `whisper --model tiny.en --word_timestamps True`. |
| **louisedesadeleer/b-roll-finder** https://github.com/louisedesadeleer/b-roll-finder (MIT) | B-roll sourcing methodology with a `TASTE.md` profile. | **Onboarding gate:** the profile counts as yours only with a literal `Confirmed-by: <name> (<date>)` line. User bans persist into the profile immediately. **Routing:** Receipts (tweets, headlines), Entity (official clip), Concept (motion graphic), Meme (the user supplies it). **Rules:** source the MEANING, not keywords; fetch "by source, not by beat"; the lean path is the default; no retries ("first failure switches, second drops"); a stills Ken Burns of about 1.5 %/s; strip b-roll audio with `-an`. |
| **hassancs91/claude-youtube-editor** https://github.com/hassancs91/claude-youtube-editor (MIT; guide: https://learnwithhasan.com/guide/claude-code-video-editing/) | Nine skills (clean-cut, make-tsx (Remotion), fake-screencast, clean-audio, suggest-sfx, packaging, thumbnail, brand-setup, vidtsx-2d-generator) plus Python tools. | **`tools/verify_cut.py`:** a second ASR pass over the RENDER, diffed against the intended kept words. It flags inserted "ghost" syllables, missing or replaced words, interior gaps of 0.40 s or more, low-confidence words, and **A/V drift** per keep. **Documented bug:** concatenating per-segment AAC built up about 1 s of lip-sync drift (see §6). **clean-audio** matches RMS rather than loudness-normalizing; denoise only; RNNoise as the free local option. **SFX library:** each sound normalized to about -20 LUFS / -1.5 dBFS with catalog metadata, so per-cue gain is meaningful. **Pipeline:** a hard stop for human audit before mixing; one locked title with three thumbnail bets; a compounding asset library ("video ten is cheaper than video one"). Uses paid AssemblyAI, ElevenLabs and Gemini. |
| **agricidaniel/claude-shorts** https://github.com/agricidaniel/claude-shorts (MIT) | Shorts clipper: faster-whisper, Claude segment scoring, `snap_boundaries.py`, Remotion captions, FFmpeg export. | `snap_boundaries.py` snaps to word boundaries, extends to finish a sentence if within 3 s, pads after the last word, and optionally uses silencedetect. `compute_reframe.py` does MediaPipe face tracking with moving-average smoothing. **Its `mp.solutions` API is gone in current mediapipe (§9).** |
| **calesthio/OpenMontage** https://github.com/calesthio/OpenMontage (**AGPL-3.0**, so do not copy code into a closed skill) | Full agentic production system: 13 pipelines including `talking-head.yaml`, many `.claude/skills`, tools. | **Tools:** `auto_reframe.py` (MediaPipe/OpenCV face track, smoothing window, `sendcmd` dynamic crop, center-crop fallback); `silence_cutter.py` (modes remove, speed_up, mark); `transcriber.py` (faster-whisper `word_timestamps=True, vad_filter=True`, int8 on CPU); `subtitle_gen.py` (max words per cue, word corrections dictionary). Free stock adapters: archive_org, coverr, mixkit, nasa, noaa, pexels, pixabay, unsplash, videvo, wikimedia, loc, esa, jaxa. Its "executive-producer" orchestration has checkpoints and a reviewer. |
| **WyattBlue/auto-editor** `skills/` https://github.com/WyattBlue/auto-editor/tree/master/skills | Official agent skills: `auto-editor`, `auto-editor-export`, `auto-editor-transcribe`, `auto-editor-effects`. | Authoritative CLI usage (see §5). |
| **heygen-com/hyperframes** `skills/` | Official skills: `talking-head-recut`, `embedded-captions`, `motion-graphics`, and others. | The main session is reading these. |
| **digitalsamba/claude-code-video-toolkit** https://github.com/digitalsamba/claude-code-video-toolkit | Remotion-centric production workspace. Skills: ffmpeg, moviepy, remotion, remotion-official, playwright-recording, elevenlabs, acestep (music), ltx2, runpod, qwen-edit. | Mostly cloud GPU and paid services, so less relevant for a free, local talking-head editor. |
| Others found but not cloned [unverified] | `Hotclip` (AGPL, local shorts with karaoke, https://claudskills.com/skills/hotclip/); `op7418/youtube-clipper-skill` (bilingual subtitles, https://claudemarketplaces.com/skills/op7418/youtube-clipper-skill/youtube-clipper); `danielmiessler/personal_ai_infrastructure` audioeditor (https://skillselion.com/skills/danielmiessler/personal_ai_infrastructure/audioeditor); `Ceeon/videocut-skills` (Chinese; now a Codex plugin plus runtime, FunASR, not useful here); `affaan-m/ecc` video-editing (https://claudeskills.info/zh/skills/affaan-m/ecc/video-editing/). | |

---

## 3. Remotion vs HyperFrames vs Motion Canvas vs Revideo (for an agent)

**HyperFrames** (Apache-2.0, HeyGen):
- The agent writes plain HTML/CSS with a paused GSAP timeline and `data-*` timing. There is no build step and no React.
- The CLI was built for agents: `lint`, `check --json`, `snapshot` contact sheets, `keyframes --shot` onion skins, and `--caption-zone` checks.
- It renders transparent WebM and ProRes 4444 overlays, and ships a 446-item registry of captions, lower-thirds and transitions. Transcribe, TTS and remove-background are built in.
- Costs: Chrome capture is slower than Remotion Lambda (one reviewer reports about 3 min locally for 30 s at 1080p), and it needs Node 22 or newer.
- Sources: https://github.com/heygen-com/hyperframes, https://moda.app/blog/hyperframes-vs-remotion [secondary], local test.

**Remotion** (React, source-available):
- Free for individuals and companies of up to 3 people. A company license is needed at 4 or more, and an "Automators" tier applies if you build a video tool for others. The license changes in v5.
- Most mature ecosystem: `@remotion/captions`, Lambda/Cloud Run, Player, and official agent skills (`remotion-dev/skills`).
- Best when the user already has a React or Remotion brand kit (hassancs91, claude-shorts and video-toolkit all use it).
- Sources: https://www.remotion.dev/docs/license/faq, https://github.com/remotion-dev/remotion/blob/main/LICENSE.md.

**Motion Canvas** (MIT):
- Generator-function TypeScript with an excellent editor for hand-authored explainers.
- Rendering runs through its editor UI, so it is poorly suited to a headless agent loop.

**Revideo** (MIT fork of Motion Canvas):
- Adds headless `renderVideo()` and API deployment.
- Maintenance activity after 2024 is unclear, with about 3k weekly downloads per a secondary 2026 source [unverified]. Sources: https://docs.re.video/, https://www.pkgpulse.com/guides/remotion-vs-motion-canvas-vs-revideo-programmatic-video-2026.

**Recommendation:** use HyperFrames as the default overlay engine for this skill. Use PIL plus ffmpeg for trivial cards, and Remotion only when the user already has a Remotion kit. video-use picks the engine per slot the same way.

---

## 4. Word-level transcription (2026)

PyPI versions as of today [verified locally with `pip index versions`]: openai-whisper 20250625, faster-whisper 1.2.1, whisperx 3.8.6, mlx-whisper 0.4.3, parakeet-mlx 0.5.3, stable-ts 2.19.1, onnx-asr 0.12.0, nemo_toolkit 3.0.0. Models could not be downloaded here because Hugging Face was blocked, so the commands below come from the READMEs.

| Tool | Install | Word timestamps | Notes |
|---|---|---|---|
| **openai-whisper** | `pip install -U openai-whisper` | `whisper a.wav --model turbo --word_timestamps True --output_format json --language hi` | Reference implementation; slow on CPU; normalizes fillers. Clipify uses `--model tiny.en` for speed and add-zooms uses `small.en`. |
| **faster-whisper** (CTranslate2) | `pip install faster-whisper` | `model.transcribe(p, word_timestamps=True, vad_filter=True)`; `BatchedInferencePipeline`; `WhisperModel("turbo"\|"large-v3"\|"distil-large-v3", device="cpu", compute_type="int8")` | Up to about 4x faster than openai-whisper; CPU int8 is good on Windows. No Apple GPU. Source: SYSTRAN/faster-whisper README. |
| **whisper.cpp** | `brew install whisper-cpp` (Mac), build with cmake, or winget [unverified for Windows] | `whisper-cli -m ggml-large-v3-turbo.bin -f a.wav -l auto -ojf -ml 1 -sow` (`-ojf` gives full JSON with token times; `-ml N` max segment chars; `-sow` split on word; `-wt 0.01` word threshold; `-dtw <model>` for DTW token timestamps; `--vad` with a silero ggml model; `-owts` writes a karaoke script) | Metal on Apple Silicon; Core ML encoder about 3x faster on the ANE. Models live at huggingface.co/ggerganov/whisper.cpp. Flags from `examples/cli/README.md` in ggml-org/whisper.cpp [from source]. **Gotcha (chrislema):** the Homebrew formula no longer ships models, so download to `~/.cache/whisper-cpp/`. |
| **mlx-whisper** (Mac) | `pip install mlx-whisper` | `mlx_whisper a.mp3 --model mlx-community/whisper-large-v3-turbo --word-timestamps True -f json`; Python `mlx_whisper.transcribe(p, path_or_hf_repo=..., word_timestamps=True)` | Fastest Whisper on Apple Silicon. Flags from `ml-explore/mlx-examples/whisper/mlx_whisper/cli.py` [from source]. |
| **WhisperX** | `pip install whisperx` or `uvx whisperx` | `whisperx a.wav --model large-v3 --language hi --compute_type int8 --device cpu --highlight_words True` | wav2vec2 forced alignment gives the most accurate word boundaries. The Hindi align model defaults to `theainerd/Wav2Vec2-large-xlsr-hindi` (also ur, te, and others in `DEFAULT_ALIGN_MODELS_HF`). On Mac use `--device cpu`. Diarization (`--diarize`) needs an HF token. [from source: m-bain/whisperX] |
| **NVIDIA Parakeet TDT 0.6B v3** | Mac: `pip install parakeet-mlx` or `uv tool install parakeet-mlx`. Elsewhere: `hyperframes models install parakeet`, onnx-asr, or NeMo. | `parakeet-mlx a.wav --output-format json` gives sentences with **token**-level `start/end`; merge subword tokens into words. `--highlight-words` adds word timing to SRT/VTT. Options: `--max-words`, `--silence-gap`, `--chunk-duration 120`. | Very fast and accurate English, with **no Whisper hallucinations**. **Languages: 25 European only, no Hindi** (https://build.nvidia.com/nvidia/parakeet-tdt-0_6b/modelcard). HyperFrames `transcribe -e auto` uses Parakeet when it covers the language and falls back to whisper otherwise [verified locally from help]. |
| **auto-editor whisper** | built into auto-editor 31.x | `auto-editor whisper a.mp4 ggml-parakeet-tdt-0.6b-v3-q8_0.bin --format json -sw -o a.json` (or a ggml Whisper model, or `apple` on macOS 26 or later) | One binary does both ASR and cutting. `-sw` gives one word per cue. Parakeet rejects `--language` and `--prompt`. [verified locally: `whisper --help` in 31.7.2; source: auto-editor-transcribe SKILL] |
| **stable-ts** | `pip install -U stable-ts` (`[fw]`, `[mlx]`, `[hf]` extras) | `stable-ts a.mp3 -o a.json` (or `-fw` for faster-whisper, `-mlx`); `result.to_ass('a.ass', word_level=True)` | Stabilized timestamps plus **`model.align(audio, text, language)`, which force-aligns a known script**. That is ideal when the user has a script or wants to correct ASR text and then re-time it. CLI: `stable-ts a.mp3 --align script.txt --language hi`. [from source: jianfch/stable-ts README] |
| **FFmpeg 8 `whisper` filter** | FFmpeg 8.0 or newer built with whisper.cpp | `ffmpeg -i in.mp4 -vn -af "whisper=model=ggml-medium.en.bin:language=en:queue=30:destination=out.srt:format=srt" -f null -` | Supports `vad_model`; json output. Reported slower than whisper-cli [unverified]. Source: https://rendi.dev/blog/ffmpeg-8-0-part-1-using-whisper-for-native-video-transcription-in-ffmpeg |

**Hindi and Hinglish notes:**
- Whisper large-v3 and turbo support Hindi, but often output Devanagari or translate. For Hinglish, set the language explicitly and pass `--initial_prompt` (or auto-editor `--prompt`) with sample romanized Hinglish text.
- **Oriserve/Whisper-Hindi2Hinglish-Apex** (successor to -Prime, Apache-2.0) outputs romanized Hinglish. Model card: https://huggingface.co/Oriserve/Whisper-Hindi2Hinglish-Prime. A CT2 build exists for faster-whisper (https://huggingface.co/Hub84/faster-whisper-hinglish-prime) and a ggml build for whisper.cpp (https://huggingface.co/gouravg8/gtm-hi2hing-ggml) [unverified quality].
- For word timing on Hindi, use WhisperX with the Hindi wav2vec2 aligner, or stable-ts `align()`.
- Parakeet v3 does not cover Hindi. NVIDIA's NIM release notes mention a separate Parakeet 1.1B RNNT multilingual "Indic" model (https://docs.nvidia.com/nim/speech/26.02.0/about/release-notes.html) [unverified for local use].
- **Recommended routing:** detect the language first. English goes to Parakeet (mlx on Mac, onnx or HyperFrames elsewhere). Hindi or Hinglish goes to whisper large-v3-turbo (mlx-whisper on Mac, faster-whisper int8 on Windows), then WhisperX or stable-ts alignment.
- Whatever engine you use, save the verbatim transcript with fillers (video-use rule 8).

---

## 5. auto-editor

- **Versions:** PyPI `auto-editor` is 29.3.1. Its wheel downloads a Nim binary from GitHub releases. GitHub releases are at **31.7.2** (tag list), and `master` CHANGELOG shows 31.7.3. **The CLI differs between them** [verified locally with both binaries].
- **Install:** `pip install auto-editor` gives 29.3.1. Download 31.x from https://github.com/WyattBlue/auto-editor/releases (asset `auto-editor-linux-x86_64`; also macOS and Windows), or use `brew install auto-editor` [unverified version].
- **31.x has a `-k, --license-key` option** that "activates certain features". Which features are gated is [unverified].

### Common syntax [verified locally on 29.3.1 and 31.7.2]

```
auto-editor in.mp4 --edit audio:threshold=0.04 --margin 0.2s -o out.mp4      # defaults: audio:0.04, margin 0.2s
auto-editor in.mp4 --edit audio:-19dB                                          # dB form
auto-editor in.mp4 --margin 0.1s,0.3s                                          # before,after padding (protects word tails)
auto-editor in.mp4 --edit "(or audio:0.04 motion:0.5)"                         # boolean combos need call form
auto-editor in.mp4 --when-silent speed:4                                       # speed through silence instead of cutting
auto-editor in.mp4 --cut-out 0,1sec  /  --add-in 10sec,20sec  /  --set-speed 2,0,30
auto-editor in.mp4 --preview                                                   # stats only, no render
auto-editor info in.mp4    |    auto-editor levels in.mp4  (per-frame loudness dump)
auto-editor in.mp4 --export premiere|resolve|resolve-fcp7|final-cut-pro|shotcut|kdenlive|clip-sequence|v1|v2|v3 -o name
auto-editor in.mp4 --export 'premiere:name="My Timeline"'
auto-editor in.mp4 -anorm ebu  |  -c:v libx264 -b:v 8M
```

- **There is no `--export json`**; it errors with "Unknown export format". The JSON timeline formats are **`v1`** and **`v3`** [verified locally].
  - `v1` = `{"version":"1","source":"in.mp4","chunks":[[startFrame,endFrame,speed],...]}`, where speed 99999 means cut.
  - `v3` = `{"version":"3","timebase":"30/1","resolution":[w,h],"samplerate":…, "v":[[{"src","start","dur","offset","stream"}]], "a":[…]}`.
  - These are the best machine-readable cut lists to feed into your own ffmpeg or HyperFrames assembly.
  - In my test, the 1.2 s silence at 3.0–4.2 s with `-m 0.1s` produced chunks [0,64), cut [64,102), [102,180) at 30 fps.

### 31.x only [verified locally: present in 31.7.2 help, rejected by 29.3.1]

- `--when-active` and `--when-inactive` (aliases `-w:1` and `-w:0`; 29.3.1 uses `--when-normal` and `--when-silent`)
- `-s/--smooth MINCUT,MINCLIP` (default `0.2s,0.1s`)
- `--transition dissolve:DUR[:MIN-CUT]`
- `--cut` and `--keep` (aliases of `--cut-out` and `--add-in`)
- `--set-action ACTION,start,end`
- `-crf`, `-preset`, `-pix_fmt`, `-g`, `--no-partial-lossless`
- `auto-editor whisper <file|:mic> <ggml model> [-sw] [-l en] [-f text|srt|json] [-o F] [--prompt TEXT] [--queue 30] [-t 0.04]`
- Per the official skill [from source]: labels `--edit:N EXPR --when:N ACTION` (N from 2 to 255, higher label wins) and `:mic` input.

### Cutting on word boundaries

auto-editor's loudness edit is threshold-based, so it can clip quiet word onsets and tails. Recommended approach:

1. **Transcript-based keep list (best).** Get word timestamps (§4). Have Claude choose keep ranges by snapping starts to `word.start - 0.05` and ends to `word.end + 0.08` (video-use and claude-shorts padding), never inside a word. Prefer gaps of 0.4 s or more as cut points. Then either render directly with an ffmpeg `trim/atrim` filtergraph, or feed auto-editor manual ranges: `auto-editor in.mp4 --edit 0 --add-in 1.20sec,4.85sec 6.10sec,9.40sec --export v3` (31.x: `--keep`). `--edit 0` means "cut everything not explicitly kept" [from source: auto-editor SKILL].
2. **Subtitle-driven:** `auto-editor whisper talk.mp4 model.bin --format srt -o talk.srt`, then `auto-editor talk.mp4 --edit subtitle` (keeps only lines with speech; the sidecar `talk.srt` is auto-loaded) or `--edit "(not word:um)"` to drop a filler word [from source; 31.x].
3. **Hybrid (WeAreNoCode style):** run auto-editor for the speech/silence map (`--export v3` or `levels`), use Parakeet for the words, then intersect. Extend any auto-editor keep that would split a word out to the word's bounds.

---

## 6. FFmpeg recipes [verified locally on ffmpeg 6.1.1 unless marked; harness `ffmpeg_tests.sh`, log `ffmpeg_tests.log`, all PASS]

```bash
# Frame-accurate cut (re-encode; -ss before -i is accurate when re-encoding)
ffmpeg -ss 1.5 -i in.mp4 -t 2.0 -c:v libx264 -crf 18 -preset veryfast -c:a aac -ar 48000 cut.mp4

# Concat demuxer (identical codec params only), stream copy
printf "file '/abs/a.mp4'\nfile '/abs/b.mp4'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4

# Single-pass trim+concat filter (one audio encode → no AAC drift) with 30 ms de-click fades
ffmpeg -i in.mp4 -filter_complex "\
[0:v]trim=1.5:3.5,setpts=PTS-STARTPTS[v0];[0:a]atrim=1.5:3.5,asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st=1.97:d=0.03[a0];\
[0:v]trim=5:7,setpts=PTS-STARTPTS[v1];[0:a]atrim=5:7,asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st=1.97:d=0.03[a1];\
[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 18 -c:a aac out.mp4
```

**AAC concat drift [verified locally].** Two 2.000 s re-encoded segments joined with the concat demuxer gave **4.0213 s**. The single-pass filter gave **4.000 s**. Each AAC segment adds priming and padding, which accumulates into lip-sync drift (Hassan saw about 1 s on a long video).

To avoid it, use one of these:
- render audio in one filtergraph pass;
- keep intermediate audio as PCM (`-c:a pcm_s16le` in `.mkv`/`.mov`) and encode AAC once at the end;
- concat video-only segments and lay a separately rendered full audio track over them.

```bash
# Crossfade video + audio (offset = dur(first) - transition)
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=1.5,format=yuv420p[v];[0:a][1:a]acrossfade=d=0.5:c1=tri:c2=tri[a]" -map "[v]" -map "[a]" x.mp4

# L-cut (A's audio runs 0.6 s under B's picture); J-cut is the mirror (B's audio starts early)
ffmpeg -i A.mp4 -i B.mp4 -filter_complex "\
[0:v]trim=0:2,setpts=PTS-STARTPTS[va];[1:v]trim=0:3,setpts=PTS-STARTPTS[vb];[va][vb]concat=n=2:v=1:a=0[v];\
[0:a]atrim=0:2.6,asetpts=PTS-STARTPTS,afade=t=out:st=2.45:d=0.15[aa];\
[1:a]atrim=0.6:3,asetpts=PTS-STARTPTS,afade=t=in:d=0.1,adelay=2600|2600[ab];\
[aa][ab]amix=inputs=2:duration=longest:normalize=0[a]" -map "[v]" -map "[a]" lcut.mp4
```

Punch-in zooms. Keep peaks at 1.30x or less on 1080p.

```bash
# (a) eased ramp via scale(eval=frame)+crop
ffmpeg -i in.mp4 -vf "scale=w='iw*(1+0.2*min(1,max(0,(t-1)/0.25)))':h=-2:eval=frame:flags=lanczos,crop=1920:1080:(iw-1920)/2:(ih-1080)/2" z.mp4
# (b) instant hard punch (Tella style) with face-biased y
ffmpeg -i in.mp4 -vf "crop=w='if(between(t,1,3),iw/1.2,iw)':h='if(between(t,1,3),ih/1.2,ih)':x='(iw-ow)/2':y='(ih-oh)*0.42',scale=1920:1080:flags=lanczos,setsar=1" z.mp4
# (c) zoompan Ken Burns on VIDEO input: d=1 and fps/s must match source
ffmpeg -i in.mp4 -vf "zoompan=z='min(1+0.0015*on,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30" z.mp4
```

For smooth eased curves, write the easing into the expression, for example smoothstep `p*p*(3-2*p)` with `p=clip((t-t0)/dur,0,1)`. Alternatively, render the zoom as a GSAP `scale` on a wrapper div in HyperFrames.

Burn in ASS subtitles with libass. Put subtitles LAST, after all overlays.

```bash
ffmpeg -i in.mp4 -vf "subtitles=subs.ass:fontsdir=./fonts" -c:a copy out.mp4
```

The ASS test is in the harness. The `\k` karaoke and the `\t` pop rendered [verified locally, frame inspected]. On Windows, escape the drive colon: `subtitles='C\:/path/subs.ass'` [unverified locally, documented ffmpeg filter-escaping rule: https://ffmpeg.org/ffmpeg-filters.html#Notes-on-filtergraph-escaping].

Overlay a transparent VP9 WebM or ProRes 4444 at time T:

```bash
ffmpeg -i base.mp4 -c:v libvpx-vp9 -i ov.webm -i ov.mov -filter_complex \
"[1:v]setpts=PTS-STARTPTS+1/TB[o1];[2:v]setpts=PTS-STARTPTS+2/TB[o2];\
[0:v][o1]overlay=x=100:y=H-h-100:eof_action=pass[t];[t][o2]overlay=x=W-w-100:y=100:eof_action=pass,format=yuv420p[v]" \
-map "[v]" -map 0:a out.mp4
```

Gotchas, all [verified locally]:
- `-c:v libvpx-vp9` must come before the WebM `-i`, or the alpha is lost.
- Without `eof_action=pass`, overlay repeats the last frame forever.
- `drawbox` on a transparent canvas does NOT write alpha. Build test overlays with `color=red@0.85,format=yuva420p,pad=...:color=black@0`.

```bash
# Encode alpha deliverables
-c:v libvpx-vp9 -pix_fmt yuva420p        # WebM alpha (ffprobe shows yuv420p + ALPHA_MODE=1)
-c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le   # MOV alpha

# Sidechain ducking (music under voice)
ffmpeg -i voice.mp4 -i music.wav -filter_complex "[0:a]asplit=2[vo][key];[1:a]volume=0.5[m];\
[m][key]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300:makeup=1[duck];\
[vo][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]" -map 0:v -map "[a]" -c:v copy -c:a aac out.mp4

# Two-pass loudnorm to -14 LUFS / -1 dBTP (pass 1 prints JSON on stderr)
ffmpeg -i mix.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -
ffmpeg -i mix.mp4 -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=..:measured_TP=..:measured_LRA=..:measured_thresh=..:offset=..:linear=true,aresample=48000" -c:v copy -c:a aac -b:a 192k out.mp4
# measure: ffmpeg -i out.mp4 -af ebur128=peak=true -f null -     → got I: -13.9 LUFS
```

- Use `amix ... normalize=0`, because the default normalization quietly halves levels.
- `loudnorm` upsamples to 192 kHz internally, so always add `aresample=48000`.

```bash
# silencedetect
ffmpeg -i in.mp4 -af silencedetect=noise=-35dB:d=0.4 -f null -   # → silence_start/silence_end lines on stderr

# Scene detection
ffmpeg -i in.mp4 -vf "select='gt(scene,0.3)',metadata=print:file=scenes.txt" -f null -
ffmpeg -i in.mp4 -vf "scdet=threshold=10" -f null -              # newer dedicated filter (lavfi.scd.time)

# Contact sheet, representative thumbnail
ffmpeg -i in.mp4 -vf "fps=1/2,scale=480:-2,tile=4x3:padding=4:margin=4" -frames:v 1 sheet.png
ffmpeg -i in.mp4 -vf "thumbnail=60,scale=640:-2" -frames:v 1 thumb.png

# Dominant colours (8-swatch palette → read pixels)
ffmpeg -i in.mp4 -vf "fps=1,scale=160:-2,palettegen=max_colors=8:reserve_transparent=0:stats_mode=full" -frames:v 1 pal.png
ffmpeg -i pal.png -f rawvideo -pix_fmt rgb24 -  | python3 -c "...unique RGB triplets..."

# Waveform image
ffmpeg -i in.mp4 -filter_complex "aformat=channel_layouts=mono,showwavespic=s=1920x240:colors=0x00E5FF:scale=sqrt" -frames:v 1 wave.png

# QA
ffmpeg -i out.mp4 -vf "blackdetect=d=0.5:pix_th=0.10" -an -f null -        # black_start/black_end
ffmpeg -i out.mp4 -vf "freezedetect=n=-60dB:d=1" -map 0:v -f null -        # freeze_start/duration/end
ffmpeg -i out.mp4 -af astats=measure_overall=Peak_level:measure_perchannel=none -f null -   # clipping check

# 16:9 → 9:16 static face-centred crop, and blurred-background fit
ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih:x='min(max(FACE_X-ow/2,0),iw-ow)':y=0,scale=1080:1920:flags=lanczos,setsar=1" v.mp4
ffmpeg -i in.mp4 -filter_complex "[0:v]split[bg][fg];[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:5,eq=brightness=-0.08[b];[fg]scale=1080:-2[f];[b][f]overlay=(W-w)/2:(H-h)/2,setsar=1[v]" -map "[v]" -map 0:a v.mp4

# Free voice cleanup (no ML)
-af "highpass=f=80,afftdn=nr=12:nf=-40,deesser,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2"
```

- **Platform note [from source: chrislema/videoeditor README].** Older Homebrew `ffmpeg` builds lack `drawtext`, and `brew install ffmpeg-full` has it. Always probe first with `ffmpeg -hide_banner -filters | grep -E " (subtitles|ass|drawtext|zoompan|xfade|sidechaincompress|loudnorm) "`. Whether current Homebrew ffmpeg includes libass is [unverified].
- **Windows** [unverified]: `winget install Gyan.FFmpeg` (full build includes libass and libvpx).

---

## 7. ASS subtitles for karaoke and word highlight

Reference: Aegisub override tags, https://aegisub.org/docs/latest/ass_tags/. Rendering confirmed with libass [verified locally].

**[Script Info]**
- `PlayResX`/`PlayResY` define the coordinate space. Set them to the output resolution (1080x1920 for Shorts) so font sizes and margins are in real pixels.
- `ScaledBorderAndShadow: yes`
- `WrapStyle: 2` (no auto-wrap; you control line breaks with `\N`)

**Style line order:** `Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold(-1/0), Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle(1=outline+shadow, 3=opaque box), Outline, Shadow, Alignment(numpad 1–9; 2=bottom-centre, 5=middle, 8=top), MarginL, MarginR, MarginV, Encoding`.

**Colours:**
- Colours are `&HAABBGGRR`, in **BGR order**, with alpha 00 = opaque and FF = invisible. Yellow is `&H0000FFFF`, and the accent in my test was `&H0000E5FF`.
- Inline: `\c&HBBGGRR&` or `\1c` for fill, `\3c` for outline, `\4c` for shadow.
- `\alpha&H80&`, `\1a`, `\3a`

**Karaoke tags:**
- `{\kNN}`: syllable timing in **centiseconds**. Unsung text shows SecondaryColour and switches to PrimaryColour instantly.
- `\kf` (or `\K`): sweep fill left to right.
- `\ko`: outline-only.

**Pop and animation tags:**
- `\t(t1,t2,[accel,]tags)`: times in ms relative to the line start. Example pop: `{\fscx80\fscy80\t(0,120,\fscx110\fscy110)\t(120,200,\fscx100\fscy100)}`
- `\fad(in,out)`, `\move(x1,y1,x2,y2,t1,t2)`, `\pos(x,y)`, `\an5`, `\org`
- `\bord6`, `\shad2`, `\blur2` or `\be1` (soft outline), `\fs`, `\fn`, `\b1`, `\frz` (rotation)

**Two word-highlight patterns:**
1. **One Dialogue per word.** Re-emit the whole chunk each time, coloring the active word with `\c` and optionally `\t`-scaling it (clipify `build_ass.py`). This is most robust and allows a per-word scale pop and background-box highlight.
2. **One Dialogue per chunk with `\k`.** Smaller file, but limited to a colour switch or sweep.

Chunking rules (video-use): 2–3 words, uppercase for Shorts, break on punctuation or pauses of 0.3 s or more, never flash a cue shorter than 0.35 s, `MarginV` about 35 px at 1080p or a larger ratio for 9:16, and keep the bottom 20 % clear of platform UI. stable-ts can emit word-level ASS directly with `result.to_ass(..., word_level=True)`.

**HTML caption alternative (HyperFrames):**
- Install a caption component (`hyperframes add caption-highlight` / `caption-pill-karaoke` / `caption-kinetic-slam` …) or write spans timed from `transcript.json` (`hyperframes transcribe` writes word-level timestamps into the project).
- Render as a **transparent WebM or MOV** and overlay LAST with ffmpeg, or render the whole edit inside HyperFrames with the `<video>` as the base layer.
- Benefits: web fonts, gradients, emoji, blur and layout that ASS cannot do. `check --caption-zone "x0=0;y0=.82;x1=1;y1=1;severity=error"` QA's caption placement against overlap.
- Cost: a slower render than libass.

---

## 8. Free asset sources and licenses

| Type | Source | License summary | Source URL |
|---|---|---|---|
| Fonts | Google Fonts | Mostly SIL OFL 1.1 (some Apache-2.0). Free commercial use, embedding and bundling allowed; cannot sell the font alone. DM Sans is OFL (used by WeAreNoCode). | https://fonts.google.com/knowledge ; WeAreNoCode PDF above |
| Fonts | Fontshare (Indian Type Foundry) | "ITF Free Font License": free for personal and commercial use [unverified in session; the license page did not render] | https://www.fontshare.com/licenses |
| Fonts | Velvetyne | Libre fonts, mostly SIL OFL [unverified per font; check each] | https://velvetyne.fr |
| SFX | Freesound | Per-sound CC0, CC-BY (credit required) or CC-BY-NC (no monetized use). Filter for CC0 [unverified in session] | https://freesound.org/help/faq/ |
| SFX, music, video | Pixabay | Free, no attribution, may modify. Cannot redistribute standalone. No commercial use of recognisable trademarks or brands. [from source] **Content ID risk:** some uploads are fingerprinted, so keep the license certificate [secondary] | https://pixabay.com/service/license-summary/ ; https://www.foximusic.com/blog/?p=10 |
| SFX, music, video | Mixkit | SFX free for commercial and personal use, no attribution. Stock Music Free License excludes broadcast, CD and games uses [secondary] | https://mixkit.co/llm-info/ ; https://kripeshadwani.com/mixkit-review/ |
| Music | YouTube Audio Library (YouTube Studio) | Free; tracks downloaded there are not Content-ID claimed. Some tracks require attribution (check the per-track label) [secondary] | https://www.foximusic.com/blog/?p=546 |
| Music | Uppbeat free tier | 3 downloads (one restored per month) with partial catalogue access. Free users must paste the credit into each video's description; the safelist is paid only. | https://uppbeat.io/pricing |
| Stock video | Pexels | Free commercial use, no attribution, cannot sell unaltered copies [unverified in session]. Free API key. | https://www.pexels.com/license/ |
| Stock video | Coverr | Free commercial use, no attribution. No resale, no competing service, **no AI training use** [from source] | https://coverr.co/license |
| Icons | Lucide | ISC [from source: LICENSE] | https://github.com/lucide-icons/lucide |
| Icons | Phosphor | MIT [from source] | https://github.com/phosphor-icons/core |
| Icons | Iconify | Aggregator; the license is per icon set (MIT, Apache, CC-BY…), so check the `license` field in each set's JSON [unverified] | https://iconify.design |
| Lottie | LottieFiles free animations | Lottie Simple License: free personal and commercial use, attribution not required; cannot redistribute or resell standalone files [secondary/help-centre] | https://help.lottiefiles.com/hc/en-us/articles/900002438343 |
| UI for graphics | shadcn/ui | MIT [from source] | https://github.com/shadcn-ui/ui |
| UI for graphics | Magic UI | MIT [from source] | https://github.com/magicuidesign/magicui |
| UI for graphics | React Bits | **MIT + Commons Clause** (free use, cannot sell the components themselves) [from source: LICENSE.md] | https://github.com/DavidHDev/react-bits |
| UI for graphics | Aceternity UI | The licence page covers Pro (end products include videos). Free-component terms were not stated on that page [from source, partial] | https://ui.aceternity.com/licence |
| UI for graphics | Motion Primitives (ibelick) | MIT per the repo [unverified; the LICENSE path 404'd] | https://github.com/ibelick/motion-primitives |

**Important for porting React UI kits to HyperFrames:** these libraries animate with Framer Motion or CSS on wall-clock time. HyperFrames needs seekable, paused GSAP timelines and no `Date.now`/rAF, so treat them as visual design references and re-implement the motion in GSAP. HyperFrames ships `/remotion-to-hyperframes` and a `gsap` doc for this.

---

## 9. Other things a top-tier editor skill should include

- **Face detection, with a breaking change [verified locally].**
  - `mediapipe` on PyPI is now **1.1.0**, and its wheel contains **no `mediapipe/python/solutions/` at all**. Code using `mp.solutions.face_detection` (OpenMontage `face_tracker.py`, claude-shorts `compute_reframe.py`) fails on a fresh install.
  - Use the Tasks API instead: `mediapipe.tasks.python.vision.FaceDetector`, with a `blaze_face_short_range.tflite` model file (present in the wheel), or `FaceLandmarker`.
  - Alternatives that need no model download: OpenCV Haar (`cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'`, ships with opencv-python, used by chrislema) or OpenCV YuNet (`cv2.FaceDetectorYN`, model from opencv_zoo).
  - Sample at about 5 fps.
- **Caption placement:** detect the face box per section, then put captions in the band that avoids it. Typical spots are the lower-third band in 16:9 and about 65–75 % height in 9:16, above the Shorts UI. Verify with `hyperframes check --caption-zone`.
- **Auto-reframe 16:9 to 9:16:**
  - Use one static crop per section or sentence and cut at section boundaries rather than tracking every frame (chrislema).
  - If panning, smooth the face-x with a moving average or EMA and change crop x through `sendcmd` or a piecewise `crop` x-expression (OpenMontage, clipify).
  - Never crop off the top of the head: keep the face at about 30 % from the top.
  - For two speakers, use ROI motion-energy speaker detection (clipify) or a split-screen stack.
- **B-roll retrieval:** Pexels and Pixabay APIs (free keys), plus OpenMontage's adapter list (archive.org, NASA, Wikimedia, LoC, Coverr, Mixkit). Follow b-roll-finder's method: classify each beat as Receipts, Entity, Concept or Meme; source the meaning; strip audio; apply a subtle Ken Burns on stills.
- **yt-dlp** (2026.08.19) [verified locally: flags present in `--help`]:
  - `yt-dlp -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 -o "%(title)s.%(ext)s" URL`
  - `--download-sections "*00:01:00-00:02:00" --force-keyframes-at-cuts`
  - `--write-auto-subs --sub-langs "en.*,hi" --skip-download --convert-subs srt`
  - `--cookies-from-browser chrome`, `--write-info-json`
  - The new `--js-runtimes` option: YouTube extraction now needs a JS runtime such as Deno [unverified detail].
- **Beat detection [verified locally, librosa 1.0.0]:**
  - `tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')` and `librosa.onset.onset_detect(y=y, sr=sr, units='time')`.
  - Gotcha: `tempo` comes back as an ndarray (`[117.45]`), so use `float(np.atleast_1d(tempo)[0])`. With `trim=True` (the default) the first beat can be dropped.
  - HyperFrames also has `hyperframes beats` (writes `beats/<audio>.json`).
- **Denoise and voice:**
  - DeepFilterNet prebuilt binary: `deep-filter -D -o outdir in_48k.wav`. **It accepts 48 kHz WAV only**, and **use `-D/--compensate-delay` or A/V sync shifts**. Python route: `pip install torch torchaudio` then `pip install deepfilternet`, then `deepFilter in.wav -o out/ [--pf]` [from source: Rikorose/DeepFilterNet README].
  - FFmpeg `arnndn=m=model.rnnn` (RNNoise; needs a model from GregorR/rnnoise-models) or `afftdn` (present in this build).
  - Match RMS after denoising rather than loudness-normalizing; master once at the end (hassancs91).
- **Background removal:** `hyperframes remove-background in.mp4 -o subject.webm [-b plate.webm]` gives a transparent subject for "text behind the speaker" [verified locally: help only]. `rembg` 2.0.85 is image-focused: `pip install "rembg[cpu,cli]"`, then `rembg i in.png out.png` / `rembg p indir outdir` [unverified locally].
- **Eye contact:** I found no free, offline, open-source tool for recorded video. NVIDIA Broadcast Eye Contact (Windows with RTX GPU, free) and Apple's FaceTime eye contact (live only) are the practical options [unverified]. Recommend "look at the lens" coaching instead.
- **QA loop worth copying:**
  1. `ffprobe` duration against the EDL.
  2. `ebur128` integrated loudness and true peak, plus per-section RMS.
  3. A filmstrip and waveform at every cut ±1.5 s (video-use `timeline_view`).
  4. A second ASR pass over the render, diffed against the kept words, with an A/V drift check (hassancs91 `verify_cut.py`).
  5. blackdetect and freezedetect.
  6. HyperFrames `check --json` and a `snapshot` contact sheet.
  7. A critic sub-agent for anything the user will publish.
  8. Cap the passes at 3.
- **Memory and learning:**
  - `edit/project.md` session log (video-use)
  - `TASTE.md` with a `Confirmed-by:` gate, and bans persisted immediately (b-roll-finder)
  - "Can you learn from what we did and add it to the skill?" (WeAreNoCode)
  - A STYLE-GUIDE with a "Yours" column (WeAreNoCode)
  - A compounding SFX and component library with loudness metadata (hassancs91)
- **Taste defaults collected:**
  - Pad cuts 50 ms before and 80 ms after.
  - Prefer silences of 0.4 s or more as cut points; under 0.15 s is unsafe.
  - Use 0.4–0.6 s of air at speaker handoffs.
  - Punch zooms 1.18–1.30 as hard cuts; Ken Burns at most 1.14; focal y 0.42.
  - Use no more than about 8 SFX per 18 s, each tied to a visible event and started `attack` seconds early.
  - Duck music 12–15 dB under speech.
  - Master to -14 LUFS / -1 dBTP.
  - Hold the final frame of an animation for at least 1 s.
  - Show one new element at a time.
