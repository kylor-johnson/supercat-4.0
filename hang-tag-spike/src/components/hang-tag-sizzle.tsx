import { TemplateTag } from "@/components/template-tag";
import type { HangTagSku } from "@/data/sku";
import type { HangTagTemplate } from "@/data/template";

export function HangTagSizzle({
  sku,
  template,
}: {
  sku: HangTagSku;
  template: HangTagTemplate;
}) {
  return (
    <figure className="hang-tag-sizzle" aria-label={`${sku.item_number} hang-tag preview`}>
      <img className="hang-tag-sizzle-photo" src={sku.image} alt="" />
      <span className="hang-tag-sizzle-hook" aria-hidden />
      <div className="hang-tag-sizzle-tag">
        <TemplateTag sku={sku} template={template} />
        <span className="hang-tag-sizzle-ring" aria-hidden />
      </div>
      <figcaption className="hang-tag-sizzle-caption">
        {sku.collection_name} · {sku.item_number}
      </figcaption>
    </figure>
  );
}
