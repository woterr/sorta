from pathlib import Path
from typing import Optional

import typer
from rich import print

from sorta.main import app
from sorta.config_loader import load_config
from sorta.pipeline import process_pdf


@app.command()
def run(
    folder: Optional[str] = typer.Option(
        None,
        "--folder",
        "-f",
        help="Folder to scan (defaults to dropbox)",
    ),
    here: bool = typer.Option(
        False,
        "--here",
        help="Scan the current working directory",
    ),
):
    """
    Process all PDF files inside a folder once.
    """

    config = load_config()

    if here:
        scan_dir = Path.cwd()
    elif folder is None:
        scan_dir = Path(config["dropbox"]).expanduser()
    else:
        scan_dir = Path(folder).expanduser().resolve()

    if not scan_dir.exists():
        print(f"[bold red]Error:[/bold red] Folder not found → {scan_dir}")
        raise typer.Exit(code=1)

    print(f"\n[bold cyan]Sorting PDFs in:[/bold cyan] {scan_dir}")

    pdfs = list(scan_dir.glob("*.pdf"))

    if not pdfs:
        print("[yellow]No PDF files found.[/yellow]")
        return

    for pdf in pdfs:
        print(f"\n[bold]Processing:[/bold] {pdf.name}")

        try:
            new_path = process_pdf(str(pdf), config, mode="run")
            print(f"[green]Moved →[/green] {new_path}")

        except Exception as e:
            print(f"[red]Failed:[/red] {pdf.name} ({e})")

    print("\n[bold green]Done.[/bold green]")
