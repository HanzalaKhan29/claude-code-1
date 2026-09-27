"use client";

import { useEffect, useState } from "react";
import { LINKS, PRICING } from "@/lib/content";
import { useLaunch, money } from "@/lib/use-launch";
import { approx, attribute, track } from "@/lib/tracking";

type Plan = "starter" | "custom";

export function useCheckoutHref(plan: Plan) {
  const { active } = useLaunch();
  const base = plan === "custom" ? LINKS.custom : active ? LINKS.starterLaunch : LINKS.starterRegular;
  const [href, setHref] = useState<string>(base);
  useEffect(() => setHref(attribute(base)), [base]);
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

  return (
    <a
      href={href}
      className={className}
      data-placement={placement}
      onClick={() =>
        track("InitiateCheckout", {
          content_name: plan === "custom" ? "Solo & Starving? Custom Plan" : "Solo & Starving? The Interactive Cookbook",
          value: plan === "custom" ? PRICING.customPrice : price,
          currency: "USD",
        })
      }
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

/** "about €17.71, charged in USD" for visitors outside the US. Renders nothing for US visitors. */
export function LocalPrice({ plan = "starter", className = "" }: { plan?: Plan; className?: string }) {
  const { price } = useLaunch();
  const usd = plan === "custom" ? PRICING.customPrice : price;
  const [text, setText] = useState("");
  useEffect(() => setText(approx(usd)), [usd]);
  if (!text) return null;
  return <span className={className}>About {text}, charged in USD</span>;
}
