import type { HangTagSku } from "@/data/sku";
import type { BarcodeFormat } from "@/data/template";

export function scanValue(sku: HangTagSku): string {
  const digits = sku.upc_value.replace(/\D/g, "");
  return digits || sku.item_number;
}

export function upcFixtureSrc(sku: HangTagSku): string {
  const digits = sku.upc_value.replace(/\D/g, "");
  return digits ? `/fixtures/barcodes/${digits}.svg` : "";
}

function svgDataUrl(svg: string): string {
  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
}

async function code128DataUrl(value: string): Promise<string> {
  const JsBarcode = (await import("jsbarcode")).default;
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  JsBarcode(svg, value, {
    format: "CODE128",
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

export async function codeImageSrc(
  format: BarcodeFormat,
  sku: HangTagSku,
): Promise<string> {
  if (format === "upc") return upcFixtureSrc(sku);
  const value = scanValue(sku);
  if (!value) return "";
  if (format === "qr") return qrDataUrl(value);
  return code128DataUrl(value);
}
