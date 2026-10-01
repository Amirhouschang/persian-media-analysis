[English](../en/02_processing.md) | **Deutsch**

# 02 – Aufbereitung: Datenbank und Textbereinigung

[← zurück zur Übersicht](../../README.de.md)

Dieser Schritt überführt die Rohdaten in eine relationale **PostgreSQL**-Datenbank und bereitet die persischen Texte
für die Analyse auf.

| Teil | Status |
|---|---|
| Datenbank `iran_media_2026` | ✅ abgeschlossen |
| Textbereinigung | ✅ abgeschlossen |

---

## 1. Datenbank

### Aufbau

Die Beiträge stehen in der Mitte, beschreibende Tabellen sind über Schlüssel verbunden
(Snowflake-Schema: `channels` → `source_groups`, `dates` → `phases`).

![Datenbankschema](../../images/database_schema.png)

| Tabelle | Schlüssel | Inhalt | Zeilen |
|---|---|---|---|
| `posts` | `channel_id` + `post_id` | alle Beiträge: Zeitpunkt, Text, bereinigter Text, Aufrufe, Weiterleitungen, Link | 328.330 |
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

## 2. Textbereinigung

`04_clean_text.py` bereinigt jeden Beitrag und schreibt drei neue Spalten in `posts`. Die Originalspalte `text` bleibt unverändert.

| Spalte | Inhalt |
|---|---|
| `text_clean` | bereinigter Text |
| `tokens` | Inhaltswörter ohne Füllwörter – Grundlage der Wortanalyse |
| `word_count` | Anzahl Wörter in `text_clean` |

### Regeln

| Schritt | Beispiel |
|---|---|
| Kanalwerbung entfernen (kurze Zeilen wie „folgt uns auf …“) | `ایرنا را در بله و روبیکا دنبال کنید` → entfernt |
| Links, `@Erwähnungen`, Emojis und Symbole entfernen | `🔹`, `📡 @Mehrnews`, `mehrnews.com` → entfernt |
| Hashtags werden zu Wörtern | `#اینفو_ایرنا` → `اینفو ایرنا` |
| Arabische Buchstabenvarianten → persisch | `ي ى` → `ی`, `ك` → `ک`, `ة` → `ه` |
| Arabische und lateinische Ziffern → persisch | `2026` → `۲۰۲۶` |
| Vokalzeichen und Dehnungszeichen entfernen | `شَهید` → `شهید`, `ســـلام` → `سلام` |
| Halbleerzeichen statt Leerzeichen nach der Vorsilbe می / نمی | `می گوید` → `می‌گوید` |
| Halbleerzeichen vor der Pluralendung ها / های und vor ترین | `کشور های` → `کشورهای`, `برنامه ها` → `برنامه‌ها`, `بزرگ ترین` → `بزرگ‌ترین` |
| Halbleerzeichen vor ای nach einem Wort auf ه | `منطقه ای` → `منطقه‌ای` |
| Alef mit Hamza → Alef, beide Schreibweisen zählen als ein Wort | `تأکید` → `تاکید` |
| He mit Hamza → He (schreibt nur ein Kanal) | `تنگۀ هرمز` → `تنگه هرمز` |
| Zusammengesetzte Wörter mit Leerzeichen verbinden | `بین المللی` → `بین‌المللی`, `گفت و گو` → `گفت‌وگو`, `آموزش و پرورش`, `سیستان و بلوچستان` … |
| Kein Halbleerzeichen nach Buchstaben, die nicht nach links verbinden (ا د ذ ر ز ژ و) | `کشور‌های` → `کشورهای` |
| Füllwörter entfernen (nur in `tokens`) | `از`, `به`, `که`, `این` … |

Die persischen Buchstaben پ چ ژ گ und das Halbleerzeichen bleiben erhalten.

Die Regeln ab der Pluralendung kamen in einer zweiten Runde hinzu: Die Wortanalyse (Seite 04) zeigte, dass dasselbe
Wort in mehreren Schreibweisen gezählt wurde (`کشورهای` und `کشور های`, `تأکید` und `تاکید`) und dass bei
`بین المللی` nach dem Entfernen der Füllwörter nur `المللی` übrig blieb. Danach wurde die Bereinigung erneut ausgeführt.

**Warum nicht `hazm`?** Die Bibliothek `hazm` erzwingt eine alte `numpy`-Version, mit der `pandas` in dieser Umgebung
nicht mehr läuft. Die Regeln sind deshalb direkt im Skript umgesetzt; nur die Füllwortliste stammt aus `hazm`
(`stopwords_fa.txt`, MIT-Lizenz).

### Ergebnis

| Kanal | Beiträge | ohne Text | Ø Wörter pro Beitrag |
|---|---|---|---|
| IRNA | 59.546 | 16,4 % | 86 |
| IRIB News | 47.698 | 10,8 % | 45 |
| Mehr News | 65.728 | 21,2 % | 48 |
| Tasnim News | 58.160 | 17,0 % | 63 |
| Fars News | 49.925 | 26,6 % | 46 |
| Jamaran | 47.273 | 18,5 % | 78 |

„Ohne Text“ = Bilder oder Videos ohne Beschreibung oder Beiträge, die nur aus Werbung oder Links bestanden.

### Prüfung

`05_check_cleaning.sql` prüft das Ergebnis:

| Prüfung | Ergebnis |
|---|---|
| Arabische Buchstabenvarianten übrig | ✅ 0 |
| Links oder `@Erwähnungen` übrig | 1 – geprüft, korrekt |
| Beiträge mit persischem Text, die nach der Bereinigung leer sind | 22 – geprüft: nur Werbezeilen |
| 20 Beiträge mit den meisten entfernten Wörtern | ✅ geprüft: nur Werbung, Links, `@Erwähnungen` entfernt |
| Zufallsstichprobe von 20 Beiträgen, vollständig gelesen | ✅ korrekt |
| Allein stehendes ها / های nach der zweiten Runde | 37 von 328.330 Beiträgen – vernachlässigbar |

Der erste Lauf trennte Wörter, die mit می beginnen (`میدان` → `می‌دان`). Die Regel wurde auf `می` mit
folgendem Leerzeichen beschränkt und die Bereinigung erneut ausgeführt.

---

## Technik

PostgreSQL 18 · Python (`pandas`, `SQLAlchemy`, `psycopg`) · DBeaver

| Datei | Aufgabe |
|---|---|
| `scripts/database/01_schema.sql` | Tabellenstruktur |
| `scripts/database/02_load_database.py` | Rohdaten laden |
| `scripts/database/03_example_queries.sql` | Beispielabfragen |
| `scripts/database/04_clean_text.py` | Textbereinigung |
| `scripts/database/stopwords_fa.txt` | persische Füllwörter (aus `hazm`, MIT-Lizenz) |
| `scripts/database/05_check_cleaning.sql` | Prüfung der Bereinigung |
