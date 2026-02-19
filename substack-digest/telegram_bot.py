"""Telegram bot for delivering Substack digests."""

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

from config import (
    FEEDS,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    WEEKLY_CRON_DAY,
    WEEKLY_CRON_HOUR,
    WEEKLY_CRON_MINUTE,
)
from fetcher import fetch_all_feeds
from summarizer import generate_digest

logger = logging.getLogger(__name__)

# Telegram message length limit
MAX_MESSAGE_LENGTH = 4096


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def split_message(text: str, limit: int = MAX_MESSAGE_LENGTH) -> list[str]:
    """Split a long message into chunks that fit Telegram's limit.

    Tries to break on newlines to keep formatting intact.
    """
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    while text:
        if len(text) <= limit:
            chunks.append(text)
            break

        # Find a good break point (prefer double-newline, then newline)
        split_at = text.rfind("\n\n", 0, limit)
        if split_at == -1:
            split_at = text.rfind("\n", 0, limit)
        if split_at == -1:
            split_at = limit

        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")

    return chunks


async def send_long_message(
    bot,
    chat_id: str | int,
    text: str,
    parse_mode: str | None = None,
) -> None:
    """Send a message, splitting into multiple if it exceeds the limit."""
    for chunk in split_message(text):
        try:
            await bot.send_message(chat_id=chat_id, text=chunk, parse_mode=parse_mode)
        except Exception:
            # If parse_mode fails (bad formatting), retry without it
            logger.warning("Failed to send with parse_mode=%s, retrying as plain text", parse_mode)
            await bot.send_message(chat_id=chat_id, text=chunk)


def _build_digest(days: int) -> str:
    """Fetch articles and generate a digest (synchronous)."""
    articles = fetch_all_feeds(days=days)
    if not articles:
        return "No articles found for this period."
    return generate_digest(articles, days=days)


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start — welcome message."""
    welcome = (
        "👋 *Welcome to your Substack Digest Bot!*\n\n"
        "I read your Substack subscriptions and deliver a curated weekly digest "
        "powered by Claude AI.\n\n"
        "*Commands:*\n"
        "/digest — Generate a fresh weekly digest now\n"
        "/today — Quick summary of the last 24 hours\n"
        "/feeds — List all active feeds\n\n"
        f"Your chat ID is `{update.effective_chat.id}` — "
        "add it to your `.env` as `TELEGRAM_CHAT_ID` if you haven't already."
    )
    await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN)


async def cmd_digest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /digest — generate and send a full weekly digest."""
    await update.message.reply_text("⏳ Fetching articles and generating your digest… this may take a minute.")
    try:
        digest = _build_digest(days=7)
        await send_long_message(update.message.bot, update.effective_chat.id, digest)
    except Exception:
        logger.exception("Error generating digest")
        await update.message.reply_text("❌ Something went wrong generating the digest. Check the logs.")


async def cmd_today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /today — quick summary of last 24 hours."""
    await update.message.reply_text("⏳ Checking what dropped in the last 24 hours…")
    try:
        digest = _build_digest(days=1)
        await send_long_message(update.message.bot, update.effective_chat.id, digest)
    except Exception:
        logger.exception("Error generating today's summary")
        await update.message.reply_text("❌ Something went wrong. Check the logs.")


async def cmd_feeds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /feeds — list all active feeds."""
    lines = ["*Active Feeds:*\n"]
    for f in FEEDS:
        lines.append(f"• {f['name']} [{f['category']}]")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)


# ---------------------------------------------------------------------------
# Scheduled job
# ---------------------------------------------------------------------------

async def scheduled_digest(app: Application) -> None:
    """Send the weekly digest on schedule."""
    if not TELEGRAM_CHAT_ID:
        logger.error("TELEGRAM_CHAT_ID not set — cannot send scheduled digest")
        return

    logger.info("Running scheduled weekly digest…")
    try:
        digest = _build_digest(days=7)
        await send_long_message(app.bot, TELEGRAM_CHAT_ID, digest)
        logger.info("Scheduled digest sent successfully")
    except Exception:
        logger.exception("Failed to send scheduled digest")


# ---------------------------------------------------------------------------
# Bot setup
# ---------------------------------------------------------------------------

def create_bot_app() -> Application:
    """Build and return the Telegram Application (not yet running).

    The APScheduler is started inside post_init so it has access to the
    running event loop created by run_polling / run_webhook.
    """
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    scheduler = AsyncIOScheduler()

    async def post_init(application: Application) -> None:
        scheduler.add_job(
            scheduled_digest,
            trigger=CronTrigger(
                day_of_week=WEEKLY_CRON_DAY,
                hour=WEEKLY_CRON_HOUR,
                minute=WEEKLY_CRON_MINUTE,
                timezone="UTC",
            ),
            args=[application],
            id="weekly_digest",
            name="Weekly Substack Digest",
            replace_existing=True,
        )
        scheduler.start()
        logger.info("APScheduler started inside running event loop")

    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Register command handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("digest", cmd_digest))
    app.add_handler(CommandHandler("today", cmd_today))
    app.add_handler(CommandHandler("feeds", cmd_feeds))

    return app


def run_polling(app: Application) -> None:
    """Run the bot in polling mode (local development)."""
    logger.info("Bot running in polling mode (scheduler active)")
    app.run_polling(drop_pending_updates=True)


def run_webhook(app: Application, webhook_url: str, port: int = 8443) -> None:
    """Run the bot in webhook mode (production)."""
    logger.info("Bot running in webhook mode on port %d", port)
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=webhook_url,
    )
