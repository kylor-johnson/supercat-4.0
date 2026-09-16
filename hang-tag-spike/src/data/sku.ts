export type HangTagSku = {
  item_number: string;
  collection_name: string;
  FinishOptions: string;
  LampType: string;
  Voltage: string;
  ColorTemperature: string;
  Wattage: string;
  Lumens: string;
  product_dimensions_in: string;
  us_imap: string;
  cad_imap: string;
  upc_value: string;
  image: string;
};

export const KUZCO_LOGO = "/fixtures/kuzco-logo.png";

function shortenFinishPart(part: string): string {
  const slash = part.indexOf("/");
  if (slash > 0 && part.length > 14) {
    return part.slice(0, slash).trim();
  }
  return part;
}

export function formatFinish(raw: string, compact = false): string {
  const parts = raw
    .split("|")
    .map((part) => part.trim())
    .filter(Boolean);
  if (!compact) return parts.join(" / ");
  const shortened = parts.map(shortenFinishPart);
  if (shortened.length > 2) {
    return `${shortened.slice(0, 2).join(" / ")} …`;
  }
  return shortened.join(" / ");
}

export function formatLamp(raw: string, compact: boolean): string {
  const value = raw.trim();
  if (!compact) return value;
  const comma = value.lastIndexOf(",");
  if (comma > 0) return value.slice(comma + 1).trim();
  return value;
}

export function formatDimensions(raw: string, compact: boolean): string {
  const value = raw.trim();
  if (!compact) return value;
  const labeled = value.match(
    /^(\S+)\s+[LWDH]\s+x\s+(\S+)\s+[LWDH]\s+x\s+(\S+)\s+[LWDHE]$/i,
  );
  if (labeled) return `${labeled[1]} × ${labeled[2]} × ${labeled[3]}`;
  return value.replaceAll(" x ", " × ");
}

export function formatImap(raw: string, currency: "usd" | "cad"): string {
  const amount = Number(raw);
  if (!Number.isFinite(amount)) return "";
  const formatted = amount.toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  return currency === "usd" ? `$${formatted}` : `C$${formatted}`;
}

export function formatCct(raw: string, compact: boolean): string {
  const value = raw.trim();
  if (!compact) return value;
  const match = value.match(/^(\d+CCT)/i);
  return match ? match[1] : value;
}

export function joinSpecs(parts: Array<string | undefined>): string {
  return parts
    .map((part) => part?.trim() ?? "")
    .filter(Boolean)
    .join(" · ");
}
