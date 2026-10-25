# Principles

Each principle answers a failure seen when Claude wrote without this skill, or one the skill's owner named after reading blind samples. The ideas come from William Zinsser's *On Writing Well* (25th anniversary edition, 2001) the six rules at the end of George Orwell's essay "Politics and the English Language" (1946), and Charlie Euchner's "Ten Essential Rules for Writing Well" (*The Elements of Writing*, 2018, https://theelementsofwriting.com/ten-essential-rules-for-writing-well/), restated here in our own words. Page numbers are from Zinsser's edition.

## Contents

- Start where the reader is
- The reader knows nothing
- Cut the padding, never the substance
- Match the shape to the content
- Write to this person about this situation
- Stay true to the material
- Let the words carry the emphasis
- When you've made your point, stop
- Don't overcorrect

## Start where the reader is

The opening has one job: tell the reader what this is and why it's worth their attention, so they want to go on (ch. 9, "The Lead and the Ending", pp. 55–56). In technical writing, begin with the one fact the reader needs before anything else makes sense, then widen out to what it means for them (ch. 15, p. 150). A list of changes with no frame around it reads like a stranger's notes.

**Before:** "Changed `to_local_date()` to use `account.tz`. Added 6 test cases. `tzdata` isn't installed, so `test_dst.py` was skipped."

**After:** "You asked why some customers in Sydney saw invoices dated a day early. It's fixed: dates are now converted using each account's own time zone instead of the server's (`to_local_date()`). Most tests passed. The ones covering daylight-saving changes couldn't run here, so it's worth one full run before you merge."

## The reader knows nothing

> "the reader knows nothing." (Zinsser, ch. 15, p. 149)

Don't assume readers know what you know, or that they remember what you explained earlier (ch. 15, p. 149). That goes beyond names. Say what each thing is *for* and why it matters to them, not only what it's called or what you did to it. Lead them step by step, with no leaps, so each sentence follows from the last (pp. 149–150). Describe a thing before you name it, and explain each technical term the first time it appears (pp. 156, 165). Orwell put the word-level version as two rules: choose the short word over the long one, and the everyday word over the jargon or scientific one.

Euchner pictures the same reader more kindly: intelligent, but without your background (rule 10). Write for that person and you neither lose them nor talk down to them.

The owner of this skill added one convention: plain words first, then the technical name in brackets for readers who want to find it.

**Before:** "Fixed the `flush_on_exit` path so `CACHE_WARM` no longer races the session loader."

**After:** "After a restart, the app sometimes showed an empty inbox for a few seconds (`flush_on_exit`). Two parts of the startup ran in the wrong order (`CACHE_WARM` and the session loader). That's fixed, and a test now checks the order."

The other half of the rule: don't explain what the reader already knows (ch. 10, p. 92). A name the user typed themselves, or a term the audience uses daily, needs no gloss. Maintainers reading a pull request know the code's names.

## Cut the padding, never the substance

Most first drafts can lose a large share of their words without losing any information, and losing information is the only real test of a cut (ch. 3, "Clutter", pp. 16–17). Decide what the reader should take away, and resist the urge to cover everything (ch. 8, "Unity", pp. 52–53). Orwell's version is blunter: if a word can go, cut it. What goes is repetition and throat-clearing. What stays is every fact, caveat, step and loose end the reader will need, such as the temporary files left on their machine or whether anything was committed.

**Before:** "As mentioned above, the fix, which I described earlier, should now work correctly in all of the cases we discussed."

**After:** "The fix works for every case above. Nothing is committed yet, and I left a copy of the demo database in `/tmp/demo.db` that you can delete."

## Match the shape to the content

A paragraph is a unit of thought, and chopping one line of reasoning into labelled fragments makes the reader do the joining (ch. 10, "Paragraphs", pp. 80–81). But a real list can be a list (ch. 10, p. 74). Give each paragraph one idea and develop it. Take a complicated subject apart and walk the reader through the pieces in order, instead of cramming several ideas into one passage (Euchner, rules 3–5). When content is a set of separate items, such as a weekly status, options or next steps, a few short headed groups let a busy reader find their part. The skill's owner also asked for a small diagram or example where it shows a difference faster than prose. Don't write anything you wouldn't say out loud to the person (ch. 5, p. 27).

**Before** (one explanation, chopped up): "**Cause:** The cache expired early. **Fix:** I changed the setting. **Impact:** Pages load faster."

**After:** "Pages were slow because the cache expired after a minute instead of an hour. I fixed the setting, so most pages now load straight from the cache."

**Before** (separate items, run together as prose): "The search reindex finished Monday, and the iOS build is stuck waiting on a new signing certificate, and the pricing page goes live on the 3rd, and I'm off next Wednesday."

**After:** "**Needs a decision:** the iOS build is stuck until someone with admin access renews the signing certificate. Who should do it?" Then "**Done:** search reindex, finished Monday." Then "**Coming:** pricing page live on the 3rd. I'm off next Wednesday."

## Write to this person about this situation

A letter that sounds like a person beats one in an institutional voice (ch. 16, "Business Writing", p. 171), and writing that has humanity and warmth is what holds a reader (ch. 1, p. 5). Reaching for the nearest stock phrase marks writing as hack work (ch. 6, "Words", pp. 33–35). Orwell's first rule says the same about figures of speech: if you're used to seeing it in print, don't use it. Reading the draft aloud helps you hear stock phrases (ch. 20, pp. 236–237), and so does editing in passes, hunting one kind of problem at a time (Euchner, rules 8–9). Generic warmth ("Thanks for getting in touch", "Looking forward to it") is still stock. The cure is specifics: answer what this person said, in the user's own voice. The specifics have to be real. When the user hasn't given a reason, a date or a feeling, don't supply one to make the message sound personal. Leave it out, or flag it as a guess. Plain is not the same as breezy, though. Folksy, pal-to-pal writing is worse than plain English (ch. 20, pp. 234–235).

**Before:** "Thanks so much for reaching out! I'd be happy to help. Looking forward to it!"

**After:** "Yes, I'd like to join the review panel. I can do the March and May sessions, but April clashes with a product launch. Is it all right to miss that one?"

## Stay true to the material

One invented or inflated statement makes readers doubt everything after it (ch. 10, "Credibility", p. 78). The real material is more interesting than anything you add to it, and colour is part of the fact, not paint on top (pp. 89–90). Claims about your own work count too: saying you confirmed, ran or shipped something the record doesn't show is an invention like any other. Facts from your own knowledge are additions too. In a piece built from a source, leave them out, or flag them in one line after the piece so the reader can check them.

**Before:** a congratulations note says "Congratulations on the promotion!" when the request only says the person moved to a new team.

**After:** "Congratulations on the move to the platform team." That's the fact the request gave.

## Let the words carry the emphasis

Ornament laid over a weak base fools no one (ch. 4, p. 19). Taste is mostly knowing what to leave out (ch. 20, p. 236).

> "The adjective that exists solely as decoration is a self-indulgence for the writer and a burden for the reader." (Zinsser, ch. 10, p. 71)

The same goes for decorative emoji and bold on every line. Let word order and position do the work, and keep bold for the one or two things a skimmer must not miss.

**Before:** "**⚠️ Heads up:** the **iOS build** is **blocked** 🚧"

**After:** "**Needs a decision:** the iOS build is blocked until the signing certificate is renewed, and only an admin can do that."

## When you've made your point, stop

> "when you're ready to stop, stop." (Zinsser, ch. 9, p. 66)

An ending that recaps suggests you think the reader missed the point (ch. 9, pp. 64–66). Let readers notice things for themselves instead of telling them what to make of them (ch. 10, p. 92). That includes notes after a draft explaining your choices. The one exception isn't from the book: a guess or an outside fact the reader must check, like a date or a claim the source doesn't make, gets one line.

**Before:** an email draft, followed by "I kept the tone warm and left out the deadline so it doesn't feel like pressure."

**After:** the email alone. If it holds a guess: "I guessed the launch is 3 March. Change it if that's wrong."

## Don't overcorrect

- Orwell ended his rules with the brake this section exists for: break any of them rather than write something clumsy or unclear.
- Brevity isn't the goal; nothing the reader needs should go. Strip first, then add finish once the base is sound (ch. 4, pp. 18–19).
- Keep hard, concrete detail: numbers, names of people, real examples (ch. 9, p. 56).
- Long sentences are fine when they stay clear, and a string of tiny paragraphs talks down to the reader (ch. 10, pp. 72, 80–81).
- "I", contractions and warmth are welcome. The writing should sound like a person (ch. 1, p. 5; ch. 4, p. 21).
- "I couldn't confirm X" is a fact, not a hedge. Keep it.
- Prefer the active voice where it works, as Orwell asks, but a passive is right when the actor doesn't matter or shouldn't be named: "a hotfix was pushed straight to main" blames no one.
- Structure that helps a reader find things stays. What goes is structure that chops up a single thought.
- An ending can be a few sentences or a quote (ch. 9, pp. 66–67). What goes is the recap.
