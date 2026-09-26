"""
ai_core.py – TECHNOLOGY: build the prompt, ask Ollama, check the answer
=======================================================================
Used by 03a and 03. Normally you do not need to change anything here.
Because both scripts use THESE functions, they are guaranteed to work the same way.
"""
import json
import requests

import ai_config as cfg
from codebook import (TOPICS, TONES, RULE_1_NO_CONTEXT, RULE_1_WITH_CONTEXT,
                      FURTHER_RULES, CODEBOOK_VERSION, SOURCES, SOURCE_RULE)


def _as_list(d):
    """dictionary -> readable list '- key: definition'"""
    return "\n".join(f"- {k}: {v}" for k, v in d.items())


def load_background():
    """Reads background.txt. Missing or empty file -> empty text."""
    if cfg.BACKGROUND_FILE.exists():
        return cfg.BACKGROUND_FILE.read_text(encoding="utf-8").strip()
    return ""


def build_prompt(with_context, extended=False):
    """
    Assembles the instruction for the AI (without the post itself).
      with_context = True -> background knowledge from background.txt + overview of the sources
      extended     = True -> additionally actors + summary (optional, not used in the main run)
    """
    background = load_background() if with_context else ""
    rule_1 = RULE_1_WITH_CONTEXT if background else RULE_1_NO_CONTEXT

    parts = [
        "You are an analyst classifying Persian-language news posts.",
        "Read the post and choose exactly ONE topic and exactly ONE tone, using only the definitions below.",
        "",
        "TOPICS:", _as_list(TOPICS), "",
        "TONES (check in this order):", _as_list(TONES), "",
        "General rules:", rule_1, FURTHER_RULES,
    ]
    if with_context:
        parts += [SOURCE_RULE, "",
                  "NEWS SOURCES IN THIS DATASET (neutral description):", _as_list(SOURCES), ""]
    else:
        parts += [""]
    if background:
        parts += ["BACKGROUND (neutral facts, for understanding only):", background, ""]

    if extended:
        parts += [
            "Also list the states or organizations mentioned in the post (in English, max. 5)",
            "and write a one-sentence summary in English.",
            "",
            "Answer ONLY with JSON in this format:",
            '{"reason": "<one short sentence in English>", "topic": "<topic key>", "tone": "<tone key>",',
            ' "actors": ["<actor>", "..."], "summary": "<one sentence>"}',
        ]
    else:
        parts += [
            "Answer ONLY with JSON in this format:",
            '{"reason": "<one short sentence in English>", "topic": "<topic key>", "tone": "<tone key>"}',
        ]
    return "\n".join(parts) + "\n"


def installed_models():
    """Asks Ollama which models are installed."""
    response = requests.get(f"{cfg.OLLAMA}/api/tags", timeout=30)
    return {m["name"] for m in response.json()["models"]}


def unload(model):
    """Removes a model from memory before the next one starts."""
    try:
        requests.post(f"{cfg.OLLAMA}/api/generate",
                      json={"model": model, "keep_alive": 0}, timeout=60)
    except requests.RequestException:
        pass


def classify(model, text, with_context, extended=False, prompt=None, kanal=None):
    """
    Sends ONE post to ONE model and returns a clean result.
    If the JSON is broken, the model is asked once more.
    'prompt' can be passed ready-made so it is not rebuilt for every post.
    'kanal'  -> with context, the source of the post is stated before the post.
    """
    prompt = prompt or build_prompt(with_context, extended)
    source = ""
    if with_context and kanal in SOURCES:
        source = f"Source of this post: {SOURCES[kanal]}\n"
    content = f"{prompt}\n{source}Post:\n{str(text)[:cfg.MAX_CHARS]}"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "format": "json",           # enforce valid JSON
        "stream": False,            # answer in one piece
        "options": {
            "temperature": 0,       # no randomness
            "seed": 42,             # additionally: same input -> same output
            "num_ctx": cfg.CONTEXT_LENGTH,
        },
    }
    if model.startswith(("gemma4", "qwen3")):
        payload["think"] = False    # thinking mode off -> much faster
    elif model.startswith("gpt-oss"):
        payload["think"] = "low"    # gpt-oss cannot switch it off completely, only low/medium/high

    last_error = None
    for _ in range(2):              # at most 2 attempts
        try:
            response = requests.post(f"{cfg.OLLAMA}/api/chat", json=payload, timeout=cfg.TIMEOUT)
            answer = json.loads(response.json()["message"]["content"])
            break
        except (json.JSONDecodeError, KeyError) as e:
            last_error = e
    else:
        raise RuntimeError(f"No valid answer: {last_error}")

    topic = str(answer.get("topic", "")).strip().lower()
    tone = str(answer.get("tone", "")).strip().lower()
    result = {
        "topic": topic if topic in TOPICS else "invalid",   # invented category -> invalid
        "tone": tone if tone in TONES else "invalid",
        "reason": str(answer.get("reason", "")),
    }
    if extended:
        actors = answer.get("actors", []) or []
        result["actors"] = ", ".join(map(str, actors)) if isinstance(actors, list) else str(actors)
        result["summary"] = str(answer.get("summary", ""))
    return result


def run_name(model, with_context):
    """Short name for a run, e.g. 'gemma4:26b | context'"""
    return f"{model} | {'context' if with_context else 'no-context'}"


__all__ = ["build_prompt", "classify", "installed_models", "unload",
           "run_name", "TOPICS", "TONES", "CODEBOOK_VERSION"]
