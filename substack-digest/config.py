"""Configuration: Substack feed list and application settings."""

import os
from dotenv import load_dotenv

load_dotenv()

# Claude API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"
MAX_WORDS_PER_ARTICLE = 2000

# Email (optional fallback)
EMAIL_TO = os.getenv("EMAIL_TO", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Schedule
WEEKLY_CRON_DAY = "sun"
WEEKLY_CRON_HOUR = 8
WEEKLY_CRON_MINUTE = 0

# Feeds
FEEDS = [
    # Tech & VC
    {"url": "https://a16z.substack.com/feed", "name": "a16z", "category": "tech"},
    {"url": "https://a16zcrypto.substack.com/feed", "name": "a16z crypto", "category": "crypto"},

    # Personal / Misc
    {"url": "https://alessandro.substack.com/feed", "name": "Alessandro's Substack", "category": "general"},

    # Culture & Ideas
    {"url": "https://theartofnoticing.substack.com/feed", "name": "The Art of Noticing", "category": "culture"},
    {"url": "https://blackmagic.substack.com/feed", "name": "Black Magic Newsletter", "category": "culture"},
    {"url": "https://blundercheck.substack.com/feed", "name": "Blundercheck", "category": "general"},

    # Finance & Macro
    {"url": "https://chamathpalihapitiya.substack.com/feed", "name": "Chamath Palihapitiya", "category": "finance"},
    {"url": "https://contraptions.substack.com/feed", "name": "Contraptions", "category": "general"},
    {"url": "https://crossingthemidcurve.substack.com/feed", "name": "Crossing the Mid Curve", "category": "finance"},
    {"url": "https://cryptotreasuryalpha.substack.com/feed", "name": "Crypto Treasury Alpha", "category": "crypto"},

    # Culture & Ideas
    {"url": "https://theculturist.substack.com/feed", "name": "The Culturist", "category": "culture"},

    # Tech
    {"url": "https://danielromero.substack.com/feed", "name": "Daniel Romero", "category": "tech"},

    # Personal Development
    {"url": "https://marlenekonu.substack.com/feed", "name": "Find your flow - Marlene Konu", "category": "personal"},

    # Culture
    {"url": "https://illustrated.substack.com/feed", "name": "ILLUSTRATED", "category": "culture"},

    # General
    {"url": "https://jeffs.substack.com/feed", "name": "Jeff's Substack", "category": "general"},

    # Crypto & Macro
    {"url": "https://jordivisser.substack.com/feed", "name": "Jordi Visser Macro-AI-Crypto Substack", "category": "crypto"},
    {"url": "https://leighcuen.substack.com/feed", "name": "Leigh Cuen's Adventures", "category": "crypto"},

    # Trends
    {"url": "https://metatrends.substack.com/feed", "name": "Metatrends", "category": "trends"},

    # Economics & Ideas
    {"url": "https://noahpinion.substack.com/feed", "name": "Noahpinion", "category": "ideas"},

    # Culture
    {"url": "https://npc.substack.com/feed", "name": "NPC Inc.", "category": "culture"},

    # Business
    {"url": "https://theprofile.substack.com/feed", "name": "The Profile", "category": "business"},

    # Finance
    {"url": "https://quanttradingrules.substack.com/feed", "name": "Quant Trading Rules", "category": "finance"},
    {"url": "https://russellwalter.substack.com/feed", "name": "The Russell Walter Substack", "category": "finance"},

    # Economics
    {"url": "https://saifedean.substack.com/feed", "name": "Saifedean", "category": "economics"},

    # Meta
    {"url": "https://substackpost.substack.com/feed", "name": "The Substack Post", "category": "general"},

    # Culture
    {"url": "https://summerlightning.substack.com/feed", "name": "Summer Lightning", "category": "culture"},
    {"url": "https://unchartedterritories.substack.com/feed", "name": "Uncharted Territories", "category": "ideas"},
    {"url": "https://usefulfictions.substack.com/feed", "name": "Useful Fictions", "category": "culture"},

    # --- New additions ---

    # Crypto & Web3
    {"url": "https://pomp.substack.com/feed", "name": "The Pomp Letter", "category": "crypto"},
    {"url": "https://rektcapital.substack.com/feed", "name": "Rekt Capital", "category": "crypto"},
    {"url": "https://thedailygwei.substack.com/feed", "name": "The Daily Gwei", "category": "crypto"},

    # Finance & Markets
    {"url": "https://doomberg.substack.com/feed", "name": "Doomberg", "category": "finance"},
    {"url": "https://michaeljburry.substack.com/feed", "name": "Cassandra Unchained", "category": "finance"},
    {"url": "https://netinterest.substack.com/feed", "name": "Net Interest", "category": "finance"},
    {"url": "https://thebearcave.substack.com/feed", "name": "The Bear Cave", "category": "finance"},
    {"url": "https://qualitycompounding.substack.com/feed", "name": "Compounding Quality", "category": "finance"},

    # Tech & AI/VC
    {"url": "https://newsletter.pragmaticengineer.com/feed", "name": "The Pragmatic Engineer", "category": "tech"},
    {"url": "https://www.newcomer.co/feed", "name": "Newcomer", "category": "tech"},
    {"url": "https://diff.substack.com/feed", "name": "The Diff", "category": "tech"},
    {"url": "https://www.lennysnewsletter.com/feed", "name": "Lenny's Newsletter", "category": "tech"},

    # Economics & Big Ideas
    {"url": "https://adamtooze.substack.com/feed", "name": "Chartbook", "category": "ideas"},
    {"url": "https://paulkrugman.substack.com/feed", "name": "Paul Krugman", "category": "economics"},
    {"url": "https://theovershoot.co/feed", "name": "The Overshoot", "category": "economics"},
    {"url": "https://geopoliticsunplugged.substack.com/feed", "name": "Geopolitics Unplugged", "category": "ideas"},

    # Culture & Creativity
    {"url": "https://haleynahman.substack.com/feed", "name": "Maybe Baby", "category": "culture"},
    {"url": "https://1000wordsofsummer.substack.com/feed", "name": "Craft Talk", "category": "culture"},
]

# Category groupings for the digest prompt
CATEGORY_GROUPS = {
    "world_affairs": ["general", "ideas", "economics", "trends", "business"],
    "markets_crypto": ["finance", "crypto"],
    "tech_ai": ["tech"],
    "culture_ideas": ["culture", "personal"],
}
