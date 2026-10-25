"""Run the writing tasks through Claude Code headless, in a clean setup.

The clean setup was settled by a spike on Claude Code 2.1.283, without an API key:
  --setting-sources project  keeps out the user's CLAUDE.md, personal skills, plugins and hooks
  --strict-mcp-config        keeps out every MCP server
  Each call runs from a fresh temp folder. For the real and forced arms that folder holds the
  always-on lines as CLAUDE.md, which is where a user would put them. (--add-dir did not load them.)
  --add-dir on the plugin folder lets the skill read its own reference files; without it, headless
  mode denied the Read and the skill ran on SKILL.md alone.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARMS = ("baseline", "real", "forced")
SLASH_COMMAND = "/wordcraft:wordcraft"
CLEAN_FLAGS = [
    "--setting-sources", "project",
    "--strict-mcp-config",
    "--output-format", "stream-json",
    "--verbose",
]
# Words that only appear when the user's own setup leaked in.
LEAK_MARKERS = ("humanizer", "unslop", "poteto", "superpowers", "behavioral guidelines")
# A long-session summary on Opus can take several minutes.
TIMEOUT_SECONDS = 600
WORKERS = 4
REFERENCE_FILES = ("principles.md", "forms.md")
LIST_PROMPT = (
    "List every skill you can use, by name. Then quote the first line of any "
    "CLAUDE.md instructions you were given, or say 'none'."
)


@dataclass
class RunResult:
    text: str
    skill_triggered: bool
    input_tokens: int
    output_tokens: int
    error: str = ""
    reference_reads: list[str] = field(default_factory=list)


def build_command(arm: str, model: str, prompt: str, plugin_dir: Path) -> list[str]:
    if arm not in ARMS:
        raise ValueError(f"unknown arm {arm!r}; expected one of {ARMS}")
    if arm == "forced":
        prompt = f"{SLASH_COMMAND} {prompt}"
    cmd = ["claude", "-p", prompt, "--model", model, *CLEAN_FLAGS]
    if arm != "baseline":
        cmd += ["--plugin-dir", str(plugin_dir), "--add-dir", str(plugin_dir)]
    return cmd


def workdir_for(arm: str, always_on: Path) -> Path:
    workdir = Path(tempfile.mkdtemp(prefix="wordcraft-"))
    if arm != "baseline":
        shutil.copy(always_on, workdir / "CLAUDE.md")
    return workdir


def parse_stream(lines: list[str]) -> RunResult:
    triggered = False
    reads: list[str] = []
    result = None
    for line in lines:
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                if (
                    block.get("type") == "tool_use"
                    and block.get("name") == "Skill"
                    and "wordcraft" in str(block.get("input", {}).get("skill", ""))
                ):
                    triggered = True
                if block.get("type") == "tool_use" and block.get("name") == "Read":
                    name = Path(str(block.get("input", {}).get("file_path", ""))).name
                    if name in REFERENCE_FILES:
                        reads.append(name)
        elif event.get("type") == "result":
            result = event
    if result is None:
        raise ValueError("stream has no result event")
    usage = result.get("usage", {})
    input_tokens = (
        usage.get("input_tokens", 0)
        + usage.get("cache_creation_input_tokens", 0)
        + usage.get("cache_read_input_tokens", 0)
    )
    return RunResult(result.get("result") or "", triggered, input_tokens, usage.get("output_tokens", 0),
                     reference_reads=reads)


def _subprocess_runner(cmd: list[str], cwd: Path) -> list[str]:
    done = subprocess.run(
        cmd, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True,
        text=True, timeout=TIMEOUT_SECONDS, check=True,
    )
    return done.stdout.splitlines()


def execute(cmd: list[str], cwd: Path, runner=_subprocess_runner) -> RunResult:
    """Run one call, retrying once; a call that fails twice is recorded, not raised."""
    last_error = ""
    for _ in range(2):
        try:
            return parse_stream(runner(cmd, cwd))
        except (subprocess.SubprocessError, OSError, ValueError) as exc:
            last_error = repr(exc)
    return RunResult("", False, 0, 0, error=last_error)


def is_clean(text: str) -> bool:
    lowered = text.lower()
    return not any(marker in lowered for marker in LEAK_MARKERS)


def load_tasks(root: Path, task_set: str = "") -> list[dict]:
    # task_set "" is the original ten tasks; "heldout" is evals/heldout/
    return json.loads((root / "evals" / task_set / "tasks.json").read_text())


def load_task_prompt(task: dict, root: Path, task_set: str = "") -> str:
    parts = [task["prompt"]]
    for name in task["fixtures"]:
        content = (root / "evals" / task_set / "fixtures" / name).read_text()
        parts.append(f"--- {name} ---\n{content}")
    return "\n\n".join(parts)


def run_all(root: Path, arms: list[str], models: list[str], reps: int,
            task_ids: list[str], out: Path, dry_run: bool,
            task_set: str = "", skill_dir: Path | None = None, always_on: Path | None = None) -> None:
    tasks = load_tasks(root, task_set)
    skill_dir = skill_dir or root
    if task_ids != ["all"]:
        tasks = [t for t in tasks if t["id"] in task_ids]
    jobs = []
    for model in models:
        for arm in arms:
            for task in tasks:
                for rep in range(1, reps + 1):
                    path = out / model / arm / task["id"] / f"rep{rep}.json"
                    # a rerun only redoes calls that are missing or failed
                    if path.exists() and not json.loads(path.read_text()).get("error"):
                        continue
                    jobs.append((model, arm, task, rep, path))
    print(f"{len(jobs)} calls")
    if dry_run:
        return
    always_on = always_on or root / "always-on.md"

    def do(job):
        model, arm, task, rep, path = job
        prompt = load_task_prompt(task, root, task_set)
        workdir = workdir_for(arm, always_on)
        try:
            result = execute(build_command(arm, model, prompt, skill_dir), workdir)
        finally:
            shutil.rmtree(workdir, ignore_errors=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        record = {**asdict(result), "model": model, "arm": arm, "task_id": task["id"], "rep": rep, "prompt": prompt}
        path.write_text(json.dumps(record, indent=2))
        status = (f"error: {result.error}" if result.error else
                  f"{len(result.text.split())} words, skill={result.skill_triggered}, reads={result.reference_reads}")
        print(f"{model}/{arm}/{task['id']}/rep{rep}: {status}", flush=True)

    with ThreadPoolExecutor(WORKERS) as pool:
        list(pool.map(do, jobs))


def probe(root: Path, model: str = "haiku") -> int:
    """Three live calls that check the plumbing with a stand-in skill. Exit 0 only if clean."""
    stub_plugin = root / "tests" / "fixtures" / "stub-plugin"
    stub_always_on = root / "tests" / "fixtures" / "stub-always-on.md"
    checks = [
        ("baseline", LIST_PROMPT,
         lambda r: is_clean(r.text) and "wordcraft" not in r.text.lower()),
        ("real", LIST_PROMPT,
         lambda r: is_clean(r.text) and r.text.lstrip().startswith("Okay") and "wordcraft" in r.text.lower()),
        ("forced", "Write a two-line note to a colleague saying the meeting moved to 3pm.",
         lambda r: r.skill_triggered and "PINEAPPLE" in r.text),
    ]
    failures = 0
    for arm, prompt, passes in checks:
        workdir = workdir_for(arm, stub_always_on)
        try:
            result = execute(build_command(arm, model, prompt, stub_plugin), workdir)
        finally:
            shutil.rmtree(workdir, ignore_errors=True)
        ok = not result.error and passes(result)
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'} {arm}: {result.error or result.text[:200]!r}")
    return 1 if failures else 0


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    run_p = sub.add_parser("run", help="run tasks and save each output")
    run_p.add_argument("--arms", nargs="+", choices=ARMS, required=True)
    run_p.add_argument("--models", nargs="+", required=True)
    run_p.add_argument("--reps", type=int, default=3)
    run_p.add_argument("--tasks", nargs="+", default=["all"])
    run_p.add_argument("--out", type=Path, required=True)
    run_p.add_argument("--dry-run", action="store_true")
    run_p.add_argument("--task-set", default="", help="a folder under evals/ with its own tasks.json, e.g. heldout")
    run_p.add_argument("--skill-dir", type=Path, help="plugin folder holding the skill version to test (default: this repo)")
    run_p.add_argument("--always-on", type=Path, help="always-on lines for that version (default: always-on.md)")
    probe_p = sub.add_parser("probe", help="check the clean setup with three live calls")
    probe_p.add_argument("--model", default="haiku")
    args = parser.parse_args(argv)
    if args.command == "probe":
        return probe(root, args.model)
    run_all(root, args.arms, args.models, args.reps, args.tasks, args.out, args.dry_run, args.task_set, args.skill_dir, args.always_on)
    return 0


if __name__ == "__main__":
    sys.exit(main())
