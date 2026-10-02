**English** | [Deutsch](../de/04_analyse.md)

# 04 – Analysis: what the channels say, whom they name and how they name

[← back to overview](../../README.md)

This page shows the results of the analysis of the **complete corpus** – with counts and statistics in
Python. It answers five questions:

1. **What** does each source group write about clearly more than the others?
2. **Whom** do they name – and how often?
3. **How do they name** the same actors (Israel, the USA, opponents at home)?
4. **When** does this change – and which event is behind each peak?
5. **Which countries and allies** do they name – when and in which context?

The method is at the end of the page ([section 10](#10-method)). Section 7 adds the topics according to the AI
classification of a weighted sample ([03](03_ai_classification.md)) – with measured accuracy.

| | |
|---|---|
| Basis | 328,330 posts from 6 channels, 267,548 of them with text; 1 Jan – 31 Aug 2026 |
| Groups | **state**: IRNA, IRIB News, Mehr News · **IRGC-affiliated**: Tasnim News, Fars News · **reformist**: Jamaran |
| Unit | frequency **per 1,000 words** – so groups of different size can be compared |
| Notation | Persian terms with transliteration and translation: `رژیم صهیونیستی` *rezhim-e sahyunisti* ("Zionist regime") |
| Result files | numbers, terms and links, in `results/` – no post texts; the AI files contain short AI reasons ([description](../../results/README.md)) |

### Timeline

The event dates come from the project's researched background (`scripts/ai/background.txt`); the dates of the
funeral ceremonies from Al Jazeera reports.

| Date | Event |
|---|---|
| 28 Dec 2025 – mid-Jan | nationwide protests over the economic situation; internet blackout from **8 Jan** |
| 6, 17, 26 Feb | US–Iran nuclear talks in Muscat and Geneva, mediated by Oman; no agreement |
| **28 Feb** | US and Israeli strikes on Iran, **Ali Khamenei killed**; Iran attacks Israel and US bases in the Gulf states; strike on the Shajareh Tayyebeh elementary school in **Minab** (about 156 dead, about 120 of them children) |
| 1 Mar | Ali Khamenei's death officially confirmed in Iran |
| 2 Mar | Hezbollah enters the war |
| **8 Mar** | the Assembly of Experts selects **Mojtaba Khamenei** as Supreme Leader |
| 17 Mar | Ali Larijani (Secretary of the Supreme National Security Council) killed |
| **8 Apr** | US–Iran **ceasefire**, mediated by Pakistan; 11–12 Apr talks in **Islamabad** without agreement |
| 13 Apr | US naval blockade of Iranian shipping |
| 17–18 Jun | **"Islamabad Memorandum"**: 60 days of negotiations, passage through Hormuz, timetable for ending the blockade |
| **3–10 Jul** | **farewell ceremony and funeral processions for Ali Khamenei**: state ceremony 3 Jul, Tehran prayer ground (Mosalla) from 4 Jul, procession in Tehran 6 Jul, Qom 7 Jul, Najaf and Karbala 8 Jul, Mashhad 9 Jul, burial 10 Jul – clearly visible in the data, see [section 5](#5-change-over-time-what-happened-when) |
| **7–8 Jul** | attacks on commercial vessels near Hormuz, renewed US strikes – **collapse of the ceasefire** |
| 13–14 Jul | naval blockade reinstated |
| 10 Aug | Mojtaba Khamenei reshuffles the military leadership |
| 24 Aug | new US sanctions; the rial falls to a record low (about 2 million per US dollar) |

---

## Key findings

- **Three groups with different wording.** The state channels speak as **government and administration**: foreign ministry
  spokesman, ministers, provincial authorities – and the language of international law ("aggression", "condemnation",
  "UN human rights"). The IRGC-affiliated channels report on **missiles, drones, arrests and "riots"** and mobilise
  ("oath of allegiance", "blood revenge"). Jamaran reports on **negotiations, US politics, the nuclear issue and the
  internet** – and quotes international media and reformist politicians.
- **Israel is called the "Zionist regime" more and more often** – in state and IRGC-affiliated channels in 57% and 53%
  of mentions after the collapse of the ceasefire (before: 42–48% and 35–40%). At Jamaran it is 26%; "Israel" is its most frequent designation over the whole period (65%).
- **Jamaran names Trump most often and most often writes "Trump claims"** (8.2% of all words directly after "Trump",
  3% in the other groups). IRGC-affiliated channels more often call him "criminal" and "gambler".
- **No channel calls Mojtaba Khamenei the Leader before his selection on 8 March.** Nevertheless, of the
  posts that name one of the two Khameneis, **74%** in the ceasefire and **79%** after the collapse concern the killed
  Ali Khamenei (war: 55%).
- **Persons:** President Pezeshkian is named much less often during the war (IRGC-affiliated: from 0.60 to 0.17
  per 1,000 words). Speaker of Parliament **Ghalibaf** gains weight during the ceasefire. Former presidents and
  ministers of the reformist camp – **Khatami, Rouhani, Zarif** – appear much more often at Jamaran (Khatami 0.12 per 1,000 words against 0.01 and 0.02).
- **The largest peaks are not at the start of the war** but at the beginning of July: in the weeks of the
  farewell ceremony for Ali Khamenei, "martyr" and "revenge" reach their highest values – IRGC-affiliated 21.6 times
  "martyr" per 1,000 words, about ten times the level of a typical week (median 2.1).
- **Most peaks can be linked to an event:** "negotiations" rises in the weeks of Muscat (6 Feb), Islamabad (8–12 Apr) and the
  Memorandum (17–18 Jun); opponent labels in the weeks of the protests and the internet blackout in January. One exception: the crime terms of
  the IRGC-affiliated channels peak in the week from 20 Jul with no single event recognisable.
- **Countries:** with the start of the war the focus shifts to the region – Russia and China fall to a third in the
  IRGC-affiliated channels, Gaza to between a fifth and a third in all groups. Bahrain and Kuwait, hardly named before,
  become scenes of action. Every phase has its country: Lebanon and Pakistan in the ceasefire, Saudi Arabia, Yemen and
  Iraq afterwards.
- **One country, three pictures:** for the state media the UAE are a currency hub, for the IRGC-affiliated channels a
  target (port of Fujairah), for Jamaran an actor of US politics. Saudi Arabia is a partner in talks for the state
  media and the opponent in Yemen for the IRGC-affiliated channels.
- **Topics according to the AI:** during the war 36–45% of posts are military (before: 4–5%). Jamaran has the highest
  share of diplomacy in every phase. AI accuracy on topic: 72.5%; the AI does not measure tone reliably enough for
  comparisons between groups.
- **Reach:** the IRGC-affiliated channels (Tasnim, Fars) reach a median of **11,858 views per post**, the state channels
  1,259 and Jamaran 1,593.

---

## 1. What each group writes about

Which terms does a group use **clearly more often** than the two others? Measured with the weighted log-odds ratio; a
term only counts if **every** channel of the group uses it more often (method: [section 10](#10-method)). The strength of
the difference is the z-score – from 2 it is statistically clear, above 10 very strong. The tables below sort the 200
most typical terms of each group by theme; full lists in `results/words/typical_terms.xlsx`.

### State channels – the voice of government and administration

The top of the ranking consists of everyday administrative words: provinces, month names, weekdays. This is because
the three state channels publish service news every day. Below that lies the political voice – weaker (z 3–9), but
clear in all three channels:

| Theme | typical terms | z |
|---|---|---|
| Government spokespeople and diplomacy | `بقائی` *Baghaei* (Esmail Baghaei, foreign ministry spokesman) · `وزیر امور خارجه` *vazir-e omur-e kharejeh* (foreign minister) · `غریب‌آبادی` *Gharibabadi* (Kazem Gharibabadi, deputy foreign minister) · `مهاجرانی` *Mohajerani* (Fatemeh Mohajerani, government spokeswoman) · `مجلس شورای اسلامی` *majles* (parliament) | 3–9 |
| Language of international law | `تجاوز` *tajavoz* (aggression) · `محکوم` / `محکومیت` *mahkum* (condemned / condemnation) · `نقض` *naqz* (violation) · `سازمان ملل` *sazman-e melal* (United Nations) · `حقوق بشر سازمان ملل` *hoquq-e bashar* (UN human rights council) · `جنایت` *jenayat* (crime) · `جنگ تحمیلی` *jang-e tahmili* ("imposed war") | 3–6 |
| Judiciary | `محسنی اژه‌ای` *Mohseni-Ejei* (Gholam-Hossein Mohseni-Ejei, head of the judiciary) | 3.5 |
| Military statements | `بسم الله قاصم الجبارین` *besmellah qasem al-jabbarin* ("in the name of God, the breaker of tyrants" – heading of military statements) · `قاتلوهم` *qatiluhum* ("fight them", Quran verse) | 3–5 |
| Education | `دانش آموزان` *daneshamuzan* (pupils) · `سازمان سنجش آموزش کشور` (national examination authority) · `آزمون` (exam) · `رشته` (field of study) · `کلاس درس` (classroom) | 3–6 |
| Administration and services | `استان` *ostan* (province) · `مدیرکل` *modir-kol* (director general) · `راهداری` (road authority) · `سازمان هواشناسی` (weather service) · `زلزله` (earthquake) · `جمعیت هلال احمر` (Red Crescent) | 3–11 |
| Calendar | month names `اردیبهشت` *ordibehesht*, `خرداد` *khordad*, `تیر` *tir*, `مرداد` *mordad*, `شهریور` *shahrivar* · weekdays | 4–11 |
| Culture, sport, religion | `جشنواره فیلم فجر` (Fajr film festival) · taekwondo, wrestling · `اربعین` *arbain* (pilgrimage to Karbala) | 4–5 |

**The three state channels differ** (each channel compared with the five others): IRNA writes about government,
economy and culture (`دولت چهاردهم` "14th government" = Pezeshkian's government, gold, tourism, theatre). IRIB News
warns during the war (`آژیرها` sirens, `هشدار نارنجی` "orange alert", `پناهگاه بروند` "go to the shelters") and reports
on `تجمعات شبانه` (nightly pro-government rallies). Mehr News is the channel of mourning and mobilisation: `سوگ`
(mourning), `مراسم تشییع پیکر` (funeral procession), `رهبر شهید` (the martyred Leader), `میناب` (Minab), `جنگ رمضان`
*jang-e ramazan* ("Ramadan war" – the war began during Ramadan).

### IRGC-affiliated channels – war, security and mobilisation

| Theme | typical terms | z |
|---|---|---|
| Weapons and attacks | `پهپاد` *pahpad* (drone) · `موشک` *mushak* (missile) · `پهپاد انتحاری` (kamikaze drone) · `هدف قرار` (targeted) · `اصابت` (impact) · `انهدام` (destruction) | 7–15 |
| Targets in Israel and the Gulf | `حیفا` (Haifa) · `الجلیل` (Galilee) · `کریات شمونه` (Kiryat Shmona) · `فلسطین اشغالی` *felestin-e eshghali* ("occupied Palestine" = Israel) · `فجیره` (Fujairah, UAE) · `اربیل` (Erbil, Iraq) · Saudi Arabia, UAE, Kuwait, Bahrain | 5–11 |
| Allies | `حزب‌الله` *Hezbollah* – the most typical term of the group (z 20.8) · `یمن` (Yemen) · `النبطیه` (Nabatieh, southern Lebanon) | 5–21 |
| Protests as "riots" | `اغتشاشات` *eghteshashat* ("riots") · `اغتشاشگران` ("rioters") · `آشوبگران` ("agitators") · `ضدانقلاب` ("counter-revolution") · `منافقین` ("hypocrites" = People's Mojahedin) · `کشته‌سازی` *koshteh-sazi* ("staged deaths") | 6–14 |
| Security and arrests | `دستگیر` (arrested) · `بازداشت` (detention) · `کشف` (discovered) · `عناصر` ("elements") · `تروریست` (terrorist) · `سازمان اطلاعات سپاه` (IRGC intelligence organisation) | 5–12 |
| Opposition abroad | `اینترنشنال` (Iran International, Persian-language broadcaster abroad) · `رضا پهلوی` *Reza Pahlavi* (son of the last Shah) | 11–12 |
| Mobilisation and religion | `بیعت` *bey'at* (oath of allegiance – above all during the war, after the selection of the new Leader) · `خونخواهی` *khunkhahi* (blood revenge) · `انتقام` *enteqam* (revenge) · `لبیک` ("at your service") · `مداحی` (religious lament singing) · `حرم حضرت معصومه` (shrine in Qom) · `خیابان`, `تجمع` (street, rally) | 5–13 |
| Killed commanders | `شهید پاکپور` (Mohammad Pakpour, IRGC commander, killed 28 Feb) · `شهید سلامی` (Hossein Salami, killed 2025) · `غلامرضا سلیمانی` (Basij commander, killed 17 Mar) · `شهید رئیسی` (Ebrahim Raisi, president, died in a crash in 2024) | 5–7 |
| Football | `پرسپولیس` (Persepolis) · `استقلال` (Esteghlal) · `تراکتور` (Tractor) | 6–9 |

Tasnim is marked by funerals (`بدرقه` send-off, `شهید` martyr) and Lebanon; Fars by missile impacts, the judiciary and
banks.

### Jamaran – diplomacy, the nuclear issue and the reformist camp

| Theme | typical terms | z |
|---|---|---|
| USA and negotiations | `ترامپ` *Trump* – the most typical term (z 44.6) · `ایالات متحده` (United States) · `مذاکرات` (negotiations) · `توافق` (agreement) · `ونس` (JD Vance) · `روبیو` (Marco Rubio) · `ویتکاف` (Steve Witkoff) · `کوشنر` (Jared Kushner) · `برجام` (2015 nuclear deal) | 9–45 |
| Nuclear issue | `هسته‌ای` (nuclear) · `غنی‌سازی` (enrichment) · `اورانیوم` (uranium) · `گروسی` (Rafael Grossi, head of the IAEA) | 10–23 |
| Distance from statements | `مدعی` *moddai* ("claims") · `ادعای` ("claim") · `احتمالا` (probably) · `بعید` (unlikely) · `ظاهرا` (apparently) | 8–33 |
| International media | `آکسیوس` (Axios) · CNN · Fox News · New York Times · Wall Street Journal · Bloomberg · Reuters · Al Jazeera · RIA Novosti | 9–22 |
| Reformist camp | `سید حسن خمینی` (Hassan Khomeini, grandson of the founder of the revolution) · `خاتمی` (Mohammad Khatami, president 1997–2005) · `ظریف` (Mohammad Javad Zarif, foreign minister 2013–2021) · `حسن روحانی` (Hassan Rouhani, president 2013–2021) · `ابطحی` (Mohammad-Ali Abtahi, vice president under Khatami) · `زیدآبادی` (Ahmad Zeidabadi, journalist) · `عارف` (Mohammad Reza Aref, first vice president) · `اصلاحات` (reforms) | 10–28 |
| Opponents at home | `کیهان` (Kayhan, conservative newspaper) · `شریعتمداری` (Hossein Shariatmadari, editor of Kayhan) · `نبویان` (Mahmoud Nabavian, member of parliament) · `اصولگرا` (principlists) · `تندروها` (hardliners) | 9–15 |
| Internet and society | `اینترنت` (internet, z 39.1) · `فیلترینگ` (blocking) · `فیلترشکن` (VPN) · `اینترنت پرو` ("Internet Pro" – separate internet access) · `حجاب` (headscarf) · `طبقاتی` (class-based) | 9–39 |
| Obituaries | `مرحوم` (the late) · `درگذشت` (passed away) · `تسلیت` (condolences) | 9–13 |

---

## 2. Whom the channels name

Mentions per 1,000 words, whole period. Name and name variants are counted (`naming_terms.csv`, e.g. for Ghalibaf the
spellings `قالیباف`, `قالی‌باف` and `قالی باف`; the full name `محمدباقر قالیباف` *Mohammad-Bagher Ghalibaf* is counted
via the surname).

| Persian | Person | Role | state | IRGC-affiliated | Jamaran |
|---|---|---|---|---|---|
| `ترامپ` | Donald Trump | President of the USA | 1.86 | 2.06 | **3.11** |
| `نتانیاهو` | Benjamin Netanyahu | Prime Minister of Israel | 0.31 | 0.38 | **0.50** |
| `پزشکیان` | Masoud Pezeshkian | President of Iran (since 2024) | 0.42 | 0.35 | **0.56** |
| `عراقچی` | Abbas Araghchi | Foreign Minister (since 2024) | **0.48** | 0.43 | 0.46 |
| `بقائی` | Esmail Baghaei | foreign ministry spokesman | **0.28** | 0.14 | 0.13 |
| `قالیباف` | Mohammad Bagher Ghalibaf | Speaker of Parliament (since 2020); formerly commander of the IRGC Air Force, police chief and mayor of Tehran | 0.23 | **0.32** | 0.27 |
| `ظریف` | Mohammad Javad Zarif | Foreign Minister 2013–2021 | 0.01 | 0.01 | **0.06** |
| `خاتمی` | Mohammad Khatami | President 1997–2005, reformist camp | 0.01 | 0.02 | **0.12** |
| `حسن روحانی` | Hassan Rouhani | President 2013–2021 | 0.00 | 0.00 | **0.03** |
| `احمدی‌نژاد` | Mahmoud Ahmadinejad | President 2005–2013 | 0.00 | 0.00 | **0.02** |

In absolute numbers: Khatami 366 times at Jamaran compared with 122 times in all three state channels and 87 times in both IRGC-affiliated channels;
Rouhani 78 compared with 30 (state) and 16 (IRGC-affiliated). Rouhani is only counted with his full name, because `روحانی` alone also means
"cleric".

**Who matters when** (per 1,000 words by phase, `naming.xlsx`, sheet `persons_phases`):

| | before the war | war | ceasefire | after the collapse |
|---|---|---|---|---|
| Pezeshkian, IRGC-affiliated | 0.60 | **0.17** | 0.37 | 0.37 |
| Pezeshkian, state | 0.55 | **0.26** | 0.39 | 0.50 |
| Araghchi, all three groups | **0.68–0.76** | 0.36–0.48 | 0.41–0.47 | 0.30–0.38 |
| Ghalibaf, IRGC-affiliated | 0.20 | 0.23 | **0.43** | 0.28 |
| Ghalibaf, Jamaran | 0.10 | 0.15 | **0.39** | 0.32 |
| Khatami, Jamaran | 0.08 | 0.03 | 0.13 | **0.22** |

- The **president** recedes into the background during the war – most strongly in the IRGC-affiliated channels.
- The **foreign minister** is most present before the war, at the time of the nuclear talks.
- **Ghalibaf** is named two to four times as often during the ceasefire as before the war.

### Ghalibaf over time

![Ghalibaf per 1,000 words](../../results/timeline/charts/ghalibaf.png)

The peaks fall on three events. The right column lists the terms that were most typical of the week as a whole
(`11_peak_weeks.py`, see [section 5](#5-change-over-time-what-happened-when)):

| Week from | highest value | typical terms of this week | Event |
|---|---|---|---|
| 13 Apr | IRGC-affiliated 0.95 | `آتش‌بس` *atash-bas* (ceasefire) · `محاصره دریایی` *mohasereh-ye darya'i* (naval blockade) · `مذاکرات` *mozakerat* (negotiations) · `تنگه هرمز` (Strait of Hormuz) | talks in Islamabad (11–12 Apr), US naval blockade (13 Apr) |
| 29 Jun | Jamaran 1.04 · state 0.56 | `مراسم وداع` *marasem-e veda'* (farewell ceremony) · `رهبر شهید` *rahbar-e shahid* (the martyred Leader) · `مصلی تهران` *mosalla* (Tehran prayer ground) · `ادای احترام` (paying respects) | farewell ceremony for Ali Khamenei |
| 17 Aug | Jamaran 0.87 · IRGC-affiliated 0.82 · state 0.65 | `چهلم` *chehelom* (40th-day memorial) · `تدفین` *tadfin* (burial) · `اقتصادی` (economic) · `بنزین` *benzin* (petrol) · `نفوذ` *nofuz* ("infiltration") · `مصدق` *Mosaddegh* (anniversary of the coup of 19 Aug 1953) | memorial ceremonies for Ali Khamenei; debates on the economy and petrol |

Ghalibaf is named often in three very different contexts: the negotiations, the mourning for the Leader and economic
policy afterwards. The terms show the context of the week, not every single statement about him; the exact content is
shown by `04_context.py قالیباف`.

### Which words stand next to Trump

| Word directly after "Trump" | state | IRGC-affiliated | Jamaran |
|---|---|---|---|
| `مدعی` *moddai* ("claims") | 2.8% | 3.0% | **8.2%** |
| `جنایتکار` *jenayatkar* ("criminal") | 0.5% | **1.4%** | – |
| `قمارباز` *qomarbaz* ("gambler") | – | **0.6%** | – |

Share of all words directly after "Trump"; "–" = not among the 20 most frequent. Before "Trump", all groups most often
write `دونالد` (Donald), then `دولت` (administration) and `ادعای` ("the claim of") – 5.2% at Jamaran, 3.2–3.3% in the
others. Before "Netanyahu", the most frequent word is `بنیامین` (Benjamin; 25–40%); `توهمات` (*tavahhomat*, "delusions") is among the
20 most frequent words before him in all groups (0.5–1.1%). Full lists:
`results/naming/neighbours.csv`.

---

## 3. How the channels name

### Israel

Share of all names for Israel:

| | state | IRGC-affiliated | Jamaran |
|---|---|---|---|
| `رژیم صهیونیستی` *rezhim-e sahyunisti* ("Zionist regime"), whole period | 48% | 40% | 29% |
| – before the war (until 27 Feb) | 46% | 40% | 28% |
| – war (28 Feb – 7 Apr) | 42% | 35% | 31% |
| – ceasefire (8 Apr – 6 Jul) | 48% | 40% | 29% |
| – after the collapse (from 7 Jul) | **57%** | **53%** | 26% |
| `اسرائیل` *Esra'il* ("Israel"), whole period | 45% | 50% | **65%** |
| `صهیونیست‌ها` *sahyunist-ha* ("the Zionists") | 4% | **6%** | 3% |

- After the collapse of the ceasefire (from 7 July), state and IRGC-affiliated channels use "Zionist regime" clearly more often; Jamaran does not.
- For Israeli territory, IRGC-affiliated channels more often write `فلسطین اشغالی` *felestin-e eshghali*
  ("occupied Palestine", 10% compared with 3% at Jamaran).

![Share of "Zionist regime"](../../results/timeline/charts/israel_zionist_regime_share.png)

### USA

- `آمریکا` *Amrika* ("America") is the main name everywhere (76–84%).
- Jamaran more often uses the formal name `ایالات متحده` *Eyalat-e Mottahedeh* ("United States"): 11% compared with
  7% (state) and 5% (IRGC-affiliated).
- Pejorative names such as `ارتش تروریستی آمریکا` ("terrorist army of America") and `ارتش کودک‌کش آمریکا`
  ("child-killing army of America") increase clearly after the collapse of the ceasefire: together 3–5% of all names
  for the USA, 1–2% during the war, 0% before the war.
- `رئیس دولت تروریستی آمریکا` ("head of the terrorist government of America" – for Trump) is used above all by Tasnim.

### Revenge, opponents, crimes, diplomacy

Per 1,000 words, whole period:

| Group of terms | Examples | state | IRGC-affiliated | Jamaran |
|---|---|---|---|---|
| Diplomacy | `مذاکره` *mozakereh* (negotiation) · `توافق` *tavafoq* (agreement) · `آتش‌بس` *atash-bas* (ceasefire) · `صلح` *solh* (peace) | 3.88 | 3.04 | **5.39** |
| Crimes | `جنایت` *jenayat* (crime) · `نسل‌کشی` *nasl-koshi* (genocide) · `کودک‌کش` *kudak-kosh* (child-killer) · `میناب` (Minab) | **1.03** | 0.90 | 0.75 |
| Opponents at home | `مزدور` *mozdur* (mercenary) · `خائن` *kha'en* (traitor) · `اغتشاشگر` *eghteshashgar* (rioter) · `وطن‌فروش` *vatan-forush* (traitor to the homeland) · `ضدانقلاب` (counter-revolution) | 0.25 | **0.48** | 0.22 |
| Revenge | `انتقام` *enteqam* (revenge) · `خونخواهی` *khunkhahi* (blood revenge) · `قصاص` *qesas* (retribution) · `انتقام سخت` ("harsh revenge") | 0.20 | **0.32** | 0.12 |

- About a third of the crime terms concern the strike on the school in **Minab** (32–37%).
- At Jamaran, "blood revenge" is rare (16% of the revenge terms compared with 34–35%).

---

## 4. Which Khamenei is meant?

`خامنه‌ای` *Khamenei* and `رهبر` *rahbar* ("the Leader") can mean Ali Khamenei (killed on 28 Feb) or his son and
successor Mojtaba Khamenei. Every mention was assigned with rules and checked with samples (method:
[section 10](#10-method)).

- All six channels write `رهبر شهید` *rahbar-e shahid* ("the martyred Leader") for the first time on **1 March** – the
  day the death was officially confirmed.
- All six channels mention Mojtaba Khamenei in one sentence with "Leader" for the first time on **8 March** – the day
  of his selection, **no channel earlier**. Jamaran and Mehr name him from 3 March, Tasnim from 5 March – not yet as
  the Leader.
- Afterwards, the killed Leader stays more present than the new one:

| Phase | Ali Khamenei | Mojtaba Khamenei | both |
|---|---|---|---|
| war (28 Feb – 7 Apr) | 55% | 35% | 10% |
| ceasefire | 74% | 22% | 4% |
| after the collapse of the ceasefire | 79% | 17% | 3% |

22,897 posts, all six channels; per channel in `results/leader/leader_mentions.xlsx`. During the war, Fars (45%) and
IRIB News (42%) report most on Mojtaba.

---

## 5. Change over time: what happened when

The charts show the terms per **calendar week** (every point = one week, not a running total). Vertical lines: start of
the war (28 Feb), new Leader (8 Mar), ceasefire (8 Apr), collapse of the ceasefire (8 Jul). The first and the last
week are incomplete and are left out of the charts.

**Why is there a peak?** `11_peak_weeks.py` compares every peak week with all other weeks of the same group and lists
the terms that were typical of **exactly this week** (same method as section 1). So a peak can usually be linked to an
event with the data itself (one exception: crime terms, IRGC-affiliated, week from 20 Jul). The terms describe the whole week, not only the posts with the counted word. All weeks and
terms: `results/timeline/peak_weeks.csv`.

### Negotiations

![Negotiations](../../results/timeline/charts/negotiations.png)

| Week from | peak (per 1,000 words) | typical terms of this week | Event |
|---|---|---|---|
| 2 Feb | Jamaran 6.2 · state 3.7 · IRGC-affiliated 3.5 | `مسقط` *Masqat* (Muscat) · `عراقچی` (Abbas Araghchi) · `ویتکاف` (Steve Witkoff) | nuclear talks in Muscat (6 Feb) |
| 6 Apr | Jamaran 4.4 · IRGC-affiliated 3.5 · state 3.0 | `آتش‌بس` (ceasefire) · `اسلام‌آباد` (Islamabad) · `پاکستان` (Pakistan) · `لبنان` (Lebanon) · `چهلمین روز شهادت` (40th day after Ali Khamenei's death) · `خرازی` (Kamal Kharazi, former foreign minister, died 9 Apr) | ceasefire (8 Apr), talks in Islamabad (11–12 Apr) |
| 15 Jun | Jamaran 4.1 · IRGC-affiliated 2.9 | `تفاهم‌نامه` *tafahom-nameh* (memorandum) · `امضای` (signing) · `محرم` (month of Muharram) | "Islamabad Memorandum" (17–18 Jun) |

Jamaran writes most about negotiations in each of these weeks. After the collapse of the ceasefire, Jamaran's value
stays more than twice as high as in the other groups (1.39 compared with 0.58 and 0.60).

### Ceasefire and Trump

| Week from | typical terms of this week | Event |
|---|---|---|
| 6 Apr | ceasefire · Islamabad · Pakistan | the ceasefire takes effect (8 Apr) |
| 13 Apr | `محاصره دریایی` (naval blockade) · `تنگه هرمز` (Strait of Hormuz) · `پاپ لئو` (Pope Leo) · `ترامپ` (Trump) | US naval blockade (13 Apr) – the highest value for "Trump" in all groups (Jamaran 4.5, IRGC-affiliated 4.0, state 3.4) |
| 20 Apr | `تمدید` *tamdid* (extension) · ceasefire · naval blockade | Trump extends the ceasefire (21 Apr) |

![Ceasefire](../../results/timeline/charts/ceasefire.png)

![Trump](../../results/timeline/charts/trump.png)

Jamaran names Trump most often in almost every week. For state and IRGC-affiliated channels the low point is the
week from 29 Jun – the week of the farewell ceremony for Ali Khamenei (3–5 Jul); for Jamaran one week earlier.

### Martyr and revenge – the farewell ceremony for Ali Khamenei

![Martyr](../../results/timeline/charts/martyr.png)

![Revenge](../../results/timeline/charts/revenge.png)

| Week from | peak | typical terms of this week | Event |
|---|---|---|---|
| 2 Mar | revenge: IRGC-affiliated 0.89 | `موشک‌های` (missiles) · `خامنه‌ای` (Khamenei) · `سوگ` *sug* (mourning) · `مجلس خبرگان` (Assembly of Experts) · `عملیات وعده صادق` ("Operation True Promise") | killing of Ali Khamenei (28 Feb), selection of his successor |
| 29 Jun | martyr: IRGC-affiliated 19.1 · state 14.1 · Jamaran 7.6 | `مراسم وداع` *marasem-e veda'* (farewell ceremony) · `مصلی تهران` *mosalla-ye Tehran* (Tehran prayer ground) · `ادای احترام` (paying respects) · `بدرقه` *badragheh* (send-off) | farewell ceremony for Ali Khamenei in Tehran |
| 6 Jul | martyr: IRGC-affiliated **21.6** · state 17.5 · revenge: IRGC-affiliated **1.48** · state 0.84 · Jamaran 0.54 | `تشییع` *tashyi'* (funeral procession) · `پیکر مطهر` (the holy body) · `مشهد` (Mashhad) · `نجف` (Najaf) | funeral processions in Mashhad and Najaf |
| 13 Jul (second peak) | revenge: state 0.58 · Jamaran 0.41 | `بندرعباس` (Bandar Abbas) · `هرمزگان` (Hormozgan province) · `بوشهر` (Bushehr) · `اهواز` (Ahvaz) · `انفجار` (explosion) · `کویت` (Kuwait) · `اردن` (Jordan) | attacks after the collapse of the ceasefire (7–8 Jul) |

- The **highest values** for "martyr" and "revenge" in the whole period are **not** at the start of the war, but in
  the weeks of the farewell ceremony (3–5 Jul) and the funeral processions (6–9 Jul) for Ali Khamenei – four months
  after his death.
- In the week from 29 Jun (farewell ceremony) Jamaran writes "Zionist regime" in 44% of cases – the channel's highest
  value in the whole period (second highest: 39%, week from 20 Apr).

### Opponent labels and internet – the protests in January

![Opponents](../../results/timeline/charts/labels_opponents.png)

| Week from | peak | typical terms of this week | Event |
|---|---|---|---|
| 5 Jan | opponent labels: IRGC-affiliated **3.34** | `اغتشاشگران` (rioters) · `اعتراض` (protest) · `کالابرگ` *kalabarg* (food coupon) · `ارز` *arz* (foreign currency) · `روغن` (cooking oil) · `ونزوئلا` (Venezuela) · `مادورو` (Maduro) | protests over prices and the fall of the rial |
| 12 Jan | opponent labels: state 2.17 · internet: IRGC-affiliated 0.66 | `اغتشاشات` (riots) · `تروریست‌ها` (terrorists) · `مسلح` (armed) · `آشوبگران` (agitators) · `فتنه` *fetneh* ("sedition") · `پهلوی` (Pahlavi) · `موساد` (Mossad) | internet blackout from 8 Jan; the protests are presented as terrorism and as directed from abroad |

![Internet](../../results/timeline/charts/internet.png)

| Week from | peak | typical terms of this week | Event |
|---|---|---|---|
| 12 Jan | IRGC-affiliated 0.66 · state 0.49 | riots, terrorists (see above) | internet blackout from 8 Jan |
| 11 May | Jamaran 1.74 · state 0.56 | `اینترنت پرو` ("Internet Pro") · `چین` (China) · `شی جین‌پینگ` (Xi Jinping) · `بریکس` (BRICS) · `دهلی‌نو` (New Delhi) | debate on "Internet Pro"; foreign policy with China and BRICS |
| 25 May | Jamaran **1.76** | `اتصال` *ettesal* (connection) · `بازگشایی` (reopening) · `فضای مجازی` (internet, literally "virtual space") · `خاتمی` (Mohammad Khatami) | debate on reopening the internet |

Jamaran is the only channel that makes the internet a topic for months – from April to early June more than five
times as often as the other groups (1.04 compared with 0.17 and 0.20 per 1,000 words). State and IRGC-affiliated
channels mention the internet above all in January, in connection with the "riots".

### Crimes

![Crimes](../../results/timeline/charts/crimes.png)

| Week from | peak | typical terms of this week | Event |
|---|---|---|---|
| 2 Mar | state **2.08** · Jamaran 1.56 · IRGC-affiliated 1.60 (second peak) | `حمله` (attack) · `اصابت` (impact) · `تجاوز` (aggression) · `سرزمین‌های اشغالی` ("occupied territories") · `سوگ` (mourning) | first week of the war, strike on the school in Minab (28 Feb) |
| 6 Apr | state 1.90 · Jamaran 1.44 | ceasefire · Islamabad · 40th day after Ali Khamenei's death | ceasefire; review of the first weeks of the war |
| 20 Jul | IRGC-affiliated **1.79** | `اربعین` (Arbaeen) · `زائران` (pilgrims) · `عربستان` (Saudi Arabia) · `یمن` (Yemen) · `کویت` (Kuwait) · `اردن` (Jordan) | no single event visible; in this week the Houthis declared a maritime blockade on Saudi Arabia (20–22 Jul) |

### Naming the USA

!["United States"](../../results/timeline/charts/usa_united_states_share.png)

The formal name `ایالات متحده` ("United States") rises when diplomacy or foreign countries are in the news: in the week
from 5 Jan at Jamaran to 17% (typical: `ونزوئلا` Venezuela, `مادورو` Maduro), in the week from 16 Feb in
IRGC-affiliated channels to 10% (`ژنو` Geneva – nuclear talks on 17 Feb), in the week from 15 Jun at Jamaran and in
IRGC-affiliated channels to 15% and 10% (Memorandum). In IRGC-affiliated channels it falls during the war from 8% to 5%.

---

## 6. Countries and allies

Which countries and groups do the channels name – how often, when and in which context? Counted with the same rules as
in section 3 (`12_countries.py`, list in `naming_terms.csv`). About a quarter of all posts with text (67,669) name at
least one country or group on the list. This section shows the 33 with the most mentions (all 35: `results/countries/countries.xlsx`), in four regions.

### Who is named most often

Per 1,000 words, whole period; bold = highest value. Full list: `results/countries/countries.xlsx`.

| Country / group | state | IRGC-affiliated | Jamaran | mentions in total |
|---|---|---|---|---|
| `لبنان` *Lobnan* – Lebanon | 1.22 | **1.49** | 1.05 | 20,759 |
| `عراق` *Eraq* – Iraq | 0.72 | **0.75** | 0.62 | 11,655 |
| `روسیه` *Rusiyeh* – Russia | 0.63 | 0.54 | **0.70** | 10,056 |
| `حزب‌الله` *Hezbollah* – Hezbollah | 0.45 | **0.85** | 0.44 | 9,271 |
| `پاکستان` *Pakestan* – Pakistan | 0.52 | 0.42 | **0.58** | 8,266 |
| `عربستان` *Arabestan* – Saudi Arabia | 0.40 | **0.57** | 0.49 | 7,609 |
| `چین` *Chin* – China | 0.38 | 0.37 | **0.51** | 6,541 |
| `اتحادیه اروپا` *Ettehadiyeh-ye Orupa* – EU / Europe | **0.40** | 0.26 | 0.35 | 5,751 |
| `غزه` *Ghazzeh* – Gaza | **0.37** | 0.35 | 0.23 | 5,477 |
| `امارات` *Emarat* – UAE | 0.23 | **0.40** | 0.39 | 5,079 |
| `انگلیس` *Engelis* – United Kingdom | **0.31** | 0.26 | 0.26 | 4,741 |
| `یمن` *Yaman* – Yemen | 0.26 | **0.37** | 0.19 | 4,519 |
| `ترکیه` *Torkiyeh* – Turkey | 0.27 | 0.23 | **0.28** | 4,305 |
| `عمان` *Oman* – Oman | 0.25 | 0.24 | **0.34** | 4,302 |
| `قطر` *Qatar* – Qatar | 0.23 | 0.26 | **0.30** | 4,126 |
| `کویت` *Kuweyt* – Kuwait | 0.19 | **0.31** | 0.24 | 3,858 |
| `اوکراین` *Ukrayn* – Ukraine | **0.24** | 0.22 | 0.21 | 3,704 |
| `فلسطین` *Felestin* – Palestine | **0.25** | 0.20 | 0.13 | 3,493 |
| `بحرین` *Bahreyn* – Bahrain | 0.18 | **0.28** | 0.17 | 3,392 |
| `فرانسه` *Faranseh* – France | **0.22** | 0.18 | 0.20 | 3,367 |
| `ونزوئلا` *Venezuela* – Venezuela | 0.18 | 0.15 | **0.23** | 2,986 |
| `سوریه` *Suriyeh* – Syria | **0.18** | 0.17 | 0.16 | 2,833 |
| `هند` *Hend* – India | 0.16 | 0.15 | **0.17** | 2,543 |
| `اردن` *Ordon* – Jordan | 0.13 | **0.17** | 0.13 | 2,319 |
| `آلمان` *Alman* – Germany | **0.15** | 0.12 | 0.13 | 2,267 |
| `اسپانیا` *Espaniya* – Spain | **0.13** | 0.11 | 0.09 | 1,921 |
| `حماس` *Hamas* – Hamas | **0.13** | 0.07 | 0.07 | 1,648 |
| `ژاپن` *Zhapon* – Japan | **0.10** | 0.09 | 0.08 | 1,536 |
| `جمهوری آذربایجان` – Republic of Azerbaijan¹ | **0.11** | 0.08 | 0.07 | 1,520 |
| `انصارالله` *Ansarollah* / `حوثی‌ها` *Huthi-ha* – Houthis | 0.07 | **0.09** | 0.07 | 1,289 |
| `ایتالیا` *Italiya* – Italy | **0.08** | 0.06 | 0.07 | 1,152 |
| `افغانستان` *Afghanestan* – Afghanistan | 0.07 | 0.05 | **0.08** | 1,037 |
| `حشد شعبی` *Hashd-e Sha'bi* / `مقاومت عراق` – Iraqi militias | 0.04 | **0.08** | 0.03 | 799 |

¹ Too high: `آذربایجان` alone sometimes means the Iranian provinces (see [limitations](#9-limitations)).

- **IRGC-affiliated channels** name **Hezbollah almost twice as often** as the others. They also name Saudi Arabia,
  the UAE, Kuwait, Bahrain, Jordan, Yemen and the Iraqi militias most often – the places from which they report
  attacks.
- **Jamaran** names the **great powers and mediators** most often: Russia, China, Pakistan, Oman, Qatar. Jamaran names
  Palestine, Gaza and Hamas least often.
- **State channels** name Europe, the United Kingdom, France, Germany, Palestine and Hamas most often.

### In the war the world shrinks

Per 1,000 words by phase; a range means: lowest to highest value of the three groups. All values: `countries.xlsx`,
sheet `phases`.

| | before the war | war | ceasefire | after the collapse |
|---|---|---|---|---|
| Russia, IRGC-affiliated | 0.71 | **0.24** | 0.61 | 0.62 |
| China, IRGC-affiliated | 0.39 | **0.13** | 0.53 | 0.32 |
| EU / Europe, IRGC-affiliated | 0.50 | **0.18** | 0.29 | 0.16 |
| Gaza, all groups | 0.37–0.45 | **0.08–0.12** | 0.20–0.41 | 0.28–0.47 |
| Venezuela, all groups | 0.66–1.06 | **0.02–0.04** | 0.08 | 0.08–0.10 |
| Bahrain, all groups | **0.02** | 0.33–0.46 | 0.11–0.17 | 0.21–0.43 |
| Kuwait, all groups | **0.01–0.04** | 0.33–0.47 | 0.11–0.17 | 0.32–0.59 |
| UAE, IRGC-affiliated | 0.18 | **0.56** | 0.46 | 0.27 |
| Hezbollah, all groups | 0.14–0.18 | **0.65–1.24** | 0.59–1.20 | 0.16–0.22 |
| Lebanon, all groups | 0.36–0.52 | 0.61–0.88 | **1.86–2.45** | 0.59–0.98 |
| Pakistan, all groups | 0.21–0.31 | 0.16–0.26 | **0.72–0.92** | 0.30–0.50 |
| Saudi Arabia, IRGC-affiliated | 0.30 | 0.44 | 0.30 | **1.35** |
| Yemen, IRGC-affiliated | 0.18 | 0.21 | 0.18 | **1.00** |
| Iraq, IRGC-affiliated | 0.44 | 0.66 | 0.53 | **1.45** |
| Jordan, all groups | 0.07–0.09 | 0.09–0.15 | 0.03–0.06 | **0.30–0.46** |

- **With the start of the war, distant countries fall sharply in the news** – most strongly in the
  IRGC-affiliated channels: Russia and China are named there only a third as often as before the war. At Jamaran
  Russia falls by only a quarter (0.98 → 0.72) and is named three times as often during the war as in the
  IRGC-affiliated channels.
- **Bahrain and Kuwait** are practically absent before the war. With the start of the war they become scenes of
  action: Iran attacks US bases in the Gulf states.
- **Hezbollah** enters the war on 2 March and is named three to seven times as often in the war and the ceasefire as
  before. After the collapse of the ceasefire it falls almost back to its pre-war level.
- **Every phase has its country:** **Lebanon** in the ceasefire, **Pakistan** as the mediator of the ceasefire,
  **Saudi Arabia, Yemen, Iraq and Jordan** after the collapse.

### Which Gulf state was in focus when

| Phase | named most often (range of the three groups) | context |
|---|---|---|
| before the war | Oman 0.28–0.46 · Saudi Arabia 0.30–0.32 | Oman mediates the nuclear talks in Muscat |
| war | UAE 0.36–0.56 · Kuwait 0.33–0.47 · Bahrain 0.33–0.46 | Iran attacks US bases in the Gulf |
| ceasefire | UAE 0.26–0.49 · Saudi Arabia 0.23–0.37 | attack on the port of Fujairah (UAE, week from 4 May) |
| after the collapse | Saudi Arabia 0.82–1.35 · Kuwait 0.32–0.59 · Oman 0.33–0.51 · Jordan 0.30–0.46 | Yemen and Iraq; attacks on US bases; passage through Hormuz |

### When: the peaks and what is behind them

For every country `12_countries.py` finds the two weeks with the highest value (mentions per 1,000 words, all groups
together) and compares the posts about the country **in that week** with the posts about the country in all other
weeks. The tables show the most typical terms. All values: `results/countries/peak_weeks.csv`.

#### Gulf states and Jordan

![Gulf states](../../results/countries/charts/gulf_states.png)

| Country | week from (value) | typical terms of the posts about the country in that week | event |
|---|---|---|---|
| UAE | 4 May (1.36) | `بندر فجیره` *bandar-e Fujeyreh* (port of Fujairah) · `تنگه هرمز` (Strait of Hormuz) · `کوبنده` *kubandeh* ("crushing") · `نیروهای مسلح جمهوری اسلامی ایران` (Iran's armed forces) | attack on the port of Fujairah |
| UAE | 11 May (0.99) | `نتانیاهو` (Netanyahu) · `سفر` (trip) · `مخفیانه` *makhfiyaneh* (secret) · `تکذیب` *takzib* (denial) · `براکه` (Barakah nuclear power plant) | reports of a secret visit by Netanyahu to the UAE, with a denial |
| Saudi Arabia | 27 Jul (2.10) | `عراق` (Iraq) · `حملات` (attacks) · `الحشد الشعبی` (Hashd militias) · `تجاوز` (aggression) · `محکوم` (condemned) · `اربعین` (Arbaeen) · `کربلا` (Karbala) | attacks on positions of the Iraqi militias, attributed to Saudi Arabia in these posts |
| Saudi Arabia | 3 Aug (1.71) | `مزدوران` *mozduran* ("mercenaries") · `یمن` (Yemen) · `مارب` (Marib) · `المخا` (Mocha) · `توافقنامه دفاعی` (defence agreement) · `ترکیه` (Turkey) | fighting in Yemen; defence agreement with Turkey |
| Kuwait | 13 Jul (1.14), 20 Jul (0.90) | `عملیات صاعقه` *amaliyat-e sa'eqeh* ("Operation Thunderbolt") · `عریفجان` (US base Camp Arifjan) · `آشیانه` (hangar) · `پاتریوت` (Patriot air defence) · `ارتش تروریستی آمریکا` ("terrorist army of America") | Iranian attacks on US bases after the collapse of the ceasefire |
| Bahrain | 13 Jul (0.76), 20 Jul (0.60) | `مخازن سوخت` (fuel tanks) · `شیخ عیسی` (Isa Air Base) · `عملیات صاعقه` ("Operation Thunderbolt") · `آمازون` (Amazon) | the same wave of attacks |
| Jordan | 13 Jul (0.86), 20 Jul (0.71) | `مخازن سوخت` (fuel tanks) · `عملیات صاعقه` · `جنگنده‌ها` (fighter jets) | the same wave of attacks |
| Oman | 2 Feb (0.78) | `مسقط` *Masqat* (Muscat) · `استیو ویتکاف` (Steve Witkoff, US special envoy) · `هسته‌ای` (nuclear) | nuclear talks in Muscat (6 Feb) |
| Oman | 3 Aug (0.83) | `تنگه هرمز` · `ترتیبات موقت` (interim arrangements) · `کریدور` (corridor) · `بازگشایی` (reopening) | arrangements for passage through Hormuz |
| Qatar | 22 Jun (0.50) | `کمیته فنی` (technical committee) · `نظارت` (monitoring) · `سوئیس` (Switzerland) · `چهارجانبه` (four-party) | implementation of the Islamabad Memorandum |

#### Lebanon, Palestine, Iraq, Yemen, Syria

![Lebanon, Palestine, Iraq, Yemen, Syria](../../results/countries/charts/axis_of_resistance.png)

| Country / group | week from (value) | typical terms of the posts in that week | event |
|---|---|---|---|
| Lebanon | 1 Jun (**3.82**) | `ضاحیه` *Zahiyeh* (Dahiyeh, southern Beirut) · `قلعه` (castle – Beaufort) · `متوقف` (stopped) · `تماس‌های تلفنی` (phone calls) · `عراقچی` (Araghchi) · `تشدید` (escalation) | escalation in Lebanon; phone calls of the foreign minister – highest weekly value of any country |
| Hezbollah | 1 Jun (1.39) | `قلعه` / `الشقیف` (Beaufort castle, *Qal'at al-Shaqif*) · `بیروت` (Beirut) · `نبیه بری` (Nabih Berri, Speaker of Lebanon's parliament) · `ضاحیه` | the same week |
| Lebanon | 15 Jun (3.40) | `تفاهم‌نامه` (memorandum) · `خاتمه جنگ` (end of the war) · `بندهای` (clauses) · `ونس` (JD Vance, US Vice President) | Lebanon as part of the Islamabad Memorandum |
| Hezbollah | 13 Apr (1.08) | `آتش‌بس` (ceasefire) · `پذیرش مشروط` (conditional acceptance) · `بنت‌جبیل` (Bint Jbeil) | ceasefire; fighting around Bint Jbeil |
| Iraq | 6 Jul (2.07) | `نجف` (Najaf) · `تشییع` (funeral procession) · `رهبر شهید` (the martyred Leader) | funeral procession for Ali Khamenei in Najaf |
| Iraq | 27 Jul (2.11) | `عربستان` (Saudi Arabia) · `زائران` (pilgrims) · `اربعین` · `حملات` (attacks) · `محکوم` (condemned) | attacks on the Hashd militias; Arbaeen pilgrimage |
| Yemen | 20 Jul (1.02) | `محاصره دریایی` (naval blockade) · `الحدیده` (Hodeidah) · `جیزان` (Jizan) · `نفتکش` (tanker) | Houthi naval blockade against Saudi Arabia (20–22 Jul) |
| Yemen | 3 Aug (1.20) | `مارب` (Marib) · `المخا` (Mocha) · `مزدوران` ("mercenaries") | fighting in Yemen |
| Gaza | 19 Jan (0.67), 16 Feb (0.60) | `شورای صلح` *shura-ye solh* ("Board of Peace") · `ترامپ` · `منشور` (charter) · `دعوت` (invitation) | Trump's "Board of Peace" for Gaza |
| Palestine | 9 Feb (0.36) | `کرانه باختری` (West Bank) · `الحاق` *elhaq* (annexation) · `آلبانیز` (Francesca Albanese, UN Special Rapporteur) · `غیرقانونی` (illegal) | annexation plans in the West Bank |
| Palestine | 11 May (0.40) | `یامال` (Lamine Yamal) · `بارسلونا` (FC Barcelona) · `پرچم` (flag) · `نکبت` *Nakbat* (Nakba Day, 15 May) · `عزالدین الحداد` (Izz ad-Din al-Haddad, commander of Hamas's Qassam Brigades) | football and Nakba Day |
| Hamas | 20 Jul (0.27) | `خلیل الحیه` (Khalil al-Hayya) · `انتخاب` (election) · `تبریک` (congratulations) | al-Hayya new Hamas leader |
| Hamas | 27 Jul (0.28) | `خلع سلاح` *khal'-e selah* (disarmament) · `پیش‌نویس` (draft) | draft on disarming Hamas |
| Syria | 19 Jan (0.72) | `قسد` (SDF, Kurdish-led forces) · `کردها` (Kurds) · `فرار` (escape) · `داعش` (ISIS) | fighting in north-eastern Syria, ISIS prisoners |
| Syria | 17 Aug (0.59) | `ترکیه` (Turkey) · `ابوالظهور` (Abu al-Duhur airfield) · `ادلب` (Idlib) · `الشیبانی` (Asaad al-Shaibani, Syria's foreign minister) · `اسرائیل` | Turkey and Israel in Syria |

#### Great powers and neighbours

![Great powers and neighbours](../../results/countries/charts/powers_neighbours.png)

| Country | week from (value) | typical terms of the posts in that week | event |
|---|---|---|---|
| Venezuela | 5 Jan (2.50) | `ربوده` *robudeh* ("abducted") · `همسر` (wife) · `دادگاه` (court) · `حقوق بین‌الملل` (international law) · `نقض` (violation) | capture of Nicolás Maduro and his wife by the US – in Iranian channels an "abduction" and a breach of international law |
| Turkey | 26 Jan (0.73) | `عراقچی` · `مشورت‌ها` (consultations) · `کاهش تنش‌ها` (de-escalation) | the foreign minister's consultations with Turkey |
| Russia | 16 Feb (1.48) | `رزمایش` (exercise) · `نیروی دریایی` (navy) · `اقیانوس هند` (Indian Ocean) · `مشترک` (joint) | joint naval exercise |
| India | 16 Feb (0.30) | `رزمایش` (exercise) · `میلان` (MILAN) · `دریادار` (admiral) | naval exercise MILAN |
| Afghanistan | 23 Feb (0.34) | `پاکستان` · `طالبان` (Taliban) · `درگیری` (clashes) · `مرزی` (border) | clashes between Pakistan and the Taliban |
| Pakistan | 6 Apr (1.33), 13 Apr (1.27) | `مذاکرات` (negotiations) · `هیئت` (delegation) · `خبرنگار اعزامی` (dispatched reporter) · `ونس` (JD Vance) · `فرمانده ارتش پاکستان` (Pakistan's army chief, Asim Munir) · `اسلام آباد` | mediation of the ceasefire, talks in Islamabad |
| China | 11 May (1.81) | `ترامپ` · `سفر` (trip) · `شی جین‌پینگ` (Xi Jinping) · `تایوان` (Taiwan) · `پکن` (Beijing) | Trump's trip to Beijing |
| China | 18 May (0.90) | `پوتین` (Putin) · `سفر` (trip) | Putin's trip to China |
| India | 11 May (0.54) | `بریکس` (BRICS) · `دهلی نو` (New Delhi) · `عراقچی` · `وزرای خارجه` (foreign ministers) | BRICS foreign ministers' meeting in New Delhi |
| Rep. of Azerbaijan | 22 Jun (0.18) | `قالیباف` (Ghalibaf) · `باکو` (Baku) · `اجلاس` (conference) · `مجالس` (parliaments) | Ghalibaf at a parliamentary conference in Baku |
| Ukraine | 27 Jul (0.78) | `دریای خزر` (Caspian Sea) · `کشتی` (ship) · `سیبیها` (Andrii Sybiha, Ukraine's foreign minister) · `عراقچی` | dispute over a ship in the Caspian Sea |
| Japan | 10 Aug (0.17) | `کوریل` (Kurils) · `پوتین` (Putin) · `جزایر` (islands) | dispute over the Kuril Islands |
| Turkey | 17 Aug (0.57) | `سوریه` (Syria) · `پایگاه` (base) · `نتانیاهو` · `فرودگاه` (airfield) | Turkey and Israel in Syria (as for Syria in the same week) |

#### Europe

![Europe](../../results/countries/charts/europe.png)

| Country | week from (value) | typical terms of the posts in that week | event |
|---|---|---|---|
| EU / Europe | 26 Jan (1.22) | `سپاه پاسداران` (Revolutionary Guards) · `تروریستی` (terrorist) · `خصمانه` (hostile) · `غیرمسئولانه` (irresponsible) | the EU agrees politically (29 Jan) to list the Revolutionary Guards as a terrorist organisation – and Iran's reaction |
| EU / Europe, Germany | 20 Apr (0.69 / 0.26) | `رضا پهلوی` (Reza Pahlavi) · `انرژی` (energy) · `قیمت بنزین` (petrol price) | Reza Pahlavi in Europe; energy prices |
| Germany | 27 Apr (0.38) | `صدراعظم آلمان` (German Chancellor) · `تحقیر` (humiliation) · `پنتاگون` (Pentagon) · `خروج` (withdrawal) · `ترامپ` | the Chancellor's remark ("humiliation") and the reaction from Washington |
| Italy | 22 Jun (0.28) | `ناتو` (NATO) · `پایگاه‌های` (bases) · `رومانی` (Romania) | NATO bases in Europe |
| United Kingdom, France, Spain | 13 Jul (0.61 / 0.33 / 0.45) | `جام جهانی` (World Cup) · `فینال` (final) · `آرژانتین` (Argentina) · `مسی` (Messi) | football World Cup |

In the week of the World Cup final Spain is named more often than in any other week, France already in the group stage
(22 Jun): part of the mentions of European countries is sport.

### How each group presents a country

Which terms does a group use **in its posts about a country** clearly more often than the other groups in their posts
about the same country? A selection of the most typical terms; all lists: `results/countries/framing.csv`.

| Country | state | IRGC-affiliated | Jamaran |
|---|---|---|---|
| UAE | `تومان` (toman) · `سکه` (gold coin) · `حواله` (money transfer) – **Dubai as a currency hub** | `بندر فجیره` (port of Fujairah) · `زیرساخت‌ها` (infrastructure) · `پدافندی` (air defence) – **target** | `ترامپ` · `توافق` (agreement) · `اندیشکده` (think tank) – **geopolitics** |
| Saudi Arabia | `رایزنی` (consultation) · `وزیر` (minister) · `محکوم` (condemned) – **diplomatic partner** | `یمن` · `مزدوران` ("mercenaries") · `صنعا` (Sanaa) · `محاصره` (blockade) – **opponent in Yemen** | `اسرائیل` · `حوثی‌ها` (Houthis) · `ابوظبی` (Abu Dhabi) · `وابستگی` (dependence) – **regional rival** |
| Qatar | `رایزنی` (consultation) · `آل ثانی` (Al Thani) · `کاهش تنش‌ها` (de-escalation) – **mediator** | `هلیوم` (helium) · `نیروگاه` (power plant) · `راس‌لفان` (Ras Laffan, gas facilities) – **energy infrastructure** | `ترامپ` · `نیویورک‌تایمز` · `مذاکرات` – **negotiations** |
| Oman | `رایزنی` (consultation) · `وزیر امور خارجه` – **mediator** | `تنگه هرمز` · `کشتی` (ship) · `مسندم` (Musandam) – **sea route** | `پیشنهاد` (proposal) · `مدعی` ("claims") · `لاریجانی` (Ali Larijani) – **negotiations** |
| Kuwait | `بسم الله قاصم الجبارین` (heading of military statements) · `روابط عمومی سپاه پاسداران` (IRGC public relations office) · `اطلاعیه` (announcement) – **official statements** | `منابع` (sources) · `تصاویر` (images) · `شنیده‌شدن` (being heard) · `انفجارها` (explosions) – **eyewitnesses and images** | `کشورهای عربی` (Arab states) · `امنیت` (security) · `اقتصادی` (economic) – **the region** |
| Bahrain | `سخنگوی وزارت امور خارجه` (foreign ministry spokesman) · `بسم الله قاصم الجبارین` · `روابط عمومی سپاه` – **statements** | `شنیده‌شدن` (being heard) · `آمازون` (Amazon) · `ابری` (cloud) · `فرمول` (Formula 1) | `امارات متحده عربی` · `قطر` · `انرژی` (energy) · `نفت` (oil) – **the Gulf and energy** |
| Jordan | `کرانه باختری` (West Bank) · `ثبات` (stability) · `دیپلماسی` | `پایگاه` (base) · `موشک‌های` (missiles) · `گاز` · `برق` (electricity) | `اطلاعاتی` (intelligence) · `سرباز` (soldier) · `پایگاه‌ها` (bases) · `آمریکایی` – **US military** |
| Pakistan | `تجارت` (trade) · `سازمان ملل` (UN) · `بقائی` (Baghaei) – **diplomacy** | `خبرنگار اعزامی` (dispatched reporter) · `تیم مذاکره‌کننده` (negotiating team) · `قالیباف` · `ونس` – **Islamabad up close** | `ابوظبی` (Abu Dhabi) · `پیشنهاد` (proposal) · `واشنگتن` – **mediation** |
| China | `پکن` (Beijing) · `آسیا` · `رسانه‌های` (media) | `نفتکش` (tanker) · `عبور` (passage) · `تایوان` – **oil and Hormuz** | `ایالات متحده` · `نفت` (oil) · `احتمالا` (probably) – **rivalry with the US** |
| Russia | `تاس` (TASS) · `سفیر` (ambassador) · `مسکو` · `بریکس` – **official partner** | `اوکراینی` (Ukrainian) · `پالایشگاه` (refinery) · `حمله پهپادی` (drone attack) – **the war in Ukraine** | `ترامپ` · `بازارهای` (markets) · `ریانووستی` (RIA Novosti) · `صادرات` (exports) – **oil and politics** |
| Turkey | `جنگ رمضان` ("Ramadan war") · `بقائی` – **diplomacy** | `فوتبال` · `هتل` · `یورو` – **sport and travel** | `ائتلاف` (alliance) · `غنی‌سازی` (enrichment) · `تجزیه` (partition) – **security policy** |
| Lebanon | `تداوم نقض آتش بس` (continued violation of the ceasefire) · `سازمان ملل` · `وزارت بهداشت` (health ministry) – **law and victims** | `شهرک` (settlement) · `حزب‌الله` · `نظامیان` (soldiers) · `حمله موشکی` (missile attack) – **front line** | `مذاکرات` · `مدعی` ("claims") · `نتانیاهو` – **negotiations** |
| Iraq | `اربعین` · `ثبات` (stability) · `هماهنگی` (coordination) – **neighbour and pilgrimage country** | `حشد شعبی` (Hashd militias) · `تجزیه‌طلب` (separatists) · `اربیل` (Erbil) – **security, Kurdish groups** | `ترامپ` · `میلیارد دلار` · `لاریجانی` – **geopolitics** |
| Yemen | `انصارالله یمن` (Ansarallah) · `دفتر سیاسی جنبش` (political bureau of the movement) | `سعودی` (Saudi) · `مزدوران` ("mercenaries") · `باب‌المندب` (Bab al-Mandab) | `حوثی‌ها` (Houthis) · `امارات` · `ابوظبی` |
| Gaza | `مجروحان` (wounded) · `شهدای` (martyrs) · `وزارت بهداشت` (health ministry) – **victims** | `خان‌یونس` (Khan Yunis) · `منابع محلی` (local sources) · `النصیرات` (Nuseirat) – **front line** | `نتانیاهو` · `ترامپ` – **politics** |
| Syria | `نقض` (violation) · `حاکمیت` (sovereignty) · `سازمان ملل` – **international law** | `جولانی` / `الجولانی` (Jolani – former nom de guerre of President Ahmed al-Sharaa) · `شورشیان` (rebels) | `اسد` (Assad) · `ترامپ` – **politics** |
| EU / Europe | `بروکسل` (Brussels) · `دیپلماسی` · `حقوق بین‌الملل` (international law) | `رضا پهلوی` (Reza Pahlavi) · `تجمع` (rally) – **place of the opposition** | `تضمین` (guarantee) · `آینده` (future) |
| United Kingdom | `لندن` · `داونینگ‌استریت` (Downing Street) | `کشتی` (ship) · `حادثه` (incident) · `نفتکش` (tanker) – **shipping incidents** | `مصدق` (Mohammad Mossadegh, 1953 coup) · `نفت` (oil) – **history** |

**Differences between the channels** (per 1,000 words, `countries.csv`, level `channel`): IRNA names Russia during the
war almost as often as before (0.66 → 0.63), Fars, Tasnim and Mehr only a third as often (0.21–0.27). IRNA names
Hezbollah least often (0.28, Tasnim 0.88) and the UAE least often (0.19, Fars 0.48). Pakistan reaches its highest value
in all six channels during the ceasefire (0.63–0.92).

### What stands out

- **Three ways of showing the same world.** State channels report on countries in the language of diplomacy and
  international law (consultation, condemnation, UN). IRGC-affiliated channels show countries as a **scene of action**:
  ports, bases, refineries, front lines. Jamaran sees almost every country through the **lens of the US** – with Trump,
  "agreement" and "claims".
- **The UAE** are two things: for the state media a currency hub (toman, gold coins, money transfers), for the
  IRGC-affiliated channels a target (port of Fujairah, week from 4 May). In the following week the typical terms are
  Netanyahu, secret, denial – the UAE's closeness to Israel becomes a topic. At Jamaran `ابوظبی` (Abu Dhabi) also
  appears in the posts about Pakistan, Saudi Arabia, Yemen and India: the UAE as an actor in the background.
- **Saudi Arabia** is a partner in talks for the state media and the opponent in Yemen ("mercenaries") for the
  IRGC-affiliated channels. After the collapse of the ceasefire it is named there four and a half times as often as
  before.
- **Kuwait and Bahrain:** the state channels report the attacks there with the statements of the Revolutionary Guards,
  the IRGC-affiliated channels with "sources", images and explosions that "were heard".
- **Pakistan** is seen everywhere as a mediator, but differently: in the state media with trade and the UN, in the
  IRGC-affiliated channels with their own reporters in Islamabad, next to `قالیباف` (Ghalibaf) and `تیم مذاکره‌کننده`
  (negotiating team), at Jamaran with proposals, Washington and Abu Dhabi.
- **China** reaches its peak not with an event between Iran and China, but with Trump's trip to Beijing.
- **Russia** moves into the background during the war – to a third in the IRGC-affiliated channels. Their posts about
  Russia are mainly about the war in Ukraine. State channels quote Russian sources on Russia and Ukraine (`تاس` TASS,
  `سخنگوی کرملین` Kremlin spokesman, `زاخارووا` Maria Zakharova, spokeswoman of the Russian foreign ministry).
- **Syria's president** is called `جولانی` (Jolani) in the IRGC-affiliated channels – his former nom de guerre as a
  jihadist.
- **Yemen's Houthis** are called `حوثی‌ها` (Houthis) at Jamaran and `انصارالله` (Ansarallah) in the state media – the
  name the movement uses itself.
- **Gaza** falls sharply during the war (from 0.37–0.45 to 0.08–0.12) and only returns with the
  ceasefire.

---

## 7. Topics according to the AI

The basis is the AI classification of 10,750 posts (Gemma 4 31B, codebook v8), weighted to all 231,406 posts with more
than 80 characters ([03](03_ai_classification.md), `03e_topics.py`). Shown is the share of posts in percent.
In the final validation on 200 new posts the topic was correct in **72.5%** of cases (95% interval 65.9–78.2%).
**Tone** is not evaluated: the AI misses non-neutral tones, and to a different degree for each group
([03, section 8](03_ai_classification.md#8-final-validation-phase-c--result)).

| Topic | state | IRGC-affiliated | Jamaran |
|---|---|---|---|
| `military` | 16.6 | **22.5** | 22.2 |
| `diplomacy` | 12.9 | 12.0 | **20.0** |
| `domestic_politics` | **14.8** | 13.6 | 14.5 |
| `other` (service, weather, sport, culture) | **16.2** | 9.8 | 6.3 |
| `economy` | 8.0 | 8.1 | **9.7** |
| `foreign_affairs` (abroad, without Iran) | 8.5 | 7.9 | **10.4** |
| `mourning_commemoration` | **9.7** | 9.4 | 6.8 |
| `resistance_axis` | 6.5 | **9.1** | 5.8 |
| `ideology_propaganda` | 6.9 | **7.6** | 4.3 |

Shares in %, whole period. Per channel: `results/ai/topics/topic_shares.xlsx`.

![Topics by phase](../../results/ai/topics/charts/topics_by_phase.png)

| | before the war | war | ceasefire | after the collapse |
|---|---|---|---|---|
| Military, all groups | 4–5 | **36–45** | 13–15 | 14–28 |
| Domestic politics, all groups | **24–31** | 6–10 | 11–13 | 15–19 |
| Diplomacy, Jamaran | 23.2 | 18.2 | **25.1** | 11.5 |
| Diplomacy, IRGC-affiliated | 11.6 | **6.7** | 16.8 | 8.8 |
| Mourning and commemoration, all groups | 3–5 | 6–8 | **9–12** | 6–10 |
| Resistance axis, IRGC-affiliated | 4.5 | 7.9 | 10.3 | **11.0** |
| Ideology, state / IRGC-affiliated | 7.3 / 7.2 | **11.4 / 12.4** | 6.5 / 6.8 | 4.1 / 4.1 |
| Other, state | 20.5 | **5.2** | 18.5 | 17.9 |

Shares in %; a range means: lowest to highest value of the three groups.

- **The war pushes everything else aside:** in the war phase 36–45% of posts are military, before 4–5%. Domestic
  politics falls from 24–31% to 6–10%; "other" (service, sport, culture) falls from 20.5% to 5.2% in the state channels.
- **Jamaran is the channel of diplomacy** – with the highest share in every phase, a quarter of all posts during the
  ceasefire. This fits the word analysis (negotiations, Trump, the nuclear issue, section 1). After the collapse of the
  ceasefire diplomacy falls to 9–12% in all groups.
- **IRGC-affiliated channels** report least on diplomacy during the war (6.7%) and most on the resistance axis, whose
  share rises steadily until August.
- **Ideology** is highest in state and IRGC-affiliated channels during the war (11–12%) and low at Jamaran in all
  phases (4–5%).
- **Mourning and commemoration** rise after the war to 9–12% – the time of the commemorations and the funeral
  ceremonies for Ali Khamenei (3–10 Jul).
- **State channels** publish many service notices outside the war (other 17.9–20.5%) and report less on military matters
  after the collapse of the ceasefire (14%) than IRGC-affiliated channels (23%) and Jamaran (28%).

**Read with care:** in the final validation the AI assigned *military* too often and *diplomacy* too rarely – mainly
for analyses of the war. Military is therefore rather overestimated and diplomacy underestimated; this affects all
phases similarly, so changes over time are more reliable than levels. Topic classification was least certain for
Jamaran (55.9% correct, only 34 posts checked); the high military share after the collapse may partly come from
analyses of the war.

---

## 8. Activity and reach

| | state | IRGC-affiliated | Jamaran |
|---|---|---|---|
| Posts per day and channel | 237 | 222 | 195 |
| Views per post (median) | 1,259 | **11,858** | 1,593 |
| Forwards per post (median) | 5 | **18** | 5 |
| Forwards per 1,000 views | **5.1** | 2.1 | 4.2 |

![Posts per day](../../results/activity/charts/posts_per_day.png)

- **Activity:** Before the war a channel publishes 122–134 posts a day, averaged over the groups (single channels
  109–178). In the first week of the war (from 2 Mar) it is 321–423 – for single channels from 227 (IRNA) to 505 (Mehr
  News). The second peak is, in the state and IRGC-affiliated channels, in the week of the farewell ceremony and the
  collapse of the ceasefire (from 29 Jun / 6 Jul), at Jamaran in the week from 13 Jul.
- **January:** In the week from 12 Jan Jamaran posts only 20 posts a day and IRNA nothing at all – the time of the
  internet blackout.
- **Reach:** the IRGC-affiliated channels reach seven to nine times as many views per post (median 11,858 against
  1,259 and 1,593). This probably depends mainly on the number of
  subscribers, which was not collected – it describes reach, not quality.
- **Fewer views during the war:** With the start of the war, views per post fall at Jamaran (median from 3,329 to 969)
  and in the IRGC-affiliated channels (from 18,586 to 12,309), although more is posted. In the state channels the group
  median stays the same (1,803 before, 1,802 during the war); the single channels fall only slightly (IRNA 1,643 to
  1,510, IRIB News 3,322 to 2,742, Mehr News 1,466 to 1,408). Possible reasons – more posts for the same readers,
  restricted internet access – cannot be separated with these data.
- **Forwards:** Posts of state channels and Jamaran are forwarded 2.0 to 2.4 times as often per view as those of
  IRGC-affiliated channels (per 1,000 views: state 5.1, Jamaran 4.2, IRGC-affiliated 2.1).

More charts: [views](../../results/activity/charts/views_median.png) ·
[forwards per 1,000 views](../../results/activity/charts/forwards_per_1000_views.png)

---

## 9. Limitations

- **Counting is not understanding.** The counts do not see context: negation, quotation or irony count the same.
  Whether a term is used approvingly or at a distance is only shown by the AI classification or by reading.
- **Peak weeks:** The typical terms of a week show what shaped the week – not that every post with the counted word is
  about it. Linking peaks to events is an interpretation based on the data and the timeline.
- **Decisions of the author:** corrections list, naming list, phase and event dates. They are documented openly; other
  decisions would give slightly different numbers.
- **Rules checked with samples,** not every post read (Leader assignment, cleaning).
- **Different channel profiles:** state channels publish a lot of service and administrative content, which lowers their
  share of political terms per 1,000 words.
- **Views and forwards** are the numbers at the time of collection; subscriber numbers are missing.
- **No network analysis:** for forwarded posts only the sender name was saved during collection, which is usually empty
  for channels (96 of 328,330 posts). Who forwards whom can therefore not be analysed.
- **Gaps in January:** IRNA and Jamaran hardly posted in mid-January (internet blackout, see [01](01_data_collection.md)).
- **Time zone:** days, weeks and phases of the word, timeline and activity analyses are based on the UTC date of the posts (Tehran: UTC+3:30). Only the AI topic shares per phase use the Tehran date; there the ceasefire ends on 7 Jul (database: 6 Jul). By UTC date 48 of 10,750 AI posts would fall into another phase, and the group shares would change by at most 1.5 percentage points (details: [06](06_methodology.md#3-data-quality-and-gaps)).
- **Countries:** `عمان` means Oman, but also Amman (capital of Jordan); the Gulf of Oman (`دریای عمان`) is removed
  first. `آذربایجان` alone counts as the Republic of Azerbaijan but sometimes means the Iranian provinces of East and
  West Azerbaijan – weather terms are typical of the state posts about it; the value is therefore too high. Egypt is
  missing because `مصر` also means "insistent" (*moser*). Part of the mentions of European countries, Turkey and Qatar
  is about sport.
- **How a country is presented:** the typical terms describe the posts that name a country – not every statement
  about the country. A post naming several countries counts for each of them.
- **AI topics:** based on a weighted sample of 10,750 posts; the topic is correct in 72.5% of cases (final
  validation). Military is rather overestimated, diplomacy underestimated; tone is not evaluated (see 03).
- The "reformist" group consists of **one channel**.

---

## 10. Method

### From words to fixed terms (`01_word_frequency.py`, `03_terms.py`)

Single words are not enough: `رژیم صهیونیستی` ("Zionist regime") would be counted as `رژیم` and `صهیونیستی`.
`03_terms.py` finds fixed terms of two to four words **without a predefined word list** and counts every place in a text
exactly once.

| Rule | Example |
|---|---|
| A word sequence occurs at least 100 times | – |
| Two words: at least 25% of the occurrences of the rarer word are in this sequence | `تنگه هرمز` (Strait of Hormuz) → term |
| Three or four words: at least 25% of both shorter parts are in this sequence | `وزیر امور خارجه` (foreign minister) → term; `حمله رژیم صهیونیستی` (attack by the Zionist regime) → not a term |
| Office words (`وزیر` minister, `رئیس` president, `سخنگوی` spokesman …) only as the first word | `عباس عراقچی وزیر امور` → not a term, person and office stay separate |
| In the text the longer term wins; with the same length the more frequent one | `رهبر شهید انقلاب` ("martyred Leader of the Revolution") counts once, not also as `رهبر شهید` |

Result: **1,501 fixed terms** (1,490 automatic, 11 added by the author). `phrases.csv` shows how often a word sequence
occurs (`count`, also inside longer terms) and how often it was counted as a term of its own (`count_used`,
before spelling variants are merged). `count` is a lower bound: occurrences in channel/phase parts in which the sequence appears fewer than 5 times are
not added (at most 4 per part, at most 96 over the 24 parts); `count_used` is exact and can therefore be larger than `count` for
a sequence that is rarely part of a longer term. The selection of the fixed terms rests on `count`; for sequences close to the
thresholds (100 occurrences, 25%) it can differ from an exact count (not recalculated – the unpublished raw texts are needed).

**Corrections list** (`phrase_corrections.csv`) – the author's decisions, kept openly in one file:

| Action | Number | Example |
|---|---|---|
| `title` – office word | 12 | `وزیر` (minister), `رئیس` (president/head), `سخنگوی` (spokesman), `فرمانده` (commander) |
| `add` – long names as one term | 11 | `نیروی دریایی سپاه پاسداران انقلاب اسلامی` (IRGC Navy, 6 words) · `وزارت کشور` (Ministry of the Interior) |
| `remove` – terms found by mistake | 5 | `امور خارجه جمهوری اسلامی` (two terms joined) |
| `merge` – spelling and name variants | 56 | `سید عباس عراقچی` → `عراقچی` (Araghchi) · `حاج قاسم` → `سلیمانی` (Qasem Soleimani) |
| `ignore` – without content, counted but not listed | 263 | channel names, "live", "photo", reporting verbs such as `تاکید` ("emphasised"), titles without a name |

In addition, 3,824 spellings that differ only by the half-space are merged. Singular and plural stay separate:
`کشور` *keshvar* (country – often Iran itself) and `کشورهای` *keshvar-ha-ye* (countries – other states). The list was
checked in several rounds; work stopped when further corrections no longer changed the findings.

### Typical terms (`07_typical_terms.py`, `11_peak_weeks.py`)

Weighted log-odds ratio with an informative prior ("Fightin' Words", Monroe, Colaresi & Quinn 2008): for every term a
z-score of how much more frequent it is in one group than in the others; above 1.96 the difference is statistically
clear. Rare terms are damped (minimum frequency 50). **Every channel must agree:** IRNA has the most and longest posts
and would otherwise decide on its own what is "typically state". Therefore every channel is compared with the channels
of the other groups; the z-score of the group is the lowest of its channels. `11_peak_weeks.py` applies the same
method to one week compared with all other weeks of the same group.

### Naming and persons (`08_naming.py`)

An open list (`naming_terms.csv`): 113 concepts with 188 spellings in 10 categories. Only whole words (`اسرائیلی`
"Israeli" does not count as `اسرائیل` "Israel"); within a category the longest form comes first
(`ارتش تروریستی آمریکا` is not counted again as `آمریکا`).

### Which Khamenei? (`06_leader_mentions.py`)

| Date (set by the author) | |
|---|---|
| 1 Mar | Ali Khamenei's death officially confirmed in Iran (`DEATH_DAY`) |
| 8 Mar | Mojtaba Khamenei selected (`APPOINTMENT_DAY`) |

Mojtaba only counts with his full name (`سید مجتبی` alone often means other persons); hints to Ali are e.g.
`رهبر شهید` (the martyred Leader), `سوگ رهبر` (mourning the Leader), `مراسم تشییع` (funeral procession); brothers and
other sons are removed first. Until 8 March, `رهبر` without a name means Ali Khamenei, afterwards Mojtaba, unless the
text contains a hint to Ali. **Check:** 50 random posts from 1 to 8 March without a name – all concerned Ali
Khamenei; samples of every category were read and led to new rules. The check file with texts stays private.

### Countries (`12_countries.py`)

The category `countries_actors` of `naming_terms.csv`, counted as in `08_naming.py`: only whole words, the longest form
first – `دریای عمان` (Gulf of Oman) does not count as Oman, `فلسطین اشغالی` ("occupied Palestine" = Israel) not as
Palestine. For the terms around a country the same method as in `07` and `11`, but at group level (without checking
each channel) and with a minimum frequency of 20 instead of 50, because the amount of text per country is smaller.

| Analysis | Comparison |
|---|---|
| Peak weeks | posts about the country in the peak week against the posts about the country in all other weeks (all groups together) |
| Presentation | a group's posts about the country against the other groups' posts about the same country; only from 100 posts of the group |

### Time series and activity (`09_timeline.py`, `10_activity.py`)

The same counts per calendar week; only complete weeks in the charts. Activity: posts per day and channel (for groups
divided by the number of channels), views and forwards as median, forwards per 1,000 views. Colours: state blue,
IRGC-affiliated red, Jamaran green – checked for colour-vision deficiency.

### AI topics (`scripts/ai/03e_topics.py`)

Weighted share of every topic per group, channel and phase: each post counts with its weight (posts of its
channel-week / posts drawn). Phases here by date in Tehran time (ceasefire until 7 Jul, then from 8 Jul; the database and all other analyses use UTC days with the boundary 6/7 Jul, see [06](06_methodology.md#3-data-quality-and-gaps)). Classification and testing of the
AI: [03](03_ai_classification.md).

### Detours and helper scripts

| Script | What it showed |
|---|---|
| `02_word_pairs.py` | word pairs – counted the same place several times, replaced by 03 |
| `03b_terms_long.py` | test with up to 8 words: longer sequences were almost only chains of person and office → limit of 4 words plus list |
| `04_context.py` | neighbouring words and example sentences for one word, terminal only |
| `05_noise_candidates.py` | suggests words without content for the `ignore` list |
| network analysis (dropped) | who forwards whom? – not possible, see limitations |

---

## 11. Files

| Script | Purpose | Result (`results/`) |
|---|---|---|
| `scripts/analysis/01_word_frequency.py` | most frequent single words | `words/word_frequency.*` |
| `scripts/analysis/03_terms.py` | fixed terms, every place counted once | `words/phrases.csv`, `words/terms.*` |
| `scripts/analysis/06_leader_mentions.py` | Ali or Mojtaba Khamenei | `leader/leader_mentions.*` |
| `scripts/analysis/07_typical_terms.py` | typical terms per group and channel | `words/typical_terms.*` |
| `scripts/analysis/08_naming.py` | naming, persons, neighbouring words | `naming/naming.*`, `naming/neighbours.csv` |
| `scripts/analysis/09_timeline.py` | weekly change, charts | `timeline/timeline.*`, `timeline/charts/` |
| `scripts/analysis/10_activity.py` | activity and reach | `activity/*`, `activity/charts/` |
| `scripts/analysis/11_peak_weeks.py` | typical terms of the peak weeks | `timeline/peak_weeks.csv` |
| `scripts/analysis/12_countries.py` | countries and groups: frequency, peak weeks, presentation per group | `countries/*`, `countries/charts/` |
| `scripts/ai/03e_topics.py` | topics according to the AI per group, channel and phase | `ai/topics/*`, `ai/topics/charts/` |
| `scripts/analysis/phrase_corrections.csv` | the author's corrections list | – |
| `scripts/analysis/naming_terms.csv` | list of names and persons | – |
| `02`, `03b`, `04`, `05` | intermediate steps and helper scripts (see above) | – |

Order: `03` → `07` → `06` → `08` → `09` → `10` → `11` → `12`. Technology: Python 3.11, `pandas`, `numpy`, `matplotlib`,
`SQLAlchemy`. Description of all result files: [results/README.md](../../results/README.md).
