import type { CSSProperties } from "react";
import { boundImageSrc, boundText } from "@/data/bindings";
import type { HangTagSku } from "@/data/sku";
import type { HangTagTemplate, TemplateObject } from "@/data/template";

function objectStyle(spec: TemplateObject): CSSProperties {
  const wrapPrice = spec.binding === "price_line";
  return {
    position: "absolute",
    left: `${spec.x}in`,
    top: `${spec.y}in`,
    width: `${spec.width}in`,
    height: `${spec.height}in`,
    fontSize: spec.fontSize ? `${spec.fontSize}pt` : undefined,
    fontWeight: spec.fontWeight,
    letterSpacing: spec.letterSpacing,
    textTransform: spec.textTransform,
    fontFamily:
      spec.binding === "item_number"
        ? "var(--font-mono), ui-monospace, monospace"
        : undefined,
    overflow: "hidden",
    lineHeight: 1.15,
    whiteSpace: wrapPrice ? "normal" : "nowrap",
  };
}

function TemplateObjectView({
  spec,
  sku,
}: {
  spec: TemplateObject;
  sku: HangTagSku;
}) {
  if (spec.type === "text") {
    const text =
      (spec.binding ? boundText(sku, spec.binding) : spec.text) || "";
    if (!text) return null;
    return (
      <div className="template-tag-object" style={objectStyle(spec)}>
        {text}
      </div>
    );
  }

  const src = spec.binding ? boundImageSrc(sku, spec.binding) : "";
  if (!src) return null;
  return (
    <img
      className={
        spec.type === "barcode"
          ? "template-tag-object template-tag-barcode"
          : "template-tag-object template-tag-image"
      }
      style={objectStyle(spec)}
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
      {template.objects.map((spec) => (
        <TemplateObjectView key={spec.id} spec={spec} sku={sku} />
      ))}
    </article>
  );
}
