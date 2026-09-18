"use client";

import { useSyncExternalStore } from "react";
import fixture from "@/data/kuzco-fixture.json";
import type { HangTagSku } from "@/data/sku";
import {
  CATALOG_CHANGE_EVENT,
  CATALOG_STORAGE_KEY,
  parseStoredCatalog,
} from "@/lib/catalog";

const FIXTURE = fixture as HangTagSku[];

export type CatalogState = {
  skus: HangTagSku[];
  imported: boolean;
};

const SERVER_STATE: CatalogState = { skus: FIXTURE, imported: false };

let cachedRaw: string | null | undefined;
let cachedState: CatalogState = SERVER_STATE;

function subscribe(onChange: () => void) {
  const handler = () => onChange();
  window.addEventListener("storage", handler);
  window.addEventListener(CATALOG_CHANGE_EVENT, handler);
  return () => {
    window.removeEventListener("storage", handler);
    window.removeEventListener(CATALOG_CHANGE_EVENT, handler);
  };
}

function readCatalog(): CatalogState {
  const raw = window.localStorage.getItem(CATALOG_STORAGE_KEY);
  if (raw === cachedRaw) return cachedState;
  cachedRaw = raw;
  const parsed = parseStoredCatalog(raw);
  cachedState = parsed
    ? { skus: parsed, imported: true }
    : { skus: FIXTURE, imported: false };
  return cachedState;
}

export function useCatalog(): CatalogState {
  return useSyncExternalStore(subscribe, readCatalog, () => SERVER_STATE);
}
