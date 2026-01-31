from pathlib import Path

import typer
from rich import print

from sorta.main import app
from sorta.config_loader import load_config
from sorta.pdf_extract import extract_pdf_text
from sorta.classifier import classify


@app.command("classify")
def classify_file(path: str):
    """
    Debug classification for one file.
    """
    config = load_config()

    file_path = Path(path).expanduser().resolve()

    if not file_path.exists():
        print(f"[bold red]Error:[/bold red] File not found → {file_path}")
        raise typer.Exit(code=1)

    print(f"\n[bold yellow]Reading:[/bold yellow] {file_path}")

    text = extract_pdf_text(str(file_path))

    if len(text.strip()) < 50:
        print("[red]No extractable text found (maybe scanned PDF).[/red]")
        return

    result = classify(text, config)

    print("\n[bold green]Classification Result:[/bold green]")
    print(result)

    print("\n[cyan]Destination would be:[/cyan]")
    print(result["dest"])
