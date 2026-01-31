from pathlib import Path
from rich import print
import re

from sorta.main import app
from sorta.config_loader import load_config, CONFIG_PATH


def find_reachable_roots(config):
    roots = config["roots"]
    parent = config["parent_root"]

    reachable = set()

    def dfs(node):
        if node in reachable:
            return
        reachable.add(node)

        meta = roots[node]
        for child in meta.get("children", []):
            dfs(child)

    dfs(parent)
    return reachable


@app.command()
def doctor():
    """
    Check config health and common mistakes.
    """

    print("\n[bold cyan]sorta doctor[/bold cyan]")
    print("Running diagnostics...\n")

    # CONFIG
    try:
        config = load_config()
        print("[green]OK[/green] Config loads successfully")
    except Exception as e:
        print("[bold red]FAIL[/bold red] Config could not load")
        print(e)
        return

    roots = config["roots"]
    rules = config["rules"]

    print(f"[green]OK[/green] Roots loaded: {len(roots)}")
    print(f"[green]OK[/green] Rules loaded: {len(rules)}")

    # RULES
    missing_rules = []

    for root_name, meta in roots.items():
        for r in meta.get("rule_set", []):
            if r not in rules:
                missing_rules.append((root_name, r))

    if missing_rules:
        print("\n[bold red]FAIL[/bold red] Missing rule templates:")
        for root, rule in missing_rules:
            print(f"  Root '{root}' references undefined rule '{rule}'")
    else:
        print("[green]OK[/green] All rule_set references are valid")

    # MULTILINE
    raw_text = Path(CONFIG_PATH).read_text(encoding="utf-8")

    multiline_children = re.findall(r"children\s*=\s*\[\s*\n", raw_text)

    if multiline_children:
        print("\n[bold yellow]WARNING[/bold yellow] Multi-line children list detected!")
        print("Your helpers (add-root) only support single-line children arrays.")
        print("Fix by formatting like:")
        print('  children = ["study", "work", "finance"]\n')
    else:
        print("[green]OK[/green] Children arrays are single-line (helpers safe)")

    # DROPBOX
    dropbox = Path(config["dropbox"]).expanduser()
    if not dropbox.exists():
        print("\n[bold yellow]WARNING[/bold yellow] Dropbox folder missing:")
        print(f"  {dropbox}")
        print("Create it with:")
        print(f"  mkdir -p {dropbox}\n")
    else:
        print("[green]OK[/green] Dropbox folder exists")

    # FALLBACK FILE UNSORTED
    unsorted = Path(config["unsorted"]).expanduser()
    if not unsorted.exists():
        print("\n[bold yellow]WARNING[/bold yellow] UNSORTED folder missing:")
        print(f"  {unsorted}")
        print("It will be created automatically on first move.\n")
    else:
        print("[green]OK[/green] UNSORTED folder exists")

    # LOGS
    log_dir = Path(config.get("log_dir", "~/.cache/sorta")).expanduser()

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        testfile = log_dir / ".write_test"
        testfile.write_text("ok")
        testfile.unlink()
        print("[green]OK[/green] Log directory writable")
    except Exception:
        print("\n[bold red]FAIL[/bold red] Log directory not writable:")
        print(f"  {log_dir}\n")

    # IF ALL CHILDREN ARE LINKED
    reachable = find_reachable_roots(config)
    all_roots = set(config["roots"].keys())

    unused = all_roots - reachable

    if unused:
        print("\n[bold yellow]WARNING[/bold yellow] Unattached roots detected:")
        for r in unused:
            print(f"  • {r} (not reachable from parent_root)")
        print("\nAttach them by adding to a parent's children list.")
    else:
        print("[green]OK[/green] All roots are attached to the tree")

    print("\n[bold green]Doctor finished.[/bold green]")
