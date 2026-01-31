from pathlib import Path
from sorta.pdf_extract import extract_pdf_text
from sorta.logger import logger
from sorta.classifier import classify
from sorta.move import move


def process_pdf(path, config, mode="run"):
    file_path = Path(path)

    try:
        text = extract_pdf_text(str(file_path))

        if len(text.strip()) < 50:
            result = {
                "root": None,
                "type": None,
                "dest": config["unsorted"],
            }
            status = "NO_TEXT"

        else:
            result = classify(text, config)
            status = result["type"]

            if status == "AMBIGUOUS":
                status = "AMBIGUOUS"

        new_path = move(str(file_path), result["dest"])

        logger(
            {
                "event": "process",
                "mode": mode,
                "status": "MOVED",
                "file": {
                    "name": file_path.name,
                    "src": str(file_path),
                    "dest": str(new_path),
                },
                "decision": {
                    "root": result.get("root"),
                    "type": result.get("type"),
                    "candidates": result.get("candidates"),
                },
                "error": None,
            },
            config,
        )

        return new_path

    except FileNotFoundError as e:
        logger(
            {
                "event": "process",
                "mode": mode,
                "status": "MISSING_SOURCE",
                "file": {
                    "name": file_path.name,
                    "src": str(file_path),
                    "dest": None,
                },
                "decision": None,
                "error": {
                    "kind": "FileNotFoundError",
                    "message": str(e),
                },
            },
            config,
        )

    except PermissionError as e:
        logger(
            {
                "event": "process",
                "mode": mode,
                "status": "PERMISSION_DENIED",
                "file": {
                    "name": file_path.name,
                    "src": str(file_path),
                    "dest": None,
                },
                "decision": None,
                "error": {
                    "kind": "PermissionError",
                    "message": str(e),
                },
            },
            config,
        )

    except OSError as e:
        logger(
            {
                "event": "process",
                "mode": mode,
                "status": "OS_ERROR",
                "file": {
                    "name": file_path.name,
                    "src": str(file_path),
                    "dest": None,
                },
                "decision": None,
                "error": {
                    "kind": "OSError",
                    "message": str(e),
                },
            },
            config,
        )

    except Exception as e:
        logger(
            {
                "event": "process",
                "mode": mode,
                "status": "UNKNOWN_ERROR",
                "file": {
                    "name": file_path.name,
                    "src": str(file_path),
                    "dest": None,
                },
                "decision": None,
                "error": {
                    "kind": type(e).__name__,
                    "message": str(e),
                },
            },
            config,
        )
