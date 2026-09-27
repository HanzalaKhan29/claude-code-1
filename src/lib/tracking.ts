"use client";

// Ported from the live site so ad data stays continuous:
// same Meta Pixel, same consent key, same event names and values.
import { TRACKING } from "./content";

const CONSENT_KEY = "ssCookieConsent";

type Fbq = ((...args: unknown[]) => void) & { callMethod?: (...a: unknown[]) => void; queue?: unknown[]; loaded?: boolean; version?: string; push?: unknown };

declare global {
  interface Window {
    fbq?: Fbq;
    _fbq?: Fbq;
    __ssPixelActive?: boolean;
  }
}

export type Consent = "accepted" | "declined" | null;

export function readConsent(): Consent {
  try {
    const v = localStorage.getItem(CONSENT_KEY);
    return v === "accepted" || v === "declined" ? v : null;
  } catch {
    return null;
  }
}

export function writeConsent(v: "accepted" | "declined") {
  try {
    localStorage.setItem(CONSENT_KEY, v);
  } catch {}
}

/** Prior opt-in is a UK/EU requirement. Everyone else is counted right away and can opt out. */
export function looksEUorUK(): boolean {
  try {
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
    return /^Europe\//.test(tz) || /^Atlantic\/(Faroe|Canary|Madeira)$/.test(tz);
  } catch {
    return true;
  }
}

export function loadPixel() {
  if (typeof window === "undefined" || window.__ssPixelActive || !TRACKING.metaPixelId) return;
  window.__ssPixelActive = true;
  const n = function (...args: unknown[]) {
    if (n.callMethod) n.callMethod(...args);
    else n.queue!.push(args);
  } as Fbq;
  if (!window._fbq) window._fbq = n;
  n.push = n;
  n.loaded = true;
  n.version = "2.0";
  n.queue = [];
  window.fbq = n;
  const s = document.createElement("script");
  s.async = true;
  s.src = "https://connect.facebook.net/en_US/fbevents.js";
  document.head.appendChild(s);
  window.fbq("init", TRACKING.metaPixelId);
  window.fbq("track", "PageView");
  window.fbq("track", "ViewContent", {
    content_name: "Solo & Starving? The Interactive Cookbook",
    value: 19.25,
    currency: "USD",
  });
}

export function track(event: string, data?: Record<string, unknown>) {
  try {
    window.fbq?.("track", event, data ?? {});
  } catch {}
}

export function trackCustom(event: string, data?: Record<string, unknown>) {
  try {
    window.fbq?.("trackCustom", event, data ?? {});
  } catch {}
}

/* ------------------------------------------------ attribution */

const AFF_KEY = "ssAffiliateId";
const AFF_TTL = 30 * 24 * 60 * 60 * 1000; // matches Gumroad's own affiliate cookie
const UTM = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"];

/** Gumroad affiliate id from ?a= / ?affiliate_id= / ?aff= / ?aff_id= / ?ref=, remembered for 30 days. */
export function affiliateId(): string | null {
  try {
    const q = new URLSearchParams(window.location.search);
    const incoming = q.get("a") || q.get("affiliate_id") || q.get("aff") || q.get("aff_id") || q.get("ref");
    const now = Date.now();
    if (incoming) {
      localStorage.setItem(AFF_KEY, JSON.stringify({ id: incoming, ts: now }));
      return incoming;
    }
    const raw = localStorage.getItem(AFF_KEY);
    if (raw) {
      const p = JSON.parse(raw) as { id?: string; ts?: number };
      if (p.id && p.ts && now - p.ts < AFF_TTL) return p.id;
    }
  } catch {}
  return null;
}

/** Adds the affiliate id and the ad's UTMs to a Gumroad link. */
export function attribute(base: string): string {
  try {
    const url = new URL(base);
    const q = new URLSearchParams(window.location.search);
    for (const k of UTM) {
      const v = q.get(k);
      if (v && !url.searchParams.has(k)) url.searchParams.set(k, v);
    }
    const aff = affiliateId();
    if (aff && !url.searchParams.has("a")) url.searchParams.set("a", aff);
    return url.toString();
  } catch {
    return base;
  }
}

/* ------------------------------------------------ currency hint */

const RATES: Record<string, number> = {
  EUR: 0.92, GBP: 0.79, CHF: 0.88, SEK: 10.4, NOK: 10.6, DKK: 6.9, PLN: 4.0, CZK: 23.5, HUF: 385, RON: 4.6, TRY: 34.2,
  ISK: 138, CAD: 1.38, AUD: 1.53, NZD: 1.66, INR: 83.3, JPY: 149, KRW: 1360, PHP: 56, THB: 34.7, IDR: 15900, MYR: 4.4,
  SGD: 1.34, HKD: 7.8, VND: 24500, CNY: 7.1, BRL: 5.4, MXN: 18.3, ARS: 990, CLP: 940, COP: 4100, ZAR: 18.1, AED: 3.67,
  SAR: 3.75, ILS: 3.7, TND: 3.1, EGP: 48,
};
const REGION: Record<string, string> = {
  US: "USD", GB: "GBP", IE: "EUR", DE: "EUR", FR: "EUR", IT: "EUR", ES: "EUR", PT: "EUR", NL: "EUR", BE: "EUR", AT: "EUR",
  FI: "EUR", GR: "EUR", LU: "EUR", SK: "EUR", SI: "EUR", EE: "EUR", LV: "EUR", LT: "EUR", CY: "EUR", MT: "EUR", HR: "EUR",
  CH: "CHF", SE: "SEK", NO: "NOK", DK: "DKK", PL: "PLN", CZ: "CZK", HU: "HUF", RO: "RON", TR: "TRY", IS: "ISK", CA: "CAD",
  AU: "AUD", NZ: "NZD", IN: "INR", JP: "JPY", KR: "KRW", PH: "PHP", TH: "THB", ID: "IDR", MY: "MYR", SG: "SGD", HK: "HKD",
  VN: "VND", CN: "CNY", BR: "BRL", MX: "MXN", AR: "ARS", CL: "CLP", CO: "COP", ZA: "ZAR", AE: "AED", SA: "SAR", IL: "ILS",
  TN: "TND", EG: "EGP",
};
const TZ: Record<string, string> = {
  "Europe/London": "GBP", "Europe/Zurich": "CHF", "Europe/Oslo": "NOK", "Europe/Stockholm": "SEK", "Europe/Copenhagen": "DKK",
  "Europe/Warsaw": "PLN", "Europe/Prague": "CZK", "Europe/Budapest": "HUF", "Europe/Bucharest": "RON", "Europe/Istanbul": "TRY",
  "Europe/Reykjavik": "ISK", "Africa/Tunis": "TND", "Africa/Cairo": "EGP", "Africa/Johannesburg": "ZAR", "Asia/Kolkata": "INR",
  "Asia/Calcutta": "INR", "Asia/Tokyo": "JPY", "Asia/Seoul": "KRW", "Asia/Manila": "PHP", "Asia/Bangkok": "THB",
  "Asia/Jakarta": "IDR", "Asia/Kuala_Lumpur": "MYR", "Asia/Singapore": "SGD", "Asia/Hong_Kong": "HKD", "Asia/Ho_Chi_Minh": "VND",
  "Asia/Shanghai": "CNY", "Asia/Dubai": "AED", "Asia/Riyadh": "SAR", "Asia/Jerusalem": "ILS", "Pacific/Auckland": "NZD",
  "America/Toronto": "CAD", "America/Vancouver": "CAD", "America/Edmonton": "CAD", "America/Winnipeg": "CAD",
  "America/Halifax": "CAD", "America/Mexico_City": "MXN", "America/Tijuana": "MXN", "America/Sao_Paulo": "BRL",
  "America/Argentina/Buenos_Aires": "ARS", "America/Bogota": "COP", "America/Santiago": "CLP",
};

/** Time zone first (in-app browsers often report a bare "en"), then language region. */
function detectCurrency(): { code: string; locale: string } {
  let locale = "en-US";
  try {
    locale = navigator.languages?.[0] || navigator.language || "en-US";
  } catch {}
  let code: string | undefined;
  try {
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
    code = TZ[tz] ?? (/^Europe\//.test(tz) ? "EUR" : /^Australia\//.test(tz) ? "AUD" : undefined);
  } catch {}
  const parts = locale.split("-");
  const region = parts.length > 1 ? parts[parts.length - 1].toUpperCase() : "";
  return { code: code || REGION[region] || "USD", locale };
}

/** "about €17.71" for non-US visitors, empty string for USD. */
export function approx(usd: number): string {
  try {
    const { code, locale } = detectCurrency();
    if (code === "USD" || !RATES[code]) return "";
    const v = usd * RATES[code];
    return new Intl.NumberFormat(locale, { style: "currency", currency: code, maximumFractionDigits: v >= 100 ? 0 : 2 }).format(v);
  } catch {
    return "";
  }
}
