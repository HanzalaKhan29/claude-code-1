# Video plan: Solo & Starving?

## The short answer

**Put your money and time into UGC ad videos first.** Add one small product-demo video to the website second. Don't put a big video in the website hero.

| | UGC ad video | Website video |
|---|---|---|
| Job | Stops the scroll on TikTok / Reels and gets the click | Proves the PDF is real and easy to use |
| Impact | Decides whether anyone visits at all. On paid social, the creative drives most of the result | A small lift at the decision point |
| Risk | Low | A heavy hero video slows the page on mobile data, and slow pages lose ad clicks |
| Priority | **1** | **2** (short, muted, loops, lazy-loaded) |

The site already has a slot for the demo video in "How it works". It stays hidden until you add the file (see the bottom of this doc).

## Two honesty rules (these protect your ad account)

1. **No fake customer testimonials.** You have no reviews yet. An AI person saying "I bought this and it changed my life" is a fake review. Meta and TikTok can reject the ad or restrict the account, and the FTC treats it as deceptive. Use a **creator-style demo** ("here's how this works") or, much better, **Yassine or Nourhene on camera**. Two real founders cooking in a real kitchen is your strongest proof right now.
2. **Label AI video.** If any shot has a realistic AI-generated person, switch on TikTok's "AI-generated content" label and Meta's AI disclosure.

## Ad links

Send every ad to the quiz, tagged so you know which video sold:

```
https://YOUR-DOMAIN/?quiz=1&utm_source=tiktok&utm_campaign=launch&utm_content=ugc_hook1
https://YOUR-DOMAIN/?quiz=1&utm_source=facebook&utm_campaign=launch&utm_content=feed_energy
```

The site passes these tags through to Gumroad, and the Meta Pixel records QuizStart, QuizComplete, ViewPersonalizedPlan and InitiateCheckout.

---

## Video 1: UGC ad, "The 9pm problem" (main ad)

- **Ratio:** 9:16, 1080 x 1920
- **Length:** 20 to 25 s
- **Where:** TikTok, Instagram Reels, Facebook Reels, Stories
- **Safe zone:** keep text out of the top 150 px and the bottom 400 px (app buttons cover them)
- **Best version:** filmed on a phone by one of you, natural light, no music bed, just voice plus light kitchen sound

### Script and shot list

| Time | Shot | Voice (to camera) | On-screen text |
|---|---|---|---|
| 0-2 s | Close-up of a thumb hovering over a delivery app at night, phone glow on a face | "It's 9pm, you're tired, and your thumb already knows the way." | It's 9pm. Again. |
| 2-5 s | Person drops the phone on the counter, opens the fridge: half a bag of spinach | "This is the fourth $18 dinner this week." | $18 x 4 |
| 5-10 s | Phone screen: the cookbook PDF, a finger taps "Tired mode" in the index, lands on the Chicken Caprese page | "So I use this. Every recipe is sorted by how tired you are. Normal, Tired, Dead Tired." | Pick your energy, not a recipe |
| 10-17 s | Fast cuts: one pan, chicken in, tomatoes, mozzarella melting, plated on dark wood | "Twenty minutes, one pan, and there's a second portion for tomorrow." | 20 min. $2.90. 2 portions |
| 17-22 s | Eating on the couch, relaxed, then back to the phone showing the quiz | "Take the 1-minute quiz, it builds your first week." | Take the 1-min quiz (link) |

### AI video prompt (Seedance, Veo, Kling, Higgsfield), one per shot, all 9:16

**Shot 1**
```
Vertical 9:16 smartphone-style UGC footage, 1080x1920. Night, a small apartment kitchen lit only by a phone screen and a warm under-cabinet light. Extreme close-up of a thumb hovering over a food delivery app icon, then pulling back. Handheld, slight natural shake, shallow depth of field, realistic skin texture, no text, no logos, no brand names visible. Moody, tired, relatable. 2 seconds.
```

**Shot 3 (product screen): don't generate with AI.** Screen-record the real PDF on a phone. AI will invent a fake interface, and a fake product screen in an ad is misleading.

**Shot 4**
```
Vertical 9:16, 1080x1920, cinematic food close-ups in one cast iron skillet on a dark wooden counter, warm tungsten light, night mood. Sequence: seasoned chicken breast searing, cherry tomatoes halved and dropped in, shredded mozzarella melting, fresh basil torn on top, steam rising. Handheld macro, shallow depth of field, rich warm tones matching dark rustic food photography. No people's faces, no text, no logos. 6 seconds.
```

**Shot 5**
```
Vertical 9:16 smartphone UGC style, 1080x1920. A person in comfortable home clothes sits on a couch at night eating from a bowl, relaxed and content, warm lamp light, casual real apartment, natural handheld framing from a friend's point of view. Realistic, candid, not posed, no text, no logos. 4 seconds.
```

---

## Video 2: Feed ad, "Energy switch" (no person needed)

- **Ratio:** 4:5, 1080 x 1350
- **Length:** 12 to 15 s
- **Where:** Facebook and Instagram feed
- **Why:** it shows your one unique mechanic in under 5 seconds, and it works with the sound off

### Storyboard
1. **0-3 s:** Title "How tired are you tonight?" over a dark wood background.
2. **3-6 s:** "NORMAL, 30 min". Turkey Chili slides in. Label: 25 min, $3.10.
3. **6-9 s:** "TIRED, 20 min". Chicken Caprese Skillet. Label: 20 min, $2.90.
4. **9-12 s:** "DEAD TIRED, 10 min". Greek Yogurt Chocolate Crunch. Label: 10 min, $1.35.
5. **12-15 s:** "88 recipes for one, sorted by energy. $19.25 launch price." Then "Take the 1-min quiz".

Use your existing dish photos from `public/images/`. Build it in CapCut or Canva with a slow 5% push-in on each photo, lavender (#BBA3F5) labels and the Bricolage Grotesque font to match the site.

### AI motion prompt, to animate each still photo (image-to-video, 4:5)
```
Image-to-video, 4:5 aspect ratio, 1080x1350. Keep the dish exactly as in the source photo. Add a slow cinematic push-in (about 5 percent), gentle rising steam, subtle flicker of warm kitchen light on the dark wooden table. No new objects, no hands, no text, no camera shake. 3 seconds, seamless and calm.
```

---

## Video 3: Website demo loop (goes in the "How it works" slot)

- **Ratio:** 9:16, 1080 x 1920. It sits inside a phone frame on the page.
- **Length:** 12 to 15 s, loops cleanly
- **Size target:** under 2 MB (H.264 MP4, no audio track)
- **Content:** a real screen recording, not AI. Open the PDF in the phone's Files app. Show the index, tap "Tired", land on a recipe, scroll the ingredients and swaps, tap back, tap the 4 Week Dinner Plans, show Week 1.

### How to add it to the site
1. Export `demo.mp4` (and a first-frame screenshot `demo-poster.webp`).
2. Put both in `public/video/`.
3. In `src/lib/content.ts`, set `DEMO_VIDEO.src = "/video/demo.mp4"` and `poster = "/video/demo-poster.webp"`.
4. Rebuild. The video appears muted and looping, and it only downloads when someone scrolls to it.

## Priority order

1. Film Video 1 yourselves (one afternoon, one phone).
2. Build Video 2 from the photos you already have (about 1 hour in CapCut).
3. Screen-record Video 3 and drop it into the site.
4. Test 3 different openings for Video 1 (the first 2 seconds decide most of the result): "It's 9pm, you're tired...", "This is my fourth $18 dinner this week", "Cooking for one is weirdly hard, right?"
