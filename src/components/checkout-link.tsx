"use client";

import { useEffect, useState } from "react";
import { LINKS, PRICING } from "@/lib/content";
import { useLaunch, money } from "@/lib/use-launch";

type Plan = "starter" | "custom";

declare global {
  interface Window {
    fbq?: (...args: unknown[]) => void;
    ttq?: { track: (event: string, data?: Record<string, unknown>) => void };
  }
}

const PASS_THROUGH = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"];

/** Carries ad UTMs through to Gumroad so sales can be traced back to the ad that sent them. */
function withUtm(base: string, search: string) {
  if (!search) return base;
  const incoming = new URLSearchParams(search);
  const url = new URL(base);
  for (const key of PASS_THROUGH) {
    const v = incoming.get(key);
    if (v && !url.searchParams.has(key)) url.searchParams.set(key, v);
  }
  return url.toString();
}

export function useCheckoutHref(plan: Plan) {
  const { active } = useLaunch();
  const base = plan === "custom" ? LINKS.custom : active ? LINKS.starterLaunch : LINKS.starterRegular;
  const [href, setHref] = useState<string>(base);
  useEffect(() => setHref(withUtm(base, window.location.search)), [base]);
  return href;
}

export function CheckoutLink({
  plan = "starter",
  className = "",
  children,
  placement,
}: {
  plan?: Plan;
  className?: string;
  children: React.ReactNode;
  placement: string;
}) {
  const href = useCheckoutHref(plan);
  const { price } = useLaunch();
  const value = plan === "custom" ? PRICING.customPrice : price;

  return (
    <a
      href={href}
      className={className}
      data-placement={placement}
      onClick={() => {
        window.fbq?.("track", "InitiateCheckout", { value, currency: "USD", content_name: plan });
        window.ttq?.track("InitiateCheckout", { value, currency: "USD", content_id: plan });
      }}
    >
      {children}
    </a>
  );
}

/** Price that follows the launch window. */
export function StarterPrice({ className = "" }: { className?: string }) {
  const { price } = useLaunch();
  return <span className={className}>{money(price)}</span>;
}
