"""
04_clean_text.py – Clean and normalise the Persian post texts in the database
==============================================================================

RUN (in the folder scripts/database, after 02_load_database.py):
  python 04_clean_text.py

WHAT IT DOES (the original column 'text' is never changed)
  1. removes channel advertising ("follow us on ..."), links, @mentions and emojis
  2. normalises Persian script:
       Arabic letter variants -> Persian (ي ى -> ی, ك -> ک, ة -> ه); the Persian letters پ چ ژ گ stay as they are
       Arabic and Latin digits -> Persian digits
       removes diacritics (e.g. شَهید -> شهید) and the stretching character ـ (e.g. ســـلام -> سلام)
       half-space instead of a space after the prefix می / نمی (می گوید -> می‌گوید); words like میدان stay unchanged
  3. splits the text into words and removes stop words (stopwords_fa.txt, from hazm)
  and writes three columns into the table 'posts':
       text_clean – cleaned text   |   tokens – content words   |   word_count – number of words

WHY NOT THE LIBRARY hazm?
  hazm 0.10 forces numpy 1.24, which breaks pandas 3 in this environment. The same normalisation rules
  are therefore implemented here directly; only hazm's stop word list is used (MIT licence).
"""
import re
import time
import unicodedata
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg:///iran_media_2026"
STOPWORDS = {w.strip() for w in (Path(__file__).parent / "stopwords_fa.txt").read_text(encoding="utf-8").splitlines()
             if w.strip() and not w.startswith("#")}

ZWNJ = "\u200c"                  # zero-width non-joiner = Persian half-space – must be kept

# channel advertising ("follow us on ...", "see the website ...") – short lines with these phrases are dropped
SIGNATURE_LINE = re.compile(r"دنبال کنید|را در آدرس زیر ببینید|روی این لینک بزنید|عضو شوید")
SIGNATURE_MAX_LEN = 160               # longer lines are content: only the phrase is removed
SIGNATURE_WORDS = re.compile(r"لینک خبر|(?:\s-\s*)?\bLink\b", re.IGNORECASE)

URL = re.compile(r"https?://\S+|www\.\S+|\bt\.me/\S+|\b[\w.-]+\.(?:com|ir|net|org|news)(?:/\S*)?", re.IGNORECASE)
MENTION = re.compile(r"@\w+")
HASHTAG = re.compile(r"#(\w+)")
DIACRITICS = re.compile("[\u064b-\u065f\u0670\u0640]")   # vowel marks, superscript alef, tatweel
MI_PREFIX = re.compile(r"(?<![\w\u200c])(ن?می) (?=[\u0600-\u06ff])")   # only "می گوید" with a space; "میدان" stays
LETTERS = str.maketrans({
    "ي": "ی",   # Arabic yeh    -> Persian yeh  (ي -> ی)
    "ى": "ی",   # alef maksura  -> Persian yeh  (ى -> ی)
    "ك": "ک",   # Arabic kaf    -> Persian kaf  (ك -> ک)
    "ة": "ه",   # teh marbuta   -> heh          (ة -> ه)
    **{chr(0x0660 + i): chr(0x06f0 + i) for i in range(10)},   # Arabic digits -> Persian digits
    **{str(i): chr(0x06f0 + i) for i in range(10)},            # Latin digits  -> Persian digits
})
WORD = re.compile("[\u0621-\u063a\u0641-\u064a\u067e\u0686\u0698\u06a9\u06af\u06cc\u06c0\u200c]+")   # Persian letters


def remove_symbols(t):
    """Removes emojis and pictographic symbols; keeps letters, digits, punctuation and the half-space."""
    return "".join(
        ch for ch in t
        if ch == ZWNJ or not (
            unicodedata.category(ch) in ("So", "Sk", "Cs", "Co")    # emojis and other symbols
            or ch in "\u200d\ufe0e\ufe0f"                   # emoji joiners and variation selectors
            or 0x2190 <= ord(ch) <= 0x21ff                         # arrows
            or 0x25a0 <= ord(ch) <= 0x25ff                         # geometric shapes, e.g. black squares
            or 0x2b00 <= ord(ch) <= 0x2bff))                       # more arrows and shapes


def clean(raw):
    if not isinstance(raw, str) or not raw.strip():
        return ""
    lines = []
    for line in raw.splitlines():
        if SIGNATURE_LINE.search(line):
            if len(line) <= SIGNATURE_MAX_LEN:
                continue                                           # pure advertising line
            line = SIGNATURE_LINE.sub(" ", line)
        lines.append(line)
    t = "\n".join(lines)
    t = SIGNATURE_WORDS.sub(" ", t)
    t = URL.sub(" ", t)
    t = MENTION.sub(" ", t)
    t = HASHTAG.sub(lambda m: m.group(1).replace("_", " "), t)
    t = remove_symbols(t)
    t = t.translate(LETTERS)
    t = DIACRITICS.sub("", t)
    t = MI_PREFIX.sub(lambda m: m.group(1) + ZWNJ, t)
    t = re.sub("\u200c{2,}", ZWNJ, t)                          # double half-spaces
    t = re.sub(" ?\u200c ?", ZWNJ, t)                          # half-space next to a space
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()


def words(t):
    return [w.strip(ZWNJ) for w in WORD.findall(t) if w.strip(ZWNJ)]


def main():
    engine = create_engine(DATABASE_URL)
    with engine.begin() as con:                                    # older databases: add the columns
        for col, typ in [("text_clean", "TEXT"), ("tokens", "TEXT"), ("word_count", "INTEGER")]:
            con.execute(text(f"ALTER TABLE posts ADD COLUMN IF NOT EXISTS {col} {typ}"))

    start = time.time()
    df = pd.read_sql("SELECT channel_id, post_id, text FROM posts", engine)
    print(f"{len(df)} posts read")

    df["text_clean"] = df["text"].map(clean)
    all_words = df["text_clean"].map(words)
    df["word_count"] = all_words.map(len)
    df["tokens"] = all_words.map(lambda ws: " ".join(w for w in ws if w not in STOPWORDS and len(w) > 1))
    print(f"cleaned in {time.time() - start:.0f} s")

    # write back: temporary table + one UPDATE (much faster than row by row)
    out = df[["channel_id", "post_id", "text_clean", "tokens", "word_count"]]
    out.to_sql("tmp_clean", engine, if_exists="replace", index=False, chunksize=5_000, method="multi")
    with engine.begin() as con:
        con.execute(text("""
            UPDATE posts p
            SET text_clean = t.text_clean, tokens = t.tokens, word_count = t.word_count
            FROM tmp_clean t
            WHERE p.channel_id = t.channel_id AND p.post_id = t.post_id
        """))
        con.execute(text("DROP TABLE tmp_clean"))
    print(f"written to the database, {time.time() - start:.0f} s in total\n")

    # check
    summary = pd.read_sql("""
        SELECT c.name AS channel,
               COUNT(*) AS posts,
               ROUND(100.0 * AVG((word_count = 0)::int), 1) AS no_text_pct,
               ROUND(AVG(word_count) FILTER (WHERE word_count > 0)) AS avg_words
        FROM posts p JOIN channels c ON c.channel_id = p.channel_id
        GROUP BY c.channel_id, c.name ORDER BY c.channel_id
    """, engine)
    print(summary.to_string(index=False))

    print("\nExamples (original -> cleaned):")
    for _, r in df[df["word_count"] > 5].sample(3, random_state=1).iterrows():
        print("-" * 80)
        print(r["text"][:300])
        print("  ->")
        print(r["text_clean"][:300])


if __name__ == "__main__":
    main()
