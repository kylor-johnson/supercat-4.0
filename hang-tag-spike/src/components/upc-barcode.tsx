type UpcBarcodeProps = {
  value: string;
};

export function UpcBarcode({ value }: UpcBarcodeProps) {
  const digits = value.replace(/\D/g, "");
  if (digits.length < 11) {
    return <div className="hang-tag-upc-text">{value}</div>;
  }

  return (
    <img
      className="hang-tag-upc"
      src={`/fixtures/barcodes/${digits}.svg`}
      alt={`UPC ${digits}`}
    />
  );
}
