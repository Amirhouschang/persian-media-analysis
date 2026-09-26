"""
03_ai_classify.py – Main run: classify a stratified sample with the chosen model
================================================================================

RUN (in the folder scripts/ai, conda environment iran-analyse):
  python 03_ai_classify.py --test      -> test run (4 posts per channel)
  python 03_ai_classify.py --count     -> only show how large the sample will be (no AI)
  systemd-inhibit --what=idle:sleep python -u 03_ai_classify.py    -> full run (keeps the computer awake)

SAMPLE
  Stratified by channel x week: PER_CHANNEL_WEEK posts per channel and week (ai_config.py).
  Weeks with fewer posts -> all posts of that week.
  Only posts with more than 80 characters of text (as in the test set).
  Column 'gewicht' (weight) = posts in this channel-week / posts drawn
  -> used later to project shares onto the whole channel (weighted mean).

SAME SETTINGS AS IN THE TEST
  The AI receives exactly the prompt from the model comparison (topic + tone + reasoning),
  so the measured agreement rates also apply to this run.

INTERRUPTIONS ARE NO PROBLEM
  Every row is saved immediately; on restart the run continues.
  The order is shuffled: even a half-finished run covers all channels and weeks.
  The file name contains model, context and codebook version -> nothing is overwritten.
"""

import argparse
import re
import time
import pandas as pd

import ai_config as cfg
import ai_core as core

cfg.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def output_file(test):
    """e.g. classification_gemma4-31b_context_v8.csv"""
    model = re.sub(r"[^a-zA-Z0-9.]+", "-", cfg.CLASSIFICATION_MODEL)
    context = "context" if cfg.CLASSIFICATION_CONTEXT else "no-context"
    prefix = "test_classification" if test else "classification"
    return cfg.OUTPUT_DIR / f"{prefix}_{model}_{context}_{core.CODEBOOK_VERSION}.csv"


def load_data():
    """Reads all raw files, removes posts that are too short, computes the week."""
    df = pd.concat([pd.read_csv(p, low_memory=False) for p in cfg.INPUT_FILES], ignore_index=True)
    df["datum"] = pd.to_datetime(df["datum"], utc=True)
    df = df[df["text"].fillna("").str.len() > 80].copy()
    # week = Monday of the week (same split for all channels); column name kept in German
    df["woche"] = (df["datum"].dt.tz_convert(None).dt.to_period("W-SUN").dt.start_time).dt.date
    return df


def draw_sample(df, test):
    if test:
        s = df.groupby("kanal").sample(n=cfg.PER_CHANNEL_TEST_RUN, random_state=cfg.SAMPLE_SEED)
        s["gewicht"] = 1.0
        return s
    parts = []
    for (channel, week), g in df.groupby(["kanal", "woche"]):
        n = min(cfg.PER_CHANNEL_WEEK, len(g))
        t = g.sample(n=n, random_state=cfg.SAMPLE_SEED)
        t["gewicht"] = len(g) / n                     # how many posts one drawn post represents
        parts.append(t)
    s = pd.concat(parts)
    return s.sample(frac=1, random_state=cfg.SAMPLE_SEED)   # shuffle the order


def main(test, count_only):
    df = load_data()
    sample = draw_sample(df, test)

    overview = sample.groupby("kanal").agg(posts=("id", "size"), weeks=("woche", "nunique"))
    print(overview.to_string())
    print(f"Total: {len(sample)} posts", flush=True)
    if count_only:
        return

    output = output_file(test)
    print(f"\nModel: {cfg.CLASSIFICATION_MODEL} | Context: {cfg.CLASSIFICATION_CONTEXT} "
          f"| Codebook: {core.CODEBOOK_VERSION}\nOutput: {output}", flush=True)
    if cfg.CLASSIFICATION_MODEL not in core.installed_models():
        raise SystemExit(f"Model missing: ollama pull {cfg.CLASSIFICATION_MODEL}")

    done = set(pd.read_csv(output)["key"]) if output.exists() else set()
    first_row = not output.exists()
    open_posts = len(sample) - len(done)
    print(f"Already done: {len(done)} | open: {open_posts}\n", flush=True)

    prompt = core.build_prompt(cfg.CLASSIFICATION_CONTEXT)   # same prompt as in the model comparison
    finished, run_start = 0, time.time()

    for z in sample.itertuples():
        key = f"{z.kanal}_{z.id}"
        if key in done:
            continue
        start = time.time()
        try:
            res = core.classify(cfg.CLASSIFICATION_MODEL, z.text, cfg.CLASSIFICATION_CONTEXT,
                                prompt=prompt, kanal=z.kanal)
        except Exception as e:
            print(f"{key}: error {e}", flush=True)
            continue

        pd.DataFrame([{
            "key": key, "kanal": z.kanal, "seite": z.seite, "id": z.id, "datum": z.datum,
            "woche": z.woche, "gewicht": round(z.gewicht, 3),
            "topic": res["topic"], "tone": res["tone"], "reason": res["reason"],
            "seconds": round(time.time() - start, 1),
            "model": cfg.CLASSIFICATION_MODEL, "context": cfg.CLASSIFICATION_CONTEXT,
            "codebook": core.CODEBOOK_VERSION,
        }]).to_csv(output, mode="w" if first_row else "a", header=first_row,
                   index=False, encoding="utf-8-sig")
        first_row = False
        finished += 1

        # progress with estimated remaining time
        per_post = (time.time() - run_start) / finished
        remaining_h = (open_posts - finished) * per_post / 3600
        print(f"{len(done) + finished}/{len(sample)} {key}: {res['topic']} | {res['tone']}"
              f"  (about {remaining_h:.1f} h left)", flush=True)

    print(f"\nDone. Results in {output}", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="AI classification: stratified sample")
    p.add_argument("--test", action="store_true", help="test run only (4 per channel)")
    p.add_argument("--count", action="store_true", help="only show the sample size, no AI")
    a = p.parse_args()
    main(a.test, a.count)
