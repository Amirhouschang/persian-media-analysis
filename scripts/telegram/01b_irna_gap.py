"""
Checks the IRNA gap in January 2026 directly on Telegram.
  python 01b_irna_gap.py
Result: posts per day in the terminal + irna_gap.csv (if anything is found)
"""
import os
import asyncio
from datetime import datetime, timezone
import pandas as pd
from telethon import TelegramClient

API_ID = int(os.environ["TG_API_ID"])
API_HASH = os.environ["TG_API_HASH"]
SESSION_NAME = "sitzung"                     # existing session file (sitzung.session) – do not change
CHANNEL = "irna_1313"
START = datetime(2026, 1, 8, tzinfo=timezone.utc)
END = datetime(2026, 1, 26, tzinfo=timezone.utc)


async def main():
    rows = []
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        async for m in client.iter_messages(CHANNEL, offset_date=END):
            if m.date < START:
                break
            # column names kept in German, same as in the main data
            rows.append({"kanal": CHANNEL, "seite": "staat", "id": m.id, "datum": m.date,
                         "text": m.message or "", "views": m.views,
                         "weiterleitungen": m.forwards,
                         "weitergeleitet_von": getattr(m.fwd_from, "from_name", None) if m.fwd_from else None})

    df = pd.DataFrame(rows)
    if df.empty:
        print("No posts between 8 and 25 January -> the channel really paused.")
        return
    print("Posts per day:")
    print(df.groupby(df["datum"].dt.date).size().to_string())
    df.to_csv("irna_gap.csv", index=False, encoding="utf-8-sig")
    print(f"\n{len(df)} posts saved in irna_gap.csv")


asyncio.run(main())
