"""Judge two arms blind, each pair twice with the order swapped, and score them per task."""

import argparse
import json
import random
import re
import shutil
import statistics
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import run

ROOT = Path(__file__).resolve().parent.parent
PROMPT_TEMPLATE = (ROOT / "evals" / "judge-prompt.md").read_text()
JUDGE_MODEL = "opus"
# On the quick question, flag arm a when its median length is more than this many times arm b's.
LENGTH_FLAG_RATIO = 1.5
# The fixtures follow the task prompt after this header; the owner sample shows only the request.
FIXTURE_HEADER = "\n\n--- "

JudgeFn = Callable[[str, str, str], tuple[str, str]]


@dataclass
class Pair:
    task_id: str
    rep: int
    a: Path
    b: Path


def make_pairs(runs: Path, model: str, arm_a: str, arm_b: str, runs_b: Path | None = None) -> list[Pair]:
    """Pair each arm-a output with the arm-b output for the same task and rep."""
    runs_b = runs_b or runs
    pairs = []
    for a_path in sorted((runs / model / arm_a).glob("*/rep*.json")):
        task_id, rep_file = a_path.parent.name, a_path.name
        b_path = runs_b / model / arm_b / task_id / rep_file
        if b_path.exists():
            pairs.append(Pair(task_id, int(rep_file[3:-5]), a_path, b_path))
    return pairs


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def judge_pair(pair: Pair, judge_fn: JudgeFn, log: list | None = None) -> str:
    """Return "a", "b" or "tie". Each order is judged once; a split decision is a tie."""
    a, b = _load(pair.a), _load(pair.b)
    if not a["text"] or not b["text"]:
        # a failed run loses without spending a judge call
        return "tie" if a["text"] == b["text"] else ("a" if a["text"] else "b")
    first, first_reason = judge_fn(a["prompt"], a["text"], b["text"])
    second, second_reason = judge_fn(a["prompt"], b["text"], a["text"])
    if log is not None:
        log.append({"task_id": pair.task_id, "rep": pair.rep, "order": "a-first", "winner": first, "reason": first_reason})
        log.append({"task_id": pair.task_id, "rep": pair.rep, "order": "b-first", "winner": second, "reason": second_reason})
    a_votes = (first == "1") + (second == "2")
    b_votes = (first == "2") + (second == "1")
    if a_votes == 2:
        return "a"
    if b_votes == 2:
        return "b"
    return "tie"


def score(verdicts: dict[tuple[str, int], str]) -> dict[str, str]:
    """Per task, the majority of non-tie verdicts: "win" for arm a, "loss", or "tie"."""
    tally: dict[str, list[int]] = {}
    for (task_id, _rep), verdict in verdicts.items():
        counts = tally.setdefault(task_id, [0, 0])
        if verdict == "a":
            counts[0] += 1
        elif verdict == "b":
            counts[1] += 1
    return {
        task_id: "win" if a > b else "loss" if b > a else "tie"
        for task_id, (a, b) in sorted(tally.items())
    }


def length_flag(a_words: list[int], b_words: list[int]) -> bool:
    return statistics.median(a_words) > LENGTH_FLAG_RATIO * statistics.median(b_words)


def owner_sample(pairs: list[Pair], n: int = 10, seed: int = 0) -> tuple[str, dict]:
    """A markdown page of unlabelled reply pairs in random order, and the key to it."""
    rng = random.Random(seed)
    chosen = rng.sample(pairs, min(n, len(pairs)))
    sections, key = [], {}
    for number, pair in enumerate(chosen, start=1):
        a, b = _load(pair.a), _load(pair.b)
        a_first = rng.random() < 0.5
        reply_1, reply_2 = (a, b) if a_first else (b, a)
        request = a["prompt"].split(FIXTURE_HEADER, 1)[0]
        sections.append(
            f"## Pair {number}\n\n**Request:** {request}\n\n"
            f"### Reply 1\n\n{reply_1['text']}\n\n### Reply 2\n\n{reply_2['text']}\n"
        )
        key[number] = {"task_id": pair.task_id, "rep": pair.rep, "reply_1": "a" if a_first else "b"}
    page = "# Blind sample\n\nFor each pair, note which reply you would rather receive: 1 or 2.\n\n" + "\n".join(sections)
    return page, key


def claude_judge(request: str, reply_1: str, reply_2: str) -> tuple[str, str]:
    """The default judge: Opus in the clean setup, answering in JSON."""
    prompt = (PROMPT_TEMPLATE.replace("{request}", request)
              .replace("{reply_1}", reply_1).replace("{reply_2}", reply_2))
    workdir = run.workdir_for("baseline", ROOT / "evals" / "always-on" / "CLAUDE.md")
    try:
        result = run.execute(run.build_command("baseline", JUDGE_MODEL, prompt, ROOT), workdir)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    match = re.search(r"\{.*\}", result.text, re.DOTALL)
    try:
        answer = json.loads(match.group(0)) if match else {}
    except json.JSONDecodeError:
        answer = {}
    winner = str(answer.get("winner", ""))
    # an unreadable answer counts as no preference, which makes the pair a tie
    return (winner if winner in ("1", "2") else "", answer.get("reason", result.error or result.text[:200]))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, required=True)
    parser.add_argument("--runs-b", type=Path, help="where arm b's outputs live, if not in --runs")
    parser.add_argument("--model", required=True)
    parser.add_argument("--a", required=True)
    parser.add_argument("--b", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--owner-sample", type=int, default=0, help="also write a blind sample of N pairs")
    args = parser.parse_args(argv)

    pairs = make_pairs(args.runs, args.model, args.a, args.b, args.runs_b)
    out = args.runs / args.model / f"judge-{args.a}-vs-{args.b}.json"
    done = json.loads(out.read_text()) if out.exists() else {"verdicts": {}, "log": []}
    todo = [p for p in pairs if f"{p.task_id}/{p.rep}" not in done["verdicts"]]
    print(f"{len(todo)} pairs, up to {2 * len(todo)} judge calls")
    if args.dry_run:
        return 0

    def do(pair: Pair) -> tuple[Pair, str, list]:
        log: list = []
        return pair, judge_pair(pair, claude_judge, log), log

    with ThreadPoolExecutor(run.WORKERS) as pool:
        for pair, verdict, log in pool.map(do, todo):
            done["verdicts"][f"{pair.task_id}/{pair.rep}"] = verdict
            done["log"] += log
            out.write_text(json.dumps(done, indent=2))
            print(f"{pair.task_id}/rep{pair.rep}: {verdict}", flush=True)

    verdicts = {(k.split("/")[0], int(k.split("/")[1])): v for k, v in done["verdicts"].items()}
    per_task = score(verdicts)
    print(f"\n{'task':<22}{'verdict':<8}{args.a + ' words':>14}{args.b + ' words':>16}")
    for task_id, verdict in per_task.items():
        task_pairs = [p for p in pairs if p.task_id == task_id]
        a_words = [len(_load(p.a)["text"].split()) for p in task_pairs]
        b_words = [len(_load(p.b)["text"].split()) for p in task_pairs]
        flag = "  LONGER" if task_id == "quick-question" and length_flag(a_words, b_words) else ""
        print(f"{task_id:<22}{verdict:<8}{statistics.median(a_words):>14}{statistics.median(b_words):>16}{flag}")
    results = list(per_task.values())
    print(f"\n{args.a} vs {args.b} on {args.model}: {results.count('win')} wins, "
          f"{results.count('loss')} losses, {results.count('tie')} ties")

    if args.owner_sample:
        page, key = owner_sample(pairs, args.owner_sample)
        (args.runs / args.model / "owner-sample.md").write_text(page)
        (args.runs / args.model / "owner-sample-key.json").write_text(json.dumps(key, indent=2))
        print(f"owner sample: {args.runs / args.model / 'owner-sample.md'} (keep the key file closed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
