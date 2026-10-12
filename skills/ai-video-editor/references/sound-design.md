# Sound design

Sound carries more of an edit than picture does. Two tests decide whether the sound works: the **Closed Eye
Test** (below) and listening on a phone speaker. Numbers marked [PRACTITIONER] are the consensus of working
editors, not lab measurements; [UNVERIFIED] means reported but not confirmed.

## Contents
1. Where music and SFX come from (ask every project)
2. The mix: levels, ducking, de-essing
3. SFX craft
4. Music structure
5. Texture beds
6. Code-native scoring
7. QA: the Closed Eye Test

## 1. Where music and SFX come from (ask every project)

The user has a paid **Epidemic Sound** plan. Every project, ask which source to use; never assume:

- **Epidemic Sound**: the user downloads the tracks/SFX (or gives the files); keep the licence crediting the
  plan requires, and note track IDs in `EDIT_STATE.md`. Channel/whitelisting is the user's account setting.
  The licence covers videos published **while the subscription is active**: if the plan lapses, earlier
  videos stay cleared, new uploads do not. Confirm it is active on the publish date.
- **Free, copyright-safe**: YouTube Audio Library (check each track's attribution requirement), Pixabay Music
  and SFX, Mixkit, Freesound (CC0 or CC-BY only; CC-BY needs credit). Write the source URL and licence of
  every file into `EDIT_STATE.md`.
- Never use commercial music the user has no licence for, "no copyright" compilations from YouTube, or
  tracks ripped from other videos. YouTube Content ID claims or mutes them, and Instagram can mute or block the audio.
- A persistent sound library across projects lives in `assets/style-lab.md` (tagged by role: riser, impact,
  whoosh, pop, bed; rated Keep / Maybe / Drop), so the next video starts from proven sounds.

## 2. The mix: levels, ducking, de-essing

- Delivery loudness: -14 LUFS integrated, -1 dBTP (`finish.py`). Mastering hotter buys nothing.
- **Music bed under voice: 16-25 dB below the voice.** Auto-duckers (Premiere, CapCut) pin at about -16 to
  -20 dB of bed depth; the extra 3-5 dB of sidechain gain reduction is the icing applied after that, not the
  cake. `finish.py --music-sep 20 --duck` does both stages. [PRACTITIONER]
- **The bed level is relative to the measured voice**, not an absolute number: `--music-sep 20` measures the
  voice LUFS and the music LUFS and sets the bed 20 LU under the voice, so a quiet track and a slammed track
  land at the same place. `--music-db` is the old absolute gain, kept only as an override.
- **Voice chain:** `--voice-chain light` (high-pass 80 Hz only, default) or `full` (high-pass, 3:1 compressor,
  then de-esser) for uneven mic distance or harsh S sounds. A mono voice is upmixed to stereo first; music is
  forced to stereo, so the master never collapses to mono.
- **Duck recovery 600 ms - 1 s** (`--duck-release`, default 700). Faster pumps audibly; slower buries the
  start of the next phrase under music. [PRACTITIONER]
- **Dynamic EQ instead of (or under) broadband ducking:** dip only the music's 2-5 kHz presence band while the
  voice speaks, so the bed stays alive. ffmpeg has `adynamicequalizer` but no sidechain key for it; do this
  in a DAW when it matters, otherwise duck. [PARTIAL: technique documented, depth not measured]
- **De-esser placement is contested.** Default: after the compressor (compression exaggerates sibilance the
  de-esser then catches). Alternative: before it, when the compressor pumps hard. A light pass in both places
  is a common compromise. ffmpeg: `deesser=i=0.4` after `acompressor`.
- Room-tone bed: a constant ambience under dialogue cuts at roughly -45 to -50 dB (about -32 LUFS) glues edits
  the ear would otherwise hear as dropouts. [documented, not measured in a session]

## 3. SFX craft

- **SFX only where something visibly changes** (a cut, a graphic landing, a number stopping). Explainers: at
  most about one per second, none on top of a key word.
- **Riser ends AT the hit.** The riser's peak lands on the impact frame; early or late reads as a mistake. In
  `sfx.json` use `"end_at": <hit time>` (or `"peak_at"`) instead of `"at"`: `finish.py` finds the SFX's
  loudest sample and lands THAT on the frame, not the file's edge. SFX `"db"` is relative to the voice peak
  (-6 = 6 dB under the voice peak); an SFX that would start before 0 or run past the end is skipped with a WARN.
- **Whoosh sits under the impact, as its own layer.** Riser builds anticipation, whoosh sells motion, impact
  sells weight: three jobs, three layers. A good whoosh itself has 3-4 frequency layers (sub sweep, mid noise
  band, high air, optional tonal element), each with its own EQ band, which is why it survives phone speakers.
- **Text and UI pops at 20-40% of the impact level** (about 8-14 dB under it). Full-volume pops fatigue the ear
  within seconds; their job is confirmation, not announcement.
- **Never repeat an identical SFX.** Every repeat gets a pitch/speed variation of about 5-10%. `finish.py`
  does this automatically for any file used more than once (0.94-1.08x, deterministic); `"vary": false` keeps
  a sound identical on purpose. Building variety from one whoosh: slow a copy to 60% speed and -5 semitones
  for a deep layer, speed a copy to 120% and +4-5 semitones for a high layer; the peak always lands on the
  movement. Source: luvkilomedia, youtube.com/watch?v=U6wVF2PMBUw, 09:12-11:07.
- **Diegetic detail.** Sounds that exist inside the shot (keyboard clicks, footsteps, a cup on a desk) make
  B-roll feel real. Most editors only add designed SFX; lay the literal sound too. Source: Abhay PS Rajawat,
  youtube.com/watch?v=SWAYLiH7p5M, 05:42-06:10.

## 4. Music structure

- **Riser -> smash cut -> silence.** Build, hard cut to the reveal, then about 0.25-0.5 s of near-silence before
  the payoff lands [exact ms UNVERIFIED]. Silence after the cut is the loudest moment in the video.
- **Full stop on the beat.** Stopping the music dead on a beat makes that moment land harder:
  `finish.py --music-stop <time>`. By default the last 10 frames ring out as a ~3 s reverb tail (the "cinematic
  end" recipe: cut 10 frames before the end point, duplicate that tail, extend it about 4 s, reverb it, drop
  about 5 dB to offset the overlap). `--music-tail cut` for a hard stop. Source: luvkilomedia (U6wVF2PMBUw)
  03:04-04:47; Abhay PS Rajawat (SWAYLiH7p5M) 05:29-05:37.
- **Rotate the bed every 60-90 s.** The ear adapts to a track and stops hearing it; change track, tempo or
  energy at section boundaries. [creator rule, Abhay PS Rajawat 04:11-04:31]
- **Chapter changes on musical bars, cuts on beats.** One timeline drives picture and score (the beat grid).
- Music-first sequencing for B-roll montages: cut the assembly to the music's structure (drops, breaks,
  builds) first, then fine-cut to the voice.

## 5. Texture beds

- **Background-talking texture** (documentary/crime): isolate talking from news or interview footage, lay it at
  -15 to -20 dB under the scene, cut it into segments around the gaps, then EQ it slightly muffled (lowpass
  about 3-4 kHz) so it sits inside the soundtrack. Source: luvkilomedia (U6wVF2PMBUw) 13:41-16:29.

## 6. Code-native scoring (optional)

A score can be synthesised per scene instead of licensed: a cue timeline drives instrument recipes (kick, sub,
hats, pads, risers), no samples, no licence. Doctrines from the one public implementation
(tuzhechen2005/opus-video-skills, kinetic-reel sound references): no whooshes inside the score (they are
transition SFX, not music), silence on about half the cuts so the score breathes, chapter changes on bars.
[SECONDARY: repo, not evaluated here.] Offer it when the user wants a fully original, licence-free bed.

## 7. QA: the Closed Eye Test

Play the cut with eyes closed. If it still holds attention, the edit works; if it is boring, it is pretty but
not engaging. Fix voice, rhythm, silences and gaps **before** visual polish. Source: Abhay PS Rajawat
(SWAYLiH7p5M) 00:36-01:54. (The "brain sides with audio" mechanism he cites is unproven; the habit is the
rule.) Then listen once on a phone speaker: anything that disappears there (sub-only hits, low whooshes) needs
a mid layer.

For long-form narrative edits, build the sound skeleton first: dialogue cut, then music, score, field
recordings and SFX with zero visuals ("treat it as a song", with a rise and fall), and only then lay picture
on top. Source: Max McCoy, youtube.com/watch?v=XUWjBQiT1Iw, 01:08-08:54. For code-built kinetic reels, picture
and sound co-evolve; the Closed Eye Test is the check instead.
