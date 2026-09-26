[English](../en/01_data_collection.md) | **Deutsch**

# 01 – Datenerhebung

[← zurück zur Übersicht](../../README.de.md)

Dieser Schritt beschreibt, wie die Rohdaten gesammelt und auf Vollständigkeit geprüft wurden.
Die Rohtexte sind aus urheberrechtlichen Gründen nicht Teil des Repositorys.

---

## Überblick

| | |
|---|---|
| Zugang | offizielle Telegram-API |
| Werkzeug | Python, `Telethon` |
| Umfang | 6 öffentliche Kanäle, 328.330 Beiträge |
| Zeitraum | 01.01.–31.08.2026 |
| Status | abgeschlossen |

Die Kanäle sind in **drei Quellengruppen** eingeteilt:

| Gruppe | Kanäle |
|---|---|
| 1 – staatlich / amtlich | IRNA, IRIB News, Mehr News |
| 2 – IRGC-nah | Tasnim News, Fars News |
| 3 – reformorientiert | Jamaran |

---

## 1. Vorgehen

- Zugriff über die **offizielle API** mit eigenem Entwicklerzugang (API-ID/-Hash)
- Nur **öffentliche Kanäle** redaktioneller Medien – keine Gruppen, keine privaten Nutzer, kein Beitritt zu Kanälen nötig
- Anmeldung einmalig per QR-Code; die Sitzungsdatei bleibt lokal
- Beiträge werden rückwärts ab dem Enddatum gelesen, bis das Startdatum erreicht ist
- Automatische Pausen bei Ratenbegrenzung durch die API
- Später ergänzte Kanäle (hier: Jamaran) werden mit einem eigenen Skript in eine **separate Datei** gesammelt, damit bestehende Daten nicht überschrieben werden

### Erfasste Felder

| Feld | Bedeutung |
|---|---|
| `kanal` | Telegram-Name des Kanals |
| `seite` | Quellengruppe |
| `id` | eindeutige Beitragsnummer im Kanal (Beitrag abrufbar unter `t.me/<kanal>/<id>`) |
| `datum` | Veröffentlichungszeit (UTC) |
| `text` | Beitragstext (Persisch) |
| `views` | Aufrufe |
| `weiterleitungen` | wie oft weitergeleitet |
| `weitergeleitet_von` | Ursprung, falls der Beitrag selbst weitergeleitet wurde |

---

## 2. Ergebnis

**328.330 Beiträge** aus 6 Kanälen:

| Kanal | Gruppe | Beiträge |
|---|---|---|
| IRNA (`@IRNA_1313`) | 1 | 59.546 |
| IRIB News (`@iribnews`) | 1 | 47.698 |
| Mehr News (`@mehrnews`) | 1 | 65.728 |
| Tasnim News (`@Tasnimnews`) | 2 | 58.160 |
| Fars News (`@farsna`) | 2 | 49.925 |
| Jamaran (`@jamarannews`) | 3 | 47.273 |

---

## 3. Qualitätsprüfung

Ein eigenes Prüfskript kontrolliert die Daten auf sieben Punkte und speichert je einen Prüfbericht.

| Prüfung | Ergebnis |
|---|---|
| Zeilen je Kanal = Ausgabe der Sammlung | ✅ übereinstimmend |
| Zeitraum je Kanal vollständig | ✅ 01.01.–31.08. bei allen Kanälen |
| Doppelte Beiträge | ✅ 0 |
| Beiträge ohne Text | 11–27 % je Kanal (Bilder/Videos ohne Beschreibung) |
| Tage ohne Beiträge | ⚠️ IRNA: 16 Tage – 14 am Stück (09.–22.01.) sowie 16.–17.03. · Jamaran: 6 Tage (09.–14.01.) · alle anderen: keine |
| Beiträge pro Woche | Tabelle zur Erkennung von Einbrüchen |

### Umgang mit Lücken
Für IRNA wurde der Januar-Zeitraum mit einem separaten Skript **gezielt erneut abgefragt**.
Ergebnis: Die Beiträge fehlen auch direkt auf Telegram – die Sammlung war vollständig, die Lücke liegt im Kanal selbst.

Die Januar-Lücken bei IRNA und Jamaran fallen in den Zeitraum Anfang Januar, in dem der Internetzugang in Iran
während der Proteste stark eingeschränkt war. Sie werden in der Analyse berücksichtigt
(Vergleiche pro Tag statt absoluter Summen, Januar gesondert betrachtet).

### Abgrenzung
Zusätzlich wurde das Webarchiv von **Sepah News**, dem offiziellen Nachrichtenportal der IRGC, erhoben
(rund 5.300 Artikel); der Telegram-Kanal war aus Deutschland nicht abrufbar.
Das Archiv wird in dieser Analyse nicht berücksichtigt: Lange Webartikel ohne Aufrufzahlen sind mit
Telegram-Beiträgen nicht direkt vergleichbar, und die lokale KI-Auswertung langer Texte erfordert
einen deutlich höheren Rechenaufwand. Die Daten sind für eine gesonderte Auswertung vorgesehen.

### Erste Beobachtung aus der Wochentabelle
Die Veröffentlichungsaktivität steigt ab Ende Februar bei fast allen Kanälen deutlich an
und zeigt einen zweiten Anstieg im Juli. IRNA folgt diesem Muster kaum. Details folgen in 04 – Analyse.

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
telegram-iran/
├── data/
│   ├── row/        ← Rohdaten + Prüfberichte (nicht im Repo)
│   └── ki/         ← Ergebnisse der KI-Einordnung
└── scripts/
    ├── telegram/   ← Login, Sammlung, Nachsammlung, Prüfung
    └── ai/         ← KI-Einordnung (siehe 03)
```
