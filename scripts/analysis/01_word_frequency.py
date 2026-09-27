"""
01_word_frequency.py – Most frequent words per channel, per source group and per phase
=======================================================================================

RUN (in the folder scripts/analysis, after scripts/database/04_clean_text.py):
  python 01_word_frequency.py

WHAT IT DOES
  Counts the words in the column 'tokens' (stop words already removed) – no word list is given in advance.
  Frequencies are given per 1,000 words, so channels and groups of different size can be compared.

  1. each channel          (whole period)
  2. each source group     (whole period)
  3. each channel and each source group per phase (before_war, war, ceasefire, after_truce_collapse)

OUTPUT (folder results/words)
  word_frequency.xlsx – sheet 'channels', sheet 'groups', then one sheet per channel and per group with the phases
  word_frequency.csv  – the same numbers as one long table (for later analysis and the dashboard)
"""
from collections import Counter
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg:///iran_media_2026"
TOP_N = 1000                                                 # words per list
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "results" / "words"
ALL = "all"                                                  # name for the whole period


def read_posts(engine):
    return pd.read_sql("""
        SELECT c.channel_id, c.name AS channel, g.group_id, g.name AS source_group,
               ph.phase_id, ph.name AS phase, p.tokens
        FROM posts p
        JOIN channels c       ON c.channel_id = p.channel_id
        JOIN source_groups g  ON g.group_id   = c.group_id
        JOIN dates d          ON d.date_key   = p.date_key
        JOIN phases ph        ON ph.phase_id  = d.phase_id
        WHERE p.tokens <> ''
    """, engine)


def count_words(df):
    """One counter per channel and phase; all other combinations are sums of these."""
    counts = {}
    for (channel, phase), tokens in df.groupby(["channel", "phase"])["tokens"]:
        c = Counter()
        for t in tokens:
            c.update(t.split())
        counts[(channel, phase)] = c
    return counts


def top_words(counter, level, name, phase):
    total = sum(counter.values())
    return pd.DataFrame(
        [{"level": level, "name": name, "phase": phase, "rank": i, "word": w, "count": n,
          "per_1000": round(1000 * n / total, 2)}
         for i, (w, n) in enumerate(counter.most_common(TOP_N), start=1)])


def build_table(df, counts):
    channels = df.drop_duplicates("channel").sort_values("channel_id")
    groups = df.drop_duplicates("source_group").sort_values("group_id")
    phases = df.drop_duplicates("phase").sort_values("phase_id")["phase"].tolist()

    rows = []
    for level, names, members in [
        ("channel", channels["channel"], lambda n: [n]),
        ("group", groups["source_group"], lambda n: channels.loc[channels["source_group"] == n, "channel"]),
    ]:
        for name in names:
            for phase in [ALL] + phases:
                c = Counter()
                for ch in members(name):
                    for ph in (phases if phase == ALL else [phase]):
                        c += counts.get((ch, ph), Counter())
                rows.append(top_words(c, level, name, phase))
    return pd.concat(rows, ignore_index=True), phases


def wide(table, level, names, phase_list):
    """Side by side: for every name/phase two columns (word, per 1,000)."""
    blocks = []
    for name in names:
        for phase in phase_list:
            part = table[(table["level"] == level) & (table["name"] == name) & (table["phase"] == phase)]
            title = name if phase == ALL else f"{name} – {phase}"
            blocks.append(part[["word", "per_1000"]].reset_index(drop=True)
                          .set_axis([title, "per 1,000"], axis=1))
    out = pd.concat(blocks, axis=1)
    out.index = out.index + 1
    out.index.name = "rank"
    return out


def main():
    engine = create_engine(DATABASE_URL)
    df = read_posts(engine)
    print(f"{len(df)} posts with words read")

    counts = count_words(df)
    table, phases = build_table(df, counts)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUTPUT_DIR / "word_frequency.csv", index=False, encoding="utf-8-sig")   # utf-8-sig: Persian shows correctly in Excel and Power BI

    channels = table.loc[table["level"] == "channel", "name"].unique()
    groups = table.loc[table["level"] == "group", "name"].unique()
    with pd.ExcelWriter(OUTPUT_DIR / "word_frequency.xlsx") as xl:
        wide(table, "channel", channels, [ALL]).to_excel(xl, sheet_name="channels")
        wide(table, "group", groups, [ALL]).to_excel(xl, sheet_name="groups")
        for name in channels:
            wide(table, "channel", [name], phases).to_excel(xl, sheet_name=name[:31])
        for name in groups:
            wide(table, "group", [name], phases).to_excel(xl, sheet_name=name[:31])
    print(f"saved to {OUTPUT_DIR}\n")

    # short overview: top 10 per channel
    for name in channels:
        top = table[(table["level"] == "channel") & (table["name"] == name) & (table["phase"] == ALL)].head(10)
        print(f"{name}: " + "  ".join(top["word"]))


if __name__ == "__main__":
    main()
