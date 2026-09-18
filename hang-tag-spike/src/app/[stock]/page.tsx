import { notFound } from "next/navigation";
import { SheetChrome } from "@/components/sheet-chrome";
import { StockScreen } from "@/components/template-sheet";
import { isSheetCode, SHEETS, SHEET_CODES } from "@/data/sheets";

export function generateStaticParams() {
  return SHEET_CODES.filter((code) => code !== "5371").map((stock) => ({
    stock,
  }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ stock: string }>;
}) {
  const { stock } = await params;
  if (!isSheetCode(stock)) return { title: "Hang tags — Kuzco" };
  const sheet = SHEETS[stock];
  return {
    title: `Hang tags — Kuzco ${sheet.shortLabel}`,
    description: `${sheet.name} hang tags for Kuzco Lighting`,
  };
}

export default async function StockPage({
  params,
}: {
  params: Promise<{ stock: string }>;
}) {
  const { stock } = await params;
  if (!isSheetCode(stock) || stock === "5371") notFound();

  return (
    <main className="hang-tag-page">
      <SheetChrome sheet={stock} />
      <StockScreen stock={stock} />
    </main>
  );
}
