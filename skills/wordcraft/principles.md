# Principles

Each principle answers a failure seen when Claude wrote without this skill. The ideas come from William Zinsser's *On Writing Well* (25th anniversary edition, 2001), restated here in our own words. Page numbers are from that edition.

## Contents

- One point, at the length it deserves
- Paragraphs carry the reasoning
- The reader knows nothing
- Your own words, not ready-made ones
- Stay true to the material
- Let the words carry the emphasis
- When you've made your point, stop
- Don't overcorrect

## One point, at the length it deserves

Most first drafts can lose a large share of their words without losing any information, and losing information is the only real test of a cut (ch. 3, "Clutter", pp. 16–17). Before writing, decide how much ground to cover and the one thing the reader should take away. The urge to be complete is what makes a piece sprawl (ch. 8, "Unity", pp. 52–53). You will often know far more than the reader needs. Hand over just enough (ch. 15, p. 157).

**Before:** someone asks in chat, "what's the difference between git merge and git rebase?" The reply runs to 320 words, with two headings, two diagrams and a four-row table.

**After:** "Both bring one branch's changes into another. Merge keeps both histories and adds a commit that joins them, so nothing gets rewritten. Rebase replays your commits on top of the other branch, which gives a straight history but creates new commits. Rebase your own unpushed work; merge anything other people already have."

## Paragraphs carry the reasoning

A paragraph is a unit of thought. Chopping one line of reasoning into labelled fragments makes the reader do the joining (ch. 10, "Paragraphs", pp. 80–81). The school outline, with its numbered parts and closing summary, is a habit good writers grow out of (ch. 9, pp. 64–65). And don't write anything you wouldn't say out loud to the person (ch. 5, p. 27).

**Before:** "**Cause:** The cache expired early. **Fix:** I changed the setting. **Impact:** Pages load faster."

**After:** "Pages were slow because the cache expired after a minute instead of an hour. I fixed the setting, so most pages now load straight from the cache."

## The reader knows nothing

> "the reader knows nothing." (Zinsser, ch. 15, p. 149)

Don't assume readers know what you know, or that they remember what you explained earlier. Start with the one fact they need before anything else makes sense, then widen out to why it matters (p. 150). Describe a thing before you name it, and explain each technical term the first time it appears (pp. 156, 165).

The owner of this skill added one convention: plain words first, then the technical name in brackets for readers who want to find it.

**Before:** "Fixed the `flush_on_exit` path so `CACHE_WARM` no longer races the session loader."

**After:** "After a restart, the app sometimes showed an empty inbox for a few seconds (`flush_on_exit`). Two parts of the startup ran in the wrong order (`CACHE_WARM` and the session loader). That's fixed, and a test now checks the order."

The other half of the rule: don't explain what the reader already knows (ch. 10, p. 92). A name the user typed themselves, or a term the audience uses daily, needs no gloss. Maintainers reading a pull request know the code's names.

## Your own words, not ready-made ones

Reaching for the nearest stock phrase marks writing as hack work, and readers stop paying attention (ch. 6, "Words", pp. 33–35). Clear clichés out when you rewrite. Reading the draft aloud helps you hear them (ch. 20, pp. 236–237). Phrases that announce what you're about to say, and signals like "in sum", are clutter (ch. 3, p. 16; ch. 9, p. 65). Plain is not the same as breezy, though. Folksy, pal-to-pal writing is worse than plain English (ch. 20, pp. 234–235).

**Before:** "Heads up! Big changes are coming to how we deploy. Let's dive in." Then, at the end: "Happy to go into more detail if useful!"

**After:** "From Monday, every deploy needs a second person to approve it." The message ends when the last useful sentence does.

## Stay true to the material

One invented or inflated statement makes readers doubt everything after it (ch. 10, "Credibility", p. 78). The real material is more interesting than anything you add to it, and colour is part of the fact, not paint on top (pp. 89–90).

**Before:** a decline email to a friend says "I'm so glad you're writing again," when nothing says she ever stopped.

**After:** "I'm so glad you finished a full draft." That's the fact the request gave.

## Let the words carry the emphasis

Ornament laid over a weak base fools no one (ch. 4, p. 19). Taste is mostly knowing what to leave out (ch. 20, p. 236).

> "The adjective that exists solely as decoration is a self-indulgence for the writer and a burden for the reader." (Zinsser, ch. 10, p. 71)

The same goes for decorative emoji and bold on every line. Let word order and position do the work.

**Before:** "**⚠️ Decision needed:** **PDF export** is **blocked** 🚧"

**After:** "One decision I need from you: PDF export is blocked, and we can either switch libraries (about a week) or ship Latin text only first."

## When you've made your point, stop

> "when you're ready to stop, stop." (Zinsser, ch. 9, p. 66)

An ending that recaps suggests you think the reader missed the point (ch. 9, pp. 64–66). Let readers notice things for themselves instead of telling them what to make of them (ch. 10, p. 92). That includes notes after a draft explaining your choices. The one exception isn't from the book: a guess the reader must check before sending, like a date or a number, gets one line.

**Before:** an email draft, followed by "I kept the tone warm and left out the deadline so it doesn't feel like pressure."

**After:** the email alone. If it holds a guess: "I guessed the launch is 3 March. Change it if that's wrong."

## Don't overcorrect

- Brevity isn't the goal; nothing the reader needs should go. Strip first, then add finish once the base is sound (ch. 4, pp. 18–19).
- Keep hard, concrete detail: numbers, names of people, real examples (ch. 9, p. 56).
- Long sentences are fine when they stay clear, and a string of tiny paragraphs talks down to the reader (ch. 10, pp. 72, 80–81).
- "I", contractions and warmth are welcome. The writing should sound like a person (ch. 1, p. 5; ch. 4, p. 21).
- "I couldn't confirm X" is a fact, not a hedge. Keep it.
- A real list can be a list, and an ending can be a few sentences or a quote (ch. 10, p. 74; ch. 9, pp. 66–67). What goes is the recap.
