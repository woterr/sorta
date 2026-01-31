import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from sorta.pipeline import process_pdf


class SortaHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config

    def handle_file(self, file_path: Path):
        if file_path.suffix.lower() != ".pdf":
            return

        if file_path.name.startswith(".") or ".part" in file_path.name:
            return

        if not wait_until_stable(file_path):  # to handle writing from browser
            return

        if not file_path.exists():
            return

        print(f"\nNew file: {file_path.name}")

        try:
            new_path = process_pdf(str(file_path), self.config, mode="watch")
            print(f"Moved → {new_path}")

        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

    def on_created(self, event):
        if event.is_directory:
            return
        self.handle_file(Path(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            return
        self.handle_file(Path(event.src_path))


def watch_folder(folder: str, config: dict):
    folder_path = Path(folder).expanduser()

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder_path}")

    event_handler = SortaHandler(config)
    observer = Observer()

    observer.schedule(event_handler, str(folder_path), recursive=False)

    print(f"\nWatching: {folder_path}")
    print("Drop PDFs here. Ctrl+C to stop.\n")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def wait_until_stable(path: Path, timeout=10):
    start = time.time()
    last_size = -1
    stable_count = 0

    while time.time() - start < timeout:
        if not path.exists():
            return False

        size = path.stat().st_size

        if size == last_size:
            stable_count += 1
            if stable_count >= 2:
                return True
        else:
            stable_count = 0

        last_size = size
        time.sleep(0.5)

    return False
