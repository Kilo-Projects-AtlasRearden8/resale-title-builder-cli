"""Tests for the length rules and title builder."""

from resale_title_builder.builder import BuildResult, ListingAttributes, build_title

EBAY_LIMIT = 80
AMAZON_LIMIT = 200


def test_ebay_limit_is_80_chars() -> None:
    result = build_title(ListingAttributes(brand="x" * 80), "ebay")
    assert result.limit == EBAY_LIMIT
    assert not result.over_limit
    assert result.length == EBAY_LIMIT
    assert result.overflow == 0


def test_amazon_limit_is_200_chars() -> None:
    result = build_title(ListingAttributes(brand="x" * 200), "amazon")
    assert result.limit == AMAZON_LIMIT
    assert not result.over_limit
    assert result.length == AMAZON_LIMIT


def test_one_char_over_limit_is_flagged() -> None:
    result = build_title(ListingAttributes(brand="x" * 81), "ebay")
    assert result.over_limit is True
    assert result.overflow == 1
    assert result.length == 81


def test_exactly_at_limit_is_not_over_limit() -> None:
    result = build_title(ListingAttributes(brand="x" * 80), "ebay")
    assert result.over_limit is False
    assert result.overflow == 0


def test_truncated_title_respects_limit() -> None:
    result = build_title(ListingAttributes(brand="x" * 120), "ebay")
    assert len(result.truncated_title) == EBAY_LIMIT
    assert result.truncated_title == "x" * EBAY_LIMIT


def test_unknown_marketplace_falls_back_to_ebay_limit() -> None:
    result = build_title(ListingAttributes(brand="x" * 90), "mercari")
    assert result.limit == EBAY_LIMIT
    assert result.marketplace == "mercari"


def test_empty_attributes_produce_empty_title() -> None:
    result = build_title(ListingAttributes(), "ebay")
    assert result.title == ""
    assert result.length == 0
    assert not result.over_limit


def test_title_field_order() -> None:
    result = build_title(
        ListingAttributes(
            brand="Nike",
            model="Air Max",
            item="sneakers",
            condition="Used",
            size="10",
            color="Black",
            quantity="1",
        ),
        "ebay",
    )
    assert result.title == "Nike Air Max sneakers Used 10 Black 1"


def test_keyword_hints_dedup_and_order() -> None:
    from resale_title_builder.builder import keyword_hints

    attrs = ListingAttributes(brand="Nike Nike", item="sneakers")
    assert keyword_hints(attrs) == ["nike", "sneakers"]
