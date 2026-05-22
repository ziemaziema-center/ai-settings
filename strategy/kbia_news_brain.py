from __future__ import annotations

import html
import re
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any


SCHEMA_VERSION = "kbia.news_brain.v1"
SAFE_NEXT_ACTION = "daily_digest_shadow_reference_only_no_trade_execution"

DEFAULT_WATCH_SYMBOLS = ("BTC", "ETH", "SOL", "ETC", "DOGE", "DOT", "ALGO", "FCT2")


@dataclass(frozen=True)
class NewsSource:
    name: str
    url: str
    tier: str
    credibility: float


DEFAULT_SOURCES = (
    NewsSource("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/", "major_crypto_media", 0.78),
    NewsSource("Decrypt", "https://decrypt.co/feed", "major_crypto_media", 0.68),
    NewsSource("Cointelegraph", "https://cointelegraph.com/rss", "crypto_media_crosscheck", 0.58),
    NewsSource("Blockworks", "https://blockworks.co/feed", "institutional_crypto_media", 0.70),
)

SYMBOL_KEYWORDS = {
    "BTC": ("btc", "bitcoin", "spot bitcoin", "bitcoin etf"),
    "ETH": ("eth", "ether", "ethereum", "ethereum etf"),
    "SOL": ("sol", "solana"),
    "ETC": ("etc", "ethereum classic"),
    "DOGE": ("doge", "dogecoin"),
    "DOT": ("dot", "polkadot"),
    "ALGO": ("algo", "algorand"),
    "FCT2": ("fct2", "firmachain"),
}

RISK_KEYWORDS = {
    "REGULATION": ("sec", "fsc", "fiu", "lawsuit", "ban", "regulation", "enforcement", "probe", "investigation"),
    "EXCHANGE": ("upbit", "bithumb", "binance", "coinbase", "listing", "delisting", "suspension", "halt"),
    "SECURITY": ("hack", "exploit", "bridge", "drain", "stolen", "phishing", "vulnerability"),
    "MACRO": ("fed", "rate", "inflation", "cpi", "treasury", "dollar", "etf inflows", "outflows"),
    "MARKET_STRESS": ("liquidation", "sell-off", "crash", "plunge", "bankruptcy", "insolvency"),
}


def _strip(value: str | None) -> str:
    text = html.unescape(value or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _parse_datetime(value: str | None) -> str | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError, OverflowError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat(timespec="seconds")


def _first_text(element: ET.Element, names: tuple[str, ...]) -> str:
    for name in names:
        found = element.find(name)
        if found is not None and found.text:
            return _strip(found.text)
    for child in element:
        tag = child.tag.rsplit("}", 1)[-1]
        if tag in {name.rsplit("}", 1)[-1] for name in names} and child.text:
            return _strip(child.text)
    return ""


def _first_link(element: ET.Element) -> str:
    link = _first_text(element, ("link", "{http://www.w3.org/2005/Atom}link"))
    if link:
        return link
    for child in element:
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "link" and child.attrib.get("href"):
            return child.attrib["href"]
    return ""


def parse_feed(xml_text: str, source: NewsSource, limit: int = 25) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_text)
    entries = root.findall(".//item")
    if not entries:
        entries = root.findall(".//{http://www.w3.org/2005/Atom}entry")
    items = []
    for entry in entries[:limit]:
        title = _first_text(entry, ("title", "{http://www.w3.org/2005/Atom}title"))
        if not title:
            continue
        summary = _first_text(entry, ("description", "summary", "{http://www.w3.org/2005/Atom}summary"))
        published = _parse_datetime(_first_text(entry, ("pubDate", "published", "updated", "{http://www.w3.org/2005/Atom}published", "{http://www.w3.org/2005/Atom}updated")))
        items.append(
            {
                "source": source.name,
                "source_tier": source.tier,
                "source_credibility": source.credibility,
                "title": title,
                "summary": summary[:240],
                "link": _first_link(entry),
                "published_utc": published,
            }
        )
    return items


def fetch_feed(source: NewsSource, timeout: int = 15) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    request = urllib.request.Request(source.url, headers={"User-Agent": "KBIA-News-Brain/1.0", "Accept": "application/rss+xml, application/xml, text/xml"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            text = response.read().decode("utf-8", errors="replace")
        return parse_feed(text, source), None
    except Exception as exc:  # noqa: BLE001 - returned as sanitized telemetry.
        return [], {"source": source.name, "url": source.url, "error_type": exc.__class__.__name__, "error_message": str(exc)[:160]}


def _dedupe(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result = []
    for item in items:
        key = re.sub(r"[^a-z0-9]+", " ", (item.get("link") or item.get("title") or "").lower()).strip()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def _symbols_for(text: str, watch_symbols: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    symbols = []
    for symbol in watch_symbols:
        keywords = SYMBOL_KEYWORDS.get(symbol, (symbol.lower(),))
        if any(re.search(rf"\b{re.escape(keyword)}\b", lowered) for keyword in keywords):
            symbols.append(symbol)
    return symbols


def _risk_tags(text: str) -> list[str]:
    lowered = text.lower()
    tags = []
    for tag, keywords in RISK_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            tags.append(tag)
    return tags


def score_item(item: dict[str, Any], watch_symbols: tuple[str, ...] = DEFAULT_WATCH_SYMBOLS) -> dict[str, Any]:
    text = f"{item.get('title', '')} {item.get('summary', '')}"
    symbols = _symbols_for(text, watch_symbols)
    tags = _risk_tags(text)
    base = float(item.get("source_credibility") or 0.5) * 50
    symbol_score = min(25, len(symbols) * 8)
    risk_score = min(30, len(tags) * 8)
    broad_market_score = 10 if re.search(r"\b(bitcoin|btc|ethereum|eth|etf|fed|sec|regulation)\b", text.lower()) else 0
    score = round(base + symbol_score + risk_score + broad_market_score, 2)
    result = dict(item)
    result.update(
        {
            "affected_symbols": symbols,
            "risk_tags": tags,
            "relevance_score": min(score, 100.0),
            "brain_signal": _brain_signal(symbols, tags),
        }
    )
    return result


def _brain_signal(symbols: list[str], tags: list[str]) -> str:
    if "SECURITY" in tags or "MARKET_STRESS" in tags:
        return "RISK_REDUCTION_WATCH"
    if "REGULATION" in tags or "EXCHANGE" in tags:
        return "EVENT_RISK_WATCH"
    if symbols:
        return "SYMBOL_CONTEXT_WATCH"
    return "BROAD_CONTEXT"


def build_digest(items: list[dict[str, Any]], source_failures: list[dict[str, Any]] | None = None, watch_symbols: tuple[str, ...] = DEFAULT_WATCH_SYMBOLS, top_n: int = 12) -> dict[str, Any]:
    scored = [score_item(item, watch_symbols) for item in _dedupe(items)]
    scored = sorted(scored, key=lambda row: (row["relevance_score"], row.get("published_utc") or ""), reverse=True)
    top = scored[:top_n]
    risk_tag_counts: dict[str, int] = {}
    symbol_counts: dict[str, int] = {}
    for item in top:
        for tag in item["risk_tags"]:
            risk_tag_counts[tag] = risk_tag_counts.get(tag, 0) + 1
        for symbol in item["affected_symbols"]:
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
    daily_bias = "NORMAL_REFERENCE"
    if risk_tag_counts.get("SECURITY", 0) or risk_tag_counts.get("MARKET_STRESS", 0):
        daily_bias = "DEFENSIVE_REFERENCE"
    elif risk_tag_counts.get("REGULATION", 0) or risk_tag_counts.get("EXCHANGE", 0):
        daily_bias = "EVENT_RISK_REFERENCE"
    return {
        "schema_version": SCHEMA_VERSION,
        "mode": "daily_crypto_news_digest",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "watch_symbols": list(watch_symbols),
        "items_scanned": len(scored),
        "top_items": top,
        "risk_tag_counts": dict(sorted(risk_tag_counts.items())),
        "symbol_counts": dict(sorted(symbol_counts.items())),
        "daily_brain_bias": daily_bias,
        "source_failures": source_failures or [],
        "execution_allowed": False,
        "live_order_allowed": False,
        "live_sell_allowed": False,
        "automation_allowed": False,
        "order_endpoint_allowed": False,
        "cancel_endpoint_allowed": False,
        "market_sell_allowed": False,
        "scheduler_allowed": False,
        "no_profit_guarantee": True,
        "next_safe_action": SAFE_NEXT_ACTION,
    }


def collect_daily_digest(sources: tuple[NewsSource, ...] = DEFAULT_SOURCES, watch_symbols: tuple[str, ...] = DEFAULT_WATCH_SYMBOLS) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for source in sources:
        source_items, failure = fetch_feed(source)
        items.extend(source_items)
        if failure:
            failures.append(failure)
    return build_digest(items, failures, watch_symbols)
