"""Title building logic for resale listing titles."""

from __future__ import annotations

from dataclasses import dataclass

MARKETPLACE_LIMITS = {"ebay": 80, "amazon": 200}
DEFAULT_MARKETPLACE = "ebay"

# Attribute order used when assembling a title: most identifying first.
FIELD_ORDER = ("brand", "model", "item", "condition", "size", "color", "quantity")


@dataclass
class ListingAttributes:
    """Item attributes supplied by the reseller."""

    brand: str = ""
    model: str = ""
    item: str = ""
    condition: str = ""
    size: str = ""
    color: str = ""
    quantity: str = ""

    def provided(self) -> dict[str, str]:
        """Return only the attributes that have a non-blank value."""
        return {
            field: value
            for field, value in self.__dict__.items()
            if str(value).strip()
        }


@dataclass
class BuildResult:
    """Outcome of building a listing title."""

    title: str
    marketplace: str
    limit: int
    length: int
    over_limit: bool
    overflow: int
    truncated_title: str


def build_title(
    attrs: ListingAttributes, marketplace: str = DEFAULT_MARKETPLACE
) -> BuildResult:
    """Assemble a listing title and measure it against the marketplace limit."""
    marketplace = marketplace.lower()
    limit = MARKETPLACE_LIMITS.get(marketplace, MARKETPLACE_LIMITS[DEFAULT_MARKETPLACE])

    parts = [
        str(getattr(attrs, field)).strip()
        for field in FIELD_ORDER
        if str(getattr(attrs, field)).strip()
    ]
    title = " ".join(parts)

    over_limit = len(title) > limit
    overflow = max(len(title) - limit, 0)
    truncated_title = title[:limit] if over_limit else title

    return BuildResult(
        title=title,
        marketplace=marketplace,
        limit=limit,
        length=len(title),
        over_limit=over_limit,
        overflow=overflow,
        truncated_title=truncated_title,
    )


def keyword_hints(attrs: ListingAttributes) -> list[str]:
    """Suggest keywords drawn from the provided attributes, in order of appearance."""
    seen: set[str] = set()
    hints: list[str] = []
    for value in attrs.provided().values():
        for word in str(value).split():
            word = word.strip(".,()[]/\\-").lower()
            if not word or word in seen:
                continue
            seen.add(word)
            hints.append(word)
    return hints
