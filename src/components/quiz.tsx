"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { ArrowLeft, ArrowRight, ArrowCounterClockwise } from "@phosphor-icons/react";
import { MODES, PRICING, RECIPES, type Mode } from "@/lib/content";
import { CheckoutLink, StarterPrice } from "./checkout-link";

type Option = { label: string; value: string };
type Question = { id: string; prompt: string; options: Option[] };

const QUESTIONS: Question[] = [
  {
    id: "habit",
    prompt: "It's 6:30pm and you still don't know what's for dinner. What happens next?",
    options: [
      { label: "I open a delivery app", value: "scroller" },
      { label: "Cereal, toast, or whatever is there", value: "survivor" },
      { label: "The same 3 meals on repeat", value: "rerun" },
      { label: "I cook, but it eats the whole evening", value: "marathon" },
    ],
  },
  {
    id: "energy",
    prompt: "On a normal weeknight, how much energy is left by dinner?",
    options: [
      { label: "Some. I could cook for half an hour", value: "normal" },
      { label: "Not much. 20 minutes, tops", value: "tired" },
      { label: "None. I want food in 10 minutes", value: "dead" },
    ],
  },
  {
    id: "spend",
    prompt: "Roughly what goes on takeout and delivery in a week?",
    options: [
      { label: "Almost nothing", value: "5" },
      { label: "$15 to $40", value: "27" },
      { label: "$40 to $80", value: "60" },
      { label: "More than $80", value: "100" },
    ],
  },
  {
    id: "skill",
    prompt: "Be honest. How are your cooking skills?",
    options: [
      { label: "I've never really cooked", value: "never" },
      { label: "I can do the basics", value: "basics" },
      { label: "Fine, I just lack ideas and time", value: "fine" },
    ],
  },
  {
    id: "needs",
    prompt: "Does your plan have to work around anything?",
    options: [
      { label: "Nope, I'll eat most things", value: "none" },
      { label: "Allergies or foods I won't eat", value: "allergies" },
      { label: "A very tight grocery budget", value: "budget" },
      { label: "It's a gift for someone else", value: "gift" },
    ],
  },
];

const TYPES: Record<string, { name: string; line: string }> = {
  scroller: {
    name: "The Delivery Scroller",
    line: "You're not lazy, you're out of decisions. When dinner is already picked, the app stops winning.",
  },
  survivor: {
    name: "The Cereal Survivor",
    line: "You skip dinner more than you'd admit. You need meals so short they beat pouring a bowl.",
  },
  rerun: {
    name: "The Rerun",
    line: "You can cook, you're just bored of your own three dishes. You need range without risk.",
  },
  marathon: {
    name: "The Accidental Marathon",
    line: "Recipes built for four turn your evening into a project. You need one pan and a short list.",
  },
};

const SKILL_TIP: Record<string, string> = {
  never: "Start with the Start Here page: heat levels, rice, pasta, and exactly when chicken is done.",
  basics: "You'll be fine from page one. Every recipe lists prep, tools and swaps before you start.",
  fine: "Skip to the 4 Week Dinner Plans. The thinking is done, you just shop the list and cook.",
};

// Average delivery order with fees, as used on the original site. Home cost is the cookbook's typical per-serving cost.
const DELIVERY_ORDER = 18;
const HOME_DINNER = 2.9;

export function Quiz() {
  const reduce = useReducedMotion();
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const done = step >= QUESTIONS.length;
  const box = useRef<HTMLDivElement>(null);

  // Keep the start of each step on screen; the result card is taller than the questions.
  useEffect(() => {
    const el = box.current;
    if (!el || (step === 0 && !done)) return;
    if (el.getBoundingClientRect().top < 64) el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
  }, [step, done, reduce]);

  const choose = (qid: string, value: string) => {
    setAnswers((a) => ({ ...a, [qid]: value }));
    window.setTimeout(() => setStep((s) => s + 1), reduce ? 0 : 180);
  };

  const restart = () => {
    setAnswers({});
    setStep(0);
  };

  return (
    <div
      ref={box}
      className="relative scroll-mt-24 overflow-hidden rounded-card bg-surface shadow-[inset_0_0_0_1px_var(--color-line)]"
    >
      <AnimatePresence mode="wait" initial={false}>
        {!done ? (
          <motion.div
            key={step}
            initial={reduce ? { opacity: 0 } : { opacity: 0, x: 24 }}
            animate={{ opacity: 1, x: 0 }}
            exit={reduce ? { opacity: 0 } : { opacity: 0, x: -24 }}
            transition={{ duration: 0.28, ease: [0.16, 1, 0.3, 1] }}
            className="p-5 sm:p-8"
          >
            <QuestionView
              q={QUESTIONS[step]}
              step={step}
              selected={answers[QUESTIONS[step].id]}
              onChoose={choose}
              onBack={() => setStep((s) => Math.max(0, s - 1))}
            />
          </motion.div>
        ) : (
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

function QuestionView({
  q,
  step,
  selected,
  onChoose,
  onBack,
}: {
  q: Question;
  step: number;
  selected?: string;
  onChoose: (qid: string, value: string) => void;
  onBack: () => void;
}) {
  return (
    <fieldset>
      <div className="mb-6 flex items-center justify-between gap-4">
        <div className="flex gap-1.5" aria-hidden>
          {QUESTIONS.map((_, i) => (
            <span
              key={i}
              className={`h-1.5 w-7 rounded-full transition-colors duration-300 ${i <= step ? "bg-accent" : "bg-raised"}`}
            />
          ))}
        </div>
        <span className="font-mono text-xs text-faint">
          Question {step + 1} of {QUESTIONS.length}
        </span>
      </div>
      <legend className="sr-only">
        Question {step + 1} of {QUESTIONS.length}
      </legend>
      <h3 className="mb-6 max-w-[28ch] font-display text-2xl font-semibold leading-[1.15] tracking-tight text-cream sm:text-[28px]">
        {q.prompt}
      </h3>
      <div className="grid gap-2.5">
        {q.options.map((o) => {
          const on = selected === o.value;
          return (
            <button
              key={o.value}
              type="button"
              onClick={() => onChoose(q.id, o.value)}
              aria-pressed={on}
              className={`group flex items-center justify-between rounded-field px-4 py-3.5 text-left text-[15px] font-medium transition-all duration-200 active:scale-[0.99] ${
                on
                  ? "bg-accent text-accent-ink"
                  : "bg-raised text-cream shadow-[inset_0_0_0_1px_var(--color-line)] hover:bg-[#2a2d33] hover:shadow-[inset_0_0_0_1px_var(--color-line-strong)]"
              }`}
            >
              {o.label}
              <ArrowRight
                size={16}
                weight="bold"
                aria-hidden
                className={`shrink-0 transition-transform duration-200 group-hover:translate-x-0.5 ${on ? "" : "text-faint"}`}
              />
            </button>
          );
        })}
      </div>
      <div className="mt-6 flex items-center justify-between text-sm">
        {step > 0 ? (
          <button type="button" onClick={onBack} className="inline-flex items-center gap-1.5 text-muted hover:text-cream">
            <ArrowLeft size={14} weight="bold" aria-hidden /> Back
          </button>
        ) : (
          <span className="text-faint">Takes about a minute. No email needed.</span>
        )}
      </div>
    </fieldset>
  );
}

function Result({ answers, onRestart }: { answers: Record<string, string>; onRestart: () => void }) {
  const type = TYPES[answers.habit] ?? TYPES.scroller;
  const mode = (answers.energy as Mode) ?? "tired";
  const weekly = Number(answers.spend ?? 27);
  const orders = weekly / DELIVERY_ORDER;
  const yearly = Math.max(0, Math.round(((weekly - orders * HOME_DINNER) * 52) / 10) * 10);
  const custom = answers.needs === "allergies" || answers.needs === "gift";

  const picks = RECIPES.filter((r) => r.mode === mode);
  const shown = (picks.length >= 2 ? picks : [...picks, ...RECIPES.filter((r) => r.mode === "tired")]).slice(0, 2);

  return (
    <div>
      <div className="grid grid-cols-2 gap-px bg-line">
        {shown.map((r) => (
          <figure key={r.slug} className="relative flex h-40 sm:h-48 flex-col justify-end bg-surface">
            <Image src={r.image} alt={r.name} fill sizes="(min-width: 1024px) 360px, 50vw" className="object-cover" />
            <figcaption className="relative bg-gradient-to-t from-ink via-ink/80 to-transparent p-4 pt-12">
              <span className="block font-display text-[15px] font-semibold leading-tight text-cream">{r.name}</span>
              <span className="font-mono text-xs text-muted">
                {r.minutes} min, {r.cost}
              </span>
            </figcaption>
          </figure>
        ))}
      </div>
      <div className="p-5 sm:p-8">
        <p className="mb-2 text-sm text-muted">Your solo dinner type</p>
        <h3 className="font-display text-3xl font-semibold leading-[1.1] tracking-tight text-cream sm:text-4xl">
          {type.name}
        </h3>
        <p className="mt-3 max-w-[48ch] text-[15px] leading-relaxed text-muted">{type.line}</p>

        <div className="mt-6 grid gap-4 border-t border-line pt-6 sm:grid-cols-2">
          <div>
            <p className="text-sm text-faint">Start in</p>
            <p className="font-display text-xl font-semibold text-cream">
              {MODES[mode].label} mode, {MODES[mode].minutes} min
            </p>
          </div>
          {weekly >= 15 ? (
            <div>
              <p className="text-sm text-faint">Back in your pocket, roughly</p>
              <p className="font-display text-xl font-semibold text-accent">${yearly.toLocaleString("en-US")} a year</p>
            </div>
          ) : (
            <div>
              <p className="text-sm text-faint">Money isn't your problem</p>
              <p className="font-display text-xl font-semibold text-cream">Time and ideas are</p>
            </div>
          )}
        </div>
        <p className="mt-4 text-sm leading-relaxed text-muted">{SKILL_TIP[answers.skill] ?? SKILL_TIP.basics}</p>
        {weekly >= 15 && (
          <p className="mt-2 text-xs leading-relaxed text-faint">
            Estimate: your answer, an average ${DELIVERY_ORDER} delivery order with fees, and about ${HOME_DINNER.toFixed(2)} per
            home-cooked serving. Your prices will vary.
          </p>
        )}

        <div className="mt-7 flex flex-col flex-wrap gap-3 sm:flex-row sm:items-center">
          {custom ? (
            <>
              <CheckoutLink plan="custom" placement="quiz-result" className="btn btn-primary px-6 py-3.5 text-[15px]">
                <span>Get my custom plan, ${PRICING.customPrice}</span> <ArrowRight size={16} weight="bold" aria-hidden />
              </CheckoutLink>
              <CheckoutLink plan="starter" placement="quiz-result-alt" className="btn btn-ghost px-6 py-3.5 text-[15px]">
                <span>
                  Just the cookbook, <StarterPrice />
                </span>
              </CheckoutLink>
            </>
          ) : (
            <>
              <CheckoutLink plan="starter" placement="quiz-result" className="btn btn-primary px-6 py-3.5 text-[15px]">
                <span>
                  Get the cookbook for <StarterPrice />
                </span>{" "}
                <ArrowRight size={16} weight="bold" aria-hidden />
              </CheckoutLink>
              <a href="#offer" className="text-sm text-muted underline decoration-line-strong underline-offset-4 hover:text-cream">
                Compare both plans
              </a>
            </>
          )}
        </div>
        {custom && (
          <p className="mt-3 text-sm text-muted">
            {answers.needs === "gift"
              ? "The Custom Plan is built around their tastes and can include a personal message page."
              : "The Custom Plan is built by a real person around your allergies and the foods you skip."}
          </p>
        )}
        <button
          type="button"
          onClick={onRestart}
          className="mt-6 inline-flex items-center gap-1.5 text-sm text-faint hover:text-cream"
        >
          <ArrowCounterClockwise size={14} weight="bold" aria-hidden /> Retake the quiz
        </button>
      </div>

    </div>
  );
}
