# AI classification – published results

No post texts are included (copyright). Every post can be opened via the `url` column (`t.me/<channel>/<id>`).

| File | Content |
|---|---|
| `model_comparison_v8_summary.csv` | one row per model: agreement with manual coding (exact and including borderline cases), Cohen's kappa, seconds per post (median) – codebook v8, 150 posts |
| `model_comparison_v8_details.csv` | every single AI answer: channel, post ID, manual coding, AI coding, AI reasoning |
| `testset2_labels.csv` | manual reference coding of the 150 test posts (topic, optional secondary topic, tone) |

Column names: `kanal` = channel, `datum` = publication date (UTC).
Method and interpretation: [docs/en/03_ai_classification.md](../../docs/en/03_ai_classification.md) · Deutsch: [docs/de/03_ki_einordnung.md](../../docs/de/03_ki_einordnung.md)
