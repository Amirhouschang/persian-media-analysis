"""
09_timeline.py – Week by week: how the naming and the key terms change over time
==================================================================================

RUN (in the folder scripts/analysis, after 08_naming.py works):
  python 09_timeline.py

WHAT IT DOES
  Counts every concept of naming_terms.csv (same rules as 08_naming.py) plus a few extra single words
  (EXTRA_TERMS) per calendar week, for every source group and every channel:
    - per 1,000 words
    - share within the category (e.g. share of رژیم صهیونیستی among all names for Israel)
  Key events are marked in the charts (EVENTS).

OUTPUT (folder results/timeline, only numbers – no post texts)
  timeline.csv   – everything as one long table (for the dashboard)
  timeline.xlsx  – one sheet per category: weeks in rows, group × concept in columns (per 1,000 words)
  charts/*.png   – line charts of the key concepts per source group (CHARTS); only complete weeks – the first
                   week (29.12.–04.01., data from 01.01.) and the last week (only 31.08.) are left out of the
                   charts, because values from a few days jump by chance. They stay in timeline.csv/xlsx.
"""
import importlib.util
import datetime as dt
from collections import Counter
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sqlalchemy import create_engine, text

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("naming", HERE / "08_naming.py")   # same concepts and counting rules
naming_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(naming_module)

OUTPUT_DIR = HERE.parents[1] / "results" / "timeline"
EXTRA_TERMS = ["شهید", "اینترنت"]                    # single words followed in addition to naming_terms.csv

# (date, label, side of the line the label stands on) – war begins left, new leader right: they are only 8 days apart
EVENTS = [(dt.date(2026, 2, 28), "war begins", "left"), (dt.date(2026, 3, 8), "new leader", "right"),
          (dt.date(2026, 4, 8), "ceasefire", "right"), (dt.date(2026, 7, 8), "ceasefire collapses", "right")]

# (value, category, concept or None for the whole category, English title, file name)
CHARTS = [
    ("share_pct", "israel_naming", "رژیم صهیونیستی", "Share of 'Zionist regime' among all names for Israel (%)",
     "israel_zionist_regime_share"),
    ("share_pct", "usa_naming", "ایالات متحده", "Share of 'United States' among all names for the USA (%)",
     "usa_united_states_share"),
    ("per_1000_words", "diplomacy", "مذاکره / مذاکرات", "'Negotiation(s)' per 1,000 words", "negotiations"),
    ("per_1000_words", "diplomacy", "آتش‌بس", "'Ceasefire' per 1,000 words", "ceasefire"),
    ("per_1000_words", "revenge", None, "Revenge terms (all) per 1,000 words", "revenge"),
    ("per_1000_words", "labels_opponents", None, "Labels for opponents (traitor, mercenary, rioter ...) per 1,000 words",
     "labels_opponents"),
    ("per_1000_words", "crimes", None, "Crime terms (genocide, child-killer, war crimes ...) per 1,000 words", "crimes"),
    ("per_1000_words", "persons", "ترامپ", "'Trump' per 1,000 words", "trump"),
    ("per_1000_words", "persons", "قالیباف", "'Ghalibaf' per 1,000 words", "ghalibaf"),
    ("per_1000_words", "extra_terms", "شهید", "'Martyr' per 1,000 words", "martyr"),
    ("per_1000_words", "extra_terms", "اینترنت", "'Internet' per 1,000 words", "internet"),
]
GROUP_LABELS = {"state": "State", "irgc_affiliated": "IRGC-affiliated", "reformist": "Reformist (Jamaran)"}
COLORS = {"state": "#2a78d6", "irgc_affiliated": "#c42f2f", "reformist": "#1baf7a"}   # blue, red, green – checked for colour blindness
INK, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#e1e0d9", "#fcfcfb"


def read_posts(engine):
    return pd.read_sql(text("""
        SELECT c.channel_id, c.name AS channel, g.group_id, g.name AS source_group,
               d.date, d.week_start, p.text_clean, p.word_count
        FROM posts p
        JOIN channels c       ON c.channel_id = p.channel_id
        JOIN source_groups g  ON g.group_id   = c.group_id
        JOIN dates d          ON d.date_key   = p.date_key
        WHERE p.word_count > 0
    """), engine)


def build_table(df, naming):
    counts, words = {}, {}
    for (channel, week), part in df.groupby(["channel", "week_start"]):
        counts[(channel, week)] = naming_module.count_part("\n".join(part["text_clean"]), naming)
        words[(channel, week)] = part["word_count"].sum()

    channels = df.drop_duplicates("channel").sort_values("channel_id")
    concepts = naming[["category", "concept"]].drop_duplicates()
    weeks = sorted(df["week_start"].unique())
    rows = []
    for level, names, members in [
        ("group", channels.drop_duplicates("source_group").sort_values("group_id")["source_group"].tolist(),
         lambda n: channels.loc[channels["source_group"] == n, "channel"].tolist()),
        ("channel", channels["channel"].tolist(), lambda n: [n]),
    ]:
        for name in names:
            for week in weeks:
                c, total = Counter(), 0
                for ch in members(name):
                    c += counts.get((ch, week), Counter())
                    total += words.get((ch, week), 0)
                if not total:
                    continue
                for cat, concept in concepts.itertuples(index=False):
                    n = c[(cat, concept)]
                    rows.append({"level": level, "name": name, "week_start": week, "category": cat,
                                 "concept": concept, "count": n, "per_1000_words": 1000 * n / total})
    table = pd.DataFrame(rows)
    cat_total = table.groupby(["level", "name", "week_start", "category"])["count"].transform("sum")
    table["share_pct"] = (100 * table["count"] / cat_total.where(cat_total > 0)).round(1)
    table["per_1000_words"] = table["per_1000_words"].round(3)
    return table


def chart(table, value, category, concept, title, filename, groups):
    part = table[(table["level"] == "group") & (table["category"] == category)]
    if concept is None:                                               # whole category: sum of its concepts
        series = part.groupby(["name", "week_start"])["per_1000_words"].sum().unstack("name")
    else:
        series = part[part["concept"] == concept].pivot(index="week_start", columns="name", values=value)
    series.index = pd.to_datetime(series.index)

    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for day, label, side in EVENTS:                          # label next to its line, all at the same height
        ax.axvline(pd.Timestamp(day), color="#c3c2b7", linewidth=1, zorder=1)
        ax.annotate(label, (mdates.date2num(day), 0.99), xycoords=ax.get_xaxis_transform(),
                    xytext=(-4 if side == "left" else 4, 0), textcoords="offset points",
                    ha="right" if side == "left" else "left", va="top", fontsize=8, color=MUTED, zorder=5,
                    bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1))       # grid line not through the text
    drawn = False
    for g in groups:
        if g not in series:
            continue
        s = series[g].dropna()
        if s.empty:
            continue
        ax.plot(s.index, s.values, color=COLORS[g], linewidth=2, solid_capstyle="round", label=GROUP_LABELS[g],
                zorder=3)
        ax.plot(s.index[-1], s.values[-1], "o", color=COLORS[g], markersize=6,
                markeredgecolor=SURFACE, markeredgewidth=2, zorder=4)
        drawn = True
    ax.set_ylim(0, ax.get_ylim()[1] * 1.12)                    # free space at the top for the event labels
    if drawn:                                                  # legend top right, outside the plot: never on a line
        ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False, fontsize=8, labelcolor=INK)
    ax.set_title(title, loc="left", fontsize=11, color=INK, pad=12)
    ax.grid(axis="y", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.tick_params(colors=MUTED, labelsize=8, length=0)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.margins(x=0.02)
    fig.text(0.01, 0.01, "Weekly values (complete weeks only). Source: 6 Iranian Telegram channels, Jan–Aug 2026.", fontsize=7, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 0.9, 1))
    fig.savefig(OUTPUT_DIR / "charts" / f"{filename}.png", facecolor=SURFACE)
    plt.close(fig)


def main():
    engine = create_engine(naming_module.terms.DATABASE_URL)
    df = read_posts(engine)
    naming = naming_module.load_naming()
    extra = pd.DataFrame({"category": "extra_terms", "concept": EXTRA_TERMS, "variant": EXTRA_TERMS})
    extra["pattern"] = [naming_module.re.compile(f"(?<!{naming_module.LETTER}){w}(?!{naming_module.LETTER})")
                        for w in EXTRA_TERMS]
    extra["length"] = extra["variant"].str.len()
    naming = pd.concat([naming, extra], ignore_index=True)
    print(f"{len(df)} posts, {df['week_start'].nunique()} weeks, {naming[['category', 'concept']].drop_duplicates().shape[0]} concepts")

    table = build_table(df, naming)
    groups = ["state", "irgc_affiliated", "reformist"]

    (OUTPUT_DIR / "charts").mkdir(parents=True, exist_ok=True)
    table.to_csv(OUTPUT_DIR / "timeline.csv", index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUTPUT_DIR / "timeline.xlsx") as xl:
        for cat in naming["category"].unique():
            part = table[(table["level"] == "group") & (table["category"] == cat)]
            wide = part.pivot_table(index="week_start", columns=["name", "concept"], values="per_1000_words",
                                    dropna=False)
            wide.columns = [f"{n} – {c}" for n, c in wide.columns]
            wide.to_excel(xl, sheet_name=cat[:31])
    # charts: only complete weeks (7 days of data) – the first and last week have only a few days and jump
    first, last = pd.Timestamp(df["date"].min()), pd.Timestamp(df["date"].max())
    ws = pd.to_datetime(table["week_start"])
    complete = (ws >= first) & (ws + pd.Timedelta(days=6) <= last)
    dropped = sorted(ws[~complete].dt.date.unique())
    print(f"charts without incomplete weeks: {', '.join(str(d) for d in dropped)}")
    for c in CHARTS:
        chart(table[complete], *c, groups)
    print(f"saved to {OUTPUT_DIR} ({len(CHARTS)} charts in charts/)")


if __name__ == "__main__":
    main()
