"""
03d_export_results.py – Export AI results for publication (GitHub) WITHOUT post texts
=====================================================================================

RUN (in the folder scripts/ai):
  python 03d_export_results.py

WHAT IT DOES
  Reads the result files in data/ki/ and writes publishable CSV files to results/ai/.
  Post texts are never exported (copyright). Every row gets a link to the original post:
  https://t.me/<channel>/<id>
  Files that do not exist yet are simply skipped – run the script again after each step.

  data/ki/model_comparison_<testset>_<version>.xlsx -> model_comparison_<version>_summary.csv
                                                     -> model_comparison_<version>_details.csv
  data/ki/testset*.csv                              -> <testset>_labels.csv  (manual coding only)
  data/ki/classification_<model>_..._<version>.csv  -> main_run_<version>.csv (AI results of the main run)
  data/ki/validation_phase_c.csv                    -> validation_phase_c_labels.csv
  data/ki/validation_phase_c_results.xlsx           -> validation_phase_c_summary.csv / _per_channel.csv

CONFIDENCE INTERVALS
  Agreement measured on a sample (150 test posts, 200 validation posts) is an estimate. For every agreement
  the 95% confidence interval (Wilson) is given: *_ci95_low / *_ci95_high = the range in which the true
  agreement lies with 95% certainty. Model comparison: computed here; Phase C: computed in 03c_validation.py.
"""

from collections import Counter
import pandas as pd

import ai_config as cfg

SOURCE = cfg.OUTPUT_DIR                                  # data/ki/
TARGET = cfg.PROJECT / "results" / "ai"
TARGET.mkdir(parents=True, exist_ok=True)


def add_url(df):
    """Link to the original post instead of the text."""
    df = df.copy()
    df.insert(df.columns.get_loc("id") + 1, "url", "https://t.me/" + df["kanal"] + "/" + df["id"].astype(str))
    return df


def wilson(hits, n, z=1.96):
    """95% confidence interval (Wilson) for a share: where the true agreement lies with 95% certainty."""
    if n == 0:
        return float("nan"), float("nan")
    p = hits / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5 / d
    return round((centre - half) * 100, 1), round((centre + half) * 100, 1)


def kappa(a, b):
    """Cohen's kappa: agreement corrected for chance."""
    n = len(a)
    po = (a == b).mean()
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / n / n
    return round((po - pe) / (1 - pe), 2) if pe < 1 else 1.0


def save(df, name):
    assert "text" not in df.columns, "post texts must never be exported"
    df.to_csv(TARGET / name, index=False, encoding="utf-8")
    print(f"  written: results/ai/{name} ({len(df)} rows)")


# ---------------------------------------------------------------
# 1. Model comparison
# ---------------------------------------------------------------
for path in sorted(SOURCE.glob("model_comparison_*.xlsx")):
    version = path.stem.split("_")[-1]
    print(f"Model comparison: {path.name}")
    det = pd.read_excel(path, sheet_name="details")
    if "topic2_manual" not in det.columns:
        det["topic2_manual"] = ""
    det["topic2_manual"] = det["topic2_manual"].fillna("")

    summary = pd.read_excel(path, sheet_name="summary").drop(columns=["run", "sec_per_post"], errors="ignore")
    def model_stats(g):
        t_ok = g.topic_manual == g.topic_ai
        o_ok = g.tone_manual == g.tone_ai
        t_ok2 = t_ok | ((g.topic2_manual != "") & (g.topic_ai == g.topic2_manual))
        stats = {}
        for name, ok in [("topic_match", t_ok), ("tone_match", o_ok), ("both_match", t_ok & o_ok),
                         ("both_match_incl_2", t_ok2 & o_ok)]:
            stats[f"{name}_ci95_low"], stats[f"{name}_ci95_high"] = wilson(int(ok.sum()), len(g))
        return pd.Series({
            "kappa_topic": kappa(g.topic_manual.values, g.topic_ai.values),
            "kappa_tone": kappa(g.tone_manual.values, g.tone_ai.values),
            **stats,
            "sec_per_post_median": round(g.seconds.median(), 1),
            "n_posts": len(g),
        })

    extra = det.groupby("model").apply(model_stats)
    extra["n_posts"] = extra["n_posts"].astype(int)
    save(summary.merge(extra, left_on="model", right_index=True), f"model_comparison_{version}_summary.csv")

    cols = ["model", "kanal", "id", "topic_manual", "topic2_manual", "topic_ai",
            "tone_manual", "tone_ai", "reason_ai", "seconds"]
    save(add_url(det[cols]), f"model_comparison_{version}_details.csv")

# ---------------------------------------------------------------
# 2. Test sets: manual coding only
# ---------------------------------------------------------------
for path in sorted(SOURCE.glob("testset*.csv")):
    t = pd.read_csv(path)
    keep = [c for c in ["kanal", "id", "datum", "topic_manual", "topic2_manual", "tone_manual"] if c in t.columns]
    print(f"Test set: {path.name}")
    save(add_url(t[keep]), f"{path.stem}_labels.csv")

# ---------------------------------------------------------------
# 3. Main run (AI results)
# ---------------------------------------------------------------
for path in sorted(SOURCE.glob("classification_*.csv")):        # test_classification_* is not included
    version = path.stem.split("_")[-1]
    m = pd.read_csv(path)
    print(f"Main run: {path.name}")
    keep = [c for c in ["kanal", "seite", "id", "datum", "woche", "gewicht", "topic", "tone", "reason", "model", "codebook"]
            if c in m.columns]
    save(add_url(m[keep]), f"main_run_{version}.csv")

# ---------------------------------------------------------------
# 4. Phase C (final validation)
# ---------------------------------------------------------------
path = SOURCE / "validation_phase_c.csv"
if path.exists():
    v = pd.read_csv(path)
    print(f"Phase C: {path.name}")
    save(add_url(v[["kanal", "id", "datum", "topic_manual", "topic2_manual", "tone_manual"]]),
         "validation_phase_c_labels.csv")

path = SOURCE / "validation_phase_c_results.xlsx"
if path.exists():
    print(f"Phase C: {path.name}")
    save(pd.read_excel(path, sheet_name="summary"), "validation_phase_c_summary.csv")
    save(pd.read_excel(path, sheet_name="per_channel"), "validation_phase_c_per_channel.csv")

print(f"\nDone. Upload the folder results/ai/ to GitHub.")
