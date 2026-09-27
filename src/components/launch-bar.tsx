"use client";

import { useLaunch, splitTime } from "@/lib/use-launch";

const pad = (n: number) => String(n).padStart(2, "0");

export function Countdown({ className = "" }: { className?: string }) {
  const { msLeft } = useLaunch();
  if (msLeft === null) return <span className={className}>Oct 1</span>;
  const t = splitTime(msLeft);
  return (
    <span className={`font-mono tabular-nums ${className}`} aria-label={`${t.d} days ${t.h} hours ${t.m} minutes left`}>
      {t.d}d {pad(t.h)}h {pad(t.m)}m {pad(t.s)}s
    </span>
  );
}

export function LaunchOnly({ children }: { children: React.ReactNode }) {
  const { active } = useLaunch();
  return active ? <>{children}</> : null;
}

export function LaunchBar() {
  const { active } = useLaunch();
  if (!active) return null;
  return (
    <div className="relative z-40 border-b border-line bg-night text-[13px] text-muted">
      <div className="mx-auto flex max-w-7xl items-center justify-center gap-2 px-4 py-2 text-center">
        <span>
          <strong className="font-semibold text-cream">Launch price, 45% off.</strong>{" "}
          <span className="hidden sm:inline">Goes up to $35 in </span>
          <span className="sm:hidden">Ends in </span>
        </span>
        <Countdown className="text-accent" />
      </div>
    </div>
  );
}
