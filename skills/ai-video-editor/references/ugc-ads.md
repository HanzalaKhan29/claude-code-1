# UGC and AI-avatar ads

Paid social creative follows different rules from organic content: it is built to be tested, iterated and
disclosed. Practitioner numbers are labelled [PRACTITIONER]; nothing here is platform-measured unless stated.

## Structure

- **The 4-part hook stack, all in the first 3 s:** visual hook (what the thumb stops for), verbal hook (first
  line), text hook (on-screen line), audio hook (sound that breaks the feed). Most weak hooks are missing a
  part, not weak in all four.
- **Test the visual hook first.** When iterating, swap the opening image before the words: it moves results
  more in practitioner testing. [PRACTITIONER]
- **A second hook at 3-5 s** re-catches viewers the first hook stopped but did not convince.
- **Winning skeleton:** problem -> friend-style recommendation (not a pitch) -> proof -> soft CTA.
- **Founder on camera in the first seconds with a title overlay** ("Name, founder of X") answers "who is this"
  before it is asked. Reported as a split-test winner; test details are thin. [REPORTED]
- **End card 2-3 s:** brand + one-line CTA (same spec as the motion-reels end card).

## Modular production

- **Hook x body x CTA modules:** e.g. 12 hooks x 4 bodies x 1 CTA = 48 testable variants from one shoot;
  refresh hooks about every 3 weeks. Build the edit as separate module renders plus a variant matrix so any
  combination can be exported. [PRACTITIONER]
- **Creative diversity over one winner** (reported effect of Meta's Andromeda ranking update): many genuinely
  different concepts outperform small tweaks of one ad. Meta has not published the mechanism. [PRACTITIONER]
- **Native vs polished** is a per-brand test, not a law.
- **Shoot for the edit:** 3 full takes of every setup, about 3 s handles at both ends.
- Hook-rate benchmarks circulate widely; treat them as direction (kill a variant that is clearly below its
  siblings), not as targets.

## AI avatars and synthetic presenters

- **Cover seams with B-roll.** Lip-sync drift and loop points are where avatars fail; cut to B-roll over them.
  One practitioner reported about +20% on their metric from doing this (single source). [n=1]
- **One base image per character** across every variant; never regenerate the face per scene.
- No specific caption treatment for avatar videos was found to matter; use the normal caption rules.

## Disclosure (verified 2026-10-11 against primary sources)

**When in doubt, disclose.** A visible "AI-generated" or "synthetic presenter" label costs almost nothing in
performance and removes the legal risk in every market below. Default to disclosing any AI person or voice in
a paid ad; drop it only when the user confirms with counsel that it is not needed.

**C2PA survives only on the master.** `finish.py` and every ffmpeg re-encode strip C2PA / Content Credentials
metadata. Keep the AI tool's original export (with its provenance) in `source/` or `renders/masters/`, and
tell the user the delivered MP4 no longer carries it, so platform "AI info" labels will not trigger
automatically: they must set the platform's AI toggle by hand.

- **New York, GBL section 396-b** (S.8420-A / A.8887-B, signed 11 Dec 2025, **in force since 9 June 2026**):
  an advertiser who knowingly uses a "synthetic performer" (an AI or algorithm-made person not recognisable as
  any real performer) in an ad must disclose it conspicuously. Civil penalty $1,000 for a first violation,
  $5,000 for each later one. Exempt: audio-only ads, AI used only to translate a real performer, and ads for
  expressive works consistent with the work. Source: nysenate.gov/legislation/bills/2025/S8420/amendment/A.
- **California AI Transparency Act** (SB 942, amended by AB 853): operative **2 Aug 2026**. Its duties fall
  mainly on large generative-AI providers (detection tools, embedded provenance), not directly on advertisers;
  more duties phase in 2027-2028. Practical effect: keep provenance metadata from AI tools intact (do not strip
  C2PA data on export when avoidable).
- **EU AI Act, Article 50:** applies from **2 Aug 2026**. Deployers who publish deepfake image, audio or video
  content must disclose that it is artificially generated or manipulated (lighter rules for evidently
  artistic or satirical work). Fines up to EUR 15 million or 3% of worldwide turnover. Some marking duties for
  providers are deferred to 2 Dec 2026.
- **Platforms:** Meta shows "AI info" labels from C2PA/IPTC metadata and requires disclosure of digitally
  altered media in political and social-issue ads; TikTok has an AI-generated content toggle and asks creators
  to label realistic AI content; YouTube requires the "altered or synthetic content" disclosure for realistic
  synthetic media. Check each platform's current ad policy before a paid launch.
- This is information, not legal advice: for paid campaigns in these markets, tell the user to confirm with
  their counsel.

## Ethics (not testable)

No fabricated testimonials, no fake before/afters, no invented results or reviews, no impersonation of real
people. If a brief asks for any of these, decline that part and say why.
