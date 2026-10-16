#!/usr/bin/env python3
"""Print the date range the next weekly report should cover.

Start = day after the end date of the latest weekly_report_<start>_<end>.md in the
reports directory (or today - 7 days if none exist). End = yesterday.
Output: "<start> <end>" (ISO dates), or "NONE" if there are no uncovered days.
"""
import re
import sys
from datetime import date, timedelta
from pathlib import Path

PATTERN = re.compile(r"^weekly_report_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})\.md$")


def report_range(reports_dir: Path, today: date) -> tuple[date, date] | None:
    ends = [
        date.fromisoformat(m.group(2))
        for p in (reports_dir.iterdir() if reports_dir.is_dir() else [])
        if (m := PATTERN.match(p.name))
    ]
    start = max(ends) + timedelta(days=1) if ends else today - timedelta(days=7)
    end = today - timedelta(days=1)
    return (start, end) if start <= end else None


if __name__ == "__main__":
    reports_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "weekly_reports")
    today = date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else date.today()
    r = report_range(reports_dir, today)
    print(f"{r[0]} {r[1]}" if r else "NONE")
