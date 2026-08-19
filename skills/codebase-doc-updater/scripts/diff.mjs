// diff.mjs — change detection for the updater (skill 2) and watcher (skill 3).
//
// Compares the current source tree against .codedocs/manifest.json and reports
// exactly what changed, so an agent only rewrites the CODE_DETAILS.md files
// that actually need it.
//
// Usage:
//   node diff.mjs [rootDir]              # print change report (JSON) to stdout
//   node diff.mjs [rootDir] --apply      # also refresh maps + manifest and
//                                          write .codedocs/plan.json (incremental)
//   node diff.mjs [rootDir] --pending    # merge changes into .codedocs/pending.json
//                                          (used by hooks/watcher; no LLM needed)
//
// Exit code is 0 always; read the JSON `hasChanges` field to branch.

import fs from 'node:fs';
import path from 'node:path';
import {
  scan, loadManifest, buildManifest, writeManifest, writeMaps,
  DOC_DIR, PENDING, DETAIL_FILE,
} from './core.mjs';

const args = process.argv.slice(2);
const flags = new Set(args.filter((a) => a.startsWith('--')));
const root = path.resolve(args.find((a) => !a.startsWith('--')) || process.cwd());

function diff(root) {
  const prev = loadManifest(root);
  const current = scan(root);
  const curManifest = buildManifest(root, current);

  if (!prev) {
    return {
      hasManifest: false,
      hasChanges: true,
      note: 'No manifest found — run the generator (skill 1) first for a full build.',
      current,
      curManifest,
    };
  }

  const prevPkgs = new Set(Object.keys(prev.packages || {}));
  const curPkgs = new Set(Object.keys(curManifest.packages));

  const packagesAdded = [...curPkgs].filter((d) => !prevPkgs.has(d)).sort();
  const packagesRemoved = [...prevPkgs].filter((d) => !curPkgs.has(d)).sort();

  // Per-file changes within surviving packages.
  const prevFiles = prev.files || {};
  const curFiles = curManifest.files;
  const changedPkgs = new Map(); // pkg -> { added:[], removed:[], modified:[] }

  const touch = (pkg) => {
    if (!changedPkgs.has(pkg)) changedPkgs.set(pkg, { added: [], removed: [], modified: [] });
    return changedPkgs.get(pkg);
  };

  for (const [rel, info] of Object.entries(curFiles)) {
    const before = prevFiles[rel];
    if (!before) {
      if (!packagesAdded.includes(info.pkg)) touch(info.pkg).added.push(rel);
    } else if (before.hash !== info.hash) {
      touch(info.pkg).modified.push(rel);
    }
  }
  for (const [rel, info] of Object.entries(prevFiles)) {
    if (!curFiles[rel] && !packagesRemoved.includes(info.pkg)) {
      touch(info.pkg).removed.push(rel);
    }
  }

  const packagesChanged = [...changedPkgs.entries()]
    .map(([pkg, v]) => ({ pkg, ...v }))
    .sort((a, b) => a.pkg.localeCompare(b.pkg));

  // Nav structure change → which maps to refresh. Compare child sets.
  const prevNav = new Map((prev.navDirs || []).map((n) => [n.dir, (n.children || []).join(',')]));
  const curNav = new Map(current.navDirs.map((n) => [n.dir, n.children.join(',')]));
  const navChanged = packagesAdded.length || packagesRemoved.length
    || [...curNav.keys()].some((d) => prevNav.get(d) !== curNav.get(d))
    || [...prevNav.keys()].some((d) => !curNav.has(d));

  const hasChanges = packagesAdded.length > 0 || packagesRemoved.length > 0
    || packagesChanged.length > 0 || navChanged;

  return {
    hasManifest: true,
    hasChanges,
    packagesAdded,
    packagesRemoved,
    packagesChanged,
    navChanged,
    current,
    curManifest,
  };
}

function incrementalPlan(root, d) {
  const pkgFiles = new Map(d.current.packages.map((p) => [p.dir, p.files.map((f) => f.rel)]));
  const toWrite = new Set([...d.packagesAdded, ...d.packagesChanged.map((c) => c.pkg)]);
  return {
    root,
    generatedAt: new Date().toISOString(),
    detailDocsToWrite: [...toWrite].sort().map((pkg) => ({
      package: pkg,
      reason: d.packagesAdded.includes(pkg) ? 'new package' : 'source changed',
      detailDoc: path.posix.join(pkg === '.' ? '' : pkg, DETAIL_FILE),
      sourceFiles: pkgFiles.get(pkg) || [],
    })),
    detailDocsToDelete: d.packagesRemoved.map((pkg) =>
      path.posix.join(pkg === '.' ? '' : pkg, DETAIL_FILE)),
  };
}

function mergePending(root, d) {
  const p = path.join(root, PENDING);
  let cur = { updatedAt: null, packages: {} };
  try { cur = JSON.parse(fs.readFileSync(p, 'utf8')); } catch {}
  cur.updatedAt = new Date().toISOString();
  cur.packages = cur.packages || {};
  const mark = (pkg, reason) => {
    cur.packages[pkg] = { reason, since: cur.packages[pkg]?.since || cur.updatedAt };
  };
  d.packagesAdded.forEach((pkg) => mark(pkg, 'added'));
  d.packagesChanged.forEach((c) => mark(c.pkg, 'changed'));
  d.packagesRemoved.forEach((pkg) => mark(pkg, 'removed'));
  fs.mkdirSync(path.join(root, DOC_DIR), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(cur, null, 2));
  return Object.keys(cur.packages);
}

function main() {
  const d = diff(root);

  if (flags.has('--apply') && d.hasChanges) {
    writeMaps(root, d.current.navDirs, d.current.packages);
    // delete detail docs for removed packages
    for (const doc of (d.packagesRemoved || [])) {
      const abs = path.join(root, doc === '.' ? '' : doc, DETAIL_FILE);
      try { fs.unlinkSync(abs); } catch {}
    }
    const plan = incrementalPlan(root, d);
    fs.mkdirSync(path.join(root, DOC_DIR), { recursive: true });
    fs.writeFileSync(path.join(root, DOC_DIR, 'plan.json'), JSON.stringify(plan, null, 2));
    // Note: manifest is rewritten only AFTER the agent finishes the detail docs,
    // via `node diff.mjs --commit`. Until then the manifest still reflects the
    // last fully-documented state, so re-running diff stays correct.
  }

  if (flags.has('--commit')) {
    // Call this after detail docs are written to mark the new state as current.
    writeManifest(root, d.curManifest);
  }

  if (flags.has('--pending') && d.hasChanges) {
    mergePending(root, d);
  }

  const report = {
    hasManifest: d.hasManifest,
    hasChanges: d.hasChanges,
    packagesAdded: d.packagesAdded || [],
    packagesRemoved: d.packagesRemoved || [],
    packagesChanged: (d.packagesChanged || []).map((c) => ({
      pkg: c.pkg, added: c.added.length, removed: c.removed.length, modified: c.modified.length,
    })),
    navChanged: d.navChanged || false,
    note: d.note,
  };
  console.log(JSON.stringify(report, null, 2));
}

main();