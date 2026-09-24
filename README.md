# Mehrsprachige Medienanalyse persischsprachiger Quellen

**Python · SQL · NLP · lokale KI**

Ende-zu-Ende-Projekt zur Erhebung, Aufbereitung und Auswertung von über 286.000 persischsprachigen
Nachrichtenbeiträgen – von der automatisierten Datensammlung über eine relationale Datenbank bis zur
Einordnung mit lokal betriebenen Sprachmodellen. Im Mittelpunkt steht die Methode: Wie lassen sich
fremdsprachige Medien systematisch, überprüfbar und reproduzierbar auswerten?

> **Hinweis:** Rohdaten, Quellenliste und inhaltliche Einzelergebnisse sind nicht Teil dieses Repositorys.
> Eine Vorstellung des Projekts ist im persönlichen Gespräch möglich.

---

## Fragestellung

Wie unterscheiden sich zwei Gruppen von Nachrichtenquellen in **Umfang, Themenwahl, Wortwahl, Ton und
Reichweite** – und wie verändern sich diese Muster rund um einschneidende Ereignisse?

## Quellen

Die Quellen werden anonymisiert als **A–F** bezeichnet und zwei Gruppen zugeordnet.

| Gruppe | Quelle | Art | Beiträge (01.01.–31.08.2026) |
|---|---|---|---|
| 1 | A | Messenger-Kanal | 59.546 |
| 1 | B | Messenger-Kanal | 47.698 |
| 1 | C | Messenger-Kanal | 65.728 |
| 2 | D | Messenger-Kanal | 58.160 |
| 2 | E | Messenger-Kanal | 49.925 |
| 2 | F | Nachrichten-Webarchiv | 5.319 |

## Datenbasis

| | |
|---|---|
| Zeitraum | 01.01.–31.08.2026 |
| Quellen | 6 Quellen (A–F) in zwei Quellengruppen: 5 öffentliche Messenger-Kanäle + 1 Nachrichten-Webarchiv |
| Umfang | 281.057 Messenger-Beiträge + 5.319 Web-Artikel |
| Sprache | Persisch |

---

## Pipeline und Stand

| Schritt | Inhalt | Status | Details |
|---|---|---|---|
| 1. Datenerhebung | Messenger-API, Web-Archiv, Qualitätsprüfung | ✅ abgeschlossen | [01 – Datenerhebung](docs/01_datenerhebung.md) |
| 2. Aufbereitung | Bereinigung persischer Texte, Kalenderumrechnung, PostgreSQL | ⬜ geplant | 02 – Aufbereitung |
| 3. KI-Einordnung | Codebuch, Modellvergleich, Kontext-Experiment | ⏳ in Arbeit | 03 – KI-Einordnung |
| 4. Analyse | Zeitreihen, Ereignisanalyse, Framing, Reichweite | ⬜ geplant | 04 – Analyse |
| 5. Dashboard | lokales interaktives Dashboard | ⬜ geplant | 05 – Dashboard |
| 6. Methodik & Grenzen | Einschränkungen, Datenschutz, Sicherheit | ⬜ geplant | 06 – Methodik |

### 1. Datenerhebung
- Abruf öffentlicher Kanäle über die offizielle Messenger-API (`Telethon`)
- Web-Archiv über fortlaufende Artikel-IDs (`requests`, `BeautifulSoup`), Umrechnung persischer Kalenderdaten
- Fortsetzungslogik bei Abbrüchen, Pausen zwischen Anfragen, Testmodus vor dem vollen Lauf
- Automatische Qualitätsprüfung (Vollständigkeit, Duplikate, Lücken) mit gezielter Nachprüfung auffälliger Zeiträume

### 2. Aufbereitung *(geplant)*
- Normalisierung persischer Schrift (arabische vs. persische Zeichen, Halbleerzeichen) mit `hazm`
- Bereinigung von Links, Emojis, Dubletten; Zuordnung zu Zeitphasen
- Relationale Datenbank in **PostgreSQL**, Abfragen und Prüfung in **DBeaver**

### 3. KI-Einordnung *(in Arbeit)*
- Einordnung nach **Thema** und **Ton** mit **lokal betriebenen Sprachmodellen** (`Ollama`) – keine Cloud, alle Daten bleiben auf dem eigenen Rechner
- **Codebuch** mit operationalen Definitionen: Jede Kategorie beschreibt sichtbare Textmerkmale statt Deutungen; weiterentwickelt über drei Versionen
- **Validierung:** manuell kodiertes Testset als Referenz; Trefferquote, Verwechslungen und Begründungen der KI werden ausgewertet
- **Modellvergleich:** Gemma 4 (26B, 31B), Qwen 2.5 (32B), Qwen 3.6 (27B), Aya Expanse (8B, 32B)
- **Kontext-Experiment:** Einordnung mit und ohne neutrales Hintergrundwissen sowie Angaben zur Herkunft der Quelle
- Ergebnisse und gewähltes Modell folgen in *03 – KI-Einordnung*

### 4. Analyse *(geplant)*
- Veröffentlichungsaktivität im Zeitverlauf und rund um Schlüsselereignisse
- Vergleich der Quellengruppen nach Thema, Ton und Reichweite
- Terminologie- und Framing-Analyse: Welche Begriffe verwenden welche Quellen für dieselben Sachverhalte?

### 5. Dashboard *(geplant)*
- Interaktive Grafiken mit `Plotly`, lokales Dashboard mit `Streamlit`

---

## Tech-Stack

| Bereich | Werkzeuge |
|---|---|
| Sprache & Umgebung | Python 3.11, conda, Linux |
| Datenerhebung | Telethon, requests, BeautifulSoup, jdatetime |
| Textverarbeitung | hazm |
| Datenbank & SQL | PostgreSQL, DBeaver |
| Analyse | pandas |
| Lokale KI | Ollama (Gemma 4, Qwen, Aya Expanse) |
| Visualisierung | Plotly, Streamlit |

---

## Projektstruktur

```
projekt/
├── README.md
├── docs/                ← ausführliche Seiten zu jedem Schritt
├── scripts/
│   ├── telegram/        ← Messenger: Login, Sammlung, Nachsammlung, Prüfung
│   ├── web/             ← Webarchiv-Sammlung
│   └── ai/              ← KI-Einordnung: Konfiguration, Codebuch, Modellvergleich, Klassifizierung
└── data/                ← Rohdaten und Ergebnisse (nicht im Repository)
```

---

## Datenschutz & Methodik

- ausschließlich **öffentlich zugängliche** redaktionelle Veröffentlichungen
- **keine personenbezogenen Daten** von Nutzern, keine privaten Gruppen oder Kommentare
- Verarbeitung vollständig **lokal**, auch die KI-Einordnung
- Zugangsdaten nur als Umgebungsvariablen; Rohdaten und Sitzungsdateien vom Repository ausgeschlossen
- KI-Ergebnisse werden nicht ungeprüft übernommen, sondern gegen manuelle Kodierung validiert

## Kompetenzen, die das Projekt zeigt

- Datenerhebung über APIs und Web-Archive, inklusive Fehlerbehandlung und Fortsetzung
- Datenqualität: systematische Prüfung, Umgang mit Lücken, Dokumentation von Einschränkungen
- Verarbeitung nicht-lateinischer Schriften und fremder Kalendersysteme
- SQL und relationale Datenbanken
- Einsatz und **Validierung** lokaler KI: Codebuch-Entwicklung, Modellvergleich, messbare Experimente
- Quellenkritische Auswertung fremdsprachiger Medien

## Status

In Bearbeitung – die Seiten unter `docs/` werden nach jedem abgeschlossenen Schritt ergänzt.
