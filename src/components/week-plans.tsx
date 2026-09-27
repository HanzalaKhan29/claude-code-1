"use client";

import { useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { WEEKS } from "@/lib/content";

type Wk = 1 | 2 | 3 | 4;
const ORDER: Wk[] = [1, 2, 3, 4];

/** The 4 Week Dinner Plans bonus, browsable week by week. */
export function WeekPlans() {
  const [week, setWeek] = useState<Wk>(1);
  const reduce = useReducedMotion();
  const W = WEEKS[week];
  const longest = Math.max(...W.d.map((x) => x[4]));

  return (
    <div className="grid gap-8 lg:grid-cols-[0.9fr_1.1fr] lg:gap-14">
      <div>
        <div role="tablist" aria-label="Choose a week" className="grid grid-cols-2 gap-2 sm:grid-cols-4 lg:grid-cols-2">
          {ORDER.map((w) => {
            const on = w === week;
            return (
              <button
                key={w}
                role="tab"
                aria-selected={on}
                aria-controls="week-panel"
                onClick={() => setWeek(w)}
                className={`relative rounded-field px-4 py-3 text-left transition-colors ${
                  on ? "text-accent-ink" : "bg-surface text-cream shadow-[inset_0_0_0_1px_var(--color-line)] hover:bg-raised"
                }`}
              >
                {on && (
                  <motion.span
                    layoutId="week-pill"
                    className="absolute inset-0 -z-0 rounded-field bg-accent"
                    transition={reduce ? { duration: 0 } : { type: "spring", stiffness: 420, damping: 36 }}
                  />
                )}
                <span className="relative block text-xs opacity-70">Week {w}</span>
                <span className="relative block font-semibold">{WEEKS[w].short}</span>
              </button>
            );
          })}
        </div>
        <p className="mt-6 max-w-[44ch] text-lg leading-relaxed text-muted">{W.blurb}</p>
        <dl className="mt-6 flex gap-8">
          <div>
            <dt className="text-sm text-faint">Per dinner</dt>
            <dd className="font-display text-3xl font-bold text-cream">${W.avg.toFixed(2)}</dd>
          </div>
          <div>
            <dt className="text-sm text-faint">Longest cook</dt>
            <dd className="font-display text-3xl font-bold text-cream">{longest} min</dd>
          </div>
        </dl>
      </div>

      <div id="week-panel" role="tabpanel" aria-live="polite" className="rounded-card bg-surface p-2 shadow-[inset_0_0_0_1px_var(--color-line)]">
        <AnimatePresence mode="wait" initial={false}>
          <motion.ol
            key={week}
            initial={reduce ? { opacity: 0 } : { opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className="divide-y divide-line"
          >
            {W.d.map(([day, num, name, cuisine, mins, cost]) => (
              <li key={day} className="grid grid-cols-[3rem_1fr_auto] items-baseline gap-3 px-4 py-3.5">
                <span className="font-mono text-sm text-faint">{day}</span>
                <span className="text-cream">
                  {name}
                  <span className="block text-xs text-faint">
                    Recipe {num}, {cuisine}, {mins} min
                  </span>
                </span>
                <span className="font-mono text-sm text-muted">${cost.toFixed(2)}</span>
              </li>
            ))}
          </motion.ol>
        </AnimatePresence>
        <p className="px-4 pt-2 pb-3 text-xs text-faint">Each week comes with its own shopping list, split into protein, fresh and pantry.</p>
      </div>
    </div>
  );
}
