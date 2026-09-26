"""
03a_model_comparison.py – Which model (with/without background knowledge) classifies best?
==========================================================================================

RUN – no change in the code needed:
  python 03a_model_comparison.py draw                        -> new test set (testset.csv)
  python 03a_model_comparison.py draw --name testset2.csv --seed 11
  python 03a_model_comparison.py compare                     -> comparison with testset.csv
  python 03a_model_comparison.py compare --name testset2.csv

WHAT HAPPENS WHEN COMPARING?
  Every model from ai_config.COMPARISON_MODELS is tested with every variant from
  ai_config.CONTEXT_VARIANTS:
    without context = codebook + post only
    with context    = additionally background knowledge (background.txt) + who is behind the source
  Result: ONE Excel file with five sheets:
    summary         – one row per run: agreement rates, time (sorted, best on top)
                      *_incl_2_% = also counts as a hit if the AI topic equals your
                      secondary topic (column topic2_manual in the test set, borderline cases only)
    side_by_side    – one row per post, all runs next to each other
    disagreements   – only cases where the AI and you decided differently, with the AI's reasoning
    confusion       – which category is confused with which (for improving the codebook)
    details         – every single answer

INTERRUPTIONS ARE NO PROBLEM
  The Excel file is saved after every run. On restart, finished runs are skipped.
"""

import argparse
import sys
import time
import pandas as pd

import ai_config as cfg
import ai_core as core

cfg.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------
def read_testset(path):
    """Reads your test set and unifies column names (old German names still work)."""
    test = pd.read_csv(path)
    test = test.rename(columns={"thema_manuell": "topic_manual", "ton_manuell": "tone_manual",
                                "ton_manual": "tone_manual"})
    for column in ["topic_manual", "tone_manual"]:
        if column not in test.columns or test[column].isna().any():
            sys.exit(f"Column '{column}' is missing or not completely filled in.")
        test[column] = test[column].astype(str).str.strip().str.lower()

    # Check that only allowed terms were used
    wrong = test[~test["topic_manual"].isin(core.TOPICS) | ~test["tone_manual"].isin(core.TONES)]
    if len(wrong):
        print("Unknown terms in the test set (typo?):")
        print(wrong[["kanal", "id", "topic_manual", "tone_manual"]].to_string(index=False))
        sys.exit("Please correct and restart.")

    # Secondary topic (optional, set only by the human coder): empty cells = no secondary topic
    if "topic2_manual" not in test.columns:
        test["topic2_manual"] = ""
    test["topic2_manual"] = test["topic2_manual"].fillna("").astype(str).str.strip().str.lower()
    wrong2 = test[(test["topic2_manual"] != "") & ~test["topic2_manual"].isin(core.TOPICS)]
    if len(wrong2):
        print("Unknown terms in topic2_manual:")
        print(wrong2[["kanal", "id", "topic2_manual"]].to_string(index=False))
        sys.exit("Please correct and restart.")

    test["headline"] = test["text"].astype(str).str.split("\n").str[0].str[:120]
    return test


def result_file(testset_path):
    """File name contains test set + codebook version -> nothing is overwritten."""
    return cfg.OUTPUT_DIR / f"model_comparison_{testset_path.stem}_{core.CODEBOOK_VERSION}.xlsx"


def evaluate(test, details):
    """Computes the sheets of the Excel file from all single answers."""
    det = pd.DataFrame(details)
    if "topic2_manual" not in det.columns:                 # older runs without secondary topic
        det["topic2_manual"] = ""
    det["topic2_manual"] = det["topic2_manual"].fillna("").astype(str)

    # --- summary: one row per run
    rows = []
    for run, d in det.groupby("run", sort=False):
        t_ok = d.topic_manual == d.topic_ai
        o_ok = d.tone_manual == d.tone_ai
        # fair: AI topic = your main topic OR your secondary topic (borderline case set by YOU)
        t_ok2 = t_ok | ((d.topic2_manual != "") & (d.topic_ai == d.topic2_manual))
        rows.append({
            "run": run, "model": d.model.iloc[0], "context": d.context.iloc[0],
            "topic_match_%": round(t_ok.mean() * 100, 1),
            "tone_match_%": round(o_ok.mean() * 100, 1),
            "both_match_%": round((t_ok & o_ok).mean() * 100, 1),
            "topic_match_incl_2_%": round(t_ok2.mean() * 100, 1),
            "both_match_incl_2_%": round((t_ok2 & o_ok).mean() * 100, 1),
            "invalid_or_error": int(d[["topic_ai", "tone_ai"]].isin(["invalid", "error"]).any(axis=1).sum()),
            "sec_per_post": round(d.seconds.median(), 1),   # median: robust against pauses (e.g. sleep mode)
            "codebook": core.CODEBOOK_VERSION,
        })
    summary = pd.DataFrame(rows).sort_values(["both_match_%", "topic_match_%"], ascending=False)

    # --- side_by_side: one row per post
    wide = test[["kanal", "id", "headline", "topic_manual", "topic2_manual", "tone_manual"]].copy()
    for run, g in det.groupby("run", sort=False):
        g = g.set_index("id")
        wide[f"{run} | topic"] = wide["id"].map(g["topic_ai"])
        wide[f"{run} | tone"] = wide["id"].map(g["tone_ai"])

    # --- disagreements: differences only, with headline and the AI's reasoning
    diff = det[(det.topic_manual != det.topic_ai) | (det.tone_manual != det.tone_ai)].copy()
    diff = diff.merge(test[["id", "headline"]], on="id", how="left")
    diff = diff[["run", "kanal", "id", "headline", "topic_manual", "topic2_manual", "topic_ai",
                 "tone_manual", "tone_ai", "reason_ai"]]

    # --- confusion: which category is confused with which? (long table, filterable)
    conf = []
    for dim in ["topic", "tone"]:
        c = det.groupby(["run", f"{dim}_manual", f"{dim}_ai"]).size().reset_index(name="count")
        c.columns = ["run", "manual", "ai", "count"]
        c.insert(1, "dimension", dim)
        conf.append(c)
    confusion = pd.concat(conf)
    confusion = confusion[confusion.manual != confusion.ai]   # confusions only

    return summary, wide, diff, confusion, det


def save(path, test, details):
    summary, wide, diff, confusion, det = evaluate(test, details)
    with pd.ExcelWriter(path) as xl:
        summary.to_excel(xl, sheet_name="summary", index=False)
        wide.to_excel(xl, sheet_name="side_by_side", index=False)
        diff.to_excel(xl, sheet_name="disagreements", index=False)
        confusion.to_excel(xl, sheet_name="confusion", index=False)
        det.to_excel(xl, sheet_name="details", index=False)
    return summary


# ---------------------------------------------------------------
# STEP A – DRAW A TEST SET
# ---------------------------------------------------------------
def draw(name, seed):
    target = cfg.OUTPUT_DIR / name
    if target.exists():
        sys.exit(f"{target} already exists – it will not be overwritten. Choose another --name.")

    df = pd.concat([pd.read_csv(p, low_memory=False) for p in cfg.INPUT_FILES], ignore_index=True)
    df = df[df["text"].fillna("").str.len() > 80]            # remove posts that are too short

    old_ids = set()                                          # exclude posts from earlier test sets
    for old in cfg.OUTPUT_DIR.glob("testset*.csv"):
        old_ids |= set(pd.read_csv(old)["id"])
    df = df[~df["id"].isin(old_ids)]

    test = df.groupby("kanal").sample(n=cfg.PER_CHANNEL_TESTSET, random_state=seed)
    test = test[["kanal", "id", "datum", "text"]].copy()
    test["topic_manual"] = ""
    test["topic2_manual"] = ""                               # fill in only when really needed
    test["tone_manual"] = ""
    test.to_csv(target, index=False, encoding="utf-8-sig")
    print(f"{len(test)} posts saved in {target}")
    print("Topics:", ", ".join(core.TOPICS))
    print("Tones: ", ", ".join(core.TONES))


# ---------------------------------------------------------------
# STEP B – COMPARE
# ---------------------------------------------------------------
def compare(name):
    testset_path = cfg.OUTPUT_DIR / name
    test = read_testset(testset_path)
    path = result_file(testset_path)

    # Which models are installed?
    available = core.installed_models()
    missing = [m for m in cfg.COMPARISON_MODELS if m not in available]
    if missing:
        print("Not installed, skipped:", ", ".join(missing), "(ollama pull <name>)")
    models = [m for m in cfg.COMPARISON_MODELS if m in available]

    # Resume: take over finished runs from the Excel file
    details = []
    if path.exists():
        old = pd.read_excel(path, sheet_name="details")
        details = old.to_dict("records")
        print("Already finished (skipped):", ", ".join(old["run"].unique()))
    finished = {d["run"] for d in details}

    runs = [(m, c) for m in models for c in cfg.CONTEXT_VARIANTS]
    for nr, (model, with_context) in enumerate(runs, 1):
        run = core.run_name(model, with_context)
        if run in finished:
            continue
        print(f"\n=== [{nr}/{len(runs)}] {run} ===", flush=True)
        prompt = core.build_prompt(with_context)              # build once, use for all posts

        for z in test.itertuples():
            start = time.time()
            try:
                res = core.classify(model, z.text, with_context, prompt=prompt, kanal=z.kanal)
            except Exception as e:
                print(f"  Error: {e}", flush=True)
                res = {"topic": "error", "tone": "error", "reason": str(e)}
            details.append({
                "run": run, "model": model, "context": with_context,
                "kanal": z.kanal, "id": z.id,
                "topic_manual": z.topic_manual, "topic_ai": res["topic"],
                "topic2_manual": z.topic2_manual,
                "tone_manual": z.tone_manual, "tone_ai": res["tone"],
                "reason_ai": res["reason"], "seconds": round(time.time() - start, 1),
            })
            mark = "✓" if (res["topic"], res["tone"]) == (z.topic_manual, z.tone_manual) else " "
            print(f"  {mark} {z.kanal}_{z.id}: {res['topic']} | {res['tone']}", flush=True)

        save(path, test, details)                            # save after every run
        core.unload(model)

    summary = save(path, test, details)
    print("\n", summary.drop(columns=["codebook"]).to_string(index=False), flush=True)
    print(f"\nEverything saved in: {path}", flush=True)


# ---------------------------------------------------------------
# START
# ---------------------------------------------------------------
if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Model comparison for the AI classification")
    p.add_argument("step", choices=["draw", "compare"])
    p.add_argument("--name", default="testset.csv", help="name of the test set in data/ki/")
    p.add_argument("--seed", type=int, default=7, help="random seed when drawing")
    a = p.parse_args()
    draw(a.name, a.seed) if a.step == "draw" else compare(a.name)
