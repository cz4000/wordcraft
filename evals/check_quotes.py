"""Check that the skill restates the book instead of copying it.

Usage: python evals/check_quotes.py <path to your copy of the book>.pdf
The book never enters the repo: its text goes to a temp file and is deleted.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "wordcraft"
RUN_LENGTH = 8  # a shared run of this many words counts as copying
MAX_QUOTES = 3
MAX_QUOTE_WORDS = 25


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.lower().replace("’", "'"))


def overlaps(text: str, book: str, n: int = RUN_LENGTH) -> list[str]:
    """Every maximal run of n or more words that appears in both texts."""
    words = _words(text)
    book_words = _words(book)
    book_grams = {tuple(book_words[i:i + n]) for i in range(len(book_words) - n + 1)}
    runs, i = [], 0
    while i <= len(words) - n:
        if tuple(words[i:i + n]) in book_grams:
            end = i + n
            while end < len(words) and tuple(words[end - n + 1:end + 1]) in book_grams:
                end += 1
            runs.append(" ".join(words[i:end]))
            i = end
        else:
            i += 1
    return runs


def quote_problems(text: str) -> list[str]:
    quotes = [line[2:] for line in text.splitlines() if line.startswith("> ")]
    problems = [f"quote of {len(q.split())} words: {q[:60]}" for q in quotes if len(q.split()) >= MAX_QUOTE_WORDS]
    if len(quotes) > MAX_QUOTES:
        problems.append(f"{len(quotes)} quote lines; at most {MAX_QUOTES} allowed")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 2
    with tempfile.TemporaryDirectory() as tmp:
        book_txt = Path(tmp) / "book.txt"
        subprocess.run(["pdftotext", argv[0], str(book_txt)], check=True)
        book = book_txt.read_text(errors="ignore")
    all_text, problems = "", []
    for path in sorted(SKILL_DIR.glob("*.md")):
        text = path.read_text()
        all_text += text
        unquoted = "\n".join(line for line in text.splitlines() if not line.startswith("> "))
        problems += [f"{path.name}: copied run: {run}" for run in overlaps(unquoted, book)]
    problems += quote_problems(all_text)
    for problem in problems:
        print(problem)
    print("ok" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
