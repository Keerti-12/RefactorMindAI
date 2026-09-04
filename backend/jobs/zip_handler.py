import tempfile
import zipfile
import os

def extract_zip(file: str) -> str:
    """
    Given a zip file, extract it and store it temporarily.
    Return the path to the extracted zip.
    """
    temp_dir = tempfile.mkdtemp(prefix="refactormind_")
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    return temp_dir