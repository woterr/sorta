from rich import print
from sorta.main import app
from pathlib import Path


@app.command()
def config():
    """
    Show the config file location.
    """
    path = Path.home() / ".config" / "sorta" / "config.toml"
    print(path)
