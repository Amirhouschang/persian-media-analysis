"""
Checks telegram_reform_jan_aug_2026.csv (the Jamaran file) for completeness.
  python 01d_check_jamaran.py
Output: seven checks in the terminal + weekly table pruefung_reform_pro_woche.csv in data/row/
"""
from pathlib import Path
import pandas as pd

PROJECT = Path(__file__).resolve().parents[2]          # telegram-iran/
DATA_DIR = PROJECT / "data" / "row"
INPUT_FILE = "telegram_reform_jan_aug_2026.csv"
WEEKLY_FILE = "pruefung_reform_pro_woche.csv"

df = pd.read_csv(DATA_DIR / INPUT_FILE, parse_dates=["datum"], low_memory=False)
df["tag"] = df["datum"].dt.date                        # day of publication

print("1) Total rows:", len(df))

print("\n2) Posts per channel (compare with the collection output):")
print(df["kanal"].value_counts().to_string())

print("\n3) Period per channel (should be about 2026-01-01 to 2026-08-31):")
print(df.groupby("kanal")["datum"].agg(["min", "max"]).to_string())

print("\n4) Duplicate posts (should be 0):", df.duplicated(["kanal", "id"]).sum())

print("\n5) Share without text (images/videos without caption are normal):")
print((df["text"].isna() | (df["text"].str.strip() == "")).groupby(df["kanal"]).mean()
      .mul(100).round(1).astype(str).add(" %").to_string())

print("\n6) Days WITHOUT posts per channel (gaps):")
all_days = pd.date_range("2026-01-01", "2026-08-31").date
for channel, g in df.groupby("kanal"):
    missing = sorted(set(all_days) - set(g["tag"]))
    print(f"  {channel}: {len(missing)} days missing", [str(d) for d in missing])

print("\n7) Posts per week (sharp drops = possible gap or internet shutdown):")
weekly = df.groupby([pd.Grouper(key="datum", freq="W"), "kanal"]).size().unstack(fill_value=0)
print(weekly.to_string())
weekly.to_csv(DATA_DIR / WEEKLY_FILE)
print(f"\nWeekly table saved: {WEEKLY_FILE}")
