import { copyFileSync, mkdirSync, existsSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The bot runs from a different working directory, so locate entry.png
// relative to this script file, never via process.cwd().
const BOT_DIR = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || "/output";

mkdirSync(OUT_DIR, { recursive: true });

const src = join(BOT_DIR, "entry.png");
const dst = join(OUT_DIR, "entry.png");

if (!existsSync(src)) {
  throw new Error("entry.png not found next to main.ts: " + src);
}

copyFileSync(src, dst);

// Verify the copy landed byte-for-byte: same size on both sides.
const srcBytes = statSync(src).size;
const dstBytes = statSync(dst).size;
if (srcBytes !== dstBytes) {
  throw new Error(
    `entry.png copy mismatch: source ${srcBytes} bytes, ` +
      `destination ${dstBytes} bytes`,
  );
}
console.log(`copied entry.png -> ${dst} (${dstBytes} bytes, verified)`);
