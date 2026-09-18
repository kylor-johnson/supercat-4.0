import type { HangTagSku } from "@/data/sku";
import type { BarcodeFormat } from "@/data/template";

const BARCODE_OPTIONS = {
  displayValue: true,
  fontSize: 11,
  height: 28,
  width: 1.35,
  margin: 8,
  marginTop: 2,
  marginBottom: 2,
  background: "#ffffff",
  lineColor: "#000000",
  font: "ui-monospace, SFMono-Regular, Menlo, monospace",
} as const;

export function scanValue(sku: HangTagSku): string {
  const digits = sku.upc_value.replace(/\D/g, "");
  return digits || sku.item_number;
}

function svgDataUrl(svg: string): string {
  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
}

async function barcodeDataUrl(
  value: string,
  format: "upc" | "CODE128",
): Promise<string> {
  const JsBarcode = (await import("jsbarcode")).default;
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  JsBarcode(svg, value, {
    ...BARCODE_OPTIONS,
    format,
    margin: format === "upc" ? 12 : 8,
  });
  return svgDataUrl(new XMLSerializer().serializeToString(svg));
}

async function qrDataUrl(value: string): Promise<string> {
  const QRCode = (await import("qrcode")).default;
  const svg = await QRCode.toString(value, {
    type: "svg",
    width: 256,
    margin: 1,
    errorCorrectionLevel: "M",
    color: { dark: "#000000", light: "#ffffff" },
  });
  return svgDataUrl(svg);
}

async function upcDataUrl(value: string): Promise<string> {
  const digits = value.replace(/\D/g, "");
  try {
    if (digits.length === 11 || digits.length === 12) {
      return await barcodeDataUrl(digits, "upc");
    }
  } catch {
    // Invalid check digit or length — still print something.
  }
  return barcodeDataUrl(value, "CODE128");
}

export async function codeImageSrc(
  format: BarcodeFormat,
  sku: HangTagSku,
): Promise<string> {
  const value = scanValue(sku);
  if (!value) return "";
  if (format === "qr") return qrDataUrl(value);
  if (format === "upc") return upcDataUrl(value);
  return barcodeDataUrl(value, "CODE128");
}
