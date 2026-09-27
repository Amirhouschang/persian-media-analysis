"""
06_leader_mentions.py – Which Khamenei is meant, and when was Mojtaba Khamenei first called leader?
=====================================================================================================

RUN (in the folder scripts/analysis):
  python 06_leader_mentions.py                   # tables + first dates
  python 06_leader_mentions.py --check mojtaba   # 30 random posts of one category to read (ali / mojtaba / both)

WHY
  خامنه‌ای and رهبر can mean Ali Khamenei (killed in the war) or his son Mojtaba Khamenei (his successor).
  Thousands of posts cannot be read, so the post is assigned by rules; the author checks a random sample.

RULES (per post that mentions the leader)
  mojtaba – مجتبی خامنه‌ای is named (سید مجتبی alone is not enough: often another person, e.g. سیدمجتبی حسینی),
            or the post is from APPOINTMENT_DAY or later and has no hint to Ali (رهبر alone = the new leader)
  ali     – سید علی خامنه‌ای, رهبر شهید, قائد شهید, امام شهید, امام خامنه‌ای, آیت‌الله العظمی, مرجع عالیقدر,
            سوگ رهبر, مراسم تشییع, اربعین رهبر, فرزند رهبر, به شهادت رساندن ... is named
            (رهبر شهید حماس / حزب‌الله is excluded),
            or the post is from before APPOINTMENT_DAY (see below)
  both    – both of the above (e.g. posts about the succession)
  (his brothers and other sons – محمد, هادی, محمدباقر, مصطفی, مسعود, میثم خامنه‌ای – are removed first;
   posts only about them are not counted)
  Until APPOINTMENT_DAY, رهبر without a name means Ali Khamenei – also in the week between his death and the
  appointment. Checked by the author: in a random sample of 50 posts from 1–8 March without any name or hint,
  all 50 referred to Ali Khamenei (earlier version of this script: category "unclear").

FIRST DATES (per channel)
  first day with رهبر شهید, first day Mojtaba is named, and first day Mojtaba and رهبر stand in the same sentence
  (= called leader; not counted: فرزند/پسر رهبر = son of the leader, رهبر سابق/شهید, مجلس خبرگان رهبری); the sentence is printed so it can be checked. Compared with APPOINTMENT_DAY (official date):
  how many days after the official appointment each channel first called him leader.

OUTPUT (folder results/leader, only numbers, no post texts – for GitHub)
  leader_mentions.xlsx – sheet 'by_channel_phase' (counts and shares), sheet 'first_dates'
  leader_mentions.csv  – counts per channel, phase and category

CHECK FILE (folder data/check – WITH post texts, private, not for GitHub)
  leader_check.xlsx – sheet 'first_dates' with the sentences, and per category 'sample_ali', 'sample_mojtaba',
                      'sample_both' with SAMPLE_SIZE random posts (channel, date, link, text)
"""
import argparse
import datetime as dt
import random
import re
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg:///iran_media_2026"

# official dates (entered by the author)
DEATH_DAY = dt.date(2026, 3, 1)        # killed on 28 Feb; death officially confirmed in Iran on 1 Mar.
                                       # Until then Iranian media still wrote about him as the living leader.
APPOINTMENT_DAY = dt.date(2026, 3, 8)  # Mojtaba Khamenei officially appointed leader after the election
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "results" / "leader"
CHECK_DIR = Path(__file__).resolve().parents[2] / "data" / "check"      # private: contains post texts
SAMPLE_SIZE = 50
SEGMENT_BREAK = re.compile(r"[\n.،,؛;:!؟?«»\"'()\[\]{}|/\\…]+")

LEADER = re.compile(r"خامنه\u200cای|سید ?مجتبی|رهبر انقلاب|رهبر معظم|مقام معظم رهبری|رهبر شهید|قائد شهید|سومین رهبر|رهبر جدید")
MOJTABA = re.compile(r"مجتبی (حسینی )?خامنه\u200cای")          # only with Khamenei: سید مجتبی alone is often another person
ALI = re.compile(r"سید ?علی (حسینی )?خامنه\u200cای|رهبر شهید(?!\s*(?:حماس|حزب|جهاد|مقاومت))|قائد شهید|امام شهید"
                 r"|امام مجاهد شهید|رهبر فقید|آقای شهید|سوگ رهبر|شهادت رهبر|ترور رهبر|تشییع (?:پیکر )?(?:مطهر )?رهبر"
                 r"|اربعین رهبر|امام خامنه\u200cای|آیت\u200c?الله[\u200c ]?العظمی|مرجع عالیقدر|به شهادت رساندن"
                 r"|فرزند رهبر|مراسم تشییع|تشییع باشکوه|تشییع پیکر")    # killed Hamas/Hezbollah leaders excluded
OTHER_KHAMENEI = re.compile(r"(?:سید ?)?(?:محمد|هادی|محمدباقر|مصطفی|مسعود|میثم) (?:حسینی )?خامنه\u200cای")   # brothers and other sons, removed first
LEADER_WORD = re.compile(r"(?<!فرزند )(?<!پسر )(?<!خبرگان )رهبر(?!\s*(?:شهید|سابق|فقید))")   # not "son of the leader", not "former/killed leader", not "Assembly of Experts"
CATEGORIES = ["ali", "mojtaba", "both"]


def read_posts(engine):
    df = pd.read_sql("""
        SELECT c.channel_id, c.name AS channel, ph.phase_id, ph.name AS phase, d.date, p.post_url, p.text_clean
        FROM posts p
        JOIN channels c ON c.channel_id = p.channel_id
        JOIN dates d    ON d.date_key   = p.date_key
        JOIN phases ph  ON ph.phase_id  = d.phase_id
        WHERE p.text_clean ~ 'خامنه|مجتبی|رهبر'
    """, engine)
    # Python regex via map: pandas 3 (pyarrow) does not understand \u200c inside a pattern
    return df[df["text_clean"].map(lambda t: bool(LEADER.search(t)))].copy()


def categorise(row, death_day):
    ali_named = bool(ALI.search(row.text_leader))
    m = bool(MOJTABA.search(row.text_leader)) or (row.date >= APPOINTMENT_DAY and not ali_named)
    a = ali_named or row.date < APPOINTMENT_DAY                      # until the appointment, the leader is Ali
    return "both" if m and a else "mojtaba" if m else "ali"


def first_dates(df):
    rows = []
    for channel, part in df.sort_values("date").groupby("channel", sort=False):
        entry = {"channel": channel}
        for label, test in [
            ("first_rahbar_shahid", lambda s: bool(re.search(r"رهبر شهید(?!\s*(?:حماس|حزب|جهاد|مقاومت))", s))),
            ("first_mojtaba_named", lambda s: bool(MOJTABA.search(s))),
            ("first_mojtaba_as_leader", lambda s: bool(MOJTABA.search(s)) and bool(LEADER_WORD.search(s))),
        ]:
            entry[label], entry[label + "_url"], entry[label + "_sentence"] = None, None, None
            for r in part.itertuples():
                hit = next((seg for seg in SEGMENT_BREAK.split(r.text_leader) if test(seg)), None)
                if hit:
                    entry[label], entry[label + "_url"], entry[label + "_sentence"] = r.date, r.post_url, hit.strip()
                    break
        rows.append(entry)
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", choices=CATEGORIES, help="print 30 random posts of this category")
    args = parser.parse_args()

    engine = create_engine(DATABASE_URL)
    df = read_posts(engine)
    df["text_leader"] = df["text_clean"].map(lambda t: OTHER_KHAMENEI.sub(" ", t))   # without his brothers
    df = df[df["text_leader"].map(lambda t: bool(LEADER.search(t)))].copy()
    if DEATH_DAY is None or APPOINTMENT_DAY is None:
        print("Please enter DEATH_DAY and APPOINTMENT_DAY at the top of the script first.")
        return
    df["category"] = [categorise(r, DEATH_DAY) for r in df.itertuples()]
    print(f"{len(df)} posts mention the leader (death {DEATH_DAY}, appointment {APPOINTMENT_DAY})\n")

    if args.check:
        part = df[df["category"] == args.check]
        random.seed(42)
        for r in random.sample(list(part.itertuples()), min(30, len(part))):
            print("-" * 80)
            print(f"{r.channel} | {r.date} | {r.post_url}")
            print(r.text_clean[:300])
        return

    counts = (df.groupby(["channel_id", "channel", "phase_id", "phase", "category"]).size()
              .unstack("category", fill_value=0).reindex(columns=CATEGORIES, fill_value=0).reset_index())
    total = counts[CATEGORIES].sum(axis=1)
    for c in CATEGORIES:
        counts[f"{c}_pct"] = (100 * counts[c] / total).round().astype(int)
    counts = counts.sort_values(["channel_id", "phase_id"]).drop(columns=["channel_id", "phase_id"])

    firsts = first_dates(df)
    firsts["days_after_appointment"] = [(d - APPOINTMENT_DAY).days if pd.notna(d) else None
                                        for d in firsts["first_mojtaba_as_leader"]]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    counts.to_csv(OUTPUT_DIR / "leader_mentions.csv", index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(OUTPUT_DIR / "leader_mentions.xlsx") as xl:
        counts.to_excel(xl, sheet_name="by_channel_phase", index=False)
        firsts.drop(columns=[c for c in firsts.columns if c.endswith("_sentence")]).to_excel(
            xl, sheet_name="first_dates", index=False)

    print(counts.to_string(index=False))
    print("\nFirst dates (check the sentence):")
    for r in firsts.itertuples():
        print("-" * 80)
        print(f"{r.channel}: رهبر شهید {r.first_rahbar_shahid} | Mojtaba named {r.first_mojtaba_named} | "
              f"Mojtaba as leader {r.first_mojtaba_as_leader} ({r.days_after_appointment} days after appointment)")
        print(f"  {r.first_mojtaba_as_leader_url}\n  {str(r.first_mojtaba_as_leader_sentence)[:200]}")
    CHECK_DIR.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(CHECK_DIR / "leader_check.xlsx") as xl:
        firsts.to_excel(xl, sheet_name="first_dates", index=False)
        for c in CATEGORIES:
            part = df[df["category"] == c]
            part.sample(min(SAMPLE_SIZE, len(part)), random_state=42).sort_values("date")[
                ["channel", "date", "phase", "post_url", "text_clean"]].to_excel(
                xl, sheet_name=f"sample_{c}", index=False)

    print(f"\nsaved to {OUTPUT_DIR}")
    print(f"check file WITH texts (do not upload): {CHECK_DIR / 'leader_check.xlsx'}")


if __name__ == "__main__":
    main()
