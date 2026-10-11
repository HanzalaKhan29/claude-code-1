# Pre-delivery QA checklist

Do not tell the user "done" until every line is checked or explicitly reported as not checkable.

## Before the build (gates)
- [ ] Storyboard approved by the user (`storyboard.py` passed: contiguous scenes, verbatim VO, 2+ style options)
- [ ] Visual sources decided (user assets / web with licences / Higgsfield yes-no / prompt pack) and every
      scene has a visual or a stand-in
- [ ] Music/SFX source decided (Epidemic Sound or free, licence noted)
- [ ] 3-4 still frames per scene reviewed before animating it (HyperFrames snapshots)

## Automatic (scripts)
- [ ] `python3 scripts/qa.py <final> --edl work/edl.json --captions <ass> --platform <p>` shows no FAIL
- [ ] Loudness -14 LUFS (+/-1), true peak at most -1 dBTP
- [ ] H.264 (or HEVC/AV1 on request), yuv420p, AAC 48 kHz, faststart, BT.709 tags
- [ ] Duration matches the EDL (render_cut.py prints both); audio and video stream durations match (ffprobe)
- [ ] No black frames, no frozen live footage, no flash frames (shots under 3 frames)
- [ ] `python3 scripts/verify_cut.py <render> work/words_cut.json`: no clipped or ghost words at cut points; no drift over 120 ms
- [ ] HyperFrames graphics: `npx hyperframes check .` 0 findings for every composition

## Look (open every sheet yourself)
- [ ] `qa/cuts.png`: every edit point invisible or intentional; no jump that the punch-in failed to hide
- [ ] `qa/captions.png`: readable, correct spelling of names, inside the safe box, never over eyes or mouth, one highlight per group
- [ ] `qa/overview.png`: colour consistent shot to shot; nothing broken; rhythm varies
- [ ] Every graphic frame (`npx hyperframes snapshot`): no clipped text, no overlaps, contrast holds, on-brand, lands on its word
- [ ] First frame works as a thumbnail (Shorts) and the first 3 s already deliver the hook
- [ ] Slop audit: at most 2 font families, 1 accent, no emoji icons, no default-banned effects unless chosen

## Listen (if you cannot hear audio, say so and list the timestamps the user should check)
- [ ] Every join: no click, no clipped consonant, no doubled breath
- [ ] Music never fights the voice; no vocals under speech; silence before reveals where planned
- [ ] SFX land on visible events only
- [ ] **Closed Eye Test:** the cut holds attention with eyes closed (fix voice, rhythm and gaps before polish)
- [ ] Repeated SFX are varied (finish.py does it), risers peak on the hit frame, pops 8-14 dB under impacts
- [ ] Phone-speaker listen: nothing important lives only in the sub

## Structure
- [ ] First visible motion within about 0.13 s; frame 1 is not black, a logo or a slow fade
- [ ] 0-3-8 s ladder: visual hook at 0 s, promise by 3 s, first payoff/escalation by 8 s
- [ ] Long-form: thumbnail/title promise confirmed within 15 s (stopwatch it), then extended; the opening does
      not repeat the thumbnail text
- [ ] **Mute test:** the first 15 s confirm the promise without sound
- [ ] Pacing arc: no two same-tempo scenes back to back; no repeated pattern
- [ ] Tile strip across the timeline (contact sheet every 2 s): no palette drift, type tiers respected, one
      accent, 70/20/10 visual weight
- [ ] Motion reels: 25-40% of words captioned (captions.py --selective prints the share), one accent, grain on

## Truth
- [ ] Every number, name, quote and claim on screen comes from the transcript or the user
- [ ] Licences noted for music, SFX, stock, fonts (Fontshare fonts not redistributed)
- [ ] No Pinterest or Google Images downloads shipped without a known licence; user-supplied assets used as supplied
- [ ] Synthetic people in ads disclosed where required (ugc-ads.md)

## Deliver
- [ ] Final file in `renders/` with a version number; source untouched
- [ ] `.srt` exported for YouTube upload
- [ ] For YouTube: chapters list (00:00 first, 3+ chapters, 10 s+ each) and end-screen window (last 5-20 s) suggested
- [ ] `EDIT_STATE.md` updated (what was delivered, open notes)
- [ ] Asked: "Should I add what we learned to the skill?"
