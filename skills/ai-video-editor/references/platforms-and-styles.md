# Delivery Specs, Safe Zones, Creator Editing Styles, Retention Principles

Contents: PART A: Export specs per platform · PART B: Safe zones for vertical video (1080x1920) · PART C: Creator editing-style breakdowns · PART D: Retention-backed principles (evidence vs opinion) · Source-confidence summary

Research reference for an AI video-editor skill. Compiled 2026-10-11.

**Confidence labels used throughout**
- **[OFFICIAL]**: quoted or paraphrased from the platform's own help or docs page, fetched this session (2026-10-11).
- **[OFFICIAL-snippet]**: official page, but I only saw a search-engine excerpt, not the full page.
- **[3RD-PARTY]**: reputable secondary source (press, tool vendor, educator). Not confirmed by the platform.
- **[UNVERIFIED]**: folk wisdom, my own background knowledge, or sources that disagree. Do not present as fact.
- **[OBSERVED, UNMEASURED]**: qualitative description of a style. No published measurement exists.

All fetched web content was treated as untrusted data.

---

## PART A: Export specs per platform

### A1. YouTube long-form: official recommended upload encoding [OFFICIAL]
Source: https://support.google.com/youtube/answer/1722171?hl=en

| Item | YouTube recommendation |
|---|---|
| Container | MP4. No edit lists. moov atom at the front of the file ("Fast Start"). |
| Video codec | H.264, progressive (no interlacing), **High Profile**, 2 consecutive B-frames, **closed GOP, GOP of half the frame rate**, CABAC, VBR (no bitrate limit required), chroma subsampling **4:2:0**. |
| Audio codec | AAC-LC, Opus, or Eclipsa Audio. Channels: Stereo, or Stereo + 5.1, or Stereo + Eclipsa. **Sample rate 48 kHz.** |
| Audio bitrate | Mono 128 kbps · **Stereo 384 kbps** · 5.1 512 kbps (Eclipsa: 128 kbps per channel). |
| Frame rate | Encode at the recorded frame rate. Common: 24, 25, 30, 48, 50, 60 (others accepted). Deinterlace interlaced sources (1080i60 becomes 1080p30). |
| Aspect | 16:9 standard on desktop. The player adapts to vertical or square. |
| SDR color | **BT.709** primaries, transfer and matrix (H.273 value 1). An unspecified TRC or matrix is assumed to be BT.709. Full range is converted to limited range. The RGB matrix is not recommended. BT.2020 without an HDR transfer is converted to 8-bit BT.709. |

**Recommended SDR video bitrates [OFFICIAL]**

| Resolution | 24/25/30 fps | 48/50/60 fps |
|---|---|---|
| 8K | 80–160 Mbps | 120–240 Mbps |
| 2160p (4K) | 35–45 Mbps | 53–68 Mbps |
| 1440p | 16 Mbps | 24 Mbps |
| 1080p | 8 Mbps | 12 Mbps |
| 720p | 5 Mbps | 7.5 Mbps |
| 480p | 2.5 Mbps | 4 Mbps |
| 360p | 1 Mbps | 1.5 Mbps |

**HDR bitrates [OFFICIAL]:** 4K 44–56 Mbps (SFR) and 66–85 Mbps (HFR). 1440p 20/30. 1080p 10/15. 720p 6.5/9.5. HDR is not supported at 480p or 360p.

**HDR requirements [OFFICIAL]** (https://support.google.com/youtube/answer/7126552?hl=en):
- Transfer function PQ or HLG (Rec. 2100), Rec. 2020 primaries, Rec. 2020 non-constant-luminance matrix, 10- or 12-bit.
- Recommended codecs: VP9 Profile 2, AV1, or HEVC. ProRes, DNxHR and 10-bit H.264 also work but need very high bitrates. Tested containers: MOV, MP4, MKV.
- PQ uploads should carry SMPTE ST 2086 mastering metadata plus MaxFALL and MaxCLL. If these are missing, YouTube assumes a Sony BVM-X300 display. HDR10+ dynamic metadata is optional.
- SDR down-conversion is automatic. You can supply a .cube LUT to guide it.
- **Practical rule:** creators should deliver SDR BT.709 unless they truly mastered in HDR. A phone HLG or HDR clip graded carelessly will look wrong on SDR screens.

### A2. YouTube Shorts [OFFICIAL]
Source: https://support.google.com/youtube/answer/15424877?hl=en
- **Max length: 3 minutes.** Any square or vertical upload of 3 minutes or less, uploaded on or after 2024-10-15, is classified as a Short. For Official Artist Channels this applies from 2025-12-08.
- To avoid Shorts classification, use a wider aspect ratio such as 16:9.
- **A Short over 1 minute with any active Content ID claim is blocked globally.** Shorts under 1 minute are unchanged.
- Shorts Audio Library: most songs can be used for up to 90 s in a 3-minute Short. Some are limited to 60 or 30 s.
- Resolution: YouTube publishes no Shorts-specific resolution. Use **1080x1920 (9:16)** with the same encoding rules as long-form. [UNVERIFIED as an official number; it is the universal practice]
- Shorts view counting changed on 2025-03-31: a view now counts when playback starts or replays, with no minimum watch time. [3RD-PARTY: https://www.bytecap.io/research/youtube-shorts-retention-benchmarks, https://1of10.com/blog/youtube-shorts-analytics/]

### A3. Instagram Reels
- **Length:** you can record or edit Reels up to **20 minutes**, but "Reels over 3 minutes won't be recommended to new audiences." [OFFICIAL-snippet: https://help.instagram.com/2720958398006062/]
- **Aspect:** between 1.91:1 and 9:16. **Minimum 30 fps, minimum 720 px resolution.** [OFFICIAL: https://help.instagram.com/1038071743007909]
- **Boosting a Reel** requires 90 s or less, 9:16, and no licensed music. [OFFICIAL-snippet: https://help.instagram.com/570215404599013/]
- **Reels ad specs (Meta Ads Guide)** [OFFICIAL: https://www.facebook.com/business/ads-guide/update/video/instagram-reels]:
  - MP4 or MOV, 9:16, **recommended 1440x2560**.
  - H.264, square pixels, fixed frame rate, progressive, **stereo AAC 128 kbps+**.
  - 0 s to 15 min, max 4 GB.
- **Practical delivery:** 1080x1920, H.264 High, 30 fps (or native 24/25/60), constant frame rate, AAC 48 kHz. Instagram recompresses heavily. Uploading a cleaner, higher-bitrate file (12–20 Mbps at 1080p) and enabling "Upload at highest quality" in the app helps. [UNVERIFIED practice]
- Feed grid preview crops Reels to the centre. Keep the cover's key content in the middle of the frame. [UNVERIFIED exact ratio. Instagram changed the grid to 3:4 in 2025 per press reports, but I did not confirm this officially.]

### A4. TikTok
- **Length:** videos recorded in TikTok can be up to **10 min**. Videos uploaded in TikTok can be up to **60 min**. [OFFICIAL-snippet: https://support.tiktok.com/en/using-tiktok/creating-videos/camera-tools]
- **TikTok Studio (web) upload rules:** MP4 or WebM, **720x1280 or higher**, **up to 30 min**, under 10 GB. [OFFICIAL: https://support.tiktok.com/en/using-tiktok/creating-videos/creator-tools-on-tiktok, which redirects to tiktok.com/support/faq_detail?id=7581820704895703564]
  - Note the conflict: the in-app limit is 60 min, the web Studio page says 30 min. Treat 30 min as the safe cross-surface limit.
- **Series** videos run from 30 s to 20 min. [OFFICIAL-snippet: https://support.tiktok.com/en/business-and-creator/tiktok-series/create-and-manage-series]
- **In-Feed ad specs** [OFFICIAL: https://ads.tiktok.com/help/article/video-ads-specifications]:
  - 9:16 recommended, at least 540x960. Also .mp4, .mov, .mpeg, .3gp, .avi.
  - Up to 10 min, 500 MB or less, **bitrate 516 kbps or more**.
  - Ad caption up to 4 lines.
  - Safe zones come as downloadable template files only (no numbers in the text).
- **Practical delivery:** 1080x1920, H.264 High, 30 or 60 fps CFR, AAC 48 kHz, 10–20 Mbps. [UNVERIFIED practice]

### A5. LinkedIn video
- **LinkedIn Pages** [OFFICIAL-snippet: https://www.linkedin.com/help/linkedin/answer/a1311816]: 75 KB to 5 GB, **3 s to 10 min**, resolution 256x144 to 4096x2304.
- **Member posts** [OFFICIAL-snippet: https://www.linkedin.com/help/linkedin/answer/a7174587 and a548372]: minimum 3 s on desktop or 2 s on mobile, resolution 256x144 to 4096x2304.
  - Max duration is **15 min on desktop and 10 min on mobile** per a third-party source [3RD-PARTY: https://www.descript.com/blog/article/linkedin-video-the-complete-guide]. I could not fetch the LinkedIn page itself because the site blocks scrapers.
- **Video ads:** 75 KB to 500 MB. LinkedIn recommends 15–30 s. [OFFICIAL-snippet: https://www.linkedin.com/help/linkedin/answer/a424737]
- **Captions:** LinkedIn accepts SRT caption upload on video posts. [UNVERIFIED this session; long-standing feature]
- **Practical delivery:** 1080x1080 (1:1), 1080x1350 (4:5) or 1920x1080. Feed autoplays muted, so burned-in captions are strongly advised. [UNVERIFIED practice]

### A6. X (Twitter) video
- **Length and size** [OFFICIAL: https://help.x.com/en/using-x/x-videos]:
  - Non-Premium: up to **140 s, 512 MB**.
  - Premium: under 4 h at **1080p**, max 16 GB. Videos from 2 h to 4 h upload at 720p.
- **API "best practices"** [OFFICIAL-snippet: https://docs.x.com/x-api/media/quickstart/best-practices]:
  - H.264 High Profile, 30 or 60 fps, AAC-LC audio.
  - Recommended resolution 1280x720 (landscape), 720x1280 (portrait) or 720x720 (square).
  - The page itself blocks scrapers.
- **Practical delivery:** 1920x1080 or 1080x1920, H.264 High, AAC 48 kHz at 128–256 kbps, 30 fps. [UNVERIFIED practice]

### A7. Loudness targets
No major video platform officially publishes a LUFS target. Everything below about platforms is measured or community knowledge.

| Platform or standard | Target | Status |
|---|---|---|
| YouTube | Playback normalized toward about **−14 LUFS** integrated. Turns loud uploads **down only** and does not boost quiet ones. Shown as "content loudness" in Stats for Nerds. | [3RD-PARTY measured: https://meterplugs.com/blog/2019/09/18/youtube-changes-loudness-reference-to-14-lufs.html, https://youlean.co/?p=30813]. Not documented by YouTube. |
| TikTok / Instagram / Facebook | No published spec. Vendor guides cite −14 LUFS, while others claim a "louder" −10 to −12 LUFS performs better. | [UNVERIFIED, conflicting: https://www.forasoft.com/learn/audio-for-video/articles-audio/lufs-targets-per-platform-2026, https://openclip.app/learn/audio-normalization] |
| AES TD1008 (2021, streaming/online) | Speech and "assorted" content: **−18 LUFS** distribution loudness. It superseded TD1004 (−16 to −20 LUFS, −1 dBTP max). | [3RD-PARTY summary: https://productionadvice.co.uk/td1008/] |
| EBU R128 (broadcast, EU/India broadcast practice) | −23 LUFS ±1, −1 dBTP | [UNVERIFIED this session; standard knowledge] |
| ATSC A/85 (US broadcast) | −24 LKFS, −2 dBTP | [UNVERIFIED this session; standard knowledge] |

**Recommended default for the skill (opinion):**
- Master to **−14 LUFS integrated, true peak ≤ −1.0 dBTP** for YouTube, Shorts, Reels, TikTok, LinkedIn and X.
- Keep dialogue LRA about 6–9 LU for talking-head content. Keep music beds about 18–24 dB under voice in speech sections.
- Optional "loud shorts" variant at −12 LUFS, −1 dBTP. Label it as opinion.
- Use a two-pass ffmpeg `loudnorm` (see A10).

### A8. Thumbnails [OFFICIAL]
Source: https://support.google.com/youtube/answer/72431?hl=en (current text, fetched 2026-10-11)
- **Resolution:** the page now says "3840 x 2160 pixels for videos and 2160 x 3840 for Shorts". The minimum width is 640 px for videos, and the minimum height is 640 px for Shorts.
  - **The old "1280x720" spec is out of date as the recommendation.** It is still accepted because it is above 640 px wide.
- **Format:** image formats "such as JPG or PNG".
- **Size limit:** **2 MB when uploading on mobile** (10 MB for podcasts). **50 MB on desktop** for video, Shorts and podcast thumbnails.
- **Aspect:** 16:9 for videos, 9:16 for Shorts, 1:1 for podcast playlists.
- Custom thumbnails require a verified account. [OFFICIAL page intro]
- **Skill default:**
  - Render 3840x2160 PNG or JPG master, plus a 1920x1080 JPG at quality 90 or below 2 MB for mobile or legacy upload.
  - Check legibility at 168x94 px, the size of a mobile list thumbnail. [UNVERIFIED pixel size]

### A9. Caption file formats
- **YouTube** [OFFICIAL: https://support.google.com/youtube/answer/2734698?hl=en]:
  - Basic formats: **SRT** (plain UTF-8, no styling), **SBV/SUB**, MPsub, LRC, Videotron Lambda .cap.
  - Advanced formats: SAMI, RealText, **WebVTT** (positioning supported, styling limited to `<b><i><u>`), **TTML/DFXP** (styling and positioning supported, iTT subset).
  - Broadcast formats: **SCC** (preferred for CEA-608), EBU-STL, .tds, .cin, .asc, .cap.
- **Hindi tip:** upload SRT in **UTF-8** Devanagari for a Hindi track and a separate Latin-script Hinglish or English track. Set the video language correctly so auto-translate and auto-dub behave. [UNVERIFIED best practice]
- **LinkedIn:** SRT. **Facebook:** SRT named `name.xx_XX.srt`. **X:** SRT via the web or Media Studio. **TikTok and Instagram:** generally no sidecar upload for organic posts, so **burn captions in**. [All UNVERIFIED this session]

### A10. Practical ffmpeg export presets
The YouTube spec above is documented. The ffmpeg flags are standard ffmpeg semantics (https://trac.ffmpeg.org/wiki/Encode/H.264; the page timed out this session, so the CRF facts below come from my knowledge of that wiki: CRF range 0–51, default 23, "17–18 visually lossless or nearly so", `-movflags +faststart` for web playback, `-pix_fmt yuv420p` for compatibility with non-FFmpeg players).

**YouTube long-form, 1080p SDR, master-quality upload**
```bash
ffmpeg -i in.mov \
  -c:v libx264 -preset slow -crf 17 -profile:v high -level:v 4.2 \
  -pix_fmt yuv420p -bf 2 -g <fps/2> -keyint_min <fps/2> -sc_threshold 0 \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
  -r <source_fps> -fps_mode cfr \
  -c:a aac -b:a 384k -ar 48000 -ac 2 \
  -movflags +faststart out.mp4
```
- `-g <fps/2>` (for example 15 at 30 fps) follows YouTube's "GOP of half the frame rate" [OFFICIAL spec]. Most editors ignore this with no visible penalty. Making it optional is fine. [UNVERIFIED that it matters]
- x264 uses closed GOP by default. Do not pass `-x264-params open-gop=1`.
- CRF 16–18 at 1080p typically lands well above YouTube's 8–12 Mbps floor, which is fine. To force a floor or ceiling, use 2-pass `-b:v 16M -maxrate 24M -bufsize 32M`.
- **AAC:** YouTube recommends 384 kbps stereo. 320 kbps is also fine. The ffmpeg native `aac` encoder is acceptable at 256 kbps or more. `libfdk_aac` is better but rarely compiled in. [UNVERIFIED quality claim]
- **Color tagging:** tag BT.709 explicitly. Untagged files are assumed to be 709 [OFFICIAL], but tagging avoids gamma or "washed-out" mismatches in QuickTime and Premiere round trips. [UNVERIFIED claim on mismatches]
  - If the source is sRGB or full-range screen recordings, convert first: `-vf "scale=out_range=tv:out_color_matrix=bt709,format=yuv420p"` or use `zscale`.

**Vertical Shorts, Reels or TikTok (1080x1920)**
```bash
ffmpeg -i in.mov -vf "scale=1080:1920:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset slow -crf 18 -profile:v high -level:v 4.2 -r 30 -fps_mode cfr \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart out_vertical.mp4
```
- Use `-r 60` for gameplay or fast motion. Keep CFR, because Meta requires a "fixed frame rate" [OFFICIAL].

**Loudness, two-pass**
```bash
ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1:LRA=9:print_format=json -f null -
# then feed measured_I/TP/LRA/thresh back in with linear=true
```

**HEVC and AV1 notes**
- YouTube lists HEVC and AV1 as recommended **for HDR** [OFFICIAL]. For SDR the documented codec is H.264.
- HEVC (`libx265 -crf 20 -pix_fmt yuv420p10le -tag:v hvc1`) and AV1 (`libsvtav1 -crf 30-35 -preset 6`) give smaller files for upload over slow Indian broadband or 4G. Everything is re-encoded server-side anyway. [UNVERIFIED benefit]
- SVT-AV1: CRF 0–63, default 35. Presets trade speed against efficiency. Default keyframe interval is about 2–3 s. Film-grain synthesis is available via `film-grain=X`. [OFFICIAL ffmpeg wiki: https://trac.ffmpeg.org/wiki/Encode/AV1]
- Instagram, TikTok, LinkedIn and X: deliver **H.264** for safety. [UNVERIFIED; their docs list H.264]

**Should you export 4K from a 1080p source for YouTube?**
- **Documented:** higher-resolution uploads get higher recommended bitrates, and "to view new 4K uploads in 4K, use a browser or device that supports VP9" [OFFICIAL]. YouTube does not document that a 4K upload changes the codec or bitrate served at 1080p.
- **Folk wisdom, partially supported:** uploading 1440p or 2160p makes YouTube assign VP9 or AV1, with more bitrate per rendition, so the 1080p stream looks better than from a 1080p upload. [3RD-PARTY: https://www.provideocoalition.com/uploading-to-youtube-is-4k-worth-it/, https://filmdaft.com/?p=769]
- **Evidence complicates it:** Streaming Learning Center found AV1 renditions tied to **view count**. High-view 4K videos had AV1, while a 4K video with about 36k views had VP9 only. [3RD-PARTY: https://streaminglearningcenter.com/codecs/which-codec-does-youtube-use-part-iii.html]
- **Skill rule:** offer an optional "YouTube 4K upscale" export (`scale=3840:2160:flags=lanczos`, CRF 18, or about 40–45 Mbps). Label it "folk wisdom, widely reported, costs 4–5x upload size and longer processing". Default to native resolution when bandwidth is limited, which is common in India.

---

## PART B: Safe zones for vertical video (1080x1920)
None of the three platforms publishes these pixel numbers as text.
- Meta publishes percentages.
- TikTok publishes template PNG/ZIP files.
- Google publishes an annotated image.

The pixel figures below are those percentages or images converted to pixels by third parties.

| Platform | Top | Bottom | Left | Right | Source |
|---|---|---|---|---|---|
| **Instagram Reels** | 14% ≈ **269 px** | 35% ≈ **672 px** | 6% ≈ 65 px | 6% ≈ 65 px | [OFFICIAL %: Meta Ads Guide, https://www.facebook.com/business/ads-guide/update/video/instagram-reels]. Meta's canvas is 1440x2560; percentages scale. |
| **TikTok (In-Feed)** | **240 px** | **660 px** | 120 px | 120 px, plus an action rail about **300 px wide from y≈840 px down** | [3RD-PARTY measurement of TikTok's official template: https://www.upload-post.com/tools/safe-zone-checker/, checked 2026-09-23]. Official templates: https://ads.tiktok.com/help/article/video-ads-specifications |
| TikTok (alt. measurement) | 254 px | 707 px | 122 px | 242 px rail | [3RD-PARTY: https://adkit.so/tools/safe-zones/tiktok, March 2026] |
| **YouTube Shorts** | **288 px** | **672 px** | 48 px | **192 px** | [3RD-PARTY reading of Google Ads Help image: https://www.upload-post.com/tools/safe-zone-checker/]. Image source: https://support.google.com/google-ads/answer/9128498?hl=en |

**Caveats.** Margins vary by device aspect (for example 19.5:9 phones crop the sides), by caption length, and by whether an ad CTA is present. Meta asks for 40% bottom clearance on ads with disclaimers [3RD-PARTY citing Meta: https://www.inro.social/tools/instagram-reels-safe-zone-checker]. The platforms' UIs change several times a year.

**Universal cross-platform safe box (the intersection; skill default):**
- Usable area: **x 120 to 888 (768 px wide), y 288 to 1248 (960 px tall)**.
- Treat the TikTok right rail (x > 780 for y 840 to 1500) as a no-go for anything important.

**Placement guidance (synthesis; opinion unless noted):**
- **Burned-in captions:** centre horizontally. Put the caption block in **y ≈ 900–1240**, about 47–65% of frame height.
  - Never put captions below y = 1248, where they hit the TikTok, Reels and Shorts bottom UI and description.
  - Max width about 760 px. That gives roughly 2–4 words per line at 70–90 px bold sans for Hormozi-style captions, or 1–2 lines of 6–8 words for calmer styles.
- **Hook or title text (first 1–3 s):** y ≈ 300–600 (upper-middle). This sits below the top UI (search, "Following/For You", Shorts title) and above the face.
- **Face or eyes:** about y 500–800 for single-speaker talking heads, so captions sit under the chin and do not cover the mouth.
- **Logos and CTAs:** inside the safe box, never bottom-right, where the like, comment and share rail sits.
- **Devanagari captions** need about 15–20% more vertical line height than Latin because of matras above and below the line.
  - Fonts with Devanagari coverage: Noto Sans Devanagari, Mukta, Hind, Baloo 2, Poppins (Poppins has Devanagari plus Latin).
  - ffmpeg/libass needs a HarfBuzz-enabled build for correct conjunct shaping. [UNVERIFIED this session; known behaviour]

---

## PART C: Creator editing-style breakdowns
Hard numbers are rare. Every number below has a citation. Everything else is labelled [OBSERVED, UNMEASURED]: my best synthesis from commonly cited breakdowns and familiarity with the channels. The skill should treat these as starting presets to verify by analysing an actual reference video. Measure cuts per minute with scene detection such as `ffmpeg -vf "select='gt(scene,0.3)',showinfo"` or PySceneDetect.

**Key for "ASL"**: average shot length in seconds (running time ÷ number of shots). Cuts per minute = 60 ÷ ASL.

### MrBeast
- **Hard numbers:**
  - Tubefilter counted cuts in one minute from the midpoint of two videos: an older video had **38 cuts in 60 s (ASL ≈ 1.6 s)**, while the 2024 "abandoned city" video had **23 cuts per minute (ASL ≈ 2.6 s)**, with "lingering, zoomed-out shots". [3RD-PARTY: https://tubefilter.com/2024/03/04/mrbeast-editing-style-number-of-cuts-per-video/]
  - MrBeast, March 2024: "This past year i've slowed down our videos, focused on story telling, let scenes breathe, yelled less, more personality, longer videos". [same source, quoting his tweet]
- **Leaked production handbook, "How to succeed in MrBeast production"** (circa 2022, leaked August 2024 by Rosanna Pansino). Authenticity was confirmed by two anonymous former producers to Passionfruit, and MrBeast declined comment. Full text: https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/ ; coverage: https://passionfru.it/mrbeast-leaked-document-81151/ , https://www.creatorhandbook.net/leaked-document-allegedly-reveals-mrbeasts-secrets-to-youtube-success-the-key-takeaways/
  - **Metrics:** CTR, AVD, AVP. "The first minute has the most loss… The first minute of each video is the most important minute." In one example they lost 21M viewers in the first minute.
  - **First minute:** match the expectations of the title and thumbnail ("YOU MUST KNOW THE TITLE AND THUMBNAILS"), and front-load interesting content. Good lighting at the start correlates with less drop-off ("there is, have good lighting at the start of the video").
  - **Minutes 1–3:** "transition from hype to execution… Stop telling people what they will be watching and start showing them." Use "crazy progression", for example covering multiple days in the first 3 minutes.
  - **About 3:00, the "3 minute re-engagement":** a spectacle that "only MrBeast can do".
  - **Minutes 3–6:** "the most exciting and interesting content that is also very simple… lots of quick scene changes and highly stimulating simple content."
  - **About 6:00:** another re-engagement that "needs a little more explanation and will push the story in the back half."
  - **Back half:** viewers are in a "lull", and long explanations can live here. "Don't ever signal the end of the video unless it's to build hype for the prize or payoff."
  - **Length:** average video length over the last 100 videos was 818 s (13:37). Everyone must know "what minute mark" they are working on.
  - **Other principles:** "wow factor" (things no other creator can do). "BRAND DEALS ARE CONTENT". "Me like simple."
- **Observed, unmeasured:**
  - High-saturation, bright, warm grade. Wide-angle multi-cam.
  - Constant on-screen counters and timers (money, days, people left) as progress devices.
  - Punchy SFX on every reveal. Music changes per segment.
  - Bold captions only on key moments in long-form. Shorts and dubbed versions use more text.

### Ali Abdaal (and his editing team)
- **Hard numbers:** a typical video takes about **30 h of editing**: about **4 h** cleaning A-roll (dead space, mistakes, repeats, filler words) and about **8 h** adding B-roll from a personal library plus custom footage. [3RD-PARTY, Adobe blog: https://blog.adobe.com/en/publish/2024/09/05/how-ai-helps-ali-abdaal-save-hours-every-week]
- **Shorts style per Choppity's frame analysis** [3RD-PARTY vendor: https://www.choppity.com/tools/recreate-video-editing-style/ali-abdaal/]:
  - **2–5 s per shot** (ASL), so 12–30 cuts per minute. Cuts fall at thought transitions.
  - Desaturated or B&W base with a selective **yellow** colour pop.
  - Phrase-by-phrase captions (not word-by-word) placed beside the speaker, white with yellow key words, in a handwritten or script-style font.
  - Calm lo-fi or ambient music. Hook is a question or reframe.
  - Submagic describes his captions as "sober" with no bouncy animation [3RD-PARTY: https://www.submagic.co/blog/make-captions-like-ali-abdaal]. The two vendors disagree on reveal style.
- **Tools:** FireCut (AI zoom, silence-cut and caption plugin) was co-developed by Ali Abdaal and Suhail Idrees, so its claims carry a conflict of interest. [3RD-PARTY: https://firecut.ai/blog/how-ali-abdaal-edits-10x-faster-a-deep-dive-into-firecut/]
- **Long-form, observed, unmeasured:**
  - Bright, warm, soft-key home-studio look. Two-camera (front plus 45° side) angle switches used instead of jump cuts.
  - Frequent 110–120% punch-ins on emphasis.
  - Clean sans-serif text pop-ups with icons or emoji. Notion or Apple-style rounded cards, numbered "chapter" title cards.
  - Screen recordings and book covers as B-roll. Gentle whoosh and pop SFX. Light lo-fi bed.
  - Hook: a 15–45 s cold open stating the promise, then a short branded sting.

### Alex Hormozi (and the Iman Gadzhi / "business shorts" family)
- **Hormozi per Choppity** [3RD-PARTY vendor frame analysis: https://www.choppity.com/tools/recreate-video-editing-style/alex-hormozi/]:
  - **Jump cuts every 1–3 s** (20–60 cuts per minute), zero dead air, cuts on emphasis words.
  - **10–20% digital punch-ins**, alternating medium and tight framing. Speaker fills at least 60% of the frame.
  - Captions: bold uppercase sans **close to Montserrat Black**, white with a thick black stroke, **active word highlighted yellow**, **2–4 words visible**, word-by-word pop with a slight bounce, large and centred low.
  - Minimal B-roll. Subtle low-energy music. **No transition SFX**.
  - Dark background, crushed blacks, warm skin. The hook is an immediate bold or contrarian claim with no intro.
- **Other descriptions:**
  - VidPros: Montserrat Black 900, occasional italics, about 3° tilted text, font sizes varied for emphasis. [3RD-PARTY: https://vidpros.com/how-to-edit-videos-like-alex-hormozi/]
  - A CapCut tutorial: max 2 lines, about 6 words. [3RD-PARTY: https://gotranscript.com/public/mastering-youtube-shorts-capcut-tutorial-for-ali-abdaal-alex-hormozi-and-cody-sanchez-styles]
- **Iman Gadzhi:**
  - Subtle zooms, with the "intro zoom" as the most powerful. Switches camera angles on key phrases. B-roll as a pacing tool, including old footage used as flashback. [3RD-PARTY: https://www.opus.pro/pt-br/blog/how-to-edit-instagram-reels-exactly-like-iman-ghadzi]
  - Motion design uses accent colours pulled from the footage, in four types: on-screen text, UI mock-ups, illustrated scenes, and rare 3D. Heavy animation is reserved for moments needing focus. [3RD-PARTY video summary: https://sozai.app/transcript/ai-edit-iman-gadzhi-videos/]
  - **Observed, unmeasured:**
    - Cinematic, teal-and-warm "luxury" grade. Shallow depth of field. Travel, cars and city B-roll at high B-roll share (roughly 40–60% of screen time in long-form).
    - Risers, whooshes and bass hits on transitions. Serif or clean sans titles.
    - Slower long-form pacing (ASL about 3–5 s), faster in Shorts.

### Dan Koe (minimal, aesthetic)
- **[OBSERVED, UNMEASURED]** No reliable published breakdown exists. Search results were only Fiverr gigs and asset packs, for example https://julianbytes.gumroad.com/l/koepack.
  - Long-form essay or monologue, often a single static camera in a dim, minimal room. Alternatively voiceover over **black or near-black backgrounds with sparse white typography** and simple line illustrations or diagrams.
  - Desaturated, moody grade. Slow pacing (ASL often 5–15 s). Little to no SFX. Ambient or piano beds.
  - Minimal captions in long-form. Shorts and Reels use clean centred sentence-case captions.
  - B-roll is sparse: abstract nature, desk or notebook shots.
- Treat this as "quiet authority": restraint is the style. A skill preset should lower cut density, remove punch-ins and use plenty of negative space.

### Johnny Harris (map and documentary motion graphics)
- **Tools:**
  - Maps are built in **After Effects with the GEOlayers plugin**. Johnny's own December 2020 tutorial "How to Create Animated Maps with AfterEffects" covers GEOlayers (about $200) plus a cheaper path, with Mapbox Studio for custom map styles. [3RD-PARTY: https://aescripts.com/learn/how-johnny-harris-makes-maps/, https://aescripts.com/learn/making-maps-for-johnny-harris---volcanoes/, https://glasp.co/youtube/GsojLuJpe_0]
  - Animated globe or camera orbit moves using bearing and pitch, and country highlight overlays. [3RD-PARTY]
- **Texture:**
  - Most graphics and photos carry **textured overlays, film burns, light leaks and noise or grain**.
  - Photos slide in with position keyframes plus blur, with an old projector SFX. [3RD-PARTY: https://blog.motionarray.com/learn/premiere-pro/edit-documentary-in-premiere-pro/]
  - The "physical props" look: paper, desk and hand-drawn annotations. [3RD-PARTY: https://rndr.beehiiv.com/p/5-visuals-next-video-ead0]
- **Observed, unmeasured:**
  - Vlog-documentary hybrid: handheld on-location pieces to camera, plus a desk with printed maps, pins and highlighters, plus archival footage and documents with highlight sweeps.
  - Moderate ASL of about 3–6 s. Heavy original or atmospheric score with deliberate silences. Paper and whoosh SFX.
  - Off-white or cream paper palettes with red and yellow accents. Long-form runs 15–30 min.
  - Hook: personal "I went to X / I found this document" cold open, about 30–60 s.

### Vox explainers
- Founding producer Joe Posner called the format an "animated opinion essay", with rules against desks and talking-head interviews as the backbone. [3RD-PARTY quoting Vox: https://easy-peasy.ai/blog/how-to-make-vox-style-videos-with-ai]
- **Motion:** graphics are often **animated at 12 fps inside a 24 fps edit**, which gives the stepped or "choppy" look. [3RD-PARTY tutorial: https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/]
- **Visual language:** highlighter-pen sweeps over scanned documents or articles, paper-collage textures, maps, charts and kinetic typography. [3RD-PARTY: https://contra.com/s/WZggPY3k-vox-style-motion-graphics-modern-journalism]
- **Observed, unmeasured:**
  - Voiceover-led, nearly 100% B-roll and graphics. ASL about 3–5 s. Muted pastel or off-white palettes with a bold accent (Vox yellow).
  - Clean grotesque sans typography. Subtle music beds and paper or pen SFX.
  - Runs 6–15 min. Hook is a striking chart or question within 15 s.

### Kurzgesagt
- **Hard numbers:** about **1,200+ hours per video** and a team of **45 full-time** staff (2021 AMA). They published only about 150 videos in 8 years. [3RD-PARTY citing the Reddit AMA and channel descriptions: https://thetvdb.com/series/kurzgesagt-in-a-nutshell/episodes/7594048, https://cal1.lr.ggtyler.dev/r/IAmA/duplicates/ql88mw]
- **Tools:** illustration in Adobe Illustrator, animation in After Effects. [3RD-PARTY: https://www.toolfarm.com/?p=77543]
- **Style:** flat vector design with rounded shapes and vibrant colours. [3RD-PARTY: https://artsatmichigan.umich.edu/ink/2019/09/27/simple-bright-beautiful-the-work-of-kurzgesagt]
- **Observed, unmeasured:**
  - Fully animated; no live action, no faces. Saturated neon-on-dark-navy palettes, soft glows and gradients.
  - Continuous camera moves and "infinite zoom" scale transitions instead of hard cuts, so the effective ASL is long but motion never stops.
  - Single narrator, an orchestral or synth score, and dense layered sound design. Runs 8–15 min.
  - Rough music attribution: the channel's in-house music label is Epic Mountain. [UNVERIFIED this session]
- An AI skill can approximate this only with a template library (flat SVG assets plus easing) and should not promise it from raw footage.

### Veritasium
- Derek Muller argues for "legit bait": enticing but accurate titles and thumbnails, iteratively tested. [3RD-PARTY summary of "Clickbait is Unreasonably Effective", 2021: https://briefy.ai/summary/v2/curfkxexuv57xsqmhbo9twba/en/clickbait-is-unreasonably-effective]
- **Observed, unmeasured:**
  - Presenter-led documentary: on-location experiments, expert interviews, clean 2D/3D explanatory animation.
  - Moderate ASL of about 4–7 s. Natural, slightly warm grade. Restrained text, used for labels and equations.
  - Cold open with a counter-intuitive demo or question, then a misconception-then-resolution structure.
  - Runs 15–35 min. Subtle score, with music and SFX used sparingly.

### Mark Rober
- Analysts describe a shift (from the 2018 Glitter Bomb video on) toward story structure: motivation, challenge, emotional payoff. They say he paces videos "like thrillers" with curiosity, setbacks and reveals. [3RD-PARTY: https://www.opus.pro/blog/mark-robers-growth-playbook-how-he-engineered-one-of-youtubes-most-trusted-brands]
- Glitter Bomb as a three-act structure: victim, build, payoff. [3RD-PARTY: https://nofilmschool.com/2018/12/fake-package-catches-thieves]
- **Observed, unmeasured:**
  - Bright, saturated, family-friendly look. Fast build montages (ASL about 1.5–3 s) set against slower explanation segments.
  - Lots of slow-motion. CAD and diagram overlays, with labels and arrows.
  - Kid-friendly humour cutaways, a "squirrel" or "kid" POV gag, and big payoff reveals near the end.
  - Upbeat score with comedic stingers. Runs 15–25 min.

### Ryan Trahan
- **Ryan on thumbnails** [OFFICIAL YouTube blog interview: https://blog.youtube/creator-and-artist-stories/ryan-trahan-thumbnail-editing-secrets-to-going-viral]:
  - "We actually connect a lot deeper with a very subtle face". "Clear background, clean background, my face and then whatever the heck is going on."
  - He brainstorms many 2–3-word thumbnail subtitles. He rejects "exploitative" retention tactics.
- **Story techniques**, from George Blackman's breakdown of "I Spent 100 Days in GTA" [3RD-PARTY: https://georgeblackman.substack.com/p/13-unexpectedly-effective-youtube]:
  - Instant context: states the rules and goal up front. A constrained goal acts as a curiosity loop.
  - Visual progress tracker: dollars pinned to the wall.
  - Recurring characters and habits (in the penny series: McDonald's coffee, brushing teeth, theme tune).
  - **Alternating pacing:** fast edits contrasted with calm moments.
  - Three-act structure, then anticlimax and revelation, and a cliffhanger end.
- **Observed, unmeasured:**
  - Handheld vlog footage plus direct-to-camera narration and voiceover recorded after the fact.
  - Map and route animations, playful handwritten-style text, on-screen counters (money, days).
  - Light, natural grade. Whimsical score. Sincere, slow emotional beats near the end.

### Marques Brownlee (MKBHD)
- **Gear:** RED V-Raptor primary camera, Sony A7S III secondary, ARRI SkyPanel S60 key light, edited in Premiere Pro. Older rigs were RED Weapon and DSMC2. [3RD-PARTY: https://vloggingpro.com/setups/mkbhd/, https://www.theringer.com/2016/8/22/16036670/the-kid-who-revolutionized-youtubes-tech-reviews-a5b9a2a03a04, https://rosetta.to/u/mkbhd/the-mkbhd-gear-tour-2019]
- **Observed, unmeasured:**
  - Ultra-clean product cinematography: matte dark-grey or black sets, motion-control or robotic-arm slider moves, turntable macro shots, very shallow depth of field.
  - Signature **red accent** colour and minimal white sans lower-thirds and spec callouts.
  - Calm, measured talking head with medium ASL (about 4–8 s), lots of B-roll of the product (about 40–60%), and minimal SFX.
  - Ambient electronic beds. Crisp 8K/4K masters delivered at 4K.
  - Structure: quick verdict-tease hook, then sections, then a "should you buy it" ending.
  - A motion-control robot arm is used in the studio. [UNVERIFIED this session; widely shown in his studio tours]

### Colin and Samir
- The format is documentary-style interviews and industry analysis for creators. It started as an audio podcast in 2018 and became a video show in 2020–21. [3RD-PARTY: https://creatorbeast.substack.com/p/colin-and-samir-the-creator-economy, https://everything-pr.com/colin-and-samir-the-creators-who-built-a-media-company-about-creators]
- **Observed, unmeasured:**
  - Two-host and guest multicam podcast set with warm practical lighting.
  - Documentary cutaways: B-roll of the guest's videos, analytics screenshots, articles.
  - Bold quote cards and pull-quotes. Chaptered segments.
  - Relaxed pacing (ASL about 4–8 s). Light music between segments.

### Dhruv Rathee (Indian explainer, Hindi)
- **Process:** he has "a whole team of researchers and fact-checkers", publishes a resource paper for every video, and scores topics on audience demand, passion and relevance. [3RD-PARTY interview: https://www.khaleejtimes.com/uae/indian-influencer-dhruv-rathee-youtube-videos-fact-checked?amp=1]
- **Editor:** a public post by Satish Gola says he has edited Dhruv Rathee's videos for 3+ years. Only the title and snippet were visible because LinkedIn blocks scraping. [https://www.linkedin.com/posts/satishgola_videocreation-dhruvrathee-takeaways-activity-7326903458375106560-m_Bp]
- **Style descriptors** (third-party and freelance listings): concise, sharply edited, explainer visuals over background footage and images, clean motion graphics and text animation, map animation. [3RD-PARTY: https://edimakor.hitpaw.com/video-editing-tips/edit-videos-like-dhruv-rathee.html, https://www.freelancer.com/projects/da-vinci-resolve/high-retention-youtube-documentary]
- **Observed, unmeasured:**
  - Hindi (Hinglish technical terms) narration. Mostly voiceover over visuals, with periodic studio talking head.
  - Vox and Johnny Harris-style **map zooms** (globe to India to state). **Newspaper and tweet screenshots with yellow highlighter sweeps**. Charts and timelines. Heavy stock and news footage, so B-roll is likely above 70% of runtime.
  - Clean white or dark backgrounds with simple sans text. Bold Devanagari or Latin titles.
  - Neutral, informative music beds. ASL about 3–5 s. Runs 15–30 min.
  - Cold open poses the question or controversy within 20–30 s.
  - He operates dubbed language channels. [UNVERIFIED details]

### Ankur Warikoo
- His content is built on personal failure stories. [3RD-PARTY: https://www.businesstoday.in/tech-today/talks/video/i-pick-up-all-my-failures-and-make-them-into-a-story-says-ankur-warikoo-352129-2022-11-07]
- **Observed, unmeasured:**
  - Direct-to-camera talking head in a warm, tidy home-office set. English and Hinglish.
  - Numbered-list structure with simple text cards. Moderate jump cuts (ASL about 3–5 s) and light punch-ins.
  - Shorts: 30–60 s, captions mid-frame, a one-line lesson hook. Minimal B-roll and SFX.

### Think School (Indian business case studies)
- Co-founder Ganesh Prasad describes videos as "built in layers: script, research, edits, feedback, revisions". The post title frames the goal as "Netflix-level quality". [3RD-PARTY snippet, LinkedIn: https://www.linkedin.com/posts/ganeshprasad1997_ive-always-believed-think-school-should-activity-7362716956929540097-Cwxe]
- Founded in 2019 by Ganesh Prasad and Parsh Kothari. [3RD-PARTY: https://www.rotoris.com/friends-and-partners/ganesh-prasad-sridharan]
- **Observed, unmeasured:**
  - Presenter in front of a dark studio backdrop, intercut with dense **2D/3D motion graphics**: company logos, charts, timelines, maps, newspaper clippings, stock footage.
  - Chapter-card structure ("Chapter 1: …"). Cinematic, dark, high-contrast grade with brand-yellow and red accents.
  - Dramatic score and risers. ASL about 2–4 s in graphic sections. Runs 15–30 min.
  - Hook: a striking business paradox in the first 30 s.

### Raj Shamani (Shorts and podcast clips)
- **[OBSERVED, UNMEASURED]** No reliable published breakdown was found.
  - Clips from the multicam "Figuring Out" podcast. Hinglish.
  - Strong headline text bar at the top of the safe zone, plus word-level captions in the lower-middle (white or yellow highlight).
  - Fast removal of pauses, and cuts between guest and host angles on every speaker change.
  - Cinematic warm grade on a dark set. Subtle music under clips. Hook is the most shocking guest line, placed first.

### Tanmay Bhat
- **[OBSERVED, UNMEASURED]**
  - Casual, conversational talking head or stream-style setup. English and Hinglish with comedic timing.
  - Meme and reaction cutaways, zoom-in-on-punchline jumps, meme SFX.
  - Lower production polish by design. Shorts are often reaction or commentary clips with simple bold captions.

### Public editing style guides and SOPs
- **MrBeast production handbook:** the only widely available real internal guide (see above). It is about structure and retention, not fonts or LUTs. https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/
- **Johnny Harris map tutorial:** his own YouTube video (December 2020) on GEOlayers maps. A summary is at https://glasp.co/youtube/GsojLuJpe_0
- **Vendor-reverse-engineered "style sheets"** with fonts, cut rates and caption specs for Hormozi, Leila Hormozi, Ali Abdaal, Codie Sanchez and Tom Noske: https://www.choppity.com/tools/recreate-video-editing-style/ (useful presets; vendor-biased)
- No public editing SOP was found for Ali Abdaal, Kurzgesagt, Vox, MKBHD or the Indian creators. Kurzgesagt has said it does not publish behind-the-scenes material. [3RD-PARTY]

### Style preset summary for the skill

| Preset | ASL (s) | Cuts/min | Punch-ins | Captions | B-roll share | Grade | SFX/music | Evidence |
|---|---|---|---|---|---|---|---|---|
| Hormozi Shorts | 1–3 | 20–60 | Frequent 10–20% | Montserrat Black caps, white + black stroke, yellow active word, 2–4 words | Low | Dark, crushed blacks | Low music, no transition SFX | Vendor analysis |
| MrBeast (2022 style) | ~1.6 | ~38 | Frequent | Key moments only | High | Bright, saturated | Heavy SFX | 1-min sample |
| MrBeast (2024+ style) | ~2.6 | ~23 | Fewer | Key moments only | High | Bright | Moderate | 1-min sample |
| Ali Abdaal Shorts | 2–5 | 12–30 | Mild | Phrase reveal, yellow key words | Low–medium | Desaturated + yellow pop | Lo-fi | Vendor analysis |
| Ali Abdaal long-form | ~3–5 | 12–20 | Mild | Pop-up text cards | Medium (~8 h/video of B-roll work) | Warm, bright | Light | Adobe hours; style observed |
| Johnny Harris / Vox / Dhruv | 3–5 | 12–20 | Rare | Labels, highlighter | Very high | Paper textures, grain | Score + paper SFX | Tutorials; observed |
| Kurzgesagt | Continuous motion | n/a | n/a | Minimal | 100% animation | Neon on navy | Full score | Observed |
| MKBHD | 4–8 | 8–15 | Rare | Minimal lower-thirds | ~50% product B-roll | Clean dark, red accent | Ambient | Observed |
| Dan Koe | 5–15 | 4–12 | None | Sparse, sentence case | Low | Moody, desaturated | Ambient | Observed |
| Ryan Trahan | 2–5 (alternating) | varies | Some | Playful text, counters | High (vlog) | Natural | Whimsical score | Blackman analysis; observed |

---

## PART D: Retention-backed principles (evidence vs opinion)

### D1. Documented by YouTube [OFFICIAL]
- **Intro metric = % of viewers still watching after the first 30 s.** To improve it, YouTube says to make the thumbnail and title "better reflect your video content" and to "modify the first 30 seconds… experiment with different styles". [https://support.google.com/youtube/answer/9314415?hl=en]
- **Top moments:** "If the top moments are occurring in a later portion in the video, consider introducing the compelling content earlier in the video. Audience sizes typically decrease over the length of the video." [same source]
- **Spikes** mean rewatches or shares, or confusing content that viewers had to rewatch. **Dips** mean skipped or abandoned segments. Key moments need a video of at least 60 s with at least 100 views. [same source]
- **End screens:** can occupy the **last 5–20 s**. The video must be at least **25 s** long. Up to **4 elements** at 16:9. Not available on made-for-kids videos. [https://support.google.com/youtube/answer/6388789?hl=en]
- **Chapters:** the first timestamp is **00:00**, with **at least 3** timestamps in ascending order and each chapter **at least 10 s**. Manual chapters override automatic ones. [https://support.google.com/youtube/answer/9884579?hl=en]
- **Shorts:** up to 3 min. A Short over 1 min with a Content ID claim is blocked. [https://support.google.com/youtube/answer/15424877?hl=en]
- **Google ABCD framework (ads):** Attract, Brand, Connect, Direct. Ads following it showed a **30% lift in short-term sales likelihood** and a 17% lift in long-term brand contribution (Google/Kantar, 2021). This is evidence about ads, not organic videos. [https://business.google.com/us/think/future-of-marketing/creative-best-practices-youtube-ads/]

### D2. Practitioner evidence (internal data, not peer-reviewed)
- **MrBeast handbook** (internal analytics described by the creator): the biggest drop is in the first minute. Matching the title and thumbnail promise and good opening lighting reduce drop-off. Re-engagement spikes at about 3:00 and 6:00. Never signal the end before the payoff.
- **MrBeast 2024:** slower pacing (38 to 23 cuts per minute in sampled minutes) coincided with higher views. Correlation only; Tubefilter notes many confounders. [https://tubefilter.com/2024/03/04/mrbeast-editing-style-number-of-cuts-per-video/]
- **Third-party benchmark dataset:** Retention Rabbit's 2025 report (10,000+ videos, vendor data, methodology not public) claims:
  - Average retention 23.7%, with about 55% of viewers lost in the first 60 s.
  - Only 16.8% of videos exceed 50% retention.
  - Only about 16% of viewers reach the final 10 s.
  - First-minute retention over 65% correlates with 58% higher AVD.
  - Sources: https://www.retentionrabbit.com/blog/2025-youtube-audience-retention-benchmark-report, summarised at https://research.stripo.email/youtube-benchmarks
  - **[3RD-PARTY, treat as directional]**
  - YouTube itself publishes no niche or length averages and advises comparing against your own recent videos. [https://prepublish.ai/blog/youtube-retention-benchmarks-2026]

### D3. Widely shared opinion (no public data; label as such)
- **Hooks:**
  - Shorts: first **1–3 s**, opening mid-action with no logo or fade-in.
  - Long-form: confirm the click in the first 5–15 s, then deliver within 30 s. [3RD-PARTY or opinion: https://www.teleprompter.com/blog/how-long-should-a-youtube-intro-be]
  - Paddy Galloway emphasises packaging and the "glance test" for thumbnails, with short thumbnail text. [3RD-PARTY interview summary: https://videohighlight.com/v/UHhTKwclHCs]
  - I found no written Galloway or Film Booth retention study. Their advice should be cited as opinion.
- **Intro length:** no branded intro, or a sting under 3 s. Cold open first. This is consistent with YouTube's "first 30 s" metric and the MrBeast memo.
- **Re-hooks:** a pattern interrupt every 30–90 s in long-form (B-roll change, graphic, SFX, location change, new question). The MrBeast memo plans major re-engagements at about 3 and 6 min. A "re-hook every 3–5 s" for Shorts is folklore. [UNVERIFIED]
- **Payoff timing:** pay off the thumbnail promise early enough to prevent the click-regret dip (MrBeast: show, don't tell, after minute 1). Hold the biggest payoff for the end, without signalling "the end".
- **End screen, last 20 s:**
  - Keep content running under the end screen.
  - Avoid "that's it for today" or "thanks for watching" verbal outros, which trigger exits.
  - Point to **one specific next video** with a reason to watch it.
  - Based on the MrBeast memo plus common practice. [OPINION]
- **Chapters:** they help skimmers and search, but some creators believe they increase skipping. No public data either way. [UNVERIFIED]
- **Shorts loop endings:**
  - Make the last line or frame flow into the first: an incomplete sentence completed by the opening, or a matching visual.
  - Since 2025-03-31 replays count as views, and APV can exceed 100% with loops. [3RD-PARTY: https://coschedule.com/social-media-marketing/youtube-metrics]
  - Whether loops boost distribution is unproven. [OPINION]
- **Storytelling devices with analyst support:**
  - Instant context, constrained goals as curiosity loops, visual progress trackers, recurring motifs.
  - Alternating fast and calm pacing (not constant motion). Three acts. Cliffhanger endings.
  - Source: Blackman on Ryan Trahan, https://georgeblackman.substack.com/p/13-unexpectedly-effective-youtube

### D4. Translating this into skill rules (recommended defaults)
1. **Shorts:** no intro, with the hook line plus on-screen hook text in frame 1. Captions from frame 1 inside the safe box. Something new about every 1.5–3 s (cut, zoom, graphic). Loop-friendly last line. Target 20–45 s unless the story needs more. Keep any third-party music claim-free if the Short is over 60 s.
2. **Long-form:** cold open of 15–45 s that restates the title and thumbnail promise and shows the "proof" visual. No logo sting over 3 s. Plan re-engagements at about 1:00, 3:00 and 6:00 and every 2–3 min after (adapted from MrBeast). Chapters with 00:00, 3+ chapters of at least 10 s each. End screen in the final 5–20 s with content still playing.
3. **Analytics loop:** after publishing, read the Intro % (30 s), dips and spikes from Studio. Feed the timestamps back into the edit notes for the next video.

---

## Source-confidence summary
- **Confirmed from official pages this session:**
  - YouTube encoding, HDR, Shorts, thumbnails, captions, end screens, chapters and key moments.
  - Instagram aspect, frame rate and resolution. Meta Reels ad specs and safe-zone percentages.
  - TikTok In-Feed ad specs and TikTok Studio upload limits.
  - X length and file-size limits.
  - ffmpeg AV1 wiki.
- **Official but excerpt-only:**
  - Instagram 20-min and 3-min recommendation rule. TikTok 10/60-min. LinkedIn sizes and durations. X API codec recommendations.
- **Not confirmable from official sources:**
  - Platform LUFS targets. Pixel-exact safe zones for TikTok and Shorts (official ones exist only as images or templates).
  - The 4K-upload quality boost. LinkedIn's 15-min member limit.
  - Most creator style numbers apart from those cited.
