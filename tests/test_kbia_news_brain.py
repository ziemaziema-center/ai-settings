import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy.kbia_news_brain import NewsSource, build_digest, parse_feed, score_item


RSS_FIXTURE = """<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <title>Fixture</title>
    <item>
      <title>SEC opens investigation into Solana exchange listing</title>
      <link>https://example.com/sol-sec</link>
      <description>Regulation and exchange listing risk for SOL markets.</description>
      <pubDate>Tue, 19 May 2026 00:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Bitcoin ETF inflows rise as Ethereum holds support</title>
      <link>https://example.com/btc-eth</link>
      <description>Macro market context for BTC and ETH.</description>
      <pubDate>Tue, 19 May 2026 01:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


def test_parse_feed_extracts_items():
    items = parse_feed(RSS_FIXTURE, NewsSource("Fixture", "https://example.com/rss", "test", 0.7))
    assert len(items) == 2
    assert items[0]["source"] == "Fixture"
    assert items[0]["published_utc"] == "2026-05-19T00:00:00+00:00"


def test_score_item_tags_symbols_and_risk():
    item = {
        "source": "Fixture",
        "source_credibility": 0.7,
        "title": "Upbit delisting notice hits Dogecoin and Solana traders",
        "summary": "Exchange suspension risk creates DOGE and SOL volatility.",
    }
    scored = score_item(item)
    assert "DOGE" in scored["affected_symbols"]
    assert "SOL" in scored["affected_symbols"]
    assert "EXCHANGE" in scored["risk_tags"]
    assert scored["brain_signal"] == "EVENT_RISK_WATCH"


def test_build_digest_is_shadow_only_and_defensive_on_security_news():
    digest = build_digest(
        [
            {
                "source": "Fixture",
                "source_credibility": 0.8,
                "title": "Bridge hack sparks Bitcoin sell-off",
                "summary": "Exploit and market liquidation risk.",
                "link": "https://example.com/hack",
            }
        ],
        [],
    )
    assert digest["daily_brain_bias"] == "DEFENSIVE_REFERENCE"
    assert digest["execution_allowed"] is False
    assert digest["live_order_allowed"] is False
    assert digest["order_endpoint_allowed"] is False
    assert digest["scheduler_allowed"] is False
    assert digest["no_profit_guarantee"] is True


if __name__ == "__main__":
    test_parse_feed_extracts_items()
    test_score_item_tags_symbols_and_risk()
    test_build_digest_is_shadow_only_and_defensive_on_security_news()
    print("KBIA_NEWS_BRAIN_TESTS_PASS")
