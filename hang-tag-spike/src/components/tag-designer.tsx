"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { HangTagSku } from "@/data/sku";
import { boundImageSrc, boundText } from "@/data/bindings";
import {
  cloneTemplate,
  EDITOR_DPI,
  inchesToPx,
  KUZCO_5371_TEMPLATE,
  parseStoredTemplate,
  pxToInches,
  STORAGE_KEY,
  type HangTagTemplate,
  type TemplateObject,
} from "@/data/template";

type FabricModule = typeof import("fabric");
type FabricCanvas = import("fabric").Canvas;

function ptToPx(points: number): number {
  return (points * EDITOR_DPI) / 72;
}

function applyObjectTransform(
  object: import("fabric").FabricObject,
  spec: TemplateObject,
) {
  object.set({
    originX: "left",
    originY: "top",
    left: inchesToPx(spec.x),
    top: inchesToPx(spec.y),
    selectable: true,
    lockRotation: true,
  });
  object.setControlsVisibility({ mtr: false });
}

async function addTemplateObject(
  fabric: FabricModule,
  canvas: FabricCanvas,
  spec: TemplateObject,
  sku: HangTagSku,
) {
  const { FabricImage, Textbox } = fabric;
  const common = { templateId: spec.id } as const;

  if (spec.type === "text") {
    const text =
      (spec.binding ? boundText(sku, spec.binding) : spec.text) || "";
    const box = new Textbox(text, {
      width: inchesToPx(spec.width),
      fontSize: ptToPx(spec.fontSize ?? 8),
      fontWeight: spec.fontWeight ?? 400,
      fontFamily:
        spec.id === "sku"
          ? "ui-monospace, SFMono-Regular, Menlo, monospace"
          : "system-ui, sans-serif",
      fill: "#1a1714",
      splitByGrapheme: false,
      originX: "left",
      originY: "top",
    });
    if (spec.textTransform === "uppercase") {
      box.set("text", text.toUpperCase());
    }
    applyObjectTransform(box, spec);
    box.set(common);
    canvas.add(box);
    return;
  }

  const src = spec.binding ? boundImageSrc(sku, spec.binding) : "";
  if (!src) return;
  const image = await FabricImage.fromURL(src);
  const naturalW = image.width || 1;
  const naturalH = image.height || 1;
  const boxW = inchesToPx(spec.width);
  const boxH = inchesToPx(spec.height);
  const scale = Math.min(boxW / naturalW, boxH / naturalH);
  image.set({
    originX: "left",
    originY: "top",
    scaleX: scale,
    scaleY: scale,
    objectCaching: false,
  });
  applyObjectTransform(image, spec);
  image.set(common);
  canvas.add(image);
}

function templateFromCanvas(
  canvas: FabricCanvas,
  current: HangTagTemplate,
): HangTagTemplate {
  const next = cloneTemplate(current);
  for (const object of canvas.getObjects()) {
    const id = object.get("templateId") as string | undefined;
    if (!id) continue;
    const spec = next.objects.find((item) => item.id === id);
    if (!spec) continue;
    spec.x = pxToInches(object.left ?? 0);
    spec.y = pxToInches(object.top ?? 0);
    spec.width = pxToInches(object.getScaledWidth());
    spec.height = pxToInches(object.getScaledHeight());
  }
  return next;
}

export function TagDesigner({ skus }: { skus: HangTagSku[] }) {
  const hostRef = useRef<HTMLCanvasElement | null>(null);
  const fabricRef = useRef<FabricModule | null>(null);
  const canvasRef = useRef<FabricCanvas | null>(null);
  const templateRef = useRef<HangTagTemplate>(cloneTemplate(KUZCO_5371_TEMPLATE));
  const skuRef = useRef<HangTagSku>(skus[0]);
  const [skuIndex, setSkuIndex] = useState(0);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [ready, setReady] = useState(false);

  const persist = useCallback((template: HangTagTemplate) => {
    templateRef.current = template;
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(template));
  }, []);

  const rebuild = useCallback(async () => {
    const fabric = fabricRef.current;
    const canvas = canvasRef.current;
    if (!fabric || !canvas) return;
    canvas.clear();
    canvas.backgroundColor = "#ffffff";
    for (const spec of templateRef.current.objects) {
      await addTemplateObject(fabric, canvas, spec, skuRef.current);
    }
    canvas.requestRenderAll();
  }, []);

  useEffect(() => {
    let disposed = false;
    const canvasEl = hostRef.current;
    if (!canvasEl) return;

    const stored = parseStoredTemplate(window.localStorage.getItem(STORAGE_KEY));
    if (stored) templateRef.current = stored;

    import("fabric").then(async (fabric) => {
      if (disposed || !hostRef.current) return;
      fabricRef.current = fabric;
      const width = inchesToPx(templateRef.current.tag.width);
      const height = inchesToPx(templateRef.current.tag.height);
      const canvas = new fabric.Canvas(hostRef.current, {
        width,
        height,
        selection: true,
        preserveObjectStacking: true,
        backgroundColor: "#ffffff",
      });
      canvasRef.current = canvas;
      canvas.on("object:modified", () => {
        persist(templateFromCanvas(canvas, templateRef.current));
      });
      canvas.on("selection:created", (event) => {
        const id = event.selected?.[0]?.get("templateId") as string | undefined;
        setSelectedId(id ?? null);
      });
      canvas.on("selection:updated", (event) => {
        const id = event.selected?.[0]?.get("templateId") as string | undefined;
        setSelectedId(id ?? null);
      });
      canvas.on("selection:cleared", () => setSelectedId(null));
      await rebuild();
      setReady(true);
    });

    return () => {
      disposed = true;
      canvasRef.current?.dispose();
      canvasRef.current = null;
    };
  }, [persist, rebuild]);

  useEffect(() => {
    skuRef.current = skus[skuIndex] ?? skus[0];
    if (ready) void rebuild();
  }, [skuIndex, skus, ready, rebuild]);

  function resetLayout() {
    persist(cloneTemplate(KUZCO_5371_TEMPLATE));
    void rebuild();
  }

  function downloadJson() {
    const blob = new Blob([JSON.stringify(templateRef.current, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "kuzco-5371-template.json";
    link.click();
    URL.revokeObjectURL(url);
  }

  const sku = skus[skuIndex] ?? skus[0];
  const width = inchesToPx(KUZCO_5371_TEMPLATE.tag.width);
  const height = inchesToPx(KUZCO_5371_TEMPLATE.tag.height);

  return (
    <div className="designer-layout">
      <div className="designer-stage" style={{ width, height }}>
        <canvas ref={hostRef} width={width} height={height} />
      </div>
      <aside className="designer-sidebar">
        <label className="kf-field">
          <span className="kf-field-label">SKU</span>
          <select
            className="kf-input kf-md"
            value={skuIndex}
            onChange={(event) => setSkuIndex(Number(event.target.value))}
          >
            {skus.map((item, index) => (
              <option key={item.item_number} value={index}>
                {item.collection_name} · {item.item_number}
              </option>
            ))}
          </select>
        </label>
        <p className="designer-meta">
          Avery 5371 · 3.5×2 in. Drag to move, handles to resize. Layout saves
          in this browser as JSON inches + bindings.
        </p>
        <p className="designer-meta">
          Selected: <strong>{selectedId ?? "none"}</strong>
          <br />
          Previewing {sku.collection_name} / {sku.item_number}
        </p>
        <div className="hang-tag-actions">
          <button className="kb kb-md kb-secondary" type="button" onClick={resetLayout}>
            Reset layout
          </button>
          <button className="kb kb-md kb-primary" type="button" onClick={downloadJson}>
            Download JSON
          </button>
        </div>
      </aside>
    </div>
  );
}
