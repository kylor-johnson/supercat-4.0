"use client";

import { HangTagSizzle } from "@/components/hang-tag-sizzle";
import { TemplateTag } from "@/components/template-tag";
import { SHEETS, type SheetCode } from "@/data/sheets";
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
  const letter = sheet.kind === "avery-letter";

  return (
    <section
      className={`sheet sheet-${stock} sheet-kind-${sheet.kind} sheet-from-json`}
      aria-label={`${sheet.name} · ${tags.length} tag${tags.length === 1 ? "" : "s"}`}
      style={{
        width: `${sheet.page.width}in`,
        height: letter ? `${sheet.page.height}in` : undefined,
        minHeight: letter ? undefined : `${sheet.page.height}in`,
        padding: `${sheet.pad.top}in ${sheet.pad.right}in ${sheet.pad.bottom}in ${sheet.pad.left}in`,
      }}
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

export function StockScreen({
  stock,
  skus,
}: {
  stock: SheetCode;
  skus: HangTagSku[];
}) {
  const template = useStoredTemplate(stock);
  const sheet = SHEETS[stock];
  const tags = sheetSkusFor(template, skus, stock);

  if (sheet.preview === "sizzle") {
    return (
      <>
        <div className="hang-tag-sizzle-list no-print">
          {tags.map((sku, index) => (
            <HangTagSizzle
              key={`${sku.item_number}-${index}`}
              sku={sku}
              template={template}
            />
          ))}
        </div>
        <div className="print-only">
          <TemplateSheet stock={stock} skus={skus} template={template} />
        </div>
      </>
    );
  }

  return <TemplateSheet stock={stock} skus={skus} template={template} />;
}

const SHEET_PREVIEW_SCALE = 0.42;
const TAG_PREVIEW_SCALE = 0.72;

export function MiniSheet({
  stock,
  skus,
  template,
}: {
  stock: SheetCode;
  skus: HangTagSku[];
  template: HangTagTemplate;
}) {
  const sheet = SHEETS[stock];
  if (sheet.kind === "one-up") {
    const sku = sheetSkusFor(template, skus, stock)[0];
    if (!sku) return null;
    return (
      <div
        className="designer-sheet-frame"
        style={{
          width: `calc(${template.tag.width}in * ${TAG_PREVIEW_SCALE})`,
          height: `calc(${template.tag.height}in * ${TAG_PREVIEW_SCALE})`,
        }}
      >
        <div
          className="designer-sheet-scale designer-sheet-scale-tag"
          style={{
            width: `${template.tag.width}in`,
            height: `${template.tag.height}in`,
            transform: `scale(${TAG_PREVIEW_SCALE})`,
          }}
        >
          <TemplateTag sku={sku} template={template} />
        </div>
      </div>
    );
  }

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
