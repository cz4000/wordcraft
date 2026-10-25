# wordcraft

wordcraft is a skill that makes Claude write for the person who will read it. It works in Claude Code and in anything else that runs Claude Code skills, including agents built on Claude.

## Why I made it

I use Claude Code every day, and I didn't like how it writes. At the end of a session it handed me a long list of changes, function by function, full of names I'd never seen. Nothing at the top said what the work was about or why, and nothing said what it meant for me. It read like someone else's notes. The emails and messages it drafted came out generic, and its answers came as walls of text.

In October 2026, Tim O'Reilly published [a piece that Claude wrote and he lightly edited](https://oreillyradar.substack.com/p/owners-not-renters-raffi-krikorian), and it showed me Claude can write well. Then someone suggested turning William Zinsser's *On Writing Well* into a skill.

So I did, adding ideas from George Orwell and Charlie Euchner. I wanted Claude, and the agents people build on it, to write clearer emails, clearer updates and clearer explanations.

## What it changes

Here are three of the ten test tasks, from the v0.4.1 round. Each reply without the skill is folded away; each reply with it is shown as Claude wrote it. In all three, blind judges preferred the skill's reply in both reading orders.

### Replying to an invitation

The request: *"Draft my reply to this email. I'd like to do it but I'd prefer the 45-minute slot if it's still free, and I can't make 20 Feb for the abstract, more like 27 Feb. Ask if that works."*

<details>
<summary>Without the skill (196 words)</summary>

> Subject: Re: Speaking at Riverside DevConf this spring?
>
> Hi Dana,
>
> Thanks for getting in touch, and thanks to whoever passed my name on. I'd be glad to speak at Riverside DevConf.
>
> If one of the 45-minute slots on the second day is still free, I'd like to take it. The extra time would let me go through a worked example properly, which tends to be the part people get the most out of. If they've both gone, I'm happy to do the 30-minute version on day one.
>
> The one problem is the deadline. I can't get a title and abstract to you by 20 February. Would 27 February work, or would that hold up the schedule too much?
>
> Thanks again for the invitation. I'm looking forward to it.
>
> Best,<br>
> [Your name]
>
> ---
>
> I mentioned that the 45-minute slots are on the second day (15 May), so there's no confusion about which day you're agreeing to. The worked-example line is my guess at why you'd want the longer slot, so change or cut it if it doesn't fit. I also offered the 30-minute slot as a fallback. Remove that sentence if you'd only do the 45-minute one.

</details>

**With the skill** (78 words):

> **Subject:** Re: Speaking at Riverside DevConf this spring?
>
> Hi Dana,
>
> Thanks for getting in touch. I'd be glad to speak at Riverside DevConf.
>
> If one of the 45-minute slots on 15 May is still free, I'd prefer that. The talk fits more comfortably in the longer slot.
>
> The one problem is the deadline for the title and abstract. I can't make 20 February. Would 27 February work, or is that too late for the schedule?
>
> Best,<br>
> [Your name]

It says the three things the user said and stops. Without the skill, Claude added a fallback the user never offered and a paragraph of notes on its own draft. Two flaws remain: the stock opener "Thanks for getting in touch", and a reason the user never gave ("The talk fits more comfortably in the longer slot"), which the other version at least flagged as a guess.

### Answering a question in the middle of a coding session

Claude has just fixed a rounding bug in `naturalsize`, a function in the `humanize` library. The user comes back and asks: *"Before I merge this, does it change anything for people who call naturalsize with gnu=True, or for really small numbers? Do I need to tell anyone?"*

<details>
<summary>Without the skill (454 words)</summary>

> **It changes gnu=True output, but only near the unit boundaries. Small numbers aren't affected at all.** It's a bug fix, not an API change, so one clear line in the release notes covers it.
>
> **gnu=True:** the fix covers all three modes (decimal, binary and gnu), because the carry runs after the unit is picked no matter which suffix set is used. GNU mode works in steps of 1024, so a value that rounds up to 1024 now moves to the next letter:
> - `naturalsize(1024**2 - 1, gnu=True)` used to give `1024.0K` and now gives `1.0M`. A test covers this.
> - Values that don't round up to 1024 come out exactly as before.
> - `1.0M` is also what GNU `ls -h` and `du -h` print, so gnu mode now matches the tools it's named after.
>
> **Really small numbers:** nothing changes. Anything below 1000 bytes (1024 in binary or gnu mode) returns early as `"N Bytes"`, `"1 Byte"` or `"NB"`, before reaching the new code. That includes fractions and 0.
>
> **Other edge cases:**
> - **Negative numbers** carry the same way: `-999999` should now give `-1.0 MB`.
> - **Exact powers like `10**15`:** the old code may have shown `1000.0 TB` because of a floating-point quirk in the unit calculation. The carry should turn that into `1.0 PB`. I haven't confirmed it, because my script to check it never got permission to run.
> - **The largest unit:** values above 999.9 QB still show as e.g. `1000.0 QB`, since there's no bigger unit to move to. A test covers this.
> - **Custom `format` strings:** if the output can't be read back as a number, the code just skips the carry, so the call can't fail.
>
> **Do you need to tell anyone?** Nobody's code will break. But anyone with snapshot tests, or code that matches strings like `"1000.0 kB"` or `"1024.0K"`, will see different output for values right at the boundaries. A PR title like "Carry `naturalsize()` to the next unit when rounding reaches the base" would cover it, matching how #328 described the same fix for `metric()`.
>
> **What I couldn't check before you merge:**
> - I never ran the test suite in full. It ran without the i18n, time and benchmark tests, because their dependencies (`freezegun`, `pytest-benchmark`) aren't installed and installing them needed approval. Of the tests that did run, 326 passed, including all 83 filesize tests.
> - I couldn't run the new tests against the old code to show they fail there. Reading the old code, they would.
> - I created `src/humanize/_version.py` so the package would import. It's gitignored and won't end up in the commit.
>
> The only tracked files changed are `src/humanize/filesize.py` and `tests/test_filesize.py`. Running the full suite with `tox` once before merging would close those gaps.

</details>

**With the skill** (410 words):

> Small numbers don't change. `gnu=True` output does change, and so does the default and binary output, but only for values that sit just under a unit boundary. A short changelog line covers it. Before you merge, compare this with the maintainers' own fix for the same bug (PR #329), which is the commit right after the one this branch starts from.
>
> **What changes for callers**
>
> The fix applies to all three modes. When rounding pushes the number up to the base (1000, or 1024 for binary and GNU), it now moves to the next unit:
>
> | Call | Before | After |
> |---|---|---|
> | `naturalsize(999_999)` | `1000.0 kB` | `1.0 MB` |
> | `naturalsize(1024**2 - 1, binary=True)` | `1024.0 KiB` | `1.0 MiB` |
> | `naturalsize(1024**2 - 1, gnu=True)` | `1024.0K` | `1.0M` |
>
> The "Before" column comes from reading the old code, not from running it. All other values give the same output as before. For GNU mode, that means only values just under a power of 1024 are affected.
>
> **Really small numbers**
>
> Values below 1000 (or 1024) leave the function early as `"N Bytes"` / `"NB"`, before the new code runs, so they're unaffected. Negative numbers get the same carry, so `-999_999` should give `-1.0 MB`, but no test covers that.
>
> **Edge cases that stay as they are**
>
> - At the largest unit there's nothing to carry to, so `1000**11 - 1` still prints `1000.0 QB`. That's on purpose and has a test.
> - If a custom `format` string produces something that isn't a plain number, the carry is skipped and the output matches the old behaviour.
>
> **Who to tell**
>
> Anyone whose code or snapshot tests expect the old strings, such as `1000.0 kB` or `1024.0K`. A changelog line like "naturalsize now rolls over to the next unit when rounding reaches 1000/1024" is enough. It's a bug fix, not an API change.
>
> **Testing gaps**
>
> - I couldn't install the test dependencies without your approval, so I skipped the time, i18n and benchmark tests. The other 326 tests passed, including all 83 filesize tests.
> - I didn't confirm that the new tests fail against the old code. That needed a `git stash`, which also needed approval.
> - I created `src/humanize/_version.py` so the tests could import the package. It's gitignored, but you can delete it.
> - I also added a stray `999_960 → "1.0 MB"` test case. It passes, but check that it's in the list where you'd expect it.

Both replies answer in their first lines. The skill's version shows the change as a before-and-after table, follows the user's questions in order, and keeps every testing gap. It's only a little shorter: the gain is in the order, not the length.

### Announcing a rule change

The request: tell #engineering that from Monday, merging into `main` needs one approving review and green CI, and nobody can push to it directly, leads included, because a hotfix pushed straight to `main` last Thursday broke checkout for two hours. Admins can still override in a real emergency.

<details>
<summary>Without the skill (260 words)</summary>

> Here's a draft for the channel:
>
> ---
>
> **Heads up: `main` becomes a protected branch on Monday (Oct 26)**
>
> Starting Monday, `main` will have branch protection turned on:
>
> • **Every PR needs one approving review** before it can merge<br>
> • **CI has to be green.** No merging while checks are failing or still running<br>
> • **Nobody can push directly to `main`**, leads included. All changes go through a PR
>
> **Why:** Last Thursday a hotfix was pushed straight to `main` and broke checkout for about two hours. It could have happened to any of us. The process allowed it, and this change closes that gap. A second pair of eyes and a passing build would have caught it.
>
> **What about emergencies?** Admins can still override protection when production is down and there's no time for a review. Treat this as a last resort. If you use it, post in #engineering what you changed and why, and open a follow-up PR so the change still gets reviewed.
>
> **What to do before Monday:**<br>
> • Merge or rebase any branches you've been pushing straight to `main`<br>
> • If a hotfix needs a fast review, ask for one in #engineering. Someone will jump on it
>
> Questions or concerns? Reply in the thread. 🙏
>
> ---
>
> I didn't name the person behind the hotfix, so the message is about the process and doesn't single anyone out. I also added a rule for using the admin override (post in the channel and open a follow-up PR). If you haven't actually agreed on that rule, delete it or change it.

</details>

**With the skill** (150 words):

> Here's the message for #engineering:
>
> ---
>
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
>
> ---
>
> I kept the person who pushed the hotfix unnamed, since the point is the process and not who did it. The last sentence about asking here for a quick review is my addition, so cut it if that isn't how you want urgent fixes handled.

The news comes first, the two rules sit in a short list, and the reason takes two sentences. Gone are the bold on every line, the emoji, the sign-off and an invented procedure for using the override. One of its two closing notes rightly flags a sentence Claude added; the other explains a choice, which the skill says to leave out.

## What's in it

The skill is two files in `skills/wordcraft/`:

- `SKILL.md`, which Claude loads when it's drafting something. It holds the rules and a note for each kind of writing: end-of-task summaries, answers in the middle of a task, chat answers, emails, status updates and longer pieces.
- `principles.md`, with each principle, its source and a before-and-after pair, mostly for human readers.

On its own, the skill loads only for drafting tasks. The separate `always-on.md` is a heading, one framing line and seven rules; pasted into `~/.claude/CLAUDE.md`, they shape every reply, chat included.

## Install

Install it for every project with Vercel's [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add cz4000/wordcraft -a claude-code -g
```

Leave out `-g` to install it for one project only.

To install by hand, clone the repo and link the skill folder:

```bash
git clone https://github.com/cz4000/wordcraft.git ~/code/wordcraft
mkdir -p ~/.claude/skills && ln -s ~/code/wordcraft/skills/wordcraft ~/.claude/skills/wordcraft
```

Once it's cloned, you can try it for one session with `claude --plugin-dir ~/code/wordcraft`. That loads the skill but not the always-on lines.

Then copy [always-on.md](always-on.md) into your `~/.claude/CLAUDE.md`, so the rules apply to every reply.

## How it was tested

I ran Claude Code headless in a clean setup, with and without the skill, and had blind Opus judges compare every pair twice, once in each order. When the two readings disagreed, the pair counted as a tie. The full method and every number are in [evals/results.md](evals/results.md).

The honest headline comes from two held-out tests: sets of 15 new writing tasks, each written by an agent that never saw the skill.

| On fresh tasks (Opus) | Skill better | Plain Claude better | Tie |
|---|---|---|---|
| v0.5, set 1 | 12 | 11 | 7 |
| **v0.8, set 2** | **17** | 7 | 6 |

**v0.5 matched plain Claude, about a fifth shorter, but didn't beat it.** Where plain Claude won, it was usually because it caught a real problem in the material and flagged it. The skill's rule against notes about the draft held that back.

**v0.8 fixed that and won 17 to 7 on tasks it had never seen** (p=0.06). It checks the source for problems the reader would want caught and lists them under "Check before sending". It caught a dispute deadline that had already passed, an applicant's miscounted years in post, and a date that was only assumed. Notes explaining its own choices stay banned. Its replies are about as long as plain Claude's.

On the ten tasks the skill was developed on, the judges preferred v0.5 in 21 pairs to 4, but much of that margin came from tuning on those tasks, which is why the held-out tests matter. On Haiku (v0.4) the judges preferred the skill in about seven of ten pairs; on Sonnet (v0.4) it made no difference. Neither was run on the fresh sets.

I also tried two variations built on BLUF and SBAR (v0.6 and v0.7). Neither beat v0.5, so the skill keeps v0.5's summary order and credits both as the practices it draws on.

It won't get text past an AI detector. Pangram rated all six texts it scanned 100% AI, with and without the skill. That isn't what it's for.

I also read blind pairs myself. After the first round I preferred the skill's writing in 7 of 10, but the original's formatting wherever formatting mattered. That's where the rule "match the shape to the content" came from.

## Where the ideas come from

Every principle is restated in the skill's own words, with credit.

- William Zinsser, *On Writing Well: The Classic Guide to Writing Nonfiction* (25th anniversary edition, 2001). The core of the skill: cut clutter; write for a reader who knows nothing of your work; start with the one fact they need, then widen out; write like a person; and "when you're ready to stop, stop."
- George Orwell, the six rules at the end of "Politics and the English Language" (1946). Restated: no stale figures of speech; the short word over the long one; cut any word you can; active over passive; the everyday word over jargon; and break any rule rather than write something barbarous.
- Charlie Euchner, ["Ten Essential Rules for Writing Well"](https://theelementsofwriting.com/ten-essential-rules-for-writing-well/), *The Elements of Writing* (2018). From it: one idea per paragraph; break a complex subject into pieces, in order; edit in passes, one problem at a time; read it aloud; and write for an intelligent reader who lacks your background.
- BLUF ("bottom line up front"), from the US Army's correspondence rules (Army Regulation 25-50), and Kabir Sehgal's ["How to Write Email with Military Precision"](https://kabir.cc/how-to-write-email-with-military-precision/) (*Harvard Business Review*, 2016). The skill's summaries lead with the outcome.
- SBAR (situation, background, assessment, recommendation), the hand-off format developed by Michael Leonard, Doug Bonacum and Suzanne Graham at Kaiser Permanente and published by the [Institute for Healthcare Improvement](https://www.ihi.org/resources/Pages/Tools/SBARToolkit.aspx). The skill's end-of-task summary order draws on it.
- One convention is the project's own: describe a thing in plain words first, then give its technical name in brackets.

## Run the tests

```bash
uv run --with pytest pytest
```

The live evaluations call Claude and count against your usage. Add `--dry-run` to `python evals/run.py` or `python evals/judge.py` to print the number of calls before anything runs.

## License

MIT
