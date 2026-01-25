import re


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text


def keyword_score(text: str, keywords: list[str]) -> int:
    score = 0
    for kw in keywords:
        if kw.lower() in text:
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
    base_path = meta["path"]

    best_rule = None
    best_score = 0

    for rule_name in meta.get("rule_set", []):
        rule_keywords = config["rules"][rule_name]["keywords"]

        score = keyword_score(text, rule_keywords)

        if score > best_score:
            best_score = score
            best_rule = rule_name

    if best_rule:
        return {
            "root": root_name,
            "type": best_rule,
            "dest": f"{base_path}/{best_rule}",
        }

    return {"root": root_name, "type": None, "dest": base_path}


def classify(text: str, config: dict):
    text = normalize(text)

    current = config["parent_root"]

    while True:
        meta = config["roots"][current]

        if "children" in meta:
            children = meta["children"]

            best_child = pick_best(text, children, config)

            if best_child is None:
                return apply_rules(current, meta, text, config)

            current = best_child
            continue

        return apply_rules(current, meta, text, config)
