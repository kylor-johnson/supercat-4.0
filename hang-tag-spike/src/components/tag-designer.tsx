"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { MiniSheet } from "@/components/template-sheet";
import { HangTagSizzle } from "@/components/hang-tag-sizzle";
import { boundImageSrc, boundText } from "@/data/bindings";
import {
  BOOLEAN_BINDINGS,
  BOOLEAN_LABELS,
  type BooleanBinding,
  type HangTagSku,
} from "@/data/sku";
import { SHEETS, TAGS_PER_SHEET, type SheetCode } from "@/data/sheets";
import { codeImageSrc } from "@/lib/codes";
import { snapMovingTarget } from "@/lib/designer-geom";
import { resolvedItemNumbers } from "@/lib/sheet-skus";
import {
  BARCODE_FORMAT_LABELS,
  BARCODE_FORMATS,
  BINDING_LABELS,
  bindingsForType,
  cloneTemplate,
  DEFAULT_TEMPLATES,
  EDITOR_DPI,
  FONT_FAMILIES,
  FONT_LABELS,
  fontCanvasStack,
  HISTORY_LIMIT,
  LETTER_SPACING_OPTIONS,
  NUDGE_INCHES,
  NUDGE_SHIFT_INCHES,
  emToCharSpacing,
  inchesToPx,
  objectVisible,
  parseStoredTemplate,
  pxToInches,
  resolvedBarcodeFormat,
  resolvedFontFamily,
  resolvedFontSize,
  resolvedFontWeight,
  resolvedTextAlign,
  STORAGE_KEY,
  templateStorageKey,
  type BarcodeFormat,
  type BindingKey,
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
      fontSize: ptToPx(resolvedFontSize(spec)),
      fontWeight: resolvedFontWeight(spec),
      fontFamily: fontCanvasStack(resolvedFontFamily(template, spec)),
      textAlign: resolvedTextAlign(spec),
      charSpacing: emToCharSpacing(spec.letterSpacing),
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

function templatesEqual(a: HangTagTemplate, b: HangTagTemplate): boolean {
  return JSON.stringify(a) === JSON.stringify(b);
}

function isEditingField(target: EventTarget | null): boolean {
  if (!(target instanceof HTMLElement)) return false;
  return Boolean(target.closest("input, select, textarea, [contenteditable]"));
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
  const historyRef = useRef<HangTagTemplate[]>([]);
  const historyIndexRef = useRef(0);
  const [skuIndex, setSkuIndex] = useState(0);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [draft, setDraft] = useState<HangTagTemplate>(() =>
    cloneTemplate(DEFAULT_TEMPLATES[stock]),
  );
  const [historyState, setHistoryState] = useState({ index: 0, length: 1 });
  const [ready, setReady] = useState(false);
  const sheet = SHEETS[stock];
  const [sizzle, setSizzle] = useState(sheet.preview === "sizzle");
  const fallback = DEFAULT_TEMPLATES[stock];
  const sheetKey = (draft.itemNumbers ?? []).join("|");

  const persist = useCallback(
    (template: HangTagTemplate, options?: { history?: boolean }) => {
      const next = cloneTemplate(template);
      templateRef.current = next;
      setDraft(cloneTemplate(next));
      window.localStorage.setItem(
        templateStorageKey(stock),
        JSON.stringify(next),
      );
      if (options?.history === false) return;
      const stack = historyRef.current.slice(0, historyIndexRef.current + 1);
      const last = stack[stack.length - 1];
      if (last && templatesEqual(last, next)) return;
      stack.push(cloneTemplate(next));
      if (stack.length > HISTORY_LIMIT) stack.shift();
      historyRef.current = stack;
      historyIndexRef.current = stack.length - 1;
      setHistoryState({ index: stack.length - 1, length: stack.length });
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
      if (!objectVisible(spec, skuRef.current)) continue;
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
    historyRef.current = [cloneTemplate(initial)];
    historyIndexRef.current = 0;
    setHistoryState({ index: 0, length: 1 });

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
      canvas.on("object:moving", (event) => {
        if (!event.target) return;
        snapMovingTarget(event.target, canvas, templateRef.current);
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
    const preview = resolvedItemNumbers(templateRef.current, skus)
      .map((code) => skus.find((item) => item.item_number === code))
      .filter((item): item is HangTagSku => Boolean(item));
    skuRef.current = preview[skuIndex] ?? preview[0] ?? skus[0];
    if (ready) void rebuild();
  }, [skuIndex, skus, ready, rebuild, sheetKey]);

  function resetLayout() {
    persist(cloneTemplate(fallback));
    setSelectedIds([]);
    void rebuild(false);
  }

  const applyHistory = useCallback(
    (index: number) => {
      const template = historyRef.current[index];
      if (!template) return;
      historyIndexRef.current = index;
      setHistoryState({ index, length: historyRef.current.length });
      persist(cloneTemplate(template), { history: false });
      void rebuild();
    },
    [persist, rebuild],
  );

  const undo = useCallback(() => {
    if (historyIndexRef.current <= 0) return;
    applyHistory(historyIndexRef.current - 1);
  }, [applyHistory]);

  const redo = useCallback(() => {
    if (historyIndexRef.current >= historyRef.current.length - 1) return;
    applyHistory(historyIndexRef.current + 1);
  }, [applyHistory]);

  const nudgeSelected = useCallback(
    (dxIn: number, dyIn: number) => {
      const fabric = fabricRef.current;
      const canvas = canvasRef.current;
      if (!fabric || !canvas) return;
      const objects = canvas.getActiveObjects();
      if (objects.length === 0) return;
      canvas.discardActiveObject();
      const dx = inchesToPx(dxIn);
      const dy = inchesToPx(dyIn);
      for (const object of objects) {
        object.set({
          left: (object.left ?? 0) + dx,
          top: (object.top ?? 0) + dy,
        });
        object.setCoords();
      }
      restoreSelection(fabric, canvas, objects);
      canvas.requestRenderAll();
      persist(templateFromCanvas(canvas, templateRef.current));
    },
    [persist],
  );

  useEffect(() => {
    if (!ready) return;
    function onKey(event: KeyboardEvent) {
      if (isEditingField(event.target)) return;
      const key = event.key.toLowerCase();
      if ((event.metaKey || event.ctrlKey) && key === "z") {
        event.preventDefault();
        if (event.shiftKey) redo();
        else undo();
        return;
      }
      if ((event.metaKey || event.ctrlKey) && key === "y") {
        event.preventDefault();
        redo();
        return;
      }
      if (
        event.key !== "ArrowLeft" &&
        event.key !== "ArrowRight" &&
        event.key !== "ArrowUp" &&
        event.key !== "ArrowDown"
      ) {
        return;
      }
      if (!canvasRef.current?.getActiveObjects().length) return;
      event.preventDefault();
      const step = event.shiftKey ? NUDGE_SHIFT_INCHES : NUDGE_INCHES;
      const dx =
        event.key === "ArrowLeft" ? -step : event.key === "ArrowRight" ? step : 0;
      const dy =
        event.key === "ArrowUp" ? -step : event.key === "ArrowDown" ? step : 0;
      nudgeSelected(dx, dy);
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [nudgeSelected, persist, ready, redo, undo]);

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

  function setSheetItems(itemNumbers: string[]) {
    const next = cloneTemplate(templateRef.current);
    next.itemNumbers = itemNumbers;
    persist(next);
    const preview = resolvedItemNumbers(next, skus);
    if (skuIndex >= preview.length) setSkuIndex(0);
  }

  function toggleSheetItem(itemNumber: string) {
    const current = resolvedItemNumbers(templateRef.current, skus);
    if (current.includes(itemNumber)) {
      if (current.length === 1) return;
      setSheetItems(current.filter((code) => code !== itemNumber));
      return;
    }
    setSheetItems([...current, itemNumber]);
  }

  function moveSheetItem(itemNumber: string, direction: -1 | 1) {
    const current = resolvedItemNumbers(templateRef.current, skus);
    const index = current.indexOf(itemNumber);
    const nextIndex = index + direction;
    if (index < 0 || nextIndex < 0 || nextIndex >= current.length) return;
    const next = [...current];
    const [moved] = next.splice(index, 1);
    next.splice(nextIndex, 0, moved);
    setSheetItems(next);
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
    if (patch.fontSize !== undefined) {
      active.set("fontSize", ptToPx(patch.fontSize));
    }
    if (patch.fontWeight !== undefined) {
      active.set("fontWeight", patch.fontWeight);
    }
    if ("letterSpacing" in patch) {
      active.set("charSpacing", emToCharSpacing(patch.letterSpacing));
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

  function patchSelectedShowIf(
    mode: "always" | "true" | "false",
    binding: BooleanBinding,
  ) {
    const id = selectedIds[0];
    if (!id) return;
    const next = cloneTemplate(templateRef.current);
    const spec = next.objects.find((item) => item.id === id);
    if (!spec) return;
    if (mode === "always") delete spec.showIf;
    else spec.showIf = { binding, equals: mode === "true" };
    persist(next);
    void rebuild();
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

  const skuCatalog = skus;
  const sheetItemNumbers = resolvedItemNumbers(draft, skuCatalog);
  const previewSkus = sheetItemNumbers
    .map((code) => skuCatalog.find((item) => item.item_number === code))
    .filter((item): item is HangTagSku => Boolean(item));
  const sku = previewSkus[skuIndex] ?? previewSkus[0] ?? skuCatalog[0];
  const width = inchesToPx(fallback.tag.width);
  const height = inchesToPx(fallback.tag.height);
  const selected =
    selectedIds.length === 1
      ? draft.objects.find((item) => item.id === selectedIds[0])
      : undefined;
  const textAlign = selected ? resolvedTextAlign(selected) : "left";
  const globalFont = draft.fontFamily ?? "geist";
  const canUndo = historyState.index > 0;
  const canRedo = historyState.index < historyState.length - 1;
  const slots = TAGS_PER_SHEET[stock];
  const avery = sheet.kind === "avery-letter";
  const showMode = selected?.showIf
    ? selected.showIf.equals
      ? "true"
      : "false"
    : "always";
  const showBinding: BooleanBinding =
    selected?.showIf?.binding ?? "c.QuickShip";
  const selectedLabel =
    selectedIds.length === 0
      ? "none"
      : selectedIds.length === 1
        ? `${selectedIds[0]}${selected ? ` · ${selected.type}` : ""}`
        : `${selectedIds.length} objects`;
  const unselectedSkus = skuCatalog.filter(
    (item) => !sheetItemNumbers.includes(item.item_number),
  );

  return (
    <div className="designer-layout">
      <div className="designer-stages">
        <div>
          <p className="designer-stage-label">Edit</p>
          <div className="designer-stage" style={{ width, height }}>
            <canvas ref={hostRef} width={width} height={height} />
          </div>
        </div>
        {sizzle ? (
          <div>
            <p className="designer-stage-label">Photo preview · hole</p>
            <HangTagSizzle sku={sku} template={draft} />
          </div>
        ) : null}
        {!sizzle || avery ? (
          <div>
            <p className="designer-stage-label">
              {avery
                ? `${sheet.name} sheet · this browser`
                : `${sheet.name} · this browser`}
            </p>
            <MiniSheet stock={stock} skus={skuCatalog} template={draft} />
          </div>
        ) : null}
      </div>
      <aside className="designer-sidebar">
        <p className="designer-hint">
          {selectedIds.length === 0
            ? `Click a line for type and Field. Sheet products below print on the ${avery ? "Avery page" : "print page"} in this browser.`
            : selected?.type === "text"
              ? "Type, weight, and tracking apply to this line and the print preview. Show when hides this object from Edit, mini, and print."
              : selected?.type === "barcode"
                ? "UPC-A is the Kuzco default. QR / Code 128 encode this SKU’s UPC digits."
                : selectedIds.length > 1
                  ? "Shift-click adds to the selection. Align to selection appears at 2+; distribute at 3+."
                  : "Align to tag writes x / y inches into the JSON the print sheet reads."}
        </p>
        <p className="designer-meta">
          Selected: <strong>{selectedLabel}</strong>
          <br />
          Previewing {sku.collection_name} / {sku.item_number}
          {sku["c.QuickShip"] ? " · c.QuickShip" : ""}
        </p>

        <label className="kf-field">
          <span className="kf-field-label">Edit preview</span>
          <select
            className="kf-input kf-md"
            value={Math.min(skuIndex, Math.max(previewSkus.length - 1, 0))}
            onChange={(event) => setSkuIndex(Number(event.target.value))}
          >
            {previewSkus.map((item, index) => (
              <option key={item.item_number} value={index}>
                {item.collection_name} · {item.item_number}
                {item["c.QuickShip"] ? " · QS" : ""}
              </option>
            ))}
          </select>
          <span className="kf-field-hint">
            Layout canvas only. Does not change who is on the sheet. Switch SKU
            to prove Show when.
          </span>
        </label>

        {selected ? (
          <>
            <label className="kf-field">
              <span className="kf-field-label">Field</span>
              <select
                className="kf-input kf-md"
                value={selected.binding ?? ""}
                onChange={(event) => {
                  const value = event.target.value;
                  patchSelected(
                    { binding: value ? (value as BindingKey) : null },
                    true,
                  );
                }}
              >
                {selected.type === "text" ? (
                  <option value="">Static text</option>
                ) : null}
                {bindingsForType(selected.type).map((binding) => (
                  <option key={binding} value={binding}>
                    {BINDING_LABELS[binding]}
                  </option>
                ))}
              </select>
            </label>
            {selected.type === "text" && !selected.binding ? (
              <label className="kf-field">
                <span className="kf-field-label">Static text</span>
                <input
                  className="kf-input kf-md"
                  type="text"
                  value={selected.text ?? ""}
                  onChange={(event) =>
                    patchSelected({ text: event.target.value }, true)
                  }
                />
              </label>
            ) : null}
            <label className="kf-field">
              <span className="kf-field-label">Show when</span>
              <select
                className="kf-input kf-md"
                value={showMode}
                onChange={(event) =>
                  patchSelectedShowIf(
                    event.target.value as "always" | "true" | "false",
                    showBinding,
                  )
                }
              >
                <option value="always">Always</option>
                <option value="true">Flag is true</option>
                <option value="false">Flag is false</option>
              </select>
            </label>
            {showMode !== "always" ? (
              <label className="kf-field">
                <span className="kf-field-label">Flag</span>
                <select
                  className="kf-input kf-md"
                  value={showBinding}
                  onChange={(event) =>
                    patchSelectedShowIf(
                      showMode,
                      event.target.value as BooleanBinding,
                    )
                  }
                >
                  {BOOLEAN_BINDINGS.map((binding) => (
                    <option key={binding} value={binding}>
                      {BOOLEAN_LABELS[binding]}
                    </option>
                  ))}
                </select>
              </label>
            ) : null}
          </>
        ) : null}

        <label className="designer-sizzle-toggle">
          <input
            type="checkbox"
            checked={sizzle}
            onChange={(event) => setSizzle(event.target.checked)}
          />
          <span>Photo preview with hole</span>
        </label>
        <span className="kf-field-hint">
          On-screen sizzle only. Avery print stays a flat letter sheet of
          labels. Hang-tag print is the 2×3.5 tag, not this photo.
        </span>

        <div className="kf-field">
          <span className="kf-field-label">Sheet products</span>
          <span className="kf-field-hint">
            {avery
              ? `${sheet.name} holds ${slots} tags. Print order below. A short list repeats to fill the sheet. Same list as the print page in this browser.`
              : `${sheet.name} prints one tag per selected SKU (no repeat-to-fill). Same list as the print page in this browser.`}
          </span>
          <div className="designer-sku-list">
            {sheetItemNumbers.map((code, index) => {
              const item = skuCatalog.find((skuItem) => skuItem.item_number === code);
              if (!item) return null;
              return (
                <div className="designer-sku-row" key={code}>
                  <button
                    className="kb kb-sm kb-secondary"
                    type="button"
                    disabled={index === 0}
                    onClick={() => moveSheetItem(code, -1)}
                  >
                    Up
                  </button>
                  <button
                    className="kb kb-sm kb-secondary"
                    type="button"
                    disabled={index === sheetItemNumbers.length - 1}
                    onClick={() => moveSheetItem(code, 1)}
                  >
                    Down
                  </button>
                  <span>
                    {item.collection_name} · {item.item_number}
                  </span>
                  <button
                    className="kb kb-sm kb-secondary"
                    type="button"
                    disabled={sheetItemNumbers.length === 1}
                    onClick={() => toggleSheetItem(code)}
                  >
                    Remove
                  </button>
                </div>
              );
            })}
          </div>
          {unselectedSkus.length ? (
            <div className="designer-sku-add">
              <span className="kf-field-label">Add from fixture</span>
              {unselectedSkus.map((item) => (
                <button
                  key={item.item_number}
                  className="kb kb-sm kb-secondary"
                  type="button"
                  onClick={() => toggleSheetItem(item.item_number)}
                >
                  {item.collection_name}
                </button>
              ))}
            </div>
          ) : (
            <span className="kf-field-hint">All 10 fixture SKUs are on the sheet.</span>
          )}
        </div>

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
            <label className="kf-field">
              <span className="kf-field-label">Size (pt)</span>
              <input
                className="kf-input kf-md"
                type="number"
                min={6}
                max={24}
                step={0.5}
                value={resolvedFontSize(selected)}
                onChange={(event) =>
                  patchSelected({
                    fontSize: Number(event.target.value) || 8,
                  })
                }
              />
            </label>
            <div className="kf-field">
              <span className="kf-field-label">Weight</span>
              <div className="designer-toolbar">
                <button
                  className={toolbarClass(resolvedFontWeight(selected) === 400)}
                  type="button"
                  onClick={() => patchSelected({ fontWeight: 400 })}
                >
                  Regular
                </button>
                <button
                  className={toolbarClass(resolvedFontWeight(selected) >= 700)}
                  type="button"
                  onClick={() => patchSelected({ fontWeight: 700 })}
                >
                  Bold
                </button>
              </div>
            </div>
            <label className="kf-field">
              <span className="kf-field-label">Tracking</span>
              <select
                className="kf-input kf-md"
                value={selected.letterSpacing ?? ""}
                onChange={(event) =>
                  patchSelected({
                    letterSpacing: event.target.value || undefined,
                  })
                }
              >
                {LETTER_SPACING_OPTIONS.map((option) => (
                  <option key={option.label} value={option.value}>
                    {option.label}
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
          {sheet.name} · {fallback.tag.width}×{fallback.tag.height} in. Layout
          saves in this browser. Print sheets read the same JSON.
        </p>
        <div className="hang-tag-actions">
          <button
            className="kb kb-md kb-secondary"
            type="button"
            disabled={!canUndo}
            onClick={undo}
          >
            Undo
          </button>
          <button
            className="kb kb-md kb-secondary"
            type="button"
            disabled={!canRedo}
            onClick={redo}
          >
            Redo
          </button>
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
