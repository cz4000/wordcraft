import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "wordcraft"
SKILL_MD = SKILL_DIR / "SKILL.md"
LINK = re.compile(r"\]\(([^)#]+\.md)\)")


def split_frontmatter(text: str) -> tuple[dict, str]:
    _, front, body = text.split("---\n", 2)
    fields = {}
    for line in front.splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, body


def test_skill_md_under_500_words():
    _, body = split_frontmatter(SKILL_MD.read_text())
    assert len(body.split()) < 500


def test_frontmatter_name_and_description():
    fields, _ = split_frontmatter(SKILL_MD.read_text())
    assert fields["name"] == "wordcraft"
    description = fields["description"]
    assert 0 < len(description) <= 1024
    assert "claude" not in description.lower() and "anthropic" not in description.lower()


def test_references_one_level_deep():
    links = LINK.findall(SKILL_MD.read_text())
    assert links, "SKILL.md links no reference files"
    for link in links:
        target = SKILL_DIR / link
        assert target.is_file(), link
        assert not LINK.findall(target.read_text()), f"{link} links further"


def test_always_on_at_most_10_lines():
    lines = [l for l in (ROOT / "always-on.md").read_text().splitlines() if l.strip()]
    assert 0 < len(lines) <= 10


def test_always_on_copies_match():
    assert (ROOT / "always-on.md").read_text() == (ROOT / "evals" / "always-on" / "CLAUDE.md").read_text()
