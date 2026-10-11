# Visual sourcing: where every picture comes from

**Default: build it.** Motion graphics, cards, kinetic type, overlays, charts, UI mockups, annotations and
diagrams are made in code (HyperFrames). Sourcing is only for raster or photographic assets that cannot be
code-built: photos, PNG cut-outs, textures, archival images, product shots, B-roll.

## The cascade (in this order, every project)

1. **Ask first:** "Do you have the visuals/PNGs for this, or should I source them?" Never assume.
2. **User-provided assets win.** Brand files, logos, photos, PNGs, screen recordings the user drops in are used
   **as supplied**. Never regenerate, "improve", restyle or upscale them without a yes. Cut-outs of supplied
   photos (`rembg`, if installed) count as using them.
3. **Web sourcing** for what is missing, with a licence note per file in `EDIT_STATE.md` (source URL, licence,
   attribution text if required):
   - Free to use commercially: Unsplash, Pexels, Pixabay (photos/video), Wikimedia Commons (check each file's
     licence: CC0 / CC-BY need credit, CC-BY-SA needs share-alike, some are non-commercial), NASA and most US
     government media (public domain), Smithsonian Open Access (CC0).
   - Prefer transparent PNGs for overlays; textures (paper, grain, film burns) from the same free sources.
   - **Pinterest is a moodboard, not a licence.** It aggregates other people's images; most pins are
     copyrighted by someone else. Use it to find the look or the original source, then use the original only
     if its licence allows. Never ship a Pinterest download as-is in a monetised or client video.
   - Never use watermarked stock, comp images, or images from Google Images without a known licence.
   - Logos and product screenshots of other companies: fine for commentary/editorial use, never in a way that
     implies endorsement.
4. **Higgsfield (only if available and confirmed).** Ask once per project: "Do you want me to generate
   visuals with Higgsfield for this one?" Remember the answer in `EDIT_STATE.md`. If yes and a Higgsfield
   connector is connected in this Claude session, generate there; if not connected, say so and go to step 5.
5. **Image-generation prompt pack (always available).** For every scene that needs a visual nobody has, write
   a production-ready prompt the user can paste into any image or video model (format below), saved as
   `work/prompt-pack.md` next to the storyboard.

## Not-found protocol: a scene never ships empty

When a wanted visual is not found, pursue every available path in parallel, and report all three results:

- (a) keep sourcing with alternate search terms and other sites;
- (b) write the prompt-pack entry so the user can generate it;
- (c) generate it with Higgsfield if the project confirmed it and the connector is available;
- and meanwhile build a code-made stand-in (type card, diagram, annotated texture) so the edit can proceed.

Report: what was found (with licences), what was generated, which prompts are waiting for the user.
"Not found" is never the end of the step.

## Prompt-pack format (6 parts per visual)

```
### Scene 4 (0:12-0:15) "a whole cast"
Subject:     <who/what, specific: age, clothing, object, action>
Style:       <match the storyboard's selected option: palette hexes, film stock / illustration style, era>
Composition: <framing, angle, lens, where empty space must be for the type (e.g. top 40% clear)>
Motion:      <video only: one camera move, duration <= 3 s, what moves>
Technical:   <aspect 9:16 | 16:9, resolution, lighting, depth of field>
Negative:    <no text, no watermark, no extra fingers, no logos, no second accent colour>
Consistency: <base image / seed / character sheet to reuse; the same palette lock as other scenes>
```

## Rules for AI visuals

- **Still first, then image-to-video.** Lock the frame as an image, approve it, then animate it. Never
  text-to-video for editorial shots: it drifts.
- **Keep AI shots under about 3 s** and cover seams with cuts; long AI shots expose drift and uncanny motion.
- **One base image per character** across every scene and variant; never regenerate a face per scene.
- **Consistency pass:** all AI visuals share the palette lock and subject treatment of the selected storyboard
  option; grade-match them to the A-roll (`grade.py --match`).
- Disclose synthetic people in ads where the law requires it (see `ugc-ads.md`).
- No generic stock filler (glowing brains, handshakes, random cityscapes): every visual must illustrate the
  exact sentence it sits on.
