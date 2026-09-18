import data from "@/data/kuzco-fixture.json";
import { SheetChrome } from "@/components/sheet-chrome";
import { StockScreen } from "@/components/template-sheet";
import type { HangTagSku } from "@/data/sku";

const skus = data as HangTagSku[];

export default function Home() {
  return (
    <main className="hang-tag-page">
      <SheetChrome sheet="5371" />
      <StockScreen stock="5371" skus={skus} />
    </main>
  );
}
