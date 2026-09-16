"use client";

import { useEffect, useState } from "react";
import { TemplateTag } from "@/components/template-tag";
import { SHEETS, type SheetCode } from "@/data/sheets";
import type { HangTagSku } from "@/data/sku";
import {
  DEFAULT_TEMPLATES,
  parseStoredTemplate,
  STORAGE_KEY,
  templateStorageKey,
  type HangTagTemplate,
} from "@/data/template";

const TAGS_PER_SHEET: Record<SheetCode, number> = {
  "5371": 10,
  "5392": 6,
};

export function TemplateSheet({
  stock,
  skus,
}: {
  stock: SheetCode;
  skus: HangTagSku[];
}) {
  const fallback = DEFAULT_TEMPLATES[stock];
  const [template, setTemplate] = useState<HangTagTemplate>(fallback);
  const sheet = SHEETS[stock];
  const tags = skus.slice(0, TAGS_PER_SHEET[stock]);

  useEffect(() => {
    const stored = parseStoredTemplate(
      window.localStorage.getItem(templateStorageKey(stock)) ??
        (stock === "5371" ? window.localStorage.getItem(STORAGE_KEY) : null),
      stock,
    );
    setTemplate(stored ?? fallback);
  }, [fallback, stock]);

  return (
    <section
      className={`sheet-${stock} sheet-from-json`}
      aria-label={`${sheet.name} sheet`}
    >
      {tags.map((sku, index) => (
        <TemplateTag
          key={`${sku.item_number}-${index}`}
          sku={sku}
          template={template}
        />
      ))}
    </section>
  );
}
