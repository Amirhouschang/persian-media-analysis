[English](../en/06_methodology.md) | **Deutsch**

# 06 – Methodik, Grenzen und Sicherheit

[← zurück zur Übersicht](../../README.de.md)

Diese Seite fasst zusammen, wie die Ergebnisse zustande kamen, welche Entscheidungen der Autor gesetzt hat, was die
Ergebnisse nicht aussagen und wie Daten und Zugangsdaten geschützt wurden. Einzelheiten stehen in
[01](01_datenerhebung.md) bis [04](04_analyse.md).

> **Einordnung:** Das Projekt ist vor allem technisch und liefert einen belastbaren Überblick, keine wissenschaftliche
> Tiefenanalyse. Eine solche Studie würde die Beiträge einzeln lesen und deuten und 100 Seiten oder mehr umfassen.

---

## 1. Verfahren im Überblick

| Schritt | Verfahren | Dokument |
|---|---|---|
| Quellen | 6 öffentliche Telegram-Kanäle in drei Gruppen (staatlich: IRNA, IRIB News, Mehr News · IRGC-nah: Tasnim News, Fars News · reformorientiert: Jamaran), 01.01.–31.08.2026 | [01](01_datenerhebung.md) |
| Erhebung | offizielle Telegram-API (`Telethon`), 328.330 Beiträge, Prüfung auf sieben Punkte | [01](01_datenerhebung.md) |
| Aufbereitung | PostgreSQL-Datenbank `iran_media_2026`; persischer Text bereinigt, der Originaltext bleibt unverändert | [02](02_aufbereitung.md) |
| Zählung | 1.501 feste Begriffe (1.490 ohne vorgegebene Wortliste gefunden, 11 vom Autor ergänzt); Benennungsliste mit 113 Begriffen in 188 Schreibweisen; Einheit: Nennungen pro 1.000 Wörter | [04, Abschnitt 10](04_analyse.md#10-methode) |
| Gruppenvergleich | gewichtetes Log-Odds-Verhältnis mit z-Wert (über 1,96 statistisch deutlich); ein Begriff zählt für eine Gruppe nur, wenn jeder ihrer Kanäle ihn häufiger verwendet | [04, Abschnitt 10](04_analyse.md#10-methode) |
| KI-Themen | Gemma 4 31B lokal, Codebuch v8, 10.750 Beiträge, gewichtet auf 231.406 Beiträge mit mehr als 80 Zeichen; an 200 neuen Beiträgen blind geprüft | [03](03_ki_einordnung.md) |
| Ton | von der KI eingeordnet und gegen manuelle Kodierung geprüft, aber nicht für Gruppenvergleiche verwendet (Kappa 0,46) | [03, Abschnitt 8](03_ki_einordnung.md#8-endvalidierung-phase-c--ergebnis) |
| Darstellung | Ergebnisbericht, Diagramme und zweisprachiges Dashboard; sie zeigen nur Zahlen | [Bericht](bericht.md) |

---

## 2. Setzungen des Autors

Diese Entscheidungen liegen offen in Dateien. Andere Setzungen ergäben leicht andere Zahlen.

| Setzung | Inhalt | Datei |
|---|---|---|
| Quellenauswahl und Gruppen | 6 Kanäle in 3 Gruppen; Kanalbeschreibungen neutral formuliert („weithin als IRGC-nah beschrieben“) | `README.de.md`, `02_load_database.py` |
| Phasen | vor dem Krieg 01.01.–27.02. · Krieg 28.02.–07.04. · Waffenruhe 08.04.–06.07. · nach dem Zusammenbruch 07.07.–31.08. | `02_load_database.py` |
| Ereignisdaten | Tod Ali Khameneis offiziell bestätigt 01.03.; Wahl Mojtaba Khameneis 08.03. | `06_leader_mentions.py` |
| Korrekturliste | 347 Einträge: 12 Amtsbezeichnungen, 11 lange Namen, 5 Entfernungen, 56 Zusammenführungen, 263 ignorierte Begriffe | `phrase_corrections.csv` |
| Benennungsliste | 113 Begriffe, 188 Schreibweisen, 10 Kategorien | `naming_terms.csv` |
| Schwellen | Begriff mit mindestens 100 Vorkommen; typische Begriffe ab Mindesthäufigkeit 50 (Länder: 20); z-Wert über 1,96 | [04](04_analyse.md#10-methode) |
| Codebuch v8 | 9 Themen, 6 Töne, Regeln – z. B.: rechtliche und beschreibende Begriffe zu den Kriegen machen einen Text nicht automatisch anklagend (gilt für alle Quellen gleich); im Zweifel *neutral* | `codebook.py` |
| Hintergrundtext | neutral formulierte Zeitleiste, Akteure, Glossar; Völkerrecht für alle Staaten gleich formuliert | `background.txt` |
| KI-Stichprobe | 50 Beiträge pro Kanal und Woche, nur Beiträge mit mehr als 80 Zeichen | [03, Abschnitt 7](03_ki_einordnung.md#7-hauptlauf) |

---

## 3. Datenqualität und Lücken

| Prüfung (Einzelheiten in [01](01_datenerhebung.md)) | Ergebnis |
|---|---|
| Zeilen je Kanal, Zeitraum, Duplikate | übereinstimmend; Zeitraum bei allen Kanälen vollständig; 0 Duplikate |
| Beiträge ohne Text | 11–27 % je Kanal (Bilder oder Videos ohne Beschreibung); 267.548 von 328.330 Beiträgen enthalten Text |
| Tage ohne Beiträge | IRNA 16 Tage (09.–22.01. und 16.–17.03.), Jamaran 6 Tage (09.–14.01.), alle anderen Kanäle keine |

- **Januar-Lücken:** IRNA wurde gezielt erneut abgefragt; die Beiträge fehlen auch direkt auf Telegram. Die Lücken bei IRNA
  und Jamaran fallen in die Zeit der Internetsperre. Für den 16.–17.03. nennt die Dokumentation keine Ursache.
- **Zeitzone:** Telegram liefert UTC; Iran liegt bei UTC+3:30. Beiträge zwischen 20:30 und 24:00 UTC gehören nach Teheraner
  Zeit schon zum Folgetag.
  - **Regel:** Tage, Wochen und Phasen der Datenbank und aller darauf beruhenden Auswertungen (Begriffe, Zeitverlauf,
    Aktivität) folgen dem UTC-Datum; auch die Gewichte der KI-Stichprobe beruhen auf UTC-Wochen.
  - **Ausnahme:** Nur die KI-Themenanteile pro Phase (`03e_topics.py`) verwenden das Teheraner Datum. Dort endet die
    Waffenruhe am 07.07. und die Folgephase beginnt am 08.07. (Datenbank: 06.07. und 07.07.).
  - **Auswirkung:** Betroffen sind nur Beiträge an Tages-, Wochen- und Phasengrenzen. Für die KI-Themenanteile nachgerechnet:
    Nach dem UTC-Datum statt nach dem Teheraner Datum fielen 48 von 10.750 Beiträgen (davon 37 an der Grenze
    Waffenruhe/Zusammenbruch) in eine andere Phase. Die Themenanteile der Gruppen änderten sich um höchstens 1,5
    Prozentpunkte (2 von 108 Werten über 1 Punkt), die der Einzelkanäle um höchstens 2,1 (4 von 216 Werten über 1 Punkt).
    Für die übrigen Auswertungen wurde das Ausmaß nicht beziffert.
  - **Diagramme:** Die Ereignislinie „Zusammenbruch der Waffenruhe“ steht am 08.07.
- **Stand der Daten:** Texte, Aufrufe und Weiterleitungen entsprechen dem Zeitpunkt der Sammlung; was vorher gelöscht
  wurde, fehlt. Beiträge aus den letzten Tagen vor der Sammlung hatten weniger Zeit, Aufrufe zu sammeln. Die erste (ab
  01.01.) und die letzte Woche (nur 31.08.) sind unvollständig und fehlen in den Wochendiagrammen.
- **Weiterleitungen:** Gespeichert ist nur der Absendername, der bei Kanälen meist leer ist. Eine Netzwerkanalyse („wer
  leitet wen weiter“) ist deshalb nicht möglich.
- **Sepah News:** Das Webarchiv (rund 5.300 Artikel) wurde erhoben, wird aber nicht ausgewertet: Lange Webartikel ohne
  Aufrufzahlen sind mit Telegram-Beiträgen nicht vergleichbar, und die lokale KI-Auswertung langer Texte erfordert einen
  deutlich höheren Rechenaufwand. Der Telegram-Kanal war aus Deutschland nicht abrufbar.
- **Bereinigung:** Die Regeln wurden mit Stichproben und SQL-Prüfungen kontrolliert, nicht durch Lesen aller Beiträge
  ([02](02_aufbereitung.md)).

---

## 4. Grenzen der Aussagen

| Grenze | Folge für die Lesart |
|---|---|
| **Zählen ist nicht Verstehen** | Ein Begriff zählt gleich, ob er zustimmend, distanziert, verneinend oder zitierend verwendet wird. |
| **Auswahl** | Sechs Kanäle auf Telegram; keine Oppositions- und Exilmedien, keine anderen Plattformen. Die Ergebnisse gelten für diese Kanäle, nicht für „die iranischen Medien“. |
| **Gruppe „reformorientiert“** | Sie besteht aus einem Kanal (Jamaran). Aussagen über diese Gruppe sind Aussagen über Jamaran. |
| **Spitzenwochen** | Die typischen Begriffe beschreiben die ganze Woche, nicht nur die Beiträge mit dem gezählten Wort. Die Zuordnung zu Ereignissen ist eine Deutung; bei einer Spitze (Verbrechensbegriffe, IRGC-nah, Woche ab 20.07.) ist kein einzelnes Ereignis erkennbar. |
| **Reichweite** | Aufrufe zählen Leser des Kanals, nicht eindeutige Personen; sie beschreiben Reichweite, nicht Qualität. Abonnentenzahlen fehlen; die Unterschiede bei den Aufrufen hängen vermutlich vor allem an der Zahl der Abonnenten. |
| **Länder** | `عمان` heißt Oman und Amman; `آذربایجان` allein zählt als Republik Aserbaidschan, meint aber manchmal iranische Provinzen (Wert zu hoch); Ägypten fehlt, weil `مصر` auch „beharrlich“ heißt; ein Teil der Nennungen europäischer Länder, der Türkei und Katars betrifft Sport. |
| **KI-Themen** | Thema in 72,5 % der Fälle richtig (95-%-Intervall 65,9–78,2 %). Militär wird eher überschätzt, Diplomatie eher unterschätzt; Veränderungen über die Zeit sind verlässlicher als die Höhe der Anteile. Bei Jamaran war die Zuordnung am unsichersten (55,9 % richtig, 34 geprüfte Beiträge). Der Stichprobenfehler der Anteile (ohne Fehler der KI-Zuordnung) beträgt pro Kanal etwa ±2,5 Prozentpunkte, pro Kanal und Monat etwa ±6. |
| **KI-Ton** | Die KI stufte nur 18 von 40 nicht-neutralen Beiträgen als nicht-neutral ein (genau derselbe Ton bei 14) und übersah sie je Gruppe verschieden oft (nicht-neutral manuell/KI: staatlich 20 %/8 %, IRGC-nah 21 %/18 %, Jamaran 18 %/9 %). Der Ton wird deshalb nicht verglichen. |
| **Referenz der KI-Prüfung** | Sie stammt von einer Person. In Phase A wurde sie mit Unterstützung eines KI-Assistenten (Claude) vorkodiert, vom Autor geprüft und nach Ansicht der KI-Ergebnisse angepasst; sie ist nicht vollständig blind entstanden. Die Werte des Testsets sind deshalb eher optimistisch, maßgeblich ist die Endvalidierung (200 neue, blind kodierte Beiträge). |
| **Hardware** | Ein Laptop ohne separate Grafikkarte begrenzt Modellgröße und Stichprobe; deshalb wird eine geschichtete Stichprobe eingeordnet, nicht das ganze Korpus. |

---

## 5. Neutralität und Umgang mit Begriffen

- Begriffe stehen so da, wie sie in den Quellen stehen – auch abwertende oder feindselige. Sie werden gezählt und
  berichtet, nicht bewertet und nicht übernommen. Sie beschreiben die Wortwahl der Kanäle, nicht die Meinung des Autors.
- Das Codebuch beschreibt sichtbare Merkmale im Text, keine Deutung. Die Regel zu rechtlichen und beschreibenden Begriffen
  („Völkermord“, „Aggression“, „illegaler Krieg“) gilt für alle Quellen gleich.
- Der Hintergrundtext für die KI und die Kanalbeschreibungen sind neutral formuliert; die Kanäle werden nicht bewertet.
- Das Dashboard zeigt keine Begriffstabellen mit Übersetzungen: Übersetzungen einzelner Begriffe sollten von mindestens
  zwei Personen geprüft werden, und die Begriffe mit Erklärung stehen in [04](04_analyse.md). Die Namen der Auswahlbegriffe
  im Dashboard (69 Begriffe der Wortanalyse, 35 Länder und Akteure) stehen in `dashboard/concepts.csv`.

---

## 6. Datenschutz, Urheberrecht und Sicherheit

**Daten**
- ausschließlich öffentliche Kanäle redaktioneller Medien; keine Gruppen, keine privaten Nutzer, keine Kommentare, keine
  personenbezogenen Daten von Nutzern
- Die Rohtexte sind aus urheberrechtlichen Gründen nicht Teil des Repositorys. Jeder Beitrag ist öffentlich über
  `t.me/<kanal>/<id>` auffindbar.
- `results/` und das Dashboard enthalten keine Beitragstexte, sondern Zahlen, Begriffe, Kategorien und Links zu den
  Beiträgen. Die Ergebnisdateien der KI enthalten zusätzlich die kurze Begründung der KI je Beitrag; sie kann einzelne
  Wendungen aus dem Beitrag wiedergeben. Prüfdateien mit Texten bleiben privat.
- Die Kanäle werden namentlich genannt; Code, Methode und Ergebnisse (auch der KI-Teil) sind öffentlich.

**Zugangsdaten**
- API-ID und API-Hash nur als Umgebungsvariablen (`TG_API_ID`, `TG_API_HASH`), nie im Code
- Die Sitzungsdatei `sitzung.session` ist die Anmeldung des Telegram-Kontos und gibt Zugriff darauf. Sie bleibt lokal und
  darf nie veröffentlicht werden.
- `.gitignore` schließt aus: Sitzungsdateien, `.env`, `data/` (Rohdaten und KI-Ausgaben), die Roh-CSV-Dateien der Sammlung,
  Datenbank-Sicherungen und `__pycache__`.

**Verarbeitung**
- Datenbank und KI-Einordnung der Beiträge laufen lokal (`Ollama`); die Texte werden dafür nicht an Cloud-Anbieter
  übertragen. Ausnahme: Die 150 Beiträge des Testsets 2 wurden in Phase A mit Unterstützung eines KI-Assistenten (Claude)
  vorkodiert ([03](03_ki_einordnung.md)).
- KI-Ergebnisse werden nicht ungeprüft übernommen, sondern an neuen, blind kodierten Beiträgen mit Konfidenzintervall
  validiert.

---

## 7. Nachvollziehbarkeit

- **Reihenfolge:** `scripts/telegram/` → `scripts/database/` → `scripts/ai/` → `scripts/analysis/` (`03` → `07` → `06` →
  `08` → `09` → `10` → `11` → `12`). Jede Ergebnisdatei in `results/` stammt aus einem Skript
  ([results/README.md](../../results/README.md)); die Auswertungen laufen über die Datenbank, die KI-Einordnung über die
  Rohdateien und `Ollama`. Eingaben von Hand (Korrekturliste, Benennungsliste, Codebuch, manuelle Kodierung) liegen als
  Dateien vor.
- **Datenbank:** Das Laden ist wiederholbar; die Zahl der Beiträge pro Kanal wird nach dem Laden gegen die Sammlung geprüft
  (328.330).
- **KI:** feste Modellversion, `temperature = 0`, `seed = 42`; zwei Läufe mit gleichem Modell und Codebuch ergaben exakt
  dasselbe Ergebnis. Die Codebuch-Version steht in den Dateinamen der Klassifikationen und Modellvergleiche, sodass Ergebnisse
  verschiedener Versionen sich nicht überschreiben. Der Modellvergleich und die ersten rund 2.800 Beiträge des Hauptlaufs
  liefen mit einer früheren Fassung von `background.txt`; danach wurden sechs Daten- und Preisangaben korrigiert, ohne
  Einfluss auf Kategorien oder Regeln. Der Hauptlauf brauchte 67 Stunden.
- **Gleichstand:** Haben mehrere Begriffe dieselbe Anzahl, ist ihre Reihenfolge nicht festgelegt. Ränge und die letzten Plätze der
  Top-Listen (Top 1.000 Begriffe, Top 20 Nachbarwörter, Top 15 Begriffe einer Spitzenwoche) können deshalb von Lauf zu Lauf
  wechseln; die Zählwerte selbst bleiben gleich. Ein vollständiger Neulauf aus den Rohdaten im Oktober 2026 hat alle Zählwerte
  reproduziert: Acht Ergebnisdateien waren byte-gleich, die übrigen unterschieden sich nur in der Reihenfolge bei Gleichstand.
- **Umgebung:** Linux, Python 3.11, PostgreSQL 18, Ollama; Pakete der Skripte: [requirements-scripts.txt](../../requirements-scripts.txt), des Dashboards: `dashboard/requirements.txt`.
- **Grenze:** Die Rohdaten sind nicht veröffentlicht. Wer die Auswertung wiederholen will, muss die Beiträge mit den
  Skripten neu sammeln; Aufrufe und Weiterleitungen sowie später gelöschte Beiträge können dann abweichen.
- **Unveröffentlicht:** Der Autor hat zum eigenen Verständnis weitere SQL-Abfragen ausgeführt. Sie und die zugehörigen Daten
  sind nicht auf GitHub, weil das Projekt schon sehr umfangreich ist. Veröffentlicht sind `03_example_queries.sql` und
  `05_check_cleaning.sql`.

---

## 8. Für belastbarere Ergebnisse (Vorschläge)

- **Mehrere Kodierer:** Zwei bis drei persische Muttersprachler (z. B. Iranisten) kodieren die Beiträge unabhängig; ihre
  Übereinstimmung untereinander und mit der KI wird gemessen. Das Codebuch stammt bisher aus der Sicht des Autors und
  sollte gemeinsam diskutiert werden.
- **Anpassung an andere Fragen:** Das Codebuch lässt sich für andere Fachrichtungen und Institutionen anpassen (z. B.
  Sicherheit, Politikwissenschaft, politische Interessen und Ideologie).
- **Zweiter Gutachter** für die Begriffslisten und die Übersetzung einzelner Begriffe.
- **Tiefenanalyse:** Beiträge einzeln lesen und deuten statt zählen; das wäre eine eigene Studie von 100 Seiten oder mehr.
- **Erweiterung der Quellen:** weitere Kanäle und Plattformen, Oppositions- und Exilmedien, das Webarchiv von Sepah News,
  Abonnentenzahlen.
- **Netzwerkanalyse:** setzt voraus, dass bei der Sammlung der Ursprung weitergeleiteter Beiträge vollständig gespeichert
  wird.
- **Ton:** Ein Vergleich zwischen Gruppen wäre erst nach einer besseren Validierung sinnvoll.

---

## 9. Weiterführende Dokumente

- [Ergebnisbericht](bericht.md)
- [01 – Datenerhebung](01_datenerhebung.md) · [02 – Aufbereitung](02_aufbereitung.md) ·
  [03 – KI-Einordnung](03_ki_einordnung.md) · [04 – Analyse](04_analyse.md)
- Ergebnisdateien: [results/README.md](../../results/README.md)
