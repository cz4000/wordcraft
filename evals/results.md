# Results

wordcraft was built and tested between 24 and 25 October 2026 with Claude Code 2.1.283. This page says what the tests found, including where the skill falls short.

## The short version

With wordcraft installed, Opus and Haiku write measurably better replies, emails, updates and announcements. Blind judges preferred the skill's version in about three out of four decided pairs. On Sonnet the skill is neutral. End-of-session summaries improved but are still the weakest form. The skill does not make Claude's writing look human to an AI detector, and wasn't designed to.

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
| Opus | **v0.4** | 17 | 7 | 6 | 71% | 0.06 |
| Sonnet | v0.3 | 11 | 14 | 5 | 44% | 0.69 |
| Sonnet | **v0.4** | 12 | 11 | 7 | 52% | 1.0 |
| Haiku | v0.3 | 18 | 9 | 3 | 67% | 0.12 |
| Haiku | **v0.4** | 18 | 7 | 5 | 72% | 0.04 |

What changed between versions:

- **v0.2:** said what each change is for and why it matters. Matched the shape to the content (lists and headed groups for separate items, paragraphs for reasoning). Kept every fact the reader needs. Added Orwell's six rules.
- **v0.3:** never invent a specific to sound personal. Flag outside facts. Added Euchner's ten rules.
- **v0.4:** never claim a check, fix or release the work doesn't show. Never mention the skill in a reply.

## Against the pass bar set before testing

| Condition | v0.3 | v0.4 |
|---|---|---|
| Opus wins at least 8 of 10 tasks | ✅ 8–1–1 | ❌ 6–2–2 |
| Sonnet wins at least as many tasks as it loses | ❌ 4–5–1 | ✅ 4–4–2 |
| Haiku wins at least as many tasks as it loses | ✅ 7–3 | ✅ 6–2–2 |
| Owner's blind picks match the judges on at least 8 of 10 pairs | ❌ 4 of 6 picked pairs | not re-read |

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

Most misses were on the end-of-session summary.

## AI detection (Pangram)

Six texts from round 3 were scanned by hand with Pangram's free checker: three tasks, each with and without the skill. All six scored 100% AI (`evals/pangram/round3-opus.md`). Pangram detects who wrote a text, not how well it reads.

## Before and after (Opus, round 4)

**Reply email.** Without the skill: 207 words, opening with "Here's a draft:", thanking the colleague, offering a fallback slot the user never mentioned, and ending with a paragraph explaining the draft. With the skill: 75 words.

> Hi Dana, Thanks for asking. I'd be glad to speak at Riverside DevConf. If one of the 45-minute slots on 15 May is still free, I'd prefer that. … I can't get a title and abstract to you by 20 February, though. Would 27 February work, or is that too late for publishing the schedule?

**Quick git question.** Without the skill: 323 words, two headings, two diagrams and a four-row table. With the skill: 240 words that keep the two diagrams the readers valued and drop the reference-page scaffolding.

**Team announcement.** Without the skill: 260 words, with a date it calculated itself, a 🙏, and a rule for admin overrides that nobody asked for. With the skill: 159 words that open with what changes and why, and one line flagging the missing detail: who to contact for an emergency override.

## Known gaps

- **End-of-session summaries** are the weakest form: a tie on Opus in round 4, and they lost in rounds 1 to 3.
- **Stock openers survive.** "Heads up:" still opens most announcements.
- **Emails sometimes still add a reason the user didn't give.** v0.3 and v0.4 now flag it rather than state it as fact.
- **Sonnet** doesn't measurably benefit.
- **Small samples.** Three samples per task, and an owner read of 18 pairs in total.
