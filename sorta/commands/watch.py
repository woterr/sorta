from pathlib import Path
from typing import Optional

import typer
from rich import print

from sorta.main import app
from sorta.config_loader import load_config
from sorta.watcher import watch_folder


@app.command()
def watch(
    folder: Optional[str] = typer.Option(
        None,
        "--folder",
        "-f",
        help="Folder to watch (defaults to dropbox)",
    ),
    here: bool = typer.Option(
        False,
        "--here",
        help="Watch the current working directory",
    ),
):
    """
    Watch a folder continuously.
    """
    config = load_config()

    if here:
        watch_dir = Path.cwd()
    elif folder is None:
        watch_dir = config["dropbox"]
    else:
        watch_dir = folder

    print(f"Watching folder: {watch_dir}")
    watch_folder(watch_dir, config=config)
