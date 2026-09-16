"use client";

import { useSyncExternalStore } from "react";
import {
  DEFAULT_TEMPLATES,
  parseStoredTemplate,
  STORAGE_KEY,
  templateStorageKey,
  type HangTagTemplate,
} from "@/data/template";
import type { SheetCode } from "@/data/sheets";

const cache = new Map<string, HangTagTemplate>();

function subscribe(onChange: () => void) {
  window.addEventListener("storage", onChange);
  return () => window.removeEventListener("storage", onChange);
}

function readTemplate(stock: SheetCode): HangTagTemplate {
  const fallback = DEFAULT_TEMPLATES[stock];
  const raw =
    window.localStorage.getItem(templateStorageKey(stock)) ??
    (stock === "5371" ? window.localStorage.getItem(STORAGE_KEY) : null);
  const key = `${stock}::${raw ?? ""}`;
  const hit = cache.get(key);
  if (hit) return hit;
  const value = parseStoredTemplate(raw, stock) ?? fallback;
  cache.set(key, value);
  return value;
}

export function useStoredTemplate(stock: SheetCode): HangTagTemplate {
  const fallback = DEFAULT_TEMPLATES[stock];
  return useSyncExternalStore(
    subscribe,
    () => readTemplate(stock),
    () => fallback,
  );
}
