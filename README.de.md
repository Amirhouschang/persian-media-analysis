[English](README.md) | **Deutsch**

# Iranische Nachrichtenkanäle im Krieg 2026 – Telegram-Analyse mit lokaler KI

**Python · SQL · NLP · lokale KI**

Ende-zu-Ende-Projekt zur Erhebung, Aufbereitung und Auswertung von über **328.000 persischsprachigen
Telegram-Beiträgen** sechs iranischer Nachrichtenkanäle vom 1. Januar bis 31. August 2026 – dem Zeitraum
der Proteste im Januar, des Kriegs zwischen Israel/USA und Iran ab dem 28. Februar und der folgenden
Waffenruhen. Von der automatisierten Datensammlung über eine relationale Datenbank bis zur Einordnung mit
lokal betriebenen Sprachmodellen. Im Mittelpunkt steht die Methode: Wie lassen sich fremdsprachige Medien
systematisch, überprüfbar und reproduzierbar auswerten?

> **Hinweis:** Code, Methodik und Ergebnisse sind öffentlich. Die Rohtexte der Beiträge sind aus
> urheberrechtlichen Gründen nicht Teil des Repositorys; jeder Beitrag ist über Kanal und ID
> (`t.me/<kanal>/<id>`) öffentlich auffindbar.

---

## Fragestellung

Wie unterscheiden sich staatliche, IRGC-nahe und reformorientierte Nachrichtenkanäle in **Umfang,
Themenwahl, Wortwahl, Ton und Reichweite** – und wie verändern sich diese Muster rund um einschneidende
Ereignisse?

## Quellen

| Gruppe | Kanal | Telegram | Beschreibung (neutral) | Beiträge |
|---|---|---|---|---|
| 1 – staatlich / amtlich | IRNA | `@IRNA_1313` | amtliche staatliche Nachrichtenagentur, von der Regierung beaufsichtigt | 59.546 |
| 1 – staatlich / amtlich | IRIB News | `@iribnews` | Nachrichtendienst des staatlichen Rundfunks; die Leitung ernennt der Revolutionsführer | 47.698 |
| 1 – staatlich / amtlich | Mehr News | `@mehrnews` | halbamtliche Agentur der Islamic Development Organization (dem Revolutionsführer unterstellt) | 65.728 |
| 2 – IRGC-nah | Tasnim News | `@Tasnimnews` | halbamtliche Agentur, weithin als IRGC-nah beschrieben | 58.160 |
| 2 – IRGC-nah | Fars News | `@farsna` | halbamtliche Agentur, weithin als IRGC-nah beschrieben | 49.925 |
| 3 – reformorientiert | Jamaran | `@jamarannews` | Nachrichtenportal im Umfeld des Instituts für die Werke Ayatollah Khomeinis; dem Reformlager zugeordnet | 47.273 |

## Datenbasis

| | |
|---|---|
| Zeitraum | 01.01.–31.08.2026 |
| Quellen | 6 öffentliche Telegram-Kanäle in drei Quellengruppen |
| Umfang | 328.330 Beiträge |
| Sprache | Persisch |

---

## Pipeline und Stand

| Schritt | Inhalt | Status | Details |
|---|---|---|---|
| 1. Datenerhebung | Telegram-API, Qualitätsprüfung | ✅ abgeschlossen | [01 – Datenerhebung](docs/de/01_datenerhebung.md) |
| 2. Aufbereitung | Bereinigung persischer Texte, PostgreSQL | ⬜ geplant | 02 – Aufbereitung |
| 3. KI-Einordnung | Codebuch, Modellvergleich, Hauptlauf, Validierung | ⏳ Hauptlauf | [03 – KI-Einordnung](docs/de/03_ki_einordnung.md) |
| 4. Analyse | Zeitreihen, Ereignisanalyse, Framing, Reichweite | ⬜ geplant | 04 – Analyse |
| 5. Dashboard | lokales interaktives Dashboard | ⬜ geplant | 05 – Dashboard |
| 6. Methodik & Grenzen | Einschränkungen, Datenschutz, Sicherheit | ⬜ geplant | 06 – Methodik |

### 1. Datenerhebung
- Abruf öffentlicher Kanäle über die offizielle Telegram-API (`Telethon`)
- Pausen bei Ratenbegrenzung, separate Dateien für nachträglich ergänzte Kanäle
- Automatische Qualitätsprüfung (Vollständigkeit, Duplikate, Lücken) mit gezielter Nachprüfung auffälliger Zeiträume

### 2. Aufbereitung *(geplant)*
- Normalisierung persischer Schrift (arabische vs. persische Zeichen, Halbleerzeichen) mit `hazm`
- Bereinigung von Links, Emojis, Dubletten; Zuordnung zu Zeitphasen
- Relationale Datenbank in **PostgreSQL**, Abfragen und Prüfung in **DBeaver**

### 3. KI-Einordnung *(Hauptlauf)*
- Einordnung nach **Thema** (9 Kategorien) und **Ton** (6 Kategorien) mit **lokal betriebenen Sprachmodellen** (`Ollama`) – keine Cloud
- **Codebuch** mit operationalen Definitionen, weiterentwickelt über acht Versionen
- **Kontext:** neutrales Hintergrundwissen zu Ereignissen, Akteuren, Völkerrecht und ein Glossar persischer Begriffe
- **Modellvergleich** an 150 manuell geprüften Beiträgen: Gemma 4 (26B, 31B), Qwen 3.6 (27B, 35B), Qwen 2.5 (32B), Aya Expanse (32B)
- **Gewähltes Modell: Gemma 4 31B** – 80,7 % exakte Übereinstimmung bei Thema und Ton, 86,7 % unter Berücksichtigung von Grenzfällen; Cohens Kappa Thema 0,85, Ton 0,79
- **Hauptlauf:** geschichtete Stichprobe von ca. 10.500 Beiträgen (50 pro Kanal und Woche), gewichtet hochgerechnet
- **Endvalidierung:** 200 neue Beiträge, blind kodiert – danach keine Änderungen mehr
- Der ganze Weg inklusive Irrwege: [03 – KI-Einordnung](docs/de/03_ki_einordnung.md)

### 4. Analyse *(geplant)*
- Veröffentlichungsaktivität im Zeitverlauf und rund um Schlüsselereignisse
- Vergleich der Quellengruppen nach Thema, Ton und Reichweite
- Terminologie- und Framing-Analyse: Welche Begriffe verwenden welche Quellen für dieselben Sachverhalte?
- Dichte ideologischer Begriffe pro 1.000 Wörter

### 5. Dashboard *(geplant)*
- Interaktive Grafiken mit `Plotly`, lokales Dashboard mit `Streamlit`

---

## Tech-Stack

| Bereich | Werkzeuge |
|---|---|
| Sprache & Umgebung | Python 3.11, conda, Linux |
| Datenerhebung | Telethon |
| Textverarbeitung | hazm |
| Datenbank & SQL | PostgreSQL, DBeaver |
| Analyse | pandas |
| Lokale KI | Ollama (Gemma 4, Qwen, Aya Expanse) |
| Visualisierung | Plotly, Streamlit |

---

## Projektstruktur

```
telegram-iran/
├── README.md            ← englische Version
├── README.de.md         ← deutsche Version
├── docs/
│   ├── en/              ← ausführliche Seiten auf Englisch
│   └── de/              ← ausführliche Seiten auf Deutsch
├── scripts/
│   ├── telegram/        ← Login, Sammlung, Nachsammlung, Prüfung
│   └── ai/              ← KI-Einordnung: Konfiguration, Codebuch, Hintergrund, Modellvergleich, Hauptlauf
├── results/ai/          ← veröffentlichte KI-Ergebnisse (ohne Beitragstexte)
└── data/                ← Rohdaten (nicht im Repository)
```

---

## Datenschutz & Methodik

- ausschließlich **öffentlich zugängliche** redaktionelle Veröffentlichungen
- **keine personenbezogenen Daten** von Nutzern, keine privaten Gruppen oder Kommentare
- Verarbeitung vollständig **lokal**, auch die KI-Einordnung
- Zugangsdaten nur als Umgebungsvariablen; Rohdaten und Sitzungsdateien vom Repository ausgeschlossen
- KI-Ergebnisse werden nicht ungeprüft übernommen, sondern gegen manuelle Kodierung validiert

## Kompetenzen, die das Projekt zeigt

- Datenerhebung über APIs, inklusive Fehlerbehandlung und Ratenbegrenzung
- Datenqualität: systematische Prüfung, Umgang mit Lücken, Dokumentation von Einschränkungen
- Verarbeitung nicht-lateinischer Schriften
- SQL und relationale Datenbanken
- Einsatz und **Validierung** lokaler KI: Codebuch-Entwicklung, Modellvergleich, messbare Experimente
- Quellenkritische Auswertung fremdsprachiger Medien

## Status

In Bearbeitung – die Seiten unter `docs/` werden nach jedem abgeschlossenen Schritt ergänzt.

---

## Position des Autors

Ich lehne Krieg und Gewalt gegen Menschen ab, unabhängig davon, von welcher Seite sie ausgehen. Dieses Projekt
bezieht keine politische Position: Es beschreibt, wie Medien berichten, nicht, wer recht hat. Alle Quellen werden
nach denselben Regeln ausgewertet. In der Auswertung verwende ich für Ereignisse wie die Tötung von Politikern und
Militärs neutrale Begriffe („getötet“). Wie unterschiedlich Medien und Staaten solche Taten benennen – etwa als
„Eliminierung“, „gezielte Tötung“ oder „Terror“ –, ist selbst Gegenstand der Analyse.

Kein Mensch darf getötet werden – auch nicht hochrangige Politiker und Generäle der Islamischen Republik Iran, und
schon gar nicht in ihren Wohnhäusern, gemeinsam mit ihren Familien. Dieses Projekt ist
deshalb kein Ort für Sprache, die solche Tötungen verharmlost oder rechtfertigt, auch nicht durch Begriffe wie
„Eliminierung“.
