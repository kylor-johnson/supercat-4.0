import type { HangTagSku } from "@/data/sku";
import { BOOLEAN_BINDINGS } from "@/data/sku";

export const CATALOG_STORAGE_KEY = "hang-tag-catalog-v1";
export const CATALOG_MAP_STORAGE_KEY = "hang-tag-catalog-map-v1";
export const CATALOG_CHANGE_EVENT = "hang-tag-catalog-change";

export const SKU_FIELD_KEYS = [
  "item_number",
  "collection_name",
  "upc_value",
  "image",
  "us_imap",
  "cad_imap",
  "c.MarketSpecial",
  "c.QuickShip",
  "c.ContainerDiscount",
  "FinishOptions",
  "LampType",
  "Voltage",
  "ColorTemperature",
  "Wattage",
  "Lumens",
  "product_dimensions_in",
] as const satisfies ReadonlyArray<keyof HangTagSku>;

export type SkuFieldKey = (typeof SKU_FIELD_KEYS)[number];
export type CatalogColumnMap = Partial<Record<SkuFieldKey, string>>;

export const SKU_FIELD_LABELS: Record<SkuFieldKey, string> = {
  item_number: "item_number",
  collection_name: "collection_name",
  upc_value: "upc_value",
  image: "image",
  us_imap: "us_imap",
  cad_imap: "cad_imap",
  "c.MarketSpecial": "c.MarketSpecial",
  "c.QuickShip": "c.QuickShip",
  "c.ContainerDiscount": "c.ContainerDiscount",
  FinishOptions: "c.FinishOptions",
  LampType: "c.LampType",
  Voltage: "c.Voltage",
  ColorTemperature: "c.ColorTemperature",
  Wattage: "c.Wattage",
  Lumens: "c.Lumens",
  product_dimensions_in: "product_dimensions_in",
};

const FIELD_ALIASES: Record<SkuFieldKey, string[]> = {
  item_number: [
    "item_number",
    "itemnumber",
    "baseitemcode",
    "sku",
    "itemcode",
    "item",
  ],
  collection_name: [],
  upc_value: ["upc_value", "upcvalue", "upc", "barcode"],
  image: [
    "image",
    "imagefilename",
    "imageurl",
    "url",
    "photo",
    "photourl",
    "primaryimage",
  ],
  us_imap: [
    "us_imap",
    "usimap",
    "priceusimap",
    "priceus",
    "imap",
    "pl.usimap",
  ],
  cad_imap: [
    "cad_imap",
    "cadimap",
    "pricecadimap",
    "pricecad",
    "pl.cadimap",
  ],
  "c.MarketSpecial": [
    "c.marketspecial",
    "marketspecial",
    "marketspecialflag",
  ],
  "c.QuickShip": ["c.quickship", "quickship", "qs"],
  "c.ContainerDiscount": [
    "c.containerdiscount",
    "containerdiscount",
  ],
  FinishOptions: ["finishoptions", "c.finishoptions", "finish"],
  LampType: ["lamptype", "c.lamptype", "lamp"],
  Voltage: ["voltage", "c.voltage"],
  ColorTemperature: [
    "colortemperature",
    "c.colortemperature",
    "cct",
  ],
  Wattage: ["wattage", "c.wattage"],
  Lumens: ["lumens", "c.lumens"],
  product_dimensions_in: [
    "product_dimensions_in",
    "productdimensionsin",
    "dimensions",
    "size",
  ],
};

const COLLECTION_ALIASES = [
  "collection_name",
  "collectionname",
  "collection",
  "collectioncodes",
  "collectioncode",
];

const NAME_ALIASES = ["longdesc", "name", "productname", "product"];

export function normalizeHeader(value: string): string {
  return value.trim().toLowerCase().replace(/[\s_-]+/g, "");
}

function emptySku(): HangTagSku {
  return {
    item_number: "",
    collection_name: "",
    FinishOptions: "",
    LampType: "",
    Voltage: "",
    ColorTemperature: "",
    Wattage: "",
    Lumens: "",
    product_dimensions_in: "",
    us_imap: "",
    cad_imap: "",
    upc_value: "",
    image: "",
    "c.MarketSpecial": false,
    "c.QuickShip": false,
    "c.ContainerDiscount": false,
  };
}

export function parseBooleanCell(raw: string): boolean {
  const value = raw.trim().toLowerCase();
  return value === "y" || value === "true" || value === "1" || value === "yes";
}

function takeHeader(
  headers: string[],
  unused: Set<string>,
  aliases: string[],
): string | undefined {
  const wanted = new Set(aliases.map(normalizeHeader));
  for (const header of headers) {
    if (!unused.has(header)) continue;
    if (wanted.has(normalizeHeader(header))) {
      unused.delete(header);
      return header;
    }
  }
}

export function guessColumnMap(
  headers: string[],
  saved?: CatalogColumnMap | null,
): CatalogColumnMap {
  const unused = new Set(headers);
  const map: CatalogColumnMap = {};

  if (saved) {
    for (const field of SKU_FIELD_KEYS) {
      const previous = saved[field];
      if (!previous) continue;
      const match = headers.find(
        (header) =>
          unused.has(header) &&
          normalizeHeader(header) === normalizeHeader(previous),
      );
      if (match) {
        map[field] = match;
        unused.delete(match);
      }
    }
  }

  for (const field of SKU_FIELD_KEYS) {
    if (map[field]) continue;
    if (field === "collection_name") {
      const collection = takeHeader(headers, unused, COLLECTION_ALIASES);
      map.collection_name =
        collection ?? takeHeader(headers, unused, NAME_ALIASES);
      continue;
    }
    const hit = takeHeader(headers, unused, FIELD_ALIASES[field]);
    if (hit) map[field] = hit;
  }

  return map;
}

export function cellFor(
  row: Record<string, string>,
  header: string | undefined,
): string {
  if (!header) return "";
  return (row[header] ?? "").trim();
}

export const KUZCO_IMAGE_CDN =
  "https://supercatcdn.global.ssl.fastly.net/kll/product_image/full";

export function resolveImageSrc(raw: string): string {
  const first = raw.split(",")[0]?.trim() ?? "";
  if (!first) return "";
  if (/^https:\/\//i.test(first) || first.startsWith("/")) return first;
  if (/^http:\/\//i.test(first)) return "";
  const file = first.split(/[\\/]/).pop() ?? first;
  if (!/\.(jpe?g|png|webp|gif)$/i.test(file)) return "";
  return `${KUZCO_IMAGE_CDN}/${encodeURIComponent(file)}`;
}

export function rowToSku(
  row: Record<string, string>,
  map: CatalogColumnMap,
): HangTagSku | null {
  const sku = emptySku();
  sku.item_number = cellFor(row, map.item_number);
  sku.collection_name = cellFor(row, map.collection_name);
  if (!sku.item_number || !sku.collection_name) return null;

  sku.upc_value = cellFor(row, map.upc_value);
  sku.image = resolveImageSrc(cellFor(row, map.image));
  sku.us_imap = cellFor(row, map.us_imap);
  sku.cad_imap = cellFor(row, map.cad_imap);
  sku.FinishOptions = cellFor(row, map.FinishOptions);
  sku.LampType = cellFor(row, map.LampType);
  sku.Voltage = cellFor(row, map.Voltage);
  sku.ColorTemperature = cellFor(row, map.ColorTemperature);
  sku.Wattage = cellFor(row, map.Wattage);
  sku.Lumens = cellFor(row, map.Lumens);
  sku.product_dimensions_in = cellFor(row, map.product_dimensions_in);

  for (const flag of BOOLEAN_BINDINGS) {
    const header = map[flag];
    sku[flag] = header ? parseBooleanCell(cellFor(row, header)) : false;
  }

  return sku;
}

export type CatalogImportResult = {
  skus: HangTagSku[];
  kept: number;
  skipped: number;
};

export function rowsToCatalog(
  rows: Record<string, string>[],
  map: CatalogColumnMap,
): CatalogImportResult {
  const skus: HangTagSku[] = [];
  let skipped = 0;
  for (const row of rows) {
    const sku = rowToSku(row, map);
    if (!sku) {
      skipped += 1;
      continue;
    }
    skus.push(sku);
  }
  return { skus, kept: skus.length, skipped };
}

function isSkuField(value: string): value is SkuFieldKey {
  return (SKU_FIELD_KEYS as readonly string[]).includes(value);
}

export function parseStoredMap(raw: string | null): CatalogColumnMap | null {
  if (!raw) return null;
  try {
    const data = JSON.parse(raw) as Record<string, unknown>;
    if (!data || typeof data !== "object" || Array.isArray(data)) return null;
    const map: CatalogColumnMap = {};
    for (const [field, header] of Object.entries(data)) {
      if (isSkuField(field) && typeof header === "string" && header.trim()) {
        map[field] = header;
      }
    }
    return Object.keys(map).length ? map : null;
  } catch {
    return null;
  }
}

function coerceSku(value: unknown): HangTagSku | null {
  if (!value || typeof value !== "object") return null;
  const row = value as Record<string, unknown>;
  const sku = emptySku();
  sku.item_number = String(row.item_number ?? "").trim();
  sku.collection_name = String(row.collection_name ?? "").trim();
  if (!sku.item_number || !sku.collection_name) return null;
  sku.FinishOptions = String(row.FinishOptions ?? "");
  sku.LampType = String(row.LampType ?? "");
  sku.Voltage = String(row.Voltage ?? "");
  sku.ColorTemperature = String(row.ColorTemperature ?? "");
  sku.Wattage = String(row.Wattage ?? "");
  sku.Lumens = String(row.Lumens ?? "");
  sku.product_dimensions_in = String(row.product_dimensions_in ?? "");
  sku.us_imap = String(row.us_imap ?? "");
  sku.cad_imap = String(row.cad_imap ?? "");
  sku.upc_value = String(row.upc_value ?? "");
  sku.image = resolveImageSrc(String(row.image ?? ""));
  for (const flag of BOOLEAN_BINDINGS) {
    const raw = row[flag];
    sku[flag] =
      typeof raw === "boolean" ? raw : parseBooleanCell(String(raw ?? ""));
  }
  return sku;
}

export function parseStoredCatalog(raw: string | null): HangTagSku[] | null {
  if (!raw) return null;
  try {
    const data = JSON.parse(raw) as unknown;
    if (!Array.isArray(data) || data.length === 0) return null;
    const skus = data
      .map(coerceSku)
      .filter((sku): sku is HangTagSku => Boolean(sku));
    return skus.length ? skus : null;
  } catch {
    return null;
  }
}

export function writeStoredMap(map: CatalogColumnMap) {
  window.localStorage.setItem(CATALOG_MAP_STORAGE_KEY, JSON.stringify(map));
}

const IDB_NAME = "hang-tag-catalog-v1";
const IDB_STORE = "catalog";
const IDB_KEY = "skus";

let memoryCatalog: HangTagSku[] | null | undefined;

export function memoryImportedCatalog(): HangTagSku[] | null | undefined {
  return memoryCatalog;
}

function openCatalogDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = window.indexedDB.open(IDB_NAME, 1);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains(IDB_STORE)) {
        db.createObjectStore(IDB_STORE);
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

async function idbWrite(skus: HangTagSku[]) {
  const db = await openCatalogDb();
  await new Promise<void>((resolve, reject) => {
    const tx = db.transaction(IDB_STORE, "readwrite");
    tx.objectStore(IDB_STORE).put(skus, IDB_KEY);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
  db.close();
}

async function idbRead(): Promise<HangTagSku[] | null> {
  const db = await openCatalogDb();
  const skus = await new Promise<unknown>((resolve, reject) => {
    const tx = db.transaction(IDB_STORE, "readonly");
    const request = tx.objectStore(IDB_STORE).get(IDB_KEY);
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
  db.close();
  if (!Array.isArray(skus)) return null;
  return parseStoredCatalog(JSON.stringify(skus));
}

async function idbClear() {
  try {
    const db = await openCatalogDb();
    await new Promise<void>((resolve, reject) => {
      const tx = db.transaction(IDB_STORE, "readwrite");
      tx.objectStore(IDB_STORE).delete(IDB_KEY);
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
    db.close();
  } catch {
    // IndexedDB may be missing in private mode.
  }
}

function notifyCatalogChange() {
  window.dispatchEvent(new Event(CATALOG_CHANGE_EVENT));
}

export async function writeStoredCatalog(skus: HangTagSku[]) {
  memoryCatalog = skus;
  const json = JSON.stringify(skus);
  try {
    window.localStorage.setItem(CATALOG_STORAGE_KEY, json);
    await idbClear();
  } catch {
    window.localStorage.removeItem(CATALOG_STORAGE_KEY);
    await idbWrite(skus);
  }
  notifyCatalogChange();
}

export async function clearStoredCatalog() {
  memoryCatalog = null;
  window.localStorage.removeItem(CATALOG_STORAGE_KEY);
  await idbClear();
  notifyCatalogChange();
}

export async function hydrateStoredCatalog(): Promise<HangTagSku[] | null> {
  if (memoryCatalog !== undefined) {
    return memoryCatalog;
  }
  const fromLs = parseStoredCatalog(
    window.localStorage.getItem(CATALOG_STORAGE_KEY),
  );
  if (fromLs) {
    memoryCatalog = fromLs;
    return fromLs;
  }
  const fromIdb = await idbRead();
  memoryCatalog = fromIdb;
  return fromIdb;
}
