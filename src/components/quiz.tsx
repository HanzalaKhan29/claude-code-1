"use client";

import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { ArrowLeft, ArrowRight, ArrowCounterClockwise, Check, LockSimple } from "@phosphor-icons/react";
import { PRICING, WEEKS } from "@/lib/content";
import { trackCustom } from "@/lib/tracking";
import { useLaunch, money } from "@/lib/use-launch";
import { CheckoutLink, LocalPrice, StarterPrice } from "./checkout-link";

/* The live site's quiz, question for question. [value, label, reply] */
type Opt = [string, string, string];
const Q: { key: string; title: string; opts: Opt[] }[] = [
  {
    key: "habit",
    title: "6:30pm hits and you still don't know what's for dinner. What happens next?",
    opts: [
      ["delivery", "I open a delivery app", "Zero judgment here. Those apps are designed to be easier than thinking. The problem was never you. Cooking just hasn't been made that easy for you yet."],
      ["cereal", "Cereal, toast, or whatever is there", "Ah, the classic dinner that's technically breakfast. You're not lazy, you're out of ideas and energy at the exact same moment. Very fixable."],
      ["repeat", "The same 3 meals on repeat", "Honestly? That means you can cook. You just got stuck in a loop. A few easy new ones in rotation and it gets fun again."],
    ],
  },
  {
    key: "energy",
    title: "By the time you get to cooking, how much energy do you actually have left?",
    opts: [
      ["30", "Enough for about 30 minutes", "Nice, that opens up the good stuff. Stews, bakes, the cozy one pan dinners that taste like you tried way harder than you did."],
      ["20", "About 20 minutes, no more", "That's most people, honestly. And 20 minutes is plenty when the recipe doesn't send you hunting for 14 ingredients."],
      ["10", "10 minutes or I order something", "Totally get it. That's why the book has a whole Dead Tired mode. Real dinners in 10 minutes, mostly one pan, no heroics required."],
    ],
  },
  {
    key: "spend",
    title: "What's takeout and delivery actually costing you in a normal week?",
    opts: [
      ["15", "Under $20", "Honestly, you're doing better than most. So for you it's less about saving money and more about eating well without the effort."],
      ["35", "$20 to $50", "Quietly, that's somewhere between $1,000 and $2,600 a year. Not wild, but that's a nice trip somewhere. Hold that thought."],
      ["90", "Over $50", "That can clear $4,500 a year. Most people in this range never add it up. You just did, and that's the first step."],
    ],
  },
  {
    key: "block",
    title: "What's the one thing that makes cooking for just yourself feel pointless?",
    opts: [
      ["waste", "Recipes are sized for 4, and half goes to waste", "Right?! Half a bag of spinach turning to soup in the fridge. Painful. Every recipe here makes 2 portions: dinner tonight, lunch tomorrow. Done."],
      ["buy", "I never know what to buy", "That's the one nobody talks about. Walking into a store with no plan is how you leave with snacks and no dinner. We fixed that part too."],
      ["pointless", "It feels pointless for just me", "That one hits home. But you're the person you eat with most. You deserve a proper dinner as much as anyone you'd cook for."],
    ],
  },
  {
    key: "goal",
    title: "Last one: if you could fix ONE thing about your dinners, what would it be?",
    opts: [
      ["1", "Spending way less on food", "Love that. Let's get your dinners down to around $2 each. Yes, really, and still properly good."],
      ["2", "Real food with zero effort", "Say less. We'll make weeknights feel easy, starting with nothing over 15 minutes."],
      ["3", "No more boring meals", "Then we're going on a trip. A different cuisine every night, from Mexican to Japanese."],
    ],
  },
];

const TYPE_HABIT: Record<string, string> = { delivery: "Delivery Regular", cereal: "Cereal for Dinner Survivor", repeat: "Stuck on Repeat Cook" };
const TYPE_ENERGY: Record<string, string> = { "30": "", "20": "Busy ", "10": "Dead Tired " };
const TYPE_SUB: Record<string, string> = {
  delivery: "You're not bad at cooking. You just never had a setup that beats the app. Let's fix that.",
  cereal: "You're not lazy. You hit dinnertime out of ideas and out of energy at the same moment. Let's fix that.",
  repeat: "You can cook. You're just stuck in a loop. Let's break it without making dinner harder.",
};
const DIAG_HABIT: Record<string, string> = {
  delivery: "the delivery app wins",
  cereal: "dinner turns into cereal, toast or whatever's in the cupboard",
  repeat: "you make one of the same three meals again",
};
const DIAG_ENERGY: Record<string, string> = {
  "30": "you have about 30 minutes of energy",
  "20": "you've got 20 minutes in you, tops",
  "10": "you've got about 10 minutes before takeout starts looking good",
};
const CHIPS: Record<string, Record<string, string>> = {
  habit: { delivery: "Delivery app", cereal: "Cereal dinners", repeat: "Same 3 meals" },
  energy: { "30": "30 min energy", "20": "20 min energy", "10": "10 min energy" },
  block: { waste: "Food goes bad", buy: "Don't know what to buy", pointless: "Feels pointless solo" },
};
const FIX: Record<string, [string, string]> = {
  waste: ["No more food going in the bin", "Every recipe makes 2 portions: dinner tonight and lunch tomorrow. And each week's shopping list only has what those 7 dinners need."],
  buy: ["Walk into the store with a plan", "Every week comes with its own shopping list, split into protein, fresh and pantry."],
  pointless: ["Fast enough to feel worth it", "Every recipe takes 10 to 30 minutes, mostly one pan, and covers dinner tonight plus lunch tomorrow."],
};
const CUSTOM_FIX: Record<string, string> = {
  waste: "No generic portion sizes. Your plan is built around exactly how much you eat, so nothing goes bad in the back of the fridge.",
  buy: "Your grocery list is written around your real pantry, your allergies and your budget. Never guess in the store again.",
  pointless: "Every dinner is planned like you are worth cooking for, because you are. Built around your actual taste, not a generic solo eater.",
};
const GOAL_LABEL: Record<string, string> = { "1": "spending way less on food", "2": "real food with zero effort", "3": "no more boring meals" };

const STORE = "ssQuizV2"; // same key as the live site, so returning visitors keep their result
const DELIVERY_ORDER = 18;

type Answers = Record<string, string>;
type Phase = "quiz" | "loading" | "result";
type Wk = 1 | 2 | 3 | 4;

function pickWeek(a: Answers) {
  const goal = (parseInt(a.goal, 10) || 2) as Wk;
  const start = (a.energy === "10" && goal === 3 ? 2 : goal) as Wk;
  const path: Wk[] = [start];
  if (goal !== start) path.push(goal);
  ([1, 2, 3, 4] as Wk[]).forEach((w) => {
    if (!path.includes(w)) path.push(w);
  });
  return { start, goal, path };
}

export function Quiz() {
  const reduce = useReducedMotion();
  const [phase, setPhase] = useState<Phase>("quiz");
  const [cur, setCur] = useState(0);
  const [answers, setAnswers] = useState<Answers>({});
  const [reply, setReply] = useState(false);
  const box = useRef<HTMLDivElement>(null);
  const started = useRef(false);
  const replyTimer = useRef<number | undefined>(undefined);

  // Restore a finished quiz, unless this visit came from a ?quiz=1 ad link (always a fresh start).
  useEffect(() => {
    try {
      const fresh = new URLSearchParams(window.location.search).get("quiz") === "1";
      const saved = JSON.parse(localStorage.getItem(STORE) || "null") as { a?: Answers; done?: boolean } | null;
      if (!fresh && saved?.done && saved.a) {
        setAnswers(saved.a);
        setPhase("result");
      }
    } catch {}
    return () => window.clearTimeout(replyTimer.current);
  }, []);

  useEffect(() => {
    const el = box.current;
    if (!el || (phase === "quiz" && cur === 0)) return;
    if (el.getBoundingClientRect().top < 64) el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
  }, [cur, phase, reduce]);

  const q = Q[cur];
  const picked = q ? answers[q.key] : undefined;

  const pick = (value: string) => {
    if (!started.current) {
      started.current = true;
      trackCustom("QuizStart");
    }
    setAnswers((a) => ({ ...a, [q.key]: value }));
    setReply(false);
    window.clearTimeout(replyTimer.current);
    replyTimer.current = window.setTimeout(() => setReply(true), reduce ? 0 : 450);
  };

  const next = () => {
    if (!picked) return;
    if (cur < Q.length - 1) {
      setCur(cur + 1);
      setReply(false);
      return;
    }
    const pw = pickWeek(answers);
    try {
      localStorage.setItem(STORE, JSON.stringify({ a: answers, deadline: null, done: true }));
    } catch {}
    trackCustom("QuizComplete", { week: pw.start, goal: answers.goal, energy: answers.energy });
    setPhase("loading");
  };

  const back = () => {
    if (cur > 0) {
      setCur(cur - 1);
      setReply(true);
    }
  };

  const restart = () => {
    try {
      localStorage.removeItem(STORE);
    } catch {}
    started.current = false;
    setAnswers({});
    setCur(0);
    setReply(false);
    setPhase("quiz");
  };

  return (
    <div
      ref={box}
      className="relative scroll-mt-24 overflow-hidden rounded-card bg-surface shadow-[inset_0_0_0_1px_var(--color-line)]"
    >
      <AnimatePresence mode="wait" initial={false}>
        {phase === "quiz" && (
          <motion.div
            key={`q${cur}`}
            initial={reduce ? { opacity: 0 } : { opacity: 0, x: 24 }}
            animate={{ opacity: 1, x: 0 }}
            exit={reduce ? { opacity: 0 } : { opacity: 0, x: -24 }}
            transition={{ duration: 0.28, ease: [0.16, 1, 0.3, 1] }}
            className="p-5 sm:p-8"
          >
            <fieldset>
              <div className="mb-6 flex items-center justify-between gap-4">
                <div className="flex gap-1.5" aria-hidden>
                  {Q.map((_, i) => (
                    <span
                      key={i}
                      className={`h-1.5 w-7 rounded-full transition-colors duration-300 ${
                        i < cur || (i === cur && reply) ? "bg-accent" : i === cur ? "bg-accent/40" : "bg-raised"
                      }`}
                    />
                  ))}
                </div>
                <span className="font-mono text-xs text-faint">
                  Question {cur + 1} of {Q.length}
                </span>
              </div>
              <legend className="sr-only">
                Question {cur + 1} of {Q.length}
              </legend>
              <h3 className="mb-6 max-w-[30ch] font-display text-2xl font-semibold leading-[1.15] tracking-tight text-cream sm:text-[28px]">
                {q.title}
              </h3>
              <div className="grid gap-2.5">
                {q.opts.map(([value, label]) => {
                  const on = picked === value;
                  return (
                    <button
                      key={value}
                      type="button"
                      onClick={() => pick(value)}
                      aria-pressed={on}
                      className={`flex items-center justify-between gap-3 rounded-field px-4 py-3.5 text-left text-[15px] font-medium transition-all duration-200 active:scale-[0.99] ${
                        on
                          ? "bg-accent text-accent-ink"
                          : "bg-raised text-cream shadow-[inset_0_0_0_1px_var(--color-line)] hover:bg-[#2a2d33] hover:shadow-[inset_0_0_0_1px_var(--color-line-strong)]"
                      }`}
                    >
                      {label}
                      {on && <Check size={16} weight="bold" aria-hidden className="shrink-0" />}
                    </button>
                  );
                })}
              </div>

              <div aria-live="polite">
                <AnimatePresence>
                  {picked && reply && (
                    <motion.div
                      key={picked}
                      initial={reduce ? { opacity: 0 } : { opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
                      className="mt-5"
                    >
                      <p className="rounded-card rounded-tl-md bg-accent-soft px-4 py-3 text-[15px] leading-relaxed text-cream">
                        {q.opts.find((o) => o[0] === picked)?.[2]}
                      </p>
                      <p className="mt-1.5 pl-1 text-xs text-faint">Yassine &amp; Nourhene</p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              <div className="mt-6 flex items-center justify-between gap-4">
                {cur > 0 ? (
                  <button type="button" onClick={back} className="inline-flex items-center gap-1.5 text-sm text-muted hover:text-cream">
                    <ArrowLeft size={14} weight="bold" aria-hidden /> Back
                  </button>
                ) : (
                  <span className="text-sm text-faint">Takes about a minute. No email needed.</span>
                )}
                <button
                  type="button"
                  onClick={next}
                  disabled={!picked || !reply}
                  className="btn btn-primary px-5 py-3 text-sm disabled:pointer-events-none disabled:opacity-0"
                >
                  {cur === Q.length - 1 ? "Build my plan" : "Next question"}
                  <ArrowRight size={14} weight="bold" aria-hidden />
                </button>
              </div>
            </fieldset>
          </motion.div>
        )}

        {phase === "loading" && (
          <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <Loading answers={answers} fast={!!reduce} onDone={() => setPhase("result")} />
          </motion.div>
        )}

        {phase === "result" && (
          <motion.div
            key="result"
            initial={reduce ? { opacity: 0 } : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45, ease: [0.16, 1, 0.3, 1] }}
          >
            <Result answers={answers} onRestart={restart} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function Loading({ answers, fast, onDone }: { answers: Answers; fast: boolean; onDone: () => void }) {
  const pw = pickWeek(answers);
  const energy = ({ "30": "30 minute", "20": "20 minute", "10": "10 minute" } as Record<string, string>)[answers.energy] ?? "weeknight";
  const steps = [
    "Reading your answers",
    `Matching 88 recipes to your ${energy} evenings`,
    `Building your ${WEEKS[pw.start].short}`,
    "Doing your takeout math",
  ];
  const [i, setI] = useState(0);
  const done = useRef(onDone);
  done.current = onDone;

  useEffect(() => {
    if (i >= 4) {
      const t = window.setTimeout(() => done.current(), fast ? 0 : 400);
      return () => window.clearTimeout(t);
    }
    const t = window.setTimeout(() => setI((n) => n + 1), fast ? 60 : 750);
    return () => window.clearTimeout(t);
  }, [i, fast]);

  return (
    <div className="p-6 sm:p-10" role="status">
      <p className="font-display text-2xl font-semibold text-cream">Building your dinner plan</p>
      <ul className="mt-6 space-y-3">
        {steps.map((s, k) => (
          <li key={s} className={`flex items-center gap-3 transition-opacity duration-300 ${k <= i ? "opacity-100" : "opacity-30"}`}>
            <span
              className={`grid size-6 shrink-0 place-items-center rounded-full transition-colors duration-300 ${
                k < i ? "bg-accent text-accent-ink" : "bg-raised text-faint"
              }`}
            >
              <Check size={13} weight="bold" aria-hidden />
            </span>
            <span className="text-cream">{s}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function Result({ answers: a, onRestart }: { answers: Answers; onRestart: () => void }) {
  const { price } = useLaunch();
  const pw = pickWeek(a);
  const W = WEEKS[pw.start];
  const maxT = Math.max(...W.d.map((x) => x[4]));
  const spend = parseInt(a.spend, 10) || 35;
  const orders = spend / DELIVERY_ORDER;
  const yearly = Math.round((Math.max(0, spend - orders * W.avg) * 52) / 10) * 10;
  const payback = Math.max(1, Math.ceil(price / (DELIVERY_ORDER - W.avg)));
  const spendLabel = a.spend === "15" ? "~$15" : a.spend === "90" ? "$50+" : money(spend);
  const fix = FIX[a.block] ?? FIX.waste;
  const cfix = CUSTOM_FIX[a.block] ?? CUSTOM_FIX.waste;

  useEffect(() => {
    trackCustom("ViewPersonalizedPlan", { week: pw.start });
  }, [pw.start]);

  const why =
    `Picked for you because you want ${GOAL_LABEL[a.goal] ?? "easier dinners"}` +
    (pw.start !== pw.goal
      ? ` and you usually have about 10 minutes of energy. We start you on the easiest week, then ${WEEKS[pw.goal].short} is next.`
      : `. ${W.blurb}`);

  return (
    <div className="divide-y divide-line">
      <div className="p-5 sm:p-8">
        <p className="text-sm text-muted">Your solo dinner type</p>
        <h3 className="mt-1 font-display text-3xl font-semibold leading-[1.1] tracking-tight text-cream sm:text-4xl">
          The {TYPE_ENERGY[a.energy] ?? ""}
          {TYPE_HABIT[a.habit] ?? "Solo Cook"}
        </h3>
        <p className="mt-3 max-w-[52ch] text-[15px] leading-relaxed text-muted">{TYPE_SUB[a.habit] ?? TYPE_SUB.delivery}</p>
        <ul className="mt-4 flex flex-wrap gap-2">
          {(["habit", "energy", "block"] as const).map((k) =>
            CHIPS[k][a[k]] ? (
              <li key={k} className="rounded-full bg-raised px-3 py-1 text-xs text-cream shadow-[inset_0_0_0_1px_var(--color-line)]">
                {CHIPS[k][a[k]]}
              </li>
            ) : null,
          )}
        </ul>
        <p className="mt-4 text-[15px] text-cream/90">
          Most nights {DIAG_HABIT[a.habit] ?? DIAG_HABIT.delivery}, and by then {DIAG_ENERGY[a.energy] ?? DIAG_ENERGY["20"]}.
        </p>
      </div>

      <div className="p-5 sm:p-8">
        <p className="text-sm text-muted">Your starting week</p>
        <h4 className="mt-1 font-display text-2xl font-semibold tracking-tight text-cream">{W.name}</h4>
        <p className="mt-2 max-w-[60ch] text-sm leading-relaxed text-muted">{why}</p>
        <dl className="mt-5 grid grid-cols-3 gap-3">
          {[
            ["7", "dinners planned"],
            [`${maxT} min`, "longest cook"],
            [money(W.avg), "per dinner"],
          ].map(([v, l]) => (
            <div key={l} className="rounded-field bg-raised p-3">
              <dt className="sr-only">{l}</dt>
              <dd>
                <span className="block font-display text-xl font-semibold text-cream">{v}</span>
                <span className="text-xs text-faint">{l}</span>
              </dd>
            </div>
          ))}
        </dl>
        <ol className="mt-5 divide-y divide-line">
          {W.d.map(([day, num, name, cuisine, mins, cost]) => (
            <li key={day} className="grid grid-cols-[2.75rem_1fr_auto] items-baseline gap-3 py-2.5 text-sm">
              <span className="font-mono text-faint">{day}</span>
              <span className="text-cream">
                {name}
                <span className="block text-xs text-faint">
                  Recipe {num}, {cuisine}, {mins} min
                </span>
              </span>
              <span className="font-mono text-muted">${cost.toFixed(2)}</span>
            </li>
          ))}
        </ol>
        <p className="mt-4 flex items-center gap-2 text-sm text-muted">
          <LockSimple size={16} weight="bold" className="shrink-0 text-accent" aria-hidden />
          The full recipes and this week's shopping list come with your bundle.
        </p>
        <p className="mt-3 text-xs text-faint">Your 4 weeks: {pw.path.map((w) => `Week ${w}`).join(", then ")}.</p>
        <p className="mt-1 text-xs text-faint">
          This week is from the Starter Bundle. The Custom Plan has no fixed week; yours is built from scratch after you order.
        </p>
      </div>

      <div className="grid gap-px bg-line sm:grid-cols-2">
        <div className="bg-surface p-5 sm:p-8">
          <p className="text-xs font-semibold text-faint">Starter Bundle</p>
          <p className="mt-2 font-display text-lg font-semibold text-cream">{fix[0]}</p>
          <p className="mt-2 text-sm leading-relaxed text-muted">{fix[1]}</p>
        </div>
        <div className="bg-surface p-5 sm:p-8">
          <p className="text-xs font-semibold text-accent">Custom Plan</p>
          <p className="mt-2 font-display text-lg font-semibold text-cream">Solved exactly, not generally</p>
          <p className="mt-2 text-sm leading-relaxed text-muted">{cfix}</p>
        </div>
      </div>

      <div className="p-5 sm:p-8">
        <p className="text-sm text-muted">What your takeout is really costing you</p>
        <dl className="mt-4 grid grid-cols-3 gap-3">
          <div>
            <dt className="text-xs text-faint">Takeout a week</dt>
            <dd className="font-display text-2xl font-semibold text-cream">{spendLabel}</dd>
          </div>
          <div>
            <dt className="text-xs text-faint">Plan dinner</dt>
            <dd className="font-display text-2xl font-semibold text-cream">{money(W.avg)}</dd>
          </div>
          <div>
            <dt className="text-xs text-faint">Back a year</dt>
            <dd className="font-display text-2xl font-semibold text-accent">${yearly.toLocaleString("en-US")}</dd>
          </div>
        </dl>
        <p className="mt-4 text-[15px] text-cream/90">
          Your bundle pays for itself after about {payback} swapped takeout order{payback > 1 ? "s" : ""}.
        </p>
        <p className="mt-2 text-xs leading-relaxed text-faint">
          Estimate based on your answer, an average ${DELIVERY_ORDER} delivery order with fees, and this week's average cost per
          dinner. Your prices will vary.
        </p>
      </div>

      <div className="p-5 sm:p-8">
        <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center">
          <CheckoutLink plan="starter" placement="quiz-result" className="btn btn-primary px-6 py-3.5 text-[15px]">
            <span>
              Get the cookbook for <StarterPrice />
            </span>
            <ArrowRight size={16} weight="bold" aria-hidden />
          </CheckoutLink>
          <CheckoutLink plan="custom" placement="quiz-result" className="btn btn-ghost px-6 py-3.5 text-[15px]">
            Get my custom plan, ${PRICING.customPrice}
          </CheckoutLink>
        </div>
        <p className="mt-3 text-sm text-muted">
          Starter: ready tonight, all 4 weeks included. Custom: built by hand around you in 2 to 3 days.
        </p>
        <LocalPrice className="mt-1 block text-xs text-faint" />
        <div className="mt-5 flex flex-wrap items-center gap-x-6 gap-y-2 text-sm">
          <a href="#offer" className="text-muted underline decoration-line-strong underline-offset-4 hover:text-cream">
            Compare both plans
          </a>
          <button type="button" onClick={onRestart} className="inline-flex items-center gap-1.5 text-faint hover:text-cream">
            <ArrowCounterClockwise size={14} weight="bold" aria-hidden /> Retake the quiz
          </button>
        </div>
      </div>
    </div>
  );
}
