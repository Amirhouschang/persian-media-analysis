"""
03c_validation.py – Phase C: final validation on posts nobody has seen before
=============================================================================

RUN (in the folder scripts/ai, conda environment iran-analyse):
  python 03c_validation.py draw        -> draws 200 posts for blind manual coding
  python 03c_validation.py evaluate    -> compares your coding with the AI (after the main run)

WHY
  The test sets were used to develop the codebook, so their agreement rates are rather optimistic.
  Phase C measures the frozen procedure (codebook v8, gemma4:31b) on NEW posts:
    - drawn from the main-run sample, so the AI classifies exactly these posts in the main run
    - posts from earlier test sets are excluded
    - you code them WITHOUT looking at the AI's answers (do not open the main-run file for these posts)
    - after the evaluation nothing is changed any more

DRAW
  Same number of posts per channel (200 / 6 channels = 33, the remaining posts at random).
  Output: data/ki/validation_phase_c.csv with empty columns topic_manual, topic2_manual, tone_manual.
  The file is never overwritten.

EVALUATE
  Joins your coding with the main-run results and writes data/ki/validation_phase_c_results.xlsx:
    summary     – agreement (exact and including your secondary topic), Cohen's kappa
    per_channel – agreement per channel (are some sources classified worse than others?)
    confusion   – which categories are confused
    details     – every post with your coding, the AI coding and the AI's reasoning
"""

import argparse
import importlib.util
import sys
from collections import Counter
from pathlib import Path
import pandas as pd

import ai_config as cfg
import ai_core as core

VALIDATION_SIZE = 200
VALIDATION_SEED = 2026                                   # different from all earlier seeds
DRAW_FILE = cfg.OUTPUT_DIR / "validation_phase_c.csv"
RESULT_FILE = cfg.OUTPUT_DIR / "validation_phase_c_results.xlsx"

# Reuse the main-run functions so the sample is exactly the same (file name starts with a digit -> importlib)
_spec = importlib.util.spec_from_file_location("main_run", Path(__file__).parent / "03_ai_classify.py")
main_run = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(main_run)


# ---------------------------------------------------------------
# STEP 1 – DRAW
# ---------------------------------------------------------------
def draw():
    if DRAW_FILE.exists():
        sys.exit(f"{DRAW_FILE} already exists – it will not be overwritten.")

    sample = main_run.draw_sample(main_run.load_data(), test=False)   # the exact main-run sample

    # exclude posts from earlier test sets
    used = set()
    for old in cfg.OUTPUT_DIR.glob("testset*.csv"):
        t = pd.read_csv(old, usecols=["kanal", "id"])
        used |= set(zip(t["kanal"], t["id"]))
    sample = sample[[(k, i) not in used for k, i in zip(sample["kanal"], sample["id"])]]

    # equal number per channel, the rest at random
    per_channel = VALIDATION_SIZE // sample["kanal"].nunique()
    drawn = sample.groupby("kanal").sample(n=per_channel, random_state=VALIDATION_SEED)
    rest = VALIDATION_SIZE - len(drawn)
    if rest:
        drawn = pd.concat([drawn, sample.drop(drawn.index).sample(n=rest, random_state=VALIDATION_SEED)])

    out = drawn[["kanal", "id", "datum", "text"]].sample(frac=1, random_state=VALIDATION_SEED).copy()
    out["topic_manual"] = ""
    out["topic2_manual"] = ""                            # only for genuine borderline cases
    out["tone_manual"] = ""
    out.to_csv(DRAW_FILE, index=False, encoding="utf-8-sig")
    print(out["kanal"].value_counts().to_string())
    print(f"\n{len(out)} posts saved in {DRAW_FILE}")
    print("Code them WITHOUT looking at the AI's answers.")
    print("Topics:", ", ".join(core.TOPICS))
    print("Tones: ", ", ".join(core.TONES))


# ---------------------------------------------------------------
# STEP 2 – EVALUATE (after the main run)
# ---------------------------------------------------------------
def kappa(a, b):
    """Cohen's kappa: agreement corrected for chance."""
    n = len(a)
    po = (a == b).mean()
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / n / n
    return round((po - pe) / (1 - pe), 2) if pe < 1 else 1.0


def agreement(d):
    t_ok = d.topic_manual == d.topic
    o_ok = d.tone_manual == d.tone
    t_ok2 = t_ok | ((d.topic2_manual != "") & (d.topic == d.topic2_manual))
    return {
        "posts": len(d),
        "topic_match_%": round(t_ok.mean() * 100, 1),
        "tone_match_%": round(o_ok.mean() * 100, 1),
        "both_match_%": round((t_ok & o_ok).mean() * 100, 1),
        "topic_match_incl_2_%": round(t_ok2.mean() * 100, 1),
        "both_match_incl_2_%": round((t_ok2 & o_ok).mean() * 100, 1),
    }


def evaluate():
    manual = pd.read_csv(DRAW_FILE)
    for column in ["topic_manual", "tone_manual"]:
        if manual[column].isna().any():
            sys.exit(f"Column '{column}' is not completely filled in.")
        manual[column] = manual[column].astype(str).str.strip().str.lower()
    manual["topic2_manual"] = manual["topic2_manual"].fillna("").astype(str).str.strip().str.lower()
    wrong = manual[~manual["topic_manual"].isin(core.TOPICS) | ~manual["tone_manual"].isin(core.TONES)
                   | ((manual["topic2_manual"] != "") & ~manual["topic2_manual"].isin(core.TOPICS))]
    if len(wrong):
        print(wrong[["kanal", "id", "topic_manual", "topic2_manual", "tone_manual"]].to_string(index=False))
        sys.exit("Unknown terms – please correct and restart.")

    ai_file = main_run.output_file(test=False)
    ai = pd.read_csv(ai_file)[["kanal", "id", "topic", "tone", "reason"]]
    d = manual.merge(ai, on=["kanal", "id"], how="left")
    missing = d["topic"].isna().sum()
    if missing:
        sys.exit(f"{missing} posts are not yet classified in {ai_file.name} – finish the main run first.")

    summary = pd.DataFrame([{**agreement(d),
                             "kappa_topic": kappa(d.topic_manual.values, d.topic.values),
                             "kappa_tone": kappa(d.tone_manual.values, d.tone.values),
                             "model": cfg.CLASSIFICATION_MODEL, "codebook": core.CODEBOOK_VERSION}])
    per_channel = pd.DataFrame([{"kanal": k, **agreement(g)} for k, g in d.groupby("kanal")])

    conf = []
    for dim in ["topic", "tone"]:
        c = d.groupby([f"{dim}_manual", dim]).size().reset_index(name="count")
        c.columns = ["manual", "ai", "count"]
        c.insert(0, "dimension", dim)
        conf.append(c[c.manual != c.ai])
    confusion = pd.concat(conf)

    details = d[["kanal", "id", "topic_manual", "topic2_manual", "topic", "tone_manual", "tone", "reason"]]
    with pd.ExcelWriter(RESULT_FILE) as xl:
        summary.to_excel(xl, sheet_name="summary", index=False)
        per_channel.to_excel(xl, sheet_name="per_channel", index=False)
        confusion.to_excel(xl, sheet_name="confusion", index=False)
        details.to_excel(xl, sheet_name="details", index=False)

    print(summary.T.to_string(header=False))
    print("\nPer channel (both_match_%):")
    print(per_channel.set_index("kanal")["both_match_%"].to_string())
    print(f"\nSaved: {RESULT_FILE}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Phase C: final validation")
    p.add_argument("step", choices=["draw", "evaluate"])
    a = p.parse_args()
    draw() if a.step == "draw" else evaluate()
