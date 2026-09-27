"""
02_word_pairs.py – Most frequent terms of two and three words per channel, per source group and per phase
============================================================================================================

RUN (in the folder scripts/analysis, after scripts/database/04_clean_text.py):
  python 02_word_pairs.py

WHY
  Many terms consist of two or three words and are split in the single-word count:
  رژیم صهیونیستی, تنگه هرمز, شورای امنیت, وزیر امور خارجه, جمهوری اسلامی ایران ...
  This script counts neighbouring words of 2 and 3 words – again without any word list given in advance.

HOW
  - basis is the column 'text_clean'
  - terms never cross a line break, punctuation or a number
  - terms containing a stop word (stopwords_fa.txt) or a one-letter word are left out
  - a shorter term is dropped if it is almost always (COVERED_SHARE) part of one longer term:
      وزیر امور  -> almost always وزیر امور خارجه  -> only the three-word term is listed
      رژیم صهیونیستی -> part of many different longer terms -> stays
  - frequencies per 1,000 words, so channels and groups of different size can be compared
  - same order as 01_word_frequency.py: each channel, each group, then each channel and group per phase

OUTPUT (folder results/words)
  word_pairs.xlsx – sheet 'channels', sheet 'groups', then one sheet per channel and per group with the phases
  word_pairs.csv  – the same numbers as one long table (for later analysis and the dashboard)
"""
import re
from collections import Counter
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg:///iran_media_2026"
TOP_N = 1000                                                 # terms per list
MAX_WORDS = 3                                                # longest term (set to 4 for e.g. سپاه پاسداران انقلاب اسلامی)
MIN_COUNT = 5                                                # rarer terms are dropped early to save memory
COVERED_SHARE = 0.8                                          # see "HOW" above
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "results" / "words"
STOPWORD_FILE = Path(__file__).resolve().parents[1] / "database" / "stopwords_fa.txt"
ALL = "all"                                                  # name for the whole period

STOPWORDS = {w.strip() for w in STOPWORD_FILE.read_text(encoding="utf-8").splitlines()
             if w.strip() and not w.startswith("#")}
ZWNJ = "‌"
SEGMENT_BREAK = re.compile(r"[\n.،,؛;:!؟?«»\"'()\[\]{}|/\\\-–—_…]+")   # terms never cross these
WORD = re.compile("[ء-غف-يپچژکگیۀ‌]+")


def runs(text):
    """Sequences of neighbouring content words; numbers, Latin words, stop words and punctuation break a sequence."""
    for segment in SEGMENT_BREAK.split(text):
        run = []
        for token in segment.split():
            word = token.strip(ZWNJ)
            if WORD.fullmatch(token) and len(word) > 1 and word not in STOPWORDS:
                run.append(word)
            else:
                if len(run) > 1:
                    yield run
                run = []
        if len(run) > 1:
            yield run


def terms(text):
    """All terms of 2 to MAX_WORDS neighbouring content words."""
    result = []
    for run in runs(text):
        for n in range(2, MAX_WORDS + 1):
            result += [" ".join(run[i:i + n]) for i in range(len(run) - n + 1)]
    return result


def covered_terms(total):
    """Shorter terms that are almost always part of one single longer term."""
    longest = Counter()
    for term, n in total.items():
        words = term.split()
        if len(words) > 2:
            for part in (" ".join(words[:-1]), " ".join(words[1:])):
                longest[part] = max(longest[part], n)
    return {t for t, n in total.items() if longest[t] >= COVERED_SHARE * n}


def read_posts(engine):
    return pd.read_sql("""
        SELECT c.channel_id, c.name AS channel, g.group_id, g.name AS source_group,
               ph.phase_id, ph.name AS phase, p.text_clean, p.word_count
        FROM posts p
        JOIN channels c       ON c.channel_id = p.channel_id
        JOIN source_groups g  ON g.group_id   = c.group_id
        JOIN dates d          ON d.date_key   = p.date_key
        JOIN phases ph        ON ph.phase_id  = d.phase_id
        WHERE p.word_count > 1
    """, engine)


def count_terms(df):
    """One counter per channel and phase; all other combinations are sums of these."""
    counts, words = {}, {}
    for (channel, phase), part in df.groupby(["channel", "phase"]):
        c = Counter()
        for t in part["text_clean"]:
            c.update(terms(t))
        counts[(channel, phase)] = Counter({p: n for p, n in c.items() if n >= MIN_COUNT})
        words[(channel, phase)] = part["word_count"].sum()

    drop = covered_terms(sum(counts.values(), Counter()))   # decided once on all posts, same for every list
    for key in counts:
        for t in drop & counts[key].keys():
            del counts[key][t]
    print(f"{len(drop)} shorter terms dropped because they are part of a longer term")
    return counts, words


def top_terms(counter, total_words, level, name, phase):
    return pd.DataFrame(
        [{"level": level, "name": name, "phase": phase, "rank": i, "term": p, "n_words": len(p.split()),
          "count": n, "per_1000_words": round(1000 * n / total_words, 3)}
         for i, (p, n) in enumerate(counter.most_common(TOP_N), start=1)])


def build_table(df, counts, words):
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
                c, total = Counter(), 0
                for ch in members(name):
                    for ph in (phases if phase == ALL else [phase]):
                        c += counts.get((ch, ph), Counter())
                        total += words.get((ch, ph), 0)
                rows.append(top_terms(c, total, level, name, phase))
    return pd.concat(rows, ignore_index=True), phases


def wide(table, level, names, phase_list):
    """Side by side: for every name/phase two columns (term, per 1,000 words)."""
    blocks = []
    for name in names:
        for phase in phase_list:
            part = table[(table["level"] == level) & (table["name"] == name) & (table["phase"] == phase)]
            title = name if phase == ALL else f"{name} – {phase}"
            blocks.append(part[["term", "per_1000_words"]].reset_index(drop=True)
                          .set_axis([title, "per 1,000 words"], axis=1))
    out = pd.concat(blocks, axis=1)
    out.index = out.index + 1
    out.index.name = "rank"
    return out


def main():
    engine = create_engine(DATABASE_URL)
    df = read_posts(engine)
    print(f"{len(df)} posts with text read")

    counts, words = count_terms(df)
    table, phases = build_table(df, counts, words)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUTPUT_DIR / "word_pairs.csv", index=False, encoding="utf-8-sig")   # Persian shows correctly in Excel

    channels = table.loc[table["level"] == "channel", "name"].unique()
    groups = table.loc[table["level"] == "group", "name"].unique()
    with pd.ExcelWriter(OUTPUT_DIR / "word_pairs.xlsx") as xl:
        wide(table, "channel", channels, [ALL]).to_excel(xl, sheet_name="channels")
        wide(table, "group", groups, [ALL]).to_excel(xl, sheet_name="groups")
        for name in channels:
            wide(table, "channel", [name], phases).to_excel(xl, sheet_name=name[:31])
        for name in groups:
            wide(table, "group", [name], phases).to_excel(xl, sheet_name=name[:31])
    print(f"saved to {OUTPUT_DIR}\n")

    # short overview: top 10 per group
    for name in groups:
        top = table[(table["level"] == "group") & (table["name"] == name) & (table["phase"] == ALL)].head(10)
        print(f"{name}: " + "  |  ".join(top["term"]))


if __name__ == "__main__":
    main()
