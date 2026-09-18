import Link from "next/link";
import { PrintButton } from "@/components/print-button";
import { designerHref, SHEETS, type SheetCode } from "@/data/sheets";

export function SheetChrome({
  sheet,
  designer = false,
}: {
  sheet: SheetCode;
  designer?: boolean;
}) {
  const current = SHEETS[sheet];
  const avery = current.kind === "avery-letter";

  return (
    <header className="hang-tag-chrome no-print">
      <div>
        <h1>Hang tags</h1>
        <p>
          {designer
            ? `Edit the ${current.name} layout. Sheet products and this browser’s JSON print on the ${avery ? "Avery page" : "print page"}.`
            : avery
              ? `${current.name} · ${current.size} · ${current.grid}. Products and layout from Design in this browser. Download the PDF to share, or print from here.`
              : `${current.name} · ${current.size} · ${current.grid}. Photo preview is on-screen only. Print is the tag, not a letter label sheet.`}
        </p>
        <nav className="sheet-switcher" aria-label="Tag format">
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
                {option.shortLabel}
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
            {avery ? "Print sheet" : "Print tag"}
          </Link>
        </div>
      ) : (
        <div className="hang-tag-actions">
          {current.pdfHref && current.pdfFile ? (
            <a
              className="kb kb-md kb-secondary"
              href={current.pdfHref}
              download={current.pdfFile}
            >
              Download PDF
            </a>
          ) : null}
          <PrintButton />
        </div>
      )}
    </header>
  );
}
