export type CsvTable = {
  headers: string[];
  rows: Record<string, string>[];
};

export function parseCsvRows(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let i = 0;
  let inQuotes = false;
  const input = text.replace(/^\uFEFF/, "");

  while (i < input.length) {
    const char = input[i];
    if (inQuotes) {
      if (char === '"') {
        if (input[i + 1] === '"') {
          cell += '"';
          i += 2;
          continue;
        }
        inQuotes = false;
        i += 1;
        continue;
      }
      cell += char;
      i += 1;
      continue;
    }
    if (char === '"') {
      inQuotes = true;
      i += 1;
      continue;
    }
    if (char === ",") {
      row.push(cell);
      cell = "";
      i += 1;
      continue;
    }
    if (char === "\n" || char === "\r") {
      if (char === "\r" && input[i + 1] === "\n") i += 1;
      row.push(cell);
      cell = "";
      if (row.some((value) => value.trim() !== "")) rows.push(row);
      row = [];
      i += 1;
      continue;
    }
    cell += char;
    i += 1;
  }
  row.push(cell);
  if (row.some((value) => value.trim() !== "")) rows.push(row);
  return rows;
}

export function parseCsv(text: string): CsvTable {
  const records = parseCsvRows(text);
  if (!records.length) return { headers: [], rows: [] };
  const headers = records[0].map((header) => header.replace(/^\uFEFF/, "").trim());
  const rows: Record<string, string>[] = [];
  for (const record of records.slice(1)) {
    if (record.every((value) => value.trim() === "")) continue;
    const row: Record<string, string> = {};
    headers.forEach((header, index) => {
      row[header] = record[index] ?? "";
    });
    rows.push(row);
  }
  return { headers, rows };
}
