import shutil
import os

def cleanup_directory(path: str) -> None:
    """
    Delete a temporary directory and all its contents.
    Safe to call even if the path doesn't exist.
    Always called in a finally block — runs on success and failure.
    """
    if path and os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)