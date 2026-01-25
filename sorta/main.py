import typer
from typing import Optional
from rich import print
from pathlib import Path
from sorta.pdf_extract import extract_pdf_text
from sorta.classifier import classify
from sorta.config_loader import load_config
from sorta.move import move


app = typer.Typer(help="sorta: Document sorter using keyword-based routing")


# config = load_config()
# text = extract_pdf_text("/mnt/shared/Projects/sorta/test.pdf")

# print(classify(text, config))


@app.command()
def init():
    """
    Create default config file in ~/.config/sorta/
    """
    print("[bold green]Initializing sorta...[/bold green]")
    print("Not implemented yet (you will generate config template here).")


@app.command()
def list_pdfs():
    """
    Show available roots and rules.
    """
    config = load_config()

    print("\n[bold cyan]Roots:[/bold cyan]")
    for root in config["roots"]:
        print(" -", root)

    print("\n[bold magenta]Rules:[/bold magenta]")
    for rule in config["rules"]:
        print(" -", rule)


@app.command()
def classify_file(path: str):
    """
    Debug classification for one file.
    """
    config = load_config()

    cwd = Path.cwd()
    file_path = (cwd / path).resolve()

    if not file_path.exists():
        print(f"[bold red]Error:[/bold red] File not found → {file_path}")
        print("Tip: Run the command with the correct path:")
        print("   sorta classify-file ~/Downloads/file.pdf")
        raise typer.Exit(code=1)

    print(f"\n[bold yellow]Reading:[/bold yellow] {file_path}")

    text = extract_pdf_text(file_path)

    if len(text.strip()) < 50:
        print("[red]No extractable text found.[/red]")
        return

    result = classify(text, config)

    print("\n[bold green]Classification Result:[/bold green]")
    print(result)
    print("\n[yellow]Moving file...[/yellow]")
    move(src=file_path, dest_folder=result["dest"])


@app.command()
def run(
    folder: Optional[str] = typer.Option(
        None,
        "--folder",
        "-f",
        help="Folder to scan. If omitted, uses dropbox. If empty, uses current directory.",
    ),
    here: bool = typer.Option(
        False, "--here", help="Scan the current working directory"
    ),
):
    """
    Process all PDF files inside the dropbox (or a given folder).
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

    print(f"\n[bold cyan]Sorting files in:[/bold cyan] {scan_dir}")

    pdfs = list(scan_dir.glob("*.pdf"))

    if not pdfs:
        print("[yellow]No PDF files found.[/yellow]")
        return

    for pdf in pdfs:
        print(f"\n[bold]Processing:[/bold] {pdf.name}")

        text = extract_pdf_text(str(pdf))

        if len(text.strip()) < 50:
            dest = config["unsorted"]
            status = "NO_TEXT"

        else:
            result = classify(text, config)
            dest = result["dest"]
            status = result.get("type", "OK")

        new_path = move(str(pdf), dest)

        print(f"[green]Moved →[/green] {new_path}")

    print("\n[bold green]Done.[/bold green]")


@app.command()
def watch(folder: str):
    """
    Watch a folder continuously (not implemented yet).
    """
    print("[red]Watch mode not implemented yet.[/red]")


def main():
    app()


if __name__ == "__main__":
    main()
