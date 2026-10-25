# wordcraft

**A writing skill for Claude.** It makes Claude's emails, messages, summaries and reports clearer and easier to read, whether you're reading them yourself or building agents that write for other people.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

```bash
npx skills add cz4000/wordcraft -a claude-code -g
```

Then add the [always-on lines](always-on.md) to your `~/.claude/CLAUDE.md`. [More install options](#install).

## Why I built it

I use Claude Code every day, and I'd grown tired of reading what it wrote. Short questions got long answers. End-of-session summaries listed every function it had touched, with names I'd never seen and nothing about what any of it meant for me. Emails it drafted could have come from anyone. The information was usually there, but getting it out was work.

In October 2026, Tim O'Reilly published [a piece that Claude wrote and he only lightly edited](https://oreillyradar.substack.com/p/owners-not-renters-raffi-krikorian), and it read beautifully. So Claude *can* write well. In the comments, a reader suggested turning William Zinsser's *On Writing Well* into a skill. That's where wordcraft started.

## What's in it

wordcraft starts from Zinsser and adds what testing showed was still missing.

- **Zinsser's core.** Cut clutter, write for a reader who knows nothing of your work, start with the one fact they need, sound like a person, and stop when you're done.
- **Orwell's six rules.** The short word over the long one, the everyday word over jargon, and cut any word you can.
- **Euchner's ten rules.** One idea per paragraph, and a complex subject taken one piece at a time.
- **BLUF and SBAR.** End-of-task summaries lead with the outcome, then cover what changed, what you need to do, what couldn't be checked and what's left behind.
- **Plain words first.** A name you haven't seen comes after a plain description, in brackets (`like_this`).
- **Check before sending.** When the material has a problem you'd want caught, such as a wrong date, figures that don't add up or a missing detail, Claude lists it after the draft.
- **A note for each kind of writing.** Summaries, emails, status updates, chat answers and longer pieces each get their own guidance.

It's two files, plus a few lines for your `CLAUDE.md` so everyday chat answers follow the same rules.

## Before and after

Three real tests. In each one, blind judges read both replies, in both orders, and preferred the one written with wordcraft. "Before" is plain Claude.

### A message to a friend

Someone's old friend has just been diagnosed with breast cancer. They want to send her a message that doesn't sound like a sympathy card.

**Before** (471 words) opened with advice, then offered three draft messages and more tips:

> I'm sorry. That's a hard thing to hear about someone you love, even if you don't see her often. … **A few things that help:** …

**After** (246 words) led with one message:

> Ros, I've been thinking about you since last night. That's rubbish news and I'm so sorry. I won't make a fuss, I just want you to know I'm here, for a moan, a distraction, or something practical once chemo starts. No need to reply. x

### A card for a niece

An aunt wants to write in a card for her niece, who has just qualified as a nurse after nearly giving up.

**Before** (358 words) wrote three cards to choose from, plus tips:

> Congratulations to Amara! Here are a few options. Each one says you're proud of her without getting gushy.

**After** (128 words) wrote one:

> **Qualified nurse!** I'm so proud of you I could burst, but I'll spare you the speech. … (I'd like it noted that I said you could.)

### A job application

Someone needs a short covering email for a job. Their notes say they've worked at a hotel "since march 2019 so 6.5 yrs". By October 2026, that's seven and a half.

**Before** copied the number:

> For the past six and a half years I've worked at The Wrenfield Hotel …

**After** wrote "seven years" and flagged it after the draft:

> **How long you've been at the hotel:** March 2019 to now is about seven and a half years, not 6.5. I've put "seven years", so make sure your CV and form give the same figure.

## Does it work?

I tested it on 60 fresh writing tasks, written by agents that never saw the skill, and had blind Opus judges compare each pair with plain Claude.

| v0.8 on fresh tasks | wordcraft better | Plain Claude better | Tie |
|---|---|---|---|
| Opus, two fresh sets | 35 | 13 | 12 |
| Sonnet | 18 | 8 | 4 |
| Haiku | 19 | 6 | 5 |

The current version, v0.9, tied v0.8 head to head on another fresh set (11 pairs each), with shorter replies and fewer notes under personal messages.

Read those numbers with some care. My early versions looked far better on the tasks I developed them on than on new ones, which is why the fresh tests are the ones that count. v0.9 has only been tested on Opus. The full method, every result and the known gaps are in [evals/results.md](evals/results.md).

wordcraft won't get text past an AI detector, and isn't meant to. It's for readers.

## Install

**1. The skill.** Install it for every project with the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add cz4000/wordcraft -a claude-code -g
```

Leave out `-g` to install it for the current project only. To install by hand instead:

```bash
git clone https://github.com/cz4000/wordcraft.git ~/code/wordcraft
mkdir -p ~/.claude/skills && ln -s ~/code/wordcraft/skills/wordcraft ~/.claude/skills/wordcraft
```

**2. The always-on lines.** Copy [always-on.md](always-on.md) into your `~/.claude/CLAUDE.md`. Without it, the skill only loads when Claude is drafting something, and your everyday chat answers won't change.

To try it for one session first: `claude --plugin-dir ~/code/wordcraft`.

## Feedback

I'd like to hear what works for you and what doesn't. Find me on X at [@cz4000](https://x.com/cz4000), or [open an issue](https://github.com/cz4000/wordcraft/issues).

## Credits

- William Zinsser, *On Writing Well: The Classic Guide to Writing Nonfiction* (25th anniversary edition, 2001)
- George Orwell, "Politics and the English Language" (1946)
- Charlie Euchner, ["Ten Essential Rules for Writing Well"](https://theelementsofwriting.com/ten-essential-rules-for-writing-well/), *The Elements of Writing* (2018)
- BLUF, from the US Army's correspondence rules (Army Regulation 25-50), and Kabir Sehgal, ["How to Write Email with Military Precision"](https://kabir.cc/how-to-write-email-with-military-precision/), *Harvard Business Review* (2016)
- SBAR, developed by Michael Leonard, Doug Bonacum and Suzanne Graham at Kaiser Permanente and published by the [Institute for Healthcare Improvement](https://www.ihi.org/resources/Pages/Tools/SBARToolkit.aspx)
- Tim O'Reilly's [post](https://oreillyradar.substack.com/p/owners-not-renters-raffi-krikorian), for showing what Claude's writing can be

Every principle is restated in the skill's own words. The only quotes from the book are three short, credited lines.

## License

wordcraft is open source under the [MIT License](LICENSE). You can use, change and share it, including commercially, as long as you keep the copyright notice.

## Running the tests

```bash
uv run --with pytest pytest
```

The live evaluations call Claude and count against your usage, so `evals/run.py` and `evals/judge.py` both take `--dry-run` to print the number of calls first.
