"use client";

import { useSyncExternalStore } from "react";
import fixture from "@/data/kuzco-fixture.json";
import type { HangTagSku } from "@/data/sku";
import {
  CATALOG_CHANGE_EVENT,
  CATALOG_STORAGE_KEY,
  hydrateStoredCatalog,
  memoryImportedCatalog,
  parseStoredCatalog,
} from "@/lib/catalog";

const FIXTURE = fixture as HangTagSku[];

export type CatalogState = {
  skus: HangTagSku[];
  imported: boolean;
};

const SERVER_STATE: CatalogState = { skus: FIXTURE, imported: false };

let cachedKey = "";
let cachedState: CatalogState = SERVER_STATE;

function subscribe(onChange: () => void) {
  const handler = () => onChange();
  window.addEventListener("storage", handler);
  window.addEventListener(CATALOG_CHANGE_EVENT, handler);
  void hydrateStoredCatalog().then(() => onChange());
  return () => {
    window.removeEventListener("storage", handler);
    window.removeEventListener(CATALOG_CHANGE_EVENT, handler);
  };
}

function readCatalog(): CatalogState {
  const memory = memoryImportedCatalog();
  if (Array.isArray(memory) && memory.length) {
    const key = `mem:${memory.length}:${memory[0]?.item_number}`;
    if (key === cachedKey) return cachedState;
    cachedKey = key;
    cachedState = { skus: memory, imported: true };
    return cachedState;
  }
  if (memory === null) {
    if (cachedKey === "fixture") return cachedState;
    cachedKey = "fixture";
    cachedState = SERVER_STATE;
    return cachedState;
  }
  const raw = window.localStorage.getItem(CATALOG_STORAGE_KEY);
  const key = `ls:${raw ?? ""}`;
  if (key === cachedKey) return cachedState;
  cachedKey = key;
  const parsed = parseStoredCatalog(raw);
  cachedState = parsed
    ? { skus: parsed, imported: true }
    : SERVER_STATE;
  return cachedState;
}

export function useCatalog(): CatalogState {
  return useSyncExternalStore(subscribe, readCatalog, () => SERVER_STATE);
}
