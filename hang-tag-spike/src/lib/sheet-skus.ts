import { SHEETS, TAGS_PER_SHEET, type SheetCode } from "@/data/sheets";
import type { HangTagSku } from "@/data/sku";
import type { HangTagTemplate } from "@/data/template";

export { TAGS_PER_SHEET };

export function resolvedItemNumbers(
  template: HangTagTemplate,
  catalog: HangTagSku[],
): string[] {
  const known = new Set(catalog.map((sku) => sku.item_number));
  const unique = [
    ...new Set(
      (template.itemNumbers ?? []).filter((code) => known.has(code)),
    ),
  ];
  if (unique.length) return unique;
  return catalog.map((sku) => sku.item_number);
}

export function fillSheetSkus(
  itemNumbers: string[],
  catalog: HangTagSku[],
  slots: number,
): HangTagSku[] {
  const byCode = new Map(catalog.map((sku) => [sku.item_number, sku]));
  const selected = itemNumbers
    .map((code) => byCode.get(code))
    .filter((sku): sku is HangTagSku => Boolean(sku));
  const source = selected.length ? selected : catalog;
  if (!source.length || slots <= 0) return [];
  return Array.from(
    { length: slots },
    (_, index) => source[index % source.length],
  );
}

export function sheetSkusFor(
  template: HangTagTemplate,
  catalog: HangTagSku[],
  stock: SheetCode,
): HangTagSku[] {
  const spec = SHEETS[stock];
  const numbers = resolvedItemNumbers(template, catalog);
  if (spec.fill === "once") {
    const byCode = new Map(catalog.map((sku) => [sku.item_number, sku]));
    const selected = numbers
      .map((code) => byCode.get(code))
      .filter((sku): sku is HangTagSku => Boolean(sku));
    return selected.length ? selected : catalog.slice(0, 1);
  }
  return fillSheetSkus(numbers, catalog, spec.tagsPerSheet);
}
