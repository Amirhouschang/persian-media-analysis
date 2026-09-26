**English** | [Deutsch](../de/03_ki_einordnung.md)

# 03 – AI classification by topic and tone

[← back to overview](../../README.md)

This page describes how Persian-language Telegram posts are classified by **topic** and **tone** using
**locally run language models** – and above all, how the procedure was developed, tested and improved.
The path was not straightforward: codebook, background knowledge, test data and model choice evolved over
eight versions. Dead ends are documented as well.

---

## Overview

| | |
|---|---|
| Task | Each post receives **one topic** (9 categories) and **one tone** (6 categories) |
| Technology | [Ollama](https://ollama.com) on the author's own computer – no cloud, no data leaves the laptop |
| Selected model | **Gemma 4 31B** with background knowledge |
| Codebook | version **v8** (frozen) |
| Agreement with manual coding | **80.7%** topic and tone exact · **86.7%** taking borderline cases into account · kappa topic 0.85 / tone 0.79 |
| Main run | stratified sample, about 10,500 posts (50 per channel and week) |
| Status | main run ⏳ · final validation (phase C) ⬜ |

---

## 1. Why local AI?

- **Data protection and independence:** texts are not sent to cloud providers.
- **Reproducibility:** fixed model version, `temperature = 0`, `seed = 42` – the same input gives the same output.
  This was tested: two runs of the same model with the same codebook produced exactly the same result.
- **Cost:** no running costs, only computing time.
- **Limit:** the hardware determines which models are possible (see section 5).

**Hardware:** laptop with AMD Ryzen AI 9 HX 370, 93 GB RAM, integrated Radeon 890M graphics,
no dedicated GPU. Operating system Linux (Arch/EndeavourOS).

---

## 2. The codebook

The codebook (`scripts/ai/codebook.py`) defines **what** the AI has to decide. Core principle:
each category describes **visible features of the text**, not interpretations. Example: *mournful* requires
explicit grief language ("with deep sorrow", "condolences") – a report on a funeral without such words is *neutral*.

### Topics

| Category | Short description |
|---|---|
| `military` | attacks, weapons, troops, military statements; also war events in Israel, the Gulf states, Iraq, Jordan |
| `diplomacy` | Iran's relations with other states and organisations, negotiations, mediation |
| `domestic_politics` | the Iranian state acting at home, judiciary, arrests, public services, domestic political debates |
| `economy` | prices, exchange rates, trade, subsidies, markets |
| `ideology_propaganda` | promotion of the Islamic Republic's ideology, slogans, anniversaries |
| `mourning_commemoration` | death, funerals, mourning, remembrance of the deceased |
| `resistance_axis` | Lebanon/Hezbollah, Gaza, Houthis, Iraqi militias, Syria – Iran not the acting party |
| `foreign_affairs` | events in other countries without a link to Iran or the war |
| `other` | weather, sport, culture, accidents, too little text |

### Tones (order of checking – the first that clearly applies wins)

`threatening` → `accusatory` → `mobilizing` → `triumphant` → `mournful` → `neutral`

### Key rules (excerpt)

- Topic **and** tone follow the **main statement** (usually the headline); a single side sentence does not decide.
- Standard labels of Iranian media ("martyr", "Zionist regime") do not decide the tone on their own.
- **Legal and descriptive terms** for the wars in Gaza, Lebanon and Iran ("genocide", "war crimes", "aggression",
  "illegal war") – including for killed civilians and children – are treated as descriptive and do not automatically
  make a text *accusatory*. This rule is a deliberate choice of the project; it applies equally to all sources.
- **Arrests and trials:** labelling political opponents, protesters, journalists or minorities (e.g. Kurds, Baluch,
  Baha'is) as "terrorists", "rioters", "traitors" or "spies" without a final court verdict is *accusatory*.
  Arrests of members of organisations on the UN or EU terrorist lists are *neutral*.
- If unsure between a tone and *neutral* → *neutral*.
- The source information helps understanding but must **not** decide topic or tone.

---

## 3. Context: what the AI is told in addition

Local models have a fixed knowledge cut-off and no web search. They do not know the events of 2026.
In the "with context" setting the AI therefore also receives:

1. **Background** (`scripts/ai/background.txt`, neutrally worded, researched and sourced):
   - 2026 timeline: January protests, negotiations, start of the war on 28 Feb, ceasefires, blockades
   - killed officials, key living actors (Iran, US, Israel, mediators)
   - relations and roles: Russia, China, Pakistan, Qatar, Oman; involvement of the Gulf states
   - basic terms of international law (sovereignty, humanitarian law, war crimes, human rights) – worded equally for all states
   - **glossary** of Persian terms (e.g. "رهبر شهید" = the killed Supreme Leader, "قرار شبانه" = nightly pro-government rally)
2. **Source description:** neutrally, who is behind each channel – e.g. IRNA as the official state agency,
   Tasnim and Fars as agencies widely described as IRGC-affiliated, Jamaran as an outlet associated with the reformist camp.

Rule: the context serves **only to understand** references; it must not decide topic or tone on its own.

---

## 4. How it was tested

**Reference:** manually coded posts (topic + tone). The AI's answer is compared with this reference.

**Metrics:**
- **Exact agreement** – share of posts where topic and tone match exactly
- **Agreement with borderline cases** – the AI topic also counts as correct if it matches the **secondary topic**
  set by the human coder (only for genuine borderline cases, 29 of 150 posts)
- **Cohen's kappa** – agreement corrected for chance (above 0.8 = almost perfect, 0.6–0.8 = substantial)
- confusion table, the AI's reasoning for every disagreement, seconds per post

**Tool:** `scripts/ai/03a_model_comparison.py` produces one Excel file per run with the sheets
`summary`, `side_by_side`, `disagreements`, `confusion`, `details`.

---

## 5. The path: eight versions

### Phase 1 – First tests (codebook v1–v3, 29 posts)

- Test set of 29 posts from the first five channels (IRNA, IRIB News, Mehr, Tasnim, Fars), coded manually.
- Tested: Gemma 4 (26B, 31B), Qwen 3.6 (27B), Qwen 2.5 (32B), Aya Expanse (8B, 32B) – each **with and without context**.
- **Finding 1:** the first categories described interpretations ("propagandistic"). After switching to visible text
  features, Gemma 4 26B's agreement rose from 55% to 72%.
- **Finding 2:** background knowledge improved topic classification for most models.
- Best result (v3): Gemma 4 31B with context – topic 97%, tone 86%, both 83%.
- **But:** 29 posts are few, and the codebook had been developed on exactly these posts. The figure was too optimistic.

### Codebook v4 – sources and sharper boundaries

- *military* narrowed (commanders' greetings are not military), anniversaries to *ideology_propaganda*,
  commemoration only when the focus is on the deceased, domestic political debates to *domestic_politics*.
- Neutral description of every source, with the rule that the source must not decide.

### Phase A – New, larger test set (codebook v5–v6, 150 posts)

- **Test set 2:** 150 posts, 25 from each of the six channels (now including Jamaran), randomly drawn, excluding posts from test set 1.
- **How the reference was created:** the posts were pre-coded with the help of an AI assistant (Claude) and then
  checked and corrected line by line by the author. The reference was therefore **not created fully blind** –
  one reason for the separate final validation (phase C).
- **v5:** tone by main statement instead of single sentences; new rule on legal terms.

| Codebook v5 | Topic | Tone | Both | Sec./post |
|---|---|---|---|---|
| Gemma 4 26B | 80.7% | 84.0% | 70.0% | 3.2 |
| Gemma 4 31B | 78.7% | 87.3% | 69.3% | 20.0 |

- **Analysis of disagreements:** in 24 posts both models agreed with each other but not with the reference.
  These cases were checked one by one. Result: sometimes the reference was wrong, sometimes rules were missing – above all
  for war events abroad (sirens in Bahrain, explosions in Kuwait) and for arrests of political opponents.
- **v6:** war events in Israel, the Gulf states, Iraq and Jordan → *military*; rule on arrests and labels without a verdict;
  rule on legal terms tightened.

| Gemma 4 26B | Topic | Tone | Both |
|---|---|---|---|
| v5 | 80.7% | 84.0% | 70.0% |
| v6 | 85.3% | 91.3% | 80.0% |

- **Honest breakdown of the increase:** about half of the +10 points came from the corrected reference
  (the old v5 output already reaches 75.3% against the new reference), the other half from the new rules.

### Dead end 1 – more knowledge does not automatically help

- After analysing the errors, the background was extended with a glossary, foreign relations and international law.
- Result: 78.0% instead of 80.0% – 5 posts better, 8 worse, i.e. random variation.
- **Finding:** the knowledge arrived (the AI now recognised pro-government rallies, for example), but the remaining
  errors were due to **fuzzy boundaries between categories**, not missing knowledge.
  The extended background was kept anyway because it is useful for the ~10,500 posts of the main run.

### Dead end 2 – secondary topic set by the AI (v7)

- Idea: in genuine borderline cases the AI may give a second topic – with a very strict rule.
- Result: the AI still set a secondary topic for **38.7%** of posts. The lenient metric would have been inflated,
  and computing time rose by 0.4 seconds per post.
- **Solution (v8):** the AI gives only one topic. The secondary topic is set **only by the human** in the reference.
  This way the "borderline" metric fairly measures how often the AI hits a classification the human accepted as equivalent.

### Final comparison – all models with codebook v8

| Model | Both exact | Both incl. borderline | Kappa topic | Kappa tone | Sec./post (median) |
|---|---|---|---|---|---|
| **Gemma 4 31B** | **80.7%** | **86.7%** | 0.85 | **0.79** | 16.8 |
| Gemma 4 26B | 78.0% | 84.0% | 0.82 | 0.64 | 4.4 |
| Qwen 3.6 27B | 75.3% | 76.7% | 0.85 | 0.39 | 15.0 |
| Qwen 3.6 35B (MoE) | 70.7% | 76.0% | 0.79 | 0.56 | 4.6 |
| Qwen 2.5 32B | 65.3% | 68.7% | 0.69 | 0.61 | 16.6 |
| Aya Expanse 32B | 58.7% | 64.0% | 0.66 | 0.43 | 17.5 |

- All models with context; 150 posts; time as median (one run was interrupted by the computer's sleep mode, which distorts the mean).
- **gpt-oss 120B** could not be tested: at 66 GB it pushed memory to the limit; the system force-closed programs
  and the display crashed. It is unsuitable for continuous use on this hardware.

---

## 6. Decision

**Gemma 4 31B with context, codebook v8.**

- On topics the three best models are level; on **tone** Gemma 4 31B is clearly better
  (93% agreement, kappa 0.79 vs. 0.64 for Gemma 4 26B). Tone is a core variable of the framing analysis.
- Drawback: about four times slower. Therefore a **stratified sample** is classified instead of the whole corpus.

---

## 7. Main run

- **Sample:** 50 posts per channel and week (weeks with fewer posts: all), only posts with more than 80 characters.
  In total about **10,500 posts** from 36 weeks and 6 channels.
- **Weighting:** each post gets a weight = posts in its channel-week / posts drawn. Shares per channel are
  weighted so that busy weeks are not under-represented.
- **Precision:** about ±2.5 percentage points per channel, about ±6 points per channel and month.
- **Same settings as in the test** (prompt, model, parameters) – only then do the measured values apply.
- Runtime about 2 days; resumes after interruption, random order.
- All other measures (volume, reach, term density, time series) are based on the **full corpus**.

---

## 8. Final validation (phase C) – planned

- 200 new posts from the main run that were neither in a test set nor seen before.
- Manual coding **without knowing the AI's answer**, comparison only afterwards.
- **After phase C nothing will be changed.** The result will be reported as it comes out – also per channel,
  to check whether errors affect one source group more than another.

---

## 9. Limitations

- **Categories overlap.** For some posts, several classifications were defensible even in manual coding
  (e.g. a rally in support of the army: domestic politics, ideology or military?).
  Disagreements between AI and reference lie mostly in these borderline cases.
- **One coder.** The reference comes from one person (with AI pre-coding in phase A). A second independent
  coding would increase its validity.
- **Reference adjusted after seeing AI results** (phase A). The test set 2 figures are therefore rather
  optimistic; phase C is what counts.
- **Hardware** limits model size and sample size.
- **Choice regarding legal terms** (rule 8) affects how often *accusatory* occurs; it is documented openly.

---

## 10. What I learned

1. **Definitions beat model size.** The biggest gains came from clearer rules, not larger models.
2. **Small test sets deceive.** 83% on 29 posts became 70% on 150 new posts.
3. **Agreement is not truth.** When AI and human disagree, the error is not always the AI's.
4. **Every adjustment on the same test set inflates the figure.** Hence: freeze, then measure on unseen data.
5. **Hardware is part of the method.** Runtime, memory and sleep mode have to be planned for.

---

## 11. Technical implementation

| File | Purpose |
|---|---|
| `scripts/ai/ai_config.py` | all settings: models, sample, paths |
| `scripts/ai/codebook.py` | categories, definitions, rules, source descriptions, version number |
| `scripts/ai/background.txt` | background knowledge and glossary |
| `scripts/ai/ai_core.py` | builds the prompt, queries Ollama, checks the answer |
| `scripts/ai/03a_model_comparison.py` | draws test sets, compares models, Excel evaluation |
| `scripts/ai/03_ai_classify.py` | main run with stratified sample and weights |

**Settings:** `temperature 0`, `seed 42`, `num_ctx 8192`, JSON output enforced, thinking mode off,
at most 2,000 characters per post, one retry on invalid answers.
The codebook version is part of every file name – results of different versions never overwrite each other.
