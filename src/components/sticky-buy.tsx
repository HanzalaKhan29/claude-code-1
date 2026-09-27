"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { ArrowRight } from "@phosphor-icons/react";
import { CheckoutLink, StarterPrice } from "./checkout-link";
import { useLaunch } from "@/lib/use-launch";

/**
 * Mobile buy bar. On phones the hero button sits below the photo, so the bar is there from first paint.
 * It hides whenever an in-page buy button is on screen (hero, pricing, final CTA) so there is never a double button.
 */
export function StickyBuy() {
  const reduce = useReducedMotion();
  const { active } = useLaunch();
  const [mounted, setMounted] = useState(false);
  const [ctaVisible, setCtaVisible] = useState(false);

  useEffect(() => {
    setMounted(true);
    const targets = ["hero-cta", "offer", "final-cta"]
      .map((id) => document.getElementById(id))
      .filter(Boolean) as Element[];
    const visible = new Set<Element>();
    const obs = new IntersectionObserver((entries) => {
      for (const e of entries) e.isIntersecting ? visible.add(e.target) : visible.delete(e.target);
      setCtaVisible(visible.size > 0);
    });
    targets.forEach((t) => obs.observe(t));
    return () => obs.disconnect();
  }, []);

  const show = mounted && !ctaVisible;

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={reduce ? { opacity: 0 } : { y: "110%" }}
          animate={reduce ? { opacity: 1 } : { y: 0 }}
          exit={reduce ? { opacity: 0 } : { y: "110%" }}
          transition={{ type: "spring", stiffness: 380, damping: 36 }}
          className="fixed inset-x-0 bottom-0 z-50 border-t border-line bg-night/90 px-4 pt-3 pb-[max(0.75rem,env(safe-area-inset-bottom))] backdrop-blur-xl md:hidden"
        >
          <div className="flex items-center justify-between gap-3">
            <div className="leading-tight">
              <p className="text-sm font-semibold text-cream">
                <StarterPrice />{" "}
                {active && <span className="font-normal text-faint line-through">$35</span>}
              </p>
              <p className="text-xs text-muted">88 recipes + 2 bonuses</p>
            </div>
            <CheckoutLink plan="starter" placement="sticky-mobile" className="btn btn-primary px-5 py-3 text-sm">
              Get the cookbook <ArrowRight size={14} weight="bold" aria-hidden />
            </CheckoutLink>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
