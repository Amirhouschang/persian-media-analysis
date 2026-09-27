"""
07_typical_terms.py – Terms a source group or channel uses clearly MORE often than the others
==============================================================================================

RUN (in the folder scripts/analysis, after 03_terms.py):
  python 07_typical_terms.py

WHY
  The top lists of 03 are almost the same everywhere (ایران, آمریکا, جنگ ...). What distinguishes the sources are
  the terms one of them uses much more often than the others – e.g. رژیم صهیونیستی instead of اسرائیل.

METHOD – weighted log-odds ratio with an informative prior ("Fightin' Words", Monroe, Colaresi & Quinn 2008)
  For every term: how much more likely is it in one group than in all other groups, measured as a z-score.
  z > 1.96 = the difference is statistically clear; the larger z, the more typical the term.
  Rare terms get a weak weight (prior from all posts), so a term used 3 times does not win by chance.
  The terms are exactly those of 03_terms.py (fixed terms, corrections, merged names, ignored words left out).

COMPARISONS
  each source group against the two others  |  each channel against the five others
  each source group against the two others in every phase

GROUPS: every channel must agree
  A group is not simply the sum of its channels: IRNA has by far the most and longest posts and would decide
  what is "typical for state media" on its own. Therefore every channel of a group is compared with the channels
  of the OTHER groups, and a term only counts as typical for the group if it is typical for EACH of its channels.
  z of the group = the lowest z of its channels; column z_by_channel shows all of them.
  (The reformist group has one channel, Jamaran, so group and channel are the same there.)

OUTPUT (folder results/words)
  typical_terms.xlsx – sheet 'groups', sheet 'channels', one sheet per group with the four phases
  typical_terms.csv  – the same as one long table
                       (level, name, phase, rank, term, z, z_by_channel, count, per_1000, per_1000_rest)
"""
import importlib.util
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("terms", HERE / "03_terms.py")    # same terms as 03_terms.py
terms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(terms)

TOP_N = 200                     # terms per list
MIN_COUNT = 50                  # a term must occur at least this often in all posts
PRIOR_SIZE = 10_000             # strength of the prior (in words)
OUTPUT_DIR = terms.OUTPUT_DIR
ALL = terms.ALL
JOIN = terms.JOIN


def log_odds(target: Counter, rest: Counter, prior: Counter):
    """z-score of the weighted log-odds ratio for every term (target vs. rest)."""
    vocab = [t for t, n in prior.items() if n >= MIN_COUNT]
    y_i = np.array([target.get(t, 0) for t in vocab], dtype=float)
    y_j = np.array([rest.get(t, 0) for t in vocab], dtype=float)
    a = np.array([prior[t] for t in vocab], dtype=float)
    a = a / a.sum() * PRIOR_SIZE
    n_i, n_j, a0 = y_i.sum(), y_j.sum(), a.sum()
    delta = (np.log((y_i + a) / (n_i + a0 - y_i - a)) - np.log((y_j + a) / (n_j + a0 - y_j - a)))
    z = delta / np.sqrt(1 / (y_i + a) + 1 / (y_j + a))
    return pd.DataFrame({"term": vocab, "z": z, "count": y_i.astype(int),
                         "per_1000": 1000 * y_i / n_i, "per_1000_rest": 1000 * y_j / n_j})


def finish(r, level, name, phase):
    r = r[r["z"] > 1.96].sort_values("z", ascending=False).head(TOP_N)      # only clearly typical terms
    r.insert(0, "rank", range(1, len(r) + 1))
    r.insert(0, "phase", phase)
    r.insert(0, "name", name)
    r.insert(0, "level", level)
    r["term"] = r["term"].str.replace(JOIN, " ")
    return r.round({"z": 1, "per_1000": 3, "per_1000_rest": 3})


def compare(level, name, phase, target, rest, prior):
    r = log_odds(target, rest, prior)
    r["z_by_channel"] = ""
    return finish(r, level, name, phase)


def channel_z(target, rest, prior):
    """z of one channel; a channel that does not use the term more often than the rest gets no positive z."""
    r = log_odds(target, rest, prior).set_index("term")
    return r["z"].where(r["per_1000"] > r["per_1000_rest"], r["z"].clip(upper=0))


def compare_group(name, phase, members, outside, total, prior, phase_list):
    """Typical for the group = typical for EACH member channel against the channels of the other groups."""
    rest = total(outside, phase_list)
    group = log_odds(total(members, phase_list), rest, prior).set_index("term")
    per_channel = pd.DataFrame({ch: channel_z(total([ch], phase_list), rest, prior) for ch in members})
    group["z"] = per_channel.min(axis=1)
    group["z_by_channel"] = per_channel.round(1).apply(
        lambda row: " | ".join(f"{ch} {z}" for ch, z in row.items()), axis=1)
    return finish(group.reset_index(), "group", name, phase)


def wide(table, level, names, phases):
    blocks = []
    for name in names:
        for phase in phases:
            part = table[(table["level"] == level) & (table["name"] == name) & (table["phase"] == phase)]
            title = name if phase == ALL else f"{name} – {phase}"
            blocks.append(part[["term", "z"]].reset_index(drop=True).set_axis([title, "z"], axis=1))
    out = pd.concat(blocks, axis=1)
    out.index = out.index + 1
    out.index.name = "rank"
    return out


def main():
    engine = create_engine(terms.DATABASE_URL)
    df = terms.read_posts(engine)
    titles, added, removed, ignored, merge_map = terms.load_corrections()
    phrases = terms.find_phrases(df, titles, added, removed)
    phrase_counts = dict(zip(phrases["term"].str.replace(" ", JOIN), phrases["count"]))
    counts, _ = terms.count_terms(df, phrase_counts, merge_map)
    ignored_keys = {t.replace(" ", JOIN) for t in ignored}
    counts = {k: Counter({t: n for t, n in c.items() if t not in ignored_keys}) for k, c in counts.items()}
    print(f"{len(df)} posts, {len(phrases)} fixed terms, {len(ignored)} ignored terms")

    channels = df.drop_duplicates("channel").sort_values("channel_id")
    groups = df.drop_duplicates("source_group").sort_values("group_id")["source_group"].tolist()
    phases = df.drop_duplicates("phase").sort_values("phase_id")["phase"].tolist()
    group_of = dict(zip(channels["channel"], channels["source_group"]))

    def total(members, phase_list):
        c = Counter()
        for ch in members:
            for ph in phase_list:
                c += counts.get((ch, ph), Counter())
        return c

    prior = total(channels["channel"], phases)
    rows = []
    for g in groups:
        inside = [c for c, grp in group_of.items() if grp == g]
        outside = [c for c in group_of if c not in inside]
        rows.append(compare_group(g, ALL, inside, outside, total, prior, phases))
        for ph in phases:
            rows.append(compare_group(g, ph, inside, outside, total, prior, [ph]))
    for ch in channels["channel"]:
        others = [c for c in group_of if c != ch]
        rows.append(compare("channel", ch, ALL, total([ch], phases), total(others, phases), prior))
    table = pd.concat(rows, ignore_index=True)

    table.to_csv(OUTPUT_DIR / "typical_terms.csv", index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUTPUT_DIR / "typical_terms.xlsx") as xl:
        wide(table, "group", groups, [ALL]).to_excel(xl, sheet_name="groups")
        wide(table, "channel", channels["channel"], [ALL]).to_excel(xl, sheet_name="channels")
        for g in groups:
            wide(table, "group", [g], phases).to_excel(xl, sheet_name=g[:31])
    print(f"saved to {OUTPUT_DIR}\n")

    for g in groups:
        top = table[(table["level"] == "group") & (table["name"] == g) & (table["phase"] == ALL)].head(15)
        print(f"{g}: " + "  |  ".join(top["term"]))


if __name__ == "__main__":
    main()
