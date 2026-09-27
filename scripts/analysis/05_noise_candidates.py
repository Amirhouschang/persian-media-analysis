"""
05_noise_candidates.py – Find terms that say nothing about differences between channels (candidates only)
===========================================================================================================

RUN (in the folder scripts/analysis, after 03_terms.py):
  python 05_noise_candidates.py

WHY
  The top lists still contain words that are frequent everywhere but carry no content (خواهد, قرار, اعلام ...)
  and names of the channels themselves (ایرنا, جماران). Python only PROPOSES them – the author decides.

TWO PATTERNS (based on results/words/terms.csv)
  everywhere_always – among the top terms of all six channels, used at a similar rate by every channel
                      (highest / lowest rate <= MAX_CHANNEL_RATIO) and in every phase
                      (highest / lowest rate <= MAX_PHASE_RATIO). ایران is NOT proposed: its rate rises sharply
                      in the war.
  one_channel       – at least ONE_CHANNEL_SHARE of all occurrences come from one channel (own name, signatures)

OUTPUT
  results/words/noise_candidates.xlsx – one row per candidate with the numbers behind the proposal

DECISION
  For every term that should not appear in the lists, add a line to phrase_corrections.csv:
      خواهد,ignore,auxiliary verb
  Then run 03_terms.py again. Ignored terms are still counted in the total number of words, they are only
  left out of the lists.
"""
from pathlib import Path
import pandas as pd

RESULTS = Path(__file__).resolve().parents[2] / "results" / "words"
TOP_EVERYWHERE = 300            # must be among the top 300 of every channel
MAX_CHANNEL_RATIO = 2.0         # highest channel rate at most twice the lowest
MAX_PHASE_RATIO = 1.5           # highest phase rate at most 1.5 times the lowest
ONE_CHANNEL_SHARE = 0.8         # 80 % of all occurrences from one channel
MIN_COUNT = 100                 # ignore rare terms


def main():
    t = pd.read_csv(RESULTS / "terms.csv", encoding="utf-8-sig")
    ch = t[t["level"] == "channel"]
    channels = ch["name"].unique()
    phases = [p for p in ch["phase"].unique() if p != "all"]

    whole = ch[ch["phase"] == "all"]
    rate = whole.pivot_table(index="term", columns="name", values="per_1000_words").reindex(columns=channels).fillna(0)
    rank = whole.pivot_table(index="term", columns="name", values="rank").reindex(columns=channels)
    count = whole.pivot_table(index="term", columns="name", values="count").reindex(columns=channels).fillna(0)
    by_phase = (ch[ch["phase"] != "all"].pivot_table(index="term", columns=["phase", "name"], values="per_1000_words")
                .fillna(0).T.groupby(level="phase").mean().T.reindex(columns=phases).fillna(0))

    rows = []
    for term in rate.index:
        r, n = rate.loc[term], count.loc[term]
        phase_r = by_phase.loc[term] if term in by_phase.index else pd.Series(0, index=phases)
        channel_ratio = r.max() / r.min() if r.min() > 0 else float("inf")
        phase_ratio = phase_r.max() / phase_r.min() if phase_r.min() > 0 else float("inf")
        main_share = n.max() / n.sum() if n.sum() else 0
        everywhere = rank.loc[term].notna().all() and (rank.loc[term] <= TOP_EVERYWHERE).all()

        if everywhere and channel_ratio <= MAX_CHANNEL_RATIO and phase_ratio <= MAX_PHASE_RATIO:
            reason = "everywhere_always"
        elif n.sum() >= MIN_COUNT and main_share >= ONE_CHANNEL_SHARE:
            reason = "one_channel"
        else:
            continue
        rows.append({"term": term, "n_words": term.count(" ") + 1, "reason": reason,
                     "per_1000_words_avg": round(r.mean(), 2),
                     "channel_ratio": round(channel_ratio, 2), "phase_ratio": round(phase_ratio, 2),
                     "main_channel": n.idxmax(), "main_channel_pct": round(100 * main_share),
                     **{f"per_1000_{p}": round(phase_r[p], 2) for p in phases}})

    out = pd.DataFrame(rows).sort_values(["reason", "per_1000_words_avg"], ascending=[False, False])
    out.to_excel(RESULTS / "noise_candidates.xlsx", index=False)
    print(out.groupby("reason").size().to_string())
    print(f"\nsaved to {RESULTS / 'noise_candidates.xlsx'}\n")
    for reason in ["everywhere_always", "one_channel"]:
        part = out[out["reason"] == reason].head(25)
        print(f"{reason}: " + "  |  ".join(part["term"]))


if __name__ == "__main__":
    main()
