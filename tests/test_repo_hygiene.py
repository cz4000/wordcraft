import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PRIVATE_WORDS = ROOT / ".private-words"


def git_ls_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return out.stdout.splitlines()


def test_no_private_words_in_tracked_files():
    # .private-words is local-only, so this skips in anyone else's clone
    if not PRIVATE_WORDS.exists():
        pytest.skip(".private-words is local-only")
    words = [
        w.strip().lower()
        for w in PRIVATE_WORDS.read_text().splitlines()
        if w.strip() and not w.startswith("#")
    ]
    hits = []
    for name in git_ls_files():
        path = ROOT / name
        if path.is_file():
            text = path.read_text(errors="ignore").lower()
            hits += [f"{name}: {w}" for w in words if w in text]
    assert not hits, hits


def test_book_never_tracked():
    assert not [f for f in git_ls_files() if f.endswith((".pdf", "book.txt"))]


def test_private_words_file_never_tracked():
    assert ".private-words" not in git_ls_files()
