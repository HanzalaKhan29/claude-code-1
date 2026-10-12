# Install and first run (for you, the human)

## Install in Claude Desktop

**Recommended: Code tab (Local) or Cowork.** Full editing needs your computer's ffmpeg, Node and Python.

1. Claude Desktop, open the Code tab, choose **Local**, pick a folder (for example `Video Editing`), permissions on Auto, latest model.
2. Put this `ai-video-editor` folder in `~/.claude/skills/` (every project) or `Video Editing/.claude/skills/` (this project only). Or type: "Install the ai-video-editor skill from <path> into ~/.claude/skills".
3. Start a **new thread** (skills load when a thread starts).
4. Type: **"Set up video editing."** Claude runs `scripts/doctor.py`, shows what is missing (ffmpeg, Node 22, a Whisper engine, HyperFrames), and installs it after you say yes. Then it runs a 5-second test on your clip.

**Chat with skills (claude.ai / Desktop chat):** Settings, Capabilities, Skills, upload `ai-video-editor.zip`. The chat sandbox has no ffmpeg/Chrome and limited network, so use it for planning, style cards and caption files; do real edits in the Code tab.

## Prompts that work

- "Edit this video for YouTube: `raw/take1.mp4`. Style like <creator> (links). Captions style 5."
- "Cut the ums, retakes and dead air from `raw.mp4` and show me the cut list first."
- "Make a vertical Short from 2:10 to 2:55 of `podcast.mp4` with viral captions."
- "Break down the editing style of these 3 videos and write me a style card."
- "Make a 6-second animated stat card: 'from 1,200 to 48,000 subscribers'. Look 20, transparent background."
- "Make a 30-second motion-graphics reel like @metromedia.house from my voiceover `vo.mp3`. Storyboard it first."
- "Calm explainer for LinkedIn, no texture, clean captions. Build the graphics in Remotion."
- "Same edit, 3 hook variants for ads: one Remotion template, different props."
- "Here's my channel <URL>. Find my top 10 edits and tell me what my style actually is."
- "Grade `broll/` to match my talking-head footage and give me the look as a LUT."
- "Edit this UGC ad into 12 hook variants; the avatar is AI, handle the disclosure."
- Notes after watching: "At 0:22 the caption covers my mouth. At 0:41 the zoom is too strong. Too many sound effects."
- After every round: **"Can you learn from what we did and add it to the skill?"**

## Record so it edits well

4K if you can (zooms stay sharp), flat footage (no baked-in zooms or captions), pause and repeat a flubbed line (the editor keeps the last take), 5 seconds of room tone at the start, constant frame rate.

## Credits

Built on Luv Sankhla's AI Video Editor skill, WeAreNoCode's YouTube-editor workflow and 20 Looks, HeyGen HyperFrames (Apache-2.0) skills, Tella's open-source zoom and b-roll skills, browser-use/video-use, and sourced design and attention research (see `references/`). Fonts are downloaded from Google Fonts (OFL) at use time; no music, footage or logos are included.
