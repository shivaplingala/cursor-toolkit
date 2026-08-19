# Knowledge capture (FCD + FCD-V2)

**Owner:** main / orchestrator (or **qa-engineer** for QA-only lessons).  
**Corpus:** `$FCD_ROOT/knowledge/` (shared by `/full-cycle-delivery` and `/fcd-v2`).

## When (mandatory)

1. **Phase 7** before claiming ship-ready / after PR opened  
2. When the human **stops** a delivery with meaningful implement/debug work (even mid-phase)  
3. After a **novel** failure mode is solved (don’t wait for Phase 7 if the lesson is sharp)

## When (optional mid-flight)

After a non-obvious build/debug/fix/perf win during Phase 4–6 — capture one bullet so the next chat benefits.

## Steps

1. Read `knowledge/INDEX.md` and the topic file(s) you will touch.
2. Extract **durable** lessons only:
   - how to **build** (patterns, wiring, host install)
   - how to **debug** (symptoms → checks)
   - how to **fix** (what actually cleared findings/QA)
   - how to fix **performance** (runtime, tokens, CI time)
   - **qa** / **swarm** if applicable
3. Append under today’s date in `knowledge/log.md`:
   ```markdown
   ## YYYY-MM-DD
   - <lesson> (context: <slug or work type>)
   ```
4. Merge into the matching topic file as a plain bullet (dedupe; rewrite in place if refining).
5. If a topic file exceeds **40** bullets → distill (merge duplicates / drop obsolete) then add.
6. Note in **progress.md** history: `knowledge: captured N bullets → build|debug|fix|performance|qa|swarm`.
7. Do **not** put secrets, tokens, phone numbers, or customer data in the corpus.

## Output

```text
KNOWLEDGE: captured | none-new
TOPICS: …
LOG: knowledge/log.md ## <date>
PROGRESS: history line added
```

## Forbidden

- Skipping capture after Phase 7 when any Phase 4+ work happened
- Duplicating the same lesson every run
- Replacing workspace `AGENTS.md` product facts with delivery craft (keep DOX for product; corpus for FCD craft)
