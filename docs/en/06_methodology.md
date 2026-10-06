**English** | [Deutsch](../de/06_methodik.md)

# 06 – Methodology, Limitations and Security

[← back to overview](../../README.md)

This page summarises how the results came about, which decisions the author set, what the results do not say and how
data and credentials were protected. Details are in [01](01_data_collection.md) to [04](04_analysis.md).

> **Scope:** The project is primarily technical and gives a reliable overview, not an in-depth scholarly analysis. Such a
> study would read and interpret the posts individually and would run to 100 pages or more.

---

## 1. Overview of the procedure

| Step | Procedure | Document |
|---|---|---|
| Sources | 6 public Telegram channels in three groups (state: IRNA, IRIB News, Mehr News · IRGC-affiliated: Tasnim News, Fars News · reformist: Jamaran), 1 Jan – 31 Aug 2026 | [01](01_data_collection.md) |
| Collection | official Telegram API (`Telethon`), 328,330 posts, checks on seven points | [01](01_data_collection.md) |
| Processing | PostgreSQL database `iran_media_2026`; Persian text cleaned, the original text stays unchanged | [02](02_processing.md) |
| Counting | 1,501 fixed terms (1,490 found without a predefined word list, 11 added by the author); naming list with 113 terms in 188 spellings; unit: mentions per 1,000 words | [04, section 10](04_analysis.md#10-method) |
| Group comparison | weighted log-odds ratio with z-score (above 1.96 statistically clear); a term counts for a group only if every one of its channels uses it more often | [04, section 10](04_analysis.md#10-method) |
| AI topics | Gemma 4 31B local, codebook v8, 10,750 posts, weighted to 231,406 posts with more than 80 characters; checked blind on 200 new posts | [03](03_ai_classification.md) |
| Tone | classified by the AI and checked against manual coding, but not used for comparisons between groups (kappa 0.46) | [03, section 8](03_ai_classification.md#8-final-validation-phase-c--result) |
| Presentation | results report, charts and a bilingual dashboard; they show numbers only | [Report](report.md) |

---

## 2. Decisions made by the author

These decisions are documented in files. Other decisions would give slightly different numbers.

| Setting | Content | File |
|---|---|---|
| Choice of sources and groups | 6 channels in 3 groups; channel descriptions worded neutrally ("widely described as IRGC-affiliated") | `README.md`, `02_load_database.py` |
| Phases | before the war 1 Jan – 27 Feb · war 28 Feb – 7 Apr · ceasefire 8 Apr – 6 Jul · after the collapse 7 Jul – 31 Aug | `02_load_database.py` |
| Event dates | Ali Khamenei's death officially confirmed 1 Mar; Mojtaba Khamenei elected 8 Mar | `06_leader_mentions.py` |
| Correction list | 347 entries: 12 titles, 11 long names, 5 removals, 56 merges, 263 ignored terms | `phrase_corrections.csv` |
| Naming list | 113 terms, 188 spellings, 10 categories | `naming_terms.csv` |
| Thresholds | term with at least 100 occurrences; typical terms from a minimum frequency of 50 (countries: 20); z-score above 1.96 | [04](04_analysis.md#10-method) |
| Codebook v8 | 9 topics, 6 tones, rules – e.g. legal and descriptive terms about the wars do not automatically make a text accusatory (the same for all sources); when in doubt, *neutral* | `codebook.py` |
| Background text | neutrally worded timeline, actors, glossary; international law worded the same for all states | `background.txt` |
| AI sample | 50 posts per channel and week, only posts with more than 80 characters | [03, section 7](03_ai_classification.md#7-main-run) |

---

## 3. Data quality and gaps

| Check (details in [01](01_data_collection.md)) | Result |
|---|---|
| Rows per channel, period, duplicates | matching; period complete for all channels; 0 duplicates |
| Posts without text | 11–27% per channel (images or videos without a caption); 267,548 of 328,330 posts contain text |
| Days without posts | IRNA 16 days (9–22 Jan and 16–17 Mar), Jamaran 6 days (9–14 Jan), all other channels none |

- **January gaps:** IRNA was queried again on purpose; the posts are missing on Telegram itself. The gaps at IRNA and
  Jamaran fall in the time of the internet blackout. For 16–17 Mar the documentation gives no cause.
- **Time zone:** Telegram delivers UTC; Iran is at UTC+3:30. Posts between 20:30 and 24:00 UTC already belong to the next
  day in Tehran time.
  - **Rule:** days, weeks and phases of the database and of all analyses built on it (terms, timeline, activity) use the
    UTC date; the weights of the AI sample are also based on UTC weeks.
  - **Exception:** only the AI topic shares per phase (`03e_topics.py`) use the Tehran date. There the ceasefire ends on
    7 Jul and the next phase begins on 8 Jul (database: 6 and 7 Jul).
  - **Effect:** only posts at the boundaries of days, weeks and phases are affected. Recalculated for the AI topic shares:
    by the UTC date instead of the Tehran date, 48 of 10,750 posts (37 of them at the ceasefire/collapse boundary) would
    fall into another phase. The topic shares of the groups would change by at most 1.5 percentage points (2 of 108 values
    above 1 point), those of the single channels by at most 2.1 (4 of 216 values above 1 point). For the other analyses
    the extent was not quantified.
  - **Charts:** the event line "collapse of the ceasefire" is at 8 Jul.
- **State of the data:** Texts, views and forwards correspond to the time of collection; anything deleted before then is
  missing. Posts from the last days before the collection had less time to collect views. The first week (from 1 Jan) and
  the last week (31 Aug only) are incomplete and are left out of the weekly charts.
- **Forwards:** Only the sender name is stored, which is mostly empty for channels. A network analysis ("who forwards
  whom") is therefore not possible.
- **Sepah News:** The web archive (about 5,300 articles) was collected but is not analysed: long web articles without view
  counts are not comparable with Telegram posts, and the local AI analysis of long texts requires much more computing
  effort. The Telegram channel could not be reached from Germany.
- **Cleaning:** The rules were checked with samples and SQL checks, not by reading all posts ([02](02_processing.md)).

---

## 4. Limits of the findings

| Limit | Consequence for reading |
|---|---|
| **Counting is not understanding** | A term counts the same whether used approvingly, at a distance, negated or as a quotation. |
| **Selection** | Six channels on Telegram; no opposition or exile media, no other platforms. The results apply to these channels, not to "Iranian media". |
| **"Reformist" group** | It consists of one channel (Jamaran). Statements about this group are statements about Jamaran. |
| **Peak weeks** | The typical terms describe the whole week, not only the posts with the counted word. Assigning a peak to an event is an interpretation; for one peak (crime terms, IRGC-affiliated, week from 20 Jul) no single event is recognisable. |
| **Reach** | Views count readers of the channel, not unique people; they describe reach, not quality. Subscriber numbers are missing; the differences in views probably depend mostly on the number of subscribers. |
| **Countries** | `عمان` means Oman and Amman; `آذربایجان` alone counts as the Republic of Azerbaijan but sometimes means Iranian provinces (value too high); Egypt is missing because `مصر` also means "persistent"; part of the mentions of European countries, Turkey and Qatar concerns sport. |
| **AI topics** | Topic correct in 72.5% of cases (95% interval 65.9–78.2%). Military is rather overestimated, diplomacy rather underestimated; changes over time are more reliable than the level of the shares. For Jamaran the assignment was the least certain (55.9% correct, 34 posts checked). The sampling error of the shares (excluding errors of the AI assignment) is about ±2.5 percentage points per channel and about ±6 per channel and month. |
| **AI tone** | The AI marked only 18 of 40 non-neutral posts as non-neutral (exactly the same tone for 14) and missed them to a different degree in each group (non-neutral, manual/AI: state 20%/8%, IRGC-affiliated 21%/18%, Jamaran 18%/9%). Tone is therefore not compared. |
| **Reference for the AI check** | It comes from one person. In phase A it was pre-coded with the help of an AI assistant (Claude), checked by the author and adjusted after seeing the AI results; it was not created fully blind. The values of the test set are therefore rather optimistic, the final validation (200 new posts coded blind) is decisive. |
| **Hardware** | A laptop without a separate graphics card limits model size and sample; a stratified sample is therefore classified, not the whole corpus. |

---

## 5. Neutrality and handling of terms

- Terms appear as they do in the sources – including derogatory or hostile ones. They are counted and reported, not judged
  and not adopted. They are the wording of the channels, not the opinion of the author.
- The codebook describes visible features in the text, not interpretation. The rule on legal and descriptive terms
  ("genocide", "aggression", "illegal war") applies equally to all sources.
- The background text for the AI and the channel descriptions are worded neutrally; the channels are not judged.
- The dashboard shows no term tables with translations: translations of single terms should be checked by at least two
  people, and the terms with explanations are in [04](04_analysis.md). The names of the terms in the dashboard selectors
  (69 terms of the word analysis, 35 countries and actors) are in `dashboard/concepts.csv`.

---

## 6. Data protection, copyright and security

**Data**
- only public channels of editorial media; no groups, no private users, no comments, no personal data of users
- The raw texts are not part of the repository for copyright reasons. Every post can be found publicly via
  `t.me/<channel>/<id>`.
- `results/` and the dashboard contain no post texts, but numbers, terms, categories and links to the posts. The AI result
  files also contain the AI's short reasoning for each post; it may repeat single phrases from the post. Check files with
  texts stay private.
- The channels are named; code, methodology and results (including the AI part) are public.

**Credentials**
- API ID and API hash only as environment variables (`TG_API_ID`, `TG_API_HASH`), never in the code
- The session file `sitzung.session` is the login of the Telegram account and gives access to it. It stays local and must
  never be published.
- `.gitignore` excludes: session files, `.env`, `data/` (raw data and AI output), the raw CSV files of the collection,
  database backups and `__pycache__`.

**Processing**
- Database and AI classification of the posts run locally (`Ollama`); the texts are not transmitted to cloud providers for
  this. Exception: the 150 posts of test set 2 were pre-coded in phase A with the help of an AI assistant (Claude)
  ([03](03_ai_classification.md)).
- AI results are not taken over unchecked but validated on new, blind-coded posts with a confidence interval.

---

## 7. Reproducibility

- **Order:** `scripts/telegram/` → `scripts/database/` → `scripts/ai/` → `scripts/analysis/` (`03` → `07` → `06` → `08` →
  `09` → `10` → `11` → `12`). Every result file in `results/` comes from a script
  ([results/README.md](../../results/README.md)); the analyses run on the database, the AI classification on the raw files
  and `Ollama`. Manual inputs (correction list, naming list, codebook, manual coding) are available as files.
- **Database:** Loading is repeatable; the number of posts per channel is checked against the collection after loading
  (328,330).
- **AI:** fixed model version, `temperature = 0`, `seed = 42`; two runs with the same model and codebook gave exactly the
  same result. The codebook version is in the file names of the classifications and model comparisons, so results of different
  versions do not overwrite each other. The model comparison and the first about 2,800 posts of the main run used an
  earlier version of `background.txt`; afterwards six date and price details were corrected, without effect on categories
  or rules. The main run took 67 hours.
- **Ties:** Where several terms have the same count, their order is not fixed. Ranks and the last places of the top lists
  (top 1,000 terms, top 20 neighbouring words, top 15 terms of a peak week) can therefore change from run to run; the counts
  themselves stay the same. A complete re-run from the raw data in October 2026 reproduced all counts: eight result
  files were byte-identical, the others differed only in the order of tied terms.
- **Environment:** Linux, Python 3.11, PostgreSQL 18, Ollama; packages of the scripts: [requirements-scripts.txt](../../requirements-scripts.txt), of the dashboard: `dashboard/requirements.txt`.
- **Limit:** The raw data are not published. Anyone who wants to repeat the analysis has to collect the posts again with
  the scripts; views and forwards as well as posts deleted later may then differ.
- **Unpublished:** To understand the material for himself, the author ran several further SQL queries. They and the data
  belonging to them are not on GitHub, because the project is already very extensive. `03_example_queries.sql` and
  `05_check_cleaning.sql` are published.

---

## 8. For more robust results (suggestions)

- **Several coders:** Two or three native Persian speakers (e.g. Iranists) code the posts independently; their agreement
  with each other and with the AI is measured. The codebook so far reflects the author's view and should be discussed
  together.
- **Adaptation to other questions:** The codebook can be adapted to other disciplines and institutions (e.g. security,
  political science, political interests and ideology).
- **A second reviewer** for the term lists and the translation of single terms.
- **In-depth analysis:** reading and interpreting the posts individually instead of counting; that would be a study of its
  own, of 100 pages or more.
- **Wider sources:** more channels and platforms, opposition and exile media, the Sepah News web archive, subscriber
  numbers.
- **Network analysis:** requires that the origin of forwarded posts is stored completely during collection.
- **Tone:** A comparison between groups would only make sense after better validation.

---

## 9. Further documents

- [Results report](report.md)
- [01 – Data collection](01_data_collection.md) · [02 – Processing](02_processing.md) ·
  [03 – AI classification](03_ai_classification.md) · [04 – Analysis](04_analysis.md)
- Result files: [results/README.md](../../results/README.md)
