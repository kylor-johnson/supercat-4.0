"use client";

import { useEffect, useState, type CSSProperties } from "react";
import type { HangTagSku } from "@/data/sku";
import type { BarcodeFormat } from "@/data/template";
import { codeImageSrc, upcFixtureSrc } from "@/lib/codes";

export function BarcodeMark({
  sku,
  format,
  className,
  style,
}: {
  sku: HangTagSku;
  format: BarcodeFormat;
  className?: string;
  style?: CSSProperties;
}) {
  const upcSrc = upcFixtureSrc(sku);
  const [generated, setGenerated] = useState("");

  useEffect(() => {
    if (format === "upc") return;
    let cancelled = false;
    void codeImageSrc(format, sku).then((next) => {
      if (!cancelled) setGenerated(next);
    });
    return () => {
      cancelled = true;
    };
  }, [format, sku]);

  const src = format === "upc" ? upcSrc : generated;
  if (!src) return null;
  return <img className={className} style={style} src={src} alt="" />;
}
