#!/usr/bin/env python3
"""Substack Digest — orchestrator.

Usage:
    python main.py                        # Webhook mode (production)
    python main.py --polling              # Polling mode (local dev)
    python main.py --dry-run              # Print digest to console
    python main.py --dry-run --days 1     # Print last 24h digest
    python main.py --send-email           # Generate + send via email
"""

import argparse
import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Substack Weekly Digest Bot")
    parser.add_argument("--dry-run", action="store_true", help="Print digest to console instead of sending")
    parser.add_argument("--days", type=int, default=7, help="Number of days to look back (default: 7)")
    parser.add_argument("--polling", action="store_true", help="Run Telegram bot in polling mode (local dev)")
    parser.add_argument("--send-email", action="store_true", help="Send digest via email (SendGrid)")
    parser.add_argument("--webhook-url", type=str, default=None, help="Telegram webhook URL for production")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8443")), help="Port for webhook server")
    args = parser.parse_args()

    if args.dry_run:
        # Generate and print — no delivery
        from fetcher import fetch_all_feeds
        from summarizer import generate_digest

        logger.info("Dry run: fetching articles from the last %d day(s)…", args.days)
        articles = fetch_all_feeds(days=args.days)
        if not articles:
            print("No articles found for this period.")
            return
        logger.info("Generating digest…")
        digest = generate_digest(articles, days=args.days)
        print("\n" + "=" * 60)
        print(digest)
        print("=" * 60)
        return

    if args.send_email:
        # One-shot: generate + email
        from fetcher import fetch_all_feeds
        from summarizer import generate_digest
        from emailer import send_email
        import markdown

        logger.info("Generating digest for email…")
        articles = fetch_all_feeds(days=args.days)
        if not articles:
            logger.warning("No articles found — skipping email.")
            return
        digest = generate_digest(articles, days=args.days)
        html = markdown.markdown(digest)
        success = send_email(subject="Your Weekly Substack Digest", body_html=html)
        if not success:
            sys.exit(1)
        return

    # ── Telegram bot mode ──────────────────────────────────────────────
    from telegram_bot import create_bot_app, run_polling, run_webhook

    app = create_bot_app()

    if args.polling:
        run_polling(app)
    else:
        webhook_url = args.webhook_url or os.getenv("WEBHOOK_URL", "")
        if not webhook_url:
            logger.error(
                "Webhook URL required. Set WEBHOOK_URL env var or use --webhook-url, "
                "or run with --polling for local development."
            )
            sys.exit(1)
        run_webhook(app, webhook_url=webhook_url, port=args.port)


if __name__ == "__main__":
    main()
