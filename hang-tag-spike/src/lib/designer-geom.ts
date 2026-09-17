import {
  inchesToPx,
  SNAP_INCHES,
  type HangTagTemplate,
} from "@/data/template";

type FabricObject = import("fabric").FabricObject;
type FabricCanvas = import("fabric").Canvas;

export function snapValue(
  value: number,
  targets: number[],
  threshold: number,
): number {
  let best = value;
  let bestDist = threshold;
  for (const target of targets) {
    const distance = Math.abs(value - target);
    if (distance < bestDist) {
      bestDist = distance;
      best = target;
    }
  }
  return best;
}

export function snapMovingTarget(
  target: FabricObject,
  canvas: FabricCanvas,
  template: HangTagTemplate,
) {
  const tagW = inchesToPx(template.tag.width);
  const tagH = inchesToPx(template.tag.height);
  const threshold = inchesToPx(SNAP_INCHES);
  const width = target.getScaledWidth();
  const height = target.getScaledHeight();
  const skip = new Set<FabricObject>([target]);
  const grouped =
    target.type === "activeselection"
      ? (target as import("fabric").ActiveSelection).getObjects()
      : [];
  for (const object of grouped) skip.add(object);

  const xTargets = [0, (tagW - width) / 2, tagW - width];
  const yTargets = [0, (tagH - height) / 2, tagH - height];
  for (const other of canvas.getObjects()) {
    if (skip.has(other)) continue;
    const otherW = other.getScaledWidth();
    const otherH = other.getScaledHeight();
    const otherL = other.left ?? 0;
    const otherT = other.top ?? 0;
    xTargets.push(otherL, otherL + otherW - width, otherL + otherW, otherL - width);
    yTargets.push(otherT, otherT + otherH - height, otherT + otherH, otherT - height);
  }

  target.set({
    left: snapValue(target.left ?? 0, xTargets, threshold),
    top: snapValue(target.top ?? 0, yTargets, threshold),
  });
  target.setCoords();
}
