# Results

wordcraft was built and tested between 24 and 25 October 2026 with Claude Code 2.1.283. This page says what the tests found, including where the skill falls short.

## The short version

With wordcraft, blind judges preferred Opus's and Haiku's writing in about seven of ten decided pairs. The gains were largest on announcements, explanations, status updates and pull request descriptions. On Sonnet the skill made no measurable difference. The bar set before testing was **not** met in full.

Three limits apply to every number here:

- **Tuned and scored on the same tasks.** Each version was adjusted after seeing results on the same ten tasks it was scored on, with no held-out tasks, so the gains may not carry over in full to new writing.
- **The reference files are rarely read.** In rounds 1 to 4 the test setup blocked `principles.md` and `forms.md`. After the fix (v0.4.1), Claude opened them in only 1 of 30 replies, so in practice the skill is `SKILL.md` plus the always-on lines.
- **Thirty pairs are ten tasks.** Each run's 30 pairs are 10 tasks × 3 samples, not 30 independent cases.

The skill does not make Claude's writing look human to an AI detector, and wasn't designed to.

## How it was tested

- **Ten real writing tasks** (`evals/tasks.json`): a quick chat question, an end-of-session summary, a mid-session question, a pull request description, two emails, an explanation for a non-technical manager, a status update, a team announcement and a short article. All source material is public: a real bug fix on the open-source `humanize` library and a Federal Reserve press conference transcript.
- **A clean setup.** Claude ran headless with none of the tester's own instructions, skills, plugins or MCP servers (`evals/run.py`). "With the skill" means the shipped setup: the always-on lines as `CLAUDE.md` plus the skill installed and left to load on its own.
- **Three samples per task**, with and without the skill.
- **Blind judges.** Opus saw each pair in both orders and picked the reply the requester would rather receive. A split decision counts as a tie. The judge prompt never mentions the skill (`evals/judge-prompt.md`).
- **The owner's own blind reads** of 10 pairs after round 1 and 8 pairs after round 3.

## What the baseline got wrong

From 30 Opus outputs without the skill (`evals/baseline-findings.md`): answers far longer than the question needed, chat formatted like a document, internal names the reader had never seen, stock phrases, notes about the draft after the draft, two invented details, and decorative emoji. It already led with the answer and wrote plainly, so the skill leaves those alone.

## Results by round

Pairs where the judges preferred one version in both orders, out of 30 per run. The p-value is a two-sided sign test on the decided pairs.

| Model | Version | Skill better | Baseline better | Tie | Skill's share | p |
|---|---|---|---|---|---|---|
| Opus | v0.1 | 15 | 11 | 4 | 58% | 0.56 |
| Opus | v0.2 | 16 | 8 | 6 | 67% | 0.15 |
| Opus | v0.3 | 19 | 5 | 6 | 79% | 0.007 |
| Opus | v0.4 | 17 | 7 | 6 | 71% | 0.06 |
| Opus | **v0.4.1** | 19 | 7 | 4 | 73% | 0.03 |
| Sonnet | v0.3 | 11 | 14 | 5 | 44% | 0.69 |
| Sonnet | v0.4 | 12 | 11 | 7 | 52% | 1.0 |
| Haiku | v0.3 | 18 | 9 | 3 | 67% | 0.12 |
| Haiku | v0.4 | 18 | 7 | 5 | 72% | 0.04 |

What changed between versions:

- **v0.2:** said what each change is for and why it matters. Matched the shape to the content (lists and headed groups for separate items, paragraphs for reasoning). Kept every fact the reader needs. Added Orwell's six rules.
- **v0.3:** never invent a specific to sound personal. Flag outside facts. Added Euchner's ten rules.
- **v0.4:** never claim a check, fix or release the work doesn't show. Never mention the skill in a reply.
- **v0.4.1:** after the final review. The always-on lines say "answer first", and the description no longer claims chat questions. The test setup now lets the skill read its reference files. Opus only.

## Results by task

A task is a win when the skill's version was preferred in more of its three samples than the baseline's.

| Task | Opus v0.3 | Opus v0.4 | Opus v0.4.1 | Sonnet v0.4 | Haiku v0.4 |
|---|---|---|---|---|---|
| quick-question | win | win | win | loss | win |
| session-summary | loss | tie | loss | win | loss |
| mid-session-answer | tie | loss | win | loss | win |
| pr-description | win | win | win | tie | win |
| email-reply | win | win | win | win | tie |
| email-decline | win | **loss** | loss | tie | **loss** |
| explain-concept | win | win | win | win | win |
| status-update | win | win | win | loss | win |
| announce-change | win | win | win | win | win |
| article-from-source | win | tie | loss | loss | tie |

The decline email lost on Opus (v0.4 and v0.4.1) and Haiku, after winning on Opus in v0.1 to v0.3. The mid-session answer lost on Opus v0.4 and Sonnet, and won on Opus v0.4.1 after the "answer first" fix. The end-of-session summary lost again on Opus v0.4.1. Only the explanation and the announcement won on every model.

## Against the pass bar set before testing

| Condition | v0.3 | v0.4 |
|---|---|---|
| Opus wins at least 8 of 10 tasks | ✅ 8–1–1 | ❌ 6–2–2 |
| Sonnet wins at least as many tasks as it loses | ❌ 4–5–1 | ✅ 4–4–2 |
| Haiku wins at least as many tasks as it loses | ✅ 7–3 | ✅ 6–2–2 |
| Owner's blind picks match the judges on at least 8 of 10 pairs | ❌ 4 of 6 picked pairs | not re-read |

Opus v0.4.1, the shipped version, went 7–3–0 by task: short of 8 wins, though its pair result (19 to 7, p=0.03) is the strongest of any Opus round.

**Neither version meets every condition.** With three samples per task, one sample can flip a task's verdict, and the Opus difference between v0.3 and v0.4 (19 against 17 better pairs) is within that noise. v0.4 ships because it is as good on Opus, better on Haiku, no longer worse on Sonnet, and its two new rules are right regardless of score.

## The owner's blind reads

- **Round 1:** the owner preferred the skill's writing in 7 of 10 pairs and the baseline's formatting in every pair where they split their pick. That finding drove v0.2.
- **Round 3:** skill 4, baseline 2, unsure 2. The end-of-session summary was one of the two "unsure" pairs.

## Does the skill load when it should?

The always-on lines cover chat answers, and the skill loads for drafting. Across round 4's drafting tasks, it loaded in:

| Model | Loaded |
|---|---|
| Opus | 24 of 24 |
| Sonnet | 22 of 24 |
| Haiku | 20 of 24 |

Five of the six misses were on the end-of-session summary. That fails the plan's own loading check, which asks for at least 2 of 3 samples on every drafting task. Haiku loaded the skill for the summary in 0 of 3 samples, and Sonnet in 1 of 3. So Haiku's summary loss happened without the skill loaded at all.

## AI detection (Pangram)

Six texts from round 3 were scanned by hand with Pangram's free checker: three tasks, each with and without the skill. All six scored 100% AI (`evals/pangram/round3-opus.md`; the word counts there are Pangram's own, which count formatting marks too). Pangram detects who wrote a text, not how well it reads.

## Before and after (Opus, round 4)

**Reply email.** Without the skill: 207 words, opening with "Here's a draft:", thanking the colleague, offering a fallback slot the user never mentioned, and ending with a paragraph explaining the draft. With the skill: 75 words.

> Hi Dana, Thanks for asking. I'd be glad to speak at Riverside DevConf. If one of the 45-minute slots on 15 May is still free, I'd prefer that. The extra time would let me cover the material properly. I can't get a title and abstract to you by 20 February, though. Would 27 February work, or is that too late for publishing the schedule?

The skill's version still breaks one of its own rules. "The extra time would let me cover the material properly" is a reason the user never gave.

**Quick git question.** Without the skill: 323 words, three headings, two diagrams and a four-row table. With the skill: 240 words that keep the two diagrams the readers valued and drop the reference-page scaffolding.

**Team announcement.** Without the skill: 260 words, with a date it calculated itself, a 🙏, and a rule for admin overrides that nobody asked for. With the skill: 159 words that open with what changes and why, and one line flagging the missing detail: who to contact for an emergency override.

## Known gaps

- **Invented reasons in emails.** All three Opus v0.4 replies to the speaker invitation add a reason the user never gave, and none flags it. The decline email adds invented details too, which may explain its losses.
- **Uneven forms.** The decline email, the mid-session answer and the end-of-session summary are the weakest. The summary also fails the loading check on Sonnet and Haiku.
- **Stock openers survive.** "Heads up:" still opens most announcements, and one reply opens "Thanks for getting in touch".
- **Sonnet** doesn't measurably benefit.
- **The reference files barely reach the model.** In 29 of 30 v0.4.1 replies, Claude worked from `SKILL.md` alone, so the summary structure and the status-update form in `forms.md` rarely apply. Moving the key form notes into `SKILL.md` is the obvious next step, and it would need its own test round.
- **Sonnet and Haiku weren't rerun on v0.4.1.**
- **Small samples.** Three samples per task, ten tasks, and an owner read of 18 pairs in total.
