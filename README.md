**English** | [Deutsch](README.de.md)

# Iranian News Channels in the 2026 War – Telegram Analysis with Local AI

**Python · SQL · NLP · local AI**

End-to-end project collecting, processing and analysing more than **328,000 Persian-language Telegram
posts** from six Iranian news channels between 1 January and 31 August 2026 – the period of the January
protests, the war between Israel/the US and Iran from 28 February, and the ceasefires that followed.
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
| 2. Processing | Cleaning Persian text, PostgreSQL | ⬜ planned | 02 – Processing |
| 3. AI classification | Codebook, model comparison, main run, validation | ⏳ main run | [03 – AI classification](docs/en/03_ai_classification.md) |
| 4. Analysis | Time series, event analysis, framing, reach | ⬜ planned | 04 – Analysis |
| 5. Dashboard | local interactive dashboard | ⬜ planned | 05 – Dashboard |
| 6. Methodology & limits | Limitations, data protection, security | ⬜ planned | 06 – Methodology |

### 1. Data collection
- Public channels retrieved via the official Telegram API (`Telethon`)
- Pauses on rate limits, separate files for channels added later
- Automated quality checks (completeness, duplicates, gaps) with targeted re-checks of unusual periods

### 2. Processing *(planned)*
- Normalising Persian script (Arabic vs. Persian characters, zero-width non-joiners) with `hazm`
- Removing links, emojis and duplicates; assigning time phases
- Relational database in **PostgreSQL**, queries and checks in **DBeaver**

### 3. AI classification *(main run)*
- Classification by **topic** (9 categories) and **tone** (6 categories) with **locally run language models** (`Ollama`) – no cloud
- **Codebook** with operational definitions, developed over eight versions
- **Context:** neutral background on events, actors, international law and a glossary of Persian terms
- **Model comparison** on 150 manually checked posts: Gemma 4 (26B, 31B), Qwen 3.6 (27B, 35B), Qwen 2.5 (32B), Aya Expanse (32B)
- **Selected model: Gemma 4 31B** – 80.7% exact agreement on topic and tone, 86.7% when borderline cases are taken into account; Cohen's kappa topic 0.85, tone 0.79
- **Main run:** stratified sample of about 10,500 posts (50 per channel and week), weighted
- **Final validation:** 200 new posts coded blind – no changes afterwards
- The full process, including dead ends: [03 – AI classification](docs/en/03_ai_classification.md)

### 4. Analysis *(planned)*
- Publishing activity over time and around key events
- Comparison of source groups by topic, tone and reach
- Terminology and framing analysis: which terms do which sources use for the same events?
- Density of ideological terms per 1,000 words

### 5. Dashboard *(planned)*
- Interactive charts with `Plotly`, local dashboard with `Streamlit`

---

## Tech stack

| Area | Tools |
|---|---|
| Language & environment | Python 3.11, conda, Linux |
| Data collection | Telethon |
| Text processing | hazm |
| Database & SQL | PostgreSQL, DBeaver |
| Analysis | pandas |
| Local AI | Ollama (Gemma 4, Qwen, Aya Expanse) |
| Visualisation | Plotly, Streamlit |

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
│   └── ai/              ← AI classification: config, codebook, background, model comparison, main run
├── results/ai/          ← published AI results (no post texts)
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
