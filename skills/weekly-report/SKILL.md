---
name: weekly-report
description: Generate a weekly development progress report covering only the days since the last weekly report. Use this when summarizing the week's work or compiling weekly updates.
---

# Weekly Report
1. Determine the date range. Reports never overlap: the range starts the day after the last report's end date and ends yesterday (today is excluded). If no previous report exists, cover the last 7 days. Compute it with:
   ```bash
   python3 ~/.agents/skills/weekly-report/scripts/report_range.py weekly_reports
   ```
   It prints `START END` (e.g. `2026-10-08 2026-10-09`), or `NONE` if every day up to yesterday is already covered — in that case tell the user and stop.
2. Gather the work done between START and END (inclusive):
   - Daily reports in `daily_reports/` whose date falls in the range (`daily_report_YYYY-MM-DD.md`).
   - Git history: `git log --all --since="START 00:00" --until="END 23:59:59" --stat`.
3. Write the report in Markdown and save it as `weekly_reports/weekly_report_START_END.md` in the project (create the directory if needed), e.g. `weekly_report_2026-10-08_2026-10-09.md`.

## Format Requirements
Please strictly follow the Markdown format below:

```markdown
# 📅 Development Weekly Report (START ~ END)

## 💡 Summary
(Use one or two sentences to summarize the period's main outcomes)

## 📝 Detailed Changes

### ✨ New Features
- [Module Name] Details ...

### 🐛 Bug Fixes
- [Module Name] Details ...

### 🔧 Refactoring & Other
- [Module Name] Details ...

## ⚠️ Notes
- Open issues, risks, and follow-ups for next period
```
