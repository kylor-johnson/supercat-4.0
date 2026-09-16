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
  letterSpacing?: string;
  textTransform?: "none" | "uppercase";
};

export type HangTagTemplate = {
  version: typeof TEMPLATE_VERSION;
  name: string;
  stock: "5371";
  tag: { width: number; height: number };
  objects: TemplateObject[];
};

export const KUZCO_5371_TEMPLATE: HangTagTemplate = {
  version: TEMPLATE_VERSION,
  name: "Kuzco 5371 showroom",
  stock: "5371",
  tag: { width: 3.5, height: 2 },
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

export function inchesToPx(value: number): number {
  return value * EDITOR_DPI;
}

export function pxToInches(value: number): number {
  return Math.round((value / EDITOR_DPI) * 1000) / 1000;
}

export function cloneTemplate(template: HangTagTemplate): HangTagTemplate {
  return structuredClone(template);
}

export function parseStoredTemplate(raw: string | null): HangTagTemplate | null {
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw) as HangTagTemplate;
    if (parsed.version !== TEMPLATE_VERSION || parsed.stock !== "5371") return null;
    if (!Array.isArray(parsed.objects)) return null;
    return parsed;
  } catch {
    return null;
  }
}
