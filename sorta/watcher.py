import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from sorta.pdf_extract import extract_pdf_text
from sorta.classifier import classify
from sorta.move import move


class SortaHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if file_path.suffix.lower() != ".pdf":
            return

        if file_path.name.startswith(".") or ".part" in file_path.name:
            return

        print(f"\nNew file detected: {file_path.name}")

        if not wait_until_stable(file_path):  # to handle browser writing
            print(f"File never stabilized: {file_path.name}")
            return

        try:
            text = extract_pdf_text(str(file_path))

            if len(text.strip()) < 50:
                dest = self.config["unsorted"]
                status = "NO_TEXT"
            else:
                result = classify(text, self.config)
                dest = result["dest"]
                status = result.get("type", "OK")

            new_path = move(str(file_path), dest)

            print(f"Moved → {new_path}")

        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")


def watch_folder(folder: str, config: dict):
    folder_path = Path(folder).expanduser()

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder_path}")

    event_handler = SortaHandler(config)
    observer = Observer()

    observer.schedule(event_handler, str(folder_path), recursive=False)

    print(f"\nWatching folder: {folder_path}")
    print("Drop PDFs here. Press Ctrl+C to stop.\n")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        observer.stop()

    observer.join()


def wait_until_stable(path: Path, timeout=10):
    """
    Wait until file size stops changing (download finished).
    """
    start = time.time()
    last_size = -1

    while time.time() - start < timeout:
        if not path.exists():
            return False

        size = path.stat().st_size

        if size == last_size:
            return True

        last_size = size
        time.sleep(0.5)

    return False
