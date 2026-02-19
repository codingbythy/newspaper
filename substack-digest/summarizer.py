"""Generate a weekly digest using the Claude API."""

import logging

import anthropic

from config import ANTHROPIC_API_KEY, CLAUDE_MODEL

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are a brilliant editorial assistant who synthesises newsletter content into \
an insightful digest. Your reader is a curious, busy professional who \
subscribes to many Substack newsletters covering tech, finance, crypto, culture, \
and ideas. They want signal, not noise.

CRITICAL FORMATTING RULES — you MUST follow these exactly:
• Output is rendered in Telegram, which supports only a subset of HTML.
• Allowed tags: <b>, <i>, <u>, <s>, <a href="...">, <code>, <pre>, <blockquote>.
• Do NOT use <h1>–<h6>, <p>, <ul>, <li>, <br>, or any other HTML tags.
• Use plain newlines for line breaks (NOT <br>).
• Use "•" (bullet character) for list items, one per line.
• Use <b> for section headers on their own line.
• Escape these HTML entities in all text: & → &amp;  < → &lt;  > → &gt;
• Do NOT wrap output in ```html or any code fence.\
"""

USER_PROMPT_TEMPLATE = """\
Below are articles from my Substack subscriptions published in the last {days} day(s). \
Produce my digest using the exact format below. Replace the placeholder lines with real content.

🌍 <b>World Affairs</b>

• [Synthesised insight across sources, not per-article summaries]
• [Flag where sources disagree]
• [5-7 bullets total]

📈 <b>Markets &amp; Crypto</b>

• [Key trends and insights from finance/crypto newsletters]

🤖 <b>Tech &amp; AI</b>

• [Key developments from the tech-focused newsletters]

🎭 <b>Culture &amp; Ideas</b>

• [Interesting ideas, contrarian takes, things worth thinking about]

💡 <b>Reflection Questions</b>

1. [Thought-provoking question inspired by this period's themes]
2. [Another question]
3. [Another question]

📚 <b>Sources</b>

• <a href="link">Title</a> — Source
• [repeat for each article referenced]

---

<b>Articles</b>

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
