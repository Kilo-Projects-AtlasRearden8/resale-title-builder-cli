"""Command-line interface for the resale title builder."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

from .builder import (
    DEFAULT_MARKETPLACE,
    MARKETPLACE_LIMITS,
    BuildResult,
    ListingAttributes,
    build_title,
    keyword_hints,
)

LOG_HEADER = [
    "timestamp",
    "marketplace",
    "title",
    "length",
    "limit",
    "over_limit",
    "overflow",
]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="resale-title-builder",
        description=(
            "Build eBay/Amazon listing titles from item attributes. "
            "Local-first: no accounts, API keys, or network calls required."
        ),
    )
    parser.add_argument("--brand", default="", help="Brand name (e.g. Nike)")
    parser.add_argument("--model", default="", help="Model number or name (e.g. Air Max)")
    parser.add_argument("--item", default="", help="Item name (e.g. sneakers)")
    parser.add_argument("--condition", default="", help="Condition (e.g. Used, New)")
    parser.add_argument("--size", default="", help="Size (e.g. 10, M)")
    parser.add_argument("--color", default="", help="Color (e.g. Black)")
    parser.add_argument("--quantity", default="", help="Quantity (e.g. 1, Lot of 5)")
    parser.add_argument(
        "--marketplace",
        default=DEFAULT_MARKETPLACE,
        choices=sorted(MARKETPLACE_LIMITS),
        help=f"Target marketplace for the character limit (default: {DEFAULT_MARKETPLACE}).",
    )
    parser.add_argument(
        "--log",
        metavar="CSV_FILE",
        default=None,
        help="Append the built title to this CSV log file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the result without writing to the CSV log.",
    )
    return parser.parse_args(argv)


def _format_result(result: BuildResult) -> str:
    status = "OK" if not result.over_limit else "OVER LIMIT"
    over = f"  ({result.overflow} chars over)" if result.overflow else ""
    return (
        f"Title: {result.title}\n"
        f"Marketplace: {result.marketplace} (limit {result.limit} chars)\n"
        f"Length: {result.length} chars{over}  [{status}]\n"
        f"Truncated: {result.truncated_title}"
    )


def _log_result(log_path: Path, result: BuildResult) -> None:
    write_header = not log_path.exists() or log_path.stat().st_size == 0
    with log_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_HEADER)
        if write_header:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "marketplace": result.marketplace,
                "title": result.title,
                "length": result.length,
                "limit": result.limit,
                "over_limit": result.over_limit,
                "overflow": result.overflow,
            }
        )


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    attrs = ListingAttributes(
        brand=args.brand,
        model=args.model,
        item=args.item,
        condition=args.condition,
        size=args.size,
        color=args.color,
        quantity=args.quantity,
    )
    result = build_title(attrs, args.marketplace)

    print(_format_result(result))

    hints = keyword_hints(attrs)
    if hints:
        print("Keyword hints: " + ", ".join(hints))

    if args.dry_run:
        print("Dry-run: CSV log not written.")
        return 0

    if args.log:
        _log_result(Path(args.log), result)
        print(f"Logged to {args.log}")
    else:
        print("No --log path given; nothing written (use --dry-run to preview).")

    return 1 if result.over_limit else 0


if __name__ == "__main__":
    sys.exit(main())
