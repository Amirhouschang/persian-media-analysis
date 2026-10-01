"""
03e_topics.py – Topics of the main run: weighted shares per source group, channel and phase
===========================================================================================

RUN (in the folder scripts/ai, after the main run and 03c_validation.py):
  python 03e_topics.py

WHAT IT DOES
  Reads the main-run results (data/ki/classification_<model>_..._<version>.csv) and computes the share of every
  topic per source group, channel and phase. Every post counts with its weight (column 'gewicht' = posts of its
  channel-week / drawn posts), so the shares describe all posts with more than 80 characters, not only the sample.
  A group is the sum of its channels (larger channels count more, as in the word analysis).

  Only TOPICS are evaluated. The TONE is not compared between groups: in the final validation (Phase C) the AI
  recognised only 45% of the non-neutral posts, and this varied by group (state 8% instead of 20% non-neutral,
  IRGC-affiliated 18% instead of 21%). AI tone shares would therefore show differences between groups that the
  manual coding does not show. See docs/en/03_ai_classification.md.

  Known direction of the topic errors (Phase C): 'military' is assigned too often (32 AI vs 21 manual of 200),
  'diplomacy' too rarely (21 vs 31) – mostly analyses of the war. Changes over time are more reliable than levels.

OUTPUT (folder results/ai/topics – numbers only)
  topic_shares.csv     – level (group/channel), name, phase, topic, posts_drawn, share_pct (weighted)
  topic_shares.xlsx    – sheets groups (group × phase × topic) and channels
  charts/topics_by_phase.png – one panel per topic: share per phase, one line per source group
"""

import re
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import ai_config as cfg
import ai_core as core

TARGET = cfg.PROJECT / "results" / "ai" / "topics"
GROUPS = {"irna_1313": "state", "iribnews": "state", "mehrnews": "state",
          "Tasnimnews": "irgc_affiliated", "farsna": "irgc_affiliated", "jamarannews": "reformist"}
CHANNELS = {"irna_1313": "IRNA", "iribnews": "IRIB News", "mehrnews": "Mehr News",
            "Tasnimnews": "Tasnim News", "farsna": "Fars News", "jamarannews": "Jamaran"}
# phase boundaries as in the database; the database assigns days by UTC date, here the date is converted to Tehran time
PHASES = [("before_war", None, "2026-02-27"), ("war", "2026-02-28", "2026-04-07"),
          ("ceasefire", "2026-04-08", "2026-07-07"), ("after_truce_collapse", "2026-07-08", None)]
PHASE_LABELS = {"before_war": "before war", "war": "war", "ceasefire": "ceasefire",
                "after_truce_collapse": "after collapse"}
ALL = "all"

# chart style as in scripts/analysis/09_timeline.py
GROUP_LABELS = {"state": "State", "irgc_affiliated": "IRGC-affiliated", "reformist": "Reformist (Jamaran)"}
COLORS = {"state": "#2a78d6", "irgc_affiliated": "#c42f2f", "reformist": "#1baf7a"}
INK, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#e1e0d9", "#fcfcfb"


def main_run_file():
    model = re.sub(r"[^a-zA-Z0-9.]+", "-", cfg.CLASSIFICATION_MODEL)      # as in 03_ai_classify.py
    context = "context" if cfg.CLASSIFICATION_CONTEXT else "no-context"
    return cfg.OUTPUT_DIR / f"classification_{model}_{context}_{core.CODEBOOK_VERSION}.csv"


def phase_of(day):
    for name, start, end in PHASES:
        if (start is None or day >= start) and (end is None or day <= end):
            return name


def shares(df, key, names):
    rows = []
    for phase in [ALL] + [p for p, _, _ in PHASES]:
        part = df if phase == ALL else df[df["phase"] == phase]
        for name in names:
            g = part[part[key] == name]
            total = g["gewicht"].sum()
            for topic in core.TOPICS:
                t = g[g["topic"] == topic]
                rows.append({"name": name, "phase": phase, "topic": topic, "posts_drawn": len(t),
                             "share_pct": round(100 * t["gewicht"].sum() / total, 1) if total else float("nan")})
    return pd.DataFrame(rows)


def chart(groups_table, filename):
    topics = list(core.TOPICS)
    phases = [p for p, _, _ in PHASES]
    fig, axes = plt.subplots(3, 3, figsize=(11, 8.5), dpi=150, sharex=True)
    fig.patch.set_facecolor(SURFACE)
    top = groups_table[groups_table["phase"] != ALL]["share_pct"].max()
    for ax, topic in zip(axes.flat, topics):
        ax.set_facecolor(SURFACE)
        for g in GROUP_LABELS:
            s = groups_table[(groups_table["name"] == g) & (groups_table["topic"] == topic)].set_index("phase")
            s = s.reindex(phases)["share_pct"]
            ax.plot(range(len(phases)), s.values, color=COLORS[g], linewidth=2, marker="o", markersize=5,
                    markeredgecolor=SURFACE, markeredgewidth=1.5, label=GROUP_LABELS[g], zorder=3)
        ax.set_title(topic, loc="left", fontsize=10, color=INK)
        ax.set_ylim(0, top * 1.08)
        ax.grid(axis="y", color=GRID, linewidth=1)
        ax.set_axisbelow(True)
        for side in ["top", "right", "left"]:
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#c3c2b7")
        ax.tick_params(colors=MUTED, labelsize=8, length=0)
        ax.set_xticks(range(len(phases)))
        ax.set_xticklabels([PHASE_LABELS[p] for p in phases], fontsize=7)
    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", ncol=3, frameon=False, fontsize=8, labelcolor=INK)
    fig.suptitle("Topics per phase (AI classification, weighted share of posts in %)", x=0.01, ha="left",
                 fontsize=12, color=INK)
    fig.text(0.01, 0.01, "Gemma 4 31B, codebook v8; 10,750 posts, weighted. Final validation: topic correct in 72.5% "
             "(95% CI 65.9–78.2%); 'military' tends to be over-, 'diplomacy' under-estimated.",
             fontsize=7, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.94))
    fig.savefig(TARGET / "charts" / f"{filename}.png", facecolor=SURFACE)
    plt.close(fig)


def main():
    path = main_run_file()
    df = pd.read_csv(path)
    df["group"] = df["kanal"].map(GROUPS)
    day = pd.to_datetime(df["datum"], utc=True).dt.tz_convert("Asia/Tehran").dt.strftime("%Y-%m-%d")
    df["phase"] = day.map(phase_of)
    print(f"{path.name}: {len(df)} posts, weights sum to {df['gewicht'].sum():,.0f} posts")

    groups = shares(df, "group", list(GROUP_LABELS))
    groups.insert(0, "level", "group")
    channels = shares(df, "kanal", list(CHANNELS))
    channels["name"] = channels["name"].map(CHANNELS)
    channels.insert(0, "level", "channel")
    table = pd.concat([groups, channels], ignore_index=True)

    (TARGET / "charts").mkdir(parents=True, exist_ok=True)
    table.to_csv(TARGET / "topic_shares.csv", index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(TARGET / "topic_shares.xlsx") as xl:
        for level, part in table.groupby("level", sort=False):
            wide = part.pivot_table(index="topic", columns=["phase", "name"], values="share_pct")
            order = [ALL] + [p for p, _, _ in PHASES]
            wide = wide.reindex(columns=[c for o in order for c in wide.columns if c[0] == o])
            wide.columns = [f"{p} – {n}" for p, n in wide.columns]
            wide.to_excel(xl, sheet_name=f"{level}s")
    chart(groups, "topics_by_phase")

    wide = groups.pivot_table(index="topic", columns=["phase", "name"], values="share_pct")
    print("\nShare in % per group, whole period:")
    print(wide[ALL][list(GROUP_LABELS)].round(1).to_string())
    for g in GROUP_LABELS:
        print(f"\n{GROUP_LABELS[g]} per phase:")
        print(wide.xs(g, axis=1, level="name")[[p for p, _, _ in PHASES]].round(1).to_string())
    print(f"\nSaved to {TARGET}")


if __name__ == "__main__":
    main()
