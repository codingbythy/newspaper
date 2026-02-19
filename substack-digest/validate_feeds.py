#!/usr/bin/env python3
"""Validate which Substack RSS feeds are reachable and return entries.

Usage:
    python validate_feeds.py
"""

import sys

import feedparser

from config import FEEDS


def validate() -> bool:
    """Test every feed URL. Returns True if all feeds are healthy."""
    ok, failed = [], []

    for feed in FEEDS:
        url = feed["url"]
        name = feed["name"]
        try:
            result = feedparser.parse(url)
            if result.bozo and not result.entries:
                failed.append((name, url, str(result.bozo_exception)))
            else:
                count = len(result.entries)
                ok.append((name, url, count))
        except Exception as exc:
            failed.append((name, url, str(exc)))

    print(f"\n✅  Working feeds ({len(ok)}):")
    for name, url, count in ok:
        print(f"   {name:40s}  {count:3d} entries  {url}")

    if failed:
        print(f"\n❌  Failed feeds ({len(failed)}):")
        for name, url, err in failed:
            print(f"   {name:40s}  {url}")
            print(f"      Error: {err}")
    else:
        print("\n🎉  All feeds are working!")

    return len(failed) == 0


if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
