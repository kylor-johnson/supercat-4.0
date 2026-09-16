"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { boundImageSrc, boundText } from "@/data/bindings";
import type { HangTagSku } from "@/data/sku";
import type { SheetCode } from "@/data/sheets";
import { codeImageSrc } from "@/lib/codes";
import {
  BARCODE_FORMAT_LABELS,
  BARCODE_FORMATS,
  cloneTemplate,
  DEFAULT_TEMPLATES,
  EDITOR_DPI,
  FONT_FAMILIES,
  FONT_LABELS,
  fontCanvasStack,
  inchesToPx,
  parseStoredTemplate,
  pxToInches,
  resolvedBarcodeFormat,
  resolvedFontFamily,
  resolvedTextAlign,
  STORAGE_KEY,
  templateStorageKey,
  type BarcodeFormat,
  type FontFamily,
  type HangTagTemplate,
  type TemplateObject,
  type TextAlign,
} from "@/data/template";

type FabricModule = typeof import("fabric");
type FabricCanvas = import("fabric").Canvas;
type FabricObject = import("fabric").FabricObject;

type AlignEdge = "left" | "center" | "right" | "top" | "middle" | "bottom";

function ptToPx(points: number): number {
  return (points * EDITOR_DPI) / 72;
}

function applyObjectTransform(object: FabricObject, spec: TemplateObject) {
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

async function objectImageSrc(
  spec: TemplateObject,
  sku: HangTagSku,
  template: HangTagTemplate,
): Promise<string> {
  if (spec.type === "barcode") {
    return codeImageSrc(resolvedBarcodeFormat(template, spec), sku);
  }
  return spec.binding ? boundImageSrc(sku, spec.binding) : "";
}

async function addTemplateObject(
  fabric: FabricModule,
  canvas: FabricCanvas,
  spec: TemplateObject,
  sku: HangTagSku,
  template: HangTagTemplate,
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
      fontFamily: fontCanvasStack(resolvedFontFamily(template, spec)),
      textAlign: resolvedTextAlign(spec),
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

  const src = await objectImageSrc(spec, sku, template);
  if (!src) return;
  const image = await FabricImage.fromURL(src);
  const element = image.getElement() as CanvasImageSource & {
    naturalWidth?: number;
    naturalHeight?: number;
    width?: number;
    height?: number;
  };
  const naturalW =
    image.width || element.naturalWidth || element.width || 1;
  const naturalH =
    image.height || element.naturalHeight || element.height || 1;
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

function selectedIdsFrom(canvas: FabricCanvas): string[] {
  return canvas
    .getActiveObjects()
    .map((object) => object.get("templateId") as string | undefined)
    .filter((id): id is string => Boolean(id));
}

function restoreSelection(
  fabric: FabricModule,
  canvas: FabricCanvas,
  objects: FabricObject[],
) {
  if (objects.length === 1) {
    canvas.setActiveObject(objects[0]);
    return;
  }
  if (objects.length > 1) {
    const selection = new fabric.ActiveSelection(objects, { canvas });
    canvas.setActiveObject(selection);
  }
}

function toolbarClass(active: boolean): string {
  return active ? "kb kb-sm kb-primary" : "kb kb-sm kb-secondary";
}

export function TagDesigner({
  skus,
  stock,
}: {
  skus: HangTagSku[];
  stock: SheetCode;
}) {
  const hostRef = useRef<HTMLCanvasElement | null>(null);
  const fabricRef = useRef<FabricModule | null>(null);
  const canvasRef = useRef<FabricCanvas | null>(null);
  const templateRef = useRef<HangTagTemplate>(
    cloneTemplate(DEFAULT_TEMPLATES[stock]),
  );
  const skuRef = useRef<HangTagSku>(skus[0]);
  const [skuIndex, setSkuIndex] = useState(0);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [draft, setDraft] = useState<HangTagTemplate>(() =>
    cloneTemplate(DEFAULT_TEMPLATES[stock]),
  );
  const [ready, setReady] = useState(false);
  const fallback = DEFAULT_TEMPLATES[stock];

  const persist = useCallback(
    (template: HangTagTemplate) => {
      templateRef.current = template;
      setDraft(cloneTemplate(template));
      window.localStorage.setItem(
        templateStorageKey(stock),
        JSON.stringify(template),
      );
    },
    [stock],
  );

  const rebuild = useCallback(async (keepSelection = true) => {
    const fabric = fabricRef.current;
    const canvas = canvasRef.current;
    if (!fabric || !canvas) return;
    const previous = keepSelection ? selectedIdsFrom(canvas) : [];
    canvas.clear();
    canvas.backgroundColor = "#ffffff";
    if (document.fonts?.ready) await document.fonts.ready;
    for (const spec of templateRef.current.objects) {
      await addTemplateObject(
        fabric,
        canvas,
        spec,
        skuRef.current,
        templateRef.current,
      );
    }
    if (previous.length) {
      const objects = canvas
        .getObjects()
        .filter((object) =>
          previous.includes(object.get("templateId") as string),
        );
      restoreSelection(fabric, canvas, objects);
      setSelectedIds(objects.map((object) => object.get("templateId") as string));
    }
    canvas.requestRenderAll();
  }, []);

  useEffect(() => {
    let disposed = false;
    const canvasEl = hostRef.current;
    if (!canvasEl) return;

    const stored = parseStoredTemplate(
      window.localStorage.getItem(templateStorageKey(stock)) ??
        (stock === "5371" ? window.localStorage.getItem(STORAGE_KEY) : null),
      stock,
    );
    const initial = stored ?? cloneTemplate(fallback);
    templateRef.current = initial;
    setDraft(cloneTemplate(initial));

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
      const syncSelection = () => setSelectedIds(selectedIdsFrom(canvas));
      canvas.on("selection:created", syncSelection);
      canvas.on("selection:updated", syncSelection);
      canvas.on("selection:cleared", () => setSelectedIds([]));
      await rebuild(false);
      setReady(true);
    });

    return () => {
      disposed = true;
      canvasRef.current?.dispose();
      canvasRef.current = null;
    };
  }, [fallback, persist, rebuild, stock]);

  useEffect(() => {
    skuRef.current = skus[skuIndex] ?? skus[0];
    if (ready) void rebuild();
  }, [skuIndex, skus, ready, rebuild]);

  function resetLayout() {
    persist(cloneTemplate(fallback));
    setSelectedIds([]);
    void rebuild(false);
  }

  function downloadJson() {
    const blob = new Blob([JSON.stringify(templateRef.current, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `kuzco-${stock}-template.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  function setGlobalFont(fontFamily: FontFamily) {
    const next = cloneTemplate(templateRef.current);
    next.fontFamily = fontFamily;
    persist(next);
    void rebuild();
  }

  function patchSelected(patch: Partial<TemplateObject>, rebuildCanvas = false) {
    const id = selectedIds[0];
    if (!id) return;
    const next = cloneTemplate(templateRef.current);
    const spec = next.objects.find((item) => item.id === id);
    if (!spec) return;
    Object.assign(spec, patch);
    persist(next);
    const canvas = canvasRef.current;
    const active = canvas?.getActiveObjects()[0];
    if (rebuildCanvas || !canvas || !active) {
      void rebuild();
      return;
    }
    if (patch.fontFamily !== undefined) {
      active.set(
        "fontFamily",
        fontCanvasStack(resolvedFontFamily(next, spec)),
      );
    }
    if (patch.textAlign) {
      active.set("textAlign", patch.textAlign);
    }
    canvas.requestRenderAll();
  }

  function clearObjectFont() {
    const id = selectedIds[0];
    if (!id) return;
    const next = cloneTemplate(templateRef.current);
    const spec = next.objects.find((item) => item.id === id);
    if (!spec) return;
    delete spec.fontFamily;
    persist(next);
    const canvas = canvasRef.current;
    const active = canvas?.getActiveObjects()[0];
    if (canvas && active) {
      active.set(
        "fontFamily",
        fontCanvasStack(resolvedFontFamily(next, spec)),
      );
      canvas.requestRenderAll();
    } else {
      void rebuild();
    }
  }

  function alignObjects(mode: "tag" | "selection", edge: AlignEdge) {
    const fabric = fabricRef.current;
    const canvas = canvasRef.current;
    if (!fabric || !canvas) return;
    const objects = canvas.getActiveObjects();
    if (objects.length === 0) return;
    if (mode === "selection" && objects.length < 2) return;
    canvas.discardActiveObject();

    const boxes = objects.map((object) => ({
      object,
      left: object.left ?? 0,
      top: object.top ?? 0,
      width: object.getScaledWidth(),
      height: object.getScaledHeight(),
    }));

    const tagW = inchesToPx(templateRef.current.tag.width);
    const tagH = inchesToPx(templateRef.current.tag.height);
    let originLeft = 0;
    let originTop = 0;
    let originRight = tagW;
    let originBottom = tagH;
    let originCenterX = tagW / 2;
    let originCenterY = tagH / 2;

    if (mode === "selection") {
      originLeft = Math.min(...boxes.map((box) => box.left));
      originTop = Math.min(...boxes.map((box) => box.top));
      originRight = Math.max(...boxes.map((box) => box.left + box.width));
      originBottom = Math.max(...boxes.map((box) => box.top + box.height));
      originCenterX = (originLeft + originRight) / 2;
      originCenterY = (originTop + originBottom) / 2;
    }

    for (const box of boxes) {
      switch (edge) {
        case "left":
          box.object.set({ left: originLeft });
          break;
        case "center":
          box.object.set({ left: originCenterX - box.width / 2 });
          break;
        case "right":
          box.object.set({ left: originRight - box.width });
          break;
        case "top":
          box.object.set({ top: originTop });
          break;
        case "middle":
          box.object.set({ top: originCenterY - box.height / 2 });
          break;
        case "bottom":
          box.object.set({ top: originBottom - box.height });
          break;
      }
      box.object.setCoords();
    }

    restoreSelection(fabric, canvas, objects);
    canvas.requestRenderAll();
    persist(templateFromCanvas(canvas, templateRef.current));
  }

  function distributeObjects(axis: "horizontal" | "vertical") {
    const fabric = fabricRef.current;
    const canvas = canvasRef.current;
    if (!fabric || !canvas) return;
    const objects = canvas.getActiveObjects();
    if (objects.length < 3) return;
    canvas.discardActiveObject();

    const boxes = objects.map((object) => ({
      object,
      left: object.left ?? 0,
      top: object.top ?? 0,
      width: object.getScaledWidth(),
      height: object.getScaledHeight(),
    }));

    if (axis === "horizontal") {
      boxes.sort((a, b) => a.left - b.left);
      const first = boxes[0];
      const last = boxes[boxes.length - 1];
      const span = last.left + last.width - first.left;
      const total = boxes.reduce((sum, box) => sum + box.width, 0);
      const gap = (span - total) / (boxes.length - 1);
      let x = first.left;
      for (const box of boxes) {
        box.object.set({ left: x });
        box.object.setCoords();
        x += box.width + gap;
      }
    } else {
      boxes.sort((a, b) => a.top - b.top);
      const first = boxes[0];
      const last = boxes[boxes.length - 1];
      const span = last.top + last.height - first.top;
      const total = boxes.reduce((sum, box) => sum + box.height, 0);
      const gap = (span - total) / (boxes.length - 1);
      let y = first.top;
      for (const box of boxes) {
        box.object.set({ top: y });
        box.object.setCoords();
        y += box.height + gap;
      }
    }

    restoreSelection(fabric, canvas, objects);
    canvas.requestRenderAll();
    persist(templateFromCanvas(canvas, templateRef.current));
  }

  const sku = skus[skuIndex] ?? skus[0];
  const width = inchesToPx(fallback.tag.width);
  const height = inchesToPx(fallback.tag.height);
  const selected =
    selectedIds.length === 1
      ? draft.objects.find((item) => item.id === selectedIds[0])
      : undefined;
  const textAlign = selected ? resolvedTextAlign(selected) : "left";
  const globalFont = draft.fontFamily ?? "geist";

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

        <label className="kf-field">
          <span className="kf-field-label">Template font</span>
          <select
            className="kf-input kf-md"
            value={globalFont}
            onChange={(event) =>
              setGlobalFont(event.target.value as FontFamily)
            }
          >
            {FONT_FAMILIES.map((family) => (
              <option key={family} value={family}>
                {FONT_LABELS[family]}
              </option>
            ))}
          </select>
          <span className="kf-field-hint">
            Applies to text without its own face. SKU stays Geist Mono until you
            override it.
          </span>
        </label>

        {selected?.type === "text" ? (
          <>
            <label className="kf-field">
              <span className="kf-field-label">Object font</span>
              <select
                className="kf-input kf-md"
                value={selected.fontFamily ?? ""}
                onChange={(event) => {
                  const value = event.target.value;
                  if (!value) clearObjectFont();
                  else patchSelected({ fontFamily: value as FontFamily });
                }}
              >
                <option value="">Template default</option>
                {FONT_FAMILIES.map((family) => (
                  <option key={family} value={family}>
                    {FONT_LABELS[family]}
                  </option>
                ))}
              </select>
            </label>
            <div className="kf-field">
              <span className="kf-field-label">Text align</span>
              <div className="designer-toolbar">
                {(["left", "center", "right"] as TextAlign[]).map((align) => (
                  <button
                    key={align}
                    className={toolbarClass(textAlign === align)}
                    type="button"
                    onClick={() => patchSelected({ textAlign: align })}
                  >
                    {align}
                  </button>
                ))}
              </div>
            </div>
          </>
        ) : null}

        {selected?.type === "barcode" ? (
          <label className="kf-field">
            <span className="kf-field-label">Barcode type</span>
            <select
              className="kf-input kf-md"
              value={resolvedBarcodeFormat(draft, selected)}
              onChange={(event) =>
                patchSelected(
                  { barcodeFormat: event.target.value as BarcodeFormat },
                  true,
                )
              }
            >
              {BARCODE_FORMATS.map((format) => (
                <option key={format} value={format}>
                  {BARCODE_FORMAT_LABELS[format]}
                </option>
              ))}
            </select>
            <span className="kf-field-hint">
              UPC-A is the Kuzco default. QR and Code 128 encode the UPC digits
              on this SKU. Resize the box square for a larger QR.
            </span>
          </label>
        ) : null}

        {selectedIds.length > 0 ? (
          <div className="kf-field">
            <span className="kf-field-label">Align to tag</span>
            <div className="designer-toolbar">
              {(
                [
                  ["left", "Left"],
                  ["center", "Center"],
                  ["right", "Right"],
                  ["top", "Top"],
                  ["middle", "Middle"],
                  ["bottom", "Bottom"],
                ] as Array<[AlignEdge, string]>
              ).map(([edge, label]) => (
                <button
                  key={`tag-${edge}`}
                  className="kb kb-sm kb-secondary"
                  type="button"
                  onClick={() => alignObjects("tag", edge)}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
        ) : null}

        {selectedIds.length >= 2 ? (
          <div className="kf-field">
            <span className="kf-field-label">Align to selection</span>
            <div className="designer-toolbar">
              {(
                [
                  ["left", "Left"],
                  ["center", "Center"],
                  ["right", "Right"],
                  ["top", "Top"],
                  ["middle", "Middle"],
                  ["bottom", "Bottom"],
                ] as Array<[AlignEdge, string]>
              ).map(([edge, label]) => (
                <button
                  key={`sel-${edge}`}
                  className="kb kb-sm kb-secondary"
                  type="button"
                  onClick={() => alignObjects("selection", edge)}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
        ) : null}

        {selectedIds.length >= 3 ? (
          <div className="kf-field">
            <span className="kf-field-label">Distribute</span>
            <div className="designer-toolbar">
              <button
                className="kb kb-sm kb-secondary"
                type="button"
                onClick={() => distributeObjects("horizontal")}
              >
                Horizontal
              </button>
              <button
                className="kb kb-sm kb-secondary"
                type="button"
                onClick={() => distributeObjects("vertical")}
              >
                Vertical
              </button>
            </div>
          </div>
        ) : null}

        <p className="designer-meta">
          Avery {stock} · {fallback.tag.width}×{fallback.tag.height} in. Drag to
          move, handles to resize. Layout saves in this browser as JSON inches +
          bindings. Print sheets read the same JSON.
        </p>
        <p className="designer-meta">
          Selected:{" "}
          <strong>
            {selectedIds.length === 0
              ? "none"
              : selectedIds.length === 1
                ? selectedIds[0]
                : `${selectedIds.length} objects`}
          </strong>
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
