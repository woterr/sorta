from pathlib import Path
import json
from datetime import datetime
from pathlib import Path


def logger(log: dict, config: dict):
    log_dir = Path(config.get("log_dir", "~/.cache/sorta")).expanduser()
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "sorta.log"

    log["timestamp"] = datetime.now().isoformat()

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")
