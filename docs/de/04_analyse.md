[English](../en/04_analysis.md) | **Deutsch**

# 04 – Analyse: Wortwahl, Benennungen, Zeitverlauf und Reichweite

[← zurück zur Übersicht](../../README.de.md)

Diese Seite wertet das **vollständige Korpus** aus – ohne KI, nur mit Zählungen und Statistik in Python.
Gefragt wird: Welche Wörter und Begriffe verwenden die drei Quellengruppen, wie benennen sie dieselben Akteure,
wie verändert sich das im Zeitverlauf, und wie viele Menschen erreichen sie?

Die Einordnung nach **Thema und Ton** durch die KI ([03](03_ki_einordnung.md)) ist ein eigener Schritt; ihre
Auswertung folgt nach dem Hauptlauf.

| | |
|---|---|
| Grundlage | 328.330 Beiträge, davon 267.548 mit Text (bereinigt, siehe [02](02_aufbereitung.md)) |
| Einheit | Häufigkeit **pro 1.000 Wörter** – so sind Kanäle und Gruppen unterschiedlicher Größe vergleichbar |
| Zeit | ganzer Zeitraum, vier Phasen (siehe [02](02_aufbereitung.md#phasen)) und Kalenderwochen |
| Ergebnisse | nur Zahlen in `results/` – keine Beitragstexte |
| Status | ✅ abgeschlossen (Wortanalyse) · ⏳ Auswertung der KI-Einordnung folgt |

---

## Die wichtigsten Ergebnisse

- **Staatliche Medien** haben das Profil einer Verwaltungs- und Serviceagentur: Provinzen, Monatsnamen, Wochentage,
  Behördenleiter. **IRGC-nahe Medien** sind geprägt von Sicherheit, Militär und Protesten (Hisbollah, Drohne,
  „Unruhen“, „Randalierer“). **Jamaran** berichtet deutlich mehr über Diplomatie, US-Politik und Reformpolitiker.
- Israel wird in staatlichen und IRGC-nahen Kanälen zunehmend „zionistisches Regime“ genannt – nach dem Zusammenbruch
  der Waffenruhe in **57 %** bzw. **53 %** der Nennungen. Jamaran schreibt überwiegend „Israel“ (**70 %**).
- Alle sechs Kanäle bezeichnen Mojtaba Khamenei erst am Tag seiner offiziellen Ernennung (08.03.) als Revolutionsführer.
  Danach betreffen trotzdem rund **drei Viertel** aller Erwähnungen des Führers weiterhin den getöteten Ali Khamenei.
- Rache- und Gegnerbegriffe („Verräter“, „Söldner“, „Randalierer“) sind in IRGC-nahen Kanälen deutlich häufiger –
  Gegnerbegriffe etwa **doppelt so oft** wie in den anderen Gruppen. Jamaran nennt Trump am häufigsten und schreibt am häufigsten „Trump **behauptet**“.
- IRGC-nahe Kanäle erreichen pro Beitrag rund **zehnmal so viele Aufrufe** wie staatliche Kanäle und Jamaran,
  werden im Verhältnis dazu aber seltener weitergeleitet.

---

## 1. Von Wörtern zu festen Begriffen

### Einzelwörter (`01_word_frequency.py`)

Der erste Schritt zählt einzelne Wörter pro Kanal, Gruppe und Phase. Die Listen sind in allen Kanälen fast gleich
(ایران, آمریکا, جنگ, مردم …) und haben ein Grundproblem: Ein Begriff wie `رژیم صهیونیستی` („zionistisches Regime“)
wird als zwei Wörter gezählt, `رژیم` und `صهیونیستی`.

### Feste Begriffe (`03_terms.py`)

Das Skript findet feste Begriffe aus zwei bis vier Wörtern **ohne vorgegebene Wortliste** und zählt jede Stelle im
Text genau einmal.

| Regel | Beispiel |
|---|---|
| Eine Wortfolge kommt mindestens 100-mal vor | – |
| Zwei Wörter: mindestens 25 % der Vorkommen des selteneren Worts stehen in dieser Folge | `تنگه هرمز` (Straße von Hormus) → Begriff |
| Drei oder vier Wörter: mindestens 25 % beider kürzerer Teile stehen in dieser Folge | `وزیر امور خارجه` (Außenminister) → Begriff; `حمله رژیم صهیونیستی` (Angriff des zionistischen Regimes) → kein Begriff |
| Amtsbezeichnungen (وزیر, رئیس, سخنگوی …) nur als erstes Wort | `عباس عراقچی وزیر امور` → kein Begriff, Person und Amt bleiben getrennt |
| Im Text gewinnt der längere Begriff; bei gleicher Länge der häufigere | `رهبر شهید انقلاب` zählt einmal, nicht zusätzlich als `رهبر شهید` oder `شهید انقلاب` |

Ergebnis: **1.501 feste Begriffe** (1.490 automatisch gefunden, 11 vom Autor ergänzt). `phrases.csv` zeigt für jeden
Begriff, wie oft die Wortfolge insgesamt vorkommt (`count`) und wie oft sie tatsächlich als dieser Begriff gezählt
wurde (`count_used`). Beispiel: `اسلامی ایران` kommt 15.596-mal vor, steht aber fast immer in
`جمهوری اسلامی ایران` (Islamische Republik Iran) und wird deshalb kaum einzeln gezählt.

### Korrekturliste (`phrase_corrections.csv`)

Automatische Regeln machen Fehler. Die Entscheidungen des Autors stehen offen in einer Datei:

| Aktion | Anzahl | Beispiel |
|---|---|---|
| `title` – Amtsbezeichnung | 12 | وزیر, رئیس, سخنگوی, فرمانده |
| `add` – lange Namen als ein Begriff | 11 | نیروی دریایی سپاه پاسداران انقلاب اسلامی (Marine der Revolutionsgarde, 6 Wörter), وزارت کشور (Innenministerium) |
| `remove` – falsch gefundene Begriffe | 5 | امور خارجه جمهوری اسلامی (zwei Begriffe verbunden) |
| `merge` – Schreib- und Namensvarianten | 56 | سید عباس عراقچی → عراقچی, حاج قاسم → سلیمانی |
| `ignore` – ohne Inhalt, gezählt, aber nicht gelistet | 263 | Kanalnamen, „live“, „Foto“, Berichtsverben wie „betonte“, Titel ohne Namen |

Außerdem werden 3.824 Schreibweisen, die sich nur im Halbleerzeichen unterscheiden, zusammengeführt. Einzahl und
Mehrzahl bleiben bewusst getrennt: `کشور` (Land, oft Iran selbst) und `کشورهای` (Länder, andere Staaten) meinen
Verschiedenes.

**Wann ist die Liste fertig?** Sie wurde in mehreren Runden anhand der Ergebnislisten geprüft. Abgebrochen wurde,
als weitere Korrekturen die Aussagen nicht mehr änderten. Die Liste bleibt eine **Setzung des Autors** – mit anderer
Liste ergäben sich leicht andere Ranglisten.

### Irrwege und Hilfsskripte

| Skript | Was es zeigte |
|---|---|
| `02_word_pairs.py` | Wortpaare und Dreiergruppen – zählte dieselbe Stelle mehrfach, deshalb ersetzt durch 03 |
| `03b_terms_long.py` | Test mit bis zu 8 Wörtern: längere Folgen waren fast nur Ketten aus Person und Amt → Grenze 4 Wörter plus Liste |
| `04_context.py` | Nachbarwörter und Beispielsätze zu einem Wort, nur im Terminal – zur Prüfung einzelner Begriffe |
| `05_noise_candidates.py` | schlägt Wörter ohne Inhalt für die `ignore`-Liste vor |

---

## 2. Typische Begriffe je Quellengruppe (`07_typical_terms.py`)

Die häufigsten Begriffe sind überall fast gleich. Aufschlussreich ist, was eine Gruppe **deutlich häufiger** sagt
als die anderen.

**Methode:** gewichtetes Log-Odds-Verhältnis mit informativem Prior („Fightin' Words“, Monroe, Colaresi & Quinn 2008).
Für jeden Begriff ergibt sich ein z-Wert; über 1,96 ist der Unterschied statistisch deutlich. Seltene Begriffe werden
durch den Prior gedämpft, damit ein Wort mit drei Vorkommen nicht zufällig oben landet (Mindesthäufigkeit 50).

**Jeder Kanal muss zustimmen:** IRNA hat mit Abstand die meisten und längsten Beiträge und würde sonst allein
bestimmen, was „typisch staatlich“ ist. Deshalb wird jeder Kanal einer Gruppe gegen die Kanäle der anderen Gruppen
verglichen; ein Begriff gilt nur als typisch, wenn er es für **jeden** Kanal der Gruppe ist. Der z-Wert der Gruppe
ist der niedrigste ihrer Kanäle.

| Rang | staatlich | z | IRGC-nah | z | reformorientiert (Jamaran) | z |
|---|---|---|---|---|---|---|
| 1 | استان (Provinz) | 11,3 | حزب‌الله (Hisbollah) | 20,8 | ترامپ (Trump) | 44,6 |
| 2 | اردیبهشت (Monatsname) | 10,8 | پهپاد (Drohne) | 15,0 | اینترنت (Internet) | 39,1 |
| 3 | بقائی (Außenamtssprecher) | 9,2 | اغتشاشات („Unruhen“) | 14,2 | ایران | 36,3 |
| 4 | شنبه (Samstag) | 8,4 | صهیونیست‌ها („die Zionisten“) | 13,6 | توافق (Abkommen) | 33,8 |
| 5 | جمهوری اسلامی ایران | 8,2 | ارتش (Armee) | 13,3 | ایالات متحده (Vereinigte Staaten) | 32,7 |
| 6 | حسینی | 7,8 | خیابان (Straße) | 12,7 | مدعی („behauptet“) | 32,6 |
| 7 | معاون (Stellvertreter) | 7,6 | بیعت (Treueeid) | 12,5 | مذاکرات (Verhandlungen) | 30,3 |
| 8 | دوشنبه (Montag) | 7,1 | موشک (Rakete) | 12,4 | جنگ (Krieg) | 29,6 |
| 9 | مدیرکل (Generaldirektor) | 6,8 | دستگیر (festgenommen) | 12,4 | سید حسن خمینی | 27,6 |
| 10 | خرداد (Monatsname) | 6,6 | اینترنشنال (Iran International) | 12,0 | خاتمی (Khatami) | 25,7 |

- **Staatlich:** Verwaltung und Service – Provinzen, Kalender, Behörden, Schulen, Wetter. Die z-Werte sind niedrig:
  Die drei staatlichen Kanäle sind untereinander verschieden und teilen wenig Eigenes.
- **IRGC-nah:** Militär, Sicherheit und Proteste; Gegnerbegriffe (اغتشاشگران „Randalierer“, ضدانقلاب „Konterrevolution“),
  oppositionelle Medien und Personen (Iran International, رضا پهلوی).
- **Jamaran:** Diplomatie, US-Politik und Reformlager (Hassan Khomeini, Khatami); Internet – im Januar und April/Mai.
- **Nach Phasen** (Blätter pro Gruppe in `typical_terms.xlsx`): IRGC-nah vor dem Krieg „Unruhen“, „Randalierer“,
  „Konterrevolution“; im Krieg عبری (hebräisch – Zitate aus israelischen Medien) und „Treueeid“; nach dem Zusammenbruch
  der Waffenruhe Saudi-Arabien, Jemen, Bahrain, Kuwait. Bei Jamaran steht in der Waffenruhe „Internet“ an erster Stelle.

---

## 3. Welcher Khamenei ist gemeint? (`06_leader_mentions.py`)

`خامنه‌ای` und `رهبر` („der Führer“) können Ali Khamenei (im Krieg getötet) oder seinen Sohn und Nachfolger
Mojtaba Khamenei meinen. Tausende Beiträge lassen sich nicht lesen – deshalb Regeln, die mit Stichproben geprüft wurden.

| Datum (vom Autor gesetzt) | |
|---|---|
| 28.02. | Ali Khamenei getötet |
| 01.03. | Tod in Iran offiziell bestätigt (`DEATH_DAY`) |
| 08.03. | Mojtaba Khamenei nach der Wahl offiziell ernannt (`APPOINTMENT_DAY`) |

**Regeln:** Mojtaba nur mit vollem Namen (`سید مجتبی` allein meint oft andere Personen); Hinweise auf Ali wie
„der Märtyrer-Führer“, „Trauer um den Führer“, „Beisetzung“; Brüder und andere Söhne werden vorher entfernt.
Bis zum 08.03. meint `رهبر` ohne Namen Ali Khamenei, danach Mojtaba, sofern kein Hinweis auf Ali im Text steht.

**Prüfung:** Eine Zufallsstichprobe von 50 Beiträgen vom 1. bis 8. März ohne Namen und Hinweis betraf in allen 50 Fällen
Ali Khamenei. Zufallsstichproben je Kategorie wurden gelesen; gefundene Fehler führten zu neuen Regeln. Die Prüfdatei mit
Texten bleibt privat (`data/check/`).

**Ergebnis:**

- Alle sechs Kanäle schreiben am **01.03.** zum ersten Mal „رهبر شهید“ (der Märtyrer-Führer).
- Alle sechs Kanäle nennen Mojtaba Khamenei erst am **08.03.** in einem Satz mit „Führer“ – **kein Kanal vorher**.
  Jamaran und Mehr nennen seinen Namen schon ab dem 03.03., Tasnim ab dem 05.03. – aber noch nicht als Führer.
- Auch nach der Ernennung betrifft die Mehrheit der Erwähnungen weiterhin Ali Khamenei:

| Phase | Ali | Mojtaba | beide |
|---|---|---|---|
| Krieg (28.02.–07.04.) | 55 % | 35 % | 10 % |
| Waffenruhe | 74 % | 22 % | 4 % |
| nach dem Zusammenbruch der Waffenruhe | 79 % | 17 % | 3 % |

Alle sechs Kanäle zusammen, 22.897 Beiträge; Werte pro Kanal in `leader_mentions.xlsx`. Am höchsten ist der Anteil
Mojtabas im Krieg bei Fars (45 %) und IRIB News (42 %).

---

## 4. Benennungen: Wie heißen dieselben Dinge? (`08_naming.py`)

Hier gibt es eine **vorgegebene Liste** (`naming_terms.csv`): 108 Begriffe mit 182 Schreibweisen in 11 Kategorien,
z. B. alle Bezeichnungen für Israel. Die Liste ist offen einsehbar und kann ergänzt werden. Gezählt werden nur ganze
Wörter (`اسرائیلی` zählt nicht als `اسرائیل`); innerhalb einer Kategorie zuerst die längste Form.

### Israel

Anteil an allen Bezeichnungen für Israel:

| | staatlich | IRGC-nah | Jamaran |
|---|---|---|---|
| **رژیم صهیونیستی** („zionistisches Regime“), ganzer Zeitraum | 48 % | 40 % | 29 % |
| – vor dem Krieg | 46 % | 40 % | 28 % |
| – Krieg | 42 % | 35 % | 31 % |
| – Waffenruhe | 48 % | 40 % | 29 % |
| – nach dem Zusammenbruch der Waffenruhe | **57 %** | **53 %** | 26 % |
| **اسرائیل** („Israel“), ganzer Zeitraum | 45 % | 50 % | **65 %** |

Staatliche und IRGC-nahe Kanäle verwenden „zionistisches Regime“ nach dem 08.07. deutlich häufiger, Jamaran nicht.
IRGC-nahe Kanäle schreiben außerdem häufiger `صهیونیست‌ها` („die Zionisten“, 6 %) und `فلسطین اشغالی` („besetztes
Palästina“ für israelisches Staatsgebiet, 10 % gegenüber 3 % bei Jamaran).

![Anteil „zionistisches Regime“](../../results/timeline/charts/israel_zionist_regime_share.png)

### USA

`آمریکا` ist überall die Hauptbezeichnung (76–84 %). Jamaran schreibt häufiger die formale Bezeichnung
`ایالات متحده` („Vereinigte Staaten“, 11 % gegenüber 7 % und 5 %). Abwertende Bezeichnungen wie
`ارتش تروریستی آمریکا` („terroristische Armee Amerikas“) nehmen nach dem Zusammenbruch der Waffenruhe in allen
Gruppen zu (auf 3 %).

### Personen, Diplomatie, Rache, Gegner

Pro 1.000 Wörter:

| | staatlich | IRGC-nah | Jamaran |
|---|---|---|---|
| Trump | 1,86 | 2,06 | **3,11** |
| Ghalibaf (Parlamentspräsident) | 0,23 | **0,32** | 0,27 |
| Baghaei (Außenamtssprecher) | **0,28** | 0,14 | 0,13 |
| Khatami | 0,01 | 0,02 | **0,12** |
| Zarif | 0,01 | 0,01 | **0,06** |
| Diplomatie (Verhandlungen, Abkommen, Waffenruhe, Frieden …) | 3,88 | 3,04 | **5,39** |
| Rache (انتقام, خونخواهی, قصاص …) | 0,20 | **0,32** | 0,12 |
| Bezeichnungen für Gegner (Verräter, Söldner, Randalierer …) | 0,25 | **0,48** | 0,22 |
| Verbrechen (Völkermord, Kindermörder, Kriegsverbrechen …) | **1,03** | 0,90 | 0,75 |

### Wörter neben Trump und Netanjahu

| Wort direkt nach „Trump“ | staatlich | IRGC-nah | Jamaran |
|---|---|---|---|
| مدعی („behauptet“) | 2,8 % | 3,0 % | **8,2 %** |
| جنایتکار („Verbrecher“) | 0,5 % | **1,4 %** | – |
| قمارباز („Spieler“, Glücksspieler) | – | 0,6 % | – |

„–“ = nicht unter den 20 häufigsten Nachbarwörtern. Jamaran rahmt Trumps Aussagen als Behauptung; IRGC-nahe Kanäle
verwenden häufiger persönliche Abwertungen. Vollständige Listen in `neighbours.csv`.

---

## 5. Zeitverlauf (`09_timeline.py`)

Dieselben Begriffe pro **Kalenderwoche**. Jeder Punkt ist der Wert einer Woche, nicht aufsummiert. Die erste und die
letzte Woche sind unvollständig (Daten ab 01.01. bzw. nur 31.08.) und fehlen deshalb in den Diagrammen, stehen aber in
`timeline.csv`. Senkrechte Linien markieren Kriegsbeginn (28.02.), neuen Führer (08.03.), Waffenruhe (08.04.) und
Zusammenbruch der Waffenruhe (08.07.).

| Diagramm | Was man sieht |
|---|---|
| ![Internet](../../results/timeline/charts/internet.png) | „Internet“ fast nur bei Jamaran, mit Spitzen im Januar und von April bis Mai |
| ![Märtyrer](../../results/timeline/charts/martyr.png) | „Märtyrer“: starke Spitze Ende Juni / Anfang Juli, am höchsten bei IRGC-nahen Kanälen (21,6 pro 1.000 Wörter) |
| ![Gegner](../../results/timeline/charts/labels_opponents.png) | Gegnerbegriffe am häufigsten im Januar (Proteste), vor allem IRGC-nah |
| ![Verhandlungen](../../results/timeline/charts/negotiations.png) | „Verhandlungen“: Spitzen Anfang Februar, Anfang April und Mitte Juni; Jamaran fast immer am höchsten |

Weitere Diagramme: [Waffenruhe](../../results/timeline/charts/ceasefire.png) ·
[Rache](../../results/timeline/charts/revenge.png) ·
[Verbrechen](../../results/timeline/charts/crimes.png) ·
[Trump](../../results/timeline/charts/trump.png) ·
[Ghalibaf](../../results/timeline/charts/ghalibaf.png) ·
[„Vereinigte Staaten“](../../results/timeline/charts/usa_united_states_share.png)

---

## 6. Aktivität und Reichweite (`10_activity.py`)

| | staatlich | IRGC-nah | Jamaran |
|---|---|---|---|
| Beiträge pro Tag und Kanal | 237 | 222 | 195 |
| Aufrufe pro Beitrag (Median) | 1.259 | **11.858** | 1.593 |
| Weiterleitungen pro Beitrag (Median) | 5 | **18** | 5 |
| Weiterleitungen pro 1.000 Aufrufe | **5,1** | 2,1 | 4,2 |

- **Aktivität:** Mit Kriegsbeginn verdoppeln bis verdreifachen sich die Beiträge (von etwa 130 auf 300–420 pro Tag und
  Kanal); zweite Spitze Anfang Juli.
- **Reichweite:** Tasnim und Fars erreichen rund zehnmal so viele Aufrufe pro Beitrag. Das hängt vor allem an der
  Zahl der Abonnenten, die nicht erhoben wurde – es beschreibt Reichweite, nicht Qualität.
- Mit Kriegsbeginn sinken die Aufrufe pro Beitrag in allen Gruppen, bei Jamaran von 3.329 auf 969 (Median), obwohl mehr
  gepostet wird. Mögliche Gründe – mehr Beiträge für dieselben Leser, eingeschränkter Internetzugang – lassen sich mit
  diesen Daten nicht trennen.
- **Weiterleitungen im Verhältnis:** Beiträge staatlicher Kanäle und Jamarans werden pro Aufruf etwa doppelt so oft
  weitergeleitet wie die IRGC-naher Kanäle.

![Beiträge pro Tag](../../results/activity/charts/posts_per_day.png)

Weitere Diagramme: [Aufrufe](../../results/activity/charts/views_median.png) ·
[Weiterleitungen pro 1.000 Aufrufe](../../results/activity/charts/forwards_per_1000_views.png)

---

## 7. Grenzen

- **Zählen ist nicht Verstehen.** Die Zählung erkennt keinen Zusammenhang: Verneinung, Zitat oder Ironie zählen gleich.
  Ob ein Begriff zustimmend oder distanziert verwendet wird, zeigt erst die KI-Einordnung oder das Lesen.
- **Setzungen des Autors:** Korrekturliste, Benennungsliste, Phasen- und Ereignisdaten. Sie sind offen dokumentiert;
  andere Setzungen ergäben leicht andere Zahlen.
- **Regeln mit Stichproben geprüft,** nicht jeder Beitrag gelesen (Führer-Zuordnung, Bereinigung).
- **Unterschiedliche Kanalprofile:** Staatliche Kanäle veröffentlichen viel Service und Verwaltung, dadurch sinkt ihr
  Anteil politischer Begriffe pro 1.000 Wörter.
- **Aufrufe und Weiterleitungen** sind der Stand zum Zeitpunkt der Sammlung; Abonnentenzahlen fehlen.
- **Keine Netzwerkanalyse:** Bei der Sammlung wurde für weitergeleitete Beiträge nur der Absendername gespeichert, der bei
  Kanälen meist leer ist (96 von 328.330 Beiträgen). Wer wen weiterleitet, lässt sich deshalb nicht auswerten.
- **Lücken im Januar:** IRNA und Jamaran posteten Mitte Januar kaum (Internetsperre in Iran, siehe [01](01_datenerhebung.md)).
- Die Gruppe „reformorientiert“ besteht aus **einem Kanal**.

---

## 8. Dateien

| Skript | Aufgabe | Ergebnis (`results/`) |
|---|---|---|
| `scripts/analysis/01_word_frequency.py` | häufigste Einzelwörter | `words/word_frequency.*` |
| `scripts/analysis/02_word_pairs.py` | Wortpaare (Zwischenschritt) | – |
| `scripts/analysis/03_terms.py` | feste Begriffe, jede Stelle einmal gezählt | `words/phrases.csv`, `words/terms.*` |
| `scripts/analysis/03b_terms_long.py` | Test mit bis zu 8 Wörtern | – |
| `scripts/analysis/04_context.py` | Nachbarwörter und Beispiele (Terminal) | – |
| `scripts/analysis/05_noise_candidates.py` | Vorschläge für die `ignore`-Liste | – |
| `scripts/analysis/06_leader_mentions.py` | Ali oder Mojtaba Khamenei | `leader/leader_mentions.*` |
| `scripts/analysis/07_typical_terms.py` | typische Begriffe (Log-Odds) | `words/typical_terms.*` |
| `scripts/analysis/08_naming.py` | Benennungen, Nachbarwörter | `naming/naming.*`, `naming/neighbours.csv` |
| `scripts/analysis/09_timeline.py` | Verlauf pro Woche, Diagramme | `timeline/timeline.*`, `timeline/charts/` |
| `scripts/analysis/10_activity.py` | Aktivität und Reichweite | `activity/*`, `activity/charts/` |
| `scripts/analysis/phrase_corrections.csv` | Korrekturliste des Autors | – |
| `scripts/analysis/naming_terms.csv` | Liste der Benennungen | – |

Reihenfolge: `03` → `07` → `06` → `08` → `09` → `10`. Technik: Python 3.11, `pandas`, `numpy`, `matplotlib`,
`SQLAlchemy`. Beschreibung aller Ergebnisdateien: [results/README.md](../../results/README.md).
