[English](../en/02_processing.md) | **Deutsch**

# 02 – Aufbereitung: Datenbank und Textbereinigung

[← zurück zur Übersicht](../../README.de.md)

Dieser Schritt überführt die Rohdaten in eine relationale **PostgreSQL**-Datenbank und bereitet die persischen Texte
für die Analyse auf.

| Teil | Status |
|---|---|
| Datenbank `iran_media_2026` | ✅ abgeschlossen |
| Textbereinigung mit `hazm` | ⬜ geplant |

---

## 1. Datenbank

### Aufbau

Die Beiträge stehen in der Mitte, beschreibende Tabellen sind über Schlüssel verbunden
(Snowflake-Schema: `channels` → `source_groups`, `dates` → `phases`).

![Datenbankschema](../images/database_schema.png)

| Tabelle | Schlüssel | Inhalt | Zeilen |
|---|---|---|---|
| `posts` | `channel_id` + `post_id` | alle Beiträge: Zeitpunkt, Text, Aufrufe, Weiterleitungen, Link | 328.330 |
| `channels` | `channel_id` | Kanal, Name, Gruppe, Link, neutrale Beschreibung | 6 |
| `source_groups` | `group_id` | staatlich, IRGC-nah, reformorientiert | 3 |
| `dates` | `date_key` (JJJJMMTT) | jeder Tag: Monat, Kalenderwoche, Wochentag, Phase | 243 |
| `phases` | `phase_id` | vier Zeitabschnitte des Beobachtungszeitraums | 4 |

### Phasen

| Phase | Zeitraum | Beschreibung |
|---|---|---|
| `before_war` | 01.01.–27.02. | Proteste und Internetsperre im Januar, Verhandlungen |
| `war` | 28.02.–07.04. | von den Angriffen der USA und Israels bis zur Waffenruhe |
| `ceasefire` | 08.04.–07.07. | Waffenruhe, Seeblockade, Islamabad-Memorandum; brüchig, mit Zusammenstößen |
| `after_truce_collapse` | 08.07.–31.08. | nach dem Zusammenbruch der Waffenruhe am 08.07. |

Die Grenzen sind eine Setzung des Autors auf Basis zentraler Ereignisse und in `02_load_database.py` festgelegt.

### Vorgehen

- `01_schema.sql` legt die Tabellen mit Primär- und Fremdschlüsseln an.
- `02_load_database.py` lädt beide Rohdateien, ersetzt Kanalnamen durch Schlüssel, berechnet `date_key` und Link
  und prüft am Ende die Zahl der Beiträge pro Kanal (328.330, identisch mit der Sammlung).
- Das Laden ist **wiederholbar**: Tabellen werden jedes Mal neu aufgebaut, das Ergebnis ist immer gleich.
- Alle Zeiten in **UTC**.
- Die KI-Ergebnisse kommen nach dem Hauptlauf als eigene Tabelle `classifications` hinzu, weil nur eine
  Stichprobe eingeordnet wird, dazu die Nachschlagetabellen `topics` und `tones`.

### Beispielabfragen

`03_example_queries.sql` enthält erste Auswertungen, z. B. Beiträge pro Woche und Quellengruppe,
Aufrufe pro Kanal, fehlende Tage, Beiträge pro Phase und Tag sowie die Woche vor und nach dem 28.02.

---

## 2. Textbereinigung *(geplant)*

- Vereinheitlichung persischer Schrift (arabische vs. persische Zeichen, Halbleerzeichen) mit `hazm`
- Entfernen von Links, Emojis, Kanal-Signaturen
- Zerlegung in Wörter und Entfernen von Füllwörtern als Grundlage für die Wortanalyse

---

## Technik

PostgreSQL 18 · Python (`pandas`, `SQLAlchemy`, `psycopg`) · DBeaver

| Datei | Aufgabe |
|---|---|
| `scripts/database/01_schema.sql` | Tabellenstruktur |
| `scripts/database/02_load_database.py` | Rohdaten laden |
| `scripts/database/03_example_queries.sql` | Beispielabfragen |
