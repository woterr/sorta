from pathlib import Path

import typer
from rich import print

from sorta.main import app
from sorta.config_loader import load_config
from sorta.pipeline import process_pdf


@app.command("sort")
def sort_file(path: str):
    """
    Classify and move a file safely.
    """
    config = load_config()

    file_path = Path(path).expanduser().resolve()

    if not file_path.exists():
        print(f"[bold red]Error:[/bold red] File not found → {file_path}")
        raise typer.Exit(code=1)

    try:
        new_path = process_pdf(str(file_path), config, mode="single")
        print(f"[green]Moved →[/green] {new_path}")

    except Exception as e:
        print(f"[bold red]Failed:[/bold red] {e}")
        raise typer.Exit(code=1)
