# Result files

This folder contains the result tables of the analysis (CSV and Excel) and the charts. This page explains which file
comes from which script and what the columns mean.
**Looking for the findings?** See the [results report](../docs/en/report.md) · Deutsch: [Ergebnisbericht](../docs/de/bericht.md).

*Deutsch: Dieser Ordner enthält die Ergebnistabellen (CSV und Excel) und die Diagramme. Diese Seite erklärt, welche Datei
von welchem Skript stammt und was die Spalten bedeuten.*

- **No post texts:** only numbers, terms and links (copyright). The AI files in `ai/` contain short AI reasons that may
  repeat single phrases of a post.
- **Origin:** every file is produced by a script in `scripts/analysis/` or `scripts/ai/` and can be recreated from the
  database. Terms with the same count can change places in the top lists from run to run; the counts stay the same.
- **Opening the CSV files:** UTF-8 with BOM, so Persian shows correctly in Excel and LibreOffice. In LibreOffice choose
  the language "English (USA)" when opening, otherwise decimal numbers are misread.

Method and interpretation: [docs/en/04_analysis.md](../docs/en/04_analysis.md) · Deutsch: [docs/de/04_analyse.md](../docs/de/04_analyse.md)

Common columns: `level` = `group` (source group) or `channel` · `name` = group or channel ·
`phase` = `all` or one of the four phases · `per_1000_words` = frequency per 1,000 words ·
`share_pct` = share within the category in percent.

## `words/` – word analysis

| File | Script | Content |
|---|---|---|
| `word_frequency.csv` / `.xlsx` | `01_word_frequency.py` | most frequent single words per channel, group and phase |
| `phrases.csv` | `03_terms.py` | all 1,501 fixed terms. `count` = how often the word sequence occurs, also inside longer terms (a lower bound: up to 96 occurrences can be missing, see [04, section 10](../docs/en/04_analysis.md#10-method); basis of the term selection) · `count_used` = how often it was counted as this term (exact) · `share_pct` · `source` (auto = found automatically, added = added by the author) |
| `terms.csv` / `.xlsx` | `03_terms.py` | top 1,000 terms (single words and fixed terms) per channel, group and phase; every place counted once |
| `typical_terms.csv` / `.xlsx` | `07_typical_terms.py` | terms a group or channel uses clearly more often than the others: `z` (log-odds z-score), `z_by_channel`, `per_1000`, `per_1000_rest` |

## `leader/` – which Khamenei is meant

| File | Script | Content |
|---|---|---|
| `leader_mentions.csv` / `.xlsx` | `06_leader_mentions.py` | posts about Ali Khamenei, Mojtaba Khamenei or both, per channel and phase (counts and %); sheet `first_dates`: first day of each wording per channel, with the link to the post |

## `naming/` – how the same things are named

| File | Script | Content |
|---|---|---|
| `naming.csv` / `.xlsx` | `08_naming.py` | every concept of `naming_terms.csv` per group, channel and phase: `count`, `per_1000_words`, `share_pct`; Excel: one sheet per category and one per category with the phases |
| `neighbours.csv` | `08_naming.py` | the 20 most frequent words directly before and after ترامپ and نتانیاهو per source group |

## `timeline/` – change per week

| File | Script | Content |
|---|---|---|
| `timeline.csv` / `.xlsx` | `09_timeline.py` | every concept per group, channel and calendar week (`week_start` = Monday) |
| `charts/*.png` | `09_timeline.py` | 11 line charts per source group; complete weeks only |
| `peak_weeks.csv` | `11_peak_weeks.py` | for the 2 highest weeks of every chart and group: the terms typical of that week (`rank`, `term`, `z`, `count`) – explains what happened in a peak week |

## `activity/` – activity and reach

| File | Script | Content |
|---|---|---|
| `activity_phases.csv`, `activity.xlsx` (sheet `phases`) | `10_activity.py` | posts, posts per day and channel, views (median, mean), forwards (median, mean), forwards per 1,000 views – per group, channel and phase |
| `activity_weekly.csv`, `activity.xlsx` (sheet `weekly`) | `10_activity.py` | the same per calendar week; `complete_week` marks weeks with 7 days of data |
| `charts/*.png` | `10_activity.py` | posts per day, median views, forwards per 1,000 views |

## `countries/` – countries and allies

| File | Script | Content |
|---|---|---|
| `countries.csv` | `12_countries.py` | every country and group of the category `countries_actors` per group, channel and phase: `count`, `per_1000_words`; `label` = English name (empty for helper entries and opposition groups) |
| `countries_weekly.csv` | `12_countries.py` | the same per source group and calendar week; `complete_week` marks weeks with 7 days of data |
| `peak_weeks.csv` | `12_countries.py` | for every country the 2 weeks with the highest value (all groups together) and the terms typical of the posts about the country in that week (`rank`, `term`, `z`, `count`) |
| `framing.csv` | `12_countries.py` | for every country and group (from 100 posts): the terms the group uses clearly more often in its posts about the country than the other groups (`rank`, `term`, `z`, `count`, `posts`) |
| `countries.xlsx` | `12_countries.py` | sheets `overview` (groups × countries), `phases`, `peak_weeks`, `framing` |
| `charts/*.png` | `12_countries.py` | one chart per region (Gulf states, Lebanon/Palestine/Iraq/Yemen/Syria, great powers and neighbours, Europe), one panel per country; complete weeks only |

## `ai/` – AI classification

See [ai/README.md](ai/README.md).
