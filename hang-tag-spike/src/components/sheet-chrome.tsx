import Link from "next/link";
import { PrintButton } from "@/components/print-button";
import { SHEETS, type SheetCode } from "@/data/sheets";

export function SheetChrome({
  sheet,
  designer = false,
}: {
  sheet: SheetCode;
  designer?: boolean;
}) {
  const current = SHEETS[sheet];

  return (
    <header className="hang-tag-chrome no-print">
      <div>
        <h1>Hang tags</h1>
        <p>
          {designer
            ? "Drag objects on a 5371 tag. Layout saves as JSON (inches + bindings)."
            : `${current.name} · ${current.size} · ${current.grid}. Live kll fixture SKUs. Download the PDF to share, or print from here.`}
        </p>
        <nav className="sheet-switcher" aria-label="Avery sheet">
          {(Object.values(SHEETS) as Array<(typeof SHEETS)[SheetCode]>).map(
            (option) => (
              <Link
                key={option.code}
                href={option.href}
                className={
                  !designer && option.code === sheet
                    ? "sheet-switcher-link is-current"
                    : "sheet-switcher-link"
                }
              >
                {option.code}
              </Link>
            ),
          )}
          <Link
            href="/design"
            className={
              designer ? "sheet-switcher-link is-current" : "sheet-switcher-link"
            }
          >
            Design
          </Link>
        </nav>
      </div>
      {designer ? null : (
        <div className="hang-tag-actions">
          <a
            className="kb kb-md kb-secondary"
            href={current.pdfHref}
            download={current.pdfFile}
          >
            Download PDF
          </a>
          <PrintButton />
        </div>
      )}
    </header>
  );
}
