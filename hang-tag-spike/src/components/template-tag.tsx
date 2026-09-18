import type { CSSProperties } from "react";
import { BarcodeMark } from "@/components/barcode-mark";
import { boundImageSrc, boundText } from "@/data/bindings";
import type { HangTagSku } from "@/data/sku";
import {
  fontCssStack,
  objectVisible,
  resolvedBarcodeFormat,
  resolvedFontFamily,
  resolvedTextAlign,
  type HangTagTemplate,
  type TemplateObject,
} from "@/data/template";

function objectStyle(
  spec: TemplateObject,
  template: HangTagTemplate,
): CSSProperties {
  const wrapPrice = spec.binding === "price_line";
  const fontFamily = resolvedFontFamily(template, spec);
  return {
    position: "absolute",
    left: `${spec.x}in`,
    top: `${spec.y}in`,
    width: `${spec.width}in`,
    height: `${spec.height}in`,
    fontSize: spec.fontSize ? `${spec.fontSize}pt` : undefined,
    fontWeight: spec.fontWeight,
    fontFamily: fontCssStack(fontFamily),
    letterSpacing: spec.letterSpacing,
    textTransform: spec.textTransform,
    textAlign: spec.type === "text" ? resolvedTextAlign(spec) : undefined,
    overflow: "hidden",
    lineHeight: 1.15,
    whiteSpace: wrapPrice ? "normal" : "nowrap",
  };
}

function TemplateObjectView({
  spec,
  sku,
  template,
}: {
  spec: TemplateObject;
  sku: HangTagSku;
  template: HangTagTemplate;
}) {
  const style = objectStyle(spec, template);

  if (spec.type === "text") {
    const text =
      (spec.binding ? boundText(sku, spec.binding) : spec.text) || "";
    if (!text) return null;
    return (
      <div className="template-tag-object" style={style}>
        {text}
      </div>
    );
  }

  if (spec.type === "barcode") {
    return (
      <BarcodeMark
        key={`${sku.item_number}-${resolvedBarcodeFormat(template, spec)}`}
        sku={sku}
        format={resolvedBarcodeFormat(template, spec)}
        className="template-tag-object template-tag-barcode"
        style={style}
      />
    );
  }

  const src = spec.binding ? boundImageSrc(sku, spec.binding) : "";
  if (!src) return null;
  return (
    <img
      className="template-tag-object template-tag-image"
      style={style}
      src={src}
      alt=""
    />
  );
}

export function TemplateTag({
  sku,
  template,
}: {
  sku: HangTagSku;
  template: HangTagTemplate;
}) {
  return (
    <article
      className={`template-tag template-tag-${template.stock}`}
      style={{
        width: `${template.tag.width}in`,
        height: `${template.tag.height}in`,
      }}
    >
      {template.objects
        .filter((spec) => objectVisible(spec, sku))
        .map((spec) => (
          <TemplateObjectView
            key={spec.id}
            spec={spec}
            sku={sku}
            template={template}
          />
        ))}
    </article>
  );
}
