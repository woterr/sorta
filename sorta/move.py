import shutil
from pathlib import Path


def move(src: str, dest_folder: str):
    src_path = Path(src)
    dest_dir = Path(dest_folder)

    dest_dir.mkdir(parents=True, exist_ok=True)

    target = dest_dir / src_path.name

    if not target.exists():
        shutil.move(str(src_path), str(target))
        return target

    stem = src_path.stem
    suffix = src_path.suffix

    i = 1
    while True:
        new_target = dest_dir / f"{stem}_{i}{suffix}"
        if not new_target.exists():
            shutil.move(str(src_path), str(new_target))
            return new_target
        i += 1
