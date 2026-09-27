**English** | [Deutsch](README.de.md)

# Iranian News Channels in the 2026 War – Telegram Analysis with Local AI

**Python · SQL · NLP · local AI**

End-to-end project collecting, processing and analysing more than **328,000 Persian-language Telegram
posts** from six Iranian news channels between 1 January and 31 August 2026 – the period of the protests that began in late December 2025, 
the war between Israel/the US and Iran from 28 February, and the ceasefires that followed.
It covers automated data collection, a relational database and classification with locally run language
models. The focus is on method: how can foreign-language media be analysed systematically, verifiably
and reproducibly?

> **Note:** Code, methodology and results are public. The raw post texts are not part of this repository
> for copyright reasons; every post can be found publicly via channel and ID (`t.me/<channel>/<id>`).

---

## Research question

How do state, IRGC-affiliated and reformist news channels differ in **volume, choice of topics, wording,
tone and reach** – and how do these patterns change around key events?

## Sources

| Group | Channel | Telegram | Description (neutral) | Posts |
|---|---|---|---|---|
| 1 – state / official | IRNA | `@IRNA_1313` | official state news agency, supervised by the government | 59,546 |
| 1 – state / official | IRIB News | `@iribnews` | news service of the state broadcaster, whose head is appointed by the Supreme Leader | 47,698 |
| 1 – state / official | Mehr News | `@mehrnews` | semi-official agency owned by the Islamic Development Organization (under the Supreme Leader) | 65,728 |
| 2 – IRGC-affiliated | Tasnim News | `@Tasnimnews` | semi-official agency widely described as IRGC-affiliated | 58,160 |
| 2 – IRGC-affiliated | Fars News | `@farsna` | semi-official agency widely described as IRGC-affiliated | 49,925 |
| 3 – reformist | Jamaran | `@jamarannews` | news outlet linked to the institute publishing Ayatollah Khomeini's works; associated with the reformist camp | 47,273 |

## Data

| | |
|---|---|
| Period | 1 Jan – 31 Aug 2026 |
| Sources | 6 public Telegram channels in three source groups |
| Volume | 328,330 posts |
| Language | Persian |

---

## Pipeline and status

| Step | Content | Status | Details |
|---|---|---|---|
| 1. Data collection | Telegram API, quality checks | ✅ done | [01 – Data collection](docs/en/01_data_collection.md) |
| 2. Processing | PostgreSQL database, cleaning Persian text | ✅ done | [02 – Processing](docs/en/02_processing.md) |
| 3. AI classification | Codebook, model comparison, main run, validation | ⏳ main run | [03 – AI classification](docs/en/03_ai_classification.md) |
| 4. Analysis | Word choice, naming, change over time, countries, reach | ✅ word analysis · ⏳ AI results | [04 – Analysis](docs/en/04_analysis.md) |
| 5. Dashboard | local interactive dashboard | ⬜ planned | 05 – Dashboard |
| 6. Methodology & limits | Limitations, data protection, security | ⬜ planned | 06 – Methodology |

### 1. Data collection
- Public channels retrieved via the official Telegram API (`Telethon`)
- Pauses on rate limits, separate files for channels added later
- Automated quality checks (completeness, duplicates, gaps) with targeted re-checks of unusual periods

### 2. Processing
- Relational database in **PostgreSQL** (snowflake schema): posts, channels, source groups, dates, phases – queries in **DBeaver**
- Four phases of the period (before the war, war, ceasefire, after the ceasefire collapsed) as a separate table
- Cleaning of all 328,330 texts: normalising Persian script (Arabic vs. Persian characters, digits, half-spaces), removing links, emojis and channel advertising, removing stop words – with checks in SQL

![Database schema](images/database_schema.png)

### 3. AI classification *(main run)*
- Classification by **topic** (9 categories) and **tone** (6 categories) with **locally run language models** (`Ollama`) – no cloud
- **Codebook** with operational definitions, developed over eight versions
- **Context:** neutral background on events, actors, international law and a glossary of Persian terms
- **Model comparison** on 150 manually checked posts: Gemma 4 (26B, 31B), Qwen 3.6 (27B, 35B), Qwen 2.5 (32B), Aya Expanse (32B)
- **Selected model: Gemma 4 31B** – 80.7% exact agreement on topic and tone, 86.7% when borderline cases are taken into account; Cohen's kappa topic 0.85, tone 0.79
- **Main run:** stratified sample of about 10,500 posts (50 per channel and week), weighted
- **Final validation:** 200 new posts coded blind – no changes afterwards
- The full process, including dead ends: [03 – AI classification](docs/en/03_ai_classification.md)

### 4. Analysis *(word analysis complete)*
- Complete corpus, counted per 1,000 words; fixed terms found **without a predefined word list**, author's corrections kept openly in one file
- **Typical terms** per source group with the weighted log-odds ratio (Monroe et al. 2008) – a term only counts if it is typical for every channel of the group
- **Naming:** how each group names Israel, the USA, opponents and persons; words next to Trump and Netanyahu
- **Which Khamenei?** Rule-based assignment of every mention of the Leader to Ali or Mojtaba Khamenei, checked with samples
- **Weekly time series** around key events – every peak explained with the terms typical of that week – and **activity and reach** (posts, views, forwards)
- **Countries and allies:** 35 countries and groups (Gulf states, Lebanon and Hezbollah, Iraq, Yemen, Russia, China, Pakistan, Europe …) – how often, in which weeks, and how each group presents them

Selected findings:
- **Three voices:** state channels speak as government and administration (spokespeople, ministers, the language of international law – "aggression", "condemnation"); IRGC-affiliated channels report on missiles, drones, arrests and "riots"; Jamaran on negotiations, US politics, the nuclear issue and the internet.
- After the collapse of the ceasefire, state and IRGC-affiliated channels call Israel the "Zionist regime" (*rezhim-e sahyunisti*) in 57% and 53% of mentions; Jamaran writes "Israel" in 70%.
- No channel calls Mojtaba Khamenei the Leader before his selection on 8 March; even afterwards about three quarters of mentions of the Leader concern Ali Khamenei.
- The highest values for "martyr" and "revenge" are not at the start of the war but in the weeks of the farewell ceremony and funeral processions for Ali Khamenei (late June / early July).
- Former presidents and ministers of the reformist camp – Mohammad Khatami, Hassan Rouhani, Mohammad Javad Zarif – appear almost only at Jamaran; President Masoud Pezeshkian almost disappears from the news during the war.
- With the start of the war the world shrinks to the region: Russia and China fall to a third in the IRGC-affiliated channels; Bahrain and Kuwait, hardly named before, become scenes of action. The same country looks different in each group – the UAE are a currency hub for the state media, a target (port of Fujairah) for the IRGC-affiliated channels and an actor of US politics for Jamaran.
- IRGC-affiliated channels reach about ten times as many views per post, but are forwarded less often relative to their views.

![Share of "Zionist regime" among all names for Israel](results/timeline/charts/israel_zionist_regime_share.png)

Details, all charts and limitations: [04 – Analysis](docs/en/04_analysis.md)

### 5. Dashboard *(planned)*
- Interactive charts with `Plotly`, local dashboard with `Streamlit`

---

## Tech stack

| Area | Tools |
|---|---|
| Language & environment | Python 3.11, conda, Linux |
| Data collection | Telethon |
| Text processing | own normaliser (regex), stop words from hazm |
| Database & SQL | PostgreSQL, DBeaver |
| Analysis | pandas, numpy (log-odds) |
| Local AI | Ollama (Gemma 4, Qwen, Aya Expanse) |
| Visualisation | matplotlib; Plotly, Streamlit (planned) |

---

## Project structure

```
telegram-iran/
├── README.md            ← English version
├── README.de.md         ← German version
├── docs/
│   ├── en/              ← detailed pages in English
│   └── de/              ← detailed pages in German
├── scripts/
│   ├── telegram/        ← login, collection, re-collection, checks
│   ├── database/        ← PostgreSQL: schema, loading, example queries, text cleaning, checks
│   ├── ai/              ← AI classification: config, codebook, background, model comparison, main run
│   └── analysis/        ← word analysis, naming, leader, time series, peak weeks, activity, countries + two lists of the author
├── results/             ← published results, numbers only (no post texts) – see results/README.md
│   ├── words/           ← word frequencies, fixed terms, typical terms
│   ├── leader/          ← Ali or Mojtaba Khamenei
│   ├── naming/          ← naming, neighbouring words
│   ├── timeline/        ← weekly values, peak weeks and charts
│   ├── activity/        ← posts, views, forwards and charts
│   ├── countries/       ← countries and allies: frequency, peak weeks, presentation, charts
│   └── ai/              ← AI model comparison
└── data/                ← raw data (not in the repository)
```

---

## Data protection & methodology

- only **publicly available** editorial publications
- **no personal data** of users, no private groups or comments
- processing entirely **local**, including the AI classification
- credentials only as environment variables; raw data and session files excluded from the repository
- AI results are not taken over unchecked but validated against manual coding

## Skills demonstrated

- Data collection via APIs, including error handling and rate limits
- Data quality: systematic checks, handling gaps, documenting limitations
- Processing non-Latin scripts
- Text analysis without predefined word lists; statistical comparison of groups (log-odds, z-scores)
- SQL and relational databases
- Use and **validation** of local AI: codebook development, model comparison, measurable experiments
- Source-critical analysis of foreign-language media

## Status

Work in progress – the pages under `docs/` are extended after each completed step.

---

## Author's position

I reject war and violence against people, regardless of which side they come from. This project does not take a
political position: it describes how media report, not who is right. All sources are analysed by the same rules.
In the analysis I use neutral terms ("killed") for events such as the killing of politicians and military officers.
How differently media and states name such acts – for example as "elimination", "targeted killing" or "terror" –
is itself a subject of the analysis.

No human being may be killed – not even senior politicians and generals of the Islamic Republic of Iran, and least
of all in their homes, together with their families. This project is therefore no place for language that
trivialises or justifies such killings, including terms such as "elimination".
