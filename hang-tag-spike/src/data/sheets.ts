export const SHEET_CODES = ["5371", "5392", "hangtag"] as const;
export type SheetCode = (typeof SHEET_CODES)[number];

export type SheetKind = "avery-letter" | "one-up";
export type SheetFill = "repeat" | "once";
export type SheetPreview = "sheet" | "sizzle";

export type SheetSpec = {
  code: SheetCode;
  name: string;
  shortLabel: string;
  size: string;
  grid: string;
  href: string;
  pdfHref?: string;
  pdfFile?: string;
  kind: SheetKind;
  fill: SheetFill;
  preview: SheetPreview;
  tagsPerSheet: number;
  page: { width: number; height: number };
  pad: { top: number; right: number; bottom: number; left: number };
};

export function isSheetCode(value: unknown): value is SheetCode {
  return (
    typeof value === "string" &&
    (SHEET_CODES as readonly string[]).includes(value)
  );
}

export function designerHref(stock: SheetCode): string {
  return stock === "5371" ? "/design" : `/design?stock=${encodeURIComponent(stock)}`;
}

export const SHEETS: Record<SheetCode, SheetSpec> = {
  "5371": {
    code: "5371",
    name: "Avery 5371",
    shortLabel: "5371",
    size: "3.5×2 in",
    grid: "2×5",
    href: "/",
    pdfHref: "/reviews/kuzco-5371-sheet.pdf",
    pdfFile: "kuzco-5371-sheet.pdf",
    kind: "avery-letter",
    fill: "repeat",
    preview: "sheet",
    tagsPerSheet: 10,
    page: { width: 8.5, height: 11 },
    pad: { top: 0.5, right: 0.75, bottom: 0.5, left: 0.75 },
  },
  "5392": {
    code: "5392",
    name: "Avery 5392",
    shortLabel: "5392",
    size: "4×3 in",
    grid: "2×3",
    href: "/5392",
    pdfHref: "/reviews/kuzco-5392-sheet.pdf",
    pdfFile: "kuzco-5392-sheet.pdf",
    kind: "avery-letter",
    fill: "repeat",
    preview: "sheet",
    tagsPerSheet: 6,
    page: { width: 8.5, height: 11 },
    pad: { top: 1, right: 0.25, bottom: 1, left: 0.25 },
  },
  hangtag: {
    code: "hangtag",
    name: "Hang tag 2×3.5",
    shortLabel: "2×3.5",
    size: "2×3.5 in",
    grid: "1-up",
    href: "/hangtag",
    kind: "one-up",
    fill: "once",
    preview: "sizzle",
    tagsPerSheet: 1,
    page: { width: 8.5, height: 11 },
    pad: { top: 3.75, right: 3.25, bottom: 3.75, left: 3.25 },
  },
};

export const TAGS_PER_SHEET: Record<SheetCode, number> = {
  "5371": SHEETS["5371"].tagsPerSheet,
  "5392": SHEETS["5392"].tagsPerSheet,
  hangtag: SHEETS.hangtag.tagsPerSheet,
};
