export type SheetCode = "5371" | "5392";

export type SheetSpec = {
  code: SheetCode;
  name: string;
  size: string;
  grid: string;
  href: string;
  pdfHref: string;
  pdfFile: string;
};

export const SHEETS: Record<SheetCode, SheetSpec> = {
  "5371": {
    code: "5371",
    name: "Avery 5371",
    size: "3.5×2 in",
    grid: "2×5",
    href: "/",
    pdfHref: "/reviews/kuzco-5371-sheet.pdf",
    pdfFile: "kuzco-5371-sheet.pdf",
  },
  "5392": {
    code: "5392",
    name: "Avery 5392",
    size: "4×3 in",
    grid: "2×3",
    href: "/5392",
    pdfHref: "/reviews/kuzco-5392-sheet.pdf",
    pdfFile: "kuzco-5392-sheet.pdf",
  },
};
