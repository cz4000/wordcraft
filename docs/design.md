# wordcraft: design

A skill that makes Claude write well. Status: draft for the owner's approval. Date: 2026-10-24.

## Why

Claude's writing works, but it is not good. Answers run long and bury the point. It uses bullets where a paragraph would read better, and the reverse. The tone is stiff. It repeats the question back. In long coding sessions it talks in its own private vocabulary: function names, flags and labels it invented an hour ago, used as if the user had been reading along. The summary says what changed in the code, but not what that means for the person reading it.

The owner wants writing that is clear, warm and pleasant to read, and never a wall of text. The quality bar is a piece Tim O'Reilly published on 2026-10-23, written by Claude and lightly edited by him: <https://oreillyradar.substack.com/p/owners-not-renters-raffi-krikorian>. It is an example of the quality, not a template for length or structure.

## Goals

- Claude's everyday chat answers read better, especially in long coding sessions.
- Emails, posts, PR descriptions and other prose Claude drafts read better.
- A reader who was not inside Claude's head can follow every answer.
- The improvement is measured against Claude without the skill, not assumed.

## Non-goals

- A fixed length or a fixed template for any kind of output.
- Fiction, poetry or marketing copy.
- Rewriting the owner's own text unless asked.

## Anti-goals (a failure even if the skill technically works)

- Another list of banned words. It makes text less bad, not good, and superpowers' own tests found ban lists make shape problems worse.
- Answers that get shorter by dropping what the reader needs.
- A cute, mannered voice that is "creative" instead of clear.
- Copying the book. The skill restates principles in its own words.

## Who reads Claude's writing

1. The owner, in chat, often hours into a coding session, often skimming.
2. People who receive an email or message Claude drafted.
3. Readers of longer pieces: posts, reports, documentation.

## The principles and where they come from

The source is William Zinsser's *On Writing Well* (25th anniversary edition, 2001). The builder reads the owner's local copy; the book never goes in the repo. The skill credits the book and restates its ideas in our own words, with at most a few short quotes. The builder reads these chapters and turns each into a principle with one before-and-after pair:

| Part | Chapters | What the skill takes from it |
|---|---|---|
| Principles | 1–7: Transaction, Simplicity, Clutter, Style, Audience, Words, Usage | A person writing to a person. Know what you want to say before writing. Cut every word that does no work. Plain words. Be yourself; craft is never an excuse to lose the reader. |
| Methods | 8–10: Unity, The Lead and the Ending, Bits & Pieces | One voice, one tense, one point per piece. Open with what matters. Stop when you are done. |
| Forms | 15: Science and Technology; 16: Business Writing | "The reader knows nothing": start from the one fact they need, then widen to why it matters. Plain, human business writing, which covers email. |
| Attitudes | 20–24 | Sound like a person. Rewriting is the work. |

**One rule the owner added (2026-10-24):** describe a thing in plain words first, then put its technical name in brackets for readers who want to find it in the code. Example:

> **Before:** Fixed the `flush_on_exit` path so `CACHE_WARM` no longer races the session loader.
>
> **After:** After a restart, the app sometimes showed an empty inbox for a few seconds (`flush_on_exit`). Two parts of the startup ran in the wrong order (`CACHE_WARM` and the session loader). That's fixed, and a test now checks the order.

## Shape of the skill

The method combines Anthropic's skill-authoring guide, Anthropic's `skill-creator` and superpowers' `writing-skills`.

- **Name:** `wordcraft` (owner's choice, 2026-10-24). Names may not contain "claude" or "anthropic".
- **`SKILL.md`:** a short positive recipe for what good writing is, under 500 words, plus a final check: reread the draft as the reader. Detail lives in reference files linked directly from `SKILL.md`, one level deep.
- **Reference files:** the principles with their before-and-after pairs, plus short notes for each form: chat answer, end-of-task summary, email, longer piece. The builder decides the exact split.
- **Description:** says both what the skill does and when to use it, as Anthropic advises, but never summarizes the steps. Superpowers found that a step summary lets Claude skip the body.
- **Always-on piece:** a skill only loads when a task looks like a writing task, so on its own it won't change everyday chat answers. A few lines in the owner's global `~/.claude/CLAUDE.md` state the core rules and point to the skill. *(My call: CLAUDE.md rather than an output style, because CLAUDE.md applies everywhere the owner works.)*
- **Existing skills:** `humanizer` and `unslop` stay installed and untouched. This skill does not depend on them.

## How we prove it works

This follows Anthropic's "evaluations first" and superpowers' "no skill without a failing test first".

1. **Task set:** about ten real prompts across the forms. At least one is an end-of-session summary from a real long Claude Code session on a public open-source project, so no private material is involved. *(My call.)* At least one is a one-line question, to catch the skill making short answers longer. Others: an email reply, a hard email to say no, explaining a concept, a status update, a PR description, and turning a public talk or interview transcript into a short article. The O'Reilly piece's source notes aren't available, so it serves as a quality bar, not an answer key. *(My call.)*
2. **Environment:** every run happens in a clean setup with none of the owner's other writing rules: no personal CLAUDE.md, no superpowers hook, no humanizer, unslop or poteto-mode. The "with the skill" arm is the real shipped setup: the always-on lines plus the skill installed and left to trigger on its own. A separate check confirms that it actually triggers on the writing tasks. A third arm, the skill forced on, shows how much the skill itself contributes. *(My call: the skill has to work for anyone who installs it, so the owner's rules must not flatter or mask the result.)*
3. **Baseline:** run each task without the skill and save the outputs. Confirm that the failures in "Why" actually show up. Any failure that doesn't show up gets no guidance.
4. **With the skill:** run the same tasks with the skill loaded.
5. **Blind judging:** reviewer agents running on Opus see the two versions in random order, unlabelled, and pick the one a reader would rather get, with a reason. The owner also reads a blind sample to check that the judges' taste matches theirs. *(My call. The owner has not chosen between judging alone and judging alongside agents.)*
6. **Models:** test on Opus, Sonnet and Haiku, as Anthropic advises.
7. **Wording:** micro-test any rule that does not land: 5+ samples per wording, always with a no-skill control.
8. **Pass:** the skill wins at least 8 of 10 tasks on Opus, does not lose on Sonnet or Haiku, and the owner's blind picks agree with the judges. *(My call on the threshold.)*

**Second measure (owner request, 2026-10-24):** every output of at least 75 words is scanned with the Pangram AI-text detector, and the mean score per arm is reported. A clear drop from `baseline` to the skill corroborates the judges. It is not a pass condition, because it measures how AI-like text looks, not how well it reads.

Our own runner (`evals/run.py`) does the running, because `skill-creator`'s runner works inside the user's own setup and can't give a clean baseline. Our own two-order blind judge (`evals/judge.py`) does the judging.

## Where it lives

- A new **public, open-source** repository on the owner's personal GitHub account (owner's decision, 2026-10-24). Nothing from the owner's day job goes in it: no transcripts, names, examples or test data.
- MIT license. *(My call.)*
- The owner creates the repo or signs `gh` in to that account. Claude can't sign in for them.
- Installed by linking the repo's skill folder into `~/.claude/skills/wordcraft`, so edits in the repo take effect immediately.
- This design document becomes the repo's first commit.

## Left to the builder

- Wording of every principle and every before-and-after pair.
- The exact split of reference files.
- The exact text of the task prompts, provided they cover the forms above.
- The exact always-on lines, kept under about 10.
