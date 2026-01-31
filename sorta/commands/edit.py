import os
import typer
from rich import print
from pathlib import Path

from sorta.main import app

CONFIG_PATH = Path.home() / ".config" / "sorta" / "config.toml"


@app.command()
def edit():
    """
    Open the config file in your editor.
    """
    editor = os.environ.get("EDITOR", "nano")

    print(f"Opening config: {CONFIG_PATH}")
    os.system(f"{editor} {CONFIG_PATH}")
