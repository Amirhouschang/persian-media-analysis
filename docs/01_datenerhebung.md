# 01 – Datenerhebung

[← zurück zur Übersicht](../README.md)

Dieser Schritt beschreibt, wie die Rohdaten gesammelt und auf Vollständigkeit geprüft wurden.
Rohdaten und Quellenliste sind nicht Teil des Repositorys.

---

## Überblick

| | |
|---|---|
| Zugang | offizielle Messenger-API |
| Werkzeug | Python, `Telethon` |
| Umfang | 6 öffentliche Kanäle, 328.330 Beiträge |
| Zeitraum | 01.01.–31.08.2026 |
| Status | abgeschlossen |

Die Quellen werden anonymisiert als **A–F** bezeichnet und in **drei Quellengruppen** eingeteilt:

| Gruppe | Quellen |
|---|---|
| 1 | A, B, C |
| 2 | D, E |
| 3 | F |

---

## 1. Vorgehen

- Zugriff über die **offizielle API** mit eigenem Entwicklerzugang (API-ID/-Hash)
- Nur **öffentliche Kanäle** redaktioneller Medien – keine Gruppen, keine privaten Nutzer, kein Beitritt zu Kanälen nötig
- Anmeldung einmalig per QR-Code; die Sitzungsdatei bleibt lokal
- Beiträge werden rückwärts ab dem Enddatum gelesen, bis das Startdatum erreicht ist
- Automatische Pausen bei Ratenbegrenzung durch die API
- Später ergänzte Kanäle werden mit einem eigenen Skript in eine **separate Datei** gesammelt, damit bestehende Daten nicht überschrieben werden

### Erfasste Felder

| Feld | Bedeutung |
|---|---|
| `kanal`, `seite` | Quelle und Quellengruppe (in der Dokumentation anonymisiert als A–F / 1–3) |
| `id` | eindeutige Beitragsnummer im Kanal |
| `datum` | Veröffentlichungszeit (UTC) |
| `text` | Beitragstext (Persisch) |
| `views` | Aufrufe |
| `weiterleitungen` | wie oft weitergeleitet |
| `weitergeleitet_von` | Ursprung, falls der Beitrag selbst weitergeleitet wurde |

---

## 2. Ergebnis

**328.330 Beiträge** aus 6 Kanälen:

| Quelle | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| Gruppe | 1 | 1 | 1 | 2 | 2 | 3 |
| Beiträge | 59.546 | 47.698 | 65.728 | 58.160 | 49.925 | 47.273 |

---

## 3. Qualitätsprüfung

Ein eigenes Prüfskript kontrolliert die Daten auf sieben Punkte und speichert je einen Prüfbericht.

| Prüfung | Ergebnis |
|---|---|
| Zeilen je Kanal = Ausgabe der Sammlung | ✅ übereinstimmend |
| Zeitraum je Kanal vollständig | ✅ 01.01.–31.08. bei allen Kanälen |
| Doppelte Beiträge | ✅ 0 |
| Beiträge ohne Text | 11–27 % je Kanal (Bilder/Videos ohne Beschreibung) |
| Tage ohne Beiträge | ⚠️ Quelle A: 16 Tage – 14 am Stück (09.–22.01.) sowie 16.–17.03. · Quelle F: 6 Tage (09.–14.01.) |
| Beiträge pro Woche | Tabelle zur Erkennung von Einbrüchen |

### Umgang mit Lücken
Für Quelle A wurde der Januar-Zeitraum mit einem separaten Skript **gezielt erneut abgefragt**.
Ergebnis: Die Beiträge fehlen auch direkt beim Anbieter – die Sammlung war vollständig, die Lücke liegt in der Quelle selbst.

Die Januar-Lücken bei A und F fallen in denselben Zeitraum Anfang Januar, in dem der Internetzugang im Land
stark eingeschränkt war. Sie werden in der Analyse berücksichtigt
(Vergleiche pro Tag statt absoluter Summen, Januar gesondert betrachtet).

### Abgrenzung
Zusätzlich wurde das Webarchiv einer weiteren Quelle erhoben (rund 5.300 Artikel).
Es wird in dieser Analyse nicht berücksichtigt: Lange Webartikel ohne Aufrufzahlen sind mit
Messenger-Beiträgen nicht direkt vergleichbar, und die lokale KI-Auswertung langer Texte erfordert
einen deutlich höheren Rechenaufwand. Die Daten sind für eine gesonderte Auswertung vorgesehen.

### Erste Beobachtung aus der Wochentabelle
Die Veröffentlichungsaktivität steigt ab Ende Februar bei fast allen Kanälen deutlich an
und zeigt einen zweiten Anstieg im Juli. Quelle A folgt diesem Muster kaum. → Details in [04 – Analyse](04_analyse.md).

---

## 4. Sicherheit und Datenschutz

- API-Zugangsdaten nur als **Umgebungsvariablen**, nie im Code
- Sitzungsdatei, Rohdaten und CSV-Dateien per `.gitignore` vom Repository ausgeschlossen
- Nur redaktionelle Veröffentlichungen, **keine personenbezogenen Daten** von Nutzern
- Alle Daten werden ausschließlich lokal gespeichert und verarbeitet

---

## 5. Technische Umgebung

- Linux (Arch), conda-Umgebung mit Python 3.11
- Bibliotheken: `telethon`, `pandas`, `qrcode`

### Projektstruktur (Ausschnitt)
```
projekt/
├── data/
│   ├── row/        ← Rohdaten + Prüfberichte (nicht im Repo)
│   └── ki/         ← Ergebnisse der KI-Einordnung (nicht im Repo)
└── scripts/
    ├── telegram/   ← Login, Sammlung, Nachsammlung, Prüfung
    └── ai/         ← KI-Einordnung (siehe 03)
```
