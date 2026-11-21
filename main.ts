// Round 5 entry for news-image-20261121: copy the pre-rendered front page
// (entry.png, drawn by render.py in this same repository) to the output
// directory. Node 22 standard library only; no network. The image is
// located from this file's own path, never from the working directory.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const MAX_BYTES = 1048576; // 1 MiB, the competition's size cap

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(outDir, "entry.png");

if (!existsSync(src)) {
  console.error(`entry.png not found next to main.ts (${src})`);
  process.exit(1);
}
const size = statSync(src).size;
if (size > MAX_BYTES) {
  console.error(`entry.png is ${size} bytes, over the 1 MiB limit`);
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
console.log(`wrote ${dest} (${size} bytes)`);
