# wordcraft

A skill for Claude that makes its writing clearer and easier to read. It covers emails, status updates, announcements, pull request descriptions, articles, and the summaries Claude writes at the end of a long coding session.

Claude already writes plainly and leads with the answer. Its problems are elsewhere:

- It answers a one-line question with a reference page.
- It formats a chat reply like a report.
- It uses names you've never seen, like a function or a test package from an hour ago, as if you'd been reading along.
- It reaches for stock phrases and adds notes about its own draft.
- Now and then it invents a detail.

wordcraft teaches it to write for a smart reader who hasn't been briefed.

## What it changes

The request: *"Write a message for our #engineering channel: starting Monday, the main branch is protected. Every PR needs one approving review and green CI before it can merge, and nobody can push straight to main anymore, including leads. This is because last Thursday someone pushed a hotfix straight to main and it broke checkout for two hours. Admins can still override in a real emergency."*

Without the skill (260 words, abridged), Claude opened with "**Heads up: `main` becomes a protected branch on Monday (Oct 26)**". It went on to bold nearly every line, invent a procedure for admin overrides that nobody asked for, and sign off "Questions or concerns? Reply in the thread. 🙏".

With the skill (150 words, v0.4.1):

> **Starting Monday, `main` is protected.** You'll need to open a PR for every change, including hotfixes.
>
> To merge, a PR needs:
> - **one approving review**
> - **green CI**
>
> Nobody can push straight to `main` anymore, leads included.
>
> Here's why. Last Thursday a hotfix was pushed straight to `main` and broke checkout for two hours. A review and a CI run would very likely have caught it before it shipped.
>
> In a real emergency, admins can still override the protection. For anything urgent that isn't an emergency, open the PR and ask in this channel for a quick review.

It isn't perfect. It still adds two notes after the draft, though one of them does flag that the last sentence was its own addition. Replies to emails are weaker: all three test replies to a speaker invitation opened "Thanks for getting in touch", and gave a reason the user never stated.

## Install

wordcraft has two parts: the skill, which Claude loads when it's drafting something, and a few always-on lines that shape every chat reply.

**1. The skill.** Install it for every project with the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add cz4000/wordcraft -a claude-code -g
```

Leave out `-g` to install it for the current project only.

If you'd rather install by hand, clone the repo and link the skill folder:

```bash
git clone https://github.com/cz4000/wordcraft.git ~/code/wordcraft
```

```bash
mkdir -p ~/.claude/skills && ln -s ~/code/wordcraft/skills/wordcraft ~/.claude/skills/wordcraft
```

If you've cloned the repo, you can try the skill for one session with `claude --plugin-dir ~/code/wordcraft`. That loads the skill but not the always-on lines.

**2. The always-on lines.** Copy the contents of [always-on.md](always-on.md) into your `~/.claude/CLAUDE.md`. It's a heading, one framing line and seven rules. Without them, the skill loads only for drafting and won't change everyday chat answers.

## Does it work?

It was tested on ten everyday writing tasks, three samples each, with and without the skill. Blind Opus judges compared every pair in both orders. Opus figures are for v0.4.1, and Sonnet and Haiku figures for v0.4. The full method and every number are in [evals/results.md](evals/results.md), and the raw outputs and judge logs are in `evals/runs/`.

| Model | Pairs where judges preferred the skill (of 30) | Preferred no skill | Ties |
|---|---|---|---|
| Opus | 19 | 7 | 4 |
| Haiku | 18 | 7 | 5 |
| Sonnet | 12 | 11 | 7 |

On Opus and Haiku the judges preferred the skill in about seven of ten decided pairs. On Sonnet it made no measurable difference. The bar set before testing (win 8 of 10 tasks on Opus, and break even on Sonnet and Haiku) was not met in full: v0.4.1 won 7 of 10 on Opus.

Treat the numbers with some care, for four reasons:

- **Tuning and scoring used the same tasks.** The skill was adjusted on the same ten tasks it was scored on.
- **The skill's two reference files are rarely used.** Claude opened them in 1 of 30 replies, so `SKILL.md` and the always-on lines do almost all the work.
- **Some forms are still weak:** decline emails, end-of-session summaries, and articles written from a transcript.
- **The current version is untested.** v0.4.2 is v0.4.1 plus wording fixes from a final edit, and it hasn't been measured separately.

It does not make writing pass an AI detector, which isn't what it's for.

## Where the ideas come from

The principles are restated in the skill's own words, with credit:

- William Zinsser, *On Writing Well* (25th anniversary edition, 2001). The core: cut clutter, write for the reader, start with the one fact they need, and when you're ready to stop, stop.
- George Orwell's six rules, from "Politics and the English Language" (1946).
- Charlie Euchner, ["Ten Essential Rules for Writing Well"](https://theelementsofwriting.com/ten-essential-rules-for-writing-well/) (*The Elements of Writing*, 2018).
- One convention of the project's own: describe a thing in plain words first, then give its technical name in brackets.

The quality bar was [a piece Tim O'Reilly published](https://oreillyradar.substack.com/p/owners-not-renters-raffi-krikorian) in October 2026, written by Claude and lightly edited by him.

## Run the tests

```bash
uv run --with pytest pytest
```

The live evaluations call Claude and count against your Claude usage, so each command has a `--dry-run` that prints the call count first:

```bash
python evals/run.py run --arms baseline real --models opus --reps 3 --out evals/runs/mine --dry-run
```

```bash
python evals/judge.py --runs evals/runs/mine --model opus --a real --b baseline --dry-run
```

`python evals/check_quotes.py <your copy of On Writing Well>.pdf` needs `pdftotext`. It checks that the skill copies no run of eight or more words from the book outside its three credited quotes.

## License

MIT
