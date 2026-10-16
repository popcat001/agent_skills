---
name: repo-dashboard
description: Create or update a repo dashboard artifact with a changelog of major features. Use when the user asks to create, update, refresh, or republish a repo or project dashboard, or after a major feature ships in a project that already has one.
---

# Repo dashboard

A single-page dashboard for a repo, published as a Claude artifact and saved in the repo (default `docs/dashboard/`). Its core is an **Updates** changelog of major features.

## Create

Create a dashboard artifact for this repo. Look at the project first and choose sections that fit it, for example headline stats, recent activity, a list of its main components, and the Updates changelog. Save the file in the repo, publish it, and put the artifact link in an HTML comment at the top of the file so later runs can find it.

Updates requirements:
- Major features only, not every detail. Leave out bug fixes, refactors, doc or test commits, UI polish, and dependency bumps.
- One sentence per entry, saying what the feature does for the user.
- Grouped by month, newest first, with a date and an area tag.
- Expandable and collapsible, with expand all and collapse all.
- Build it from the full git history, including any submodules, not a sample.

## Update

Find the existing dashboard file and its artifact link. Add the new major feature to Updates under the right month, following the same requirements, and refresh any stats or component lists the change affects. Republish to the same artifact link.

## Always

Do not commit the file without asking.
