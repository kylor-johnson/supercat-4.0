import {
  formatCct,
  formatDimensions,
  formatFinish,
  formatImap,
  formatLamp,
  joinSpecs,
  KUZCO_LOGO,
  type HangTagSku,
} from "@/data/sku";
import type { BindingKey } from "@/data/template";

export function boundText(sku: HangTagSku, binding: BindingKey): string {
  const compact = true;
  switch (binding) {
    case "collection_name":
      return sku.collection_name;
    case "item_number":
      return sku.item_number;
    case "finish":
      return formatFinish(sku.FinishOptions, compact);
    case "lamp_line":
      return joinSpecs([
        formatLamp(sku.LampType, compact),
        sku.Voltage,
        formatCct(sku.ColorTemperature, compact),
        sku.Wattage,
      ]);
    case "size_line":
      return joinSpecs([
        sku.Lumens,
        formatDimensions(sku.product_dimensions_in, compact),
      ]);
    case "price_line": {
      const us = formatImap(sku.us_imap, "usd");
      const cad = formatImap(sku.cad_imap, "cad");
      return joinSpecs([
        us ? `${us} US IMAP` : "",
        cad ? `${cad} CAD IMAP` : "",
      ]);
    }
    default:
      return "";
  }
}

export function boundImageSrc(sku: HangTagSku, binding: BindingKey): string {
  switch (binding) {
    case "primary_image":
      return sku.image;
    case "logo":
      return KUZCO_LOGO;
    case "upc_image": {
      const digits = sku.upc_value.replace(/\D/g, "");
      return `/fixtures/barcodes/${digits}.svg`;
    }
    default:
      return "";
  }
}
