from pathlib import Path
import typer
from rich import print

from sorta.main import app


CONFIG_PATH = Path.home() / ".config" / "sorta" / "config.toml"


@app.command("add-rule")
def add_rule(
    name: str,
    keywords: str = typer.Option(
        ...,
        "--keywords",
        "-k",
        help="Comma separated keywords (e.g. notes,lecture,unit)",
    ),
):
    """
    Add a new global rule template.
    """

    rule_name = name.strip().upper()
    keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]

    if not keyword_list:
        print("[bold red]Error:[/bold red] No keywords provided.")
        raise typer.Exit(code=1)

    config_text = CONFIG_PATH.read_text(encoding="utf-8")

    if f"[rules.{rule_name}]" in config_text:
        print(f"[bold yellow]Rule already exists:[/bold yellow] {rule_name}")
        raise typer.Exit(code=1)

    block = "\n\n" + f"[rules.{rule_name}]\n"
    block += f"keywords = {keyword_list}\n"

    with open(CONFIG_PATH, "a", encoding="utf-8") as f:
        f.write(block)

    print(f"[bold green]Added rule:[/bold green] {rule_name}")
