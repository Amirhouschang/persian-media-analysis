**English** | [Deutsch](../de/bericht.md)

# Wording, Topics and Reach of Iranian News Channels on Telegram, 2026

**Results report** · six channels · 1 Jan – 31 Aug 2026 · 328,330 posts

[← back to overview](../../README.md)

> **Scope of this report:** It summarises the results. The results come from [04 – Analysis](04_analysis.md) (with charts,
> method and limitations) and from the AI check in [03 – AI classification](03_ai_classification.md), the channel counts
> from [01 – Data collection](01_data_collection.md), the events from the project's background material. Terms appear as
> they do in the sources; they are counted and reported, not judged. Assigning a peak to an event is an interpretation
> based on the typical terms of the week (see section 3).

## Summary

The study covers 328,330 posts from six Persian-language Telegram channels of Iranian news organisations: three state
channels (IRNA, IRIB News, Mehr News), two affiliated with the Revolutionary Guards (IRGC) (Tasnim News, Fars News) and
one reformist channel (Jamaran). The period includes the protests at the turn of 2025/26, the war between Israel, the US
and Iran from 28 Feb 2026, the ceasefire from 8 April and its collapse on 7/8 July. All posts were counted in full; in
addition, a locally run language model assigned a topic to 10,750 posts.

1. **Volume and topics** change strongly with the war. Averaged over the groups, a channel publishes 122–134 posts per day before the war, in the
   first full week of the war (from 2 Mar) 321–423 (single channels: 227 at IRNA to 505 at Mehr News). The share of military posts rises from 4–5% to 36–45%, the share of domestic-politics
   posts falls from 24–31% to 6–10% (AI classification).
2. **The highest values for "martyr" and "revenge"** are not at the start of the war but in the weeks of the funeral
   ceremony and processions for Ali Khamenei (3–10 July).
3. **"Zionist regime"** makes up 57% (state) and 53% (IRGC-affiliated) of all designations for Israel after the collapse
   of the ceasefire, 26% at Jamaran; "Israel" is Jamaran's most frequent designation over the whole period at 65%.
4. **Mojtaba Khamenei** is called "leader" by no channel before his election on 8 March. Of the posts about one of the two
   Khameneis, 74% (ceasefire) and 79% (after the collapse) concern the killed Ali Khamenei.
5. **The three groups** differ in terms, topics and countries: the state channels use the language of government,
   administration and international law, the IRGC-affiliated channels that of weapons, targets and mobilisation, Jamaran
   that of negotiations, the US and the nuclear issue.
6. **Reach:** the IRGC-affiliated channels reach a median of 11,858 views per post, the state channels 1,259, Jamaran
   1,593. Subscriber numbers were not collected.

---

## 1. Subject, data and method

**Question.** How do state, IRGC-affiliated and reformist news channels differ in volume, choice of topics, wording and
reach – and how do these patterns change around key events? (Tone is not evaluated, see Method.)

**Data.** The collected posts of the six channels from 1 Jan to 31 Aug 2026; 267,548 of the 328,330 posts contain text.

| Group | Channel | Posts |
|---|---|---|
| state | IRNA | 59,546 |
| state | IRIB News | 47,698 |
| state | Mehr News | 65,728 |
| IRGC-affiliated | Tasnim News | 58,160 |
| IRGC-affiliated | Fars News | 49,925 |
| reformist | Jamaran | 47,273 |

**Phases** (days by UTC date, boundaries set by the author):

| Phase | Period |
|---|---|
| before the war | 1 Jan – 27 Feb |
| war | 28 Feb – 7 Apr |
| ceasefire | 8 Apr – 6 Jul |
| after the collapse of the ceasefire | 7 Jul – 31 Aug |

**Events for orientation** (from the project's background material, `scripts/ai/background.txt`; 1 March as the day of
the official confirmation is set by the author, the dates of the funeral ceremony come from Al Jazeera reports):

| Date | Event |
|---|---|
| 28 Dec 2025 | nationwide protests begin over the economic situation; internet blackout from 8 Jan |
| 6 Feb, 17 Feb, 26 Feb | US–Iran nuclear talks in Muscat and Geneva, mediated by Oman; no agreement |
| 28 Feb | US and Israeli strikes on Iran, Ali Khamenei killed; strike on the elementary school in Minab (about 156 dead, about 120 of them children) |
| 1 Mar | Ali Khamenei's death officially confirmed in Iran |
| 8 Mar | Assembly of Experts selects Mojtaba Khamenei as Supreme Leader |
| 8 Apr | US–Iran ceasefire, mediated by Pakistan; 11–12 Apr talks in Islamabad without agreement |
| 13 Apr | US naval blockade of Iranian shipping |
| 17–18 Jun | "Islamabad Memorandum" (60 days of negotiations, passage through Hormuz, timetable for ending the blockade) |
| 3–10 Jul | funeral ceremony and processions for Ali Khamenei |
| 7–8 Jul | attacks on commercial vessels near Hormuz, renewed US strikes, collapse of the ceasefire |
| 20–22 Jul | Houthis declare a maritime blockade on Saudi Arabia |

**Method** (details: [04, section 10](04_analysis.md#10-method)).

- **Counting:** Fixed terms of two to four words were found without a predefined word list, and every passage of text was
  counted exactly once (1,501 terms). States, persons and actors were counted from an open list (113 terms with 188
  spellings in 10 categories). Unit: mentions **per 1,000 words**; time series per calendar week (starting Monday),
  complete weeks only.
- **Typical terms:** weighted log-odds ratio with z-score (above 1.96 statistically clear). A term counts for a group only
  if every one of its channels uses it more often. For peak weeks, one week is compared with all other weeks of the same
  group.
- **Topics:** Gemma 4 31B (local), codebook v8, 10,750 posts, weighted to all 231,406 posts with more than 80 characters.
  Final validation on 200 new, hand-coded posts: topic correct in 72.5% of cases (95% interval 65.9–78.2%; kappa 0.68).
- **Tone:** not evaluated (kappa 0.46; the AI overlooks non-neutral tones, to a different degree in each group).

---

## 2. Results

### 2.1 Topics and activity by phase

Share of posts per topic in percent (AI classification, weighted); a range gives the lowest to the highest value of the
three groups ([04, section 7](04_analysis.md#7-topics-according-to-the-ai)).

| | before the war | war | ceasefire | after the collapse |
|---|---|---|---|---|
| Military, all groups | 4–5 | 36–45 | 13–15 | 14–28 |
| Domestic politics, all groups | 24–31 | 6–10 | 11–13 | 15–19 |
| Diplomacy, Jamaran | 23.2 | 18.2 | 25.1 | 11.5 |
| Diplomacy, IRGC-affiliated | 11.6 | 6.7 | 16.8 | 8.8 |
| Mourning and commemoration, all groups | 3–5 | 6–8 | 9–12 | 6–10 |
| Other (service, weather, sport, culture), state | 20.5 | 5.2 | 18.5 | 17.9 |

- Jamaran has the highest share of diplomacy in every phase.
- **Activity:** averaged over the groups, a channel publishes 122–134 posts per day before the war (single channels
  109–178); in the first week of the war (from 2 Mar) 321–423 (IRNA 227, Mehr News 505). A second peak lies in the state and
  IRGC-affiliated channels in the weeks from 29 Jun and 6 Jul (funeral ceremony, collapse of the ceasefire), at Jamaran in
  the week from 13 Jul.
- **Caution:** the AI assigned *military* too often and *diplomacy* too rarely; changes over time are more reliable than
  the level of the values. For Jamaran the assignment was the least certain (55.9% correct, 34 posts checked).

### 2.2 January and February: protests, internet blackout, negotiations

([04, section 5](04_analysis.md#5-change-over-time-what-happened-when) and [6](04_analysis.md#6-countries-and-allies)). Values for individual countries are mentions per 1,000 words, all groups together.

- **Opponent labels** (e.g. "rioters", "traitors", "counter-revolution"): highest value in the IRGC-affiliated channels in
  the week from 5 Jan (3.34 per 1,000 words). Typical for that week were, among others, "rioters", "protest", "food
  coupon", "foreign currency", "cooking oil", "Venezuela" and "Maduro".
- In the week from 12 Jan the highest value is in the state channels (2.17). Typical were "riots", "terrorists", "armed",
  "agitators", "sedition", "Pahlavi" and "Mossad". In that week Jamaran published 20 posts per day, IRNA none.
- **Venezuela:** highest value in the week from 5 Jan (2.50, all groups); typical were "abducted", "wife", "court",
  "international law" and "violation" – the posts concern the capture of Nicolás Maduro and his wife by the US.
- **EU:** highest value in the week from 26 Jan (1.22); typical were "Revolutionary Guards", "terrorist", "hostile" and
  "irresponsible" – the EU's political agreement of 29 Jan to list the Revolutionary Guards as a terrorist organisation.
- **Negotiations:** highest value in the week from 2 Feb (nuclear talks in Muscat on 6 Feb): Jamaran 6.2, state 3.7,
  IRGC-affiliated 3.5.

### 2.3 Start of the war and change of leader (28 Feb – 8 Mar)

([04, section 4](04_analysis.md#4-which-khamenei-is-meant) and [3](04_analysis.md#3-how-the-channels-name))

- On 1 March, the day of the official confirmation, all six channels write "the martyr leader" (`رهبر شهید`) for the first
  time.
- **Crime terms** (e.g. "crime", "genocide", "child killer", "Minab") reach their highest value in the state channels
  (2.08 per 1,000 words) and at Jamaran (1.56) in the week from 2 Mar, the first full week after the start of the war. In
  the IRGC-affiliated channels this week (1.60) is second; their highest value (1.79) lies in the week from 20 Jul, with no
  single event recognisable. Over the whole period about a third of the crime terms (32–37%) concern the strike on the
  elementary school in Minab.
- All six channels name Mojtaba Khamenei in a sentence with "leader" for the first time on 8 March, the day of his
  election, none earlier. Jamaran and Mehr News write his name from 3 March, Tasnim from 5 March, not yet as leader.
- Share of the posts that name one of the two Khameneis (22,897 posts, all six channels):

  | Phase | Ali Khamenei | Mojtaba Khamenei | both |
  |---|---|---|---|
  | war (28 Feb – 7 Apr) | 55% | 35% | 10% |
  | ceasefire | 74% | 22% | 4% |
  | after the collapse | 79% | 17% | 3% |

- **President Pezeshkian** is named less often in the war: IRGC-affiliated 0.17 per 1,000 words (before the war 0.60, in
  the ceasefire and after 0.37), state 0.26 (before 0.55).

### 2.4 Ceasefire and negotiations (8 Apr – 6 Jul)

([04, section 5](04_analysis.md#5-change-over-time-what-happened-when) and [6](04_analysis.md#6-countries-and-allies)). Values for individual countries: all groups together.

- **Trump:** in the week from 13 Apr (US naval blockade) "Trump" reaches its highest value in all groups: Jamaran 4.5,
  IRGC-affiliated 4.0, state 3.4.
- **Ghalibaf:** in the same week his value in the IRGC-affiliated channels is 0.95 (whole period: 0.32). Typical for the
  week were "ceasefire", "naval blockade", "negotiations" and "Strait of Hormuz". In the ceasefire he rises in the
  IRGC-affiliated channels from 0.23 (war) to 0.43, at Jamaran from 0.15 to 0.39.
- **Pakistan:** in all six channels the highest value is in the ceasefire (groups: 0.72–0.92 per 1,000 words, before the
  war 0.21–0.31). In posts about Pakistan the IRGC-affiliated channels use "dispatched reporter", "negotiating team",
  "Ghalibaf" and "Vance" especially often.
- **Lebanon:** 1.86–2.45 in the ceasefire (war: 0.61–0.88). Highest weekly value of all countries: week from 1 Jun (3.82),
  3.40 in the week from 15 Jun (Lebanon as part of the memorandum).
- **Islamabad Memorandum (17–18 Jun):** in the week from 15 Jun "negotiations" is 4.1 at Jamaran and 2.9 in the
  IRGC-affiliated channels; typical were "memorandum", "signing" and "Muharram".
- **United Arab Emirates:** highest value in the week from 4 May (1.36; strike on the port of Fujairah), 0.99 in the week
  from 11 May (typical: "Netanyahu", "trip", "secret", "denial" – reports of a secret visit by Netanyahu, with a denial).
- **China:** highest value in the week from 11 May (1.81; typical: "Trump", "trip", "Xi Jinping", "Beijing" – Trump's trip
  to Beijing); 0.90 in the week from 18 May ("Putin", "trip").
- **Internet:** from April to early June Jamaran names the internet more than five times as often as the other groups
  (1.04 versus 0.17 and 0.20). Highest values: week from 11 May (1.74; "Internet Pro") and from 25 May (1.76;
  "reopening").

### 2.5 July: funeral ceremony and collapse of the ceasefire

([04, section 5](04_analysis.md#5-change-over-time-what-happened-when) and [6](04_analysis.md#6-countries-and-allies))

| Week from | Value per 1,000 words | Typical terms of the week |
|---|---|---|
| 29 Jun | "martyr": IRGC-affiliated 19.1 · state 14.1 · Jamaran 7.6 | "farewell ceremony", "Tehran prayer ground", "paying respects", "escort" |
| 6 Jul | "martyr": IRGC-affiliated **21.6** · state 17.5; revenge terms: IRGC-affiliated **1.48** · state 0.84 · Jamaran 0.54 | "funeral procession", "holy body", "Mashhad", "Najaf" |
| 13 Jul (second peak) | revenge terms: state 0.58 · Jamaran 0.41 | "Bandar Abbas", "Hormozgan", "Bushehr", "Ahvaz", "explosion", "Kuwait", "Jordan" |

- The highest values for "martyr" and "revenge" in the whole period lie in these weeks, not in the first week of the war
  (revenge terms then: IRGC-affiliated 0.89).
- After the collapse of the ceasefire Kuwait (week from 13 Jul: 1.14), Bahrain (0.76) and Jordan (0.86) also reach their
  highest values; typical for the posts about these countries were "Operation Blitz" (Kuwait: week from 20 Jul) and "fuel
  tanks" (Bahrain, Jordan).
- In the week from 29 Jun (funeral ceremony) Jamaran writes "Zionist regime" in 44% of the designations for Israel – the
  channel's highest value in the whole period (second highest: 39%, week from 20 Apr).
- **Saudi Arabia** is named 1.35 per 1,000 words in the IRGC-affiliated channels after the collapse (before 0.30–0.44),
  **Yemen** 1.00 (before 0.18–0.21), **Iraq** 1.45 (before 0.44–0.66). **Hezbollah** falls to 0.16–0.22 (ceasefire:
  0.59–1.20; before the war: 0.14–0.18).

### 2.6 Designations and persons

([04, section 2](04_analysis.md#2-whom-the-channels-name) and [3](04_analysis.md#3-how-the-channels-name))

Share of all designations for Israel:

| | state | IRGC-affiliated | Jamaran |
|---|---|---|---|
| "Zionist regime" (`رژیم صهیونیستی`), whole period | 48% | 40% | 29% |
| before the war | 46% | 40% | 28% |
| war | 42% | 35% | 31% |
| ceasefire | 48% | 40% | 29% |
| after the collapse | 57% | 53% | 26% |
| "Israel" (`اسرائیل`), whole period | 45% | 50% | 65% |

- **USA:** "America" is the main designation in all groups (76–84%). Jamaran uses the formal designation "United States"
  more often (11% versus 7% and 5%). Derogatory designations ("terrorist army of America", "child-killing army of
  America") make up 3–5% of all designations for the US after the collapse of the ceasefire, 1–2% in the war, 0% before the
  war.
- **Words directly after "Trump":** "claims" 8.2% at Jamaran, 2.8% state, 3.0% IRGC-affiliated; "criminal" 1.4% in the
  IRGC-affiliated channels (state 0.5%); "gambler" 0.6% (among the 20 most frequent only in the IRGC-affiliated channels).
- **Mentions per 1,000 words, whole period:** Trump 1.86 (state), 2.06 (IRGC-affiliated), 3.11 (Jamaran); Khatami
  0.01 / 0.02 / 0.12. In absolute numbers Khatami is named 366 times at Jamaran, 122 times in the three state channels
  together.

### 2.7 Countries

([04, section 6](04_analysis.md#6-countries-and-allies))

About a quarter of all posts with text (67,669) name at least one country or group of the list ([04, section 6](04_analysis.md#6-countries-and-allies)). Named most
often are Lebanon (20,759 mentions), Iraq (11,655) and Russia (10,056). The IRGC-affiliated channels name Hezbollah almost
twice as often as the others (0.85 versus 0.45 and 0.44).

Mentions per 1,000 words by phase (for "all groups": lowest to highest value of the three groups):

| | before the war | war | ceasefire | after the collapse |
|---|---|---|---|---|
| Russia, IRGC-affiliated | 0.71 | 0.24 | 0.61 | 0.62 |
| China, IRGC-affiliated | 0.39 | 0.13 | 0.53 | 0.32 |
| Gaza, all groups | 0.37–0.45 | 0.08–0.12 | 0.20–0.41 | 0.28–0.47 |
| Bahrain, all groups | 0.02 | 0.33–0.46 | 0.11–0.17 | 0.21–0.43 |
| Kuwait, all groups | 0.01–0.04 | 0.33–0.47 | 0.11–0.17 | 0.32–0.59 |
| Hezbollah, all groups | 0.14–0.18 | 0.65–1.24 | 0.59–1.20 | 0.16–0.22 |
| Lebanon, all groups | 0.36–0.52 | 0.61–0.88 | 1.86–2.45 | 0.59–0.98 |
| Pakistan, all groups | 0.21–0.31 | 0.16–0.26 | 0.72–0.92 | 0.30–0.50 |
| Saudi Arabia, IRGC-affiliated | 0.30 | 0.44 | 0.30 | 1.35 |
| Yemen, IRGC-affiliated | 0.18 | 0.21 | 0.18 | 1.00 |
| Iraq, IRGC-affiliated | 0.44 | 0.66 | 0.53 | 1.45 |

The same country appears in the groups with different terms (typical terms of the posts about the country):

- **United Arab Emirates:** state "toman", "gold coin", "transfer" (currency trading in Dubai); IRGC-affiliated "port of
  Fujairah", "infrastructure", "air defence"; Jamaran "Trump", "agreement", "think tank".
- **Saudi Arabia:** state "consultation", "minister", "condemned"; IRGC-affiliated "Yemen", "mercenaries", "Sanaa",
  "blockade"; Jamaran "Israel", "Houthis", "Abu Dhabi", "dependence".

### 2.8 Profiles of the groups

([04, section 1](04_analysis.md#1-what-each-group-writes-about))

- **State:** government spokespeople and diplomacy ("foreign ministry spokesman", "foreign minister"), the language of
  international law ("aggression", "condemnation", "United Nations"), administration and service (provinces, weather
  service, earthquakes, examination authority), calendar. Outside the war 17.9–20.5% of posts belong to "other".
- **IRGC-affiliated:** weapons and attacks ("drone", "missile", "impact"), targets in Israel and the Gulf, Hezbollah (most
  typical term, z 20.8), protests as "riots", arrests, mobilisation ("oath of allegiance", "blood revenge", "revenge").
- **Jamaran:** Trump (most typical term, z 44.6), negotiations, the nuclear issue, words of distance ("claims",
  "probably", "unlikely"), international media (Axios, CNN, New York Times and others), politicians of the reformist camp
  (Khatami, Zarif, Rouhani), the internet and blocking.

### 2.9 Activity and reach

([04, section 8](04_analysis.md#8-activity-and-reach))

| | state | IRGC-affiliated | Jamaran |
|---|---|---|---|
| Posts per day and channel | 237 | 222 | 195 |
| Views per post (median) | 1,259 | 11,858 | 1,593 |
| Forwards per post (median) | 5 | 18 | 5 |
| Forwards per 1,000 views | 5.1 | 2.1 | 4.2 |

With the start of the war the views per post fall at Jamaran (from 3,329 to 969) and in the IRGC-affiliated channels
(from 18,586 to 12,309), although more is posted; in the state channels the group median stays the same (1,803 and
1,802). Possible reasons cannot be separated with these data. Reach probably depends mostly on the number of subscribers, which was not
collected.

---

## 3. Limitations

- **Counting is not understanding:** a term counts the same whether used approvingly, at a distance or as a quotation.
- **Peak weeks:** the typical terms describe the whole week, not only the posts with the counted word. Assigning weeks to
  events is an interpretation based on the data and the timeline.
- **Selection:** six channels on Telegram, the reformist camp represented by one channel only; opposition and exile
  media are not included. The results apply to these channels.
- **The author's settings:** correction list, naming list, phase and event dates; other settings would give slightly
  different numbers.
- **AI topics:** weighted sample, topic correct in 72.5% of cases; military rather overestimated, diplomacy rather
  underestimated; the reference and the codebook come from one person. Tone is not evaluated.
- **Reach:** views and forwards are the state at the time of collection; subscriber numbers are missing.
- **Countries:** `عمان` means Oman and Amman; `آذربایجان` alone counts as the Republic of Azerbaijan but sometimes means
  Iranian provinces (value too high); Egypt is missing; part of the mentions of European countries concerns sport.
- **January:** IRNA and Jamaran published hardly any posts in mid-January (internet blackout).
- **Time zone:** days, weeks and phases are based on the UTC date of the posts (Tehran: UTC+3:30); only the AI topic shares use the Tehran date (there the ceasefire ends on 7 Jul instead of 6 Jul). By UTC date, 48 of 10,750 AI posts would fall into another phase (37 of them at this boundary), and the group shares would change by at most 1.5 percentage points.
- **Scope of the project:** it is primarily technical and gives a reliable overview, not an in-depth scholarly analysis;
  such a study would read the posts individually and run to 100 pages or more. For firmer results, several native Persian
  speakers should code independently and discuss the codebook together.

## 4. Further documents

- [04 – Analysis](04_analysis.md): all results with charts, method and limitations
- [03 – AI classification](03_ai_classification.md): codebook, model comparison, final validation
- [06 – Methodology](06_methodology.md): settings, limitations, data protection, security, reproducibility
- [02 – Processing](02_processing.md) and [01 – Data collection](01_data_collection.md)
- Result files: [results/README.md](../../results/README.md)
