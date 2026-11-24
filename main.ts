// The Daily Meridian -- harness entrypoint.
//
// The judged image, entry.png, sits beside this file in the repository
// (it was drawn by generate.py during development). All this program
// does is deliver that image to the harness: it resolves the output
// directory, makes sure the directory exists, and copies entry.png
// into it under the same name.
//
// Node 22, standard library only -- no packages, no network.

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

try {
  if (!existsSync(source)) {
    throw new Error(`source image not found next to main.ts: ${source}`);
  }
  mkdirSync(outDir, { recursive: true });
  copyFileSync(source, target);
  // A truncated or partial copy must not pass as a delivered entry:
  // verify the destination holds exactly as many bytes as the source.
  const want = statSync(source).size;
  const got = statSync(target).size;
  if (got !== want) {
    throw new Error(
      `copied image is incomplete: ${target} holds ${got} of ${want} bytes`,
    );
  }
} catch (err) {
  console.error(`entrypoint: failed to deliver entry.png: ${err.message}`);
  process.exit(1);
}
