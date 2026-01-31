import tomllib
from pathlib import Path

import typer
from rich import print


CONFIG_PATH = Path.home() / ".config" / "sorta" / "config.toml"


def expand_path(path: str) -> str:
    """Expand ~ into full home directory path."""
    return str(Path(path).expanduser())


def config_error(msg: str):
    """
    Print a clean config error and exit without traceback.
    """
    print("\n[bold red]Configuration Error[/bold red]")
    print(f"[yellow]{msg}[/yellow]\n")
    print("Config file location:")
    print(f"  [cyan]{CONFIG_PATH}[/cyan]\n")
    print("Fix the file and try again.\n")
    raise typer.Exit(code=1)


def validate_config(config: dict):
    roots = config["roots"]

    for root_name, meta in roots.items():

        for child in meta.get("children", []):
            if child not in roots:
                config_error(
                    f"Root '{root_name}' references missing child '{child}'.\n"
                    f"Define it with:\n"
                    f"  [roots.{child}]"
                )

        if "children" not in meta and "rule_set" not in meta:
            config_error(
                f"Leaf root '{root_name}' must define a rule_set.\n"
                f"Example:\n"
                f'  rule_set = ["NOTES"]'
            )

        if "children" in meta and "rule_set" in meta:
            config_error(
                f"Root '{root_name}' cannot have BOTH children and rule_set.\n"
                f"Choose one:\n"
                f"  children = [...]   OR   rule_set = [...]"
            )


def load_config() -> dict:
    """
    Load config.toml.
    """

    if not CONFIG_PATH.exists():
        print("\n[bold red]No configuration found.[/bold red]\n")
        print("Run this first:")
        print("  [cyan]sorta init[/cyan]\n")
        raise typer.Exit(code=1)

    try:
        with open(CONFIG_PATH, "rb") as f:
            config = tomllib.load(f)

    except tomllib.TOMLDecodeError as e:
        config_error(f"Invalid TOML syntax:\n{e}")

    if "parent_root" not in config:
        config_error("Missing required key: parent_root")

    if "roots" not in config:
        config_error("Missing required section: [roots.*]")

    if "rules" not in config:
        config_error("Missing required section: [rules.*]")

    parent = config["parent_root"]
    if parent not in config["roots"]:
        config_error(
            f"Parent root '{parent}' is not defined.\n" f"Add:\n  [roots.{parent}]"
        )
    validate_config(config)

    config["dropbox"] = expand_path(config["dropbox"])
    config["unsorted"] = expand_path(config["unsorted"])

    for _, meta in config["roots"].items():
        if "path" in meta:
            meta["path"] = expand_path(meta["path"])

    return config
