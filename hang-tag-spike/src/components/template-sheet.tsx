"use client";

import { TemplateTag } from "@/components/template-tag";
import { SHEETS, type SheetCode } from "@/data/sheets";
import type { HangTagSku } from "@/data/sku";
import { useStoredTemplate } from "@/lib/use-stored-template";

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
  const template = useStoredTemplate(stock);
  const sheet = SHEETS[stock];
  const tags = skus.slice(0, TAGS_PER_SHEET[stock]);

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
