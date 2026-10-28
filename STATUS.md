# STATUS

## What was built

`resale-title-builder` — a local-first Python CLI for eBay/Amazon resellers to build listing titles from item attributes.

Package `resale_title_builder`:
- `builder.py` — assembles titles from brand/model/item/condition/size/color/quantity (in that order), measures them against marketplace character limits (eBay 80, Amazon 200), flags over-limit titles with overflow count, and produces a safely truncated title. `keyword_hints()` suggests de-duplicated keywords from the provided attributes.
- `cli.py` — argparse CLI: `--brand`, `--model`, `--item`, `--condition`, `--size`, `--color`, `--quantity`, `--marketplace`, `--log CSV_FILE`, `--dry-run`. Prints title, length, limit, over-limit status, truncated title, and keyword hints. `--dry-run` previews without writing the log; `--log` appends a row (timestamp, marketplace, title, length, limit, over_limit, overflow) to a CSV file.
- `__init__.py` — public API exports.

Other files:
- `pyproject.toml` — project metadata, `resale-title-builder` console script entry point.
- `tests/test_rules.py` — 9 tests for length rules (80-char eBay limit, 200-char Amazon limit, exactly-at-limit OK, one-char-over flagged, truncation respects limit, unknown marketplace falls back to eBay, empty attributes, field order, keyword hints).
- `LICENSE` — MIT License, copyright `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `README.md` — install, usage, dry-run, CSV log, tests, license; credits Asdale Dynamics, LLC.
- `.gitignore` — Python/cache artifacts.
- `STATUS.md` — this file.

No `.github/workflows` files. No secrets, API keys, or personal data.

## How to run it

```bash
cd /workspace/kilo-lab/resale-title-builder-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest   # for tests

# Preview a title (dry-run, nothing written):
resale-title-builder --brand Nike --item sneakers --condition Used --size 10 --dry-run

# Build and log to CSV:
resale-title-builder --brand Nike --model "Air Max" --item sneakers --condition Used --size 10 --color Black --quantity 1 --marketplace ebay --log titles.csv

# Run tests:
pytest
```

## Verification results

- `pytest`: 9 passed in 0.02s (all length-rule tests).
- CLI smoke test (eBay, full attributes): title built correctly, length counted, `[OK]` status, keyword hints printed.
- `--dry-run`: preview printed, "CSV log not written", no file created.
- `--log titles.csv`: row appended with header on first create; second run appended without duplicating header.
- Over-limit test (90-char brand on eBay): `[OVER LIMIT]`, `overflow: 10`, truncated title exactly 80 chars, CLI exit code 1.
- Verified with Python 3.13.5 and pytest 9.1.1 in an isolated venv.

## Known gaps

- Marketplace limits are hardcoded defaults (eBay 80, Amazon 200); category-specific Amazon limits and other marketplaces are not supported — add entries to `MARKETPLACE_LIMITS` in `resale_title_builder/builder.py`.
- No configuration file; all input via CLI flags.
- CSV log is append-only local file; no rotation, encryption, or export options.
- Title assembly is a simple space-join with no smart truncation at word boundaries.
