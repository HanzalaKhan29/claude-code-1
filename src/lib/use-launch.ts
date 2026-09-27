"use client";

import { useEffect, useState } from "react";
import { PRICING } from "./content";

const END = new Date(PRICING.launchEndsAt).getTime();

export type LaunchState = {
  /** null until mounted, so server and client render the same markup */
  msLeft: number | null;
  active: boolean;
  price: number;
};

export function useLaunch(): LaunchState {
  const [msLeft, setMsLeft] = useState<number | null>(null);

  useEffect(() => {
    const tick = () => setMsLeft(Math.max(0, END - Date.now()));
    tick();
    const id = window.setInterval(tick, 1000);
    return () => window.clearInterval(id);
  }, []);

  // Before mount we assume the launch is on so server and client markup match.
  const active = msLeft === null ? true : msLeft > 0;
  return { msLeft, active, price: active ? PRICING.launchPrice : PRICING.regularPrice };
}

export function splitTime(ms: number) {
  const s = Math.floor(ms / 1000);
  return {
    d: Math.floor(s / 86400),
    h: Math.floor((s % 86400) / 3600),
    m: Math.floor((s % 3600) / 60),
    s: s % 60,
  };
}

export const money = (n: number) => `$${n % 1 === 0 ? n.toFixed(0) : n.toFixed(2)}`;
