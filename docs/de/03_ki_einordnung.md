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
| Technik | [Ollama](https://ollama.com) auf dem eigenen Rechner – keine Cloud, keine Daten verlassen den Laptop |
| Gewähltes Modell | **Gemma 4 31B** mit Hintergrundwissen |
| Codebuch | Version **v8** (eingefroren) |
| Übereinstimmung mit manueller Kodierung | **80,7 %** Thema und Ton exakt · **86,7 %** unter Berücksichtigung von Grenzfällen · Kappa Thema 0,85 / Ton 0,79 |
| Hauptlauf | geschichtete Stichprobe, ca. 10.500 Beiträge (50 pro Kanal und Woche) |
| Status | Hauptlauf ⏳ · Endvalidierung (Phase C) ⬜ |

---

## 1. Warum lokale KI?

- **Datenschutz und Unabhängigkeit:** Die Texte werden nicht an Cloud-Anbieter übertragen.
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
- Getestet: Gemma 4 (26B, 31B), Qwen 3.6 (27B), Qwen 2.5 (32B), Aya Expanse (8B, 32B) – jeweils **mit und ohne Kontext**.
- **Erkenntnis 1:** Die ersten Kategorien beschrieben Deutungen („propagandistisch“). Nach Umstellung auf sichtbare Textmerkmale
  stieg die Übereinstimmung von Gemma 4 26B von 55 % auf 72 %.
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
- **Erkenntnis:** Das Wissen kam an (die KI erkannte nun z. B. regierungsnahe Kundgebungen), aber die verbleibenden
  Fehler lagen an **unscharfen Grenzen zwischen Kategorien**, nicht an fehlendem Wissen.
  Der erweiterte Hintergrund wurde trotzdem beibehalten, weil er für die ~10.500 Beiträge des Hauptlaufs inhaltlich nützlich ist.

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
- Nachteil: etwa viermal langsamer. Deshalb wird nicht das ganze Korpus, sondern eine **geschichtete Stichprobe** eingeordnet.

---

## 7. Hauptlauf

- **Stichprobe:** 50 Beiträge pro Kanal und Woche (Wochen mit weniger Beiträgen: alle), nur Beiträge mit mehr als 80 Zeichen.
  Insgesamt ca. **10.500 Beiträge** aus 36 Wochen und 6 Kanälen.
- **Gewichtung:** Jeder Beitrag erhält ein Gewicht = Beiträge der Kanal-Woche / gezogene Beiträge. Anteile pro Kanal
  werden gewichtet hochgerechnet, damit aktive Wochen nicht unterrepräsentiert sind.
- **Genauigkeit:** pro Kanal etwa ±2,5 Prozentpunkte, pro Kanal und Monat etwa ±6 Punkte.
- **Gleiche Einstellungen wie im Test** (Prompt, Modell, Parameter) – nur so gelten die gemessenen Werte.
- Laufzeit ca. 2 Tage; Fortsetzung nach Abbruch, zufällige Reihenfolge.
- Alle übrigen Kennzahlen (Umfang, Reichweite, Begriffsdichte, Zeitreihen) beruhen auf dem **vollständigen Korpus**.

---

## 8. Endvalidierung (Phase C) – geplant

- 200 neue Beiträge aus dem Hauptlauf, die weder im Testset waren noch vorher angesehen wurden.
- Manuelle Kodierung **ohne Kenntnis der KI-Antwort**, erst danach Vergleich.
- **Nach Phase C wird nichts mehr geändert.** Das Ergebnis wird so berichtet, wie es ausfällt – auch pro Kanal,
  um zu prüfen, ob Fehler eine Quellengruppe stärker treffen als eine andere.

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

---

## 10. Was ich gelernt habe

1. **Definitionen schlagen Modellgröße.** Die größten Sprünge kamen von klareren Regeln, nicht von größeren Modellen.
2. **Kleine Testsets täuschen.** 83 % an 29 Beiträgen wurden an 150 neuen Beiträgen zu 70 %.
3. **Übereinstimmung ist nicht Wahrheit.** Wenn KI und Mensch abweichen, liegt der Fehler nicht immer bei der KI.
4. **Jede Anpassung am selben Testset schönt die Zahl.** Deshalb: einfrieren, dann an unbekannten Daten messen.
5. **Hardware ist Teil der Methode.** Laufzeit, Arbeitsspeicher und Ruhezustand müssen eingeplant werden.

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

**Einstellungen:** `temperature 0`, `seed 42`, `num_ctx 8192`, JSON-Ausgabe erzwungen, Denkmodus aus,
maximal 2.000 Zeichen pro Beitrag, ein Wiederholungsversuch bei ungültiger Antwort.
Die Codebuch-Version steht in jedem Dateinamen – Ergebnisse verschiedener Versionen überschreiben sich nie.
