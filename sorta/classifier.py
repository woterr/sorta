import re
from pathlib import Path
from datetime import datetime
import json
import re


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[-–—]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def keyword_score(text: str, keywords: list[str]) -> int:
    score = 0

    for kw in keywords:
        kw = kw.strip().lower()

        pattern = r"\b" + re.escape(kw) + r"\b"

        if re.search(pattern, text):
            score += 1

    return score


def pick_best(text: str, candidates: list[str], config: dict):
    best = None
    best_score = 0

    for name in candidates:
        meta = config["roots"][name]
        score = keyword_score(text, meta.get("keywords", []))

        if score > best_score:
            best_score = score
            best = name

    return best


def apply_rules(root_name, meta, text, config):
    def get_rule_keywords(root_meta, rule_name, config):
        overrides = root_meta.get("rule_overrides", {})
        if rule_name in overrides:
            return overrides[rule_name]["keywords"]
        return config["rules"][rule_name]["keywords"]

    base_path = meta["path"]

    scores = []

    for rule_name in meta.get("rule_set", []):
        keywords = get_rule_keywords(meta, rule_name, config)
        score = keyword_score(text, keywords)

        if score > 0:
            scores.append((rule_name, score))

    if not scores:
        return {"root": root_name, "type": None, "dest": base_path}

    scores.sort(key=lambda x: x[1], reverse=True)

    best_rule, best_score = scores[0]

    if len(scores) > 1 and scores[1][1] == best_score:
        return {
            "root": root_name,
            "type": "AMBIGUOUS",
            "dest": config["unsorted"],
            "candidates": scores,
        }

    return {"root": root_name, "type": best_rule, "dest": f"{base_path}/{best_rule}"}


def classify(text: str, config: dict):
    text = normalize(text)

    current = config["parent_root"]

    while True:
        meta = config["roots"][current]

        if "children" in meta:
            children = meta["children"]

            best_child = pick_best(text, children, config)

            if best_child is None:
                return {"root": None, "type": None, "dest": config["unsorted"]}

            current = best_child
            continue

        result = apply_rules(current, meta, text, config)
        return result
