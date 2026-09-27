"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { LINKS } from "@/lib/content";
import { loadPixel, looksEUorUK, readConsent, writeConsent } from "@/lib/tracking";

/**
 * Same consent model as the live site: UK/EU visitors opt in before the pixel loads,
 * everyone else is counted right away and can opt out. Choice is remembered.
 */
export function Consent() {
  const reduce = useReducedMotion();
  const [open, setOpen] = useState(false);
  const [gated, setGated] = useState(true);

  useEffect(() => {
    const c = readConsent();
    if (c === "accepted") return loadPixel();
    if (c === "declined") return;
    const g = looksEUorUK();
    setGated(g);
    if (!g) loadPixel();
    setOpen(true);
  }, []);

  const choose = (v: "accepted" | "declined") => {
    writeConsent(v);
    setOpen(false);
    if (v === "accepted" && gated) loadPixel();
  };

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          role="dialog"
          aria-label="Cookie notice"
          initial={reduce ? { opacity: 0 } : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: reduce ? 0 : 16 }}
          transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
          className="fixed bottom-3 left-3 right-3 z-[55] max-w-sm rounded-card bg-raised p-3.5 text-[13px] text-muted sm:p-4 sm:text-sm shadow-[0_20px_60px_-20px_rgb(0_0_0/0.8),inset_0_0_0_1px_var(--color-line-strong)] md:bottom-6 md:left-6 md:right-auto"
        >
          <p>
            We use cookies to measure the site and our ads.{" "}
            <a href={LINKS.privacy} className="text-cream underline underline-offset-2">
              Privacy Policy
            </a>
          </p>
          <div className="mt-3 flex gap-2">
            <button type="button" onClick={() => choose("accepted")} className="btn btn-primary px-4 py-2 text-sm">
              Accept
            </button>
            <button type="button" onClick={() => choose("declined")} className="btn btn-ghost px-4 py-2 text-sm">
              Necessary only
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
