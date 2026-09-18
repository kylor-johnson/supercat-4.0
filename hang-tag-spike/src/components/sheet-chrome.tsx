import Link from "next/link";
import { PrintButton } from "@/components/print-button";
import { SuperCatMark } from "@/components/supercat-mark";
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
  const printLabel = avery ? "Print sheet" : "Print tag";
  const lede = designer
    ? "Format → products → design → print."
    : avery
      ? "Print this 8.5×11 sheet of labels."
      : "On-screen hole preview. Print is the tag.";

  return (
    <header className="hang-tag-chrome no-print">
      <div className="hang-tag-brand">
        <span className="hang-tag-mark">
          <SuperCatMark />
        </span>
        <div>
          <h1>Hang tags</h1>
          <p className="hang-tag-lede">{lede}</p>
        </div>
      </div>
      <nav
        className="ktab ktab-seg ktab-sm hang-tag-switcher"
        aria-label="Tag format"
      >
        {(Object.values(SHEETS) as Array<(typeof SHEETS)[SheetCode]>).map(
          (option) => (
            <Link
              key={option.code}
              href={designer ? designerHref(option.code) : option.href}
              className="ktab-item"
              role="tab"
              aria-selected={option.code === sheet}
              title={option.navHint}
            >
              {option.navLabel}
              {option.code === "hangtag" ? (
                <span className="ktab-item-spec">{option.navHint}</span>
              ) : null}
            </Link>
          ),
        )}
      </nav>
      <div className="hang-tag-actions">
        {designer ? (
          <Link className="kb kb-md kb-primary" href={current.href}>
            {printLabel}
          </Link>
        ) : (
          <>
            <Link className="kb kb-md kb-secondary" href={designerHref(sheet)}>
              Design
            </Link>
            {current.pdfHref && current.pdfFile ? (
              <a
                className="kb kb-md kb-secondary"
                href={current.pdfHref}
                download={current.pdfFile}
              >
                Download PDF
              </a>
            ) : null}
            <PrintButton label={printLabel} />
          </>
        )}
      </div>
    </header>
  );
}
