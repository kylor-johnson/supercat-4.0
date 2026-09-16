import data from "@/data/kuzco-fixture.json";
import { TagDesigner } from "@/components/tag-designer";
import { SheetChrome } from "@/components/sheet-chrome";
import type { HangTagSku } from "@/data/sku";
import type { SheetCode } from "@/data/sheets";

const skus = data as HangTagSku[];

export const metadata = {
  title: "Hang tags — designer",
  description: "Drag-and-drop hang tag template for Kuzco Avery letter stock",
};

function parseStock(value: string | string[] | undefined): SheetCode {
  const raw = Array.isArray(value) ? value[0] : value;
  return raw === "5392" ? "5392" : "5371";
}

export default async function DesignPage({
  searchParams,
}: {
  searchParams: Promise<{ stock?: string | string[] }>;
}) {
  const stock = parseStock((await searchParams).stock);

  return (
    <main className="hang-tag-page">
      <SheetChrome sheet={stock} designer />
      <TagDesigner key={stock} skus={skus} stock={stock} />
    </main>
  );
}
