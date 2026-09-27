"""
04_context.py – Show in which context a word or term is used
=============================================================

RUN (in the folder scripts/analysis):
  python 04_context.py اسلامی
  python 04_context.py "امور خارجه"
  python 04_context.py رژیم --examples 30

WHAT IT SHOWS (in the terminal only – no file, because it contains post texts)
  1. the most frequent words directly BEFORE and AFTER the term, with count
  2. random example sentences with channel and link, to read what is meant
  e.g. اسلامی: is it جمهوری اسلامی, انقلاب اسلامی, کشورهای اسلامی ... ?
"""
import argparse
import random
import re
from collections import Counter
import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg:///iran_media_2026"
TOP_NEIGHBOURS = 20
SEGMENT_BREAK = re.compile(r"[\n.،,؛;:!؟?«»\"'()\[\]{}|/\\\-–—_…]+")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("term", help="word or term in Persian, several words in quotes")
    parser.add_argument("--examples", type=int, default=15, help="number of example sentences")
    args = parser.parse_args()
    target = args.term.split()
    n = len(target)

    engine = create_engine(DATABASE_URL)
    df = pd.read_sql(text("""
        SELECT c.name AS channel, p.post_url, p.text_clean
        FROM posts p JOIN channels c ON c.channel_id = p.channel_id
        WHERE p.text_clean LIKE :pattern
    """), engine, params={"pattern": f"%{args.term}%"})

    before, after, examples = Counter(), Counter(), []
    for channel, url, t in df.itertuples(index=False):
        for segment in SEGMENT_BREAK.split(t):
            words = segment.split()
            for i in range(len(words) - n + 1):
                if words[i:i + n] == target:
                    before[words[i - 1] if i > 0 else "(start)"] += 1
                    after[words[i + n] if i + n < len(words) else "(end)"] += 1
                    examples.append((channel, url, segment.strip()))

    total = sum(before.values())
    print(f"\n'{args.term}': {total} places in {df.shape[0]} posts\n")
    if not total:
        return

    left, right = before.most_common(TOP_NEIGHBOURS), after.most_common(TOP_NEIGHBOURS)
    print(f"{'word before':>25} {'count':>7}   {'word after':>25} {'count':>7}")
    for i in range(max(len(left), len(right))):
        l = left[i] if i < len(left) else ("", "")
        r = right[i] if i < len(right) else ("", "")
        print(f"{l[0]:>25} {l[1]:>7}   {r[0]:>25} {r[1]:>7}")

    print(f"\n{min(args.examples, len(examples))} random examples:")
    random.seed(42)
    for channel, url, segment in random.sample(examples, min(args.examples, len(examples))):
        print("-" * 80)
        print(f"{channel} | {url}")
        print(segment[:250])


if __name__ == "__main__":
    main()
