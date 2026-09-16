import data from "@/data/kuzco-fixture.json";
import { TagDesigner } from "@/components/tag-designer";
import { SheetChrome } from "@/components/sheet-chrome";
import type { HangTagSku } from "@/data/sku";

const skus = data as HangTagSku[];

export const metadata = {
  title: "Hang tags — designer",
  description: "Drag-and-drop hang tag template for Kuzco Avery 5371",
};

export default function DesignPage() {
  return (
    <main className="hang-tag-page">
      <SheetChrome sheet="5371" designer />
      <TagDesigner skus={skus} />
    </main>
  );
}
