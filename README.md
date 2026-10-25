# wordcraft

A skill for Claude that makes its writing clearer and easier to read. It covers emails, status updates, announcements, pull request descriptions, articles, and the summaries Claude writes at the end of a long coding session.

Claude already writes plainly and gets to the point. Its problems are elsewhere:

- It answers a one-line question with a reference page.
- It formats a chat reply like a report.
- It uses names you've never seen, like a function or a test package from an hour ago, as if you'd been reading along.
- It reaches for stock phrases and adds notes about its own draft.
- Now and then it invents a detail.

wordcraft teaches it to write for a smart reader who hasn't been briefed.

## What it changes

Before, a reply to a speaker invitation (207 words, abridged):

> Here's a draft: … Thanks for getting in touch, and please thank your colleague for passing my name on. … If both have gone, I'm happy to do the 30-minute version on day one. … Thanks again for the invitation. I'm looking forward to it. … The 45-minute slots are on day two (15 May), so the draft says that. I've added that you'd still do the 30-minute slot…

After (75 words):

> Hi Dana, Thanks for asking. I'd be glad to speak at Riverside DevConf. If one of the 45-minute slots on 15 May is still free, I'd prefer that. The extra time would let me cover the material properly. I can't get a title and abstract to you by 20 February, though. Would 27 February work, or is that too late for publishing the schedule?

It isn't perfect. "The extra time would let me cover the material properly" is a reason the user never gave, which is exactly what the skill tells Claude not to do.

## Install

wordcraft has two parts: the skill, which Claude loads when it's drafting something, and a few always-on lines that shape every chat reply.

**1. The skill.** In Claude Code:

```bash
git clone https://github.com/cz4000/wordcraft.git ~/code/wordcraft
```

```bash
ln -s ~/code/wordcraft/skills/wordcraft ~/.claude/skills/wordcraft
```

To try it for one session without installing, run `claude --plugin-dir ~/code/wordcraft` instead.

**2. The always-on lines.** Copy the contents of [always-on.md](always-on.md) into your `~/.claude/CLAUDE.md`. It's a heading and nine short rules. Without them, the skill only loads for drafting tasks and won't change everyday chat answers.

## Does it work?

It was tested on ten real writing tasks, three samples each, with and without the skill. Blind Opus judges compared every pair in both orders. The full method and every number are in [evals/results.md](evals/results.md).

| Model | Judges preferred the skill | Preferred no skill | Ties |
|---|---|---|---|
| Opus | 17 | 7 | 6 |
| Haiku | 18 | 7 | 5 |
| Sonnet | 12 | 11 | 7 |

On Opus and Haiku the judges preferred the skill in about seven of ten decided pairs. On Sonnet it made no measurable difference. The pass bar set before testing was not met in full.

Treat the numbers with some care, for three reasons:

- **Tuning and scoring used the same tasks.** The skill was adjusted on the same ten tasks it was scored on.
- **The skill's two reference files couldn't be read** during the test runs.
- **Some forms are still weak:** decline emails, mid-session answers and end-of-session summaries.

It does not make writing pass an AI detector, which isn't what it's for.

## Where the ideas come from

The principles are restated in the skill's own words, with credit:

- William Zinsser, *On Writing Well* (25th anniversary edition, 2001). The core: cut clutter, write for the reader, start with the one fact they need, and when you're ready to stop, stop.
- George Orwell's six rules, from "Politics and the English Language" (1946).
- Charlie Euchner, ["Ten Essential Rules for Writing Well"](https://theelementsofwriting.com/ten-essential-rules-for-writing-well/) (*The Elements of Writing*, 2018).
- One convention from the project's owner: describe a thing in plain words first, then give its technical name in brackets.

The project was prompted by Tim O'Reilly's experiment in [teaching Claude to write like a human](https://oreillyradar.substack.com/p/owners-not-renters-raffi-krikorian).

## Run the tests

```bash
uv run --with pytest pytest
```

The live evaluations call Claude and cost usage, so each command has a `--dry-run` that prints the call count first:

```bash
python evals/run.py run --arms baseline real --models opus --reps 3 --out evals/runs/mine --dry-run
```

```bash
python evals/judge.py --runs evals/runs/mine --model opus --a real --b baseline --dry-run
```

`python evals/check_quotes.py <your copy of On Writing Well>.pdf` checks that the skill quotes the book only in its three credited lines.

## License

MIT
