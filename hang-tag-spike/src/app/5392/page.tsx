import data from "@/data/kuzco-fixture.json";
import { HangTag } from "@/components/hang-tag";
import { SheetChrome } from "@/components/sheet-chrome";
import type { HangTagSku } from "@/data/sku";

const skus = data as HangTagSku[];

export const metadata = {
  title: "Hang tags — Kuzco 5392",
  description: "Avery 5392 showroom hang tags for Kuzco Lighting",
};

export default function Avery5392Page() {
  return (
    <main className="hang-tag-page">
      <SheetChrome sheet="5392" />
      <section className="sheet-5392" aria-label="Avery 5392 sheet">
        {skus.slice(0, 6).map((sku) => (
          <HangTag key={sku.item_number} sku={sku} layout="5392" />
        ))}
      </section>
    </main>
  );
}
