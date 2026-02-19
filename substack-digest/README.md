# Substack Weekly Digest Bot

A Python bot that fetches your Substack RSS feeds, uses Claude AI to generate an insightful weekly digest, and delivers it via Telegram.

## Features

- Fetches articles from 28+ Substack newsletters
- Claude AI synthesises content into structured sections: World Affairs, Markets & Crypto, Tech & AI, Culture & Ideas
- Generates 3 weekly reflection questions
- Delivers via Telegram bot with interactive commands
- Optional email fallback via SendGrid
- Runs on a weekly schedule or on-demand

## Project Structure

```
substack-digest/
├── config.py          # Feed list and settings
├── fetcher.py         # RSS fetching logic
├── summarizer.py      # Claude API summarisation
├── emailer.py         # Email sending (optional fallback)
├── telegram_bot.py    # Telegram bot with commands and scheduling
├── validate_feeds.py  # Test which feeds work
├── main.py            # Orchestrator
├── requirements.txt
├── .env.example
├── Procfile           # Railway deployment
├── Dockerfile         # Fly.io deployment
├── railway.toml
├── fly.toml
└── .github/workflows/weekly-digest.yml
```

## Quick Start

### 1. Install dependencies

```bash
cd substack-digest
pip install -r requirements.txt
```

### 2. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your API keys (see below)
```

### 3. Validate feeds

```bash
python validate_feeds.py
```

### 4. Run a dry run (no Telegram/email needed)

```bash
python main.py --dry-run
python main.py --dry-run --days 1   # last 24 hours only
```

### 5. Run the Telegram bot locally

```bash
python main.py --polling
```

## Setting Up Telegram

1. Message **@BotFather** on Telegram
2. Send `/newbot` and follow the prompts to create a bot
3. Copy the bot token → add to `.env` as `TELEGRAM_BOT_TOKEN`
4. Start a chat with your new bot and send `/start`
5. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` to find your `chat_id`
6. Copy `chat_id` → add to `.env` as `TELEGRAM_CHAT_ID`

### Bot Commands

| Command   | Description                          |
|-----------|--------------------------------------|
| `/start`  | Welcome message and setup info       |
| `/digest` | Generate a fresh weekly digest       |
| `/today`  | Quick summary of the last 24 hours   |
| `/feeds`  | List all active feeds                |

## Environment Variables

| Variable             | Required | Description                        |
|----------------------|----------|------------------------------------|
| `ANTHROPIC_API_KEY`  | Yes      | Claude API key                     |
| `TELEGRAM_BOT_TOKEN` | Yes*     | Telegram bot token from BotFather  |
| `TELEGRAM_CHAT_ID`   | Yes*     | Your Telegram chat ID              |
| `WEBHOOK_URL`        | Prod     | Webhook URL for production deploy  |
| `PORT`               | No       | Server port (default: 8443)        |
| `EMAIL_TO`           | No       | Recipient email (SendGrid)         |
| `EMAIL_FROM`         | No       | Sender email (SendGrid)            |
| `SENDGRID_API_KEY`   | No       | SendGrid API key                   |

*Not required for `--dry-run` mode.

## Deployment

### Option A: Railway (Recommended)

1. Push your repo to GitHub
2. Go to [railway.app](https://railway.app) and create a new project from your repo
3. Set environment variables in the Railway dashboard:
   - `ANTHROPIC_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `WEBHOOK_URL` (Railway provides this — use your app's public URL)
4. Railway auto-deploys on push. The `Procfile` and `railway.toml` handle the rest.

### Option B: Fly.io

1. Install the Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Authenticate: `fly auth login`
3. Launch the app:
   ```bash
   fly launch    # creates the app
   ```
4. Set secrets:
   ```bash
   fly secrets set ANTHROPIC_API_KEY=sk-ant-...
   fly secrets set TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
   fly secrets set TELEGRAM_CHAT_ID=123456789
   fly secrets set WEBHOOK_URL=https://substack-digest.fly.dev/webhook
   ```
5. Deploy:
   ```bash
   fly deploy
   ```

### Option C: GitHub Actions (Free, No Server)

This option uses GitHub's scheduled workflows to send digests without a running server. Interactive bot commands (`/digest`, `/today`) are **not** supported — only the scheduled weekly send and manual triggers.

1. Go to your repo → Settings → Secrets and variables → Actions
2. Add these repository secrets:
   - `ANTHROPIC_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. The workflow runs automatically every Sunday at 8 AM UTC
4. To trigger manually: Actions tab → "Weekly Substack Digest" → "Run workflow"

## Customising

### Adding/removing feeds

Edit the `FEEDS` list in `config.py`. Each feed needs:

```python
{"url": "https://example.substack.com/feed", "name": "Display Name", "category": "tech"}
```

Categories: `tech`, `crypto`, `finance`, `culture`, `ideas`, `economics`, `general`, `personal`, `business`, `trends`

### Changing the digest format

Edit the prompt templates in `summarizer.py` — the `SYSTEM_PROMPT` and `USER_PROMPT_TEMPLATE`.

### Changing the schedule

Edit `WEEKLY_CRON_DAY`, `WEEKLY_CRON_HOUR`, `WEEKLY_CRON_MINUTE` in `config.py`.
