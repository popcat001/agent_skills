---
name: tidy-up
description: "Reconcile memory and docs after a long Codex session. Use ONLY when the user explicitly invokes it via `/tidy`, `run tidy-up`, or a phrase like \"clean up docs and memory before I stop\". NEVER auto-trigger on casual phrases like \"tidy\", \"clean up\", \"sync\", or \"wrap up\" — this skill makes targeted edits to persistent state and requires explicit invocation."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# tidy-up

Reconciles three layers of persistent state after a working session so they stop drifting from the code: (1) **memory** — the silent layer at `~/.Codex/memory/` and `~/.Codex/projects/<encoded-cwd>/memory/` (MEMORY.md + typed `user_*`, `feedback_*`, `project_*`, `reference_*` files); (2) **project root** — visible repo files like `AGENTS.md` and `AGENTS.md`; (3) **external docs** — `README.md`, `docs/`, anything humans read. Concept credit: the public `neat-freak` skill. This skill is a stricter, dry-run-first reimplementation. It does not auto-execute, does not enumerate the whole tree, and has a strong bias toward keeping content rather than deleting it.

## When to invoke

Run only on explicit user request. Do not infer it from "tidy", "clean up", "sync", or end-of-session pleasantries — those are too ambiguous and the cost of a wrong edit (lost rationale in a memory file, a doc rewrite the user did not want) is high.

## Workflow

The skill runs in five phases. Phases 2 and 4 are approval gates — stop and wait for explicit "approved" / "go" before continuing.

### Phase 1 — Inventory (bounded scope)

Determine the change set. Default scope is files modified during the current session, nothing else. Discovery order:

1. If in a git repo and a session-start commit is known (ask the user for the SHA, or use `git log -1 --before="<session start>"` heuristically), run `git diff --name-status <session-start>..HEAD` plus `git status --short` to capture committed and uncommitted changes.
2. If no session-start commit is available, fall back to `git status --short` plus `git diff --name-status HEAD` — uncommitted work only.
3. If not in a repo, ask the user for the file list. Do not scan the directory.

Anything outside this set is out of scope. If the user wants to reconcile a wider set ("also check docs/architecture/"), they must opt in explicitly and you add only the named paths.

Before proceeding to the impact matrix, show the resulting file list to the user and ask "is this the session change set?" When `git status --short` is the source, unrelated uncommitted work may be present — let the user prune it. If the inventory is empty, report "nothing to reconcile" and stop.

Then read `references/impact-matrix.md` to map each changed file to which memory/doc layers it could affect. Skip layers the matrix marks as unaffected.

### Phase 2 — Plan (dry-run, approval gate)

Produce a single markdown plan with two clearly separated sections — **Memory pass** and **Doc pass** — and within each, three buckets: **UPDATE**, **ADD**, **DELETE**. Each entry is one line: target path, one-sentence rationale, and a diff sketch (before → after, ≤2 lines each). Group `DELETE` candidates last and visually separate them; they require their own confirmation even if the rest is approved.

Deletion bias is conservative. Default for ambiguous content is **KEEP**. Only propose `DELETE` when one of these holds: (a) a newer entry in the same file or sibling file demonstrably supersedes it, (b) the content contradicts the current code (cite the code line), or (c) the user explicitly named it for removal. Never propose deleting entries that record incidents, postmortems, constraints, or "why we don't do X" reasoning, even if they look stale — flag those as **REVIEW** and let the user decide.

When rewriting, preserve the "why". `Why:` and `How to apply:` lines in `feedback_*` and `project_*` memories must survive any edit. Do not collapse relative phrasing ("two weeks before launch freeze", "after the v3 cutover") into absolute dates unless the user confirms the relative meaning is gone — flag as **REVIEW** instead.

Output the plan, then stop. Wait for user approval. The user may approve all, approve UPDATE/ADD only, or approve item-by-item. Honor whichever they choose.

### Phase 3 — Memory pass (silent layer)

Execute only the approved memory edits. Targets:

- `~/.Codex/memory/` — global user memory (cross-project preferences, workflow rules).
- `~/.Codex/projects/<encoded-cwd>/memory/` — project memory. The encoded directory replaces `/` with `-`, so `/Users/foo/bar` → `-Users-foo-bar`. Pick the directory that matches the current project's cwd; if multiple plausible candidates exist, ask.

Inside each memory dir, edit the typed files (`MEMORY.md`, `user_*.md`, `feedback_*.md`, `project_*.md`, `reference_*.md`) directly. These are silent — no git trace — so do not bundle them with doc edits, and do not include them in any git staging or commit you make for the doc pass. After edits, re-read each touched file once and verify the `Why:` / `How to apply:` lines are still intact; if any were dropped, restore them.

### Phase 4 — Doc plan reconfirm (approval gate)

Re-show the **Doc pass** section of the plan. Memory edits may have changed your understanding (e.g., a memory rewrite revealed a constraint that makes a proposed README change wrong). Ask the user to reconfirm the doc edits before touching tracked files. Do not skip this gate even if Phase 2 was approved wholesale.

### Phase 5 — Doc pass (visible layer)

Execute only the reconfirmed doc edits. Targets in priority order: `AGENTS.md` / `AGENTS.md` at the project root, then `README.md`, then files under `docs/`. Edits are visible in `git diff` — leave them unstaged unless the user asks you to stage or commit. Report a summary at the end: file paths touched, count of UPDATE/ADD/DELETE per pass, anything left in REVIEW that the user should look at later.

## Hard rules

- No auto-execute path. Phases 2 and 4 are mandatory stops.
- Memory and doc passes never share an approval. Two gates, two confirmations.
- Default scope is the session's changed files. Wider scope requires explicit opt-in with named paths.
- When in doubt, KEEP. Flag as REVIEW rather than DELETE.
- Preserve `Why:` and `How to apply:` lines verbatim across rewrites.
- Do not stage or commit doc edits unless asked.
- If the user declines, gives ambiguous feedback, or does not respond with explicit approval at any gate, abort cleanly: report "no changes made" and exit. Never proceed on partial or implied approval.
