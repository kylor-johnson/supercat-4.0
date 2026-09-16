import data from "@/data/kuzco-fixture.json";
import { HangTag } from "@/components/hang-tag";
import { SheetChrome } from "@/components/sheet-chrome";
import type { HangTagSku } from "@/data/sku";

const skus = data as HangTagSku[];
const sheet5371 = skus.slice(0, 10);

export default function Home() {
  return (
    <main className="hang-tag-page">
      <SheetChrome sheet="5371" />
      <section className="sheet-5371" aria-label="Avery 5371 sheet">
        {sheet5371.map((sku, index) => (
          <HangTag key={`${sku.item_number}-${index}`} sku={sku} layout="5371" />
        ))}
      </section>
    </main>
  );
}
