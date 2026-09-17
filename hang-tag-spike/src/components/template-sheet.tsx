"use client";

import { TemplateTag } from "@/components/template-tag";
import { SHEETS, TAGS_PER_SHEET, type SheetCode } from "@/data/sheets";
import type { HangTagSku } from "@/data/sku";
import type { HangTagTemplate } from "@/data/template";
import { sheetSkusFor } from "@/lib/sheet-skus";
import { useStoredTemplate } from "@/lib/use-stored-template";

export function TemplateSheet({
  stock,
  skus,
  template: override,
}: {
  stock: SheetCode;
  skus: HangTagSku[];
  template?: HangTagTemplate;
}) {
  const stored = useStoredTemplate(stock);
  const template = override ?? stored;
  const sheet = SHEETS[stock];
  const tags = sheetSkusFor(template, skus, stock);

  return (
    <section
      className={`sheet-${stock} sheet-from-json`}
      aria-label={`${sheet.name} sheet · ${TAGS_PER_SHEET[stock]} tags`}
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

const SHEET_PREVIEW_SCALE = 0.42;

export function MiniSheet({
  stock,
  skus,
  template,
}: {
  stock: SheetCode;
  skus: HangTagSku[];
  template: HangTagTemplate;
}) {
  return (
    <div
      className="designer-sheet-frame"
      style={{
        width: `calc(8.5in * ${SHEET_PREVIEW_SCALE})`,
        height: `calc(11in * ${SHEET_PREVIEW_SCALE})`,
      }}
    >
      <div
        className="designer-sheet-scale"
        style={{ transform: `scale(${SHEET_PREVIEW_SCALE})` }}
      >
        <TemplateSheet stock={stock} skus={skus} template={template} />
      </div>
    </div>
  );
}
