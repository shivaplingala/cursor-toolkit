// core.mjs — shared, zero-dependency scanning + manifest logic.
// Runs on any Node >=16. No npm installs required.
//
// Concepts:
//  - "package dir": a directory that DIRECTLY contains a `src/` folder.
//                   It gets a CODE_DETAILS.md describing everything under src/.
//  - "nav dir":     any directory on the path to one or more package dirs.
//                   It gets a CODEBASE_MAP.md pointing to its children.
//  - manifest:      .codedocs/manifest.json — records a content hash for every
//                   source file plus which package/doc covers it, so the updater
//                   can tell exactly what changed.

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export const DOC_DIR = '.codedocs';
export const MANIFEST = path.join(DOC_DIR, 'manifest.json');
export const PENDING = path.join(DOC_DIR, 'pending.json');
export const MAP_FILE = 'CODEBASE_MAP.md';
export const DETAIL_FILE = 'CODE_DETAILS.md';
export const SRC_DIR_NAME = 'src';

export const CODE_EXT = new Set([
  '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.mts', '.cts',
]);

export const IGNORE_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', 'out', '.next', '.nuxt',
  '.svelte-kit', '.astro', '.output', '.vercel', '.netlify', 'coverage',
  '.turbo', '.cache', '.parcel-cache', '.vite', 'tmp', 'temp', '.idea',
  '.vscode', '.DS_Store', DOC_DIR, '.codedocs',
]);

const IGNORE_FILE_SUFFIX = ['.d.ts', '.min.js', '.test.ts', '.test.tsx',
  '.spec.ts', '.spec.tsx', '.test.js', '.spec.js'];

export function sha1(buf) {
  return crypto.createHash('sha1').update(buf).digest('hex').slice(0, 16);
}

function isCodeFile(name) {
  if (IGNORE_FILE_SUFFIX.some((s) => name.endsWith(s))) return false;
  return CODE_EXT.has(path.extname(name));
}

function listDir(abs) {
  let entries;
  try { entries = fs.readdirSync(abs, { withFileTypes: true }); }
  catch { return { dirs: [], files: [] }; }
  const dirs = [];
  const files = [];
  for (const e of entries) {
    if (e.name.startsWith('.') && e.name !== '.codedocs') {
      // skip hidden dirs/files except none we care about
      if (e.isDirectory()) continue;
    }
    if (e.isDirectory()) {
      if (!IGNORE_DIRS.has(e.name)) dirs.push(e.name);
    } else if (e.isFile()) {
      files.push(e.name);
    }
  }
  dirs.sort();
  files.sort();
  return { dirs, files };
}

// Recursively collect code files under a directory (used for a package's src/).
export function collectSrcFiles(root, srcAbs) {
  const out = [];
  const walk = (abs) => {
    const { dirs, files } = listDir(abs);
    for (const f of files) {
      if (isCodeFile(f)) {
        const full = path.join(abs, f);
        let content = '';
        try { content = fs.readFileSync(full); } catch { content = Buffer.from(''); }
        out.push({
          rel: path.relative(root, full).split(path.sep).join('/'),
          hash: sha1(content),
          bytes: content.length,
          lines: content.toString('utf8').split('\n').length,
        });
      }
    }
    for (const d of dirs) walk(path.join(abs, d));
  };
  walk(srcAbs);
  out.sort((a, b) => a.rel.localeCompare(b.rel));
  return out;
}

function readPkgMeta(absDir) {
  const p = path.join(absDir, 'package.json');
  try {
    const j = JSON.parse(fs.readFileSync(p, 'utf8'));
    return { name: j.name || null, description: j.description || null };
  } catch { return { name: null, description: null }; }
}

// Walk the whole tree. Returns { packages: [...], navDirs: [...] }.
// A nav dir is any dir that contains (transitively) at least one package dir.
export function scan(root) {
  const packages = [];          // { dir, src, meta, files }
  const navChildren = new Map(); // navDir(rel) -> { dirs:Set, isPackage:bool }

  const rel = (abs) => {
    const r = path.relative(root, abs).split(path.sep).join('/');
    return r === '' ? '.' : r;
  };

  // returns true if `abs` leads to at least one package
  const walk = (abs) => {
    const { dirs } = listDir(abs);
    const hasSrc = dirs.includes(SRC_DIR_NAME);
    const relDir = rel(abs);
    let leadsToPkg = false;

    if (hasSrc) {
      const srcAbs = path.join(abs, SRC_DIR_NAME);
      const files = collectSrcFiles(root, srcAbs);
      packages.push({
        dir: relDir,
        src: rel(srcAbs),
        meta: readPkgMeta(abs),
        files,
      });
      leadsToPkg = true;
    }

    const childPkgDirs = [];
    for (const d of dirs) {
      if (d === SRC_DIR_NAME) continue; // src handled as package contents
      const childAbs = path.join(abs, d);
      if (walk(childAbs)) {
        leadsToPkg = true;
        childPkgDirs.push(d);
      }
    }

    if (leadsToPkg) {
      navChildren.set(relDir, {
        dirs: childPkgDirs,
        isPackage: hasSrc,
        meta: hasSrc ? readPkgMeta(abs) : { name: null, description: null },
      });
    }
    return leadsToPkg;
  };

  walk(root);

  const navDirs = [...navChildren.entries()]
    .map(([dir, v]) => ({ dir, children: v.dirs, isPackage: v.isPackage, meta: v.meta }))
    .sort((a, b) => a.dir.localeCompare(b.dir));

  packages.sort((a, b) => a.dir.localeCompare(b.dir));
  return { packages, navDirs };
}

function escapeCell(s) {
  return String(s).replace(/\|/g, '\\|').replace(/\n/g, ' ').slice(0, 160);
}

// Writes CODEBASE_MAP.md at the root and every nav dir that has child folders.
// Leaf packages get no map (they only need CODE_DETAILS.md). Pure structure —
// safe to re-run any time.
export function writeMaps(root, navDirs, packages) {
  const pkgByDir = new Map(packages.map((p) => [p.dir, p]));
  const navByDir = new Map(navDirs.map((n) => [n.dir, n]));
  const written = [];

  for (const nav of navDirs) {
    if (nav.children.length === 0) continue;
    const absDir = path.join(root, nav.dir === '.' ? '' : nav.dir);
    const lines = [];
    const title = nav.dir === '.' ? path.basename(root) : nav.dir;
    lines.push(`# Codebase Map: ${title}`);
    lines.push('');
    lines.push('> Navigation file. Lists the child folders under this directory that contain code,');
    lines.push('> and where to look next. Generated by codebase-doc tooling — do not hand-edit the');
    lines.push('> structural lists; the updater rewrites them.');
    lines.push('');

    if (nav.isPackage) {
      const p = pkgByDir.get(nav.dir);
      const desc = p?.meta?.description ? ` — ${p.meta.description}` : '';
      lines.push(`**This folder is itself a package${p?.meta?.name ? ` (\`${p.meta.name}\`)` : ''}.**${desc}`);
      lines.push(`Detailed code reference for this folder: [\`${DETAIL_FILE}\`](./${DETAIL_FILE})`);
      lines.push('');
    }

    lines.push('## Child folders');
    lines.push('');
    lines.push('| Folder | What it is | Look here for |');
    lines.push('| --- | --- | --- |');
    for (const child of nav.children) {
      const childRel = nav.dir === '.' ? child : `${nav.dir}/${child}`;
      const childPkg = pkgByDir.get(childRel);
      const childNav = navByDir.get(childRel);
      if (childPkg) {
        const kind = childPkg.meta?.description
          || (childPkg.meta?.name ? `package \`${childPkg.meta.name}\`` : 'package');
        lines.push(`| [\`${child}/\`](./${child}/${DETAIL_FILE}) | ${escapeCell(kind)} | functions, classes, types → \`${DETAIL_FILE}\` |`);
      } else {
        const n = childNav?.children.length || 0;
        lines.push(`| [\`${child}/\`](./${child}/${MAP_FILE}) | folder with ${n} code sub-folder${n === 1 ? '' : 's'} | its own \`${MAP_FILE}\` |`);
      }
    }
    lines.push('');
    fs.writeFileSync(path.join(absDir, MAP_FILE), lines.join('\n') + '\n');
    written.push(path.posix.join(nav.dir === '.' ? '' : nav.dir, MAP_FILE));
  }
  return written;
}

export function loadManifest(root) {
  try {
    return JSON.parse(fs.readFileSync(path.join(root, MANIFEST), 'utf8'));
  } catch { return null; }
}

export function buildManifest(root, { packages, navDirs }) {
  const files = {};
  const pkgs = {};
  for (const p of packages) {
    pkgs[p.dir] = {
      src: p.src,
      detailDoc: path.posix.join(p.dir === '.' ? '' : p.dir, DETAIL_FILE),
      name: p.meta.name,
      description: p.meta.description,
      fileCount: p.files.length,
    };
    for (const f of p.files) {
      files[f.rel] = { hash: f.hash, pkg: p.dir };
    }
  }
  return {
    schema: 1,
    generatedAt: new Date().toISOString(),
    navDirs: (navDirs || []).map((n) => ({ dir: n.dir, children: n.children })),
    packages: pkgs,
    files,
  };
}

export function writeManifest(root, manifest) {
  const dir = path.join(root, DOC_DIR);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(root, MANIFEST), JSON.stringify(manifest, null, 2));
}