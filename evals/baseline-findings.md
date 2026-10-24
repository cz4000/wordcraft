# Baseline findings: Opus without the skill

30 outputs: 10 tasks × 3 samples, Opus, clean setup, run on 2026-10-24. I read every one.

**The short version:** Opus already writes plainly and leads with the answer. Its problems are elsewhere. It answers small questions at length and formats chat replies like documents. It uses names the reader has never seen, reaches for stock phrases, and adds notes about its own draft. The skill should fix those and leave the rest alone.

## The failures the design named

| Failure | Seen? | Where | Example |
|---|---|---|---|
| Too long for the question | **Yes** | quick-question 3/3 (306–344 words, headings, diagrams, a table, for a one-line chat question); mid-session-answer 3/3 (415–454 words for a yes/no question); session-summary 3/3 (~375 words) | A casual "what's the difference between merge and rebase?" gets `## git merge`, `## git rebase` and a four-row table. |
| Point buried | **No** | 0/30. Every output opens with the answer. | "I fixed it: `naturalsize(999999)` now returns `'1.0 MB'`." |
| Wrong form (list vs paragraph) | **Yes**, always toward too much structure | Bold-label sections in 5 of 10 tasks, including a short message to a non-technical manager | "**Why reports got faster:** Before, building a report meant…" |
| Stiff or formal tone | **No**, but stock phrases | The tone is plain. The same set phrases recur across samples. | "Happy to go into more detail if useful." (explain-concept 3/3); "Your book deserves better than that, and so do you." (email-decline, a variant in 3/3) |
| Repeating the question back | **No** | 0/30 | — |
| Names the reader never saw | **Yes** | session-summary 3/3, mid-session-answer 3/3 | "`freezegun` isn't installed", "This matches how `metric()` was fixed in #328.", "`1000**11 - 1` still gives `1000.0 QB`", "stashing the fix needed approval" |

## Failures the design didn't name

| Failure | Where | Example |
|---|---|---|
| A note about the draft after the draft | 16 of 18 draft outputs (email-reply 2/3, email-decline 3/3, explain-concept 3/3, status-update 3/3, announce-change 3/3, article 2/3) | "I didn't name the person behind the hotfix, so the message is about the process and doesn't single anyone out." Sometimes useful (it flags a guess), usually not. |
| Invented detail | email-decline 1/3, article 1/3 | "I'm so glad you're writing again" (nothing says she stopped). Headline: "Its First Cut in Over a Year" (it was the first in over four years). |
| Decoration | status-update 2/3, announce-change 3/3 | "**⚠️ Decision needed**", "🔒", "Questions or concerns? Reply in the thread. 🙏". Bold on nearly every line. |
| Stock framing | article 2/3, announce-change 3/3 | "## The bottom line", "**Heads up:**" |

## What Opus already does well (the skill must not break these)

- Opens with the answer or the outcome, every time.
- Uses specific numbers and examples rather than adjectives.
- Says plainly what it did not check ("I couldn't confirm that the new tests fail on the old code").
- Defines a term for a general reader when the audience is clearly general: the articles explain the federal funds rate in one clause.
- Emails are honest about the constraint and ask the question the user wanted asked.

## Not a writing problem

In 2 of 3 status updates, Claude tried to publish the update as a web page using a tool built into Claude Code, and one reply printed that page's temporary file path. That tool is part of every clean setup, so it affects both arms equally. It is not in scope for the skill.

## What this means for the skill

Guidance goes only to failures that showed up: length that fits the question, prose over bold-label sections in messages, plain words before internal names, no stock phrases, no notes about the draft unless they flag a guess the user must check, no invented detail, no decoration.

No guidance for "point buried" or "repeating the question": neither showed up.

**Risk to the pass bar:** the baseline is already strong on the emails, the article and the announcement. On those tasks the judges may call ties, which would make "wins at least 8 of 10 tasks on Opus" hard to reach even if the skill helps. The clearest room for gains is quick-question, session-summary, mid-session-answer and explain-concept.
