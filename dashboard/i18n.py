"""
i18n.py – texts of the dashboard in German and English
================================================================
Everything the reader sees (except the Persian terms of the analysis themselves) is defined here:
  UI          – interface texts
  GROUPS, CHANNELS, PHASES, TOPICS, CATEGORIES – names of the data categories
  EVENTS      – dated events shown as lines in the charts
The translations of the single terms (69 terms of the word analysis and 35 countries / actors) are in concepts.csv.
"""

LANGS = {"de": "Deutsch", "en": "English"}

GROUPS = {
    "state": {"de": "Staatlich", "en": "State"},
    "irgc_affiliated": {"de": "IRGC-nah", "en": "IRGC-affiliated"},
    "reformist": {"de": "Reformorientiert (Jamaran)", "en": "Reformist (Jamaran)"},
}
GROUP_COLORS = {"state": "#2a78d6", "irgc_affiliated": "#c42f2f", "reformist": "#1baf7a"}

# channel names as in the result tables -> (group, colour, line style)
CHANNELS = {
    "IRNA": ("state", "#2a78d6", "solid"),
    "IRIB News": ("state", "#7fb2ee", "dash"),
    "Mehr News": ("state", "#14437f", "dot"),
    "Tasnim News": ("irgc_affiliated", "#c42f2f", "solid"),
    "Fars News": ("irgc_affiliated", "#ec8a8a", "dash"),
    "Jamaran": ("reformist", "#1baf7a", "solid"),
}

# colours for several terms of one source (Okabe-Ito, colour-blind safe)
TERM_COLORS = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#7a7a7a", "#000000"]

PHASES = {   # (first day, last day) – dates in Tehran time, as in the database
    "before_war": ("2026-01-01", "2026-02-27"),
    "war": ("2026-02-28", "2026-04-07"),
    "ceasefire": ("2026-04-08", "2026-07-07"),
    "after_truce_collapse": ("2026-07-08", "2026-08-31"),
}
PHASE_NAMES = {
    "before_war": {"de": "vor dem Krieg", "en": "before the war"},
    "war": {"de": "Krieg", "en": "war"},
    "ceasefire": {"de": "Waffenruhe", "en": "ceasefire"},
    "after_truce_collapse": {"de": "nach dem Zusammenbruch", "en": "after the collapse"},
}
PHASE_FILL = {"before_war": "rgba(120,120,120,0.07)", "war": "rgba(196,47,47,0.07)",
              "ceasefire": "rgba(27,175,122,0.07)", "after_truce_collapse": "rgba(196,47,47,0.07)"}

TOPICS = {
    "military": {"de": "Militär", "en": "Military"},
    "diplomacy": {"de": "Diplomatie", "en": "Diplomacy"},
    "domestic_politics": {"de": "Innenpolitik", "en": "Domestic politics"},
    "economy": {"de": "Wirtschaft", "en": "Economy"},
    "ideology_propaganda": {"de": "Ideologie", "en": "Ideology"},
    "mourning_commemoration": {"de": "Trauer und Gedenken", "en": "Mourning and commemoration"},
    "resistance_axis": {"de": "Achse des Widerstands", "en": "Axis of resistance"},
    "foreign_affairs": {"de": "Ausland ohne Iran", "en": "Foreign affairs (not Iran)"},
    "other": {"de": "Sonstiges (Service, Wetter, Sport, Kultur)", "en": "Other (service, weather, sport, culture)"},
}

CATEGORIES = {
    "israel_naming": {"de": "Bezeichnungen für Israel", "en": "Names for Israel"},
    "israel_territory": {"de": "Bezeichnungen für Israels Gebiet", "en": "Names for Israel's territory"},
    "israel_army": {"de": "Bezeichnungen für Israels Armee", "en": "Names for Israel's army"},
    "usa_naming": {"de": "Bezeichnungen für die USA", "en": "Names for the USA"},
    "labels_opponents": {"de": "Gegnerbegriffe", "en": "Labels for opponents"},
    "persons": {"de": "Personen", "en": "Persons"},
    "diplomacy": {"de": "Diplomatie", "en": "Diplomacy"},
    "crimes": {"de": "Verbrechen", "en": "Crimes"},
    "revenge": {"de": "Rache", "en": "Revenge"},
    "extra_terms": {"de": "Weitere Begriffe", "en": "Further terms"},
}

REGIONS = {   # as in scripts/analysis/12_countries.py (REGIONS)
    "gulf": {"de": "Golfstaaten und Jordanien", "en": "Gulf states and Jordan",
             "concepts": ["امارات", "عربستان", "قطر", "کویت", "بحرین", "عمان", "اردن"]},
    "axis": {"de": "Libanon, Palästina, Irak, Jemen, Syrien", "en": "Lebanon, Palestine, Iraq, Yemen, Syria",
             "concepts": ["لبنان", "حزب‌الله", "غزه", "حماس", "فلسطین", "عراق", "مقاومت عراق / حشد شعبی", "یمن",
                          "انصارالله / حوثی‌ها", "سوریه", "داعش"]},
    "powers": {"de": "Großmächte und Nachbarn", "en": "Great powers and neighbours",
               "concepts": ["روسیه", "چین", "پاکستان", "ترکیه", "هند", "ژاپن", "افغانستان", "جمهوری آذربایجان",
                            "اوکراین", "ونزوئلا", "طالبان"]},
    "europe": {"de": "Europa", "en": "Europe",
               "concepts": ["اتحادیه اروپا", "انگلیس", "فرانسه", "آلمان", "ایتالیا", "اسپانیا"]},
}

EVENTS = [   # (date, height of the label above the chart: 0 = low, 1, 2 = high, texts)
    # Labels stand horizontally above the chart. Events that are close in time get different heights, the later
    # one lower, so that no line runs through a neighbouring label.
    ("2026-01-08", 0, {"de": "Internetsperre", "en": "internet shutdown"}),
    ("2026-02-28", 2, {"de": "Kriegsbeginn", "en": "war begins"}),
    ("2026-03-08", 1, {"de": "neuer Führer", "en": "new leader"}),
    ("2026-04-08", 0, {"de": "Waffenruhe", "en": "ceasefire"}),
    ("2026-06-17", 2, {"de": "Islamabad-Memorandum", "en": "Islamabad memorandum"}),
    ("2026-07-03", 1, {"de": "Trauerfeier Ali Khamenei", "en": "Ali Khamenei funeral"}),
    ("2026-07-08", 0, {"de": "Waffenruhe bricht zusammen", "en": "ceasefire collapses"}),
]

UI = {
    "de": {
        "title": "Iranische Nachrichtenkanäle 2026",
        "subtitle": "Interaktive Auswertung von 328.330 Telegram-Beiträgen aus sechs iranischen Kanälen "
                    "(01.01.–31.08.2026): Wortwahl, Länder, Themen und Aktivität.",
        "tab_time": "Wortwahl im Zeitverlauf", "tab_countries": "Länder", "tab_topics": "Themen (KI)",
        "tab_activity": "Aktivität", "tab_about": "Über das Projekt",
        "missing": "Die Datei {file} fehlt. Sie wird von {script} erzeugt.",
        # timeline / explorer
        "category": "Kategorie", "view": "Vergleichen", "view_groups": "Gruppen (ein Begriff)",
        "view_terms": "Begriffe (eine Quelle)", "term": "Begriff", "terms": "Begriffe",
        "sum_category": "Summe der ganzen Kategorie", "value": "Wert",
        "v_per1000": "pro 1.000 Wörter", "v_share": "Anteil in der Kategorie (%)", "v_count": "Anzahl Nennungen",
        "y_per1000": "pro 1.000 Wörter", "y_share": "Anteil an allen Begriffen der Kategorie (%)",
        "y_count": "Nennungen pro Woche", "level": "Quellen", "by_groups": "3 Gruppen", "by_channels": "6 Kanäle",
        "source": "Quelle", "show_events": "Ereignisse", "show_phases": "Phasen",
        "week_of": "Woche ab", "complete_weeks": "Nur vollständige Wochen (7 Tage Daten); Wochen beginnen am Montag.",
        "terms_note": "Die Begriffe sind persisch; die Übersetzung steht davor.",
        "select_one_term": "Wähle mindestens einen Begriff.",
        "peak_marker": "◆ = höchste Woche jeder Linie.",
        "phase_title": "Durchschnitt in den vier Phasen",
        "phase_note": "Mittelwert der vollständigen Wochen, die in der Phase beginnen (gleicher Wert wie im Diagramm oben).",
        "rank_title": "Die Begriffe der Kategorie im Vergleich",
        "rank_note": "Mittelwert der Wochenwerte über den ganzen Zeitraum; die acht häufigsten Begriffe, nur die drei Gruppen.",
        "rank_title_c": "Die meistgenannten Länder und Akteure der Region",
        "rank_note_c": "Ganzer Zeitraum, die zwölf häufigsten der gewählten Region, nur die drei Gruppen.",
        "kpi_posts": "Beiträge", "kpi_channels": "Kanäle", "kpi_groups": "Gruppen", "kpi_days": "Tage",
        "col_group": "Gruppe",
        # countries
        "all_regions": "alle Regionen",
        "region": "Region", "country": "Land / Akteur", "countries": "Länder / Akteure",
        "countries_note": "Gezählt wird nur die Nennung des Namens. Nur Gruppen, keine Einzelkanäle.",
        "view_groups_c": "Gruppen (ein Land)", "view_terms_c": "Länder (eine Gruppe)",
        "phases_title": "Nennungen pro 1.000 Wörter nach Phase",
        "col_phase": "Phase",
        # topics
        "topics_warn": "**Vorsicht:** Die KI hat 10.750 Beiträge eingeordnet (gewichtet auf alle Beiträge mit mehr als "
                       "80 Zeichen). Das Thema stimmt in 72,5 % der Fälle (95-%-Intervall 65,9–78,2 %). *Militär* "
                       "wird eher zu oft, *Diplomatie* eher zu selten vergeben; Veränderungen über die Zeit sind "
                       "verlässlicher als die Höhe. Der Ton wird nicht ausgewertet.",
        "topic_phase": "Phase", "all_period": "ganzer Zeitraum", "topic_view": "Ansicht",
        "topic_v_bars": "Alle Themen in einer Phase", "topic_v_lines": "Ein Thema über die Phasen",
        "topic": "Thema", "share": "Anteil der Beiträge (%)", "topic_level": "Quellen",
        # activity
        "act_metric": "Kennzahl", "m_posts": "Beiträge pro Tag und Kanal", "m_views": "Aufrufe pro Beitrag (Median)",
        "m_forwards": "Weiterleitungen pro Beitrag (Median)", "m_fw1000": "Weiterleitungen pro 1.000 Aufrufe",
        "act_note": "Aufrufe hängen vor allem an der Zahl der Abonnenten (nicht erhoben): Sie beschreiben "
                    "Reichweite, nicht Qualität.",
        # about
        "about": """
### Worum es geht
Sechs iranische Nachrichtenkanäle auf Telegram, **328.330 Beiträge** vom 01.01. bis 31.08.2026 – die Zeit der Proteste
zum Jahreswechsel, des Krieges zwischen Israel, den USA und Iran ab dem 28.02., der Waffenruhe und ihres
Zusammenbruchs. Verglichen werden drei Gruppen: **staatlich** (IRNA, IRIB News, Mehr News), **IRGC-nah** (Tasnim, Fars)
und **reformorientiert** (Jamaran).

### Wie gerechnet wird
- Alle Beiträge sind in einer Datenbank bereinigt und vollständig ausgezählt. Die Tabellen hier sind Zählwerte pro
  Woche, Gruppe und Kanal – **ohne Beitragstexte** (Urheberrecht).
- „pro 1.000 Wörter“ macht Gruppen und Wochen mit unterschiedlich vielen Beiträgen vergleichbar.
- Themen hat ein lokal betriebenes Sprachmodell (Gemma 4 31B) für 10.750 Beiträge vergeben; die Trefferquote wurde an
  200 neuen, von Hand geprüften Beiträgen gemessen.

### Grenzen
- **Überblick, keine Tiefenanalyse:** Das Projekt ist vor allem technisch. Eine wissenschaftliche Studie müsste die
  Beiträge einzeln lesen und würde 100 Seiten und mehr umfassen.
- **Eine Person:** Die Referenz für die Prüfung der KI und das Codebuch stammen von einer Person und spiegeln ihre
  Sicht. Besser wäre Gruppenarbeit: Zwei bis drei persische Muttersprachler kodieren unabhängig, die Übereinstimmung
  wird gemessen und das Codebuch gemeinsam diskutiert. Für andere Fragestellungen (Sicherheit, Politikwissenschaft,
  Ideologie) lässt es sich anpassen.
- **Wortwahl, keine Bewertung:** Begriffe – auch abwertende oder feindselige – stehen so da, wie sie in den Quellen
  stehen. Sie sind die Wortwahl der Kanäle, nicht die Meinung des Autors; die Auswertung bewertet nichts moralisch oder
  politisch, und der Autor hegt keine Feindseligkeit gegenüber Juden oder Amerikanern.
- **Weitere Abfragen:** Weitere SQL-Abfragen, die der Autor zum eigenen Verständnis ausgeführt hat, sind nicht
  veröffentlicht. Das Projekt ist schon sehr umfangreich; mehr Material würde Leser ohne Vorkenntnis eher verwirren.
- **Zählen ist nicht Verstehen:** Ein Begriff zählt gleich, ob zustimmend, distanziert oder zitierend.
- Die Zuordnung von Wochen zu Ereignissen ist eine Deutung. Die Linien im Diagramm sind Ereignisse aus
  dem Hintergrundmaterial des Projekts.
- Das Reformlager ist nur durch **einen** Kanal vertreten.
- Der Ton der KI ist nicht verlässlich genug für Gruppenvergleiche und wird nicht gezeigt.

### Mehr
[Kurzer Artikel](https://github.com/Amirhouschang/telegram-iran/blob/main/docs/de/bericht.md) ·
[Analyse mit allen Diagrammen](https://github.com/Amirhouschang/telegram-iran/blob/main/docs/de/04_analyse.md) ·
[Code und Methode auf GitHub](https://github.com/Amirhouschang/telegram-iran)
""",
    },
    "en": {
        "title": "Iranian News Channels 2026",
        "subtitle": "Interactive analysis of 328,330 Telegram posts from six Iranian channels "
                    "(1 Jan–31 Aug 2026): wording, countries, topics and activity.",
        "tab_time": "Wording over time", "tab_countries": "Countries", "tab_topics": "Topics (AI)",
        "tab_activity": "Activity", "tab_about": "About the project",
        "missing": "The file {file} is missing. It is produced by {script}.",
        "category": "Category", "view": "Compare", "view_groups": "Groups (one term)",
        "view_terms": "Terms (one source)", "term": "Term", "terms": "Terms",
        "sum_category": "Sum of the whole category", "value": "Value",
        "v_per1000": "per 1,000 words", "v_share": "share within the category (%)", "v_count": "number of mentions",
        "y_per1000": "per 1,000 words", "y_share": "share of all terms of the category (%)",
        "y_count": "mentions per week", "level": "Sources", "by_groups": "3 groups", "by_channels": "6 channels",
        "source": "Source", "show_events": "Events", "show_phases": "Phases",
        "week_of": "Week from", "complete_weeks": "Complete weeks only (7 days of data); weeks start on Monday.",
        "terms_note": "The terms are Persian; the translation comes first.",
        "select_one_term": "Select at least one term.",
        "peak_marker": "◆ = highest week of each line.",
        "phase_title": "Average in the four phases",
        "phase_note": "Mean of the complete weeks that start in the phase (same value as in the chart above).",
        "rank_title": "The terms of the category compared",
        "rank_note": "Mean of the weekly values over the whole period; the eight most frequent terms, the three groups only.",
        "rank_title_c": "The most mentioned countries and actors of the region",
        "rank_note_c": "Whole period, the twelve most frequent of the chosen region, the three groups only.",
        "kpi_posts": "Posts", "kpi_channels": "Channels", "kpi_groups": "Groups", "kpi_days": "Days",
        "col_group": "Group",
        "all_regions": "all regions",
        "region": "Region", "country": "Country / actor", "countries": "Countries / actors",
        "countries_note": "Only the naming of the country is counted. Groups only, no single channels.",
        "view_groups_c": "Groups (one country)", "view_terms_c": "Countries (one group)",
        "phases_title": "Mentions per 1,000 words by phase",
        "col_phase": "Phase",
        "topics_warn": "**Caution:** The AI classified 10,750 posts (weighted to all posts with more than 80 "
                       "characters). The topic is correct in 72.5% of cases (95% interval 65.9–78.2%). *Military* "
                       "tends to be assigned too often, *diplomacy* too rarely; changes over time are more reliable "
                       "than levels. Tone is not evaluated.",
        "topic_phase": "Phase", "all_period": "whole period", "topic_view": "View",
        "topic_v_bars": "All topics in one phase", "topic_v_lines": "One topic across the phases",
        "topic": "Topic", "share": "Share of posts (%)", "topic_level": "Sources",
        "act_metric": "Measure", "m_posts": "Posts per day and channel", "m_views": "Views per post (median)",
        "m_forwards": "Forwards per post (median)", "m_fw1000": "Forwards per 1,000 views",
        "act_note": "Views depend mostly on the number of subscribers (not collected): they describe reach, "
                    "not quality.",
        "about": """
### What this is about
Six Iranian news channels on Telegram, **328,330 posts** from 1 January to 31 August 2026 – the period of the protests
at the turn of the year, the war between Israel, the US and Iran from 28 February, the ceasefire and its collapse.
Three groups are compared: **state** (IRNA, IRIB News, Mehr News), **IRGC-affiliated** (Tasnim, Fars) and
**reformist** (Jamaran).

### How it is calculated
- All posts are cleaned in a database and counted in full. The tables here are counts per week, group and channel –
  **without post texts** (copyright).
- "per 1,000 words" makes groups and weeks with different numbers of posts comparable.
- Topics were assigned by a locally run language model (Gemma 4 31B) for 10,750 posts; its accuracy was measured on
  200 new, hand-checked posts.

### Limits
- **Overview, not an in-depth analysis:** The project is primarily technical. A scholarly study would have to read the
  posts individually and would run to 100 pages or more.
- **One person:** The reference for checking the AI and the codebook come from one person and reflect his view. Group
  work would be better: two or three native Persian speakers code independently, their agreement is measured and the
  codebook is discussed together. It can be adapted to other questions (security, political science, ideology).
- **Wording, no judgement:** Terms – including derogatory or hostile ones – appear as they do in the sources. They are
  the wording of the channels, not the author's opinion; the analysis makes no moral or political judgement, and the
  author harbours no hostility towards Jews or Americans.
- **Further queries:** Further SQL queries that the author ran for his own understanding are not published. The project
  is already very extensive; more material would confuse readers without prior knowledge.
- **Counting is not understanding:** a term counts the same whether used approvingly, at a distance or as a quotation.
- Assigning weeks to events is an interpretation. The lines in the charts are events from the project's
  background material.
- The reformist camp is represented by **one** channel only.
- The AI's tone is not reliable enough for group comparisons and is not shown.

### More
[Short article](https://github.com/Amirhouschang/telegram-iran/blob/main/docs/en/report.md) ·
[Analysis with all charts](https://github.com/Amirhouschang/telegram-iran/blob/main/docs/en/04_analysis.md) ·
[Code and method on GitHub](https://github.com/Amirhouschang/telegram-iran)
""",
    },
}
