# 01 – Datenerhebung

[← zurück zur Übersicht](../README.md)

Dieser Schritt beschreibt, wie die Rohdaten gesammelt und auf Vollständigkeit geprüft wurden.
Rohdaten und Quellenliste sind nicht Teil des Repositorys.

---

## Überblick

| | Messenger-Kanäle | Nachrichten-Webarchiv |
|---|---|---|
| Zugang | offizielle Messenger-API | öffentliche Artikelseiten |
| Werkzeug | Python, `Telethon` | Python, `requests`, `BeautifulSoup` |
| Umfang | 5 öffentliche Kanäle, 281.057 Beiträge | 1 Quelle, 5.319 Artikel im Zeitraum |
| Zeitraum | 01.01.–31.08.2026 | 01.01.–31.08.2026 |
| Status | abgeschlossen | abgeschlossen |

Die Quellen werden anonymisiert als **A–F** bezeichnet und in **zwei Quellengruppen** eingeteilt:

| Gruppe | Quellen | Art |
|---|---|---|
| 1 | A, B, C | Messenger-Kanäle |
| 2 | D, E | Messenger-Kanäle |
| 2 | F | Nachrichten-Webarchiv |

Quelle F gehört zu Gruppe 2. Ihr Messenger-Kanal war in Deutschland nicht abrufbar;
die Inhalte wurden deshalb über das öffentliche Webarchiv der Quelle erhoben.

---

## 1. Messenger-Kanäle

### Vorgehen
- Zugriff über die **offizielle API** mit eigenem Entwicklerzugang (API-ID/-Hash)
- Nur **öffentliche Kanäle** redaktioneller Medien – keine Gruppen, keine privaten Nutzer, kein Beitritt zu Kanälen nötig
- Anmeldung einmalig per QR-Code; die Sitzungsdatei bleibt lokal
- Beiträge werden rückwärts ab dem Enddatum gelesen, bis das Startdatum erreicht ist
- Automatische Pausen bei Ratenbegrenzung durch die API

### Erfasste Felder

| Feld | Bedeutung |
|---|---|
| `kanal`, `seite` | Quelle und Quellengruppe (in der Dokumentation anonymisiert als A–F / 1–2) |
| `id` | eindeutige Beitragsnummer im Kanal |
| `datum` | Veröffentlichungszeit (UTC) |
| `text` | Beitragstext (Persisch) |
| `views` | Aufrufe |
| `weiterleitungen` | wie oft weitergeleitet |
| `weitergeleitet_von` | Ursprung, falls der Beitrag selbst weitergeleitet wurde |

### Ergebnis
- **281.057 Beiträge** aus 5 Kanälen

| Quelle | A | B | C | D | E |
|---|---|---|---|---|---|
| Beiträge | 59.546 | 47.698 | 65.728 | 58.160 | 49.925 |
- Laufzeit der Sammlung: ca. 50 Minuten

---

## 2. Nachrichten-Webarchiv

### Vorgehen
- Artikel der Quelle haben **fortlaufende IDs** – der Zeitraum wurde über Stichproben auf einen ID-Bereich eingegrenzt
- Jede ID wird einzeln abgerufen; ausgelesen werden Titel, Datum, Kurztext und Volltext
- Datumsangaben im **persischen Sonnenkalender** werden in gregorianische Daten umgerechnet (`jdatetime`)
- **Testmodus** mit 5 IDs, um die Erkennung von Titel und Datum vor dem vollen Lauf zu prüfen
- Zufällige Pause von 1,5–3 Sekunden zwischen Anfragen, um den Server nicht zu belasten
- **Fortsetzungslogik:** Jede Zeile wird sofort gespeichert; nach einem Abbruch überspringt das Skript bereits erfasste IDs, fehlgeschlagene werden im nächsten Lauf nachgeholt

### Erfasste Felder
`id`, `url`, `titel`, `datum_roh` (Originaldatum), `datum` (umgerechnet), `lead` (Kurztext), `text` (Volltext)

### Ergebnis
- **5.456 Artikel** im abgerufenen ID-Bereich, davon **5.319 im Zeitraum 01.01.–31.08.2026**
  (Artikel davor und danach werden bei der Aufbereitung herausgefiltert)
- Ein zweiter Durchlauf holte 7 Artikel nach, die beim ersten Lauf an Verbindungsabbrüchen gescheitert waren
- 466 bis 885 Artikel pro Monat

---

## 3. Qualitätsprüfung

### Messenger-Kanäle
Ein eigenes Prüfskript kontrolliert die Messenger-Daten auf sieben Punkte und speichert einen Prüfbericht.

| Prüfung | Ergebnis |
|---|---|
| Zeilen je Kanal = Ausgabe der Sammlung | ✅ übereinstimmend |
| Zeitraum je Kanal vollständig | ✅ 01.01.–31.08. bei allen Kanälen |
| Doppelte Beiträge | ✅ 0 |
| Beiträge ohne Text | 11–27 % je Kanal (Bilder/Videos ohne Beschreibung) |
| Tage ohne Beiträge | ⚠️ Quelle A: 16 Tage im Januar ohne Beiträge |
| Beiträge pro Woche | Tabelle zur Erkennung von Einbrüchen |

### Umgang mit der Lücke
Für Quelle A wurde der Zeitraum mit einem separaten Skript **gezielt erneut abgefragt**.
Ergebnis: Die Beiträge fehlen auch direkt beim Anbieter – die Sammlung war vollständig, die Lücke liegt in der Quelle selbst.
Sie wird in der Analyse berücksichtigt (Vergleiche pro Tag statt absoluter Summen, Januar für Quelle A gesondert betrachtet).

### Webarchiv

| Prüfung | Ergebnis |
|---|---|
| Doppelte Artikel | ✅ 0 |
| Artikel ohne Datum | ✅ 0 – alle persischen Datumsangaben erfolgreich umgerechnet |
| Artikel ohne Text | ✅ 0 |
| Nicht abrufbare IDs | 45 von 5.501 (≈ 0,8 %) – auch im zweiten Durchlauf leer, also nicht vergebene oder gelöschte Artikelnummern |
| Tage ohne Artikel | 5 einzelne Tage, keine zusammenhängende Lücke |

### Erste Beobachtung aus der Wochentabelle
Die Veröffentlichungsaktivität verdoppelt bis verdreifacht sich bei vier von fünf Kanälen ab Ende Februar
und zeigt einen zweiten Anstieg Anfang Juli. Quelle A folgt diesem Muster kaum. → Details in [04 – Analyse](04_analyse.md).

---

## 4. Sicherheit und Datenschutz

- API-Zugangsdaten nur als **Umgebungsvariablen**, nie im Code
- Sitzungsdatei, Rohdaten und CSV-Dateien per `.gitignore` vom Repository ausgeschlossen
- Nur redaktionelle Veröffentlichungen, **keine personenbezogenen Daten** von Nutzern
- Alle Daten werden ausschließlich lokal gespeichert und verarbeitet

---

## 5. Technische Umgebung

- Linux (Arch), conda-Umgebung mit Python 3.11
- Bibliotheken: `telethon`, `requests`, `beautifulsoup4`, `jdatetime`, `pandas`, `qrcode`

### Projektstruktur (Ausschnitt)
```
projekt/
├── data/
│   ├── row/        ← Rohdaten + Prüfberichte (nicht im Repo)
│   └── ki/         ← Ergebnisse der KI-Einordnung (nicht im Repo)
└── scripts/
    ├── telegram/   ← Login, Sammlung, Nachsammlung, Prüfung
    ├── web/        ← Webarchiv-Sammlung
    └── ai/         ← KI-Einordnung (siehe 03)
```
