import data from "@/data/kuzco-fixture.json";
import { TemplateSheet } from "@/components/template-sheet";
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
      <TemplateSheet stock="5392" skus={skus.slice(0, 6)} />
    </main>
  );
}
