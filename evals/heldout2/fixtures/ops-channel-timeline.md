#ops-incidents export — Mon 12 Oct
(pasted from the channel + radio log, tidied a bit by me — Rhiannon)

**05:52** — Depot B control (radio): driver on the 7 says passengers' app tickets coming up "Ticket cannot be verified" on the validator. Assumed one-off, told driver to accept visual check.

**06:05** — 3 more reports, routes 7, 12, 31. Control phones on-call engineer (Dariusz). No answer.

**06:11** — Control tries Dariusz again + texts. No answer. (turned out phone on DND, the on-call override had been switched off in the phone update — not his fault, we've checked)

**06:20ish** — Customer service inbox starting to get emails. Social media mentions: "app's broken, driver won't let me on". Approx 40 mentions by 06:45.

**06:24** — Control rings duty manager (Ellen). Ellen authorises "accept all app tickets on sight" — instruction goes out on radio to Depot A drivers.

**06:24–07:50** — ⚠️ instruction NOT relayed to Depot B. Depot B radio desk was single-staffed, controller was dealing with a breakdown on the A61 (separate thing). Some Depot B drivers refused passengers or asked them to pay cash. We know of at least 2 schoolchildren left at the Holloway Lane stop on route 31 (complaint from parent, now with customer services, Jordan handling). 

**06:40** — Ellen escalates to IT manager (Precious) via personal mobile. Precious online 06:52.

**07:03** — Precious: validator API returning TLS handshake errors. Checks cert on validate.riderydale.example — **expired 00:00 Mon 12 Oct.**

**07:15** — Social post goes out: "We're aware of a problem with mobile tickets this morning. Please show your ticket to the driver and you will be allowed to travel." Pinned.

**07:20** — Some customers also can't open the app ticket wallet at all (white screen). Others fine. Precious thinks it depends on whether ticket was cached on phone. So people who bought tickets this morning were worst hit.

**07:50** — Depot B finally gets the accept-on-sight instruction. Supervisor goes out to Holloway Lane + Market Square stops.

**08:10** — Precious can't renew cert through usual route — auto-renewal has been failing since the domain was moved to the new hosting account in August. Renewal reminder emails were going to Tobias's old mailbox (left in July). Nobody saw them.

**08:30** — Dariusz online (saw texts). Works with Precious on manual renewal.

**09:12** — New cert issued and installed on validator API.

**09:20** — Validators coming back but some on-bus units still caching the old failed state, need a reboot. Drivers told to power cycle at next terminus.

**09:41** — All validators confirmed OK. App wallet loading for everyone.

**10:00** — Social post: resolved. Apology.

---

Numbers (from Precious + Jordan, as of Weds):
- approx 4,300 journeys made with app tickets between 05:30 and 09:41 (normal Monday)
- of those, no way to know exactly how many people were refused or paid twice. Customer service has 212 contacts so far about Monday. 63 asking for refunds (people who paid cash on top of having a ticket). Refunds being processed — approx £180 so far
- 1 formal complaint re: the schoolchildren. Parent also contacted the local paper (not run yet as far as we know)
- no data was lost or exposed. it was purely the certificate. (Precious wants this said clearly as people on social media were saying we'd been hacked)

What we're doing / have done (Precious's list, I've added some):
- cert now on auto-renewal again, tested
- renewal reminders now go to the shared it@ mailbox not a person
- added the cert expiry date to the monthly IT checklist
- on-call phone: Dariusz's phone fixed; we're going to get a dedicated on-call phone instead of using personal ones (cost ~£25/month)
- Depot B radio desk — Ellen looking at having 2 people on 05:30–08:00 weekdays. not agreed yet, cost implication
- "accept on sight" to become standing instruction in driver handbook for any ticket system failure, so drivers don't need to wait for control
- refunds — anyone who paid twice gets it back + a free day ticket. Agreed by Gareth Tuesday

Gareth wants this to go to the board (meeting 23rd) AND the passenger panel. Neither are techy. Board will want to know is it going to happen again + what it cost us.
