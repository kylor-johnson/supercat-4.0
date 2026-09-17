import type { SheetCode } from "@/data/sheets";

export const TEMPLATE_VERSION = 1 as const;
export const STORAGE_KEY = "hang-tag-template-v1";
export const EDITOR_DPI = 192;

export type BindingKey =
  | "collection_name"
  | "item_number"
  | "finish"
  | "lamp_line"
  | "size_line"
  | "price_line"
  | "primary_image"
  | "logo"
  | "upc_image";

export type TemplateObjectType = "text" | "image" | "barcode";

export const FONT_FAMILIES = [
  "geist",
  "geist-mono",
  "arial",
  "georgia",
  "times",
  "courier",
] as const;

export type FontFamily = (typeof FONT_FAMILIES)[number];

export const FONT_LABELS: Record<FontFamily, string> = {
  geist: "Geist",
  "geist-mono": "Geist Mono",
  arial: "Arial",
  georgia: "Georgia",
  times: "Times New Roman",
  courier: "Courier New",
};

export const TEXT_ALIGNS = ["left", "center", "right"] as const;
export type TextAlign = (typeof TEXT_ALIGNS)[number];

export const BARCODE_FORMATS = ["upc", "code128", "qr"] as const;
export type BarcodeFormat = (typeof BARCODE_FORMATS)[number];

export const BARCODE_FORMAT_LABELS: Record<BarcodeFormat, string> = {
  upc: "UPC-A",
  code128: "Code 128",
  qr: "QR",
};

export const DEFAULT_FONT_FAMILY: FontFamily = "geist";
export const DEFAULT_TEXT_ALIGN: TextAlign = "left";
export const DEFAULT_BARCODE_FORMAT: BarcodeFormat = "upc";
export const DEFAULT_FONT_SIZE = 8;
export const DEFAULT_FONT_WEIGHT = 400;
export const NUDGE_INCHES = 0.01;
export const NUDGE_SHIFT_INCHES = 0.1;
export const SNAP_INCHES = 0.04;
export const HISTORY_LIMIT = 20;

export const LETTER_SPACING_OPTIONS = [
  { value: "", label: "None" },
  { value: "0.02em", label: "Tight" },
  { value: "0.04em", label: "Wide" },
  { value: "0.08em", label: "Extra" },
] as const;

export type TemplateObject = {
  id: string;
  type: TemplateObjectType;
  binding: BindingKey | null;
  text?: string;
  x: number;
  y: number;
  width: number;
  height: number;
  fontSize?: number;
  fontWeight?: number;
  fontFamily?: FontFamily;
  letterSpacing?: string;
  textTransform?: "none" | "uppercase";
  textAlign?: TextAlign;
  barcodeFormat?: BarcodeFormat;
};

export type HangTagTemplate = {
  version: typeof TEMPLATE_VERSION;
  name: string;
  stock: SheetCode;
  tag: { width: number; height: number };
  fontFamily?: FontFamily;
  barcodeFormat?: BarcodeFormat;
  objects: TemplateObject[];
};

function isFontFamily(value: unknown): value is FontFamily {
  return (
    typeof value === "string" &&
    (FONT_FAMILIES as readonly string[]).includes(value)
  );
}

function isTextAlign(value: unknown): value is TextAlign {
  return (
    typeof value === "string" &&
    (TEXT_ALIGNS as readonly string[]).includes(value)
  );
}

function isBarcodeFormat(value: unknown): value is BarcodeFormat {
  return (
    typeof value === "string" &&
    (BARCODE_FORMATS as readonly string[]).includes(value)
  );
}

export function fontCssStack(family: FontFamily): string {
  switch (family) {
    case "geist":
      return "var(--font-geist-sans), system-ui, sans-serif";
    case "geist-mono":
      return "var(--font-geist-mono), ui-monospace, monospace";
    case "arial":
      return "Arial, Helvetica, sans-serif";
    case "georgia":
      return "Georgia, 'Times New Roman', serif";
    case "times":
      return "'Times New Roman', Times, serif";
    case "courier":
      return "'Courier New', Courier, monospace";
  }
}

export function fontCanvasStack(family: FontFamily): string {
  if (typeof document !== "undefined") {
    if (family === "geist") {
      const value = getComputedStyle(document.documentElement)
        .getPropertyValue("--font-geist-sans")
        .trim();
      if (value) return value;
    }
    if (family === "geist-mono") {
      const value = getComputedStyle(document.documentElement)
        .getPropertyValue("--font-geist-mono")
        .trim();
      if (value) return value;
    }
  }
  switch (family) {
    case "geist":
      return "Geist, system-ui, sans-serif";
    case "geist-mono":
      return "Geist Mono, ui-monospace, monospace";
    case "arial":
      return "Arial, Helvetica, sans-serif";
    case "georgia":
      return "Georgia, Times New Roman, serif";
    case "times":
      return "Times New Roman, Times, serif";
    case "courier":
      return "Courier New, Courier, monospace";
  }
}

export function resolvedFontFamily(
  template: HangTagTemplate,
  spec: TemplateObject,
): FontFamily {
  if (spec.fontFamily) return spec.fontFamily;
  if (template.fontFamily) return template.fontFamily;
  return spec.binding === "item_number" ? "geist-mono" : DEFAULT_FONT_FAMILY;
}

export function resolvedTextAlign(spec: TemplateObject): TextAlign {
  return spec.textAlign ?? DEFAULT_TEXT_ALIGN;
}

export function resolvedFontSize(spec: TemplateObject): number {
  return spec.fontSize ?? DEFAULT_FONT_SIZE;
}

export function resolvedFontWeight(spec: TemplateObject): number {
  return spec.fontWeight ?? DEFAULT_FONT_WEIGHT;
}

export function emToCharSpacing(value?: string): number {
  if (!value) return 0;
  const match = value.trim().match(/^(-?[\d.]+)em$/i);
  if (!match) return 0;
  return Math.round(Number(match[1]) * 1000);
}

export function resolvedBarcodeFormat(
  template: HangTagTemplate,
  spec: TemplateObject,
): BarcodeFormat {
  if (spec.barcodeFormat) return spec.barcodeFormat;
  if (template.barcodeFormat) return template.barcodeFormat;
  return DEFAULT_BARCODE_FORMAT;
}

export const KUZCO_5371_TEMPLATE: HangTagTemplate = {
  version: TEMPLATE_VERSION,
  name: "Kuzco 5371 showroom",
  stock: "5371",
  tag: { width: 3.5, height: 2 },
  fontFamily: "geist",
  barcodeFormat: "upc",
  objects: [
    {
      id: "photo",
      type: "image",
      binding: "primary_image",
      x: 0.1,
      y: 0.08,
      width: 0.72,
      height: 0.72,
    },
    {
      id: "logo",
      type: "image",
      binding: "logo",
      x: 0.9,
      y: 0.08,
      width: 1.55,
      height: 0.2,
    },
    {
      id: "collection",
      type: "text",
      binding: "collection_name",
      x: 0.9,
      y: 0.3,
      width: 2.4,
      height: 0.18,
      fontSize: 8.5,
      fontWeight: 700,
      letterSpacing: "0.04em",
      textTransform: "uppercase",
    },
    {
      id: "sku",
      type: "text",
      binding: "item_number",
      x: 0.9,
      y: 0.48,
      width: 2.4,
      height: 0.16,
      fontSize: 7.5,
      fontFamily: "geist-mono",
    },
    {
      id: "finish",
      type: "text",
      binding: "finish",
      x: 0.9,
      y: 0.64,
      width: 2.4,
      height: 0.14,
      fontSize: 8,
    },
    {
      id: "lamp",
      type: "text",
      binding: "lamp_line",
      x: 0.9,
      y: 0.78,
      width: 2.4,
      height: 0.14,
      fontSize: 8,
    },
    {
      id: "size",
      type: "text",
      binding: "size_line",
      x: 0.9,
      y: 0.92,
      width: 2.4,
      height: 0.14,
      fontSize: 8,
    },
    {
      id: "price",
      type: "text",
      binding: "price_line",
      x: 0.9,
      y: 1.08,
      width: 2.4,
      height: 0.28,
      fontSize: 8,
      fontWeight: 700,
    },
    {
      id: "barcode",
      type: "barcode",
      binding: "upc_image",
      x: 0.18,
      y: 1.48,
      width: 3.14,
      height: 0.42,
    },
  ],
};

export const KUZCO_5392_TEMPLATE: HangTagTemplate = {
  version: TEMPLATE_VERSION,
  name: "Kuzco 5392 showroom",
  stock: "5392",
  tag: { width: 4, height: 3 },
  fontFamily: "geist",
  barcodeFormat: "upc",
  objects: [
    {
      id: "photo",
      type: "image",
      binding: "primary_image",
      x: 0.14,
      y: 0.12,
      width: 1.15,
      height: 1.15,
    },
    {
      id: "logo",
      type: "image",
      binding: "logo",
      x: 1.41,
      y: 0.12,
      width: 2.0,
      height: 0.28,
    },
    {
      id: "collection",
      type: "text",
      binding: "collection_name",
      x: 1.41,
      y: 0.44,
      width: 2.45,
      height: 0.22,
      fontSize: 11,
      fontWeight: 700,
      letterSpacing: "0.04em",
      textTransform: "uppercase",
    },
    {
      id: "sku",
      type: "text",
      binding: "item_number",
      x: 1.41,
      y: 0.68,
      width: 2.45,
      height: 0.18,
      fontSize: 8.5,
      fontFamily: "geist-mono",
    },
    {
      id: "finish",
      type: "text",
      binding: "finish",
      x: 1.41,
      y: 0.9,
      width: 2.45,
      height: 0.18,
      fontSize: 9.5,
    },
    {
      id: "lamp",
      type: "text",
      binding: "lamp_line",
      x: 1.41,
      y: 1.1,
      width: 2.45,
      height: 0.18,
      fontSize: 9.5,
    },
    {
      id: "size",
      type: "text",
      binding: "size_line",
      x: 1.41,
      y: 1.3,
      width: 2.45,
      height: 0.18,
      fontSize: 9.5,
    },
    {
      id: "price",
      type: "text",
      binding: "price_line",
      x: 1.41,
      y: 1.52,
      width: 2.45,
      height: 0.36,
      fontSize: 9.5,
      fontWeight: 700,
    },
    {
      id: "barcode",
      type: "barcode",
      binding: "upc_image",
      x: 0.24,
      y: 2.4,
      width: 3.52,
      height: 0.52,
    },
  ],
};

export const DEFAULT_TEMPLATES: Record<SheetCode, HangTagTemplate> = {
  "5371": KUZCO_5371_TEMPLATE,
  "5392": KUZCO_5392_TEMPLATE,
};

export function templateStorageKey(stock: SheetCode): string {
  return `${STORAGE_KEY}-${stock}`;
}

export function inchesToPx(value: number): number {
  return value * EDITOR_DPI;
}

export function pxToInches(value: number): number {
  return Math.round((value / EDITOR_DPI) * 1000) / 1000;
}

export function cloneTemplate(template: HangTagTemplate): HangTagTemplate {
  return structuredClone(template);
}

export function parseStoredTemplate(
  raw: string | null,
  stock?: SheetCode,
): HangTagTemplate | null {
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw) as HangTagTemplate;
    if (parsed.version !== TEMPLATE_VERSION) return null;
    if (parsed.stock !== "5371" && parsed.stock !== "5392") return null;
    if (stock && parsed.stock !== stock) return null;
    if (!Array.isArray(parsed.objects)) return null;
    return {
      ...parsed,
      fontFamily: isFontFamily(parsed.fontFamily)
        ? parsed.fontFamily
        : undefined,
      barcodeFormat: isBarcodeFormat(parsed.barcodeFormat)
        ? parsed.barcodeFormat
        : undefined,
      objects: parsed.objects.map((object) => ({
        ...object,
        fontFamily: isFontFamily(object.fontFamily)
          ? object.fontFamily
          : undefined,
        textAlign: isTextAlign(object.textAlign) ? object.textAlign : undefined,
        barcodeFormat: isBarcodeFormat(object.barcodeFormat)
          ? object.barcodeFormat
          : undefined,
      })),
    };
  } catch {
    return null;
  }
}
