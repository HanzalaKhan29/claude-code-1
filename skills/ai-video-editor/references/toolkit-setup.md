# Toolkit setup and troubleshooting

## Where to run this skill

| Surface | Works? | Notes |
|---|---|---|
| **Claude Desktop, Code tab, Local** (or Claude Code CLI) | Full workflow | Files stay on the user's machine; ffmpeg, Node, Python and Chrome run locally. Recommended. Permissions on "Auto" (or accept edits) avoids hundreds of prompts during renders. |
| **Claude Desktop, Cowork** | Full workflow | Runs on the user's computer; same tools. |
| **Claude.ai chat / Desktop chat with code execution** | Partial | Sandbox: no persistent folder, restricted network (model and font downloads may fail), usually no ffmpeg/Chrome. Use it for planning, style cards, caption files from uploaded transcripts. Say so plainly. |

Installing the skill:
- Code tab / Claude Code: put the `ai-video-editor` folder in `~/.claude/skills/` (all projects) or `<project>/.claude/skills/` (one project). Open a **new thread**: skills load when a thread starts.
- Claude.ai / Desktop chat: Settings, Capabilities, Skills, upload the `.zip` (the folder zipped, SKILL.md at its root).
- Recommended project folder: something like `Video Editing/`, then each video in `video-edits/<project>/`.

## Step 1: check

```bash
python3 scripts/doctor.py          # Windows: python scripts\doctor.py
```

Install only what is missing, after the user says yes. One line of "why" per tool.

## Step 2: install by OS

| Tool | Why | macOS | Windows | Linux |
|---|---|---|---|---|
| ffmpeg + ffprobe | cutting, audio, export, QA | `brew install ffmpeg` | `winget install --id Gyan.FFmpeg -e` (full build, has libass + libvpx) | `sudo apt-get install -y ffmpeg` |
| Python 3.10+ | runs the scripts (standard library only) | preinstalled or `brew install python` | `winget install Python.Python.3.12` | preinstalled |
| Node.js 22+ | HyperFrames | `brew install node@22` | `winget install OpenJS.NodeJS.LTS` | nvm: `nvm install 22` |
| HyperFrames | HTML to video motion graphics | `npx hyperframes@latest doctor`, then `npx hyperframes browser ensure` | same | same |
| HyperFrames skills | official composition workflows | `npx hyperframes skills update` | same | same |
| Remotion (optional, per project) | React motion graphics with frame-level control | `cp -r assets/remotion <project>/work/remotion && cd <project>/work/remotion && npm install` (no global install; first render downloads Chrome Headless Shell) | same | same |
| Transcription (one is enough) | word timestamps | `python3 -m pip install mlx-whisper` (Apple Silicon, fastest) | `python -m pip install faster-whisper` | `python3 -m pip install faster-whisper` |
| yt-dlp (optional) | download reference videos | `brew install yt-dlp` | `winget install yt-dlp.yt-dlp` | `python3 -m pip install -U yt-dlp` |
| opencv-python (optional) | face share in style analysis, face-centred reframe | `python3 -m pip install opencv-python` | same with `python` | same |
| DeepFilterNet (optional) | heavy voice denoise | prebuilt `deep-filter` binary from GitHub releases, or `pip install torch torchaudio deepfilternet` | same | same |
| rembg (optional) | background removal for stills | `python3 -m pip install "rembg[cpu,cli]"` | same | same |

Notes:
- Homebrew ffmpeg: check filters with `ffmpeg -hide_banner -filters | grep -E " (subtitles|ass|drawtext|zoompan|sidechaincompress|loudnorm) "`. If `subtitles` is missing, `brew install ffmpeg-full` (or the tap that bundles libass).
- Transcription on a GPU machine with a broken CUDA/cuDNN install: `transcribe.py` tries the GPU in a child process and falls back to CPU int8 on a crash. Pass `--device cpu` to skip the attempt.
- Remotion licence: free for individuals, for-profit companies with up to 3 employees and non-profits; larger companies need a Company License (remotion.pro). HyperFrames is Apache-2.0.
- Whisper models download on first use (hundreds of MB from Hugging Face). Corporate networks may block it; `transcribe.py` then falls back to `npx hyperframes transcribe` and finally reports every engine's error.
- Model choice: `large-v3-turbo` for most work; `small` for quick drafts; `large-v3` for Hindi and accented speech. Parakeet (via `npx hyperframes transcribe -e parakeet` or `parakeet-mlx`) is very fast and accurate for English and European languages but has no Hindi.
- auto-editor is optional. Note that PyPI ships 29.x while GitHub releases are 31.x with different flags (`--when-silent` vs `--when-inactive`); there is no `--export json` (use `--export v3`). This skill's `plan_cuts.py` does transcript-aware cutting without it.

## Step 3: tiny test (prove it works before a real edit)

```bash
python3 scripts/probe.py <their clip>
ffmpeg -ss 0 -t 5 -i <their clip> -c:v libx264 -crf 20 -c:a aac work/test5s.mp4
python3 scripts/qa.py work/test5s.mp4 --out work/qa-test
```
Show the user the 5 s file and the QA lines. For HyperFrames: `npx hyperframes init test --non-interactive --example blank`, copy `gsap.min.js` in if offline, `npx hyperframes render test -o test.mp4`.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| HyperFrames render: `Cannot read properties of null (reading 'timeline')` | GSAP CDN blocked | vendor `gsap.min.js` next to `index.html` |
| Render extremely slow / times out on Mac | software Chrome rendering | `PRODUCER_BROWSER_GPU_MODE=hardware` or `--browser-gpu`; fewer `--workers` on 8 GB machines |
| Render waits 45 s then works | composition without a timeline | add `data-no-timeline` to the root |
| Video freezes under graphics | sparse source keyframes | re-encode with `-g <fps> -keyint_min <fps>` (probe.py prints the command) |
| Wrong font in render, no error | font not found, fallback used | local `@font-face` with the real file; for libass pass `--fonts` folder; check with `fc-scan` |
| Transparent WebM has a black background after compositing | native VP9 decoder drops alpha | decode with `-c:v libvpx-vp9` before the `-i` (overlay.py does this) or use ProRes 4444 `.mov` |
| Captions out of sync after cutting | captions made from the raw transcript | use `work/words_cut.json`; re-run plan_cuts after any EDL change |
| Lip-sync drift on long edits | per-chunk AAC joins | render_cut.py renders audio in one pass; re-render with the current version |
| Whisper text where nobody speaks | hallucination over silence | delete those words from words.json; consider `--verbatim` and checking low-confidence words |
| Hindi comes out translated to English | auto language detection | `--language hi`; for romanized output see captions.md section 8 |
| Washed-out colours after export | HDR source or missing colour tags | probe.py warns on HDR; tone-map first; our encodes tag BT.709 |
| Windows: subtitles filter fails on path | drive-letter colon in filtergraph | captions.py escapes it; if hand-writing, use `subtitles='C\:/path/subs.ass'` |
| yt-dlp: "Sign in to confirm" or extraction errors | YouTube changes | `yt-dlp -U`; `--cookies-from-browser chrome`; or ask the user for the file |
