import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { DOMImplementation, XMLSerializer } from "@xmldom/xmldom";
import JsBarcode from "jsbarcode";
import fixture from "../src/data/kuzco-fixture.json" with { type: "json" };

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const outDir = join(root, "public/fixtures/barcodes");
mkdirSync(outDir, { recursive: true });

const document = new DOMImplementation().createDocument(
  "http://www.w3.org/1999/xhtml",
  "html",
  null,
);
const serializer = new XMLSerializer();

const upcs = [...new Set(fixture.map((sku) => sku.upc_value.replace(/\D/g, "")))];

for (const upc of upcs) {
  const svgNode = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  JsBarcode(svgNode, upc, {
    xmlDocument: document,
    format: "upc",
    displayValue: true,
    fontSize: 11,
    height: 28,
    width: 1.35,
    margin: 12,
    marginTop: 2,
    marginBottom: 2,
    background: "#ffffff",
    lineColor: "#000000",
    font: "ui-monospace, SFMono-Regular, Menlo, monospace",
  });
  const svg = serializer.serializeToString(svgNode);
  writeFileSync(join(outDir, `${upc}.svg`), svg);
  console.log(`wrote ${upc}.svg`);
}
