**English** | [Deutsch](../de/01_datenerhebung.md)

# 01 – Data collection

[← back to overview](../../README.md)

This step describes how the raw data was collected and checked for completeness.
The raw post texts are not part of the repository for copyright reasons.

---

## Overview

| | |
|---|---|
| Access | official Telegram API |
| Tool | Python, `Telethon` |
| Volume | 6 public channels, 328,330 posts |
| Period | 1 Jan – 31 Aug 2026 |
| Status | done |

The channels are divided into **three source groups**:

| Group | Channels |
|---|---|
| 1 – state / official | IRNA, IRIB News, Mehr News |
| 2 – IRGC-affiliated | Tasnim News, Fars News |
| 3 – reformist | Jamaran |

---

## 1. Procedure

- Access via the **official API** with a personal developer account (API ID/hash)
- Only **public channels** of editorial media – no groups, no private users, no need to join channels
- One-time login via QR code; the session file stays local
- Posts are read backwards from the end date until the start date is reached
- Automatic pauses when the API applies rate limits
- Channels added later (here: Jamaran) are collected into a **separate file** with their own script, so existing data is never overwritten

### Fields collected

| Field | Meaning |
|---|---|
| `kanal` | Telegram name of the channel |
| `seite` | source group |
| `id` | unique post number within the channel (post available at `t.me/<channel>/<id>`) |
| `datum` | publication time (UTC) |
| `text` | post text (Persian) |
| `views` | views |
| `weiterleitungen` | number of forwards |
| `weitergeleitet_von` | origin, if the post itself was forwarded |

---

## 2. Result

**328,330 posts** from 6 channels:

| Channel | Group | Posts |
|---|---|---|
| IRNA (`@IRNA_1313`) | 1 | 59,546 |
| IRIB News (`@iribnews`) | 1 | 47,698 |
| Mehr News (`@mehrnews`) | 1 | 65,728 |
| Tasnim News (`@Tasnimnews`) | 2 | 58,160 |
| Fars News (`@farsna`) | 2 | 49,925 |
| Jamaran (`@jamarannews`) | 3 | 47,273 |

---

## 3. Quality checks

A dedicated check script tests the data on seven points and saves a report for each file.

| Check | Result |
|---|---|
| Rows per channel = collection output | ✅ matching |
| Period complete per channel | ✅ 1 Jan – 31 Aug for all channels |
| Duplicate posts | ✅ 0 |
| Posts without text | 11–27% per channel (images/videos without caption) |
| Days without posts | ⚠️ IRNA: 16 days – 14 consecutive (9–22 Jan) plus 16–17 Mar · Jamaran: 6 days (9–14 Jan) · all others: none |
| Posts per week | table for detecting drops |

### Handling gaps
For IRNA, the January period was **specifically re-queried** with a separate script.
Result: the posts are also missing directly on Telegram – the collection was complete; the gap lies in the channel itself.

The January gaps at IRNA and Jamaran fall into early January, when internet access in Iran was heavily
restricted during the protests. They are taken into account in the analysis
(comparisons per day instead of absolute totals, January considered separately).

### Scope
In addition, the web archive of **Sepah News**, the IRGC's official news site, was collected
(about 5,300 articles); its Telegram channel was not accessible from Germany.
The archive is not included in this analysis: long web articles without view counts are not directly
comparable with Telegram posts, and local AI classification of long texts requires considerably more
computing time. The data is reserved for a separate analysis.

### First observation from the weekly table
Publishing activity rises sharply from late February for almost all channels
and shows a second increase in July. IRNA hardly follows this pattern. Details will follow in 04 – Analysis.

---

## 4. Security and data protection

- API credentials only as **environment variables**, never in the code
- Session file, raw data and CSV files excluded from the repository via `.gitignore`
- Only editorial publications, **no personal data** of users
- All data is stored and processed locally only

---

## 5. Technical environment

- Linux (Arch), conda environment with Python 3.11
- Libraries: `telethon`, `pandas`, `qrcode`

### Project structure (excerpt)
```
telegram-iran/
├── data/
│   ├── row/        ← raw data + check reports (not in the repo)
│   └── ki/         ← AI classification results
└── scripts/
    ├── telegram/   ← login, collection, re-collection, checks
    └── ai/         ← AI classification (see 03)
```
