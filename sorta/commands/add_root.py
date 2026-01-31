from pathlib import Path
import typer
from rich import print

from sorta.main import app

CONFIG_PATH = Path.home() / ".config" / "sorta" / "config.toml"


def parse_csv(value: str):
    return [x.strip() for x in value.split(",") if x.strip()]


def attach_child(config_text: str, parent: str, child: str) -> str:
    lines = config_text.splitlines()
    marker = f"[roots.{parent}]"

    for i, line in enumerate(lines):
        if line.strip() == marker:

            for j in range(i + 1, i + 20):
                if j >= len(lines):
                    break

                if lines[j].strip().startswith("children"):
                    existing = lines[j]

                    if f'"{child}"' in existing:
                        return "\n".join(lines)

                    updated = existing.rstrip("]")
                    updated += f', "{child}"]'
                    lines[j] = updated
                    return "\n".join(lines)

                if lines[j].strip().startswith("[roots."):
                    break

            lines.insert(i + 1, f'children = ["{child}"]')
            return "\n".join(lines)

    print(f"[bold red]Error:[/bold red] Parent root '{parent}' not found.")
    raise typer.Exit(code=1)


@app.command()
def add_root(
    name: str,
    parent: str = typer.Option(..., "--parent", help="Parent root name"),
    path: str = typer.Option(..., "--path", help="Destination folder path"),
    keywords: str = typer.Option(..., "-k", "--keywords"),
    rules: str = typer.Option(..., "-r", "--rules"),
    override: list[str] = typer.Option(
        None,
        "--override",
        help="Add rule override: RULE=kw1,kw2,... (can repeat)",
    ),
):
    """
    Add a new leaf root, attach under parent, optionally add rule overrides.
    """

    root_name = name.strip().lower()
    parent_name = parent.strip()

    keyword_list = parse_csv(keywords)
    rule_list = [r.upper() for r in parse_csv(rules)]

    if not keyword_list:
        print("[bold red]Error:[/bold red] No keywords provided.")
        raise typer.Exit(code=1)

    if not rule_list:
        print("[bold red]Error:[/bold red] No rules provided.")
        raise typer.Exit(code=1)

    config_text = CONFIG_PATH.read_text(encoding="utf-8")

    if f"[roots.{root_name}]" in config_text:
        print(f"[bold yellow]Root already exists:[/bold yellow] {root_name}")
        raise typer.Exit(code=1)

    updated_config = attach_child(config_text, parent_name, root_name)

    block = "\n\n" + f"[roots.{root_name}]\n"
    block += f'path = "{path}"\n'
    block += f"keywords = {keyword_list}\n"
    block += f"rule_set = {rule_list}\n"

    if override:
        for item in override:
            if "=" not in item:
                print("[bold red]Invalid override format.[/bold red]")
                print("Use: --override RULE=kw1,kw2,...")
                raise typer.Exit(code=1)

            rule_name, kw_string = item.split("=", 1)
            rule_name = rule_name.strip().upper()
            kw_list = parse_csv(kw_string)

            if not kw_list:
                continue

            block += "\n"
            block += f"[roots.{root_name}.rule_overrides.{rule_name}]\n"
            block += f"keywords = {kw_list}\n"

    updated_config += block
    CONFIG_PATH.write_text(updated_config, encoding="utf-8")

    print(f"[bold green]Added root:[/bold green] {root_name}")
    print(f"[bold cyan]Attached under parent:[/bold cyan] {parent_name}")

    if override:
        print("[green]Overrides added.[/green]")
