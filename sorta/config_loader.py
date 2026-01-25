import tomllib
from pathlib import Path


CONFIG_PATH = Path.home() / ".config" / "sorta" / "config.toml"


def expand_path(path): # remove `~`
    return str(Path(path).expanduser())


def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Config not found: {CONFIG_PATH}\n" "Run `sorta init` to generate one."
        )

    with open(CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)

    if "parent_root" not in config:
        raise ValueError("Config must define `parent_root`.")

    if "roots" not in config:
        raise ValueError("Config must define `[roots.*]` blocks.")

    if "rules" not in config:
        raise ValueError("Config must define `[rules.*]` templates.")

    parent = config["parent_root"]

    if parent not in config["roots"]:
        raise ValueError(f"Parent root '{parent}' not defined inside [roots].")

    config["dropbox"] = expand_path(config["dropbox"])
    config["unsorted"] = expand_path(config["unsorted"])

    for root_name, meta in config["roots"].items():
        if "path" in meta:
            meta["path"] = expand_path(meta["path"])

    return config
