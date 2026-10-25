# Wordcraft

**A writing skill for AI agents.** It makes the emails, messages, summaries and reports your agent writes clearer and easier to read, whether you're reading them yourself or building agents that write for other people. It installs on Claude Code, Codex, Cursor, Gemini CLI and other agents that support skills.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

```bash
npx skills add cz4000/wordcraft -g
```

Then add the [always-on lines](always-on.md) to your agent's instructions file. [More install options](#install).

## Why I built it

I use Claude Code every day, and I'd grown tired of reading what it wrote. Short questions got long answers. End-of-session summaries listed every function it had touched, with names I'd never seen and nothing about what any of it meant for me. Emails it drafted could have come from anyone. The information was usually there, but getting it out was work.

In October 2026, Tim O'Reilly published [a piece that Claude wrote and he only lightly edited](https://oreillyradar.substack.com/p/owners-not-renters-raffi-krikorian), and it read beautifully. So Claude *can* write well. Then, on X, [@samsonfraser](https://x.com/samsonfraser) suggested turning William Zinsser's *On Writing Well* into a skill. That's where Wordcraft started.

## What's in it

Wordcraft starts from Zinsser and adds what testing showed was still missing.

- **Zinsser's core.** Cut clutter, write for a reader who knows nothing of your work, start with the one fact they need, sound like a person, and stop when you're done.
- **Orwell's six rules.** The short word over the long one, the everyday word over jargon, and cut any word you can.
- **Euchner's ten rules.** One idea per paragraph, and a complex subject taken one piece at a time.
- **BLUF and SBAR.** End-of-task summaries lead with the outcome, then cover what changed, what you need to do, what couldn't be checked and what's left behind.
- **Plain words first.** A name you haven't seen comes after a plain description, in brackets (`like_this`).
- **Check before sending.** When the material has a problem you'd want caught, such as a wrong date, figures that don't add up or a missing detail, the agent lists it after the draft.
- **A note for each kind of writing.** Summaries, emails, status updates, chat answers and longer pieces each get their own guidance.

It's two files, plus a few lines for your agent's instructions file so everyday chat answers follow the same rules.

## Before and after

> [!TIP]
> **Clearer, and shorter.** In blind tests on fresh writing tasks, judges preferred Opus 5.5 with Wordcraft in about 7 of every 10 comparisons that weren't ties. Its replies used 5–8% fewer words and 7–37% fewer output tokens than Opus 5.5 alone. Loading the skill adds some input tokens, most of them cached.

### Negotiating a job offer

**The request:**

> Got the offer through for the Brindlemoor job and it's lower than I was hoping. I do really want this one though, and I don't want to come across as greedy or blow it. Can you write my reply to Lena? Her email and my notes are below.

**Opus 5.5** (517 words)

> Here's a draft. It's warm and clearly keen, and it makes two asks.
>
> ---
>
> **Subject:** Re: Offer – Senior Insight Analyst
>
> Hi Lena,
>
> Thank you so much, and thank you for being so helpful throughout the process. I really enjoyed meeting Graham and Sanjeev, and I'm delighted the arrears case study went down well. I'm very excited about this role and the team, and I'd love to make it work.
>
> Before I accept, I'd like to discuss two points:
>
> **Salary:** I was hoping for a base nearer the top of the advertised £48–56k range. I have seven years' experience, I led the Power BI migration at Kestrel, and I currently line-manage two junior analysts, so I think I'd bring a lot from day one. Would Brindlemoor be able to offer £56,000?
>
> **Office days:** Graham mentioned in the interview that most of the team work two days in the office. Could this role be on the same pattern? It would make a real difference to me, as the commute is around 50 minutes each way.
>
> Everything else looks great. The pension is very generous, and 1 December works well with my one-month notice period.
>
> I know Graham wants to move quickly, so I'm happy to jump on a call whenever suits you this week if that's easier.
>
> Thanks again, I'm really looking forward to hearing back.
>
> Best wishes,
> Ruth
>
> ---
>
> **Why I wrote it this way:**
>
> - **It asks for £56k because that's what you want.** If they meet you halfway, you're at about £54k, which is the number you'd take. Your 7 years, the migration and managing two people make the top of the band easy to justify, and that's the only argument the email makes.
> - **The office-days ask uses Graham's own words.** That makes it a question about fairness rather than a demand. I left the parking cost out because it reads as a complaint. If they push back, you can bring it up on a call as the reason the extra day matters.
> - **It doesn't mention annual leave.** Three asks start to look like a list. I'd keep the 27 days for later: if they say they can't go higher on salary, you can ask, "Could you look at 27 days' leave instead?" It's an easy thing for them to give, and you can point out it's what you have now.
> - **It doesn't mention Calvert, Mags's salary, or what you said on the first call.** You don't want to bluff about Calvert. Quoting a friend's salary can feel awkward to the person reading it. And since you can't remember whether you said "low to mid fifties" or 55, it's safer not to mention it. If Lena brings it up, "mid fifties" fits £56k.
> - **Your walk-away number of £52.5k isn't in the email.** Asking for more isn't greedy, especially when you're saying you want the job. Companies expect a counter, and offering to call shows you'll be easy to deal with.
>
> If you'd rather go for 27 days of leave now as well, I can add it as a short third point.

**Opus 5.5 with Wordcraft** (404 words)

> Here's a reply that's clearly keen but makes two firm asks: £56k and two office days. It doesn't mention your fallback figures or Calvert.
>
> ---
>
> **Subject:** Re: Offer – Senior Insight Analyst
>
> Hi Lena,
>
> Thank you, that's brilliant news. I'm really keen to join Brindlemoor and the team, and I'd like to make this work.
>
> Before I accept, I'd like to raise two things.
>
> **Salary.** I have seven years' experience, led the Power BI migration at Kestrel and managed two junior analysts, so I'd hoped for an offer nearer the top of the £48–56k range in the advert. Would you be able to move the base salary to £56,000?
>
> **Office days.** Graham mentioned in the interview that most of the team work two days in the office. Could this role follow the same pattern, with two days at Ashby Road and three at home? With the commute, that would make a real difference.
>
> Everything else works well for me, and 1 December fits with my one-month notice period.
>
> I know Graham wants to get this settled before the budget round, so I'm happy to talk it through on a call this week if that's easier.
>
> Best wishes,
> Ruth
>
> ---
>
> **Check before sending**
>
> - **1 December 2026 is a Tuesday, not a Monday.** Ask Lena which date she means. With one month's notice, you'll need to resign by about 1 November to start then.
> - **The deadline probably comes before your Calvert interview.** Lena wants an answer by the end of the week, and your Calvert interview is next Tuesday. If talks go quickly, you may have to decide on Brindlemoor first.
> - **Leave isn't in the draft.** I kept to two asks so it doesn't read as a list of demands. If they come back below £56k, asking for 27 days is a reasonable next step. You could also add it now as a third line.
> - **Have your answer ready if they offer £54k with two office days.** By your own notes, you'd take that. A likely reply is somewhere in between, so decide in advance whether you'd accept, for example, £53k with two days.
> - **The email doesn't mention what you said on your first call or Mags's salary.** You're not sure whether you said "low to mid fifties" or £55k, so quoting it could backfire. Mags's figure is second-hand and two years old, so the advertised range is the safer anchor.

### An email to the team

**The request:**

> need an email to the whole warehouse team (about 40 people) that Hollis is leaving at the end of the month. he's been our warehouse supervisor for 9 years, everyone likes him. he and his wife are moving to Portugal, he's happy for people to know that. Ines is covering his role from 1 Dec until we hire someone. leaving drinks Thurs 26th at the Anchor from 5. there's a card going round, it's in the office

**Opus 5.5** (239 words)

> **Subject:** Hollis is leaving us at the end of November
>
> Hi all,
>
> I'm sorry to tell you that Hollis is leaving at the end of November. He's been our warehouse supervisor for nine years, and I know many of you will be as sad to see him go as I am.
>
> The good news is that he's leaving for a great reason. Hollis and his wife are moving to Portugal to start a new chapter, so please do ask him about it.
>
> **Who to go to from 1 December**
> Ines will cover the warehouse supervisor role from 1 December while we recruit a permanent replacement. From then on, please take anything you'd normally bring to Hollis to Ines. We'll let you know how recruitment is going.
>
> **Leaving drinks**
> Please join us to send Hollis off properly:
> 📍 The Anchor
> 🗓 Thursday 26 November, from 5pm
>
> **Card**
> There's a card for Hollis in the office. Please pop in and sign it before the 26th.
>
> Hollis, thank you for nine brilliant years. We'll miss you, and we wish you and your wife all the best in Portugal.
>
> Best,
> [Your name]
>
> ---
>
> I put November as the month because 26 November 2026 is a Thursday and Ines starts on 1 December. You might also want to add who's collecting money for a gift, if anyone is, or a "let us know if you're coming" line if you need numbers for the Anchor.

**Opus 5.5 with Wordcraft** (201 words)

> **Subject: Hollis is leaving us at the end of November**
>
> Hi all,
>
> I'm sorry to say that Hollis is leaving at the end of November. He's been our warehouse supervisor for 9 years, and I know many of you will miss him as much as I will.
>
> He's leaving for a happy reason. He and his wife are moving to Portugal, and he's glad for everyone to know.
>
> From 1 December, Ines will cover Hollis's role until we hire a new supervisor. Please go to her with anything you'd normally take to him.
>
> **Leaving drinks: Thursday 26 November, at the Anchor from 5pm.** Please come and give him a proper send-off.
>
> There's also a card going round for him. It's in the office, so do stop by and sign it.
>
> Thanks,
> [Your name]
>
> ---
>
> **Check before sending**
> - I assumed "end of the month" means November. That makes Thursday the 26th correct and fits Ines starting on 1 December. 30 November is a Monday, so you may want to give Hollis's actual last day.
> - I took "from 5" to mean 5pm.
> - If the card has a deadline for signing, or a particular spot in the office, it's worth adding.

### A card for a niece

**The request:**

> My niece Amara has just found out she's passed her finals and is officially a qualified nurse!! She failed a module last year and nearly packed it in, and she worked nights at a care home the whole way through. I'm her aunt, we're close, and I talked her round when she wanted to quit. My sister's having a little do for her on Saturday and I want to write something in the card. She'd cringe at anything too soppy but I want her to know how proud I am.

**Opus 5.5** (358 words)

> Congratulations to Amara! Here are a few options. Each one says you're proud of her without getting gushy.
>
> **Option 1: Warm with a bit of a wink**
> > Amara,
> > I know you'd rather I didn't make a fuss, so I'll keep it short: I am so ridiculously proud of you. You did this while working nights, you got knocked down and came back, and you didn't give up even when you really wanted to. That's exactly the kind of person who should be a nurse.
> > Your patients are lucky. Now go and have a drink, you've earned it.
> > Love, [Name] x
>
> **Option 2: Nods to the hard bit without dwelling on it**
> > Amara,
> > Officially a nurse! I remember the phone call when you were ready to pack it all in, and look at you now. Plenty of people would've walked away. You didn't. Nights at the care home, resits, finals, all of it, and you got there.
> > I couldn't be prouder. (That's all the soppiness you're getting, promise.)
> > Love always, [Name] x
>
> **Option 3: Short and punchy**
> > Amara,
> > Told you you could do it. 😉
> > Seriously though, after everything you juggled to get here, this is a massive achievement and I'm so proud of you. The NHS has no idea how lucky it is.
> > Love, [Name] x
>
> **A few tips:**
> - In Option 2, the line about her wanting to quit is a nice touch because you were there for it. If she's sensitive about that time, though, you could soften it to something like "I know there were times it felt impossible."
> - The "Told you so" opener in Option 3 only works if that's how you two usually talk. If you tease each other, it'll make her laugh. If not, go with one of the others.
> - If she's already got a job lined up, or you have an in-joke about scrubs, night shifts or the care home, adding one specific detail like that will mean more than any general compliment.
>
> I can change the tone or make any of these shorter if you'd like.

**Opus 5.5 with Wordcraft** (128 words)

> Here's a draft that's proud without getting soppy, with a little joke about you talking her round:
>
> ---
>
> Amara,
>
> **Qualified nurse!** I'm so proud of you I could burst, but I'll spare you the speech.
>
> You did this working nights the whole way through, and you came back from a year that would have made most people give up. You nearly did, and then you didn't. That's the bit I'll always remember.
>
> (I'd like it noted that I said you could.)
>
> Your patients are lucky to have you. Now go and sleep for a week.
>
> All my love,
> [Your name] x
>
> ---
>
> If you want it even shorter, you could keep just the first line, the bracketed line and the sign-off. Most of the pride is in those.

## Install

**1. The skill.** Install it for every project with the [skills CLI](https://github.com/vercel-labs/skills). It asks which of your agents to install it for:

```bash
npx skills add cz4000/wordcraft -g
```

To choose the agent yourself, add `-a` with its name:

| Agent | Command |
|---|---|
| Claude Code | `npx skills add cz4000/wordcraft -g -a claude-code` |
| Codex | `npx skills add cz4000/wordcraft -g -a codex` |
| Cursor | `npx skills add cz4000/wordcraft -g -a cursor` |
| Gemini CLI | `npx skills add cz4000/wordcraft -g -a gemini-cli` |
| GitHub Copilot | `npx skills add cz4000/wordcraft -g -a github-copilot` |
| OpenCode | `npx skills add cz4000/wordcraft -g -a opencode` |

Leave out `-g` to install it for the current project only. The CLI supports [many more agents](https://github.com/vercel-labs/skills/blob/main/docs/agents.md).

**2. The always-on lines.** Copy [always-on.md](always-on.md) into your agent's global instructions file, so everyday chat answers follow the same rules:

| Agent | File |
|---|---|
| Claude Code | `~/.claude/CLAUDE.md` |
| Codex | `~/.codex/AGENTS.md` |
| Gemini CLI | `~/.gemini/GEMINI.md` |
| Others | the agent's own instructions file, often `AGENTS.md` |

Without them, the skill only loads when the agent is drafting something.

Wordcraft was tested with Claude models (Opus, Sonnet and Haiku). It installs on the other agents above, but hasn't been tested with their models.

To install by hand for Claude Code instead:

```bash
git clone https://github.com/cz4000/wordcraft.git ~/code/wordcraft
mkdir -p ~/.claude/skills && ln -s ~/code/wordcraft/skills/wordcraft ~/.claude/skills/wordcraft
```

## Feedback

I'd like to hear what works for you and what doesn't. Find me on X at [@cz4000](https://x.com/cz4000), or [open an issue](https://github.com/cz4000/wordcraft/issues).

## Credits

- William Zinsser, *On Writing Well: The Classic Guide to Writing Nonfiction* (25th anniversary edition, 2001)
- George Orwell, "Politics and the English Language" (1946)
- Charlie Euchner, ["Ten Essential Rules for Writing Well"](https://theelementsofwriting.com/ten-essential-rules-for-writing-well/), *The Elements of Writing* (2018)
- BLUF, from the US Army's correspondence rules (Army Regulation 25-50), and Kabir Sehgal, ["How to Write Email with Military Precision"](https://kabir.cc/how-to-write-email-with-military-precision/), *Harvard Business Review* (2016)
- SBAR, developed by Michael Leonard, Doug Bonacum and Suzanne Graham at Kaiser Permanente and published by the [Institute for Healthcare Improvement](https://www.ihi.org/resources/Pages/Tools/SBARToolkit.aspx)
- Tim O'Reilly ([@timoreilly](https://x.com/timoreilly)), whose [post](https://oreillyradar.substack.com/p/owners-not-renters-raffi-krikorian) showed what Claude's writing can be
- [@samsonfraser](https://x.com/samsonfraser), who suggested building the skill on *On Writing Well*

Every principle is restated in the skill's own words. The only quotes from the book are three short, credited lines.

## License

Wordcraft is open source under the [MIT License](LICENSE). You can use, change and share it, including commercially, as long as you keep the copyright notice.

## Running the tests

```bash
uv run --with pytest pytest
```

The live evaluations call Claude and count against your usage, so `evals/run.py` and `evals/judge.py` both take `--dry-run` to print the number of calls first. Every test, result and known gap is written up in [evals/results.md](evals/results.md).
