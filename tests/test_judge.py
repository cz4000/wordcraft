import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evals"))

import judge  # noqa: E402


def write_run(runs: Path, arm: str, task: str, rep: int, text: str, prompt: str = "Do the task") -> Path:
    path = runs / "opus" / arm / task / f"rep{rep}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"text": text, "prompt": prompt, "error": ""}))
    return path


def make_pair(tmp_path: Path, a_text: str, b_text: str, task: str = "t1", rep: int = 1) -> judge.Pair:
    return judge.Pair(task, rep, write_run(tmp_path, "real", task, rep, a_text), write_run(tmp_path, "baseline", task, rep, b_text))


def test_make_pairs_matches_task_and_rep(tmp_path):
    for rep in (1, 2):
        write_run(tmp_path, "real", "t1", rep, "a")
        write_run(tmp_path, "baseline", "t1", rep, "b")
    write_run(tmp_path, "real", "t2", 1, "a only")
    pairs = judge.make_pairs(tmp_path, "opus", "real", "baseline")
    assert [(p.task_id, p.rep) for p in pairs] == [("t1", 1), ("t1", 2)]


def test_swapped_order_split_is_tie(tmp_path):
    always_first = lambda prompt, first, second: ("1", "first looks better")
    assert judge.judge_pair(make_pair(tmp_path, "x", "y"), always_first) == "tie"


def test_consistent_preference_wins(tmp_path):
    prefers_good = lambda prompt, first, second: ("1" if "GOOD" in first else "2", "")
    assert judge.judge_pair(make_pair(tmp_path, "GOOD reply", "meh reply"), prefers_good) == "a"
    assert judge.judge_pair(make_pair(tmp_path, "meh reply", "GOOD reply", task="t2"), prefers_good) == "b"


def test_judge_pair_logs_reasons(tmp_path):
    log = []
    prefers_good = lambda prompt, first, second: ("1" if "GOOD" in first else "2", "clearer")
    judge.judge_pair(make_pair(tmp_path, "GOOD", "meh"), prefers_good, log=log)
    assert [entry["reason"] for entry in log] == ["clearer", "clearer"]


def test_failed_run_loses_without_a_judge_call(tmp_path):
    calls = []
    judge_fn = lambda *args: calls.append(args) or ("1", "")
    assert judge.judge_pair(make_pair(tmp_path, "", "a reply"), judge_fn) == "b"
    assert calls == []


def test_score_majority_ignores_ties():
    verdicts = {
        ("t1", 1): "a", ("t1", 2): "tie", ("t1", 3): "tie",
        ("t2", 1): "a", ("t2", 2): "b", ("t2", 3): "tie",
        ("t3", 1): "b", ("t3", 2): "b", ("t3", 3): "a",
    }
    assert judge.score(verdicts) == {"t1": "win", "t2": "tie", "t3": "loss"}


def test_quick_question_length_flag():
    assert judge.length_flag([160, 170, 400], [100, 100, 100]) is True
    assert judge.length_flag([140, 150, 400], [100, 100, 100]) is False


def test_owner_sample_key_matches_page(tmp_path):
    pairs = [make_pair(tmp_path, f"ALPHA-{i}", f"BETA-{i}", task=f"t{i}") for i in range(12)]
    page, key = judge.owner_sample(pairs, n=10, seed=3)
    assert len(key) == 10
    for number, entry in key.items():
        section = page.split(f"## Pair {number}\n", 1)[1].split("\n## Pair ", 1)[0]
        reply_1 = section.split("### Reply 1\n", 1)[1].split("### Reply 2\n", 1)[0]
        expected = "ALPHA" if entry["reply_1"] == "a" else "BETA"
        assert expected in reply_1
    assert "real" not in page and "baseline" not in page
