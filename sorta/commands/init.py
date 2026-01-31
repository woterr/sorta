import typer
from rich import print
from pathlib import Path
import importlib.resources as resources

from sorta.main import app


@app.command()
def init(force: bool = typer.Option(False, "--force")):
    """
    Create default config file at ~/.config/sorta/config.toml
    """

    config_dir = Path.home() / ".config" / "sorta"
    config_file = config_dir / "config.toml"

    config_dir.mkdir(parents=True, exist_ok=True)

    if config_file.exists() and not force:
        print(f"[bold yellow]Config already exists:[/bold yellow] {config_file}")
        print("Use --force to overwrite it.")
        raise typer.Exit(code=1)

    template_text = (
        resources.files("sorta.templates")
        .joinpath("config.example.toml")
        .read_text(encoding="utf-8")
    )

    config_file.write_text(template_text, encoding="utf-8")

    print("[bold green]Initialized sorta config successfully.[/bold green]")
    print(f"Config written to: [cyan]{config_file}[/cyan]")
