from rich import print

from sorta.main import app
from sorta.config_loader import load_config


@app.command("list")
def list_config():
    """
    Show configured roots and rules.
    """

    config = load_config()

    print("\n[bold cyan]Roots:[/bold cyan]")

    for root_name, meta in config["roots"].items():
        print(f"  • {root_name}")

        if "children" in meta:
            for child in meta["children"]:
                print(f"     └─ {child}")

        if "rule_set" in meta:
            print(f"     Rules: {', '.join(meta['rule_set'])}")

        overrides = meta.get("rule_overrides", {})
        if overrides:
            print("     Overrides:")
            for rule_name, override_meta in overrides.items():
                kws = ", ".join(override_meta.get("keywords", []))
                print(f"        • {rule_name}: {kws}")

    print("\n[bold magenta]Rules:[/bold magenta]")

    for rule_name, rule_meta in config["rules"].items():
        kws = rule_meta.get("keywords", [])
        print(f"  • {rule_name}: {', '.join(kws)}")
