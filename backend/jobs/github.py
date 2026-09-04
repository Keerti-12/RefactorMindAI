import tempfile
from git import Repo

def clone_repo(url: str) -> str:
    """
    Given a GitHub URL, clone it, and store it temporarily.
    Returns the path to the cloned repository.
    """
    temp_dir = tempfile.mkdtemp(prefix='refactormind_')
    Repo.clone_from(url, temp_dir)
    return temp_dir
