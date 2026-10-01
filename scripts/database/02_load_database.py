"""
02_load_database.py – Load the raw Telegram data into PostgreSQL
================================================================

REQUIREMENTS (once):
  pip install sqlalchemy "psycopg[binary]"
  createdb iran_media_2026

RUN (in the folder scripts/database, conda environment iran-analyse):
  python 02_load_database.py

WHAT IT DOES
  1. builds the tables from 01_schema.sql (existing tables are replaced)
  2. fills 'source_groups' (3 groups) and 'channels' (6 channels) with numeric keys,
     'phases' (4 phases of the period) and 'dates' (one row per day, key YYYYMMDD)
  3. loads all posts from both raw files into 'posts'
     (German column names of the CSV files are translated to English column names,
      the channel name is replaced by its numeric key channel_id)
  4. prints the number of posts per channel – compare with the collection (328,330 in total)
"""
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

PROJECT = Path(__file__).resolve().parents[2]            # persian-media-analysis/
RAW_FILES = [
    PROJECT / "data" / "row" / "telegram_jan_aug_2026.csv",
    PROJECT / "data" / "row" / "telegram_reform_jan_aug_2026.csv",
]
SCHEMA_FILE = Path(__file__).resolve().parent / "01_schema.sql"
DATABASE_URL = "postgresql+psycopg:///iran_media_2026"   # local database, your own Linux user

SOURCE_GROUPS = [
    # group_id, name, description
    (1, "state", "State / official media"),
    (2, "irgc_affiliated", "Media widely described as affiliated with the IRGC"),
    (3, "reformist", "Media associated with the reformist camp"),
]

CHANNELS = [
    # channel_id, Telegram user name, readable name, group_id, neutral description
    (1, "irna_1313", "IRNA", 1,
     "Official state news agency, supervised by the government."),
    (2, "iribnews", "IRIB News", 1,
     "News service of the state broadcaster, whose head is appointed by the Supreme Leader."),
    (3, "mehrnews", "Mehr News", 1,
     "Semi-official news agency owned by the Islamic Development Organization (under the Supreme Leader)."),
    (4, "Tasnimnews", "Tasnim News", 2,
     "Semi-official news agency widely described as affiliated with the IRGC."),
    (5, "farsna", "Fars News", 2,
     "Semi-official news agency widely described as affiliated with the IRGC."),
    (6, "jamarannews", "Jamaran", 3,
     "News outlet linked to the institute publishing Ayatollah Khomeini's works; associated with the reformist camp."),
]

# Phases of the observation period – boundaries based on key events (see scripts/ai/background.txt).
# Change them here if you define the phases differently.
PHASES = [
    # phase_id, name, start, end, description
    (1, "before_war", "2026-01-01", "2026-02-27",
     "Protests and internet blackout in January, US-Iran talks, before the US-Israeli strikes"),
    (2, "war", "2026-02-28", "2026-04-07",
     "From the US-Israeli strikes on 28 Feb until the ceasefire"),
    (3, "ceasefire", "2026-04-08", "2026-07-06",
     "Pakistan-mediated ceasefire, naval blockade, Islamabad talks and memorandum"),
    (4, "after_truce_collapse", "2026-07-07", "2026-08-31",
     "Collapse of the truce, renewed US strikes and blockade, new sanctions"),
]
PERIOD = ("2026-01-01", "2026-08-31")

# German column names in the raw CSV files -> English column names in the database
RENAME = {
    "kanal": "username", "id": "post_id", "datum": "published_at", "text": "text",
    "views": "views", "weiterleitungen": "forwards", "weitergeleitet_von": "forwarded_from",
}


def main():
    engine = create_engine(DATABASE_URL)

    # 1. tables
    with engine.begin() as con:
        con.execute(text(SCHEMA_FILE.read_text(encoding="utf-8")))
    print("Tables created.")

    # 2. source groups and channels
    groups = pd.DataFrame(SOURCE_GROUPS, columns=["group_id", "name", "description"])
    groups.to_sql("source_groups", engine, if_exists="append", index=False)
    channels = pd.DataFrame(CHANNELS, columns=["channel_id", "username", "name", "group_id", "description"])
    channels["channel_url"] = "https://t.me/" + channels["username"]
    channels.to_sql("channels", engine, if_exists="append", index=False)
    print(f"source_groups: {len(groups)} rows | channels: {len(channels)} rows")
    channel_ids = dict(zip(channels["username"], channels["channel_id"]))

    # 3. phases and date dimension
    phases = pd.DataFrame(PHASES, columns=["phase_id", "name", "start_date", "end_date", "description"])
    for column in ["start_date", "end_date"]:
        phases[column] = pd.to_datetime(phases[column]).dt.date          # text -> real date
    phases.to_sql("phases", engine, if_exists="append", index=False)
    days = pd.DataFrame({"date": pd.date_range(*PERIOD, freq="D")})
    days["date_key"] = days["date"].dt.strftime("%Y%m%d").astype(int)
    days["year"] = days["date"].dt.year
    days["month"] = days["date"].dt.month
    days["month_name"] = days["date"].dt.month_name()
    days["iso_week"] = days["date"].dt.isocalendar().week.astype(int)
    days["week_start"] = (days["date"] - pd.to_timedelta(days["date"].dt.weekday, unit="D")).dt.date
    days["weekday"] = days["date"].dt.weekday + 1
    days["weekday_name"] = days["date"].dt.day_name()
    days["phase_id"] = 0
    for pid, _, start, end, _ in PHASES:
        days.loc[days["date"].between(start, end), "phase_id"] = pid
    assert (days["phase_id"] > 0).all(), "every day must belong to a phase"
    days["date"] = days["date"].dt.date
    days.to_sql("dates", engine, if_exists="append", index=False)
    print(f"phases: {len(phases)} rows | dates: {len(days)} rows")

    # 4. posts
    for path in RAW_FILES:
        df = pd.read_csv(path, low_memory=False)
        df = df[list(RENAME)].rename(columns=RENAME)
        df = df[df["username"].isin(channel_ids)]                 # only the six channels of this project
        df["published_at"] = pd.to_datetime(df["published_at"], utc=True)
        df["text"] = df["text"].fillna("")
        df["post_url"] = "https://t.me/" + df["username"] + "/" + df["post_id"].astype(str)
        df["channel_id"] = df["username"].map(channel_ids)        # name -> numeric key
        df["date_key"] = df["published_at"].dt.strftime("%Y%m%d").astype(int)   # day (UTC) -> date key
        df = df.drop(columns="username")
        df.to_sql("posts", engine, if_exists="append", index=False, chunksize=5_000, method="multi")   # 5,000 rows x 7 columns stays below the PostgreSQL parameter limit
        print(f"{path.name}: {len(df)} posts loaded")

    # 5. check
    check = pd.read_sql("""
        SELECT c.name AS channel, g.name AS source_group, COUNT(*) AS posts
        FROM posts p
        JOIN channels c ON c.channel_id = p.channel_id
        JOIN source_groups g ON g.group_id = c.group_id
        GROUP BY c.name, g.name, c.channel_id
        ORDER BY c.channel_id
    """, engine)
    print("\n" + check.to_string(index=False))
    print(f"\nTotal: {check['posts'].sum()} posts")


if __name__ == "__main__":
    main()
