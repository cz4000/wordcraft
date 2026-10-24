import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evals"))

import check_quotes  # noqa: E402

BOOK = "The quick brown fox jumps over the lazy dog near the quiet river bank today."


def test_overlaps_finds_8_word_run():
    text = "As he said, the QUICK brown fox, jumps over the lazy dog! Then left."
    assert check_quotes.overlaps(text, BOOK) == ["the quick brown fox jumps over the lazy dog"]


def test_overlaps_ignores_7_word_run():
    text = "Notice how the quick brown fox jumps over the fence."
    assert check_quotes.overlaps(text, BOOK) == []


def test_quote_lines_are_limited():
    ok = "> Short credited quote. (Zinsser)\nbody\n"
    assert check_quotes.quote_problems(ok) == []
    too_many = "> a\n> b\n> c\n> d\n"
    assert check_quotes.quote_problems(too_many)
    too_long = "> " + " ".join(["word"] * 25) + "\n"
    assert check_quotes.quote_problems(too_long)
