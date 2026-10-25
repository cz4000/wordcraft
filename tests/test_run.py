import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(ROOT / "evals"))

import run  # noqa: E402


def read_lines(name: str) -> list[str]:
    return (FIXTURES / name).read_text().splitlines()


def test_baseline_has_no_plugin_dir():
    cmd = run.build_command("baseline", "haiku", "hi", ROOT)
    assert cmd[:3] == ["claude", "-p", "hi"]
    assert "--plugin-dir" not in cmd
    assert cmd[cmd.index("--setting-sources") + 1] == "project"
    assert "--strict-mcp-config" in cmd


def test_real_adds_plugin_dir():
    cmd = run.build_command("real", "haiku", "hi", ROOT)
    assert cmd[cmd.index("--plugin-dir") + 1] == str(ROOT)
    assert cmd[2] == "hi"


def test_forced_prefixes_slash_command():
    cmd = run.build_command("forced", "haiku", "hi", ROOT)
    assert cmd[2] == "/wordcraft:wordcraft hi"
    assert cmd[cmd.index("--plugin-dir") + 1] == str(ROOT)


def test_workdir_for_baseline_has_no_claude_md(tmp_path):
    always_on = tmp_path / "CLAUDE.md"
    always_on.write_text("ALWAYS")
    assert not (run.workdir_for("baseline", always_on) / "CLAUDE.md").exists()


def test_workdir_for_real_holds_always_on(tmp_path):
    always_on = tmp_path / "CLAUDE.md"
    always_on.write_text("ALWAYS")
    for arm in ("real", "forced"):
        assert (run.workdir_for(arm, always_on) / "CLAUDE.md").read_text() == "ALWAYS"


def test_load_task_prompt_appends_fixtures_in_order(tmp_path):
    fx = tmp_path / "evals" / "fixtures"
    fx.mkdir(parents=True)
    (fx / "a.md").write_text("AAA")
    (fx / "b.md").write_text("BBB")
    tasks = [
        {"id": "one", "form": "x", "prompt": "Do it", "fixtures": ["a.md", "b.md"], "expects_trigger": True},
        {"id": "two", "form": "y", "prompt": "Plain", "fixtures": [], "expects_trigger": False},
    ]
    (tmp_path / "evals" / "tasks.json").write_text(json.dumps(tasks))
    loaded = run.load_tasks(tmp_path)
    assert [t["id"] for t in loaded] == ["one", "two"]
    assert run.load_task_prompt(loaded[0], tmp_path) == "Do it\n\n--- a.md ---\nAAA\n\n--- b.md ---\nBBB"
    assert run.load_task_prompt(loaded[1], tmp_path) == "Plain"


def test_parse_stream_detects_skill_call():
    result = run.parse_stream(read_lines("stream_skill.jsonl"))
    assert result.skill_triggered is True
    assert "heating" in result.text
    assert result.input_tokens > 0 and result.output_tokens > 0


def test_parse_stream_no_skill_call():
    result = run.parse_stream(read_lines("stream_no_skill.jsonl"))
    assert result.skill_triggered is False
    assert "Available Skills" in result.text


def test_is_clean_rejects_owner_rules():
    assert run.is_clean("1. dataviz\n2. code-review\nCLAUDE.md: none")
    assert not run.is_clean("1. humanizer\n2. dataviz")
    assert not run.is_clean("Behavioral guidelines to reduce common LLM coding mistakes")


def test_failed_call_retried_once_then_recorded(tmp_path):
    calls = []

    def failing(cmd, cwd):
        calls.append(cmd)
        raise subprocess.CalledProcessError(1, cmd)

    result = run.execute(["claude", "-p", "x"], tmp_path, runner=failing)
    assert len(calls) == 2
    assert result.text == ""
    assert result.error


def test_dry_run_counts_calls(tmp_path, capsys):
    tasks = [{"id": f"t{i}", "form": "x", "prompt": "p", "fixtures": [], "expects_trigger": True} for i in range(2)]
    (tmp_path / "evals").mkdir()
    (tmp_path / "evals" / "tasks.json").write_text(json.dumps(tasks))
    run.main(
        ["run", "--arms", "baseline", "real", "--models", "opus", "--reps", "3",
         "--tasks", "all", "--out", str(tmp_path / "out"), "--dry-run"],
        root=tmp_path,
    )
    assert "12 calls" in capsys.readouterr().out
    assert not (tmp_path / "out").exists()


def test_real_can_read_the_skill_reference_files():
    # principles.md and forms.md live in the plugin folder, outside the temp workdir
    for arm in ("real", "forced"):
        cmd = run.build_command(arm, "haiku", "hi", ROOT)
        assert cmd[cmd.index("--add-dir") + 1] == str(ROOT)
    assert "--add-dir" not in run.build_command("baseline", "haiku", "hi", ROOT)


def test_parse_stream_records_reference_reads():
    lines = [
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Read", "input": {"file_path": "/x/skills/wordcraft/forms.md"}},
            {"type": "tool_use", "name": "Read", "input": {"file_path": "/x/notes.txt"}},
        ]}}),
        json.dumps({"type": "result", "result": "done", "usage": {}}),
    ]
    assert run.parse_stream(lines).reference_reads == ["forms.md"]


def test_dry_run_reads_a_named_task_set(tmp_path, capsys):
    tasks = [{"id": "t0", "form": "x", "prompt": "p", "fixtures": [], "expects_trigger": True}]
    (tmp_path / "evals" / "heldout").mkdir(parents=True)
    (tmp_path / "evals" / "heldout" / "tasks.json").write_text(json.dumps(tasks))
    run.main(["run", "--arms", "baseline", "--models", "opus", "--reps", "2", "--task-set", "heldout",
              "--out", str(tmp_path / "out"), "--dry-run"], root=tmp_path)
    assert "2 calls" in capsys.readouterr().out


def test_load_task_prompt_reads_fixtures_from_the_task_set(tmp_path):
    fx = tmp_path / "evals" / "heldout" / "fixtures"
    fx.mkdir(parents=True)
    (fx / "a.md").write_text("AAA")
    task = {"prompt": "Do it", "fixtures": ["a.md"]}
    assert run.load_task_prompt(task, tmp_path, task_set="heldout") == "Do it\n\n--- a.md ---\nAAA"


def test_run_uses_the_given_skill_dir(tmp_path, monkeypatch):
    tasks = [{"id": "t0", "form": "x", "prompt": "p", "fixtures": [], "expects_trigger": True}]
    (tmp_path / "evals").mkdir()
    (tmp_path / "evals" / "tasks.json").write_text(json.dumps(tasks))
    (tmp_path / "always-on.md").write_text("A")
    seen = []
    monkeypatch.setattr(run, "execute", lambda cmd, cwd: seen.append(cmd) or run.RunResult("ok", True, 1, 1))
    skill = tmp_path / "v05"
    run.main(["run", "--arms", "real", "--models", "opus", "--reps", "1",
              "--skill-dir", str(skill), "--out", str(tmp_path / "out")], root=tmp_path)
    assert seen[0][seen[0].index("--plugin-dir") + 1] == str(skill)


def test_run_uses_the_given_always_on_file(tmp_path, monkeypatch):
    tasks = [{"id": "t0", "form": "x", "prompt": "p", "fixtures": [], "expects_trigger": True}]
    (tmp_path / "evals").mkdir()
    (tmp_path / "evals" / "tasks.json").write_text(json.dumps(tasks))
    custom = tmp_path / "v08-always-on.md"
    custom.write_text("V08 LINES")
    seen = []
    monkeypatch.setattr(run, "execute", lambda cmd, cwd: seen.append((cwd / "CLAUDE.md").read_text()) or run.RunResult("ok", True, 1, 1))
    run.main(["run", "--arms", "real", "--models", "opus", "--reps", "1",
              "--always-on", str(custom), "--out", str(tmp_path / "out")], root=tmp_path)
    assert seen == ["V08 LINES"]


def test_default_always_on_is_the_published_file(tmp_path, monkeypatch):
    tasks = [{"id": "t0", "form": "x", "prompt": "p", "fixtures": [], "expects_trigger": True}]
    (tmp_path / "evals").mkdir()
    (tmp_path / "evals" / "tasks.json").write_text(json.dumps(tasks))
    (tmp_path / "always-on.md").write_text("PUBLISHED LINES")
    seen = []
    monkeypatch.setattr(run, "execute", lambda cmd, cwd: seen.append((cwd / "CLAUDE.md").read_text()) or run.RunResult("ok", True, 1, 1))
    run.main(["run", "--arms", "real", "--models", "opus", "--reps", "1", "--out", str(tmp_path / "out")], root=tmp_path)
    assert seen == ["PUBLISHED LINES"]
