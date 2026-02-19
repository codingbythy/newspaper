"""RSS feed fetching and article extraction."""

import logging
from datetime import datetime, timedelta, timezone
from time import mktime

import feedparser
from bs4 import BeautifulSoup

from config import FEEDS, MAX_WORDS_PER_ARTICLE

logger = logging.getLogger(__name__)


def strip_html(html: str) -> str:
    """Remove HTML tags and return plain text."""
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def truncate_text(text: str, max_words: int = MAX_WORDS_PER_ARTICLE) -> str:
    """Truncate text to a maximum number of words."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + " [truncated]"


def parse_entry_date(entry) -> datetime | None:
    """Extract a datetime from a feed entry, returning None on failure."""
    for attr in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, attr, None)
        if parsed:
            try:
                return datetime.fromtimestamp(mktime(parsed), tz=timezone.utc)
            except (ValueError, OverflowError):
                continue
    return None


def fetch_feed(feed_info: dict, cutoff: datetime) -> list[dict]:
    """Fetch articles from a single RSS feed published after *cutoff*.

    Returns a list of article dicts. Logs a warning and returns [] on failure.
    """
    url = feed_info["url"]
    name = feed_info["name"]
    category = feed_info["category"]

    try:
        parsed = feedparser.parse(url)
        if parsed.bozo and not parsed.entries:
            logger.warning("Feed '%s' (%s) failed to parse: %s", name, url, parsed.bozo_exception)
            return []

        articles = []
        for entry in parsed.entries:
            pub_date = parse_entry_date(entry)
            if pub_date is None or pub_date < cutoff:
                continue

            content_html = ""
            if hasattr(entry, "content") and entry.content:
                content_html = entry.content[0].get("value", "")
            elif hasattr(entry, "summary"):
                content_html = entry.summary or ""

            plain_text = strip_html(content_html)
            truncated = truncate_text(plain_text)

            articles.append({
                "title": getattr(entry, "title", "(no title)"),
                "link": getattr(entry, "link", ""),
                "source": name,
                "category": category,
                "published": pub_date.isoformat(),
                "content": truncated,
            })

        logger.info("Feed '%s': fetched %d article(s) since %s", name, len(articles), cutoff.date())
        return articles

    except Exception:
        logger.exception("Unexpected error fetching feed '%s' (%s)", name, url)
        return []


def fetch_all_feeds(days: int = 7) -> list[dict]:
    """Fetch recent articles from all configured feeds.

    Args:
        days: Look back this many days for articles.

    Returns:
        A flat list of article dicts, sorted newest-first.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    all_articles: list[dict] = []

    for feed_info in FEEDS:
        articles = fetch_feed(feed_info, cutoff)
        all_articles.extend(articles)

    all_articles.sort(key=lambda a: a["published"], reverse=True)
    logger.info("Total articles fetched: %d", len(all_articles))
    return all_articles
