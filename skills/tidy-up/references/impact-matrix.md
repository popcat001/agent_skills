# Impact matrix

Maps a changed file (Phase 1 inventory) to the layers that could need reconciliation. Use it to prune the plan: if a row says "skip", do not propose edits in that layer for that change type. Layers: **MEM** = memory (`~/.claude/memory/`, project memory dir), **ROOT** = `CLAUDE.md` / `AGENTS.md`, **DOCS** = `README.md`, `docs/`.

| Change type | Example paths | MEM | ROOT | DOCS |
|---|---|---|---|---|
| New public API / CLI surface | `src/api/*`, `cli/*`, exported modules | check `reference_*` for stale signatures | update if it changes "how to run" | update README usage, `docs/api/` |
| Internal refactor (no API change) | rename, file move, extract function | check `project_*` "Key Files" tables | update path references only | skip unless docs cite the old path |
| Bug fix | one-off patch | add `feedback_*` if it encodes a "don't do X" lesson, else skip | skip | skip |
| New constraint / gotcha discovered | "X breaks when Y" | **add `feedback_*` with `Why:` and `How to apply:`** | skip | skip |
| Dependency / tooling change | `package.json`, `pyproject.toml`, `uv.lock` | update `project_*` env section | update if "how to install/run" changed | update README setup |
| Config / env var | `.env.example`, settings | update `project_*` env section | update if user-facing | update README config section |
| Test-only change | `tests/*`, `*_test.*` | skip | skip | skip |
| Doc-only change | `README.md`, `docs/*`, comments | skip | skip | the change IS the doc — verify only |
| Schema / data model | migrations, types | check `reference_*` schemas | update if root-level schema doc lives there | update `docs/schema/` |
| Removed feature | deletion of module/endpoint | flag `reference_*` and `feedback_*` mentions as REVIEW (do not auto-delete incident notes) | remove usage instructions | remove from README, archive in `docs/` |
| Workflow / process change | CI, hooks, commit conventions | update `user_*` or `project_*` workflow rules | update root if agents need to follow it | update CONTRIBUTING |
| Plan / scratch file | `plan_*.md`, notes | skip all layers — these are session artifacts | skip | skip |

## Notes

- "check" means read the file and confirm nothing is stale; do not edit unless something actually drifted.
- A single change can touch multiple rows — union the layers.
- If a change does not match any row, default to MEM=check, ROOT=skip, DOCS=skip and ask the user whether wider reconciliation is wanted.
