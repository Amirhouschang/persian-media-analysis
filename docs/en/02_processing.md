**English** | [Deutsch](../de/02_aufbereitung.md)

# 02 – Processing: database and text cleaning

[← back to overview](../../README.md)

This step moves the raw data into a relational **PostgreSQL** database and prepares the Persian texts for analysis.

| Part | Status |
|---|---|
| Database `iran_media_2026` | ✅ done |
| Text cleaning | ✅ done |

---

## 1. Database

### Structure

Posts are at the centre; descriptive tables are linked via keys
(snowflake schema: `channels` → `source_groups`, `dates` → `phases`).

![Database schema](../../images/database_schema.png)

| Table | Key | Content | Rows |
|---|---|---|---|
| `posts` | `channel_id` + `post_id` | all posts: time, text, cleaned text, views, forwards, link | 328,330 |
| `channels` | `channel_id` | channel, name, group, link, neutral description | 6 |
| `source_groups` | `group_id` | state, IRGC-affiliated, reformist | 3 |
| `dates` | `date_key` (YYYYMMDD) | every day: month, calendar week, weekday, phase | 243 |
| `phases` | `phase_id` | four periods of the observation window | 4 |

### Phases

| Phase | Period | Description |
|---|---|---|
| `before_war` | 1 Jan – 27 Feb | protests and internet blackout in January, negotiations |
| `war` | 28 Feb – 7 Apr | from the US-Israeli strikes until the ceasefire |
| `ceasefire` | 8 Apr – 7 Jul | ceasefire, naval blockade, Islamabad memorandum; fragile, with clashes |
| `after_truce_collapse` | 8 Jul – 31 Aug | after the ceasefire collapsed on 8 July |

The boundaries are the author's choice based on key events and are defined in `02_load_database.py`.

### Procedure

- `01_schema.sql` creates the tables with primary and foreign keys.
- `02_load_database.py` loads both raw files, replaces channel names with keys, computes `date_key` and the link,
  and finally checks the number of posts per channel (328,330, identical to the collection).
- Loading is **repeatable**: tables are rebuilt every time, the result is always the same.
- All times in **UTC**.
- After the main run, the AI results are added as a separate table `classifications`, because only a
  sample is classified, together with the lookup tables `topics` and `tones`.

### Example queries

`03_example_queries.sql` contains first analyses, e.g. posts per week and source group, views per channel,
missing days, posts per phase and day, and the week before and after 28 February.

---

## 2. Text cleaning

`04_clean_text.py` cleans every post and writes three new columns to `posts`. The original column `text` is never changed.

| Column | Content |
|---|---|
| `text_clean` | cleaned text |
| `tokens` | content words without stop words – basis for the word analysis |
| `word_count` | number of words in `text_clean` |

### Rules

| Step | Example |
|---|---|
| Remove channel advertising (short lines such as "follow us on …") | `ایرنا را در بله و روبیکا دنبال کنید` → removed |
| Remove links, `@mentions`, emojis and symbols | `🔹`, `📡 @Mehrnews`, `mehrnews.com` → removed |
| Hashtags become words | `#اینفو_ایرنا` → `اینفو ایرنا` |
| Arabic letter variants → Persian | `ي ى` → `ی`, `ك` → `ک`, `ة` → `ه` |
| Arabic and Latin digits → Persian | `2026` → `۲۰۲۶` |
| Remove diacritics and the stretching character | `شَهید` → `شهید`, `ســـلام` → `سلام` |
| Half-space instead of a space after the prefix می / نمی | `می گوید` → `می‌گوید` |
| Remove stop words (only in `tokens`) | `از`, `به`, `که`, `این` … |

The Persian letters پ چ ژ گ and the half-space (zero-width non-joiner) are kept.

**Why not `hazm`?** The library `hazm` forces an old `numpy` version that breaks `pandas` in this environment.
The rules are therefore implemented directly in the script; only hazm's stop word list is used (`stopwords_fa.txt`, MIT licence).

### Result

| Channel | Posts | without text | Ø words per post |
|---|---|---|---|
| IRNA | 59,546 | 16.4% | 86 |
| IRIB News | 47,698 | 10.8% | 45 |
| Mehr News | 65,728 | 21.2% | 48 |
| Tasnim News | 58,160 | 17.0% | 63 |
| Fars News | 49,925 | 26.6% | 46 |
| Jamaran | 47,273 | 18.5% | 78 |

"Without text" = images or videos without a caption, or posts that consisted only of advertising or links.

### Checks

`05_check_cleaning.sql` checks the result:

| Check | Result |
|---|---|
| Arabic letter variants left | ✅ 0 |
| Links or `@mentions` left | 1 – checked, correct |
| Posts with Persian text that are empty after cleaning | 22 – checked: only advertising lines |
| 20 posts with the most removed words | ✅ checked: only advertising, links, `@mentions` removed |
| Random sample of 20 posts, read in full | ✅ correct |

The first run split words beginning with می (`میدان` → `می‌دان`). The rule was restricted to
`می` followed by a space, and the cleaning was run again.

---

## Technology

PostgreSQL 18 · Python (`pandas`, `SQLAlchemy`, `psycopg`) · DBeaver

| File | Purpose |
|---|---|
| `scripts/database/01_schema.sql` | table structure |
| `scripts/database/02_load_database.py` | load raw data |
| `scripts/database/03_example_queries.sql` | example queries |
| `scripts/database/04_clean_text.py` | text cleaning |
| `scripts/database/stopwords_fa.txt` | Persian stop words (from `hazm`, MIT licence) |
| `scripts/database/05_check_cleaning.sql` | checks of the cleaning |
