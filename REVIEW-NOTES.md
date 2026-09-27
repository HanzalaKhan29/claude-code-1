# Solo & Starving? landing page: first draft review notes

Draft for review before any deploy. Nothing here is live.

## Run it locally

```bash
npm install
npm run dev        # http://localhost:3000
npm run build      # production build check
```

Stack: Next.js 16 (App Router, static export to `out/`), Tailwind CSS v4, Motion, Phosphor icons. Fonts are self-hosted through `next/font` (Bricolage Grotesque, Geist, Geist Mono).

## Deploy

The site builds to a plain static folder (`out/`), so any host works:

- **Netlify drag and drop:** run `npm run build`, then drag the `out` folder (or the ZIP of it) onto the project's **Deploys** page.
- **Netlify from GitHub:** link this repo in the project's build settings. `netlify.toml` already sets the build command and publish folder.
- **Vercel:** import the repo. It detects Next.js with no extra setup.

Security and cache headers are in `public/_headers` (Netlify reads this file; on Vercel, move them to `vercel.json`).

Every fact, price and link on the page lives in **`src/lib/content.ts`**. Change prices, Gumroad URLs, the launch deadline, recipes or FAQ there, not in the components.

## Ported from the live site (soloandstarving.store)

Everything that does real work on the live site is now in this build:

| Live site feature | Where it is now |
|---|---|
| **Meta Pixel `1608472060834274`** with PageView, ViewContent, InitiateCheckout (same values) | `src/lib/tracking.ts`. Loads through the consent banner |
| Cookie consent (UK/EU opt in before the pixel, everyone else counted and can opt out, same `ssCookieConsent` key) | `src/components/consent.tsx` |
| Quiz custom events: QuizStart, QuizComplete, ViewPersonalizedPlan | Quiz, same names and data |
| `?quiz=1` links (ads, bio, DMs) open straight into the quiz | Head script moves the quiz above the hero, no flash |
| Gumroad affiliate ids (`?a=`, `?ref=`, `?aff=`...) remembered 30 days and added to every checkout link | `attribute()` in `tracking.ts` |
| UTM pass-through to Gumroad | Same function |
| Local currency hint ("About 17,71 €, charged in USD") by time zone | Under both prices and in the quiz result |
| The full quiz: exact 5 questions, the personal reply after each answer, "Building your plan" steps | `src/components/quiz.tsx` |
| Quiz result: dinner type, chips, diagnosis, **real starting week from the 4 Week Dinner Plans**, 4-week path, how each plan fixes your problem, takeout math with payback, both offers | Quiz result |
| Returning visitors see their saved result (`ssQuizV2` key) | Quiz |
| All 28 dinners of the 4 Week Dinner Plans (names, recipe numbers, times, costs) | New section "A month of dinners, already decided" |
| Six "reasons" (someone far away, tired of takeout, no hour to spare, never learned, decision fatigue, tight budget) | New section |
| All research stats: USDA 58.9%, BLS $3,945 vs $6,224, Wolfson & Bleich, Cooper 46%, Ducrot 40,554, WRAP 60% | Honest proof section |
| Free-recipe email capture (same Brevo list and honeypot) | "Prefer to read first?" section |
| Guide library link (~55 guides) | Same section + footer |
| Custom Plan extras: "one recipe you've always wanted to master", personal message page, gift use | Pricing |
| Worldwide / charged in USD / VAT / no account / secure Gumroad checkout | Trust row under pricing |
| Structured data: Organization, WebSite, both Products (shipping + no-returns policy), FAQ | `page.tsx` |
| Pinterest domain verification tag | `layout.tsx` |
| Favicon from the "&" logo mark | `src/app/icon.png`, `apple-icon.png` |

### Deliberately NOT ported (and why)

- **"Your quiz price is held for 25:00", then it jumps to $35.** The same page still sells $19.25 for 3 more days, so the timer is fake urgency. Buyers who reload see it, and it's the kind of thing that gets ads flagged. The real launch countdown (to Oct 1) stays.
- **"$62 worth of content" and "private meal planning usually costs $150 to $300".** Neither item was ever sold at those prices, so they're invented anchors. $35 is the real regular price and is used as the anchor.
- **"Zero-risk guarantee, no questions asked".** That contradicts your own no-refunds policy (the FAQ and the schema both say no returns). Kept the honest version: "we fix it, swap it, or make it right".
- **GA4.** The live code still has the placeholder `G-XXXXXXXXXX`, so GA4 was never actually running. Send me a real Measurement ID and I'll add it behind the same consent banner.
- **The 55 guide pages.** They stay on soloandstarving.store/guides/ and are linked. If this site replaces that domain, the guides have to move with it (they're a real SEO asset, don't lose them).

## The big idea

Both old sites buried the one thing competitors don't have: **every recipe is tagged by energy (Normal 30 min, Tired 20 min, Dead Tired 10 min)**. The new page is built around it:

- Headline: "Dinner for one, sorted by how tired you are."
- The hero visual is an interactive energy switcher: tap Normal / Tired / Dead tired and the dish, time, cost and protein change. Visitors use the product's core mechanic in the first 3 seconds.

## Flaws fixed

### From your preview (solo-starving-design-preview.netlify.app)

| Problem | Fix |
|---|---|
| Typo "45% offends in" in the hero | Countdown moved to a clean top bar: "Launch price, 45% off. Goes up to $35 in 3d 09h..." |
| Research numbers rendered as "0%" and "0" until JS animated them (bad for slow phones, screenshots, SEO) | Numbers are real text in the HTML. No count-up |
| "46% less food wasted" cited to "van der Werf et al. (2021)" but the real site cites Cooper et al. (2023) with a different claim | Uses the real site's wording and source |
| Dessert card said "Recipe" followed by a dash and no number | Dessert shows no number |
| Quiz sat below 6 recipe cards and had no visible result on page load | Quiz is its own section, gives a type, starting mode, 2 recipes, a yearly takeout estimate and a plan recommendation |
| Hero led with the quiz, so cold ad traffic had to do homework before seeing price or food | Hero leads with the promise, food photo and a direct buy button. Quiz is the secondary option |
| Pale lavender page made the moody dark food photos look pasted in | Dark "9pm kitchen" theme that matches the photography |
| Netlify "Powered by" badge floating over the nav | Gone (it's a Netlify thing; Vercel has none) |
| No mobile buy button once you scroll | Sticky mobile buy bar with price, hides whenever another buy button is on screen |

### From the real site (soloandstarving.store)

| Problem | Fix |
|---|---|
| Emoji used as icons everywhere (🍳 ⏱ 💸 🎯 🛡️ 📧) | One icon family (Phosphor), no emoji |
| Research section and FAQ appear **twice** | Each appears once |
| 3 competing CTAs in the hero (quiz, "see both plans", worldwide badge) | 1 primary, 1 secondary |
| Hero crammed with badges, a USDA stat box and a tiny product thumbnail | Hero has 4 elements max; the food is the visual |
| "$62 total value" stack ($41 + $9 + $12) | Removed. Made-up component prices read as fake to TikTok/FB buyers and hurt trust. Anchor is the real $35 regular price |
| Cookie banner covering the first screen | No tracking scripts yet, so no banner needed (see open question 4) |
| Two "promise" boxes per card plus a separate "no reviews" box | One honest proof section plus one line of reassurance under pricing |

## Page structure (in order)

1. Launch bar (live countdown, disappears after the deadline)
2. Hero: promise + energy switcher + buy button
3. Facts strip: 88 recipes, 6 cuisines, 10-30 min, 2 portions
4. "Cooking for one is weirdly hard": an evening timeline (6:30pm, 7:15pm, 9:00pm) ending with the cookbook fix
5. How it works (3 steps)
6. Six real recipe pages (swipeable)
7. Honest proof: "No reviews yet. So here's the research instead." + who made it
8. Everything you get (bundle mockup + contents)
9. Quiz
10. Pricing (Starter recommended, Custom Plan)
11. Is this for you / not for you
12. FAQ (8 questions, with FAQ schema for Google)
13. Final CTA over the caprese photo

## Built-in conversion mechanics

- **Launch price auto-switches.** At midnight New York time on Oct 1 the countdown disappears, prices change to $35, and buttons switch to the non-discount Gumroad link. No manual edit needed.
- **UTM pass-through.** `?utm_source=tiktok&utm_campaign=...` on the ad URL is copied onto every Gumroad link, so Gumroad's sales data shows which ad sold.
- **Checkout events ready.** Every buy button fires `InitiateCheckout` to the Meta and TikTok pixels if you install them.
- **Quiz recommends the $69 plan** only when it fits (allergies or a gift). Everyone else is sent to the $19.25 bundle.

## Hero copy: 3 directions (built with A)

| | Headline | Why |
|---|---|---|
| **A (recommended, built)** | Dinner for one, sorted by how tired you are. | The unique mechanic is the headline. Nobody else owns "energy level" |
| B | Stop paying $18 for dinner you could make in 15 minutes. | Money angle. Best if your ads talk about takeout costs |
| C | What's your solo dinner type? | Quiz-first. Only if your ads literally ask this question (message match) |

**Match the hero to the ad.** If the TikTok/FB creative says "sick of takeout", switch to B.

## Open questions for you (please confirm before deploy)

1. ~~Regular Gumroad link~~ Confirmed from the live code: `.../l/Soloandstarving?wanted=true`.
2. ~~Portions~~ Confirmed from the live quiz: "2 portions: dinner tonight, lunch tomorrow".
3. **Teriyaki photo.** The file is named `japanese-teriyaki-pork-rice` but the 4 Week Plan calls recipe 55 "Teriyaki Chicken Rice Bowl". Make sure the photo shows chicken.
4. **TikTok Pixel.** The live site only has Meta. If you run TikTok ads, send the TikTok Pixel ID.
5. **Privacy page.** The footer links to the existing `soloandstarving.store/privacy`. If this site replaces that domain, the privacy page must move over too (and a Terms page if you have one).
6. **Your 9 images and the strategy PDF.** Your Windows folder (`C:\Users\imtiy\Downloads\...`) is on your computer, and this build runs in the cloud, so I couldn't open it. I used the images already on your preview site and the bundle mockup + OG image from the real site. To use the 9 planned images, add them to `public/images/` (or upload them to this chat) and I'll place them. Share the strategy PDF the same way and I'll check the page against it.

## Skills applied

See VIDEO-PLAN.md for the video recommendation and prompts.

landing-page, design-taste-frontend, ogilvy-copywriting, pricing-page, motion-framer, premium-site-builder (anti-slop rules, no invented proof, no em dashes). Not installed in this environment, so not used: web3d-integration-patterns, vercel-optimize, animejs, vercel-react-view-transitions, meta-skills:modern-web-design, optimize_lottie. Deliberately left out: 3D and Lottie. A $19 impulse buy from a TikTok ad needs a fast page more than it needs a 3D scene. Both would add hundreds of KB to a page that works on mobile data.

## Verified in this draft

- `npm run build` passes, TypeScript clean, page is fully static
- 1440px desktop and 390px mobile: no horizontal scroll, no console errors
- Energy switcher, all 5 quiz steps, result, and every Gumroad link checked in a real browser (Playwright)
- UTM pass-through confirmed on the live links
- Zero em dashes in the copy

- Oct 1 switch-over tested by fast-forwarding the browser clock: countdown disappears, price shows $35, buttons use the regular Gumroad link

Not verified yet: Lighthouse scores, real iOS Safari.
