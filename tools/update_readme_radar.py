#!/usr/bin/env python3
"""Refresh only the bounded latest-research section of the repository README.

Dates refer to Europe/Paris research report dates, never product launch dates.
This script does not approve or publish product candidates.
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

START = "<!-- DAILY_RADAR_START -->"
END = "<!-- DAILY_RADAR_END -->"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def generate(root: Path, limit: int = 7) -> str:
    reports = sorted(root.glob("reports/[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"), reverse=True)
    valid = [(p.stem, p) for p in reports if DATE_RE.fullmatch(p.stem)][:limit]
    if not valid:
        raise ValueError("No dated reports found; refusing to replace the README section")
    by_date = {}
    index = root / "index/products.csv"
    if index.exists():
        with index.open(encoding="utf-8", newline="") as f:
            for item in csv.DictReader(f):
                date = item.get("first_observed", "")
                name = item.get("name", "").replace("|", "/").replace("\n", " ").strip()
                if DATE_RE.fullmatch(date) and name:
                    by_date.setdefault(date, []).append(name)
    latest, latest_path = valid[0]
    lines = [
        START,
        "## 🛰️ Latest research / 最新研究 / Dernières recherches",
        "",
        f"**Latest: {latest} (Europe/Paris)** · [中文深度报告]({latest_path.as_posix()}) · [All reports / 全部日报](reports/README.md)",
        "",
        "> **研究提醒：** 本栏目按报告观察日期排列，**不代表产品首次发布日期**。产品榜单、创始人主张和融资不等于留存或 PMF；请阅读报告中的原始证据与反面证据。",
        "",
        "| Date (Paris) | Featured research (observed products) | Full report |",
        "| --- | --- | --- |",
    ]
    for date, path in valid:
        names = by_date.get(date, [])
        label = " · ".join(names[:4]) + (" · …" if len(names) > 4 else "") if names else "Research report (see evidence and limitations)"
        lines.append(f"| {date} | {label} | [Read]({path.as_posix()}) |")
    lines += [
        "",
        "**Browse:** [Product profiles / 产品档案](products/) · [Insights / 需求洞察](insights/) · [Structured index / 产品索引](index/products.csv) · [Methodology / 研究方法](METHODOLOGY.md)",
        "",
        "*Reports are public research; staged product candidates are **not** automatically published as verified launches.*",
        "",
        END,
    ]
    return "\n".join(lines)


def update(root: Path, check: bool = False) -> bool:
    path = root / "README.md"
    original = path.read_text(encoding="utf-8")
    if original.count(START) != 1 or original.count(END) != 1:
        raise ValueError("README markers missing or duplicated; refusing to overwrite")
    a = original.index(START)
    b = original.index(END, a) + len(END)
    new = original[:a] + generate(root) + original[b:]
    if new != original and not check:
        path.write_text(new, encoding="utf-8")
    return new != original


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = update(args.root, args.check)
    print("README needs refresh" if changed else "README already current")
    if args.check and changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
