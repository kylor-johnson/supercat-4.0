import data from "@/data/kuzco-fixture.json";
import { TemplateSheet } from "@/components/template-sheet";
import { SheetChrome } from "@/components/sheet-chrome";
import type { HangTagSku } from "@/data/sku";

const skus = data as HangTagSku[];

export default function Home() {
  return (
    <main className="hang-tag-page">
      <SheetChrome sheet="5371" />
      <TemplateSheet stock="5371" skus={skus.slice(0, 10)} />
    </main>
  );
}
