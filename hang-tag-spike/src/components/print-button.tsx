"use client";

export function PrintButton() {
  return (
    <button
      className="kb kb-md kb-primary"
      type="button"
      onClick={() => window.print()}
    >
      Print
    </button>
  );
}
