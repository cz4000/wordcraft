# Wordcraft

**A writing skill for Claude.** It makes Claude's emails, messages, summaries and reports clearer and easier to read, whether you're reading them yourself or building agents that write for other people.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

```bash
npx skills add cz4000/wordcraft -a claude-code -g
```

Then add the [always-on lines](always-on.md) to your `~/.claude/CLAUDE.md`. [More install options](#install).

## Why I built it

I use Claude Code every day, and I'd grown tired of reading what it wrote. Short questions got long answers. End-of-session summaries listed every function it had touched, with names I'd never seen and nothing about what any of it meant for me. Emails it drafted could have come from anyone. The information was usually there, but getting it out was work.

In October 2026, Tim O'Reilly published [a piece that Claude wrote and he only lightly edited](https://oreillyradar.substack.com/p/owners-not-renters-raffi-krikorian), and it read beautifully. So Claude *can* write well. In the comments, a reader suggested turning William Zinsser's *On Writing Well* into a skill. That's where Wordcraft started.

## What's in it

Wordcraft starts from Zinsser and adds what testing showed was still missing.

- **Zinsser's core.** Cut clutter, write for a reader who knows nothing of your work, start with the one fact they need, sound like a person, and stop when you're done.
- **Orwell's six rules.** The short word over the long one, the everyday word over jargon, and cut any word you can.
- **Euchner's ten rules.** One idea per paragraph, and a complex subject taken one piece at a time.
- **BLUF and SBAR.** End-of-task summaries lead with the outcome, then cover what changed, what you need to do, what couldn't be checked and what's left behind.
- **Plain words first.** A name you haven't seen comes after a plain description, in brackets (`like_this`).
- **Check before sending.** When the material has a problem you'd want caught, such as a wrong date, figures that don't add up or a missing detail, Claude lists it after the draft.
- **A note for each kind of writing.** Summaries, emails, status updates, chat answers and longer pieces each get their own guidance.

It's two files, plus a few lines for your `CLAUDE.md` so everyday chat answers follow the same rules.

## Before and after

Three real tests, shown in full. In each one, blind judges read both replies, in both orders, and preferred the one written with Wordcraft.

### A note to a grieving colleague

**The request:**

> My colleague Tomasz's mum died on Saturday, quite suddenly from what I've heard. He's off for at least a fortnight. Someone's passing round a card for the team but I want to send him something of my own on Teams too, because we're actually quite close, we started the same week four years ago. I met his mum once, she came to the office Christmas do in 2023 and brought this enormous poppy seed cake and made everyone take a slice home. I've got no idea what to say to him.

**Plain Claude** (349 words):

> Here's a draft. The poppy seed cake is the best thing you have, so I've built the message around it. A specific memory of his mum tells him more than any general sympathy line could.
>
> ---
>
> **Tomasz, I'm so sorry about your mum.**
>
> I only met her the once, at the Christmas do in 2023, but I remember her so clearly: that huge poppy seed cake, and how she wouldn't let anyone leave without a slice to take home. She was so warm and generous with people she'd only just met. I can only imagine what she was like as a mum.
>
> I'm thinking of you and your family. Please don't feel you need to reply to this, or to anything from work. If you ever want to talk, or get out of the house for a coffee or a walk, I'm here. And if you'd rather not, that's completely fine too.
>
> Take all the time you need.
>
> ---
>
> **Why it's written this way:**
>
> - **"Please don't feel you need to reply"** is probably the kindest line in it. He'll be getting a lot of messages, and answering them all is tiring.
> - **The offer is specific.** "Coffee or a walk" is easier to say yes to than "let me know if you need anything," which leaves him to come up with something.
> - **It doesn't ask what happened.** Since it was sudden, he may not want to explain it again and again.
> - **It doesn't mention work**, apart from telling him he can ignore it.
>
> **Small things to adjust:**
>
> - Use whatever name you actually call him, if it's not Tomasz.
> - If he's Polish and you'd like to add something in Polish, *"Wyrazy współczucia"* (my condolences) is the standard phrase. Only add it if it feels natural for the two of you, though. It shouldn't come across as a gesture.
> - If coffee or a walk doesn't sound like your friendship, swap in something that does.
>
> You don't have to get it perfect. He'll mostly notice that you remembered his mum and that you got in touch.

**With Wordcraft** (168 words):

> Here's a draft you can send as it is or change to sound more like you:
>
> ---
>
> Tomasz, I'm so sorry about your mum. I've been thinking about you since I heard.
>
> I only met her the once, at the Christmas do in 2023, but I still remember her turning up with that enormous poppy seed cake and making sure every one of us took a slice home. Nobody was getting out of there without one.
>
> Please don't feel you need to reply to this, or think about work at all. I'm here if you ever want to talk, or not talk, or need anything doing.
>
> ---
>
> **Check before sending**
> - I've left out the word "sudden" because you only heard it secondhand. Let him decide how much he wants to say about how it happened.
> - If there's something specific you could actually do for him, like dropping food round or covering one of his pieces of work, offering that will mean more than "need anything doing".

Plain Claude added a section explaining its choices and a list of things to adjust. Wordcraft wrote the message at half the length, and its two checks are things the sender would want to know.

### An email to the team

**The request:**

> need an email to the whole warehouse team (about 40 people) that Hollis is leaving at the end of the month. he's been our warehouse supervisor for 9 years, everyone likes him. he and his wife are moving to Portugal, he's happy for people to know that. Ines is covering his role from 1 Dec until we hire someone. leaving drinks Thurs 26th at the Anchor from 5. there's a card going round, it's in the office

**Plain Claude** (239 words):

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

**With Wordcraft** (201 words):

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

Wordcraft kept every fact, dropped the emoji and the extra headings, and caught that the 30th is a Monday, so the leaving date needs confirming.

### A card for a niece

**The request:**

> My niece Amara has just found out she's passed her finals and is officially a qualified nurse!! She failed a module last year and nearly packed it in, and she worked nights at a care home the whole way through. I'm her aunt, we're close, and I talked her round when she wanted to quit. My sister's having a little do for her on Saturday and I want to write something in the card. She'd cringe at anything too soppy but I want her to know how proud I am.

**Plain Claude** (358 words):

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

**With Wordcraft** (128 words):

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

Plain Claude offered three cards and a page of tips. Wordcraft wrote one card, at a third of the length.

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

Wordcraft is open source under the [MIT License](LICENSE). You can use, change and share it, including commercially, as long as you keep the copyright notice.

## Running the tests

```bash
uv run --with pytest pytest
```

The live evaluations call Claude and count against your usage, so `evals/run.py` and `evals/judge.py` both take `--dry-run` to print the number of calls first. Every test, result and known gap is written up in [evals/results.md](evals/results.md).
