"""
Step 1: Collect Telegram posts (1 Jan 2026 – 31 Aug 2026)
Requirements:
  pip install telethon pandas
  API ID + API hash from https://my.telegram.org (use a separate account!)
  Environment variables TG_API_ID and TG_API_HASH

Note: the column names of the output (kanal, seite, datum, ...) are kept in German
so that the existing data files stay compatible with all scripts.
"""
import os
import asyncio
from datetime import datetime, timezone
import pandas as pd
from telethon import TelegramClient

API_ID = int(os.environ["TG_API_ID"])        # never write credentials into the code
API_HASH = os.environ["TG_API_HASH"]
SESSION_NAME = "sitzung"                     # existing session file (sitzung.session) – do not change

START = datetime(2026, 1, 1, tzinfo=timezone.utc)
END = datetime(2026, 9, 1, tzinfo=timezone.utc)     # exclusive

# Check the user names in Telegram first!
# Keys = source group (stored in column 'seite'), values = channel user names
CHANNELS = {
    "staat": ["irna_1313", "iribnews", "mehrnews"],   # government / state broadcaster
    "irgc":  ["Tasnimnews", "farsna", "sepahnews"],   # IRGC-affiliated (sepahnews: not accessible from Germany)
}
# Public channels can be read without joining -> do NOT join them


async def collect(client, channel, group):
    rows = []
    async for m in client.iter_messages(channel, offset_date=END):
        if m.date < START:
            break
        rows.append({
            "kanal": channel,
            "seite": group,
            "id": m.id,
            "datum": m.date,
            "text": m.message or "",
            "views": m.views,
            "weiterleitungen": m.forwards,
            "weitergeleitet_von": getattr(m.fwd_from, "from_name", None) if m.fwd_from else None,
        })
    print(f"{channel}: {len(rows)} posts")
    return rows


async def main():
    all_posts = []
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH, flood_sleep_threshold=120) as client:
        for group, channels in CHANNELS.items():
            for channel in channels:
                try:
                    all_posts += await collect(client, channel, group)
                except Exception as e:
                    print(f"Error with {channel}: {e}")

    df = pd.DataFrame(all_posts)
    df.to_csv("telegram_jan_aug_2026.csv", index=False, encoding="utf-8-sig")
    print(f"Total: {len(df)} posts saved")


if __name__ == "__main__":
    asyncio.run(main())
