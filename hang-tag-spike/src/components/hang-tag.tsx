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
import { UpcBarcode } from "@/components/upc-barcode";
import type { SheetCode } from "@/data/sheets";

export function HangTag({
  sku,
  layout,
}: {
  sku: HangTagSku;
  layout: SheetCode;
}) {
  const compact = layout === "5371";
  const finish = formatFinish(sku.FinishOptions, compact);
  const cct = sku.ColorTemperature.trim();
  const cctIsLong = !compact && cct.length > 18;
  const lampLine = joinSpecs([
    formatLamp(sku.LampType, compact),
    sku.Voltage,
    compact ? formatCct(cct, true) : cctIsLong ? "" : cct,
    sku.Wattage,
  ]);
  const cctLine = cctIsLong ? cct.replaceAll("/", " / ") : "";
  const sizeLine = joinSpecs([
    sku.Lumens,
    formatDimensions(sku.product_dimensions_in, compact),
  ]);
  const usImap = formatImap(sku.us_imap, "usd");
  const cadImap = formatImap(sku.cad_imap, "cad");

  return (
    <article className={`hang-tag hang-tag-${layout}`}>
      <img
        className="hang-tag-photo"
        src={sku.image}
        alt=""
        width={150}
        height={150}
      />
      <div className="hang-tag-body">
        <img
          className="hang-tag-logo"
          src={KUZCO_LOGO}
          alt="Kuzco Lighting"
          width={180}
          height={60}
        />
        <div className="hang-tag-collection">{sku.collection_name}</div>
        <div className="hang-tag-sku">{sku.item_number}</div>
        {finish ? <div className="hang-tag-line">{finish}</div> : null}
        {lampLine ? <div className="hang-tag-line">{lampLine}</div> : null}
        {cctLine ? <div className="hang-tag-cct">{cctLine}</div> : null}
        {sizeLine ? <div className="hang-tag-line">{sizeLine}</div> : null}
        <div className="hang-tag-price">
          {usImap ? <span>{`${usImap} US IMAP`}</span> : null}
          {cadImap ? <span>{`${cadImap} CAD IMAP`}</span> : null}
        </div>
      </div>
      <div className="hang-tag-barcode">
        <UpcBarcode value={sku.upc_value} />
      </div>
    </article>
  );
}
