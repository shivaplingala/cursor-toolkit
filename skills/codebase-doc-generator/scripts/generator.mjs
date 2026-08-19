// generate.mjs — scaffolds the documentation layer (skill 1).
//
// Deterministic, no LLM needed:
//   1. Scan repo for package dirs (contain src/) and nav dirs.
//   2. Write CODEBASE_MAP.md at root + each nav dir (navigation only).
//   3. Write .codedocs/manifest.json (content hashes for change detection).
//   4. Write .codedocs/plan.json — the list of CODE_DETAILS.md files the
//      calling agent must author by reading the source.
//
// Usage: node generate.mjs [rootDir]

import fs from 'node:fs';
import path from 'node:path';
import {
  scan, writeMaps, buildManifest, writeManifest, DOC_DIR, DETAIL_FILE,
} from './core.mjs';

const root = path.resolve(process.argv[2] || process.cwd());

function main() {
  const result = scan(root);
  const { packages, navDirs } = result;
  if (!packages.length) {
    console.error('No package dirs (folders containing a src/) found under ' + root);
  }

  const mapsWritten = writeMaps(root, navDirs, packages);
  const manifest = buildManifest(root, result);
  writeManifest(root, manifest);

  const plan = {
    root,
    generatedAt: manifest.generatedAt,
    detailDocsToWrite: packages.map((p) => ({
      package: p.dir,
      name: p.meta.name,
      description: p.meta.description,
      detailDoc: path.posix.join(p.dir === '.' ? '' : p.dir, DETAIL_FILE),
      sourceFiles: p.files.map((f) => f.rel),
      fileCount: p.files.length,
    })),
    mapsWritten,
  };
  fs.mkdirSync(path.join(root, DOC_DIR), { recursive: true });
  fs.writeFileSync(path.join(root, DOC_DIR, 'plan.json'), JSON.stringify(plan, null, 2));

  console.log(JSON.stringify({
    packages: packages.length,
    navMapsWritten: mapsWritten.length,
    detailDocsToWrite: plan.detailDocsToWrite.length,
    plan: path.posix.join(DOC_DIR, 'plan.json'),
    manifest: path.posix.join(DOC_DIR, 'manifest.json'),
  }, null, 2));
}

main();