"use client";

import { useId, useState } from "react";
import { LINKS } from "@/lib/content";
import { trackCustom } from "@/lib/tracking";

/**
 * Posts to the same Brevo list as the live site. The form targets a hidden iframe,
 * so the visitor never leaves the page.
 */
export function EmailCapture() {
  const id = useId();
  const [sent, setSent] = useState(false);

  if (sent)
    return (
      <p role="status" className="rounded-field bg-accent-soft px-4 py-3 text-cream">
        Got it. Check your inbox soon for your free recipe.
      </p>
    );

  return (
    <>
      <iframe name="ss-brevo-frame" title="Newsletter signup" className="hidden" />
      <form
        method="POST"
        action={LINKS.brevoForm}
        target="ss-brevo-frame"
        onSubmit={() => {
          trackCustom("Lead", { source: "free-recipe" });
          window.setTimeout(() => setSent(true), 400);
        }}
      >
        {/* honeypot, same as the live form */}
        <input type="text" name="email_address_check" defaultValue="" tabIndex={-1} autoComplete="off" aria-hidden className="absolute -left-[9999px]" />
        <label htmlFor={id} className="mb-2 block text-sm font-medium text-cream">
          Your email
        </label>
        <div className="flex flex-col gap-2 sm:flex-row">
          <input
            id={id}
            type="email"
            name="EMAIL"
            required
            autoComplete="email"
            placeholder="you@email.com"
            className="min-w-0 flex-1 rounded-field bg-raised px-4 py-3 text-cream placeholder:text-faint shadow-[inset_0_0_0_1px_var(--color-line-strong)] outline-none focus:shadow-[inset_0_0_0_2px_var(--color-accent)]"
          />
          <button type="submit" className="btn btn-primary px-5 py-3 text-sm">
            Send me a recipe
          </button>
        </div>
        <p className="mt-2 text-xs text-faint">One email, no spam. Unsubscribe anytime.</p>
      </form>
    </>
  );
}
