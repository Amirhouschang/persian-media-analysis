"""
12_countries.py – Countries and allied groups: how often, when, and in which context?
=====================================================================================

RUN (in the folder scripts/analysis, after 03_terms.py):
  python 12_countries.py

WHAT IT DOES
  All countries and groups of the category 'countries_actors' in naming_terms.csv (Gulf states, China, Russia,
  Pakistan, Lebanon, Hezbollah, Iraq, Yemen, Europe ...), counted with the same rules as 08_naming.py
  (whole words; longer names first, so دریای عمان is not counted as عمان).

  1. How often: per 1,000 words, per source group, channel and phase.
  2. When: per calendar week and source group – small-multiple charts, one panel per country (REGIONS).
  3. What happened in the peak weeks: for every country the PEAK_WEEKS weeks with the most mentions (all groups
     together) and the terms that were typical of the posts mentioning the country in exactly that week
     (compared with its other weeks).
  4. In which context (framing): for every country and source group the terms that this group uses clearly more
     often than the other groups IN THE POSTS THAT MENTION THIS COUNTRY – e.g. is Pakistan presented as a
     mediator, as a neighbour, or with the Taliban?
  3 and 4 use the terms of 03_terms.py and the log-odds method of 07_typical_terms.py.

OUTPUT (folder results/countries, only numbers and terms – no post texts)
  countries.csv        – count and per 1,000 words per level (group/channel), name, phase and country
  countries_weekly.csv – the same per source group and calendar week
  peak_weeks.csv       – country, peak, week_start, value, rank, term, z, count
  framing.csv          – country, group, rank, term, z, count, posts (posts of the group that mention the country)
  countries.xlsx       – overview (groups × countries), phases, peak weeks, framing
  charts/*.png         – one small-multiple chart per region
"""
import importlib.util
from collections import Counter
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sqlalchemy import create_engine, text

HERE = Path(__file__).resolve().parent


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


timeline = load("timeline", "09_timeline.py")     # chart style, colours, events
naming_module = timeline.naming_module            # 08_naming.py: list and counting rules
terms = naming_module.terms                       # 03_terms.py: terms and corrections
typical = load("typical", "07_typical_terms.py")  # log-odds method
typical.MIN_COUNT = 20                            # smaller text base per country than in 07

OUTPUT_DIR = HERE.parents[1] / "results" / "countries"
CATEGORY = "countries_actors"
GROUPS = ["state", "irgc_affiliated", "reformist"]
PEAK_WEEKS = 2                                    # peak weeks per country
TOP_TERMS = 15                                    # terms per list
MIN_POSTS = 100                                   # framing only for countries in at least this many posts of a group
JOIN = terms.JOIN
ALL = "all"

# charts: file name -> (title, [(concept in naming_terms.csv, English label), ...])
REGIONS = {
    "gulf_states": ("Gulf states and Jordan", [
        ("امارات", "UAE"), ("عربستان", "Saudi Arabia"), ("قطر", "Qatar"), ("کویت", "Kuwait"),
        ("بحرین", "Bahrain"), ("عمان", "Oman"), ("اردن", "Jordan")]),
    "axis_of_resistance": ("Lebanon, Palestine, Iraq, Yemen, Syria", [
        ("لبنان", "Lebanon"), ("حزب‌الله", "Hezbollah"), ("غزه", "Gaza"), ("حماس", "Hamas"),
        ("فلسطین", "Palestine"), ("عراق", "Iraq"), ("مقاومت عراق / حشد شعبی", "Iraqi militias"),
        ("یمن", "Yemen"), ("انصارالله / حوثی‌ها", "Houthis"), ("سوریه", "Syria"), ("داعش", "ISIS")]),
    "powers_neighbours": ("Great powers and neighbours", [
        ("روسیه", "Russia"), ("چین", "China"), ("پاکستان", "Pakistan"), ("ترکیه", "Turkey"),
        ("هند", "India"), ("ژاپن", "Japan"), ("افغانستان", "Afghanistan"), ("جمهوری آذربایجان", "Rep. of Azerbaijan"),
        ("اوکراین", "Ukraine"), ("ونزوئلا", "Venezuela"), ("طالبان", "Taliban")]),
    "europe": ("Europe", [
        ("اتحادیه اروپا", "EU / Europe"), ("انگلیس", "United Kingdom"), ("فرانسه", "France"),
        ("آلمان", "Germany"), ("ایتالیا", "Italy"), ("اسپانیا", "Spain")]),
}
LABELS = {c: label for _, items in REGIONS.values() for c, label in items}


def read_posts(engine):
    df = pd.read_sql(text("""
        SELECT c.channel_id, c.name AS channel, g.name AS source_group, ph.phase_id, ph.name AS phase,
               d.week_start, p.text_clean, p.word_count
        FROM posts p
        JOIN channels c       ON c.channel_id = p.channel_id
        JOIN source_groups g  ON g.group_id   = c.group_id
        JOIN dates d          ON d.date_key   = p.date_key
        JOIN phases ph        ON ph.phase_id  = d.phase_id
        WHERE p.word_count > 0
    """), engine)
    df["week_start"] = df["week_start"].astype(str)
    return df


def mentions(text, patterns):
    """Countries named in one post: {concept: count}; longer names first, then removed (as in 08_naming.py)."""
    found = Counter()
    for concept, pattern in patterns:
        text, n = pattern.subn(" ", text)
        if n:
            found[concept] += n
    return found


def post_terms(df):
    """Terms of every post, same rules as 03_terms.py (fixed terms, merges, half-space variants, ignored words)."""
    titles, added, removed, ignored, merge_map = terms.load_corrections()
    phrases = terms.find_phrases(df, titles, added, removed)
    phrase_counts = dict(zip(phrases["term"].str.replace(" ", JOIN), phrases["count"]))
    longest = max(t.count(JOIN) + 1 for t in phrase_counts)
    ignored_keys = {t.replace(" ", JOIN) for t in ignored}
    lists = [[merge_map.get(t, t) for t in terms.merged_terms(text, phrase_counts, longest)]
             for text in df["text_clean"]]
    total = Counter(t for ts in lists for t in ts)
    forms = {}
    for t, n in total.items():                                    # spellings with / without half-space
        forms.setdefault(t.replace(terms.ZWNJ, ""), []).append((n, t))
    to = {t: max(v)[1] for v in forms.values() if len(v) > 1 for _, t in v}
    return [[to.get(t, t) for t in ts if to.get(t, t) not in ignored_keys] for ts in lists]


def top(result, n=TOP_TERMS):
    result = result[result["z"] > 1.96].nlargest(n, "z").copy()
    if result.empty:                              # rare country: no term clearly typical
        return result
    result["term"] = result["term"].astype(str).str.replace(JOIN, " ")
    return result


def small_multiples(weekly, items, title, filename):
    """One panel per country, one line per source group (per 1,000 words), complete weeks only."""
    n = len(items) + 1                                            # last panel: legend
    cols = 4
    rows = -(-n // cols)
    fig, axes = plt.subplots(rows, cols, figsize=(14, 2.6 * rows + 0.8), dpi=150, sharex=True)
    fig.patch.set_facecolor(timeline.SURFACE)
    axes = axes.flatten()
    for ax, (concept, label) in zip(axes, items):
        ax.set_facecolor(timeline.SURFACE)
        part = weekly[weekly["concept"] == concept].pivot(index="week_start", columns="source_group",
                                                         values="per_1000_words")
        part.index = pd.to_datetime(part.index)
        for day, _, _ in timeline.EVENTS:
            ax.axvline(pd.Timestamp(day), color="#e1e0d9", linewidth=0.8, zorder=1)
        for g in GROUPS:
            if g in part:
                ax.plot(part.index, part[g], color=timeline.COLORS[g], linewidth=1.6, zorder=3)
        ax.set_title(label, loc="left", fontsize=10, color=timeline.INK)
        ax.set_ylim(bottom=0)
        ax.grid(axis="y", color=timeline.GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        for side in ["top", "right", "left"]:
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#c3c2b7")
        ax.tick_params(colors=timeline.MUTED, labelsize=7, length=0)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    legend_ax = axes[len(items)]
    for ax in axes[len(items):]:
        ax.axis("off")
    for g in GROUPS:
        legend_ax.plot([], [], color=timeline.COLORS[g], linewidth=2, label=timeline.GROUP_LABELS[g])
    legend_ax.legend(loc="center left", frameon=False, fontsize=9, labelcolor=timeline.INK,
                     title="per 1,000 words, weekly", title_fontsize=8)
    fig.suptitle(title, x=0.01, ha="left", fontsize=13, color=timeline.INK)
    fig.text(0.01, 0.005, "Grey lines: war begins 28 Feb, new leader 8 Mar, ceasefire 8 Apr, ceasefire collapses 8 Jul. "
             "Complete weeks only. Source: 6 Iranian Telegram channels, Jan–Aug 2026.", fontsize=7,
             color=timeline.MUTED)
    fig.tight_layout(rect=(0, 0.02, 1, 0.96))
    fig.savefig(OUTPUT_DIR / "charts" / f"{filename}.png", facecolor=timeline.SURFACE)
    plt.close(fig)


def main():
    naming = naming_module.load_naming()
    naming = naming[naming["category"] == CATEGORY].sort_values("length", ascending=False)
    patterns = list(zip(naming["concept"], naming["pattern"]))
    concepts = naming["concept"].drop_duplicates().tolist()

    engine = create_engine(terms.DATABASE_URL)
    df = read_posts(engine)
    df["mentions"] = [mentions(t, patterns) for t in df["text_clean"]]
    print(f"{len(df)} posts, {len(concepts)} countries and groups; "
          f"{df['mentions'].astype(bool).sum()} posts name at least one")

    # one row per post and country: post, concept, count (+ group, channel, phase, week)
    long = pd.DataFrame([(i, c, n) for i, m in zip(df.index, df["mentions"]) for c, n in m.items()],
                        columns=["post", "concept", "count"])
    long = long.join(df[["channel", "source_group", "phase", "week_start"]], on="post")

    # 1. how often – per group / channel and phase
    channels = df.drop_duplicates("channel").sort_values("channel_id")["channel"].tolist()
    phases = df.drop_duplicates("phase").sort_values("phase_id")["phase"].tolist()
    rows = []
    for level, key, names in [("group", "source_group", GROUPS), ("channel", "channel", channels)]:
        for phase in [ALL] + phases:
            d = df if phase == ALL else df[df["phase"] == phase]
            l = long if phase == ALL else long[long["phase"] == phase]
            words = d.groupby(key)["word_count"].sum()
            counts = l.groupby([key, "concept"])["count"].sum()
            for name in names:
                for concept in concepts:
                    n = int(counts.get((name, concept), 0))
                    rows.append({"level": level, "name": name, "phase": phase, "concept": concept,
                                 "label": LABELS.get(concept, ""), "count": n,
                                 "per_1000_words": round(1000 * n / words[name], 3)})
    overview = pd.DataFrame(rows)

    # 2. when – per group and week
    weeks = sorted(df["week_start"].unique())
    complete = weeks[1:-1]                                         # first and last week are incomplete
    words = df.groupby(["source_group", "week_start"])["word_count"].sum()
    counts = long.groupby(["source_group", "week_start", "concept"])["count"].sum()
    rows = []
    for (g, w), total in words.items():
        for concept in concepts:
            n = int(counts.get((g, w, concept), 0))
            rows.append({"source_group": g, "week_start": w, "complete_week": w in complete, "concept": concept,
                         "count": n, "per_1000_words": round(1000 * n / total, 3)})
    weekly = pd.DataFrame(rows)

    # 3. and 4. context: terms of the posts that mention a country
    df["terms"] = post_terms(df)
    peak_rows, framing_rows = [], []
    for concept in concepts:
        sub = df.loc[long.loc[long["concept"] == concept, "post"].unique()]
        if sub.empty:
            continue
        per_week = weekly[(weekly["concept"] == concept) & weekly["complete_week"]].groupby("week_start")["count"].sum()
        words_week = df[df["week_start"].isin(complete)].groupby("week_start")["word_count"].sum()
        value = (1000 * per_week / words_week).dropna()
        all_terms = Counter(t for ts in sub["terms"] for t in ts)
        for peak, (week, v) in enumerate(value.nlargest(PEAK_WEEKS).items(), start=1):
            target = Counter(t for ts in sub.loc[sub["week_start"] == week, "terms"] for t in ts)
            for rank, r in enumerate(top(typical.log_odds(target, all_terms - target, all_terms)).itertuples(), 1):
                peak_rows.append({"country": concept, "label": LABELS.get(concept, ""), "peak": peak,
                                  "week_start": week, "per_1000_words": round(v, 3), "rank": rank, "term": r.term,
                                  "z": round(r.z, 1), "count": r.count})
        for g in GROUPS:
            mine = sub[sub["source_group"] == g]
            if len(mine) < MIN_POSTS:
                continue
            target = Counter(t for ts in mine["terms"] for t in ts)
            for rank, r in enumerate(top(typical.log_odds(target, all_terms - target, all_terms)).itertuples(), 1):
                framing_rows.append({"country": concept, "label": LABELS.get(concept, ""), "group": g, "rank": rank,
                                     "term": r.term, "z": round(r.z, 1), "count": r.count, "posts": len(mine)})
    peaks = pd.DataFrame(peak_rows)
    framing = pd.DataFrame(framing_rows)

    # save
    (OUTPUT_DIR / "charts").mkdir(parents=True, exist_ok=True)
    overview.to_csv(OUTPUT_DIR / "countries.csv", index=False, encoding="utf-8-sig")
    weekly.to_csv(OUTPUT_DIR / "countries_weekly.csv", index=False, encoding="utf-8-sig")
    peaks.to_csv(OUTPUT_DIR / "peak_weeks.csv", index=False, encoding="utf-8-sig")
    framing.to_csv(OUTPUT_DIR / "framing.csv", index=False, encoding="utf-8-sig")
    groups_all = overview[(overview["level"] == "group") & (overview["phase"] == ALL)]
    wide = groups_all.pivot_table(index=["concept", "label"], columns="name", values="per_1000_words")[GROUPS]
    wide["count_all"] = groups_all.groupby(["concept", "label"])["count"].sum()
    by_phase = overview[overview["level"] == "group"].pivot_table(index=["concept", "label"], columns=["phase", "name"],
                                                                  values="per_1000_words")
    by_phase = by_phase.reindex(columns=pd.MultiIndex.from_product([[ALL] + phases, GROUPS]))
    by_phase.columns = [f"{p} – {g}" for p, g in by_phase.columns]
    with pd.ExcelWriter(OUTPUT_DIR / "countries.xlsx") as xl:
        wide.sort_values("count_all", ascending=False).to_excel(xl, sheet_name="overview")
        by_phase.to_excel(xl, sheet_name="phases")
        peaks.to_excel(xl, sheet_name="peak_weeks", index=False)
        framing.to_excel(xl, sheet_name="framing", index=False)
    for filename, (title, items) in REGIONS.items():
        small_multiples(weekly[weekly["complete_week"]], items, title, filename)
    print(f"saved to {OUTPUT_DIR} ({len(REGIONS)} charts in charts/)\n")

    print(wide.sort_values("count_all", ascending=False).round(2).to_string(), "\n")
    for concept in ["امارات", "پاکستان", "عربستان", "چین", "روسیه"]:
        for g in GROUPS:
            t = framing[(framing["country"] == concept) & (framing["group"] == g)]["term"].head(10)
            print(f"{LABELS.get(concept, concept)} | {g}: " + "  |  ".join(t))


if __name__ == "__main__":
    main()
