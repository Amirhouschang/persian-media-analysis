"""
11_peak_weeks.py – What happened in the peak weeks of the charts?
===================================================================

RUN (in the folder scripts/analysis, after 03_terms.py and 09_timeline.py):
  python 11_peak_weeks.py

WHY
  The charts of 09_timeline.py show WHEN a term was used most, not WHY. This script looks at the peak weeks and
  lists the terms that were typical for exactly that week – so a peak can be explained with the data itself
  (e.g. a peak of "negotiations" together with the name of the city where the talks took place).

HOW
  1. For every chart of 09_timeline.py and every source group: the TOP_WEEKS complete weeks with the highest value
     (values from results/timeline/timeline.csv).
  2. For each of these weeks: which terms did the group use clearly more often in this week than in all its other
     weeks? Same terms as 03_terms.py (fixed terms, corrections, ignored words left out) and the same method as
     07_typical_terms.py (weighted log-odds ratio, z > 1.96).

OUTPUT (folder results/timeline, only numbers and terms – no post texts)
  peak_weeks.csv – chart, group, peak (1 = highest week), week_start, value, rank, term, z, count
"""
import importlib.util
from collections import Counter
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

HERE = Path(__file__).resolve().parent


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


terms = load("terms", "03_terms.py")              # terms and corrections
typical = load("typical", "07_typical_terms.py")  # log-odds method
timeline = load("timeline", "09_timeline.py")     # list of charts

OUTPUT_DIR = HERE.parents[1] / "results" / "timeline"
TOP_WEEKS = 2                                     # peak weeks per chart and group
TOP_TERMS = 15                                    # typical terms per peak week
GROUPS = ["state", "irgc_affiliated", "reformist"]
JOIN = terms.JOIN


def read_posts(engine):
    df = pd.read_sql(text("""
        SELECT c.channel_id, c.name AS channel, g.name AS source_group, d.week_start, p.text_clean, p.word_count
        FROM posts p
        JOIN channels c       ON c.channel_id = p.channel_id
        JOIN source_groups g  ON g.group_id   = c.group_id
        JOIN dates d          ON d.date_key   = p.date_key
        WHERE p.word_count > 0
    """), engine)
    df["week_start"] = df["week_start"].astype(str)
    df["phase"] = df["week_start"]                # 03_terms.py counts per (channel, "phase") – here: per week
    return df


def weekly_values(table, value, category, concept):
    """Same series as in the charts of 09_timeline.py: group × complete week."""
    part = table[(table["level"] == "group") & (table["category"] == category)]
    if concept is None:
        return part.groupby(["name", "week_start"])["per_1000_words"].sum().reset_index(name="value")
    part = part[part["concept"] == concept]
    return part[["name", "week_start", value]].rename(columns={value: "value"})


def main():
    table = pd.read_csv(OUTPUT_DIR / "timeline.csv", encoding="utf-8-sig", dtype={"week_start": str})
    weeks = sorted(table["week_start"].unique())
    complete = set(weeks[1:-1])                   # first and last week are incomplete (as in the charts)

    engine = create_engine(terms.DATABASE_URL)
    df = read_posts(engine)
    titles, added, removed, ignored, merge_map = terms.load_corrections()
    phrases = terms.find_phrases(df, titles, added, removed)
    phrase_counts = dict(zip(phrases["term"].str.replace(" ", JOIN), phrases["count"]))
    counts, _ = terms.count_terms(df, phrase_counts, merge_map)
    ignored_keys = {t.replace(" ", JOIN) for t in ignored}
    counts = {k: Counter({t: n for t, n in c.items() if t not in ignored_keys}) for k, c in counts.items()}
    print(f"{len(df)} posts, {len(complete)} complete weeks")

    members = df.drop_duplicates("channel").groupby("source_group")["channel"].apply(list).to_dict()
    per_week = {g: {} for g in GROUPS}
    for g in GROUPS:
        for w in weeks:
            c = Counter()
            for ch in members[g]:
                c += counts.get((ch, w), Counter())
            per_week[g][w] = c
    group_total = {g: sum(per_week[g].values(), Counter()) for g in GROUPS}
    prior = sum(group_total.values(), Counter())

    rows = []
    for value, category, concept, title, filename in timeline.CHARTS:
        series = weekly_values(table, value, category, concept)
        for g in GROUPS:
            s = series[(series["name"] == g) & series["week_start"].isin(complete)].dropna()
            for peak, r in enumerate(s.nlargest(TOP_WEEKS, "value").itertuples(), start=1):
                target = per_week[g][r.week_start]
                result = typical.log_odds(target, group_total[g] - target, prior)
                result = result[result["z"] > 1.96].nlargest(TOP_TERMS, "z")
                for rank, t in enumerate(result.itertuples(), start=1):
                    rows.append({"chart": filename, "group": g, "peak": peak, "week_start": r.week_start,
                                 "value": round(r.value, 3), "rank": rank, "term": t.term.replace(JOIN, " "),
                                 "z": round(t.z, 1), "count": t.count})
                top = result["term"].str.replace(JOIN, " ").head(10)
                print(f"{filename} | {g} | week {r.week_start} ({r.value:.2f}): " + "  |  ".join(top))

    out = pd.DataFrame(rows)
    out.to_csv(OUTPUT_DIR / "peak_weeks.csv", index=False, encoding="utf-8-sig")
    print(f"\nsaved to {OUTPUT_DIR / 'peak_weeks.csv'}")


if __name__ == "__main__":
    main()
