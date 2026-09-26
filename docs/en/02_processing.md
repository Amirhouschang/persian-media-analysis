**English** | [Deutsch](../de/02_aufbereitung.md)

# 02 – Processing: database and text cleaning

[← back to overview](../../README.md)

This step moves the raw data into a relational **PostgreSQL** database and prepares the Persian texts for analysis.

| Part | Status |
|---|---|
| Database `iran_media_2026` | ✅ done |
| Text cleaning with `hazm` | ⬜ planned |

---

## 1. Database

### Structure

Posts are at the centre; descriptive tables are linked via keys
(snowflake schema: `channels` → `source_groups`, `dates` → `phases`).

![Database schema](images/database_schema.png)

| Table | Key | Content | Rows |
|---|---|---|---|
| `posts` | `channel_id` + `post_id` | all posts: time, text, views, forwards, link | 328,330 |
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

## 2. Text cleaning *(planned)*

- Normalising Persian script (Arabic vs. Persian characters, zero-width non-joiners) with `hazm`
- Removing links, emojis and channel signatures
- Tokenising and removing stop words as the basis for the word analysis

---

## Technology

PostgreSQL 18 · Python (`pandas`, `SQLAlchemy`, `psycopg`) · DBeaver

| File | Purpose |
|---|---|
| `scripts/database/01_schema.sql` | table structure |
| `scripts/database/02_load_database.py` | load raw data |
| `scripts/database/03_example_queries.sql` | example queries |
