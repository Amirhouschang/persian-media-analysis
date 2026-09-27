"""
10_activity.py – How active are the channels, and how many people do they reach?
==================================================================================

RUN (in the folder scripts/analysis):
  python 10_activity.py

WHAT IT DOES
  For every source group and every channel – per phase and per calendar week:
    posts_per_day_per_channel  – posts per day; for a group divided by its number of channels,
                                 so the group with three channels is not automatically "more active"
    views_median / views_mean  – views per post (median = the typical post, not pulled up by a few viral posts)
    forwards_median / _mean    – how often a post was forwarded
    forwards_per_1000_views    – forwards per 1,000 views: how much readers pass the posts on
  All posts are counted, also images and videos without text.

LIMITATION
  Views and forwards are the numbers at the time of collection. Posts from the last days before the collection
  had less time to collect views – therefore the last, incomplete week is left out of the charts (as in 09).
  Views count readers of the channel, not unique people.

OUTPUT (folder results/activity, only numbers – no post texts)
  activity.xlsx          – sheet 'phases' (groups and channels, whole period and per phase), sheet 'weekly'
  activity_phases.csv    – the same as the sheet 'phases'
  activity_weekly.csv    – the same as the sheet 'weekly' (for the dashboard)
  charts/*.png           – posts per day, median views, forwards per 1,000 views per source group
                           (same style and events as 09_timeline.py)
"""
import importlib.util
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("timeline", HERE / "09_timeline.py")   # same chart style and events
timeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(timeline)

DATABASE_URL = "postgresql+psycopg:///iran_media_2026"
OUTPUT_DIR = HERE.parents[1] / "results" / "activity"
ALL = "all"
GROUPS = ["state", "irgc_affiliated", "reformist"]
METRICS = ["posts", "days", "posts_per_day_per_channel", "views_median", "views_mean", "forwards_median",
           "forwards_mean", "forwards_per_1000_views"]

# (metric, English title, file name)
CHARTS = [
    ("posts_per_day_per_channel", "Posts per day and channel", "posts_per_day"),
    ("views_median", "Views per post (median)", "views_median"),
    ("forwards_per_1000_views", "Forwards per 1,000 views", "forwards_per_1000_views"),
]


def read_data(engine):
    posts = pd.read_sql(text("""
        SELECT c.channel_id, c.name AS channel, g.group_id, g.name AS source_group,
               ph.phase_id, ph.name AS phase, d.date, d.week_start, p.views, p.forwards
        FROM posts p
        JOIN channels c       ON c.channel_id = p.channel_id
        JOIN source_groups g  ON g.group_id   = c.group_id
        JOIN dates d          ON d.date_key   = p.date_key
        JOIN phases ph        ON ph.phase_id  = d.phase_id
    """), engine)
    days = pd.read_sql(text("""
        SELECT d.date, d.week_start, ph.phase_id, ph.name AS phase
        FROM dates d JOIN phases ph ON ph.phase_id = d.phase_id
    """), engine)                                                  # calendar days, also days without any post
    return posts, days


def metrics(part, days, n_channels):
    seen = part[part["views"].notna()]
    views, forwards = seen["views"], seen["forwards"].fillna(0)
    return {
        "posts": len(part),
        "days": days,
        "posts_per_day_per_channel": round(len(part) / days / n_channels, 1),
        "views_median": views.median() if len(seen) else None,
        "views_mean": round(views.mean()) if len(seen) else None,
        "forwards_median": forwards.median() if len(seen) else None,
        "forwards_mean": round(forwards.mean(), 1) if len(seen) else None,
        "forwards_per_1000_views": round(1000 * forwards.sum() / views.sum(), 2) if views.sum() else None,
    }


def main():
    engine = create_engine(DATABASE_URL)
    posts, days = read_data(engine)
    print(f"{len(posts)} posts, {posts['views'].notna().sum()} with a view count")

    channels = posts.drop_duplicates("channel").sort_values("channel_id")
    phases = days.drop_duplicates("phase").sort_values("phase_id")["phase"].tolist()
    units = [("group", g, channels.loc[channels["source_group"] == g, "channel"].tolist()) for g in GROUPS]
    units += [("channel", ch, [ch]) for ch in channels["channel"]]

    first, last = days["date"].min(), days["date"].max()
    week_days = days.groupby("week_start").size()                  # 7, or fewer in the first/last week
    phase_rows, week_rows = [], []
    for level, name, members in units:
        mine = posts[posts["channel"].isin(members)]
        for phase in [ALL] + phases:
            part = mine if phase == ALL else mine[mine["phase"] == phase]
            n_days = len(days) if phase == ALL else int((days["phase"] == phase).sum())
            phase_rows.append({"level": level, "name": name, "phase": phase, **metrics(part, n_days, len(members))})
        for week, part in mine.groupby("week_start"):
            week_rows.append({"level": level, "name": name, "week_start": week,
                              "complete_week": bool(week_days[week] == 7),
                              **metrics(part, int(week_days[week]), len(members))})
    by_phase = pd.DataFrame(phase_rows)
    weekly = pd.DataFrame(week_rows)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    by_phase.to_csv(OUTPUT_DIR / "activity_phases.csv", index=False, encoding="utf-8-sig")
    weekly.to_csv(OUTPUT_DIR / "activity_weekly.csv", index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUTPUT_DIR / "activity.xlsx") as xl:
        by_phase.to_excel(xl, sheet_name="phases", index=False)
        weekly.to_excel(xl, sheet_name="weekly", index=False)

    # charts: same function as 09_timeline.py, only complete weeks, one line per source group
    long = weekly[(weekly["level"] == "group") & weekly["complete_week"]].melt(
        id_vars=["level", "name", "week_start"], value_vars=[m for m, _, _ in CHARTS],
        var_name="concept", value_name="value")
    long["category"] = "activity"
    timeline.OUTPUT_DIR = OUTPUT_DIR
    (OUTPUT_DIR / "charts").mkdir(exist_ok=True)
    for metric, title, filename in CHARTS:
        timeline.chart(long, "value", "activity", metric, title, filename, GROUPS)

    print(f"period {first} – {last}; saved to {OUTPUT_DIR} ({len(CHARTS)} charts in charts/)\n")
    show = by_phase[by_phase["phase"] == ALL].drop(columns=["phase", "days"])
    print(show.to_string(index=False))


if __name__ == "__main__":
    main()
