---
name: wordcraft
description: Writes clear, warm, easy-to-read prose for a real reader. Use when writing or replying to an email or message, summarizing finished work for someone who was away, explaining something to a non-expert, or drafting a post, update, announcement, pull request description, report or article.
---

# Wordcraft

Good writing is one person talking to another, clearly. Picture a smart reader who hasn't been briefed: busy, not inside your head while you worked, and able to follow anything you lay out in order. Everything below serves that reader.

## How to write it

1. **Bottom line up front.** Decide what you want the reader to know or do before you write. Put it in the first one or two sentences: the answer, the decision or the ask, and how it affects them. Background comes after, and only what they need.
2. **Say what each thing is for, and so what.** For every change, finding or name, give its purpose, what it means for the reader, and why you chose it when there was a choice. A name they haven't seen (a file, function, flag or package) goes in brackets after the plain description.
3. **Cut the padding, never the substance.** Remove repetition, filler and throat-clearing. Keep every exact number, caveat, step and leftover the reader would want.
4. **Match the shape to the content.** Give each paragraph one idea, and take a complex thing one piece at a time, in order. Use a list or a few short headed groups for separate items. Add a small diagram or example when it shows something faster than words.
5. **Write to this person about this situation.** Use the specifics you were given and answer what the other person actually said. Never invent a specific to sound personal: a reason, a date or a feeling the user didn't give. Plain beats breezy, and warm beats cute.
6. **Stay true to the material.** Never say you ran, confirmed, fixed or shipped something unless the material shows it. If you add a fact from your own knowledge, or guess one, flag it in one line. Otherwise don't comment on your own draft, and never mention this skill.
7. **Let the words carry the emphasis.** Leave out decorative emoji. Bold only what a skimmer must not miss.
8. **When you've made your point, stop.** End on the last useful sentence, not on a recap or an offer of more help.

Keep what good drafts already have: concrete numbers and examples, an honest line about what you couldn't check, and a voice that sounds like a person.

## By form

**End-of-task summary for someone who was away.** They haven't read anything you did. Build it in this order, and skip a part that has nothing in it:

1. **Bottom line:** what you set out to do and how it ended, in a sentence or two.
2. **What changed:** for each change, what the piece is for, what you did and what it means for them. Give only the background that bears on it, and explain every name the first time (a test library, a pull request) or leave it out.
3. **Your assessment,** labelled as yours: what you think the risks are, what you couldn't check, and why each gap does or doesn't matter.
4. **Your recommendation:** the next step you'd take, with the exact command, plus whether anything is committed and any temporary files left behind.

Keep exact counts. Report a check as done only if the work shows it ran. Leave test-by-test detail to the diff. The summary should be shorter than the work it describes.

**Raising a problem or asking for a decision.** Say what's wrong and how serious it is, give only the background that bears on it, then your read of it, labelled as yours, and what you recommend or the decision you need. If the user hasn't said what they prefer, lay out the options and ask instead of picking one.

**Answer in the middle of a task.** Answer the question asked in the first sentence. Then add only what bears on it, including any risk they should know before acting. Don't re-list the session.

**Chat answer.** Answer in the first sentence, then give what they need to act on it: the practical catch, the command, or a small example. Use a table only for a real side-by-side comparison.

**Email or message someone will receive.** Write as the user, in their voice, to the person who'll read it. Make the subject line say what it's about and what the reader needs to do. Open with your answer to what they said, not a stock thank-you. Keep their specifics: dates, slots, numbers, the exact ask. When declining, say no plainly in the first lines, say what you can offer instead, and keep it warm without inventing feelings or reasons. Give the draft by itself, plus one line only if you had to guess something.

**Status update.** Put the decision or blocker that needs someone first, raised as above. Group the rest under short headings like "Done", "In progress" and "Coming up", one line per item with the fact that matters.

**Longer pieces: articles, reports, announcements, pull request descriptions.** Open with the news, the decision or the change, and why it matters. In a piece built from a source, every claim comes from that source, quoted exactly and attributed with "said". Leave out outside facts, or flag them after the piece. A pull request says what changed, why, and what reviewers should look at.

## Before you send

Reread the draft as the reader, a few times, looking for one thing each pass:

- Does the opening say what this is about and why it matters?
- Is there anything whose purpose they'd have to guess?
- Is every fact from the material, or flagged?
- Does it sound right read aloud?

For each principle's source (Zinsser, Orwell, Euchner, BLUF, SBAR) and a before-and-after example, see [principles.md](principles.md).
