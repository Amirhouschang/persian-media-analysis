"""
03_terms.py – Most frequent terms (one to four words) per channel, source group and phase – every word counted once
=====================================================================================================================

RUN (in the folder scripts/analysis, after scripts/database/04_clean_text.py):
  python 03_terms.py

WHY
  01 counts single words, 02 counts neighbouring words. Both count the same place in a text several times:
  in رژیم صهیونیستی, the words رژیم and صهیونیستی are counted as well. This script counts every place ONCE:
      ... وزیر امور خارجه گفت          -> one term: وزیر امور خارجه
      ... وزارت امور خارجه اعلام کرد    -> one term: وزارت امور خارجه
      ... حمله رژیم به لبنان            -> رژیم counts on its own, because صهیونیستی does not follow
  No word list is given in advance.

HOW
  1. Find fixed terms of 2 to MAX_WORDS neighbouring content words (no stop words, no numbers, no punctuation).
     A sequence is a fixed term if it occurs at least PHRASE_MIN_COUNT times in all posts, and
       - two words: at least PHRASE_SHARE of the occurrences of its rarer word are inside this pair
           تنگه هرمز, شورای امنیت (شورای is mostly followed by امنیت, even if امنیت is a common word)
       - three or four words: at least PHRASE_SHARE of the occurrences of BOTH shorter parts are inside it
           وزیر امور خارجه    -> a large share of امور خارجه and of وزیر امور           -> fixed term
           حمله رژیم صهیونیستی -> only a small share of رژیم صهیونیستی                    -> free combination, not a term
       - an office word (e.g. وزیر, رئیس, سخنگوی) may only be the FIRST word of a term, so a person and his
         office are not joined:  وزیر امور خارجه -> term;  عباس عراقچی وزیر امور -> no term
  2. Corrections by the author in phrase_corrections.csv (same folder), column 'action':
       title  – office word for the rule above
       add    – longer names that are one term, e.g. نیروی دریایی سپاه پاسداران انقلاب اسلامی (6 words)
       remove – terms found automatically that are wrong
       ignore – terms without content (e.g. خواهد, قرار, channel names); counted, but left out of the lists
                (candidates: 05_noise_candidates.py)
       merge  – spelling or name variants counted as one term, target in column 'into'
                (سید عباس عراقچی -> عراقچی, رئیس جمهور -> رئیس‌جمهور)
     The final list of fixed terms is saved (phrases.csv, column 'source': auto or added) so it can be checked.
  3. In every text, fixed terms are joined: longer terms first; if two terms of the same length overlap,
     the more frequent one wins (حمله رژیم صهیونیستی -> حمله + رژیم صهیونیستی).
  4. Every term – single word or fixed term – is counted once per place.
  5. Spellings that differ only by the half-space are counted as one (بزرگترین / بزرگ‌ترین).
     Singular and plural stay separate on purpose: کشور (often Iran itself) vs. کشورهای (other countries).
  Frequencies per 1,000 words, in the same order as 01 and 02: each channel, each group, then per phase.

OUTPUT (folder results/words)
  phrases.csv – all fixed terms, with source (auto / added), share in percent (share_pct),
                count      = places of the word sequence, also inside longer terms – a LOWER BOUND: only the channel/phase
                             parts in which the sequence occurs at least MIN_COUNT (5) times are summed, so up to 4 places
                             per part (96 over the 24 parts) are missing; count is the basis of the selection of the fixed
                             terms (PHRASE_MIN_COUNT, PHRASE_SHARE) and decides which of two overlapping terms of the same
                             length wins
                count_used = places where it was counted as this term (exact, before spelling variants are merged; basis of terms.csv)
                so count_used can be larger than count for a sequence that is rarely part of a longer term
                e.g. اسلامی ایران: high count, but count_used small – it stands mostly inside جمهوری اسلامی ایران
  terms.xlsx  – sheet 'channels', sheet 'groups', then one sheet per channel and per group with the phases
  terms.csv   – the same numbers as one long table (for later analysis and the dashboard)
"""
import re
from collections import Counter
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg:///iran_media_2026"
TOP_N = 1000                                                 # terms per list
MAX_WORDS = 4                                                # longest automatic term; longer names: phrase_corrections.csv
PHRASE_MIN_COUNT = 100                                       # a fixed term must occur at least this often
PHRASE_SHARE = 0.25                                          # see "HOW" above
MIN_COUNT = 5                                                # per channel and phase, rarer sequences are dropped early to save memory (missing from count)
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "results" / "words"
STOPWORD_FILE = Path(__file__).resolve().parents[1] / "database" / "stopwords_fa.txt"
CORRECTIONS_FILE = Path(__file__).resolve().parent / "phrase_corrections.csv"
ALL = "all"                                                  # name for the whole period
JOIN = "_"                                                   # joins the words of a fixed term inside the program

STOPWORDS = {w.strip() for w in STOPWORD_FILE.read_text(encoding="utf-8").splitlines()
             if w.strip() and not w.startswith("#")}
ZWNJ = "\u200c"
SEGMENT_BREAK = re.compile(r"[\n.،,؛;:!؟?«»\"'()\[\]{}|/\\\-–—_…]+")   # terms never cross these
WORD = re.compile("[\u0621-\u063a\u0641-\u064a\u067e\u0686\u0698\u06a9\u06af\u06cc\u06c0\u200c]+")


def runs(text):
    """Sequences of neighbouring content words; numbers, Latin words, stop words and punctuation break a sequence."""
    for segment in SEGMENT_BREAK.split(text):
        run = []
        for token in segment.split():
            word = token.strip(ZWNJ)
            if WORD.fullmatch(token) and len(word) > 1 and word not in STOPWORDS:
                run.append(word)
            else:
                if run:
                    yield run
                run = []
        if run:
            yield run


def load_corrections():
    """Author's decisions: office words, names to add, terms to remove."""
    if not CORRECTIONS_FILE.exists():
        return set(), set(), set(), set(), {}
    c = pd.read_csv(CORRECTIONS_FILE, encoding="utf-8-sig", dtype=str)
    if "into" not in c.columns:
        c["into"] = None
    c["action"] = c["action"].str.strip()
    c["term"] = c["term"].str.split().str.join(JOIN)
    get = lambda action: set(c.loc[c["action"] == action, "term"])
    merge = c[(c["action"] == "merge") & c["into"].notna()]
    merge_map = dict(zip(merge["term"], merge["into"].str.split().str.join(JOIN)))
    return get("title"), get("add"), get("remove"), {t.replace(JOIN, " ") for t in get("ignore")}, merge_map


def read_posts(engine):
    return pd.read_sql("""
        SELECT c.channel_id, c.name AS channel, g.group_id, g.name AS source_group,
               ph.phase_id, ph.name AS phase, p.text_clean, p.word_count
        FROM posts p
        JOIN channels c       ON c.channel_id = p.channel_id
        JOIN source_groups g  ON g.group_id   = c.group_id
        JOIN dates d          ON d.date_key   = p.date_key
        JOIN phases ph        ON ph.phase_id  = d.phase_id
        WHERE p.word_count > 0
    """, engine)


# ---------- step 1: find fixed terms ----------
def find_phrases(df, titles, added, removed):
    longest = max([MAX_WORDS] + [t.count(JOIN) + 1 for t in added])
    total = Counter()
    for _, part in df.groupby(["channel", "phase"]):                # per part, to keep memory small
        c = Counter()
        for text in part["text_clean"]:
            for run in runs(text):
                for n in range(1, MAX_WORDS + 1):
                    c.update(JOIN.join(run[i:i + n]) for i in range(len(run) - n + 1))
                for n in range(MAX_WORDS + 1, longest + 1):           # longer names only if added by the author
                    c.update(t for i in range(len(run) - n + 1) if (t := JOIN.join(run[i:i + n])) in added)
        total.update({t: n for t, n in c.items() if n >= MIN_COUNT})

    phrases = []
    for term, n in total.items():
        words = term.split(JOIN)
        if len(words) < 2 or n < PHRASE_MIN_COUNT or len(words) > MAX_WORDS or term in removed:
            continue
        if any(w in titles for w in words[1:]):                                   # person + office: no term
            continue
        if len(words) == 2:
            reference = min(total.get(w, n) for w in words)                       # the rarer word
        else:
            reference = max(total.get(JOIN.join(words[:-1]), n),                  # the more frequent of the
                            total.get(JOIN.join(words[1:]), n))                   # two shorter parts
        share = n / reference
        if share >= PHRASE_SHARE:
            phrases.append({"term": " ".join(words), "n_words": len(words), "count": n,
                            "share_pct": round(100 * share), "source": "auto"})   # whole percent: read correctly
    auto = {p["term"] for p in phrases}
    for term in added:
        if term.replace(JOIN, " ") not in auto:
            phrases.append({"term": term.replace(JOIN, " "), "n_words": term.count(JOIN) + 1,
                            "count": total.get(term, 0), "share_pct": None, "source": "added"})
    return pd.DataFrame(phrases, columns=["term", "n_words", "count", "share_pct", "source"]).sort_values(
        "count", ascending=False, ignore_index=True)


# ---------- step 2 and 3: join fixed terms and count every place once ----------
def merged_terms(text, phrases, longest):
    """Terms of one text: longer fixed terms first, if they overlap the more frequent one; the rest single words."""
    result = []
    for run in runs(text):
        candidates = [(n, phrases[t], i) for n in range(2, min(longest, len(run)) + 1)
                      for i in range(len(run) - n + 1) if (t := JOIN.join(run[i:i + n])) in phrases]
        taken, start = [False] * len(run), {}
        for n, _, i in sorted(candidates, key=lambda c: (-c[0], -c[1])):
            if not any(taken[i:i + n]):
                taken[i:i + n] = [True] * n
                start[i] = n
        i = 0
        while i < len(run):
            n = start.get(i, 1)
            result.append(JOIN.join(run[i:i + n]))
            i += n
    return result


def count_terms(df, phrases, merge_map, used=None):
    """One counter per channel and phase; all other combinations are sums of these.
    used (optional Counter): how often every fixed term was really counted, i.e. not inside a longer term."""
    longest = max(t.count(JOIN) + 1 for t in phrases) if phrases else 1
    counts, words = {}, {}
    for (channel, phase), part in df.groupby(["channel", "phase"]):
        c = Counter()
        for text in part["text_clean"]:
            found = merged_terms(text, phrases, longest)
            if used is not None:
                used.update(t for t in found if JOIN in t)
            c.update(merge_map.get(t, t) for t in found)
        counts[(channel, phase)] = c
        words[(channel, phase)] = part["word_count"].sum()
    return merge_zwnj_variants(counts), words


def merge_zwnj_variants(counts):
    """Spellings that differ only by the half-space are one word (بزرگترین / بزرگ‌ترین): the more frequent form wins.
    Singular and plural are NOT merged – کشور (often Iran) and کشورهای (other countries) mean different things."""
    total = Counter()
    for c in counts.values():
        total.update(c)
    forms = {}
    for term, n in total.items():
        forms.setdefault(term.replace(ZWNJ, ""), []).append((n, term))
    to = {t: max(v)[1] for v in forms.values() if len(v) > 1 for _, t in v}
    to = {t: target for t, target in to.items() if t != target}
    print(f"{len(to)} spellings with/without half-space merged")
    merged = {}
    for key, c in counts.items():
        m = Counter()
        for t, n in c.items():
            m[to.get(t, t)] += n
        merged[key] = m
    return merged


IGNORED = set()                                              # filled in main() from phrase_corrections.csv


def top_terms(counter, total_words, level, name, phase):
    counter = Counter({t: n for t, n in counter.items() if t.replace(JOIN, " ") not in IGNORED})
    return pd.DataFrame(
        [{"level": level, "name": name, "phase": phase, "rank": i, "term": t.replace(JOIN, " "),
          "n_words": t.count(JOIN) + 1, "count": n, "per_1000_words": round(1000 * n / total_words, 3)}
         for i, (t, n) in enumerate(counter.most_common(TOP_N), start=1)])


def build_table(df, counts, words):
    channels = df.drop_duplicates("channel").sort_values("channel_id")
    groups = df.drop_duplicates("source_group").sort_values("group_id")
    phases = df.drop_duplicates("phase").sort_values("phase_id")["phase"].tolist()

    rows = []
    for level, names, members in [
        ("channel", channels["channel"], lambda n: [n]),
        ("group", groups["source_group"], lambda n: channels.loc[channels["source_group"] == n, "channel"]),
    ]:
        for name in names:
            for phase in [ALL] + phases:
                c, total = Counter(), 0
                for ch in members(name):
                    for ph in (phases if phase == ALL else [phase]):
                        c += counts.get((ch, ph), Counter())
                        total += words.get((ch, ph), 0)
                rows.append(top_terms(c, total, level, name, phase))
    return pd.concat(rows, ignore_index=True), phases


def wide(table, level, names, phase_list):
    """Side by side: for every name/phase two columns (term, per 1,000 words)."""
    blocks = []
    for name in names:
        for phase in phase_list:
            part = table[(table["level"] == level) & (table["name"] == name) & (table["phase"] == phase)]
            title = name if phase == ALL else f"{name} – {phase}"
            blocks.append(part[["term", "per_1000_words"]].reset_index(drop=True)
                          .set_axis([title, "per 1,000 words"], axis=1))
    out = pd.concat(blocks, axis=1)
    out.index = out.index + 1
    out.index.name = "rank"
    return out


def main():
    engine = create_engine(DATABASE_URL)
    df = read_posts(engine)
    print(f"{len(df)} posts with text read")

    titles, added, removed, ignored, merge_map = load_corrections()
    IGNORED.update(ignored)
    print(f"corrections: {len(titles)} office words, {len(added)} names added, {len(removed)} terms removed, "
          f"{len(ignored)} terms ignored in the lists, {len(merge_map)} variants merged")
    phrases = find_phrases(df, titles, added, removed)
    print(f"{len(phrases)} fixed terms used")
    phrase_counts = dict(zip(phrases["term"].str.replace(" ", JOIN), phrases["count"]))

    used = Counter()
    counts, words = count_terms(df, phrase_counts, merge_map, used)
    table, phase_names = build_table(df, counts, words)
    # count = places of the word sequence (lower bound, see MIN_COUNT); count_used = places where it was counted as this term
    # (not inside a longer term): اسلامی ایران occurs often, but mostly inside جمهوری اسلامی ایران
    phrases["count_used"] = phrases["term"].str.replace(" ", JOIN).map(used).fillna(0).astype(int)
    phrases = phrases.sort_values("count_used", ascending=False, ignore_index=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    phrases.to_csv(OUTPUT_DIR / "phrases.csv", index=False, encoding="utf-8-sig")
    table.to_csv(OUTPUT_DIR / "terms.csv", index=False, encoding="utf-8-sig")

    channels = table.loc[table["level"] == "channel", "name"].unique()
    groups = table.loc[table["level"] == "group", "name"].unique()
    with pd.ExcelWriter(OUTPUT_DIR / "terms.xlsx") as xl:
        wide(table, "channel", channels, [ALL]).to_excel(xl, sheet_name="channels")
        wide(table, "group", groups, [ALL]).to_excel(xl, sheet_name="groups")
        for name in channels:
            wide(table, "channel", [name], phase_names).to_excel(xl, sheet_name=name[:31])
        for name in groups:
            wide(table, "group", [name], phase_names).to_excel(xl, sheet_name=name[:31])
    print(f"saved to {OUTPUT_DIR}\n")

    print("Most frequent fixed terms (as counted): " + "  |  ".join(phrases["term"].head(15)))
    for name in groups:
        top = table[(table["level"] == "group") & (table["name"] == name) & (table["phase"] == ALL)].head(10)
        print(f"{name}: " + "  |  ".join(top["term"]))


if __name__ == "__main__":
    main()
