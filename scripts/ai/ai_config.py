"""
ai_config.py – ALL SETTINGS IN ONE PLACE
========================================
Change models, sample sizes and context here (and only here).
You do not need to open scripts 03a and 03 for this.

Which file does what?
  ai_config.py     -> settings (this file)
  codebook.py      -> categories, definitions, rules (content for the AI)
  background.txt   -> background knowledge (events, people, glossary) – plain text
  ai_core.py       -> technology (requests to Ollama) – normally no need to touch
"""
from pathlib import Path

# ---------------------------------------------------------------
# PATHS – this script lives in telegram-iran/scripts/ai/
# parents[2] goes up two folders -> telegram-iran/
# ---------------------------------------------------------------
PROJECT = Path(__file__).resolve().parents[2]

# Raw data: list of all files – the scripts read them and stack them on top of each other.
# New file? Just add a line.
INPUT_FILES = [
    PROJECT / "data" / "row" / "telegram_jan_aug_2026.csv",          # IRNA, IRIB News, Mehr, Tasnim, Fars
    PROJECT / "data" / "row" / "telegram_reform_jan_aug_2026.csv",   # Jamaran
]
OUTPUT_DIR = PROJECT / "data" / "ki"                                # all AI results
BACKGROUND_FILE = Path(__file__).resolve().parent / "background.txt"

# ---------------------------------------------------------------
# OLLAMA
# ---------------------------------------------------------------
OLLAMA = "http://localhost:11434"
CONTEXT_LENGTH = 8192    # num_ctx: room for codebook + background + post
MAX_CHARS = 2000         # maximum number of characters of a post given to the AI
TIMEOUT = 900            # seconds before a request counts as failed

# ---------------------------------------------------------------
# MODEL COMPARISON (03a)
# ---------------------------------------------------------------
# Every model is tested with every context variant. Missing models are skipped.
# gpt-oss:120b (66 GB) was removed: it exhausted the memory of the test machine.
COMPARISON_MODELS = [
    "gemma4:26b",
    "gemma4:31b",
    "qwen3.6:27b",
    "qwen3.6:35b",
    "qwen2.5:32b",
    "aya-expanse:32b",
]
CONTEXT_VARIANTS = [True]            # with background only (result of the first comparison)
PER_CHANNEL_TESTSET = 25             # when drawing a new test set: 25 x 6 channels = 150 posts

# ---------------------------------------------------------------
# MAIN RUN (03) – chosen after the model comparison (codebook v8, testset2)
# ---------------------------------------------------------------
CLASSIFICATION_MODEL = "gemma4:31b"
CLASSIFICATION_CONTEXT = True
PER_CHANNEL_WEEK = 50                # stratified sample: 50 per channel and week (~10,500 posts)
                                     # weeks with fewer posts: take all of them
PER_CHANNEL_TEST_RUN = 4             # test run with --test (4 per channel)
SAMPLE_SEED = 42                     # same number = same sample on every start
