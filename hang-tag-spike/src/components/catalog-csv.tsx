"use client";

import { useRef, useState } from "react";
import {
  CATALOG_MAP_STORAGE_KEY,
  SKU_FIELD_KEYS,
  SKU_FIELD_LABELS,
  clearStoredCatalog,
  guessColumnMap,
  parseStoredMap,
  rowsToCatalog,
  writeStoredCatalog,
  writeStoredMap,
  type CatalogColumnMap,
  type SkuFieldKey,
} from "@/lib/catalog";
import { parseCsv } from "@/lib/csv";
import { useCatalog } from "@/lib/use-catalog";

type PendingCsv = {
  name: string;
  headers: string[];
  rows: Record<string, string>[];
  map: CatalogColumnMap;
};

function loadSavedMap(): CatalogColumnMap | null {
  return parseStoredMap(window.localStorage.getItem(CATALOG_MAP_STORAGE_KEY));
}

export function CatalogCsv() {
  const { skus, imported } = useCatalog();
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [pending, setPending] = useState<PendingCsv | null>(null);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");

  async function onFile(file: File | undefined) {
    setError("");
    setStatus("");
    if (!file) return;
    const text = await file.text();
    const table = parseCsv(text);
    if (!table.headers.length || !table.rows.length) {
      setPending(null);
      setError("That CSV has no header row or data rows.");
      return;
    }
    setPending({
      name: file.name,
      headers: table.headers,
      rows: table.rows,
      map: guessColumnMap(table.headers, loadSavedMap()),
    });
  }

  function setField(field: SkuFieldKey, header: string) {
    setPending((current) => {
      if (!current) return current;
      const map = { ...current.map };
      if (!header) delete map[field];
      else {
        for (const key of SKU_FIELD_KEYS) {
          if (key !== field && map[key] === header) delete map[key];
        }
        map[field] = header;
      }
      return { ...current, map };
    });
  }

  async function applyPending() {
    if (!pending) return;
    const result = rowsToCatalog(pending.rows, pending.map);
    if (!result.kept) {
      setError(
        `No printable rows. Need item_number plus collection_name (or LongDesc / name if collection isn’t mapped). Skipped ${result.skipped}.`,
      );
      return;
    }
    writeStoredMap(pending.map);
    await writeStoredCatalog(result.skus);
    setStatus(
      result.skipped
        ? `${result.kept} SKUs in this browser · skipped ${result.skipped} incomplete rows`
        : `${result.kept} SKUs in this browser`,
    );
    setError("");
    setPending(null);
    if (inputRef.current) inputRef.current.value = "";
  }

  async function clearCsv() {
    await clearStoredCatalog();
    setPending(null);
    setError("");
    setStatus("Back to the 10-SKU fixture. Column map kept.");
    if (inputRef.current) inputRef.current.value = "";
  }

  return (
    <div className="kf-field">
      <span className="kf-field-label">Catalog CSV</span>
      <span className="kf-field-hint">
        {imported
          ? `${skus.length} imported SKUs in this browser (all three stocks). Not the git fixture.`
          : "No CSV loaded. Sheet products use the 10-SKU Kuzco fixture."}{" "}
        ImageFileName values are FTP names — the first jpg is loaded from Kuzco’s
        SuperCat CDN. Sample:{" "}
        <a href="/samples/kuzco-hang-tags.csv" download>
          kuzco-hang-tags.csv
        </a>
      </span>
      <input
        ref={inputRef}
        className="kf-input kf-md"
        type="file"
        accept=".csv,text/csv"
        onChange={(event) => void onFile(event.target.files?.[0])}
      />
      {pending ? (
        <>
          <span className="kf-field-hint">
            {pending.name} · {pending.rows.length} rows. Guessed from headers;
            fix the map, then use this catalog.
          </span>
          <div className="catalog-map">
            {SKU_FIELD_KEYS.map((field) => (
              <label className="catalog-map-row" key={field}>
                <span>{SKU_FIELD_LABELS[field]}</span>
                <select
                  className="kf-input kf-md"
                  value={pending.map[field] ?? ""}
                  onChange={(event) => setField(field, event.target.value)}
                >
                  <option value="">—</option>
                  {pending.headers.map((header) => (
                    <option key={header} value={header}>
                      {header || "(empty header)"}
                    </option>
                  ))}
                </select>
              </label>
            ))}
          </div>
          <div className="hang-tag-actions">
            <button
              className="kb kb-sm kb-primary"
              type="button"
              onClick={() => void applyPending()}
            >
              Use this catalog
            </button>
          </div>
        </>
      ) : null}
      {imported ? (
        <div className="hang-tag-actions">
          <button
            className="kb kb-sm kb-secondary"
            type="button"
            onClick={() => void clearCsv()}
          >
            Clear CSV
          </button>
        </div>
      ) : null}
      {error ? <span className="catalog-csv-error">{error}</span> : null}
      {status ? <span className="kf-field-hint">{status}</span> : null}
    </div>
  );
}
