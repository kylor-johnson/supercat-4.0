"use client";

export function PrintButton({ label = "Print" }: { label?: string }) {
  return (
    <button
      className="kb kb-md kb-primary"
      type="button"
      onClick={() => window.print()}
    >
      {label}
    </button>
  );
}
