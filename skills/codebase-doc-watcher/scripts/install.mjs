// install.mjs — wires the auto-update system into a repo (skill 3).
//
// Makes the docs self-maintaining without the skill bundle present, by copying
// the small runtime into <repo>/.codedocs/ and installing triggers.
//
// Usage:
//   node install.mjs [rootDir] [--hook=post-commit|pre-commit] [--no-agent-rules]
//
// What it installs:
//   - <repo>/.codedocs/{core.mjs,diff.mjs,watch.mjs}  (runtime, zero deps)
//   - <repo>/.codedocs/watch.config.json              (debounce + optional agent cmd)
//   - git hook that runs `node .codedocs/diff.mjs --pending` on commit
//   - agent-rule files so Cursor / Claude / Codex refresh stale docs:
//       .cursor/rules/codebase-docs.mdc, CLAUDE.md (appended), AGENTS.md (appended)
//   - .gitignore entries for pending.json / watcher pid

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const root = path.resolve(args.find((a) => !a.startsWith('--')) || process.cwd());
const hookArg = (args.find((a) => a.startsWith('--hook=')) || '--hook=post-commit').split('=')[1];
const noAgentRules = args.includes('--no-agent-rules');

const assets = path.resolve(here, '..', 'assets');
const docDir = path.join(root, '.codedocs');
fs.mkdirSync(docDir, { recursive: true });

function copyInto(srcFile, destFile) {
  fs.copyFileSync(srcFile, destFile);
  console.log('  wrote ' + path.relative(root, destFile));
}

// 1. Runtime scripts. core.mjs + diff.mjs come from the updater; watch.mjs is local.
copyInto(path.join(here, 'core.mjs'), path.join(docDir, 'core.mjs'));
copyInto(path.join(here, 'diff.mjs'), path.join(docDir, 'diff.mjs'));
copyInto(path.join(here, 'watch.mjs'), path.join(docDir, 'watch.mjs'));

// 2. watch config (only if absent — don't clobber user edits)
const cfgPath = path.join(docDir, 'watch.config.json');
if (!fs.existsSync(cfgPath)) {
  fs.writeFileSync(cfgPath, JSON.stringify({ debounceMs: 800, agentCommand: null }, null, 2) + '\n');
  console.log('  wrote ' + path.relative(root, cfgPath));
}

// 3. git hook
const gitDir = path.join(root, '.git');
if (fs.existsSync(gitDir)) {
  const hookPath = path.join(gitDir, 'hooks', hookArg);
  const marker = '# >>> codebase-doc-watcher >>>';
  const block = [
    marker,
    'if command -v node >/dev/null 2>&1 && [ -f .codedocs/diff.mjs ]; then',
    '  node .codedocs/diff.mjs --pending >/dev/null 2>&1 || true',
    'fi',
    '# <<< codebase-doc-watcher <<<',
  ].join('\n');
  let existing = '';
  try { existing = fs.readFileSync(hookPath, 'utf8'); } catch {}
  if (!existing.includes(marker)) {
    const content = existing
      ? existing.replace(/\n*$/, '\n\n') + block + '\n'
      : '#!/bin/sh\n' + block + '\n';
    fs.mkdirSync(path.dirname(hookPath), { recursive: true });
    fs.writeFileSync(hookPath, content);
    fs.chmodSync(hookPath, 0o755);
    console.log('  installed git ' + hookArg + ' hook');
  } else {
    console.log('  git ' + hookArg + ' hook already present');
  }
} else {
  console.log('  (no .git dir — skipped git hook)');
}

// 4. agent rules
if (!noAgentRules) {
  // Cursor
  const cursorDir = path.join(root, '.cursor', 'rules');
  fs.mkdirSync(cursorDir, { recursive: true });
  copyInto(path.join(assets, 'cursor-rule.mdc'), path.join(cursorDir, 'codebase-docs.mdc'));

  // Claude + Codex: append a managed block to CLAUDE.md and AGENTS.md
  const ruleBody = fs.readFileSync(path.join(assets, 'agent-rule.md'), 'utf8');
  for (const fname of ['CLAUDE.md', 'AGENTS.md']) {
    appendManagedBlock(path.join(root, fname), ruleBody);
  }
}

// 5. .gitignore
appendGitignore(path.join(root, '.gitignore'), [
  '.codedocs/pending.json',
  '.codedocs/*.pid',
]);

console.log('\nDone. Commit .codedocs/{core,diff,watch}.mjs and the agent-rule files so');
console.log('teammates and CI get the same behaviour. Start the live watcher with:');
console.log('  node .codedocs/watch.mjs');

function appendManagedBlock(file, body) {
  const start = '<!-- codebase-doc-watcher:start -->';
  const end = '<!-- codebase-doc-watcher:end -->';
  let existing = '';
  try { existing = fs.readFileSync(file, 'utf8'); } catch {}
  const block = `${start}\n${body.trim()}\n${end}`;
  let next;
  if (existing.includes(start) && existing.includes(end)) {
    next = existing.replace(new RegExp(start + '[\\s\\S]*?' + end), block);
  } else {
    next = (existing ? existing.replace(/\n*$/, '\n\n') : '') + block + '\n';
  }
  fs.writeFileSync(file, next);
  console.log('  updated ' + path.relative(root, file));
}

function appendGitignore(file, entries) {
  let existing = '';
  try { existing = fs.readFileSync(file, 'utf8'); } catch {}
  const missing = entries.filter((e) => !existing.split('\n').includes(e));
  if (!missing.length) return;
  const next = (existing ? existing.replace(/\n*$/, '\n') : '')
    + '\n# codebase-doc-watcher\n' + missing.join('\n') + '\n';
  fs.writeFileSync(file, next);
  console.log('  updated .gitignore');
}