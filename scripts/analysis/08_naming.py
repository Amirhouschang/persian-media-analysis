"""
08_naming.py – How do the sources name the same things? (Israel, USA, countries, crimes, diplomacy, revenge ...)
=================================================================================================================

RUN (in the folder scripts/analysis, after scripts/database/04_clean_text.py):
  python 08_naming.py

WHAT IT DOES
  The concepts and their spellings are listed in naming_terms.csv (category, concept, variant) – every line can be
  checked, added or deleted there. The script counts every concept per source group, channel and phase.
    - per 1,000 words, so sources of different size can be compared
    - share within the category: e.g. of all names for Israel, how many % are اسرائیل and how many رژیم صهیونیستی?
  Within one category, longer variants are counted first and then removed from the text, so the same place is
  never counted twice (ارتش تروریستی آمریکا is not counted again as آمریکا; شمال فلسطین اشغالی not again as
  فلسطین اشغالی). Different categories are counted independently.
  Whole words only: اسرائیلی does not count as اسرائیل, آمریکایی not as آمریکا.

  In addition: the words directly before and after ترامپ and نتانیاهو – which titles and adjectives are used
  for them, per source group (NEIGHBOUR_TARGETS, more names can be added there).

OUTPUT (folder results/naming)
  naming.xlsx     – one sheet per category (groups and channels, per 1,000 words and share in %),
                    one sheet per category with the phases, sheet 'neighbours' (filter by target and group)
  naming.csv      – all counts as one long table (for the dashboard)
  neighbours.csv  – words before/after every target per source group
"""
import importlib.util
import re
from collections import Counter
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("terms", HERE / "03_terms.py")    # same database query and word rules
terms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(terms)

NAMING_FILE = HERE / "naming_terms.csv"
OUTPUT_DIR = HERE.parents[1] / "results" / "naming"
Z = "\u200c"
NEIGHBOUR_TARGETS = {"person": ["ترامپ", "نتانیاهو"]}   # which adjectives and titles stand next to them
TOP_NEIGHBOURS = 20
LETTER = "[\\u0600-\\u06ff\\u200c]"
ALL = "all"


def load_naming():
    n = pd.read_csv(NAMING_FILE, encoding="utf-8-sig", dtype=str).dropna()
    n["pattern"] = [re.compile(f"(?<!{LETTER}){re.escape(v.strip())}(?!{LETTER})") for v in n["variant"]]
    n["length"] = n["variant"].str.len()
    return n


def count_part(text, naming):
    """Counts per (category, concept) in one block of text; longer variants first within a category."""
    counts = Counter()
    for category, part in naming.groupby("category", sort=False):
        t = text
        for r in part.sort_values("length", ascending=False).itertuples():
            t, n = r.pattern.subn(" ", t)
            counts[(category, r.concept)] += n
    return counts


def neighbours(texts, targets):
    """Content words directly before and after every target (same word rules as 03_terms.py)."""
    split = {t: t.split() for t in targets}
    before = {t: Counter() for t in targets}
    after = {t: Counter() for t in targets}
    for text in texts:
        for run in terms.runs(text):
            for t, words in split.items():
                n = len(words)
                for i in range(len(run) - n + 1):
                    if run[i:i + n] == words:
                        if i > 0:
                            before[t][run[i - 1]] += 1
                        if i + n < len(run):
                            after[t][run[i + n]] += 1
    return before, after


def main():
    engine = create_engine(terms.DATABASE_URL)
    df = terms.read_posts(engine)
    naming = load_naming()
    print(f"{len(df)} posts, {naming[['category', 'concept']].drop_duplicates().shape[0]} concepts, "
          f"{len(naming)} variants")

    counts, words = {}, {}
    for (channel, phase), part in df.groupby(["channel", "phase"]):
        counts[(channel, phase)] = count_part("\n".join(part["text_clean"]), naming)
        words[(channel, phase)] = part["word_count"].sum()

    channels = df.drop_duplicates("channel").sort_values("channel_id")
    groups = df.drop_duplicates("source_group").sort_values("group_id")["source_group"].tolist()
    phases = df.drop_duplicates("phase").sort_values("phase_id")["phase"].tolist()
    concepts = naming[["category", "concept"]].drop_duplicates()

    rows = []
    for level, names, members in [
        ("group", groups, lambda n: channels.loc[channels["source_group"] == n, "channel"].tolist()),
        ("channel", channels["channel"].tolist(), lambda n: [n]),
    ]:
        for name in names:
            for phase in [ALL] + phases:
                c, total_words = Counter(), 0
                for ch in members(name):
                    for ph in (phases if phase == ALL else [phase]):
                        c += counts[(ch, ph)]
                        total_words += words[(ch, ph)]
                for cat, concept in concepts.itertuples(index=False):
                    rows.append({"level": level, "name": name, "phase": phase, "category": cat, "concept": concept,
                                 "count": c[(cat, concept)], "per_1000_words": 1000 * c[(cat, concept)] / total_words})
    table = pd.DataFrame(rows)
    cat_total = table.groupby(["level", "name", "phase", "category"])["count"].transform("sum")
    table["share_pct"] = (100 * table["count"] / cat_total.where(cat_total > 0)).round(1)
    table["per_1000_words"] = table["per_1000_words"].round(3)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUTPUT_DIR / "naming.csv", index=False, encoding="utf-8-sig")
    order = {c: i for i, c in enumerate(concepts["concept"])}
    with pd.ExcelWriter(OUTPUT_DIR / "naming.xlsx") as xl:
        for cat in concepts["category"].unique():
            part = table[(table["category"] == cat) & (table["phase"] == ALL)]
            wide = part.pivot_table(index="concept", columns="name", values=["share_pct", "per_1000_words"], dropna=False)
            wide = wide.reindex(columns=groups + channels["channel"].tolist(), level=1)
            wide.columns = [f"{n} – {'share %' if v == 'share_pct' else 'per 1,000'}" for v, n in wide.columns]
            wide = wide.sort_index(key=lambda s: s.map(order))
            wide.to_excel(xl, sheet_name=cat[:31])
            ph = table[(table["category"] == cat) & (table["level"] == "group") & (table["phase"] != ALL)]
            wide_ph = ph.pivot_table(index="concept", columns=["name", "phase"], values="share_pct", dropna=False)
            wide_ph = wide_ph.reindex(columns=pd.MultiIndex.from_product([groups, phases]))
            wide_ph.columns = [f"{g} – {p} – share %" for g, p in wide_ph.columns]
            wide_ph.sort_index(key=lambda s: s.map(order)).to_excel(xl, sheet_name=f"{cat[:24]}_phases")

        targets = [t for ts in NEIGHBOUR_TARGETS.values() for t in ts]
        kind = {t: k for k, ts in NEIGHBOUR_TARGETS.items() for t in ts}
        nrows = []
        for g in groups:
            before, after = neighbours(df.loc[df["source_group"] == g, "text_clean"], targets)
            for t in targets:
                for position, c in [("before", before[t]), ("after", after[t])]:
                    mentions = sum(c.values())
                    for rank, (w, n) in enumerate(c.most_common(TOP_NEIGHBOURS), start=1):
                        nrows.append({"kind": kind[t], "target": t, "group": g, "position": position, "rank": rank,
                                      "word": w, "count": n, "share_pct": round(100 * n / mentions, 1)})
        nb = pd.DataFrame(nrows)
        nb.to_excel(xl, sheet_name="neighbours", index=False)
    nb.to_csv(OUTPUT_DIR / "neighbours.csv", index=False, encoding="utf-8-sig")
    print(f"saved to {OUTPUT_DIR}\n")

    for cat in ["israel_naming", "usa_naming"]:
        print(cat)
        part = table[(table["category"] == cat) & (table["level"] == "group") & (table["phase"] == ALL)]
        print(part.pivot_table(index="concept", columns="name", values="share_pct", dropna=False).reindex(columns=groups)
              .sort_index(key=lambda s: s.map(order)).to_string(), "\n")


if __name__ == "__main__":
    main()
