import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_IDS = [
    "quick-question", "session-summary", "mid-session-answer", "pr-description",
    "email-reply", "email-decline", "explain-concept", "status-update",
    "announce-change", "article-from-source",
]


def load():
    return json.loads((ROOT / "evals" / "tasks.json").read_text())


def test_ten_tasks_with_fixed_ids():
    tasks = load()
    assert [t["id"] for t in tasks] == EXPECTED_IDS
    for t in tasks:
        assert set(t) == {"id", "form", "prompt", "fixtures", "expects_trigger"}
    # chat answers are the always-on lines' job; the skill loads for drafting (docs/design.md)
    assert [t["id"] for t in tasks if not t["expects_trigger"]] == ["quick-question", "mid-session-answer"]


def test_every_fixture_exists():
    for t in load():
        for name in t["fixtures"]:
            assert (ROOT / "evals" / "fixtures" / name).is_file(), name


import pytest


@pytest.mark.parametrize("task_set", ["heldout", "heldout2", "heldout3", "heldout4"])
def test_heldout_set_is_complete(task_set):
    heldout = ROOT / "evals" / task_set
    tasks = json.loads((heldout / "tasks.json").read_text())
    assert len(tasks) == 15 and len({t["id"] for t in tasks}) == 15
    for t in tasks:
        assert set(t) == {"id", "form", "prompt", "fixtures", "expects_trigger"}
        for name in t["fixtures"]:
            assert (heldout / "fixtures" / name).is_file(), name
