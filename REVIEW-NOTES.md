# Solo & Starving? landing page: first draft review notes

Draft for review before any deploy. Nothing here is live.

## Run it locally

```bash
npm install
npm run dev        # http://localhost:3000
npm run build      # production build check
```

Stack: Next.js 16 (App Router, fully static), Tailwind CSS v4, Motion, Phosphor icons. Fonts are self-hosted through `next/font` (Bricolage Grotesque, Geist, Geist Mono).

Every fact, price and link on the page lives in **`src/lib/content.ts`**. Change prices, Gumroad URLs, the launch deadline, recipes or FAQ there, not in the components.

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
| Dessert card said "Recipe —" | Dessert shows no number |
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

1. **Regular Gumroad link after Oct 1.** I assumed `https://hamzaouiy4.gumroad.com/l/Soloandstarving?wanted=true`. Confirm.
2. **Portions.** The preview says "every recipe makes 2 servings"; the real site's FAQ says "portioned for one". The recipe data (300 g chicken, 4 eggs) points to 2 portions for one person. The page says "2 portions: tonight and tomorrow". Confirm this is right.
3. **Teriyaki photo.** The file is named `japanese-teriyaki-pork-rice` but the recipe is chicken. Make sure the photo matches the recipe or rename one.
4. **Tracking + consent.** No pixels are installed. If you add Meta/TikTok pixels and sell to the EU/UK, you need a consent banner first. Tell me which pixels and I'll wire them in properly.
5. **Privacy page.** The footer links to the existing `soloandstarving.store/privacy`. If this site replaces that domain, the privacy page must move over too (and a Terms page if you have one).
6. **Your 9 images and the strategy PDF.** Your Windows folder (`C:\Users\imtiy\Downloads\...`) is on your computer, and this build runs in the cloud, so I couldn't open it. I used the images already on your preview site and the bundle mockup + OG image from the real site. To use the 9 planned images, add them to `public/images/` (or upload them to this chat) and I'll place them. Share the strategy PDF the same way and I'll check the page against it.

## Skills applied

landing-page, design-taste-frontend, ogilvy-copywriting, pricing-page, motion-framer, premium-site-builder (anti-slop rules, no invented proof, no em dashes). Not installed in this environment, so not used: web3d-integration-patterns, vercel-optimize, animejs, vercel-react-view-transitions, meta-skills:modern-web-design, optimize_lottie. Deliberately left out: 3D and Lottie. A $19 impulse buy from a TikTok ad needs a fast page more than it needs a 3D scene. Both would add hundreds of KB to a page that works on mobile data.

## Verified in this draft

- `npm run build` passes, TypeScript clean, page is fully static
- 1440px desktop and 390px mobile: no horizontal scroll, no console errors
- Energy switcher, all 5 quiz steps, result, and every Gumroad link checked in a real browser (Playwright)
- UTM pass-through confirmed on the live links
- Zero em dashes in the copy

- Oct 1 switch-over tested by fast-forwarding the browser clock: countdown disappears, price shows $35, buttons use the regular Gumroad link

Not verified yet: Lighthouse scores, real iOS Safari.
