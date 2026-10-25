# Results

wordcraft was built and tested on 24 and 25 October 2026 with Claude Code 2.1.283. This page says what the tests found, including where the skill falls short. The raw outputs and judge logs (about 400 files) are kept out of the repo to keep it small. `evals/run.py` and `evals/judge.py` regenerate them.

## The short version

With wordcraft v0.5, blind judges preferred Opus's writing in 21 of 25 decided pairs (84%), and it lost no task. Haiku (tested on v0.4) came out at about seven in ten. On Sonnet (v0.4) the skill made no measurable difference. The bar set before testing was **not** met in full: Opus won 7 of 10 tasks and tied the other 3, short of 8 wins.

Three limits apply to every number here:

- **Tuned and scored on the same tasks.** Each version was adjusted after seeing results on the same ten tasks it was scored on, with no held-out tasks. The gains may not carry over in full to new writing.
- **Reference files go unread.** After the test setup stopped blocking them (v0.4.1), Claude opened `principles.md` or `forms.md` in only 1 of 30 replies. v0.5 therefore moved the form guidance into `SKILL.md` and retired `forms.md`. `principles.md` was opened in none of the 30 v0.5 replies.
- **Thirty pairs are ten tasks.** Each run's 30 pairs are 10 tasks × 3 samples, not 30 independent cases.

The skill does not make Claude's writing look human to an AI detector, and wasn't designed to.

## How it was tested

- **Ten everyday writing tasks** (`evals/tasks.json`):
  - a quick chat question;
  - an end-of-session summary;
  - a mid-session question;
  - a pull request description;
  - two emails;
  - an explanation for a non-technical manager;
  - a status update;
  - a team announcement;
  - a short article.

  The two long sources are public: a real bug fix on the open-source `humanize` library, and a Federal Reserve press conference transcript. The incoming email and the status notes were written for the test.
- **A clean setup.** Claude ran headless with none of the tester's own instructions, skills, plugins or MCP servers (`evals/run.py`). "With the skill" means the shipped setup: the always-on lines as `CLAUDE.md`, plus the skill installed and left to load on its own.
- **Three samples per task**, with and without the skill.
- **Blind judges.** Opus saw each pair in both orders and picked the reply the requester would rather receive. A split decision counts as a tie. The judge prompt never mentions the skill (`evals/judge-prompt.md`).
- **The owner's own blind reads:** 10 pairs after round 1, and 8 of 10 pairs after round 3 (the owner skipped two).

Rounds 1 to 6 tested v0.1, v0.2, v0.3, v0.4, v0.4.1 and v0.5. Round 1 also ran a third version that forced the skill on. The judges preferred it in 10 pairs and the baseline in 14, with 6 ties, so it was dropped.

## What the baseline got wrong

From 30 Opus outputs without the skill (`evals/baseline-findings.md`):

- answers far longer than the question needed;
- chat formatted like a document;
- internal names the reader had never seen;
- stock phrases;
- notes about the draft after the draft;
- two invented details;
- decorative emoji.

It already led with the answer and wrote plainly, so the skill leaves those alone.

## Results by version

Pairs where the judges preferred one version in both orders, out of 30 per run. The p-value is a two-sided sign test on the decided pairs.

| Model | Version | Skill better | Baseline better | Tie | Skill's share | p |
|---|---|---|---|---|---|---|
| Opus | v0.1 | 15 | 11 | 4 | 58% | 0.56 |
| Opus | v0.2 | 16 | 8 | 6 | 67% | 0.15 |
| Opus | v0.3 | 19 | 5 | 6 | 79% | 0.007 |
| Opus | v0.4 | 17 | 7 | 6 | 71% | 0.06 |
| Opus | v0.4.1 | 19 | 7 | 4 | 73% | 0.03 |
| Opus | **v0.5** | 21 | 4 | 5 | 84% | 0.001 |
| Sonnet | v0.3 | 11 | 14 | 5 | 44% | 0.69 |
| Sonnet | v0.4 | 12 | 11 | 7 | 52% | 1.0 |
| Haiku | v0.3 | 18 | 9 | 3 | 67% | 0.12 |
| Haiku | v0.4 | 18 | 7 | 5 | 72% | 0.04 |

What changed between versions:

- **v0.2:**
  - Say what each change is for and why it matters.
  - Match the shape to the content: lists and headed groups for separate items, paragraphs for reasoning.
  - Keep every fact the reader needs.
  - Added Orwell's six rules.
- **v0.3:**
  - Never invent a specific to sound personal.
  - Flag outside facts.
  - Added Euchner's ten rules.
- **v0.4:**
  - Never claim a check, fix or release the work doesn't show.
  - Never mention the skill in a reply.
- **v0.4.1:**
  - The always-on lines say "answer first".
  - The skill's description stops claiming chat questions, which the always-on lines now cover.
  - The test setup lets the skill read its reference files.
  - Only Opus was rerun.
- **v0.4.2:** v0.4.1 plus wording fixes from a final edit. It fixes three examples in `principles.md` that broke their own principle, and clarifies two lines of `SKILL.md` and one always-on line. It was not tested separately.
- **v0.5:**
  - The form guidance moves from `forms.md` into `SKILL.md`, which grows from 489 to 833 words, and `forms.md` is retired.
  - The end-of-task summary gets a fixed five-part order.
  - Emails open with the answer, not a stock thank-you, and declines get their own note.
  - Only Opus was rerun.

## Results by task

A task is a win when the skill's version was preferred in more of its three samples than the baseline's.

| Task | Opus v0.3 | Opus v0.4 | Opus v0.4.1 | Opus v0.5 | Sonnet v0.4 | Haiku v0.4 |
|---|---|---|---|---|---|---|
| quick-question | win | win | win | win | loss | win |
| session-summary | loss | tie | loss | win | win | loss |
| mid-session-answer | tie | loss | win | tie | loss | win |
| pr-description | win | win | win | win | tie | win |
| email-reply | win | win | win | win | win | tie |
| email-decline | win | **loss** | **loss** | tie | tie | **loss** |
| explain-concept | win | win | win | win | win | win |
| status-update | win | win | win | win | loss | win |
| announce-change | win | win | win | win | win | win |
| article-from-source | win | tie | loss | tie | loss | tie |

The decline email lost on Opus (v0.4 and v0.4.1) and on Haiku, after winning on Opus in v0.1 and v0.3 (v0.2 tied). The mid-session answer lost on Opus v0.4 and Sonnet, then won on Opus v0.4.1 after the "answer first" fix. The end-of-session summary and the article lost on Opus v0.4.1. In v0.5 the summary won, and the decline email and the article tied; no task lost. Only the explanation and the announcement won in every column above.

## Against the pass bar set before testing

| Condition | v0.3 | v0.4 | v0.4.1 | v0.5 |
|---|---|---|---|---|
| Opus wins at least 8 of 10 tasks | ✅ 8–1–1 | ❌ 6–2–2 | ❌ 7–3–0 | ❌ 7–0–3 |
| Sonnet wins at least as many tasks as it loses | ❌ 4–5–1 | ✅ 4–4–2 | not rerun | not rerun |
| Haiku wins at least as many tasks as it loses | ✅ 7–3–0 | ✅ 6–2–2 | not rerun | not rerun |
| Owner's blind picks match the judges on at least 8 of 10 pairs | ❌ 4 of 6 picked pairs | not re-read | not re-read | not re-read |

**No version meets every condition.** With three samples per task, one sample can flip a task's verdict. The Opus pair results for v0.3, v0.4 and v0.4.1 (19, 17 and 19 better pairs) are within that noise. v0.5's result (21 to 4, p=0.001) is the strongest of any Opus round, and the first with no task lost.

v0.4 replaced v0.3 because it lost less on Sonnet, and because its two new rules, no invented checks and no mention of the skill, fix real faults. v0.4.1 then fixed the conflicts the final review found. v0.5 ships.

## The owner's blind reads

- **Round 1:** the owner preferred the skill's writing in 7 of 10 pairs. Where they liked one reply's writing and the other's formatting, they preferred the baseline's formatting every time. That finding drove v0.2.
- **Round 3:** skill 4, baseline 2, unsure 2, out of the 8 pairs read. The end-of-session summary was one of the two "unsure" pairs.

## Does the skill load when it should?

The always-on lines cover chat answers, and the skill loads for drafting. Across round 4's drafting tasks, it loaded in:

| Model | Loaded |
|---|---|
| Opus | 24 of 24 |
| Sonnet | 22 of 24 |
| Haiku | 20 of 24 |

Five of the six misses were on the end-of-session summary. That fails the plan's own loading check, which asks for at least 2 of 3 samples on every drafting task. Haiku loaded the skill for the summary in 0 of 3 samples, and Sonnet in 1 of 3, so Haiku's summary loss happened without the skill loaded at all. In rounds 5 and 6 (Opus, v0.4.1 and v0.5), it loaded on all 24 drafting samples each time.

## AI detection (Pangram)

Six texts from round 3 were scanned by hand with Pangram's free checker: three tasks, each with and without the skill. All six scored 100% AI (`evals/pangram/round3-opus.md`). The word counts there are Pangram's own, which include formatting marks. Pangram detects who wrote a text, not how well it reads.

## Before and after (Opus, v0.4.1)

**Team announcement.** Without the skill: 260 words, with a date it calculated itself, a 🙏, and a procedure for admin overrides that nobody asked for. With the skill: 150 words that open with what changes, give the reason in two sentences, and end with what to do in an emergency. Two notes follow the draft, and one of them flags the draft's last sentence as an addition.

**Reply email.** Without the skill: 207 words. It opens with "Here's a draft:", thanks the colleague, offers a fallback slot the user never mentioned, and ends with a paragraph explaining the draft. With the skill, the replies are 78 to 162 words. Two have no note after the draft. The third ends with one that flags its added reason. But all three open with "Thanks for getting in touch", and all three give a reason for wanting the longer slot that the user never stated. The baseline invented one too ("go through the examples properly instead of rushing them").

## Known gaps

- **Invented reasons in emails.** All three v0.4.1 replies to the speaker invitation add a reason the user never gave, and only one flags it. In v0.5, two of three open with a plain yes and add no reason. The third still opens "Thanks for getting in touch" and gives a reason the user never stated.
- **Uneven forms.** On Opus v0.5 the decline email and the article only tie the baseline. On Sonnet and Haiku (v0.4) the summary fails the loading check.
- **Summaries still use some unexplained names.** v0.5 summaries lead with the outcome and group the changes, but still mention things like `freezegun` and `#328` without saying what they are.
- **Stock openers survive.** "Heads up:" no longer opens the Opus announcements, but all three invitation replies open "Thanks for getting in touch".
- **Sonnet** doesn't measurably benefit.
- **`principles.md` goes unread.** Its sources and examples are mostly for human readers now; the working guidance is in `SKILL.md`.
- **Sonnet and Haiku haven't been rerun since v0.4.**
- **Small samples.** Three samples per task, ten tasks, and an owner read of 18 pairs in total.
