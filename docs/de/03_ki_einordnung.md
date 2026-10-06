[English](../en/03_ai_classification.md) | **Deutsch**

# 03 – KI-Einordnung nach Thema und Ton

[← zurück zur Übersicht](../../README.de.md)

Diese Seite beschreibt, wie persischsprachige Telegram-Beiträge mit **lokal betriebenen Sprachmodellen**
nach **Thema** und **Ton** eingeordnet werden – und vor allem, wie das Verfahren entwickelt, geprüft und
verbessert wurde. Der Weg dahin war nicht geradlinig: Codebuch, Hintergrundwissen, Testdaten und
Modellauswahl wurden über acht Versionen weiterentwickelt. Auch Irrwege sind dokumentiert.

---

## Überblick

| | |
|---|---|
| Aufgabe | Jeder Beitrag erhält **ein Thema** (9 Kategorien) und **einen Ton** (6 Kategorien) |
| Technik | [Ollama](https://ollama.com) auf dem eigenen Rechner – die Einordnung läuft lokal; Ausnahme: Die Referenz von Testset 2 wurde mit einem KI-Assistenten vorkodiert (Abschnitt 5, Phase A) |
| Gewähltes Modell | **Gemma 4 31B** mit Hintergrundwissen |
| Codebuch | Version **v8** (eingefroren) |
| Testset (150 Beiträge, zur Entwicklung genutzt) | 80,7 % Thema und Ton exakt · 86,7 % mit Grenzfällen · Kappa Thema 0,85 / Ton 0,79 |
| **Endvalidierung (200 neue Beiträge)** | **Thema 72,5 %** (95-%-Intervall 65,9–78,2 %) · Ton 84,5 % · beides 62,5 % (55,6–68,9 %) · Kappa Thema 0,68 / Ton 0,46 |
| Hauptlauf | 10.750 Beiträge, geschichtete Stichprobe (50 pro Kanal und Woche), gewichtet |
| Verwendung | **Themen**: Anteile pro Gruppe und Phase ([04, Abschnitt 7](04_analyse.md#7-themen-laut-ki)) · **Ton**: nicht für Vergleiche zwischen Gruppen (Abschnitt 8) |
| Status | Hauptlauf ✅ · Endvalidierung (Phase C) ✅ |

---

## 1. Warum lokale KI?

- **Datenschutz und Unabhängigkeit:** Für die Einordnung werden die Texte nicht an Cloud-Anbieter übertragen (Ausnahme: die Vorkodierung der Referenz von Testset 2 mit einem KI-Assistenten, Abschnitt 5, Phase A).
- **Reproduzierbarkeit:** Feste Modellversion, `temperature = 0`, `seed = 42` – gleiche Eingabe ergibt gleiche Ausgabe.
  Das wurde geprüft: Zwei Läufe desselben Modells mit gleichem Codebuch ergaben exakt dasselbe Ergebnis.
- **Kosten:** keine laufenden Kosten, nur Rechenzeit.
- **Grenze:** Die Hardware bestimmt, welche Modelle möglich sind (siehe Abschnitt 5).

**Hardware:** Laptop mit AMD Ryzen AI 9 HX 370, 93 GB Arbeitsspeicher, integrierte Grafik Radeon 890M,
keine separate Grafikkarte. Betriebssystem Linux (Arch/EndeavourOS).

---

## 2. Das Codebuch

Das Codebuch (`scripts/ai/codebook.py`) legt fest, **was** die KI entscheiden soll. Grundprinzip:
Jede Kategorie beschreibt **sichtbare Merkmale im Text**, keine Deutung. Beispiel: *mournful* verlangt
ausdrückliche Trauersprache („mit tiefer Trauer“, „Beileid“) – ein Bericht über eine Beerdigung ohne
solche Worte ist *neutral*.

### Themen

| Kategorie | Kurzbeschreibung |
|---|---|
| `military` | Angriffe, Waffen, Truppen, militärische Aussagen; auch Kriegsereignisse in Israel, den Golfstaaten, Irak, Jordanien |
| `diplomacy` | Irans Beziehungen zu anderen Staaten und Organisationen, Verhandlungen, Vermittlung |
| `domestic_politics` | Handeln des iranischen Staates im Inland, Justiz, Festnahmen, öffentliche Dienste, innenpolitische Debatten |
| `economy` | Preise, Wechselkurse, Handel, Subventionen, Märkte |
| `ideology_propaganda` | Werbung für die Ideologie der Islamischen Republik, Parolen, Jahrestage |
| `mourning_commemoration` | Tod, Beerdigung, Trauer, Gedenken an Verstorbene |
| `resistance_axis` | Libanon/Hisbollah, Gaza, Huthis, irakische Milizen, Syrien – Iran nicht selbst handelnd |
| `foreign_affairs` | Ereignisse in anderen Ländern ohne Bezug zu Iran oder dem Krieg |
| `other` | Wetter, Sport, Kultur, Unfälle, zu wenig Text |

### Töne (Prüfreihenfolge – der erste, der klar zutrifft, gilt)

`threatening` → `accusatory` → `mobilizing` → `triumphant` → `mournful` → `neutral`

### Wichtige Regeln (Auszug)

- Thema **und** Ton richten sich nach der **Hauptaussage** (meist die Überschrift); ein einzelner Nebensatz entscheidet nicht.
- Standardbegriffe iranischer Medien („Märtyrer“, „zionistisches Regime“) entscheiden allein nicht über den Ton.
- **Rechtliche und beschreibende Begriffe** zu den Kriegen in Gaza, Libanon und Iran („Völkermord“, „Kriegsverbrechen“,
  „Aggression“, „illegaler Krieg“) – auch für getötete Zivilisten und Kinder – gelten als beschreibend und machen einen Text
  nicht automatisch *accusatory*. Diese Regel ist eine bewusste Setzung des Projekts; sie gilt für alle Quellen gleich.
- **Festnahmen und Prozesse:** Wer politische Gegner, Demonstranten, Journalisten oder Minderheiten (z. B. Kurden, Belutschen,
  Bahai) ohne rechtskräftiges Urteil als „Terroristen“, „Randalierer“, „Verräter“ oder „Spione“ bezeichnet, ist *accusatory*.
  Festnahmen von Mitgliedern von Organisationen auf den Terrorlisten von UN oder EU sind *neutral*.
- Im Zweifel zwischen einem Ton und *neutral* → *neutral*.
- Die Angabe der Quelle hilft beim Verstehen, darf aber **nicht** über Thema oder Ton entscheiden.

---

## 3. Kontext: Was die KI zusätzlich weiß

Lokale Modelle haben einen festen Wissensstand und keine Websuche. Ereignisse des Jahres 2026 kennen sie nicht.
Deshalb erhält die KI in der Variante „mit Kontext“ zusätzlich:

1. **Hintergrund** (`scripts/ai/background.txt`, neutral formuliert, recherchiert und belegt):
   - Zeitleiste 2026: Proteste im Januar, Verhandlungen, Kriegsbeginn am 28.02., Waffenruhen, Blockaden
   - getötete Amtsträger, wichtige lebende Akteure (Iran, USA, Israel, Vermittler)
   - Beziehungen und Rollen: Russland, China, Pakistan, Katar, Oman; Beteiligung der Golfstaaten
   - Grundbegriffe des Völkerrechts (Souveränität, humanitäres Völkerrecht, Kriegsverbrechen, Menschenrechte) – für alle Staaten gleich formuliert
   - **Glossar** persischer Begriffe (z. B. „رهبر شهید“ = der getötete Revolutionsführer, „قرار شبانه“ = nächtliche regierungsnahe Kundgebung)
2. **Quellenbeschreibung:** neutral, wer hinter jedem Kanal steht – z. B. IRNA als amtliche staatliche Agentur,
   Tasnim und Fars als weithin IRGC-nah beschriebene Agenturen, Jamaran als dem Reformlager zugeordnetes Portal.

Regel: Der Kontext dient **nur dem Verständnis** von Bezügen; er darf Thema oder Ton nicht allein bestimmen.

Der Modellvergleich und die ersten rund 2.800 Beiträge des Hauptlaufs liefen mit einer früheren Fassung von
`background.txt`; danach wurden sechs Daten- und Preisangaben korrigiert, ohne Einfluss auf Kategorien oder Regeln.

---

## 4. Wie geprüft wurde

**Referenz:** manuell kodierte Beiträge (Thema + Ton). Die KI-Antwort wird mit dieser Referenz verglichen.

**Kennzahlen:**
- **Übereinstimmung exakt** – Anteil der Beiträge, bei denen Thema und Ton genau übereinstimmen
- **Übereinstimmung mit Grenzfällen** – das KI-Thema zählt auch als richtig, wenn es dem vom Menschen festgelegten
  **Nebenthema** entspricht (nur bei echten Grenzfällen vergeben, 29 von 150 Beiträgen)
- **Cohens Kappa** – Übereinstimmung abzüglich Zufall (über 0,8 = fast vollständig, 0,6–0,8 = deutlich)
- Verwechslungstabelle, Begründung der KI bei jeder Abweichung, Sekunden pro Beitrag

**Werkzeug:** `scripts/ai/03a_model_comparison.py` erzeugt pro Durchlauf eine Excel-Datei mit den Blättern
`summary`, `side_by_side`, `disagreements`, `confusion`, `details`.

---

## 5. Der Weg: acht Versionen

### Phase 1 – Erste Tests (Codebuch v1–v3, 29 Beiträge)

- Testset aus 29 Beiträgen der ersten fünf Kanäle (IRNA, IRIB News, Mehr, Tasnim, Fars), manuell kodiert.
- Getestet: Gemma 4 (26B, 31B), Qwen 3.6 (27B), Qwen 2.5 (32B), Aya Expanse (32B) – jeweils **mit und ohne Kontext** (v3); Aya Expanse 8B nur in v1 und v2, dort noch ohne Kontextvergleich.
- **Erkenntnis 1:** Die ersten Kategorien beschrieben Deutungen („propagandistisch“). Nach Umstellung auf sichtbare Textmerkmale
  stieg die Übereinstimmung von Gemma 4 26B von 55 % (v1) auf 72 % (v3, ohne Kontext). Ein Teil des Anstiegs kommt aus der Referenz selbst:
  Zwischen v1 und v3 wurde die manuelle Kodierung bei 10 der 29 Beiträge korrigiert.
- **Erkenntnis 2:** Hintergrundwissen verbesserte bei den meisten Modellen die Themenzuordnung.
- Bestes Ergebnis (v3): Gemma 4 31B mit Kontext – Thema 97 %, Ton 86 %, beides 83 %.
- **Aber:** 29 Beiträge sind wenig, und das Codebuch war an genau diesen Beiträgen entwickelt worden. Die Zahl war zu optimistisch.

### Codebuch v4 – Quellen und schärfere Grenzen

- *military* eingeengt (Grußworte von Kommandeuren sind kein Militär), Jahrestage zu *ideology_propaganda*,
  Gedenken nur bei Fokus auf Verstorbene, innenpolitische Debatten zu *domestic_politics*.
- Neutrale Beschreibung jeder Quelle, mit der Regel, dass die Quelle nicht entscheiden darf.

### Phase A – Neues, größeres Testset (Codebuch v5–v6, 150 Beiträge)

- **Testset 2:** 150 Beiträge, 25 aus jedem der sechs Kanäle (jetzt mit Jamaran), zufällig gezogen, ohne Beiträge aus Testset 1.
- **Vorgehen bei der Referenz:** Die Beiträge wurden mit Unterstützung eines KI-Assistenten (Claude) vorkodiert und
  anschließend vom Autor Zeile für Zeile geprüft und korrigiert. Die Referenz ist damit **nicht vollständig blind**
  entstanden – ein Grund für die separate Endvalidierung (Phase C).
- **v5:** Ton nach Hauptaussage statt nach einzelnen Sätzen; neue Regel zu rechtlichen Begriffen.

| Codebuch v5 | Thema | Ton | Beides | Sek./Beitrag |
|---|---|---|---|---|
| Gemma 4 26B | 80,7 % | 84,0 % | 70,0 % | 3,2 |
| Gemma 4 31B | 78,7 % | 87,3 % | 69,3 % | 20,0 |

- **Analyse der Abweichungen:** In 24 Beiträgen waren sich beide Modelle einig, aber anders als die Referenz.
  Diese Fälle wurden einzeln geprüft. Ergebnis: teils lag die Referenz falsch, teils fehlten Regeln – vor allem
  für Kriegsereignisse im Ausland (Sirenen in Bahrain, Explosionen in Kuwait) und für Festnahmen politischer Gegner.
- **v6:** Kriegsereignisse in Israel, den Golfstaaten, Irak und Jordanien → *military*; Regel zu Festnahmen und
  Etiketten ohne Urteil; Regel zu rechtlichen Begriffen verschärft.

| Gemma 4 26B | Thema | Ton | Beides |
|---|---|---|---|
| v5 | 80,7 % | 84,0 % | 70,0 % |
| v6 | 85,3 % | 91,3 % | 80,0 % |

- **Ehrliche Einordnung des Anstiegs:** Etwa die Hälfte der +10 Punkte kam von der korrigierten Referenz
  (die alte v5-Ausgabe erreicht gegen die neue Referenz bereits 75,3 %), die andere Hälfte von den neuen Regeln.

### Irrweg 1 – Mehr Wissen hilft nicht automatisch

- Nach Analyse der Fehler wurde der Hintergrund um Glossar, Außenbeziehungen und Völkerrecht erweitert.
- Ergebnis: 78,0 % statt 80,0 % – 5 Beiträge besser, 8 schlechter, also Zufallsschwankung.
- Die veröffentlichten Dateien `model_comparison_v6_*.csv` sind dieser Lauf mit dem erweiterten Hintergrund (Thema 84,7 %, Ton 89,3 %, beides 78,0 %).
  Der frühere v6-Lauf (85,3 % / 91,3 % / 80,0 %) wurde dabei überschrieben und liegt nicht mehr als Datei vor.
- **Erkenntnis:** Das Wissen kam an (die KI erkannte nun z. B. regierungsnahe Kundgebungen), aber die verbleibenden
  Fehler lagen an **unscharfen Grenzen zwischen Kategorien**, nicht an fehlendem Wissen.
  Der erweiterte Hintergrund wurde trotzdem beibehalten, weil er für die ~10.750 Beiträge des Hauptlaufs inhaltlich nützlich ist.

### Irrweg 2 – Nebenthema durch die KI (v7)

- Idee: Die KI darf bei echten Grenzfällen ein zweites Thema angeben – mit sehr strenger Regel.
- Ergebnis: Die KI setzte trotzdem bei **38,7 %** der Beiträge ein Nebenthema. Die großzügige Kennzahl wäre dadurch
  künstlich gestiegen, und die Rechenzeit stieg um 0,4 Sekunden pro Beitrag.
- **Lösung (v8):** Die KI gibt nur ein Thema. Das Nebenthema legt **nur der Mensch** in der Referenz fest.
  So misst die Kennzahl „mit Grenzfällen“ fair, wie oft die KI eine vom Menschen als gleichwertig anerkannte Einordnung trifft.

### Endvergleich – alle Modelle mit Codebuch v8

| Modell | Beides exakt | Beides mit Grenzfällen | Kappa Thema | Kappa Ton | Sek./Beitrag (Median) |
|---|---|---|---|---|---|
| **Gemma 4 31B** | **80,7 %** | **86,7 %** | 0,85 | **0,79** | 16,8 |
| Gemma 4 26B | 78,0 % | 84,0 % | 0,82 | 0,64 | 4,4 |
| Qwen 3.6 27B | 75,3 % | 76,7 % | 0,85 | 0,39 | 15,0 |
| Qwen 3.6 35B (MoE) | 70,7 % | 76,0 % | 0,79 | 0,56 | 4,6 |
| Qwen 2.5 32B | 65,3 % | 68,7 % | 0,69 | 0,61 | 16,6 |
| Aya Expanse 32B | 58,7 % | 64,0 % | 0,66 | 0,43 | 17,5 |

- Alle Modelle mit Kontext; 150 Beiträge; Zeit als Median (ein Lauf wurde durch den Ruhezustand des Rechners unterbrochen, was den Mittelwert verfälscht).
- **gpt-oss 120B** konnte nicht getestet werden: Mit 66 GB brachte es den Arbeitsspeicher an die Grenze; das System beendete
  Programme zwangsweise und die Bildschirmanzeige stürzte ab. Für den Dauerbetrieb auf dieser Hardware ist es ungeeignet.

---

## 6. Entscheidung

**Gemma 4 31B mit Kontext, Codebuch v8.**

- Bei den Themen liegen die drei besten Modelle gleichauf; beim **Ton** ist Gemma 4 31B deutlich besser
  (93 % Übereinstimmung, Kappa 0,79 gegenüber 0,64 bei Gemma 4 26B). Der Ton ist eine Kernvariable der Framing-Analyse.
  Die Endvalidierung zeigte später, dass auch Gemma 4 31B nicht-neutrale Töne oft übersieht (Abschnitt 8).
- Nachteil: etwa viermal langsamer. Deshalb wird nicht das ganze Korpus, sondern eine **geschichtete Stichprobe** eingeordnet.

---

## 7. Hauptlauf

- **Stichprobe:** 50 Beiträge pro Kanal und Woche (Wochen mit weniger Beiträgen: alle), nur Beiträge mit mehr als 80 Zeichen.
  Insgesamt **10.750 Beiträge** aus 36 Wochen und 6 Kanälen (je 1.800; IRNA 1.750, weil IRNA in einer Woche
  der Internetsperre nichts veröffentlichte).
- **Gewichtung:** Jeder Beitrag erhält ein Gewicht = Beiträge der Kanal-Woche / gezogene Beiträge. Anteile pro Kanal
  werden gewichtet hochgerechnet, damit aktive Wochen nicht unterrepräsentiert sind. Zusammen stehen die 10.750
  Beiträge für 231.406 Beiträge mit mehr als 80 Zeichen.
- **Genauigkeit:** pro Kanal etwa ±2,5 Prozentpunkte, pro Kanal und Monat etwa ±6 Punkte.
- **Gleiche Einstellungen wie im Test** (Prompt, Modell, Parameter) – nur so gelten die gemessenen Werte.
- Rechenzeit 67 Stunden (Median 21 Sekunden pro Beitrag); Fortsetzung nach Abbruch, zufällige Reihenfolge.
- Alle übrigen Kennzahlen (Umfang, Reichweite, Begriffsdichte, Zeitreihen) beruhen auf dem **vollständigen Korpus**.

---

## 8. Endvalidierung (Phase C) – Ergebnis

**Vorgehen:** 200 neue Beiträge aus dem Hauptlauf (je Kanal 33–34), die weder im Testset waren noch vorher angesehen
wurden. Manuelle Kodierung **ohne Kenntnis der KI-Antwort**, erst danach Vergleich (`03c_validation.py`).
Nach Phase C wurde nichts mehr geändert.

**95-%-Konfidenzintervall:** 200 Beiträge sind eine Stichprobe. Das Intervall (nach Wilson) gibt an, in welchem
Bereich die wahre Übereinstimmung im ganzen Hauptlauf mit 95 % Sicherheit liegt.

| | Testset (150) | **Endvalidierung (200)** | 95-%-Intervall |
|---|---|---|---|
| Thema | 86,7 % | **72,5 %** | 65,9–78,2 % |
| Thema mit Grenzfällen | 93,3 % | 77,0 % | 70,7–82,3 % |
| Ton | 93,3 % | **84,5 %** | 78,8–88,9 % |
| Thema und Ton | 80,7 % | **62,5 %** | 55,6–68,9 % |
| Thema und Ton mit Grenzfällen | 86,7 % | 66,5 % | 59,7–72,7 % |
| Kappa Thema / Ton | 0,85 / 0,79 | **0,68 / 0,46** | |

- **Der Abstand ist echt:** Die Intervalle von Testset (73,6–86,2 %) und Endvalidierung überschneiden sich nicht.
  Das Codebuch wurde über acht Versionen am Testset verbessert und passt deshalb zu genau diesen Beiträgen.
  Die Endvalidierung zeigt den Wert für unbekannte Beiträge – dafür war sie geplant.

**Pro Kanal** (Thema und Ton; je 33–34 Beiträge, deshalb breite Intervalle):

| IRIB News | Fars News | IRNA | Mehr News | Jamaran | Tasnim News |
|---|---|---|---|---|---|
| 82,4 % | 72,7 % | 69,7 % | 51,5 % | 50,0 % | 48,5 % |

Beim Thema allein liegt Jamaran am niedrigsten (55,9 %, Intervall 39,5–71,1 %).

### Wo die KI beim Thema abweicht

| Kategorie | von der KI richtig erkannt | Richtung der Fehler |
|---|---|---|
| mourning_commemoration | 12 von 12 | – |
| military | 19 von 21 | die KI vergibt *military* zu oft: 32-mal statt 21-mal |
| foreign_affairs | 16 von 18 | – |
| economy | 10 von 13 | – |
| domestic_politics | 26 von 37 | – |
| other | 31 von 49 | die KI wählt lieber ein Sachthema (*mourning*, *domestic_politics*) |
| **diplomacy** | **17 von 31** | 10-mal *military* |

- **Diplomatie → Militär:** Fast alles Analysen des Krieges („US-Experte: Iran im Vorteil“, Analysen von CNN oder der
  Financial Times). Die Referenz sah Diplomatie, die KI Militär; bei 4 der 10 war Militär oder Sonstiges als Nebenthema
  vermerkt – echte Grenzfälle.
- **Folge:** Der Anteil *military* wird überschätzt, *diplomacy* unterschätzt. Da das in allen Phasen ähnlich
  geschieht, sind Veränderungen über die Zeit verlässlicher als die absoluten Anteile.

### Ton: die KI ist zu vorsichtig – und das je Gruppe verschieden

- Von 40 Beiträgen mit nicht-neutralem Ton stuft die KI nur **18 (45 %)** als nicht-neutral ein und vergibt bei **14 (35 %)**
  genau denselben Ton; am häufigsten übersehen: *accusatory* (10-mal *neutral*). Vergibt die KI einen nicht-neutralen Ton
  (23-mal), ist der Beitrag in 18 Fällen auch manuell nicht-neutral, in 14 Fällen stimmt der Ton genau.
- Die hohe Übereinstimmung beim Ton (84,5 %) kommt vor allem daher, dass 80 % der Beiträge neutral sind. Kappa 0,46
  zeigt, dass die seltenen Töne nur mäßig erkannt werden.

| Anteil nicht-neutral | manuell | KI |
|---|---|---|
| staatlich (100 Beiträge) | 20 % | **8 %** |
| IRGC-nah (66) | 21 % | 18 % |
| Jamaran (34) | 18 % | 9 % |

Nach der manuellen Kodierung haben alle drei Gruppen gleich oft einen nicht-neutralen Ton. Die KI würde IRGC-nahe
Kanäle doppelt so oft als nicht neutral zeigen wie staatliche – **ein Unterschied, den es in der Referenz nicht gibt.**

### Entscheidung

- **Themen werden verwendet:** gewichtete Anteile pro Gruppe und Phase, mit Trefferquote und der bekannten Richtung der
  Fehler ([04, Abschnitt 7](04_analyse.md#7-themen-laut-ki)).
- **Der Ton wird nicht für Vergleiche zwischen Gruppen verwendet.** Die Sprache der Gruppen (Rache, Verbrechen,
  Gegnerbegriffe, Benennungen) misst die Wortanalyse in [04](04_analyse.md) am vollständigen Korpus.
- Das Ergebnis wird so berichtet, wie es ausfiel; Codebuch und Modell blieben unverändert.

---

## 9. Grenzen

- **Kategorien überschneiden sich.** Bei einem Teil der Beiträge waren auch bei der manuellen Kodierung mehrere
  Einordnungen vertretbar (z. B. eine Kundgebung zur Unterstützung der Armee: Innenpolitik, Ideologie oder Militär).
  Abweichungen zwischen KI und Referenz liegen überwiegend in diesen Grenzfällen.
- **Ein Kodierer.** Die Referenz stammt von einer Person (mit KI-Vorkodierung in Phase A). Eine zweite unabhängige
  Kodierung würde die Aussagekraft erhöhen.
- **Referenz nach Ansicht der KI-Ergebnisse angepasst** (Phase A). Die Werte aus Testset 2 sind deshalb eher
  optimistisch; maßgeblich ist Phase C.
- **Hardware** begrenzt Modellgröße und Stichprobe.
- **Setzung zu rechtlichen Begriffen** (Regel 8) beeinflusst die Häufigkeit von *accusatory*; sie ist offen dokumentiert.
  Zusammen mit „im Zweifel *neutral*“ trägt sie vermutlich dazu bei, dass die KI nicht-neutrale Töne übersieht.
- **Validierung pro Kanal** beruht auf je 33–34 Beiträgen; Unterschiede zwischen Kanälen sind deshalb unsicher.

---

## 10. Was ich gelernt habe

1. **Definitionen schlagen Modellgröße.** Die größten Sprünge kamen von klareren Regeln, nicht von größeren Modellen.
2. **Kleine Testsets täuschen.** 83 % an 29 Beiträgen wurden an 150 neuen Beiträgen zu 69 % (Gemma 4 31B, v3 → v5).
3. **Übereinstimmung ist nicht Wahrheit.** Wenn KI und Mensch abweichen, liegt der Fehler nicht immer bei der KI.
4. **Jede Anpassung am selben Testset schönt die Zahl.** Deshalb: einfrieren, dann an unbekannten Daten messen.
5. **Hardware ist Teil der Methode.** Laufzeit, Arbeitsspeicher und Ruhezustand müssen eingeplant werden.
6. **Die ehrliche Zahl kommt zuletzt.** 80,7 % am Testset wurden an 200 neuen Beiträgen zu 62,5 % – und erst die
   Endvalidierung zeigte, dass die Fehler beim Ton nicht zufällig, sondern je Gruppe verschieden sind.

---

## 11. Technische Umsetzung

| Datei | Aufgabe |
|---|---|
| `scripts/ai/ai_config.py` | alle Einstellungen: Modelle, Stichprobe, Pfade |
| `scripts/ai/codebook.py` | Kategorien, Definitionen, Regeln, Quellenbeschreibungen, Versionsnummer |
| `scripts/ai/background.txt` | Hintergrundwissen und Glossar |
| `scripts/ai/ai_core.py` | Prompt bauen, Anfrage an Ollama, Antwort prüfen |
| `scripts/ai/03a_model_comparison.py` | Testset ziehen, Modelle vergleichen, Excel-Auswertung |
| `scripts/ai/03_ai_classify.py` | Hauptlauf mit geschichteter Stichprobe und Gewichten |
| `scripts/ai/03c_validation.py` | Endvalidierung: 200 Beiträge ziehen, mit der KI vergleichen, Konfidenzintervalle |
| `scripts/ai/03d_export_results.py` | Ergebnisse ohne Beitragstexte nach `results/ai/` exportieren |
| `scripts/ai/03e_topics.py` | gewichtete Themenanteile pro Gruppe, Kanal und Phase, Diagramm |

**Einstellungen:** `temperature 0`, `seed 42`, `num_ctx 8192`, JSON-Ausgabe erzwungen, Denkmodus aus,
maximal 2.000 Zeichen pro Beitrag, ein Wiederholungsversuch bei ungültiger Antwort.
Die Codebuch-Version steht in jedem Dateinamen – Ergebnisse verschiedener Versionen überschreiben sich nie.
