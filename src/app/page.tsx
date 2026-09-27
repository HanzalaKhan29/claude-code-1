import Image from "next/image";
import {
  ArrowRight,
  Check,
  X,
  Plus,
  EnvelopeSimple,
  ShieldCheck,
  DownloadSimple,
  Lightning,
} from "@phosphor-icons/react/ssr";
import { FAQ, LINKS, MODES, PRICING, RECIPES, RESEARCH, type Recipe } from "@/lib/content";
import { LaunchBar, LaunchOnly, Countdown } from "@/components/launch-bar";
import { CheckoutLink, StarterPrice } from "@/components/checkout-link";
import { ModeSwitcher } from "@/components/mode-switcher";
import { Quiz } from "@/components/quiz";
import { Reveal } from "@/components/reveal";
import { StickyBuy } from "@/components/sticky-buy";

export default function Page() {
  return (
    <>
      <StructuredData />
      <LaunchBar />
      <Nav />
      <main>
        <Hero />
        <Facts />
        <Evening />
        <HowItWorks />
        <Recipes />
        <Research />
        <Bundle />
        <QuizSection />
        <Pricing />
        <Fit />
        <Faq />
        <FinalCta />
      </main>
      <Footer />
      <StickyBuy />
    </>
  );
}

/* ---------------------------------------------------------------- nav */

function Wordmark() {
  return (
    <span className="font-display text-[19px] font-bold tracking-tight text-cream">
      Solo <span className="text-accent">&amp;</span> Starving?
    </span>
  );
}

function Nav() {
  return (
    <header className="sticky top-0 z-40 border-b border-line bg-ink/80 backdrop-blur-xl">
      <nav className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6" aria-label="Main">
        <a href="#top" aria-label="Solo and Starving, back to top">
          <Wordmark />
        </a>
        <div className="flex items-center gap-7">
          <ul className="hidden items-center gap-7 text-sm text-muted md:flex">
            <li><a className="transition-colors hover:text-cream" href="#recipes">Recipes</a></li>
            <li><a className="transition-colors hover:text-cream" href="#quiz">Quiz</a></li>
            <li><a className="transition-colors hover:text-cream" href="#offer">Pricing</a></li>
            <li><a className="transition-colors hover:text-cream" href="#faq">FAQ</a></li>
          </ul>
          <CheckoutLink plan="starter" placement="nav" className="btn btn-primary hidden px-4 py-2 text-sm md:inline-flex">
            Get the cookbook
          </CheckoutLink>
        </div>
      </nav>
    </header>
  );
}

/* ---------------------------------------------------------------- hero */

function Hero() {
  return (
    <section id="top" className="relative overflow-hidden">
      {/* warm kitchen-light glow behind the photo, tinted to the food, not the accent */}
      <div
        aria-hidden
        className="pointer-events-none absolute top-[-10%] right-[-10%] h-[680px] w-[680px] rounded-full opacity-40 blur-3xl"
        style={{ background: "radial-gradient(closest-side, rgb(196 106 58 / 0.35), transparent)" }}
      />
      {/* Mobile order: promise, food, buttons. Desktop: copy left, switcher right. */}
      <div className="relative mx-auto grid max-w-7xl gap-8 px-4 pt-8 pb-14 sm:px-6 lg:grid-cols-[1.05fr_1fr] lg:gap-x-16 lg:gap-y-0 lg:pt-14 lg:pb-20">
        <Reveal className="lg:col-start-1 lg:row-start-1 lg:self-end">
          <h1 className="max-w-[14ch] font-display text-[40px] leading-[0.98] font-bold tracking-[-0.035em] text-cream sm:text-6xl lg:text-[72px]">
            Dinner for one, sorted by how <em className="font-bold text-accent not-italic">tired</em> you are.
          </h1>
          <p className="mt-5 max-w-[44ch] text-lg leading-relaxed text-muted lg:mt-6">
            88 beginner recipes for one, ready in 10 to 30 minutes. Pick your energy level, open that page, eat tonight.
          </p>
        </Reveal>
        <Reveal delay={0.1} className="lg:col-start-2 lg:row-span-2 lg:row-start-1">
          <ModeSwitcher />
        </Reveal>
        <Reveal delay={0.05} className="lg:col-start-1 lg:row-start-2 lg:self-start">
          <div id="hero-cta" className="flex flex-col gap-3 sm:flex-row sm:items-center lg:mt-8">
            <CheckoutLink plan="starter" placement="hero" className="btn btn-primary px-7 py-4 text-base">
              <span>
                Get the cookbook for <StarterPrice />
              </span>
              <ArrowRight size={18} weight="bold" aria-hidden />
            </CheckoutLink>
            <a href="#quiz" className="btn btn-ghost px-7 py-4 text-base">
              Find my dinner type
            </a>
          </div>
          <p className="mt-5 flex items-center gap-2 text-sm text-faint">
            <DownloadSimple size={16} weight="bold" aria-hidden className="shrink-0 text-muted" />
            Instant PDF download. One-time payment, no subscription.
          </p>
        </Reveal>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- facts */

function Facts() {
  const facts = [
    ["88", "recipes for one"],
    ["6", "cuisines, from Mexican to Japanese"],
    ["10-30", "minutes per dinner"],
    ["2", "portions each: tonight and tomorrow"],
  ];
  return (
    <section aria-label="What's in the cookbook" className="border-y border-line bg-night">
      <dl className="mx-auto grid max-w-7xl grid-cols-2 px-4 sm:px-6 lg:grid-cols-4">
        {facts.map(([n, l], i) => (
          <div
            key={l}
            className={`py-6 sm:py-8 ${i % 2 === 1 ? "pl-5 sm:pl-8" : "pr-5 sm:pr-8"} ${
              i > 0 ? "lg:border-l lg:border-line lg:pl-8" : ""
            } ${i > 1 ? "border-t border-line lg:border-t-0" : ""} ${i % 2 === 1 ? "border-l border-line" : ""}`}
          >
            <dt className="sr-only">{l}</dt>
            <dd>
              <span className="block font-display text-4xl font-bold tracking-tight text-cream sm:text-5xl">{n}</span>
              <span className="mt-1 block text-sm text-muted">{l}</span>
            </dd>
          </div>
        ))}
      </dl>
    </section>
  );
}

/* ---------------------------------------------------------------- problem */

function Evening() {
  const beats = [
    { time: "6:30pm", title: "Still no plan for dinner.", body: "You open the fridge. Half a bag of spinach looks back." },
    {
      time: "7:15pm",
      title: "The recipe says \"sauté until fragrant\".",
      body: "Fragrant like what? It serves four and you're one person.",
    },
    { time: "9:00pm", title: "Your thumb opens the delivery app.", body: "Another $18 with fees. Again. The spinach goes in the bin on Thursday." },
  ];
  return (
    <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:py-32">
      <div className="grid gap-12 lg:grid-cols-[0.9fr_1.1fr] lg:gap-20">
        <Reveal className="lg:sticky lg:top-28 lg:self-start">
          <h2 className="max-w-[16ch] font-display text-4xl font-bold leading-[1.02] tracking-[-0.03em] text-cream sm:text-5xl">
            Cooking for one is weirdly hard.
          </h2>
          <p className="mt-5 max-w-[42ch] text-lg leading-relaxed text-muted">
            It's not a skills problem. Recipes are written for families, and by 9pm you have zero decisions left.
          </p>
        </Reveal>
        <ol className="relative">
          <span aria-hidden className="absolute top-3 bottom-3 left-[5px] w-px bg-line-strong sm:left-[7px]" />
          {beats.map((b, i) => (
            <li key={b.time} className="relative pb-12 pl-10 last:pb-0 sm:pl-14">
              <span
                aria-hidden
                className="absolute top-2 left-0 size-[11px] rounded-full bg-ink shadow-[0_0_0_2px_var(--color-faint)] sm:size-[15px]"
              />
              <Reveal delay={i * 0.06}>
                <p className="font-mono text-sm text-faint">{b.time}</p>
                <p className="mt-2 font-display text-2xl font-semibold leading-snug tracking-tight text-cream sm:text-3xl">
                  {b.title}
                </p>
                <p className="mt-2 max-w-[46ch] text-muted">{b.body}</p>
              </Reveal>
            </li>
          ))}
          <li className="relative pl-10 pt-12 sm:pl-14">
            <span aria-hidden className="absolute top-14 left-0 size-[11px] rounded-full bg-accent sm:size-[15px]" />
            <Reveal>
              <p className="font-mono text-sm text-accent">6:45pm, with the cookbook</p>
              <p className="mt-2 font-display text-2xl font-semibold leading-snug tracking-tight text-cream sm:text-3xl">
                You check your energy, tap Tired, and you're eating by 7:05.
              </p>
            </Reveal>
          </li>
        </ol>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- how it works */

function HowItWorks() {
  const steps = [
    {
      verb: "Check your energy",
      body: "Every recipe is tagged by effort, not just cuisine. Normal, Tired or Dead tired.",
      aside: `${MODES.normal.minutes} / ${MODES.tired.minutes} / ${MODES.dead.minutes} min`,
    },
    {
      verb: "Tap to the recipe",
      body: "The interactive index jumps straight to the page. Prep list, tools, swaps and method in order.",
      aside: "One tap",
    },
    {
      verb: "Cook once, eat twice",
      body: "Each recipe makes 2 portions for one person. Dinner tonight, sorted lunch tomorrow.",
      aside: "2 portions",
    },
  ];
  return (
    <section aria-labelledby="how-title" className="border-t border-line bg-night">
      <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:py-28">
        <Reveal>
          <h2 id="how-title" className="font-display text-4xl font-bold tracking-[-0.03em] text-cream sm:text-5xl">
            How it works
          </h2>
        </Reveal>
        <ol className="mt-12 divide-y divide-line border-y border-line">
          {steps.map((s, i) => (
            <li key={s.verb}>
              <Reveal delay={i * 0.05} className="grid gap-3 py-8 md:grid-cols-[minmax(0,1fr)_minmax(0,1.3fr)_8rem] md:items-baseline md:gap-10">
                <p className="font-display text-2xl font-semibold tracking-tight text-cream sm:text-3xl">{s.verb}</p>
                <p className="max-w-[52ch] text-muted">{s.body}</p>
                <p className="font-mono text-sm text-accent md:text-right">{s.aside}</p>
              </Reveal>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- recipes */

function Recipes() {
  return (
    <section id="recipes" aria-labelledby="recipes-title" className="py-20 lg:py-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6">
        <Reveal>
          <h2 id="recipes-title" className="max-w-[18ch] font-display text-4xl font-bold leading-[1.02] tracking-[-0.03em] text-cream sm:text-5xl">
            Six real pages from the book.
          </h2>
          <p className="mt-4 max-w-[52ch] text-lg text-muted">
            Every one of the 88 recipes shows time, cost per serving, calories, protein and easy swaps before you start.
          </p>
        </Reveal>
      </div>
      <div className="no-scrollbar relative mt-12 flex snap-x snap-mandatory gap-4 overflow-x-auto px-4 pb-4 sm:gap-5 sm:px-6 lg:scroll-px-[max(1.5rem,calc((100vw_-_80rem)/2_+_1.5rem))] lg:px-[max(1.5rem,calc((100vw_-_80rem)/2_+_1.5rem))]">
        {RECIPES.map((r) => (
          <RecipeCard key={r.slug} r={r} />
        ))}
      </div>
      <p className="mx-auto mt-6 max-w-7xl px-4 text-sm text-faint sm:px-6">Swipe for more.</p>
    </section>
  );
}

function RecipeCard({ r }: { r: Recipe }) {
  return (
    <article className="group relative w-[78vw] max-w-[340px] shrink-0 snap-start overflow-hidden rounded-card bg-surface shadow-[inset_0_0_0_1px_var(--color-line)] sm:w-[340px]">
      <div className="relative aspect-[4/3] overflow-hidden">
        <Image
          src={r.image}
          alt={r.name}
          fill
          sizes="340px"
          className="object-cover transition-transform duration-700 ease-[var(--ease-out-expo)] group-hover:scale-[1.04]"
        />
      </div>
      <div className="p-5">
        <p className="text-xs text-faint">
          {r.cuisine}
          {r.number ? `, recipe ${r.number}` : ""}
        </p>
        <h3 className="mt-1 font-display text-xl font-semibold tracking-tight text-cream">{r.name}</h3>
        <dl className="mt-3 flex flex-wrap gap-x-4 gap-y-1 font-mono text-[13px] text-muted">
          <div><dt className="sr-only">Time</dt><dd>{r.minutes} min</dd></div>
          <div><dt className="sr-only">Cost per serving</dt><dd>{r.cost}/serving</dd></div>
          <div><dt className="sr-only">Protein</dt><dd>{r.protein}g protein</dd></div>
          <div><dt className="sr-only">Calories</dt><dd>{r.kcal} kcal</dd></div>
        </dl>
        <p className="mt-3 inline-flex rounded-full bg-accent-soft px-2.5 py-1 text-xs font-medium text-accent">
          {MODES[r.mode].label} mode
        </p>
        <ul className="mt-4 space-y-1 text-sm text-cream/90">
          {r.ingredients.map((i) => (
            <li key={i}>{i}</li>
          ))}
          <li className="text-faint">+ {r.more} more</li>
        </ul>
        <p className="mt-4 border-t border-line pt-4 text-[13px] leading-relaxed text-muted">
          <span className="font-semibold text-cream">Swaps: </span>
          {r.swaps}
        </p>
      </div>
    </article>
  );
}

/* ---------------------------------------------------------------- research */

function Research() {
  return (
    <section aria-labelledby="research-title" className="border-t border-line">
      <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:py-28">
        <Reveal className="max-w-3xl">
          <p className="mb-4 text-xs font-semibold tracking-[0.16em] text-accent uppercase">Honest proof</p>
          <h2 id="research-title" className="font-display text-4xl font-bold leading-[1.02] tracking-[-0.03em] text-cream sm:text-5xl">
            No reviews yet. So here's the research instead.
          </h2>
          <p className="mt-5 max-w-[56ch] text-lg leading-relaxed text-muted">
            This cookbook just launched, so we won't show you stars from strangers. Here is what studies say about
            eating from a plan.
          </p>
        </Reveal>
        <div className="mt-14 grid gap-10 md:grid-cols-3 md:gap-8">
          {RESEARCH.map((r, i) => (
            <Reveal key={r.figure} delay={i * 0.06} className="border-t border-line-strong pt-6">
              <p className="font-display text-6xl font-bold tracking-[-0.04em] text-cream">{r.figure}</p>
              <p className="mt-1 font-semibold text-cream">{r.label}</p>
              <p className="mt-3 text-muted">{r.body}</p>
              <p className="mt-4 text-xs text-faint">{r.source}</p>
            </Reveal>
          ))}
        </div>
        <Reveal className="mt-16 flex flex-col gap-4 rounded-card bg-surface p-6 shadow-[inset_0_0_0_1px_var(--color-line)] sm:flex-row sm:items-center sm:justify-between sm:p-8">
          <p className="max-w-[60ch] text-cream">
            <span className="font-semibold">Made by Yassine &amp; Nourhene,</span>{" "}
            <span className="text-muted">
              two people who cook this way every night. Every question goes to a real inbox and gets a real reply.
            </span>
          </p>
          <a
            href={`mailto:${LINKS.email}`}
            className="inline-flex shrink-0 items-center gap-2 text-sm font-medium text-accent hover:underline"
          >
            <EnvelopeSimple size={16} weight="bold" aria-hidden />
            {LINKS.email}
          </a>
        </Reveal>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- bundle */

function Bundle() {
  const items = [
    { t: "The interactive cookbook", d: "88 recipes, 6 cuisines, tagged by energy. Tap from the index to any page." },
    { t: "Start Here guide", d: "Heat levels, rice, pasta, and exactly when chicken is done. Written for total beginners." },
    { t: "Bonus: Solo Meal Planner & Grocery Kit", d: "4 pages to plan the week and shop once." },
    { t: "Bonus: 4 Week Dinner Plans", d: "A month of dinners already decided, with a shopping list for every week." },
  ];
  return (
    <section aria-labelledby="bundle-title" className="border-t border-line bg-night">
      <div className="mx-auto grid max-w-7xl gap-12 px-4 py-20 sm:px-6 lg:grid-cols-2 lg:items-center lg:gap-20 lg:py-28">
        <Reveal className="relative order-last lg:order-first">
          <div className="relative mx-auto aspect-square max-w-[560px] overflow-hidden rounded-card shadow-[0_40px_80px_-30px_rgb(0_0_0/0.7)]">
            <Image
              src="/images/bundle-mockup.webp"
              alt="The Solo Starter Bundle: the Solo & Starving? cookbook with the Meal Planner and Dinner Plans bonus pages"
              fill
              sizes="(min-width: 1024px) 560px, 100vw"
              className="object-cover"
            />
          </div>
        </Reveal>
        <div>
          <Reveal>
            <h2 id="bundle-title" className="max-w-[16ch] font-display text-4xl font-bold leading-[1.02] tracking-[-0.03em] text-cream sm:text-5xl">
              Everything you get for <StarterPrice />.
            </h2>
          </Reveal>
          <ul className="mt-10 space-y-6">
            {items.map((it, i) => (
              <li key={it.t}>
                <Reveal delay={i * 0.05} className="flex gap-4">
                  <span className="mt-1 grid size-6 shrink-0 place-items-center rounded-full bg-accent-soft text-accent">
                    <Check size={14} weight="bold" aria-hidden />
                  </span>
                  <span>
                    <span className="block font-semibold text-cream">{it.t}</span>
                    <span className="mt-1 block text-muted">{it.d}</span>
                  </span>
                </Reveal>
              </li>
            ))}
          </ul>
          <Reveal className="mt-10 flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-6">
            <CheckoutLink plan="starter" placement="bundle" className="btn btn-primary px-7 py-4 text-base">
              Get the cookbook
              <ArrowRight size={18} weight="bold" aria-hidden />
            </CheckoutLink>
            <p className="text-sm text-faint">Works on phone, tablet and laptop.</p>
          </Reveal>
        </div>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- quiz */

function QuizSection() {
  return (
    <section id="quiz" aria-labelledby="quiz-title" className="border-t border-line">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-20 sm:px-6 lg:grid-cols-[0.8fr_1.2fr] lg:gap-16 lg:py-28">
        <Reveal className="lg:pt-6">
          <h2 id="quiz-title" className="max-w-[14ch] font-display text-4xl font-bold leading-[1.02] tracking-[-0.03em] text-cream sm:text-5xl">
            What's your solo dinner type?
          </h2>
          <p className="mt-5 max-w-[40ch] text-lg leading-relaxed text-muted">
            Five quick questions. You get your starting mode, two recipes to cook first, and what takeout is really costing
            you.
          </p>
        </Reveal>
        <Reveal delay={0.08}>
          <Quiz />
        </Reveal>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- pricing */

function Pricing() {
  const starter = [
    "88 recipes across 6 cuisines, tagged by energy",
    "Start Here guide for total beginners",
    "Cost, calories, protein and swaps on every recipe",
    "Bonus: Solo Meal Planner & Grocery Kit",
    "Bonus: 4 Week Dinner Plans with shopping lists",
    "Instant download, yours to keep",
  ];
  const custom = [
    "Everything in the Starter Bundle",
    "Built around your favorite cuisines and schedule",
    "Works around allergies and foods you won't eat",
    "Grocery prices adjusted to your country",
    "Optional personal message page, great as a gift",
    "Written by a real person, emailed in 2 to 3 days",
  ];
  return (
    <section id="offer" aria-labelledby="offer-title" className="border-t border-line bg-night">
      <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:py-28">
        <Reveal className="mx-auto max-w-2xl text-center">
          <p className="mb-4 text-xs font-semibold tracking-[0.16em] text-accent uppercase">Pricing</p>
          <h2 id="offer-title" className="font-display text-4xl font-bold leading-[1.02] tracking-[-0.03em] text-cream sm:text-5xl">
            Pick the version that fits your week.
          </h2>
          <LaunchOnly>
            <p className="mt-4 text-muted">
              Launch price ends in <Countdown className="text-cream" />
            </p>
          </LaunchOnly>
        </Reveal>

        <div className="mx-auto mt-12 grid max-w-5xl gap-5 md:grid-cols-2">
          <Reveal className="relative flex flex-col rounded-card bg-surface p-6 shadow-[inset_0_0_0_2px_var(--color-accent)] sm:p-8">
            <span className="absolute -top-3 left-6 rounded-full bg-accent px-3 py-1 text-xs font-semibold text-accent-ink sm:left-8">
              Best place to start
            </span>
            <h3 className="font-display text-2xl font-semibold text-cream">The Starter Bundle</h3>
            <p className="mt-1 text-muted">Start cooking tonight.</p>
            <p className="mt-6 flex items-baseline gap-3">
              <StarterPrice className="font-display text-5xl font-bold tracking-tight text-cream" />
              <LaunchStrike />
            </p>
            <ul className="mt-6 space-y-3 text-[15px]">
              {starter.map((s) => (
                <li key={s} className="flex gap-3 text-cream/90">
                  <Check size={18} weight="bold" className="mt-0.5 shrink-0 text-accent" aria-hidden />
                  {s}
                </li>
              ))}
            </ul>
            <CheckoutLink plan="starter" placement="pricing" className="btn btn-primary mt-8 w-full px-6 py-4 text-base">
              Get the cookbook
              <ArrowRight size={18} weight="bold" aria-hidden />
            </CheckoutLink>
          </Reveal>

          <Reveal delay={0.06} className="flex flex-col rounded-card bg-surface p-6 shadow-[inset_0_0_0_1px_var(--color-line)] sm:p-8">
            <h3 className="font-display text-2xl font-semibold text-cream">The Custom Plan</h3>
            <p className="mt-1 text-muted">Built by hand around one person's life.</p>
            <p className="mt-6 font-display text-5xl font-bold tracking-tight text-cream">${PRICING.customPrice}</p>
            <ul className="mt-6 space-y-3 text-[15px]">
              {custom.map((s) => (
                <li key={s} className="flex gap-3 text-cream/90">
                  <Check size={18} weight="bold" className="mt-0.5 shrink-0 text-accent" aria-hidden />
                  {s}
                </li>
              ))}
            </ul>
            <CheckoutLink plan="custom" placement="pricing" className="btn btn-ghost mt-auto w-full px-6 py-4 text-base">
              Get my custom plan
              <ArrowRight size={18} weight="bold" aria-hidden />
            </CheckoutLink>
          </Reveal>
        </div>

        <div className="mx-auto mt-10 grid max-w-5xl gap-6 text-sm text-muted sm:grid-cols-3">
          <p className="flex gap-3">
            <Lightning size={18} weight="bold" className="shrink-0 text-accent" aria-hidden />
            One-time payment through Gumroad. No subscription, no account.
          </p>
          <p className="flex gap-3">
            <ShieldCheck size={18} weight="bold" className="shrink-0 text-accent" aria-hidden />
            If a file won't open or something's off, we fix it, swap it, or make it right.
          </p>
          <p className="flex gap-3">
            <EnvelopeSimple size={18} weight="bold" className="shrink-0 text-accent" aria-hidden />
            VAT may be added at checkout depending on your country.
          </p>
        </div>
      </div>
    </section>
  );
}

function LaunchStrike() {
  return (
    <LaunchOnly>
      <span className="text-lg text-faint">
        <span className="line-through">${PRICING.regularPrice}</span> launch price
      </span>
    </LaunchOnly>
  );
}

/* ---------------------------------------------------------------- fit */

function Fit() {
  const yes = [
    "You cook for one, or mostly for yourself",
    "You're a beginner, or seriously out of practice",
    "You're a student or you work long days",
    "You want real meals without the takeout bill",
  ];
  const no = ["You want slow, fancy, four hour recipes", "You mainly cook for a big family", "You want a printed hardcover book"];
  return (
    <section aria-labelledby="fit-title" className="border-t border-line">
      <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:py-28">
        <Reveal>
          <h2 id="fit-title" className="font-display text-4xl font-bold tracking-[-0.03em] text-cream sm:text-5xl">
            Is this your kind of cookbook?
          </h2>
        </Reveal>
        <div className="mt-12 grid gap-12 md:grid-cols-[1.4fr_1fr] md:gap-16">
          <Reveal>
            <p className="font-semibold text-cream">Yes, if</p>
            <ul className="mt-4 space-y-4">
              {yes.map((y) => (
                <li key={y} className="flex gap-3 text-lg text-cream/90">
                  <Check size={20} weight="bold" className="mt-1 shrink-0 text-accent" aria-hidden />
                  {y}
                </li>
              ))}
            </ul>
          </Reveal>
          <Reveal delay={0.06}>
            <p className="font-semibold text-muted">Probably not, if</p>
            <ul className="mt-4 space-y-4">
              {no.map((n) => (
                <li key={n} className="flex gap-3 text-lg text-muted">
                  <X size={20} weight="bold" className="mt-1 shrink-0 text-faint" aria-hidden />
                  {n}
                </li>
              ))}
            </ul>
          </Reveal>
        </div>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- faq */

function Faq() {
  return (
    <section id="faq" aria-labelledby="faq-title" className="border-t border-line bg-night">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-20 sm:px-6 lg:grid-cols-[0.8fr_1.2fr] lg:gap-16 lg:py-28">
        <Reveal className="lg:sticky lg:top-28 lg:self-start">
          <h2 id="faq-title" className="font-display text-4xl font-bold leading-[1.02] tracking-[-0.03em] text-cream sm:text-5xl">
            Questions before you buy
          </h2>
          <p className="mt-5 text-muted">
            Something else?{" "}
            <a href={`mailto:${LINKS.email}`} className="text-accent underline-offset-4 hover:underline">
              Email us
            </a>
            . A real person answers.
          </p>
        </Reveal>
        <div className="divide-y divide-line border-y border-line">
          {FAQ.map((f) => (
            <details key={f.q} className="faq group">
              <summary className="flex cursor-pointer list-none items-center justify-between gap-6 py-5 text-left text-[17px] font-semibold text-cream">
                {f.q}
                <Plus
                  size={18}
                  weight="bold"
                  aria-hidden
                  className="shrink-0 text-muted transition-transform duration-300 group-open:rotate-45"
                />
              </summary>
              <p className="max-w-[62ch] pb-6 leading-relaxed text-muted">{f.a}</p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- final cta */

function FinalCta() {
  return (
    <section id="final-cta" className="relative isolate overflow-hidden border-t border-line">
      <Image
        src="/images/hero-caprese.webp"
        alt=""
        fill
        sizes="100vw"
        className="-z-10 object-cover object-[70%_center]"
      />
      <div aria-hidden className="absolute inset-0 -z-10 bg-gradient-to-r from-ink via-ink/85 to-ink/20" />
      <div className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:py-36">
        <Reveal className="max-w-xl">
          <h2 className="font-display text-4xl font-bold leading-[1.02] tracking-[-0.03em] text-cream sm:text-6xl">
            Tonight's dinner could already be sorted.
          </h2>
          <p className="mt-5 text-lg text-muted">88 recipes, 2 free planners, instant download.</p>
          <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-center">
            <CheckoutLink plan="starter" placement="final" className="btn btn-primary px-7 py-4 text-base">
              <span>
                Get the cookbook for <StarterPrice />
              </span>
              <ArrowRight size={18} weight="bold" aria-hidden />
            </CheckoutLink>
            <a href="#quiz" className="text-sm text-muted underline decoration-line-strong underline-offset-4 hover:text-cream">
              Not sure yet? Take the quiz
            </a>
          </div>
        </Reveal>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- footer */

function Footer() {
  return (
    <footer className="border-t border-line pb-24 md:pb-0">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-4 py-10 text-sm text-faint sm:px-6 md:flex-row md:items-center md:justify-between">
        <div>
          <Wordmark />
          <p className="mt-2">&copy; 2026 Y&amp;N Digital. Made by Yassine &amp; Nourhene.</p>
        </div>
        <ul className="flex flex-wrap gap-x-6 gap-y-2">
          <li><a className="hover:text-cream" href={LINKS.privacy}>Privacy</a></li>
          <li><a className="hover:text-cream" href={`mailto:${LINKS.email}`}>{LINKS.email}</a></li>
        </ul>
      </div>
    </footer>
  );
}

/* ---------------------------------------------------------------- schema */

function StructuredData() {
  const data = [
    {
      "@context": "https://schema.org",
      "@type": "Product",
      name: "Solo & Starving? The Interactive Cookbook",
      description: "88 beginner recipes for one, tagged by energy level, with 2 free planners. Interactive PDF.",
      image: "https://soloandstarving.store/og-image.jpg",
      brand: { "@type": "Brand", name: "Y&N Digital" },
      offers: {
        "@type": "Offer",
        price: PRICING.launchPrice.toFixed(2),
        priceCurrency: "USD",
        availability: "https://schema.org/InStock",
        url: LINKS.starterLaunch,
        priceValidUntil: PRICING.launchEndsAt.slice(0, 10),
      },
    },
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      mainEntity: FAQ.map((f) => ({ "@type": "Question", name: f.q, acceptedAnswer: { "@type": "Answer", text: f.a } })),
    },
  ];
  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }} />;
}
