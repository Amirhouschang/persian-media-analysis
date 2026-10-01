# AI classification – published results

No post texts are included (copyright). The AI reasons (columns `reason` and `reason_ai`) are short and may repeat single phrases of a post. Every post can be opened via the `url` column (`t.me/<channel>/<id>`).
All files are produced by `scripts/ai/03d_export_results.py`, except `topics/` (`scripts/ai/03e_topics.py`).

**Confidence intervals:** agreement measured on a sample is an estimate. `*_ci95_low` / `*_ci95_high` give the
95% confidence interval (Wilson) – the range in which the true agreement lies with 95% certainty.

## Model comparison (test set 2, 150 posts)

| File | Content |
|---|---|
| `model_comparison_v8_summary.csv` | one row per model: agreement with manual coding (exact and including borderline cases) with 95% intervals, Cohen's kappa, seconds per post (median) – codebook v8 |
| `model_comparison_v8_details.csv` | every single AI answer: channel, post ID, manual coding, AI coding, AI reasoning |
| `model_comparison_v6_*.csv`, `model_comparison_v7_*.csv` | the same for codebook v6 and v7 (one model each) |
| `testset_labels.csv`, `testset2_labels.csv` | manual reference coding of test set 1 (29 posts) and test set 2 (150 posts): topic, optional secondary topic, tone |

## Main run (10,750 posts)

| File | Content |
|---|---|
| `main_run_v8.csv` | AI result for every post of the stratified sample: channel, page, ID, date, week, `gewicht` (weight = posts of its channel-week / posts drawn), topic, tone, AI reasoning, model, codebook |

## Final validation (phase C, 200 new posts coded blind)

| File | Content |
|---|---|
| `validation_phase_c_labels.csv` | manual coding of the 200 posts |
| `validation_phase_c_summary.csv` | agreement (topic, tone, both; exact and with borderline cases) with 95% intervals, Cohen's kappa |
| `validation_phase_c_per_channel.csv` | the same per channel (33–34 posts each – wide intervals) |

Result: topic 72.5% (65.9–78.2%), tone 84.5% (78.8–88.9%), both 62.5% (55.6–68.9%); kappa topic 0.68, tone 0.46.
The AI misses non-neutral tones to a different degree per group – tone is therefore not used for group comparisons.

## `topics/` – topics according to the AI

| File | Content |
|---|---|
| `topic_shares.csv` | weighted share of every topic (`share_pct`) per level (group/channel), name and phase; `posts_drawn` = classified posts behind the value |
| `topic_shares.xlsx` | sheets `groups` and `channels`: topic × phase × name |
| `charts/topics_by_phase.png` | one panel per topic: share per phase, one line per source group |

Column names: `kanal` = channel, `datum` = publication date (UTC), `gewicht` = weight.
Method and interpretation: [docs/en/03_ai_classification.md](../../docs/en/03_ai_classification.md) · Deutsch: [docs/de/03_ki_einordnung.md](../../docs/de/03_ki_einordnung.md) · results: [docs/en/04_analysis.md](../../docs/en/04_analysis.md#7-topics-according-to-the-ai)
