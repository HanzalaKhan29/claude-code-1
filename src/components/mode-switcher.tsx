"use client";

import Image from "next/image";
import { useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { Clock, CurrencyDollar, Barbell } from "@phosphor-icons/react";
import { HERO_BY_MODE, MODES, RECIPES, type Mode } from "@/lib/content";

const ORDER: Mode[] = ["normal", "tired", "dead"];

export function ModeSwitcher() {
  const [mode, setMode] = useState<Mode>("tired");
  const reduce = useReducedMotion();
  const recipe = RECIPES.find((r) => r.slug === HERO_BY_MODE[mode])!;

  return (
    <div className="relative">
      <p id="mode-label" className="mb-3 text-sm text-muted">
        How much energy do you have tonight?
      </p>
      <div
        role="tablist"
        aria-labelledby="mode-label"
        className="relative mb-4 grid grid-cols-3 rounded-full bg-surface p-1 shadow-[inset_0_0_0_1px_var(--color-line)]"
      >
        {ORDER.map((m) => {
          const selected = m === mode;
          return (
            <button
              key={m}
              role="tab"
              aria-selected={selected}
              aria-controls="mode-panel"
              onClick={() => setMode(m)}
              className={`relative z-10 rounded-full px-2 py-2.5 text-sm font-semibold transition-colors sm:text-[15px] ${
                selected ? "text-accent-ink" : "text-muted hover:text-cream"
              }`}
            >
              {selected && (
                <motion.span
                  layoutId="mode-pill"
                  className="absolute inset-0 -z-10 rounded-full bg-accent"
                  transition={reduce ? { duration: 0 } : { type: "spring", stiffness: 420, damping: 34 }}
                />
              )}
              {MODES[m].label}
              <span className={`ml-1.5 font-mono text-xs font-normal ${selected ? "text-accent-ink/70" : "text-faint"}`}>
                {MODES[m].minutes}m
              </span>
            </button>
          );
        })}
      </div>

      <div id="mode-panel" role="tabpanel" aria-live="polite">
        <div className="relative aspect-[4/3] overflow-hidden rounded-card bg-surface lg:aspect-[5/4]">
          {/* All three stay mounted so switching never waits on a download. */}
          {ORDER.map((m) => {
            const r = RECIPES.find((x) => x.slug === HERO_BY_MODE[m])!;
            const on = m === mode;
            return (
              <motion.div
                key={m}
                aria-hidden={!on}
                className="absolute inset-0"
                initial={false}
                animate={{ opacity: on ? 1 : 0, scale: on || reduce ? 1 : 1.06 }}
                transition={{ duration: reduce ? 0.15 : 0.7, ease: [0.16, 1, 0.3, 1] }}
              >
                <Image
                  src={r.image}
                  alt={on ? `${r.name}, a ${MODES[m].label.toLowerCase()} mode recipe from the cookbook` : ""}
                  fill
                  priority={m === "tired"}
                  sizes="(min-width: 1024px) 560px, 100vw"
                  className="object-cover"
                />
              </motion.div>
            );
          })}
          <div className="pointer-events-none absolute inset-0 rounded-card shadow-[inset_0_0_0_1px_rgb(255_255_255/0.08)]" />
        </div>

        <AnimatePresence mode="wait" initial={false}>
          <motion.div
            key={recipe.slug}
            initial={reduce ? false : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={reduce ? { opacity: 0 } : { opacity: 0, y: -6 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="mt-4 flex flex-wrap items-baseline justify-between gap-x-6 gap-y-2"
          >
            <div>
              <p className="font-display text-lg font-semibold leading-tight text-cream">{recipe.name}</p>
              <p className="text-sm text-muted">{MODES[mode].line}</p>
            </div>
            <dl className="flex gap-4 font-mono text-sm text-cream">
              <div className="flex items-center gap-1.5">
                <dt className="sr-only">Time</dt>
                <Clock size={16} weight="bold" className="text-accent" aria-hidden />
                <dd>{recipe.minutes} min</dd>
              </div>
              <div className="flex items-center gap-1.5">
                <dt className="sr-only">Cost per serving</dt>
                <CurrencyDollar size={16} weight="bold" className="text-accent" aria-hidden />
                <dd>{recipe.cost.replace("$", "")}</dd>
              </div>
              <div className="flex items-center gap-1.5">
                <dt className="sr-only">Protein</dt>
                <Barbell size={16} weight="bold" className="text-accent" aria-hidden />
                <dd>{recipe.protein}g</dd>
              </div>
            </dl>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
