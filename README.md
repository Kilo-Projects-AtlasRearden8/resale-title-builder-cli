# Resale Title Builder

A local-first Python CLI for eBay/Amazon resellers to build listing titles from item attributes, with character counts, keyword hints, CSV logging, and a dry-run mode. No accounts, API keys, or network calls required.

Built and maintained by [Asdale Dynamics, LLC](https://dylanasdale.github.io) — Indiana, formed October 2026.

## What it does

Joins your item attributes (brand, model, item, condition, size, color, quantity) into a listing title, counts the characters, and compares them against the marketplace limit:

- eBay: 80 characters
- Amazon: 200 characters

It prints whether the title is within the limit, how many characters it is over (if any), and a safely truncated version. It also suggests keyword hints drawn from your attributes, and can append each build to a CSV log for your records.

## Install

```bash
git clone <this-repo>
cd resale-title-builder-cli
pip install -e .
```

This installs the `resale-title-builder` command on your PATH. Everything runs locally.

## Usage

```bash
resale-title-builder --brand Nike --model "Air Max" --item sneakers \
  --condition Used --size 10 --color Black --marketplace ebay
```

Example output:

```
Title: Nike Air Max sneakers Used 10 Black 1
Marketplace: ebay (limit 80 chars)
Length: 35 chars  [OK]
Truncated: Nike Air Max sneakers Used 10 Black 1
Keyword hints: nike, air, max, sneakers, used, 10, black, 1
```

### Dry-run mode

Preview a title without writing to the CSV log:

```bash
resale-title-builder --brand Nike --item sneakers --dry-run
```

### CSV log

Append each build to a CSV file for your records:

```bash
resale-title-builder --brand Nike --item sneakers --log titles.csv
```

The log contains: timestamp, marketplace, title, length, limit, over_limit, overflow.

## Tests

```bash
pip install pytest
pytest
```

Tests cover the length rules: exact-limit, one-char-over, truncation, marketplace fallback, and field ordering.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See [LICENSE](LICENSE).

## About

Asdale Dynamics, LLC is a beginner-friendly AI education and practical tools company founded by Dylan Asdale, a registered nurse turned AI author. See [dylanasdale.github.io](https://dylanasdale.github.io) for more.
