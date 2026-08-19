// watch.mjs — background file watcher (skill 3).
//
// Watches the repo for added/changed/deleted source files. On a debounced
// batch of changes it runs the diff engine to update .codedocs/pending.json
// (the queue of packages whose CODE_DETAILS.md is now stale). If an agent
// command is configured, it also invokes it so docs refresh unattended.
//
// Zero dependencies. Works on Linux/macOS/Windows (manual recursive watching,
// so it does not rely on fs.watch recursive support).
//
// Config (optional): .codedocs/watch.config.json
//   { "debounceMs": 800, "agentCommand": null }
// agentCommand example (Claude Code):
//   "claude -p 'Run the codebase-doc-updater skill to refresh stale docs'"
//
// Usage: node .codedocs/watch.mjs [rootDir]

import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { IGNORE_DIRS, DOC_DIR, CODE_EXT } from './core.mjs';

const root = path.resolve(process.argv[2] || process.cwd());
const cfgPath = path.join(root, DOC_DIR, 'watch.config.json');
let cfg = { debounceMs: 800, agentCommand: null };
try { cfg = { ...cfg, ...JSON.parse(fs.readFileSync(cfgPath, 'utf8')) }; } catch {}

const watchers = new Map();
let timer = null;
let running = false;
let dirtyAgain = false;

function shouldWatch(name) { return !IGNORE_DIRS.has(name) && !(name.startsWith('.') && name !== '.codedocs'); }
function isCode(name) { return CODE_EXT.has(path.extname(name)); }

function watchDir(abs) {
  if (watchers.has(abs)) return;
  let w;
  try {
    w = fs.watch(abs, (event, filename) => {
      if (!filename) { scheduleRun(); return; }
      const full = path.join(abs, filename);
      // new directory appeared → start watching it
      try {
        if (fs.existsSync(full) && fs.statSync(full).isDirectory() && shouldWatch(filename)) {
          addTree(full);
        }
      } catch {}
      if (isCode(filename) || event === 'rename') scheduleRun();
    });
  } catch { return; }
  watchers.set(abs, w);
}

function addTree(abs) {
  watchDir(abs);
  let entries = [];
  try { entries = fs.readdirSync(abs, { withFileTypes: true }); } catch { return; }
  for (const e of entries) {
    if (e.isDirectory() && shouldWatch(e.name)) addTree(path.join(abs, e.name));
  }
}

function scheduleRun() {
  if (timer) clearTimeout(timer);
  timer = setTimeout(run, cfg.debounceMs);
}

function run() {
  if (running) { dirtyAgain = true; return; }
  running = true;
  const diffPath = path.join(root, DOC_DIR, 'diff.mjs');
  const p = spawn(process.execPath, [diffPath, root, '--pending'], { cwd: root });
  let out = '';
  p.stdout.on('data', (d) => { out += d; });
  p.on('close', () => {
    try {
      const r = JSON.parse(out);
      if (r.hasChanges) {
        const stale = [
          ...r.packagesAdded, ...r.packagesRemoved,
          ...r.packagesChanged.map((c) => c.pkg),
        ];
        log(`changes detected → ${stale.join(', ') || 'structure'} (queued in .codedocs/pending.json)`);
        if (cfg.agentCommand) invokeAgent();
      }
    } catch { /* diff printed nothing parseable */ }
    running = false;
    if (dirtyAgain) { dirtyAgain = false; scheduleRun(); }
  });
}

function invokeAgent() {
  log(`invoking agent: ${cfg.agentCommand}`);
  const child = spawn(cfg.agentCommand, { cwd: root, shell: true, stdio: 'inherit' });
  child.on('close', (code) => log(`agent finished (exit ${code})`));
}

function log(msg) {
  console.log(`[codebase-doc-watcher ${new Date().toLocaleTimeString()}] ${msg}`);
}

log(`watching ${root} (debounce ${cfg.debounceMs}ms, agent: ${cfg.agentCommand ? 'on' : 'off'})`);
addTree(root);
process.on('SIGINT', () => { log('stopped'); process.exit(0); });