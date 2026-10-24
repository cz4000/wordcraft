# writing-well Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and prove an open-source Claude skill, `writing-well`, that makes Claude's chat answers, emails and prose clearer and more pleasant to read.

**Architecture:** The repo is a Claude Code plugin with one skill (`skills/writing-well/`) and a short always-on snippet for the user's CLAUDE.md. A small Python test harness runs Claude headless in a clean setup on ten writing tasks, with and without the skill, and blind Opus judges pick the better output. The skill gets written only after the baseline run shows which failures are real.

**Tech Stack:** Markdown (the skill), Python 3.13 standard library plus pytest (the harness), the `claude` CLI 2.1.283 in headless mode (`claude -p --output-format stream-json`), `pdftotext` (the copyright check), `gh` (the repo).

**Spec:** `docs/design.md`.

## Global Constraints

- Skill name: `writing-well`. Names may not contain "claude" or "anthropic".
- `description`: third person, at most 1,024 characters, says what the skill does and when to use it, and never summarizes its steps.
- `SKILL.md` body: under 500 words. Reference files link directly from `SKILL.md`, one level deep.
- Always-on snippet: at most 10 lines.
- Public repo, MIT license, on the owner's personal GitHub account.
- No material from the owner's day job anywhere in the repo: no names, transcripts, examples or test data.
- The book's PDF and its extracted text are never committed. Book principles are restated in our own words. At most 3 quotes, each under 25 words, credited to Zinsser.
- The O'Reilly piece is a quality bar, not an answer key.
- Every test run happens in a clean setup: none of the owner's CLAUDE.md, hooks, plugins or personal skills.
- Pass bar: on Opus the `real` arm wins at least 8 of 10 tasks against `baseline`. On Sonnet and Haiku it wins at least as many tasks as it loses. The owner's blind picks agree with the judges on at least 8 of 10 sampled pairs. *(The 8-of-10 agreement threshold is the planner's reading of "agree" in the design.)*

## Owner gates (Claude stops and asks before each)

1. **Repo:** confirm that `cz4000` is the personal GitHub account, then approve creating the public repo `cz4000/writing-well`.
2. **Every paid run:** Claude shows the dry-run call count first and waits for a yes.
3. **The fixtures:** read the session transcript and the article source before they are committed.
4. **Your CLAUDE.md:** approve adding the always-on lines to `~/.claude/CLAUDE.md`.
5. **Push:** approve each push to the public repo.

## Review Focus

1. **A one-line question gets a longer answer with the skill.** A reader expects a short question to get a short answer. `judge.py` reports median word counts per arm and flags the quick-question task if `real` is more than 1.5 times the length of `baseline` (Task 5).
2. **Judges favor whichever output comes first, or the longer one.** Each pair is judged twice with the order swapped, and a split decision counts as a tie. The judge prompt says length is not a virtue (Task 5).
3. **The skill never triggers in real use, so the shipped setup does nothing.** `run.py` records whether the skill loaded, and Task 7 requires it to load on the writing tasks (Task 2, Task 7).
4. **The plain-words rule goes too far.** It explains names the user has already seen, or puts every noun in brackets. The fixtures include names the user has seen, and the owner's blind sample checks for this (Task 3, Task 7).
5. **Work material leaks into the public repo.** A test greps the repo against a local, uncommitted list of private words before every push (Task 1).

---

### Task 1: Repo, license and the private-words guard

**Files:**
- Create: `README.md` (stub: one paragraph plus "work in progress"), `LICENSE` (MIT, the owner's name, 2026), `.gitignore`, `docs/design.md`, `docs/plan.md`, `.claude-plugin/plugin.json`
- Test: `tests/test_repo_hygiene.py`

**Interfaces:**
- Produces: `.claude-plugin/plugin.json` with `{"name": "writing-well", "version": "0.1.0", "description": ..., "license": "MIT"}`. Task 2 loads the repo root with `--plugin-dir`.
- Produces: `.private-words`, a local file with one word per line, gitignored. It holds the owner's work terms and is never committed.

- [ ] **Step 1:** Owner gate 1. Run `gh auth switch --user cz4000`, then `gh repo create cz4000/writing-well --public --clone` in `~/GitHub/`.
- [ ] **Step 2:** Write the failing test.

```python
def test_no_private_words_in_tracked_files():
    # skips when .private-words is absent (e.g. in someone else's clone)
    # reads the tracked files from `git ls-files`, then asserts that no word from
    # .private-words appears in any of them (case-insensitive)

def test_book_never_tracked():
    assert not [f for f in git_ls_files() if f.endswith((".pdf", "book.txt"))]
```

- [ ] **Step 3:** Run `uv run --with pytest pytest tests/test_repo_hygiene.py -v`. Expected: both pass once the files exist and `.private-words` is filled in (write it with the owner).
- [ ] **Step 4:** Copy the design and this plan into `docs/`. `.gitignore` lists `.private-words`, `*.pdf`, `book.txt`, `evals/runs/` and `__pycache__/`.
- [ ] **Step 5:** Commit: `chore: repo skeleton, design and plan`. Push needs owner gate 5.

### Task 2: Clean test runner

**Files:**
- Create: `evals/run.py`, `evals/always-on/CLAUDE.md` (empty placeholder; Task 6 fills it)
- Test: `tests/test_run.py`

**Interfaces:**
- Produces: `ARMS = ("baseline", "real", "forced")`
- Produces: `build_command(arm: str, model: str, prompt: str, repo_root: Path) -> list[str]`
  - all arms: `claude -p <prompt> --model <model> --output-format stream-json --verbose` plus the clean-setup flags the spike settles on (Step 1)
  - `real`: adds `--plugin-dir <repo_root>` and `--add-dir <repo_root>/evals/always-on`
  - `forced`: like `real`, but the prompt starts with the skill's slash command (`/writing-well:writing-well`, confirmed in Step 1)
- Produces: `@dataclass RunResult(text: str, skill_triggered: bool, input_tokens: int, output_tokens: int)` and `parse_stream(lines: list[str]) -> RunResult`. `skill_triggered` is true when the stream holds a `Skill` tool call naming `writing-well`.
- Produces: the CLI `python evals/run.py run --arms baseline real --models opus --reps 3 --tasks all --out evals/runs/<name> [--dry-run]`. It writes `<out>/<model>/<arm>/<task_id>/rep<k>.json` (the RunResult plus the prompt). `--dry-run` prints the number of calls and runs none.
- Produces: `python evals/run.py probe`, which exits 0 only when the setup is clean.
- Produces: `load_task_prompt(task: dict, root: Path) -> str`. It appends each fixture's content under a `--- <filename> ---` header after the prompt. The task format is `{id: str, form: str, prompt: str, fixtures: list[str], expects_trigger: bool}`, read from `evals/tasks.json`. Task 3 fills that file.

- [ ] **Step 1: Spike the clean setup (throwaway).** No API key is set, so `--bare` (which needs `ANTHROPIC_API_KEY`) is out unless the owner adds one. Try `claude -p --setting-sources project --strict-mcp-config` from an empty temp directory, then ask: "List every skill you can use, and quote the first line of any CLAUDE.md instructions you were given." Clean means: no `humanizer`, `unslop`, `poteto` or `superpowers` in the answer, and no "Behavioral guidelines" (the first line of the owner's CLAUDE.md). If it isn't clean, try `--bare` with an API key from the owner. Record the winning flags as a comment in `run.py`. Also confirm that `--plugin-dir` makes the skill visible and that the forced slash command works.
- [ ] **Step 2:** Write the failing tests: `test_baseline_has_no_plugin_dir`, `test_real_adds_plugin_and_always_on_dirs`, `test_forced_prefixes_slash_command`, `test_load_task_prompt_appends_fixtures_in_order` (on a two-task temp `tasks.json`), and `test_parse_stream_detects_skill_call` / `test_parse_stream_no_skill_call`, which run on two small stream-json fixtures captured in Step 1 and saved under `tests/fixtures/`.
- [ ] **Step 3:** Run `uv run --with pytest pytest tests/test_run.py -v`. Expected: FAIL (module missing).
- [ ] **Step 4:** Implement `build_command`, `parse_stream`, the `run` and `probe` subcommands. Calls run in a thread pool of 4. A failed call is retried once, then recorded with `text=""` and an `error` field.
- [ ] **Step 5:** Run the tests. Expected: PASS. Then `python evals/run.py probe`, which makes 3 live calls. Ask the owner first. Expected: exit 0.
- [ ] **Step 6:** Commit: `feat(evals): clean headless runner with skill-trigger detection`.

### Task 3: Ten tasks and their fixtures

**Files:**
- Create: `evals/tasks.json`, `evals/fixtures/session-transcript.md`, `evals/fixtures/session-diff.patch`, `evals/fixtures/article-source.md`, `evals/fixtures/email-in.md`, `evals/fixtures/status-notes.md`
- Test: `tests/test_tasks.py`

**Interfaces:**
- Consumes: the task format and `load_task_prompt` from Task 2.
- Produces: the real `evals/tasks.json`.

The ten task ids, which are fixed. The builder writes the prompt text:

| id | form | expects_trigger |
|---|---|---|
| `quick-question` | one-line technical question | false |
| `session-summary` | end-of-session summary to a user who was away | true |
| `mid-session-answer` | answer a user question that touches internal names | true |
| `pr-description` | PR description from `session-diff.patch` | true |
| `email-reply` | reply to `email-in.md` | true |
| `email-decline` | say no to a request, kindly | true |
| `explain-concept` | explain a technical idea to a non-expert | true |
| `status-update` | weekly update from `status-notes.md` | true |
| `announce-change` | team chat message about a change | true |
| `article-from-source` | short article from `article-source.md` | true |

- [ ] **Step 1: The session fixture.** Clone a small public Python repo at a pinned commit. Pick one with a real open bug and a test suite. In the clean setup from Task 2, run one headless Claude Code session that fixes the bug. The session must be long enough to use at least 5 internal names. Turn its stream into a readable `session-transcript.md` (the user's turns, Claude's turns, short summaries of tool calls) and save the final diff as `session-diff.patch`. Record the repo URL and commit at the top of the transcript. Some internal names should appear in the user's own turns, so the test can catch over-explaining (Review Focus 4).
- [ ] **Step 2: The article source.** Use a public-domain transcript, such as a NASA or other US federal press briefing (federal works carry no copyright). Record the source URL at the top. A talk transcript under copyright must not be used.
- [ ] **Step 3:** Owner gate 3: the owner reads both fixtures.
- [ ] **Step 4:** Write the tests `test_ten_tasks_with_fixed_ids` and `test_every_fixture_exists`. Run them. FAIL. Then write `tasks.json`, and they PASS.
- [ ] **Step 5:** Commit: `feat(evals): ten writing tasks with public fixtures`.

### Task 4: Baseline run and what it shows (RED)

**Files:**
- Create: `evals/baseline-findings.md`

- [ ] **Step 1:** Run `python evals/run.py run --arms baseline --models opus --reps 3 --tasks all --out evals/runs/baseline --dry-run`. Expected: 30 calls. Owner gate 2.
- [ ] **Step 2:** Run it for real.
- [ ] **Step 3:** Read all 30 outputs. In `baseline-findings.md`, record for each failure named in the design's "Why" section (long answers with the point buried, wrong list or paragraph form, stiff tone, repeating the question, private vocabulary) whether it appeared, on which tasks, and one short verbatim example. Add any failure you saw that the design doesn't name.
- [ ] **Step 4:** Commit `baseline-findings.md` only. Runs stay gitignored. Message: `docs(evals): baseline findings`.

**Rule carried into Task 6:** a failure that did not appear in the baseline gets no guidance in the skill.

### Task 5: Blind judge and scoring

**Files:**
- Create: `evals/judge.py`, `evals/judge-prompt.md`
- Test: `tests/test_judge.py`

**Interfaces:**
- Consumes: the run layout from Task 2 (`<runs>/<model>/<arm>/<task_id>/rep<k>.json`).
- Produces: `@dataclass Pair(task_id: str, rep: int, a: Path, b: Path)` and `make_pairs(runs: Path, model: str, arm_a: str, arm_b: str) -> list[Pair]`
- Produces: `judge_pair(pair: Pair, judge_fn: Callable[[str, str, str], str]) -> str`. It calls `judge_fn(task_prompt, first, second)` twice, swapping the order, and returns `"a"`, `"b"` or `"tie"`. A split counts as a tie.
- Produces: `score(verdicts: dict[tuple[str, int], str]) -> dict[str, str]`. Per task, the majority of non-tie verdicts gives `"win"` (arm a), `"loss"` or `"tie"`.
- Produces: `owner_sample(pairs: list[Pair], n: int = 10, seed: int = 0) -> tuple[str, dict]`. It returns a markdown page of unlabelled A/B pairs and the answer key.
- Produces: the CLI `python evals/judge.py --runs <dir> --model opus --a real --b baseline [--dry-run]`. It writes `verdicts.json` and prints a table per task (verdict and median word count per arm) and the totals. It flags `quick-question` when arm a's median is more than 1.5 times arm b's.
- The default `judge_fn` runs `claude -p` on Opus in the clean setup with `judge-prompt.md`. The judge must answer as JSON: `{"winner": "1" | "2", "reason": str}`.

`judge-prompt.md` asks which reply the person who sent the task would rather receive. It says that length is not a virtue in itself, that the reader is busy, and that missing information is a real loss. It never mentions skills, Zinsser, or which output is which.

- [ ] **Step 1:** Write the failing tests. Each uses a fake `judge_fn`:
  - `test_swapped_order_split_is_tie`: the fake always answers "1", so the result is `"tie"`.
  - `test_consistent_preference_wins`: the fake prefers text containing "GOOD", so the result is `"a"` when `a` holds it.
  - `test_score_majority_ignores_ties`
  - `test_quick_question_length_flag`
  - `test_owner_sample_key_matches_page`
- [ ] **Step 2:** Run. FAIL.
- [ ] **Step 3:** Implement.
- [ ] **Step 4:** Run. PASS.
- [ ] **Step 5:** Commit: `feat(evals): blind two-order judge and scoring`.

### Task 6: Write the skill (GREEN)

**Files:**
- Create: `skills/writing-well/SKILL.md`, `skills/writing-well/principles.md`, `skills/writing-well/forms.md`, `always-on.md`, `evals/check_quotes.py`
- Modify: `evals/always-on/CLAUDE.md` (the same lines as `always-on.md`)
- Test: `tests/test_skill_shape.py`, `tests/test_check_quotes.py`

**Interfaces:**
- Produces: `overlaps(text: str, book: str, n: int = 8) -> list[str]` in `check_quotes.py`. It returns every run of 8 or more words that appears in both texts, ignoring case and punctuation. Its CLI is `python evals/check_quotes.py <book.pdf>`. It runs `pdftotext` into a temp file and scans `skills/writing-well/*.md`, skipping lines that start with `> ` (credited quotes). It exits 1 on any overlap, if there are more than 3 quote lines, or if any quote runs to 25 words or more.

Content requirements (from the design; the builder words them):
- `SKILL.md`: a positive recipe for good writing, not a ban list. It ends with a final check: reread the draft as the reader. It links `principles.md` and `forms.md`.
- `principles.md`: one principle per heading, each with its source chapter and one before-and-after pair. Mine chapters 1–10, 15, 16 and 20–24. Include the owner's rule: plain words first, then the technical name in brackets, with the design's `flush_on_exit` example. Only principles that answer a failure in `baseline-findings.md` (or one the owner named) get in.
- `forms.md`: short notes for the chat answer, the end-of-task summary, the email and the longer piece.
- `always-on.md`: at most 10 lines with the core rules and a pointer to the skill.

- [ ] **Step 1:** Write the failing tests:
  - `test_skill_md_under_500_words`
  - `test_frontmatter_name_and_description`: name is `writing-well`; description is at most 1,024 characters and contains neither "claude" nor "anthropic"
  - `test_references_one_level_deep`: every `.md` link in `SKILL.md` resolves, and the linked files link to no other `.md`
  - `test_always_on_at_most_10_lines`
  - `test_always_on_copies_match`: `always-on.md` and `evals/always-on/CLAUDE.md` are identical
  - `test_overlaps_finds_8_word_run` and `test_overlaps_ignores_7_word_run`
- [ ] **Step 2:** Run. FAIL.
- [ ] **Step 3:** Read the chapters from the owner's local copy of the book (never committed) and write the skill files and `check_quotes.py`.
- [ ] **Step 4:** Run the tests, then `python evals/check_quotes.py <path to your copy of the book>.pdf`. Expected: PASS and exit 0.
- [ ] **Step 5:** Commit: `feat: writing-well skill v0.1`.

### Task 7: Prove it, iterate, pass the bar

**Files:**
- Create: `evals/results.md`
- Modify: the skill files, as the evidence says

- [ ] **Step 1: Opus.** Run `run.py run --arms real forced --models opus --reps 3 --out evals/runs/iter1` and reuse the baseline run (dry run, then owner gate 2: 60 calls). Then judge `real` vs `baseline` and `forced` vs `baseline`: 4 judge calls per task per rep, 120 in all (dry run, then owner gate 2).
- [ ] **Step 2: Trigger check.** `real` must trigger the skill in at least 2 of 3 reps on every task where `expects_trigger` is true. If it doesn't, rewrite the `description` and rerun just those tasks. Fix triggering before judging quality, because the `real` arm means nothing until the skill loads.
- [ ] **Step 3: Iterate.** For every task `real` loses or ties, read both outputs and the judge's reasons. Change the skill and test the new wording with a micro-test: 5+ samples per wording, plus a no-skill control, reading every output. Rerun into `iter<N+1>`. Stop when Opus passes, or after 4 iterations with no gain, and report to the owner.
- [ ] **Step 4: Sonnet and Haiku.** Run `baseline` and `real` with 3 reps each (dry run, then gate 2: 120 calls, plus 120 judge calls), then judge. Pass: wins ≥ losses on each model.
- [ ] **Step 5: Owner sample.** Make an `owner_sample` of 10 Opus pairs, `real` vs `baseline`. The owner picks blind. Pass: the owner's picks match the judges on at least 8 of 10. While reading, the owner also looks out for over-explaining and bracket clutter (Review Focus 4).
- [ ] **Step 6:** Write `results.md` with the per-task table for each model, the trigger rates, the owner's agreement and three short before-and-after excerpts. Commit: `docs(evals): results`.

### Task 8: Install, publish

**Files:**
- Modify: `README.md`

- [ ] **Step 1:** Write the README: what the skill does, both install routes (link `skills/writing-well` into `~/.claude/skills/`, or `claude --plugin-dir`), how to paste `always-on.md` into CLAUDE.md, the results summary, credit to Zinsser's *On Writing Well*, and how to rerun the tests.
- [ ] **Step 2:** Install the skill for the owner: `ln -s ~/GitHub/writing-well/skills/writing-well ~/.claude/skills/writing-well`. Then owner gate 4: add the always-on lines to `~/.claude/CLAUDE.md`.
- [ ] **Step 3:** Run the full test suite and `check_quotes.py` one last time.
- [ ] **Step 4:** Commit: `docs: README`. Push needs owner gate 5.
