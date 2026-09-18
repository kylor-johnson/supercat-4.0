import { SheetChrome } from "@/components/sheet-chrome";
import { StockScreen } from "@/components/template-sheet";

export default function Home() {
  return (
    <main id="main" className="hang-tag-page">
      <SheetChrome sheet="5371" />
      <StockScreen stock="5371" />
    </main>
  );
}
