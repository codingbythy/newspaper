"""Generate a weekly digest using the Claude API."""

import logging

import anthropic

from config import ANTHROPIC_API_KEY, CLAUDE_MODEL

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are a brilliant editorial assistant who synthesises newsletter content into \
an insightful weekly digest. Your reader is a curious, busy professional who \
subscribes to many Substack newsletters covering tech, finance, crypto, culture, \
and ideas. They want signal, not noise.

Write the digest in a clear, engaging tone. Use bullet points for quick scanning. \
Attribute insights to their sources when relevant. Flag disagreements between sources.\
"""

USER_PROMPT_TEMPLATE = """\
Below are articles from my Substack subscriptions published in the last {days} day(s). \
Please produce my weekly digest with the following sections:

## 🌍 World Affairs Brief
The 5-7 most important things I should know, synthesised across sources (not just \
per-article summaries). Flag where sources disagree.

## 📈 Markets & Crypto Brief
Key trends and insights from the finance/crypto newsletters.

## 🤖 Tech & AI Brief
Key developments from the tech-focused newsletters.

## 🎭 Culture & Ideas
Interesting ideas, contrarian takes, and things worth thinking about.

## 🤔 3 Weekly Reflection Questions
Thought-provoking questions inspired by the week's themes, designed to help me \
think critically and improve my life.

## 📚 Sources
A list of every article referenced, formatted as: "Title" — Source (link)

---

### Articles

{articles_text}
"""


def _format_articles(articles: list[dict]) -> str:
    """Format article list into text for the Claude prompt."""
    if not articles:
        return "(No articles available this period.)"

    parts: list[str] = []
    for i, a in enumerate(articles, 1):
        parts.append(
            f"[{i}] **{a['title']}**\n"
            f"Source: {a['source']} | Category: {a['category']} | Published: {a['published']}\n"
            f"Link: {a['link']}\n"
            f"Content:\n{a['content']}\n"
        )
    return "\n---\n".join(parts)


def generate_digest(articles: list[dict], days: int = 7) -> str:
    """Call Claude to produce a digest from the given articles.

    Returns the digest text (Markdown-formatted).
    """
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")

    articles_text = _format_articles(articles)
    user_prompt = USER_PROMPT_TEMPLATE.format(days=days, articles_text=articles_text)

    logger.info("Sending %d articles to Claude (%s)…", len(articles), CLAUDE_MODEL)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    digest = message.content[0].text
    logger.info("Digest generated (%d chars)", len(digest))
    return digest
