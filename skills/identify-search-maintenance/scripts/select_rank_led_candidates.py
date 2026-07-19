#!/usr/bin/env python3
"""Screen normalized Search Console page data for rank-led traffic-loss candidates."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path
from typing import Iterable, TextIO

REQUIRED_COLUMNS = (
    "url",
    "current_clicks",
    "previous_clicks",
    "current_impressions",
    "previous_impressions",
    "current_position",
    "previous_position",
)


def parse_number(value: str, column: str, row_number: int) -> float:
    try:
        number = float(value.replace(",", "").strip())
    except (AttributeError, ValueError) as error:
        raise ValueError(
            f"Row {row_number}: {column} must be numeric, got {value!r}."
        ) from error
    if not math.isfinite(number):
        raise ValueError(f"Row {row_number}: {column} must be finite, got {value!r}.")
    if (column.endswith("clicks") or column.endswith("impressions")) and number < 0:
        raise ValueError(
            f"Row {row_number}: {column} cannot be negative, got {value!r}."
        )
    if column.endswith("position") and number <= 0:
        raise ValueError(
            f"Row {row_number}: {column} must be greater than zero, got {value!r}."
        )
    return number


def percentage_change(current: float, previous: float) -> float:
    return (current - previous) / previous


def read_rows(stream: TextIO) -> Iterable[dict[str, str]]:
    reader = csv.DictReader(stream)
    if reader.fieldnames is None:
        raise ValueError("Input CSV has no header row.")

    reader.fieldnames[0] = reader.fieldnames[0].lstrip("\ufeff")
    missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
    if missing:
        raise ValueError(
            f"Input CSV is missing required columns: {', '.join(missing)}."
        )

    return reader


def select_candidates(
    rows: Iterable[dict[str, str]],
    min_previous_clicks: float,
    max_click_change: float,
    max_absolute_impression_change: float,
    min_position_worsening: float,
    min_click_gap_vs_impressions: float,
) -> list[dict[str, float | str]]:
    candidates: list[dict[str, float | str]] = []
    seen_urls: set[str] = set()
    for row_number, row in enumerate(rows, start=2):
        url = row["url"].strip()
        if not url:
            raise ValueError(f"Row {row_number}: url cannot be empty.")
        if url in seen_urls:
            raise ValueError(
                f"Row {row_number}: duplicate url {url!r}; aggregate the export first."
            )
        seen_urls.add(url)
        values = {
            column: parse_number(row[column], column, row_number)
            for column in REQUIRED_COLUMNS[1:]
        }
        previous_clicks = values["previous_clicks"]
        previous_impressions = values["previous_impressions"]
        if previous_clicks <= 0 or previous_impressions <= 0:
            continue

        click_change = percentage_change(values["current_clicks"], previous_clicks)
        impression_change = percentage_change(
            values["current_impressions"], previous_impressions
        )
        position_worsening = values["current_position"] - values["previous_position"]
        click_gap_vs_impressions = impression_change - click_change

        if (
            previous_clicks >= min_previous_clicks
            and click_change <= max_click_change
            and abs(impression_change) <= max_absolute_impression_change
            and position_worsening >= min_position_worsening
            and click_gap_vs_impressions >= min_click_gap_vs_impressions
        ):
            candidates.append(
                {
                    "url": url,
                    "current_clicks": values["current_clicks"],
                    "previous_clicks": previous_clicks,
                    "click_change": click_change,
                    "current_impressions": values["current_impressions"],
                    "previous_impressions": previous_impressions,
                    "impression_change": impression_change,
                    "current_position": values["current_position"],
                    "previous_position": values["previous_position"],
                    "position_worsening": position_worsening,
                    "click_gap_vs_impressions": click_gap_vs_impressions,
                }
            )

    return sorted(
        candidates,
        key=lambda candidate: (
            float(candidate["previous_clicks"]) - float(candidate["current_clicks"])
        ),
        reverse=True,
    )


def percentage(value: float) -> str:
    return f"{value * 100:.1f}%"


def markdown(candidates: Iterable[dict[str, float | str]]) -> str:
    lines = [
        "| URL | Clicks (current / previous) | Click change | Impressions change | Position worsening |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for candidate in candidates:
        lines.append(
            "| {url} | {current_clicks:.0f} / {previous_clicks:.0f} | {click_change} | {impression_change} | {position_worsening:+.1f} |".format(
                url=candidate["url"],
                current_clicks=float(candidate["current_clicks"]),
                previous_clicks=float(candidate["previous_clicks"]),
                click_change=percentage(float(candidate["click_change"])),
                impression_change=percentage(float(candidate["impression_change"])),
                position_worsening=float(candidate["position_worsening"]),
            )
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input", help="Normalized CSV path, or - to read CSV from standard input."
    )
    parser.add_argument("--min-previous-clicks", type=float, default=100)
    parser.add_argument("--max-click-change", type=float, default=-0.20)
    parser.add_argument("--max-absolute-impression-change", type=float, default=0.25)
    parser.add_argument("--min-position-worsening", type=float, default=0.5)
    parser.add_argument("--min-click-gap-vs-impressions", type=float, default=0.10)
    parser.add_argument("--format", choices=("markdown", "csv"), default="markdown")
    arguments = parser.parse_args()

    try:
        if arguments.input == "-":
            candidates = select_candidates(
                read_rows(sys.stdin),
                arguments.min_previous_clicks,
                arguments.max_click_change,
                arguments.max_absolute_impression_change,
                arguments.min_position_worsening,
                arguments.min_click_gap_vs_impressions,
            )
        else:
            with Path(arguments.input).open(
                encoding="utf-8-sig", newline=""
            ) as input_file:
                candidates = select_candidates(
                    read_rows(input_file),
                    arguments.min_previous_clicks,
                    arguments.max_click_change,
                    arguments.max_absolute_impression_change,
                    arguments.min_position_worsening,
                    arguments.min_click_gap_vs_impressions,
                )
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))

    if arguments.format == "markdown":
        print(markdown(candidates))
        return 0

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=(
            "url",
            *REQUIRED_COLUMNS[1:],
            "click_change",
            "impression_change",
            "position_worsening",
            "click_gap_vs_impressions",
        ),
    )
    writer.writeheader()
    writer.writerows(candidates)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
