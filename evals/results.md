# Results

wordcraft was built and tested on 24 and 25 October 2026 with Claude Code 2.1.283. This page says what the tests found, including where the skill falls short. The raw outputs and judge logs (about 400 files) are kept out of the repo to keep it small. `evals/run.py` and `evals/judge.py` regenerate them.

## The short version

**v0.9 is the current version: as good as v0.8, with shorter replies and fewer misplaced notes.** On a fourth fresh set (Opus), judges split v0.9 against v0.8 exactly evenly (11 pairs each, 8 ties). v0.9's replies used 95% of plain Claude's words against v0.8's 104%, and it put a "Check before sending" under 1 of 8 personal messages against v0.8's 4. It has been tested on one set, on Opus only.

**v0.8 beats plain Claude on writing tasks it was never tuned on, on all three models.** Across four runs on fresh tasks (sets 2 and 3), blind judges preferred v0.8 in 72 pairs and plain Claude in 27, with 21 ties (73%, p<0.0001). On set 3 alone: Opus 18 to 6, Sonnet 18 to 8, Haiku 19 to 6. What made the difference: v0.8 checks the source material for problems the reader would want caught, such as a deadline that has already passed, a miscounted number of years or an assumed date, and lists them after the draft. On Opus its replies are slightly shorter than plain Claude's; on Sonnet and Haiku they run about a quarter longer, because of the checks.

Earlier versions didn't carry over. v0.5 matched plain Claude on both fresh sets (12 to 11, and 12 to 12) while writing about a fifth shorter. Its big lead on the ten tasks it was developed on (21 to 4) came largely from tuning on them.

The bar set before testing (on the original ten tasks) was **not** met in full; the fresh-task results above are the stronger evidence.

Two more limits:

- **Reference files go unread.** After the test setup stopped blocking them (v0.4.1), Claude opened `principles.md` or `forms.md` in only 1 of 30 replies. v0.5 therefore moved the form guidance into `SKILL.md` and retired `forms.md`.
- **Small samples.** Each run is 30 pairs: 10 tasks × 3 samples on the original set, 15 tasks × 2 samples on the held-out set. Repeating a round with identical guidance for a task can flip that task's verdict.

The skill does not make Claude's writing look human to an AI detector, and wasn't designed to.

## The held-out tests

### Set 1: what didn't carry over

Fifteen new tasks were written by an agent that never saw the skill (`evals/heldout/`): everyday emails and messages, a 2,100-word report to summarize for a busy councillor, a 1,600-word short story to summarize for a book club, a true story to write for a newsletter from rough notes, printed phone instructions for a 74-year-old, a quick cooking question, and two technical hand-offs. Each ran twice on Opus: plain, with v0.5, and with v0.7.

| Version | Skill better | Baseline better | Tie | Skill's share | Words vs baseline |
|---|---|---|---|---|---|
| v0.5 | 12 | 11 | 7 | 52% | 79% |
| v0.7 | 12 | 13 | 5 | 48% | 84% |

Both versions won 5 tasks, lost 5 and tied 5. The judges' reasons explain the losses:

- **Catching problems in the material.** Plain Claude more often noticed something wrong in the source and listed it in a short check before sending: a date that falls on the wrong weekday, a policy memo that contradicts itself, a start date still in the future. The skill's rule against notes about the draft suppresses some of these useful checks.
- **One step further for the reader.** For the book club, plain Claude gave a spoiler-free blurb plus a private note on the ending. For the proposal feedback, it separated the three fixes that mattered before the deadline from the smaller points.

v0.5 won the customer reply, the mentor's card, the LinkedIn post, the report summary and the quick question.

### Set 2: v0.8

v0.8 was built from what set 1 taught: keep the ban on notes about your own choices, but check the material and list real problems under a short "Check before sending". A second agent then wrote 15 more tasks without seeing the skill or set 1 (`evals/heldout2/`). These included a deposit dispute, a job application, a nursing reference, an outage report for a non-technical board, a 2,200-word board paper to summarize before a vote, a memoir chapter to summarize for a book group, a newspaper profile from interview notes, and a council letter rewritten for a worried 79-year-old. Each ran twice on Opus with each version's own always-on lines.

| Version | Skill better | Baseline better | Tie | Skill's share | Tasks W–L–T | Words vs baseline |
|---|---|---|---|---|---|---|
| v0.5.1 | 12 | 12 | 6 | 50% | 6–5–4 | 83% |
| **v0.8** | **17** | 7 | 6 | **71%** (p=0.06) | 8–2–5 | 95% |

v0.8 added a check before sending to 25 of its 30 replies. Three examples of what it caught: the deposit reply noted that the agent's deadline had already passed, the job application noted that the applicant's own notes miscounted their years in post, and the leaving announcement noted that the month was assumed and that the 30th is a Monday. It lost the repair-café appeal and the quick credit-card question.

### Set 3: confirming v0.8 on three models

A third agent wrote 15 more tasks without seeing the skill or the earlier sets (`evals/heldout3/`). They included a condolence message, a salary negotiation, a retirement speech, a reply to an upset sister, a group trip email, feedback on a 19-year-old's cover letter, a 2,200-word house survey to summarize before a call with the estate agent, a short story for a head of English choosing set texts, a letter to a local paper, an FAQ page and a podcast write-up. Plain Claude and v0.8 ran twice on each, on each model.

| Model | Skill better | Baseline better | Tie | Skill's share | Tasks W–L–T | p | Words vs baseline |
|---|---|---|---|---|---|---|---|
| Opus | 18 | 6 | 6 | 75% | 8–1–6 | 0.02 | 92% |
| Sonnet | 18 | 8 | 4 | 69% | 8–2–5 | 0.08 | 128% |
| Haiku | 19 | 6 | 5 | 76% | 9–2–4 | 0.02 | 123% |

Every model lost the story summary for the head of English. None of those replies had a check list. Plain Claude added practical help the teacher would want, such as links to exam questions, a warning that reluctant readers may find the story slow, and a reminder about copying permission. Haiku also lost the condolence message, and v0.8 added a "Check before sending" list under the condolence note in 5 of its 6 replies across models, which is out of place in a sympathy message.

### Set 4: v0.9 against v0.8

v0.9 made two changes, both from set 3's gaps. The check list appears only when something needs the user's attention, at one line per item and one line at most in a personal message. And Claude thinks about what the reader will do next, adding the one or two practical things they'd want. A fourth agent wrote 15 more tasks without seeing the skill or the earlier sets (`evals/heldout4/`), weighted toward personal messages (a funeral tribute, a message to a friend with a cancer diagnosis, a card for a newly qualified nurse, a reply to a one-star review) and summaries for readers who must decide something. Opus only.

| Comparison | First better | Second better | Tie | Share |
|---|---|---|---|---|
| v0.9 vs v0.8 | 11 | 11 | 8 | 50% |
| v0.9 vs plain | 13 | 10 | 7 | 57% |
| v0.8 vs plain | 11 | 7 | 12 | 61% |

v0.9 won the decision summaries (an IT supplier proposal, a heat-pump study), where it tied findings to the reader's own situation. v0.8 won the house-sitter notes, the self-review, the resignation letter and the funeral words. Both versions beat plain Claude by less here than on sets 2 and 3, likely because personal messages are where plain Claude already writes well.

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

Rounds 1 to 8 on the original tasks tested v0.1, v0.2, v0.3, v0.4, v0.4.1, v0.5, v0.6 and v0.7. Round 1 also ran a third version that forced the skill on. The judges preferred it in 10 pairs and the baseline in 14, with 6 ties, so it was dropped.

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
| Opus | v0.6 | 18 | 6 | 6 | 75% | 0.02 |
| Opus | v0.7 | 18 | 6 | 6 | 75% | 0.02 |
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
- **v0.6** (not shipped): rule 1 became "bottom line up front" (BLUF), the summary followed SBAR, and a new form covered raising a problem. Openings oversimplified and articles stopped explaining terms.
- **v0.7** (not shipped): v0.5 plus SBAR's "assessment" and "recommendation" parts in the summary. No measured gain.
- **v0.5.1:** v0.5's skill text, with BLUF and SBAR credited in `principles.md` as the practices its summary order draws on.
- **v0.8:** Claude checks the source for problems the reader would want caught and lists them, with any guess or outside fact, under "Check before sending". Notes about its own choices stay banned. The always-on lines change to match. Tested on held-out sets 2 and 3, on Opus, Sonnet and Haiku.
- **v0.9** (shipped): the check list appears only when something needs attention (one line each, one line at most in personal messages), and Claude adds the one or two practical things the reader will want next. Equal to v0.8 on set 4, with shorter replies. Opus only.
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

v0.4 replaced v0.3 because it lost less on Sonnet, and because its two new rules, no invented checks and no mention of the skill, fix real faults. v0.4.1 then fixed the conflicts the final review found. v0.5 was the best on these tasks, and v0.6 and v0.7 did not beat it. Its text shipped as v0.5.1, and v0.8 replaced it after the second held-out test.

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

Six texts from round 3 were scanned by hand with Pangram's free checker: three tasks, each with and without the skill. All six scored 100% AI, with and without the skill:

| Task | With the skill | Without the skill |
|---|---|---|
| Announcement | 100% AI | 100% AI |
| Reply email | 100% AI | 100% AI |
| Decline email | 100% AI | 100% AI |

The scans used Pangram's free web checker (model "Pangram 4.1"), whose free tier covered six texts. Pangram detects who wrote a text, not how well it reads.

## Before and after (Opus, v0.4.1)

**Team announcement.** Without the skill: 260 words, with a date it calculated itself, a 🙏, and a procedure for admin overrides that nobody asked for. With the skill: 150 words that open with what changes, give the reason in two sentences, and end with what to do in an emergency. Two notes follow the draft, and one of them flags the draft's last sentence as an addition.

**Reply email.** Without the skill: 207 words. It opens with "Here's a draft:", thanks the colleague, offers a fallback slot the user never mentioned, and ends with a paragraph explaining the draft. With the skill, the replies are 78 to 162 words. Two have no note after the draft. The third ends with one that flags its added reason. But all three open with "Thanks for getting in touch", and all three give a reason for wanting the longer slot that the user never stated. The baseline invented one too ("go through the examples properly instead of rushing them").

## Known gaps

- **v0.9 is only tested on Opus, on one set.** Its fixes for misplaced check lists and missing practical extras worked mechanically, but didn't raise the judges' preference over v0.8.
- **Longer on Sonnet and Haiku (v0.8).** Their checks made replies about a quarter longer than plain Claude's; v0.9's conditional checks may help, but that hasn't been measured.
- **Invented reasons in emails.** All three v0.4.1 replies to the speaker invitation add a reason the user never gave, and only one flags it. In v0.5, two of three open with a plain yes and add no reason. The third still opens "Thanks for getting in touch" and gives a reason the user never stated.
- **Uneven forms.** On Opus v0.5 the decline email and the article only tie the baseline. On Sonnet and Haiku (v0.4) the summary fails the loading check.
- **Summaries still use some unexplained names.** v0.5 summaries lead with the outcome and group the changes, but still mention things like `freezegun` and `#328` without saying what they are.
- **Stock openers survive.** "Heads up:" no longer opens the Opus announcements, but all three invitation replies open "Thanks for getting in touch".
- **Sonnet** doesn't measurably benefit.
- **`principles.md` goes unread.** Its sources and examples are mostly for human readers now; the working guidance is in `SKILL.md`.
- **Sonnet and Haiku haven't been rerun since v0.4.**
- **Small samples.** Three samples per task, ten tasks, and an owner read of 18 pairs in total.
