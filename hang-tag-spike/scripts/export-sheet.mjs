import { mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const outDir = join(root, "public/reviews");
mkdirSync(outDir, { recursive: true });

const chrome =
  process.env.CHROME_PATH ||
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const jobs = [
  { url: "http://localhost:3000/", file: "kuzco-5371-sheet.pdf" },
  { url: "http://localhost:3000/5392", file: "kuzco-5392-sheet.pdf" },
];

for (const job of jobs) {
  const outFile = join(outDir, job.file);
  const result = spawnSync(
    chrome,
    [
      "--headless=new",
      "--disable-gpu",
      "--no-pdf-header-footer",
      "--run-all-compositor-stages-before-draw",
      "--virtual-time-budget=8000",
      `--print-to-pdf=${outFile}`,
      job.url,
    ],
    { encoding: "utf8" },
  );

  if (result.status !== 0) {
    console.error(result.stderr || result.stdout);
    process.exit(result.status ?? 1);
  }

  console.log(`wrote ${outFile}`);
}
