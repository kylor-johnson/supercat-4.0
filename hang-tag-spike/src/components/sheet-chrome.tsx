import Link from "next/link";
import { PrintButton } from "@/components/print-button";
import { SHEETS, type SheetCode } from "@/data/sheets";

function designerHref(stock: SheetCode): string {
  return stock === "5392" ? "/design?stock=5392" : "/design";
}

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
            ? `Drag objects on a ${sheet} tag. Layout saves as JSON (inches + bindings). Print sheets render that JSON.`
            : `${current.name} · ${current.size} · ${current.grid}. Fixture kll SKUs on disk. Download the PDF to share, or print from here.`}
        </p>
        <nav className="sheet-switcher" aria-label="Avery sheet">
          {(Object.values(SHEETS) as Array<(typeof SHEETS)[SheetCode]>).map(
            (option) => (
              <Link
                key={option.code}
                href={designer ? designerHref(option.code) : option.href}
                className={
                  option.code === sheet
                    ? "sheet-switcher-link is-current"
                    : "sheet-switcher-link"
                }
              >
                {option.code}
              </Link>
            ),
          )}
          <Link
            href={designerHref(sheet)}
            className={
              designer ? "sheet-switcher-link is-current" : "sheet-switcher-link"
            }
          >
            Design
          </Link>
        </nav>
      </div>
      {designer ? (
        <div className="hang-tag-actions">
          <Link className="kb kb-md kb-secondary" href={current.href}>
            Print sheet
          </Link>
        </div>
      ) : (
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
