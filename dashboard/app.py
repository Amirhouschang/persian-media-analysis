"""
app.py – Interactive dashboard: Iranian news channels on Telegram, 1 Jan – 31 Aug 2026
=====================================================================================

RUN (in the project folder):
  pip install -r dashboard/requirements.txt
  streamlit run dashboard/app.py

WHAT IT SHOWS (languages: Deutsch, English – switch at the top; the Persian terms stay in the original)
  Wording over time  – every term of naming_terms.csv per week: compare the three groups (or six channels) for one
                       term, or several terms for one source; with events, phases, highest weeks, average per phase
                       and the terms of the category compared
  Countries          – the same for 35 countries and actors, plus the most mentioned countries of a region
  Topics (AI)        – share of the topics per group and phase (10,750 posts classified by the local model)
  Activity           – posts, views and forwards per week

DATA
  Only the finished result tables in results/ are read (numbers, no post texts):
    results/timeline/timeline.csv                        (09_timeline.py)
    results/countries/countries.csv, countries_weekly.csv   (12_countries.py)
    results/ai/topics/topic_shares.csv                   (03e_topics.py)
    results/activity/activity_weekly.csv                 (10_activity.py)
  Translations of the terms in the selectors: dashboard/concepts.csv; all other texts: dashboard/i18n.py.
  RESULTS_DIR (environment variable) can point to another results folder.
"""

import math
import os
import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from i18n import (CATEGORIES, CHANNELS, EVENTS, GROUP_COLORS, GROUPS, LANGS, PHASE_FILL,
                  PHASE_NAMES, PHASES, REGIONS, TERM_COLORS, TOPICS, UI)

HERE = Path(__file__).resolve().parent
RESULTS = Path(os.environ.get("RESULTS_DIR", HERE.parent / "results"))
GROUP_KEYS = list(GROUPS)
CHANNEL_KEYS = list(CHANNELS)
ALL = "all"
SUM = "__sum__"

st.set_page_config(page_title="Iran Telegram 2026", page_icon="📊", layout="wide")


# ----------------------------------------------------------------------------------------------------------------
# data
# ----------------------------------------------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def read_csv(relative):
    path = RESULTS / relative
    if not path.exists():
        return None
    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except pd.errors.EmptyDataError:                      # a script that found nothing writes an empty table
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def concept_translations():
    table = pd.read_csv(HERE / "concepts.csv")
    return {(r.category, r.concept): {"en": r.en, "de": r.de} for r in table.itertuples()}


def load(relative, script, lang):
    """Reads a result table; shows a message and returns None when it is missing."""
    df = read_csv(relative)
    if df is None:
        st.warning(UI[lang]["missing"].format(file=f"results/{relative}", script=script))
    return df


def persian(concept):
    """The Persian term without the English note in brackets that naming_terms.csv adds to some concepts."""
    return re.sub(r"\s*\([A-Za-z][^)]*\)", "", concept).strip()


def term_label(category, concept, lang, with_persian=True):
    if concept == SUM:
        return UI[lang]["sum_category"]
    names = concept_translations().get((category, concept))
    base = names[lang] if names else concept
    return f"{base} · {persian(concept)}" if with_persian else base


def source_label(name, lang):
    if name in GROUPS:
        return GROUPS[name][lang]
    return name


def complete_weeks(df_weeks):
    """Complete weeks (7 days of data): from activity_weekly.csv, otherwise all but the first and last week."""
    act = read_csv("activity/activity_weekly.csv")
    if act is not None and "complete_week" in act:
        return set(act.loc[act["complete_week"].astype(str).str.lower() == "true", "week_start"])
    weeks = sorted(set(df_weeks))
    return set(weeks[1:-1])


# ----------------------------------------------------------------------------------------------------------------
# page style (right-to-left for Persian)
# ----------------------------------------------------------------------------------------------------------------
def inject_style():
    st.markdown("""<style>
.block-container {padding-top: 4rem; max-width: 1200px;}
h1 {font-size: 2rem !important;}
</style>""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------------------------------------------
# charts
# ----------------------------------------------------------------------------------------------------------------
PLOT_HEIGHT = 290        # height of the plot area in pixels (the margins for labels and legend come on top)
LABEL_ROW = 18           # height of one row of event labels above the plot


def line_chart(series, ytitle, lang, events=True, phases=True):
    """series: list of dicts with name, x (ISO week starts), y, color, dash.
    Event labels stand horizontally ABOVE the plot, phase names BELOW the axis and the legend at the very bottom, so
    that no line of the data runs through a text."""
    t = UI[lang]
    fig = go.Figure()
    for s in series:
        fig.add_trace(go.Scatter(x=s["x"], y=s["y"], name=s["name"], mode="lines+markers",
                                 line=dict(color=s["color"], width=2.6, dash=s.get("dash", "solid")),
                                 marker=dict(size=5), hovertemplate="%{y:.2f}"))
    for s in series:                                                       # the highest week of each line
        ys = pd.to_numeric(pd.Series(s["y"]), errors="coerce")
        if ys.notna().any() and ys.max() > 0:
            i = int(ys.idxmax())
            fig.add_trace(go.Scatter(x=[s["x"][i]], y=[ys[i]], mode="markers", showlegend=False, hoverinfo="skip",
                                     marker=dict(size=13, symbol="diamond", color=s["color"],
                                                 line=dict(color="white", width=1.5))))

    rows = max(level for _, level, _ in EVENTS) + 1
    top = 22 + rows * LABEL_ROW if events else 14
    legend_rows = math.ceil(sum(len(s["name"]) * 7 + 48 for s in series) / 1050) if len(series) > 1 else 0
    bottom = 32 + (26 if phases else 0) + (10 + 26 * legend_rows if legend_rows else 0)
    grey = "rgba(128,128,128,0.95)"

    if phases:
        for key, (start, end) in PHASES.items():
            end_edge = (pd.Timestamp(end) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
            fig.add_vrect(x0=start, x1=end_edge, fillcolor=PHASE_FILL[key], line_width=0, layer="below")
            mid = (pd.Timestamp(start) + (pd.Timestamp(end_edge) - pd.Timestamp(start)) / 2).strftime("%Y-%m-%d")
            fig.add_annotation(x=mid, y=0, yref="paper", yanchor="top", yshift=-32, text=PHASE_NAMES[key][lang],
                               showarrow=False, font=dict(size=13, color=grey))
    if events:
        for day, level, names in EVENTS:
            lift = 4 + level * LABEL_ROW                                   # pixels above the plot
            fig.add_shape(type="line", x0=day, x1=day, y0=0, y1=1 + lift / PLOT_HEIGHT, xref="x", yref="paper",
                          line=dict(color="rgba(128,128,128,0.55)", width=1), layer="above")
            fig.add_annotation(x=day, y=1, yref="paper", yanchor="bottom", yshift=lift, xanchor="left", xshift=3,
                               text=names[lang], showarrow=False, font=dict(size=12, color=grey))
    fig.update_layout(
        height=PLOT_HEIGHT + top + bottom, hovermode="x unified", margin=dict(l=10, r=10, t=top, b=bottom),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yref="container", y=0, yanchor="bottom", x=0, xanchor="left"),
        xaxis=dict(range=["2026-01-01", "2026-08-31"], hoverformat=f"{t['week_of']} %d.%m.%Y", showgrid=False,
                   tickmode="linear", tick0="2026-01-01", dtick="M1", tickformat="%d.%m." if lang == "de" else "%d %b"),
        yaxis=dict(title=ytitle, rangemode="tozero", gridcolor="rgba(128,128,128,0.2)"),
        separators=",." if lang == "de" else ".,")
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})


def finish(fig, lang, height):
    """Common look of the bar charts: transparent background, legend on top, number format of the language."""
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=34, b=10), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                                                 xanchor="left", x=0),
                      separators=",." if lang == "de" else ".,")
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})


def phase_chart(series, ytitle, lang):
    """Average weekly value of every line in the four phases (complete weeks that start in the phase)."""
    labels = [PHASE_NAMES[p][lang] for p in PHASES]
    fig = go.Figure()
    for s in series:
        frame = pd.DataFrame({"x": pd.to_datetime(s["x"]), "y": pd.to_numeric(pd.Series(s["y"]), errors="coerce")})
        means = [frame.loc[(frame["x"] >= pd.Timestamp(a)) & (frame["x"] <= pd.Timestamp(b)), "y"].mean()
                 for a, b in PHASES.values()]
        fig.add_trace(go.Bar(x=labels, y=means, name=s["name"], marker_color=s["color"], hovertemplate="%{y:.2f}"))
    fig.update_layout(barmode="group", bargap=0.25, hovermode="x unified")
    fig.update_yaxes(title=ytitle, rangemode="tozero", gridcolor="rgba(128,128,128,0.2)")
    finish(fig, lang, 340)


def ranking_chart(wide, labels, ytitle, lang):
    """Horizontal grouped bars: one row per term/country (wide.index), one bar per group (wide.columns)."""
    fig = go.Figure()
    for g in wide.columns:
        fig.add_trace(go.Bar(y=labels, x=wide[g], orientation="h", name=GROUPS[g][lang], marker_color=GROUP_COLORS[g],
                             hovertemplate="%{x:.2f}"))
    fig.update_layout(barmode="group", bargap=0.3, yaxis=dict(autorange="reversed"), hovermode="y unified")
    fig.update_xaxes(title=ytitle, rangemode="tozero", gridcolor="rgba(128,128,128,0.2)")
    finish(fig, lang, 80 + 56 * len(wide))


def term_ranking(tl, category, value, ytitle, lang, top=8):
    """The terms of a category compared: mean weekly value of each group over the whole period."""
    part = tl[(tl["level"] == "group") & (tl["category"] == category)].copy()
    part[value] = pd.to_numeric(part[value], errors="coerce")
    wide = part.pivot_table(index="concept", columns="name", values=value, aggfunc="mean")
    wide = wide.reindex(columns=[g for g in GROUP_KEYS if g in wide.columns])
    if wide.empty:
        return
    wide = wide.loc[wide.sum(axis=1).sort_values(ascending=False).index[:top]]
    ranking_chart(wide, [term_label(category, c, lang) for c in wide.index], ytitle, lang)


def country_ranking(overview, countries, value, ytitle, lang, top=12):
    """The most mentioned countries / actors of the chosen region over the whole period, per group."""
    part = overview[(overview["level"] == "group") & (overview["phase"] == ALL) & (overview["concept"].isin(countries))]
    wide = part.pivot_table(index="concept", columns="name", values=value, aggfunc="sum")
    wide = wide.reindex(columns=[g for g in GROUP_KEYS if g in wide.columns])
    if wide.empty:
        return
    wide = wide.loc[wide.sum(axis=1).sort_values(ascending=False).index[:top]]
    ranking_chart(wide, [term_label("countries_actors", c, lang) for c in wide.index], ytitle, lang)


def values_of(df, value_col, category, concept):
    """{source name: Series(week_start -> value)} for one concept or for the sum of the category."""
    part = df[df["category"] == category]
    if concept == SUM:
        s = part.groupby(["name", "week_start"])[value_col].sum()
    else:
        s = part[part["concept"] == concept].set_index(["name", "week_start"])[value_col]
    return {name: s.xs(name, level="name").sort_index() for name in s.index.get_level_values("name").unique()}


def series_by_source(df, value_col, category, concept, names, lang):
    by_name = values_of(df, value_col, category, concept)
    out = []
    for name in names:
        if name not in by_name:
            continue
        s = by_name[name]
        color, dash = GROUP_COLORS.get(name), "solid"
        if name in CHANNELS:
            color, dash = CHANNELS[name][1], CHANNELS[name][2]
        out.append({"name": source_label(name, lang), "x": list(s.index), "y": list(s.values),
                    "color": color or "#7a7a7a", "dash": dash})
    return out


def series_by_term(df, value_col, category, concepts, source, lang):
    out = []
    for i, concept in enumerate(concepts):
        s = values_of(df, value_col, category, concept).get(source)
        if s is None:
            continue
        out.append({"name": term_label(category, concept, lang, with_persian=False), "x": list(s.index),
                    "y": list(s.values), "color": TERM_COLORS[i % len(TERM_COLORS)]})
    return out


def control(kind, host, label, key, lang, options=None, default=None, **kw):
    """selectbox / radio / multiselect / checkbox whose choice survives a change of language.
    Streamlit loses the selection of a widget when its labels change. Every language therefore gets its own widget
    (key + language); the language-independent choice is kept in session_state and used as its start value."""
    shared = f"choice_{key}"
    value = st.session_state.get(shared, default)
    wkey = f"{key}__{lang}"
    if kind == "checkbox":
        out = host.checkbox(label, value=bool(value), key=wkey)
    elif kind == "multiselect":
        out = host.multiselect(label, options, default=[v for v in (value or []) if v in options], key=wkey, **kw)
    else:
        index = options.index(value) if value in options else (options.index(default) if default in options else 0)
        out = getattr(host, kind)(label, options, index=index, key=wkey, **kw)
    st.session_state[shared] = out
    return out


def source_options(df):
    """Sources of a table: the three groups and the channels (as far as the table has them)."""
    names = set(df["name"])
    return [n for n in GROUP_KEYS + CHANNEL_KEYS if n in names]


# ----------------------------------------------------------------------------------------------------------------
# tab: wording over time
# ----------------------------------------------------------------------------------------------------------------
def tab_time(lang):
    t = UI[lang]
    tl = load("timeline/timeline.csv", "09_timeline.py", lang)
    if tl is None:
        return
    tl = tl[tl["category"] != "countries_actors"]                           # countries have their own tab
    tl = tl[tl["week_start"].isin(complete_weeks(tl["week_start"]))]
    categories = [c for c in CATEGORIES if c in set(tl["category"])]
    if not categories:
        return

    row1 = st.columns([3, 3, 3])                 # category | compare | source(s)
    row2 = st.columns([7, 4])                    # term(s), wide | value
    category = control("selectbox", row1[0], t["category"], "tl_cat", lang, categories, "israel_naming",
                       format_func=lambda c: CATEGORIES[c][lang])
    view = control("radio", row1[1], t["view"], "tl_view", lang, ["groups", "terms"], "groups", horizontal=True,
                   format_func=lambda v: t["view_groups"] if v == "groups" else t["view_terms"])
    concepts = list(dict.fromkeys(tl.loc[tl["category"] == category, "concept"]))
    defaults = {"israel_naming": "رژیم صهیونیستی", "usa_naming": "ایالات متحده", "persons": "ترامپ",
                "diplomacy": "آتش‌بس", "extra_terms": "شهید"}
    default = defaults.get(category, concepts[0])
    default = default if default in concepts else concepts[0]

    if view == "groups":
        concept = control("selectbox", row2[0], t["term"], f"tl_term_{category}", lang, [SUM] + concepts, default,
                          format_func=lambda c: term_label(category, c, lang))
        level = control("radio", row1[2], t["level"], "tl_level", lang, ["group", "channel"], "group", horizontal=True,
                        format_func=lambda v: t["by_groups"] if v == "group" else t["by_channels"])
        chosen = [concept]
    else:
        chosen = control("multiselect", row2[0], t["terms"], f"tl_terms_{category}", lang, concepts, [default],
                         max_selections=len(TERM_COLORS), format_func=lambda c: term_label(category, c, lang))
        source = control("selectbox", row1[2], t["source"], "tl_source", lang, source_options(tl), "state",
                         format_func=lambda n: source_label(n, lang))
    values = ["per_1000_words", "share_pct", "count"]
    if view == "groups" and chosen[0] == SUM:
        values = ["per_1000_words", "count"]
    labels = {"per_1000_words": t["v_per1000"], "share_pct": t["v_share"], "count": t["v_count"]}
    start = "share_pct" if category in ("israel_naming", "usa_naming") and "share_pct" in values else "per_1000_words"
    value = control("radio", row2[1], t["value"], f"tl_value_{category}_{view}", lang, values, start,
                    format_func=lambda v: labels[v])
    ytitle = {"per_1000_words": t["y_per1000"], "share_pct": t["y_share"], "count": t["y_count"]}[value]

    o1, o2, _ = st.columns([1, 1, 4])
    events = control("checkbox", o1, t["show_events"], "tl_events", lang, default=True)
    phases = control("checkbox", o2, t["show_phases"], "tl_phases", lang, default=True)

    if not chosen:
        st.info(t["select_one_term"])
        return
    if view == "groups":
        names = GROUP_KEYS if level == "group" else CHANNEL_KEYS
        part = tl[tl["level"] == level]
        series = series_by_source(part, value, category, chosen[0], names, lang)
        st.markdown(f"#### {term_label(category, chosen[0], lang)}")
    else:
        part = tl[tl["level"] == ("group" if source in GROUPS else "channel")]
        series = series_by_term(part, value, category, chosen, source, lang)
        st.markdown(f"#### {source_label(source, lang)}")
    line_chart(series, ytitle, lang, events, phases)
    st.caption(t["complete_weeks"] + " " + t["peak_marker"] + " " + t["terms_note"])

    st.markdown(f"#### {t['phase_title']}")
    phase_chart(series, ytitle, lang)
    st.caption(t["phase_note"])
    st.markdown(f"#### {t['rank_title']}: {CATEGORIES[category][lang]}")
    term_ranking(tl, category, value, ytitle, lang)
    st.caption(t["rank_note"])


# ----------------------------------------------------------------------------------------------------------------
# tab: countries
# ----------------------------------------------------------------------------------------------------------------
def tab_countries(lang):
    t = UI[lang]
    weekly = load("countries/countries_weekly.csv", "12_countries.py", lang)
    overview = load("countries/countries.csv", "12_countries.py", lang)
    if weekly is None or overview is None:
        return
    weekly = weekly.rename(columns={"source_group": "name"})
    weekly["category"] = "countries_actors"
    weekly = weekly[weekly["complete_week"].astype(str).str.lower() == "true"]
    labelled = set(overview.loc[overview["label"].fillna("") != "", "concept"])

    row1 = st.columns([3, 3, 3])                 # region | compare | source
    row2 = st.columns([7, 4])                    # country / countries, wide | value
    regions = ["all"] + list(REGIONS)
    region = control("selectbox", row1[0], t["region"], "co_region", lang, regions, "all",
                     format_func=lambda r: t["all_regions"] if r == "all" else REGIONS[r][lang])
    in_region = [c for r in REGIONS.values() for c in r["concepts"]] if region == "all" else REGIONS[region]["concepts"]
    countries = [c for c in in_region if c in labelled]
    if not countries:
        st.info(t["select_one_term"])
        return
    view = control("radio", row1[1], t["view"], "co_view", lang, ["groups", "terms"], "groups", horizontal=True,
                   format_func=lambda v: t["view_groups_c"] if v == "groups" else t["view_terms_c"])

    if view == "groups":
        country = control("selectbox", row2[0], t["country"], f"co_country_{region}", lang, countries, countries[0],
                          format_func=lambda c: term_label("countries_actors", c, lang))
        chosen = [country]
    else:
        chosen = control("multiselect", row2[0], t["countries"], f"co_countries_{region}", lang, countries,
                         countries[:2], max_selections=len(TERM_COLORS),
                         format_func=lambda c: term_label("countries_actors", c, lang))
        source = control("selectbox", row1[2], t["source"], "co_source", lang, GROUP_KEYS, "state",
                         format_func=lambda n: source_label(n, lang))
    labels = {"per_1000_words": t["v_per1000"], "count": t["v_count"]}
    value = control("radio", row2[1], t["value"], "co_value", lang, list(labels), "per_1000_words",
                    format_func=lambda v: labels[v])
    ytitle = {"per_1000_words": t["y_per1000"], "count": t["y_count"]}[value]
    o1, o2, _ = st.columns([1, 1, 4])
    events = control("checkbox", o1, t["show_events"], "co_events", lang, default=True)
    phases = control("checkbox", o2, t["show_phases"], "co_phases", lang, default=True)

    if not chosen:
        st.info(t["select_one_term"])
        return
    if view == "groups":
        series = series_by_source(weekly, value, "countries_actors", chosen[0], GROUP_KEYS, lang)
        st.markdown(f"#### {term_label('countries_actors', chosen[0], lang)}")
    else:
        series = series_by_term(weekly, value, "countries_actors", chosen, source, lang)
        st.markdown(f"#### {source_label(source, lang)}")
    line_chart(series, ytitle, lang, events, phases)
    st.caption(t["complete_weeks"] + " " + t["peak_marker"] + " " + t["countries_note"])

    country = chosen[0]
    name = term_label("countries_actors", country, lang)

    st.markdown(f"#### {t['phases_title']}: {name}")
    part = overview[(overview["level"] == "group") & (overview["concept"] == country)]
    if not part.empty:
        wide = part.pivot_table(index="name", columns="phase", values="per_1000_words")
        order = [p for p in [ALL] + list(PHASES) if p in wide.columns]
        wide = wide.reindex(index=[g for g in GROUP_KEYS if g in wide.index], columns=order)
        fig = go.Figure()
        for g in wide.index:
            fig.add_trace(go.Bar(x=[t["all_period"] if p == ALL else PHASE_NAMES[p][lang] for p in order],
                                 y=wide.loc[g].values, name=GROUPS[g][lang], marker_color=GROUP_COLORS[g],
                                 hovertemplate="%{y:.2f}"))
        fig.update_layout(barmode="group", bargap=0.25, hovermode="x unified")
        fig.update_yaxes(title=t["y_per1000"], rangemode="tozero", gridcolor="rgba(128,128,128,0.2)")
        finish(fig, lang, 340)

    st.markdown(f"#### {t['rank_title_c']}")
    country_ranking(overview, countries, value, ytitle, lang)
    st.caption(t["rank_note_c"])


# ----------------------------------------------------------------------------------------------------------------
# tab: topics (AI)
# ----------------------------------------------------------------------------------------------------------------
def tab_topics(lang):
    t = UI[lang]
    df = load("ai/topics/topic_shares.csv", "03e_topics.py", lang)
    if df is None:
        return
    st.warning(t["topics_warn"])
    c1, c2, c3 = st.columns(3)
    level = control("radio", c1, t["topic_level"], "tp_level", lang, ["group", "channel"], "group", horizontal=True,
                    format_func=lambda v: t["by_groups"] if v == "group" else t["by_channels"])
    view = control("radio", c2, t["topic_view"], "tp_view", lang, ["bars", "lines"], "bars", horizontal=True,
                   format_func=lambda v: t["topic_v_bars"] if v == "bars" else t["topic_v_lines"])
    part = df[df["level"] == level]
    names = [n for n in (GROUP_KEYS if level == "group" else CHANNEL_KEYS) if n in set(part["name"])]
    phase_keys = [ALL] + list(PHASES)
    phase_label = lambda p: t["all_period"] if p == ALL else PHASE_NAMES[p][lang]

    fig = go.Figure()
    if view == "bars":
        phase = control("selectbox", c3, t["topic_phase"], "tp_phase", lang, phase_keys, ALL, format_func=phase_label)
        order = [k for k in TOPICS if k in set(part["topic"])]
        for n in names:
            s = part[(part["name"] == n) & (part["phase"] == phase)].set_index("topic").reindex(order)
            color = GROUP_COLORS.get(n) or CHANNELS.get(n, (0, "#7a7a7a"))[1]
            fig.add_trace(go.Bar(y=[TOPICS[k][lang] for k in order], x=s["share_pct"], name=source_label(n, lang),
                                 orientation="h", marker_color=color, customdata=s["posts_drawn"],
                                 hovertemplate="%{x:.1f} %  (n=%{customdata})"))
        fig.update_layout(barmode="group", yaxis=dict(autorange="reversed"), height=620)
    else:
        topic = control("selectbox", c3, t["topic"], "tp_topic", lang, list(TOPICS), "diplomacy",
                        format_func=lambda k: TOPICS[k][lang])
        for n in names:
            s = part[(part["name"] == n) & (part["topic"] == topic)].set_index("phase").reindex(list(PHASES))
            color, dash = GROUP_COLORS.get(n), "solid"
            if n in CHANNELS:
                color, dash = CHANNELS[n][1], CHANNELS[n][2]
            fig.add_trace(go.Scatter(x=[PHASE_NAMES[p][lang] for p in PHASES], y=s["share_pct"], name=source_label(n, lang),
                                     mode="lines+markers", line=dict(color=color, width=2.6, dash=dash),
                                     marker=dict(size=8), customdata=s["posts_drawn"],
                                     hovertemplate="%{y:.1f} %  (n=%{customdata})"))
        fig.update_layout(height=470, yaxis=dict(rangemode="tozero"))
    fig.update_layout(
        hovermode="y unified" if view == "bars" else "x unified", margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        separators=",." if lang == "de" else ".,")
    fig.update_xaxes(title=t["share"] if view == "bars" else None, gridcolor="rgba(128,128,128,0.2)")
    fig.update_yaxes(title=t["share"] if view == "lines" else None, gridcolor="rgba(128,128,128,0.2)")
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})
    st.caption("n = " + {"de": "klassifizierte Beiträge in der Stichprobe", "en": "classified posts in the sample"}[lang])


# ----------------------------------------------------------------------------------------------------------------
# tab: activity
# ----------------------------------------------------------------------------------------------------------------
def tab_activity(lang):
    t = UI[lang]
    act = load("activity/activity_weekly.csv", "10_activity.py", lang)
    if act is None:
        return
    act = act[act["complete_week"].astype(str).str.lower() == "true"].copy()
    act["category"] = "activity"
    metrics = {"posts_per_day_per_channel": t["m_posts"], "views_median": t["m_views"],
               "forwards_median": t["m_forwards"], "forwards_per_1000_views": t["m_fw1000"]}
    c1, c2, c3 = st.columns(3)
    metric = control("selectbox", c1, t["act_metric"], "ac_metric", lang, list(metrics), "posts_per_day_per_channel",
                     format_func=lambda m: metrics[m])
    level = control("radio", c2, t["level"], "ac_level", lang, ["group", "channel"], "group", horizontal=True,
                    format_func=lambda v: t["by_groups"] if v == "group" else t["by_channels"])
    o1, o2 = c3.columns(2)
    events = control("checkbox", o1, t["show_events"], "ac_events", lang, default=True)
    phases = control("checkbox", o2, t["show_phases"], "ac_phases", lang, default=True)
    part = act[act["level"] == level]
    series = series_by_source(part.assign(concept="x"), metric, "activity", "x",
                              GROUP_KEYS if level == "group" else CHANNEL_KEYS, lang)
    st.markdown(f"#### {metrics[metric]}")
    line_chart(series, metrics[metric], lang, events, phases)
    st.caption(t["complete_weeks"] + " " + t["act_note"])


# ----------------------------------------------------------------------------------------------------------------
# page
# ----------------------------------------------------------------------------------------------------------------
def main():
    if "lang" not in st.session_state:                       # first visit: language from the link (?lang=en) or German
        initial = st.query_params.get("lang", "de")
        st.session_state["lang"] = initial if initial in LANGS else "de"
    head, switch = st.columns([3, 2])
    with switch:
        lang = st.radio("Language", list(LANGS), horizontal=True, format_func=LANGS.get,
                        label_visibility="collapsed", key="lang")
    st.query_params["lang"] = lang
    inject_style()
    t = UI[lang]

    with head:
        st.title(t["title"])
    st.markdown(t["subtitle"])
    for col, (label, value) in zip(st.columns(4), [(t["kpi_posts"], "328.330" if lang == "de" else "328,330"),
                                                   (t["kpi_channels"], "6"), (t["kpi_groups"], "3"),
                                                   (t["kpi_days"], "243")]):
        col.metric(label, value)
    tabs = st.tabs([t["tab_time"], t["tab_countries"], t["tab_topics"], t["tab_activity"], t["tab_about"]])
    with tabs[0]:
        tab_time(lang)
    with tabs[1]:
        tab_countries(lang)
    with tabs[2]:
        tab_topics(lang)
    with tabs[3]:
        tab_activity(lang)
    with tabs[4]:
        st.markdown(t["about"])


main()
