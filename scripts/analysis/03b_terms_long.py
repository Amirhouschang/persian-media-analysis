"""
03b_terms_long.py – Like 03_terms.py, but with longer fixed terms (up to MAX_WORDS words)
==========================================================================================

Test version to find the right maximum length: names such as نیروی قدس سپاه پاسداران انقلاب اسلامی have 6 words.
Run it with MAX_WORDS = 8, sort phrases_max8.csv by n_words and check whether terms of 7 and 8 words are real names
or only parts of sentences. The results of 03_terms.py are not overwritten (file names end with _max<MAX_WORDS>).

Everything else is identical to 03_terms.py:

RUN (in the folder scripts/analysis, after scripts/database/04_clean_text.py):
  python 03b_terms_long.py

WHY
  01 counts single words, 02 counts neighbouring words. Both count the same place in a text several times:
  in رژیم صهیونیستی, the words رژیم and صهیونیستی are counted as well. This script counts every place ONCE:
      ... وزیر امور خارجه گفت          -> one term: وزیر امور خارجه
      ... وزارت امور خارجه اعلام کرد    -> one term: وزارت امور خارجه
      ... حمله رژیم به لبنان            -> رژیم counts on its own, because صهیونیستی does not follow
  No word list is given in advance.

HOW
  1. Find fixed terms of 2 to MAX_WORDS neighbouring content words (no stop words, no numbers, no punctuation).
     A sequence is a fixed term if it occurs at least PHRASE_MIN_COUNT times in all posts, and
       - two words: at least PHRASE_SHARE of the occurrences of its rarer word are inside this pair
           تنگه هرمز, شورای امنیت (شورای is mostly followed by امنیت, even if امنیت is a common word)
       - three or four words: at least PHRASE_SHARE of the occurrences of BOTH shorter parts are inside it
           وزیر امور خارجه    -> a large share of امور خارجه and of وزیر امور           -> fixed term
           حمله رژیم صهیونیستی -> only a small share of رژیم صهیونیستی                    -> free combination, not a term
     The list of fixed terms is saved (phrases_max<MAX_WORDS>.csv) so it can be checked.
  2. In every text, fixed terms are joined: longer terms first; if two terms of the same length overlap,
     the more frequent one wins (حمله رژیم صهیونیستی -> حمله + رژیم صهیونیستی).
  3. Every term – single word or fixed term – is counted once per place.
  Frequencies per 1,000 words, in the same order as 01 and 02: each channel, each group, then per phase.

OUTPUT (folder results/words)
  phrases_max8.csv – all fixed terms found, with count and share in percent (share_pct)
  terms_max8.xlsx  – sheet 'channels', sheet 'groups', then one sheet per channel and per group with the phases
  terms_max8.csv   – the same numbers as one long table (for later analysis and the dashboard)
"""
import re
from collections import Counter
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg:///iran_media_2026"
TOP_N = 1000                                                 # terms per list
MAX_WORDS = 8                                                # longest fixed term (03_terms.py: 4)
PHRASE_MIN_COUNT = 100                                       # a fixed term must occur at least this often
PHRASE_SHARE = 0.25                                          # see "HOW" above
MIN_COUNT = 5                                                # rarer sequences are dropped early to save memory
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "results" / "words"
STOPWORD_FILE = Path(__file__).resolve().parents[1] / "database" / "stopwords_fa.txt"
ALL = "all"                                                  # name for the whole period
JOIN = "_"                                                   # joins the words of a fixed term inside the program

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
                if run:
                    yield run
                run = []
        if run:
            yield run


def read_posts(engine):
    return pd.read_sql("""
        SELECT c.channel_id, c.name AS channel, g.group_id, g.name AS source_group,
               ph.phase_id, ph.name AS phase, p.text_clean, p.word_count
        FROM posts p
        JOIN channels c       ON c.channel_id = p.channel_id
        JOIN source_groups g  ON g.group_id   = c.group_id
        JOIN dates d          ON d.date_key   = p.date_key
        JOIN phases ph        ON ph.phase_id  = d.phase_id
        WHERE p.word_count > 0
    """, engine)


# ---------- step 1: find fixed terms ----------
def find_phrases(df):
    total = Counter()
    for _, part in df.groupby(["channel", "phase"]):                # per part, to keep memory small
        c = Counter()
        for text in part["text_clean"]:
            for run in runs(text):
                for n in range(1, MAX_WORDS + 1):
                    c.update(JOIN.join(run[i:i + n]) for i in range(len(run) - n + 1))
        total.update({t: n for t, n in c.items() if n >= MIN_COUNT})

    phrases = []
    for term, n in total.items():
        words = term.split(JOIN)
        if len(words) < 2 or n < PHRASE_MIN_COUNT:
            continue
        if len(words) == 2:
            reference = min(total.get(w, n) for w in words)                       # the rarer word
        else:
            reference = max(total.get(JOIN.join(words[:-1]), n),                  # the more frequent of the
                            total.get(JOIN.join(words[1:]), n))                   # two shorter parts
        share = n / reference
        if share >= PHRASE_SHARE:
            phrases.append({"term": " ".join(words), "n_words": len(words), "count": n,
                            "share_pct": round(100 * share)})             # whole percent: read correctly everywhere
    return pd.DataFrame(phrases, columns=["term", "n_words", "count", "share_pct"]).sort_values(
        "count", ascending=False, ignore_index=True)


# ---------- step 2 and 3: join fixed terms and count every place once ----------
def merged_terms(text, phrases):
    """Terms of one text: longer fixed terms first, if they overlap the more frequent one; the rest single words."""
    result = []
    for run in runs(text):
        candidates = [(n, phrases[t], i) for n in range(2, min(MAX_WORDS, len(run)) + 1)
                      for i in range(len(run) - n + 1) if (t := JOIN.join(run[i:i + n])) in phrases]
        taken, start = [False] * len(run), {}
        for n, _, i in sorted(candidates, key=lambda c: (-c[0], -c[1])):
            if not any(taken[i:i + n]):
                taken[i:i + n] = [True] * n
                start[i] = n
        i = 0
        while i < len(run):
            n = start.get(i, 1)
            result.append(JOIN.join(run[i:i + n]))
            i += n
    return result


def count_terms(df, phrases):
    """One counter per channel and phase; all other combinations are sums of these."""
    counts, words = {}, {}
    for (channel, phase), part in df.groupby(["channel", "phase"]):
        c = Counter()
        for text in part["text_clean"]:
            c.update(merged_terms(text, phrases))
        counts[(channel, phase)] = c
        words[(channel, phase)] = part["word_count"].sum()
    return counts, words


def top_terms(counter, total_words, level, name, phase):
    return pd.DataFrame(
        [{"level": level, "name": name, "phase": phase, "rank": i, "term": t.replace(JOIN, " "),
          "n_words": t.count(JOIN) + 1, "count": n, "per_1000_words": round(1000 * n / total_words, 3)}
         for i, (t, n) in enumerate(counter.most_common(TOP_N), start=1)])


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

    phrases = find_phrases(df)
    print(f"{len(phrases)} fixed terms found")
    phrase_counts = dict(zip(phrases["term"].str.replace(" ", JOIN), phrases["count"]))

    counts, words = count_terms(df, phrase_counts)
    table, phase_names = build_table(df, counts, words)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    phrases.to_csv(OUTPUT_DIR / f"phrases_max{MAX_WORDS}.csv", index=False, encoding="utf-8-sig")
    table.to_csv(OUTPUT_DIR / f"terms_max{MAX_WORDS}.csv", index=False, encoding="utf-8-sig")

    channels = table.loc[table["level"] == "channel", "name"].unique()
    groups = table.loc[table["level"] == "group", "name"].unique()
    with pd.ExcelWriter(OUTPUT_DIR / f"terms_max{MAX_WORDS}.xlsx") as xl:
        wide(table, "channel", channels, [ALL]).to_excel(xl, sheet_name="channels")
        wide(table, "group", groups, [ALL]).to_excel(xl, sheet_name="groups")
        for name in channels:
            wide(table, "channel", [name], phase_names).to_excel(xl, sheet_name=name[:31])
        for name in groups:
            wide(table, "group", [name], phase_names).to_excel(xl, sheet_name=name[:31])
    print(f"saved to {OUTPUT_DIR}\n")

    print("Most frequent fixed terms: " + "  |  ".join(phrases["term"].head(15)))
    for name in groups:
        top = table[(table["level"] == "group") & (table["name"] == name) & (table["phase"] == ALL)].head(10)
        print(f"{name}: " + "  |  ".join(top["term"]))


if __name__ == "__main__":
    main()
