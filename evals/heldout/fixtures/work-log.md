## work log — BILL-2314 (invoice totals off by a penny w/ % discount + tax-inclusive pricing)

**mon**
- repro'd from Zara's ticket: customer in tax-inclusive region, 15% discount code, 3 line items. PDF total £84.99, order confirmation email says £85.00. one of them is lying
- confirmation email uses `checkout/summary.py::build_order_summary()`, PDF uses `billing/invoice.py::render_invoice_totals()`. two separate totals paths?? yes. great
- both eventually call `billing/totals.py::apply_discount()` but in a different order relative to `compute_line_tax()`
  - summary: discount on the gross line total, then back out tax
  - invoice: back out tax per line, discount the net, then re-add tax
- rounding happens per line in the invoice path (`round_half_up` in `money.py`) and only once at the end in the summary path. that's the penny

**tue**
- wrote `tests/billing/test_invoice_totals.py::test_percent_discount_tax_inclusive_matches_summary` — fails, £84.99 vs £85.00. good, that's the bug in a test
- first try: moved rounding in `render_invoice_totals()` to the end like summary does. fixes my new test BUT breaks 4 tests in `test_invoice_lines.py` that assert per-line tax amounts shown on the PDF. those are legit — finance wants per-line tax visible and each line has to round on its own (Amir confirmed, it's a compliance thing in some regions)
- reverted that
- second try: keep per-line rounding for display, but compute the invoice grand total the summary way and put any rounding difference on a "rounding adjustment" line. Amir says finance HATES rounding adjustment lines, needs sign-off from Lorna. parked, branch `bill-2314-rounding-line` (not pushed... actually pushed, just not PR'd)

**wed (today)**
- third idea: make the summary path match the invoice instead (round per line). then email == PDF. smaller blast radius? but changes what customers see at checkout by a penny on some orders, and `test_checkout_summary.py::test_summary_total_snapshot` has ~30 snapshot cases that'd need regenerating. didn't want to regen snapshots without someone agreeing
- spent an hour on a red herring: thought `Decimal` context precision was different between the two paths. it's not, both use the default from `money.py`. ignore
- also found fixed-amount discounts (£5 off) don't have the bug — only percent. didn't dig into why yet, probably because fixed is applied once to the order not per line
- STILL FAILING: `test_percent_discount_tax_inclusive_matches_summary` on main. my branch `bill-2314-wip` has the test + some logging in `apply_discount()` — strip the logging before merging

**for whoever picks this up**
- need a decision first: option 2 (rounding line, needs Lorna) or option 3 (change checkout, needs product to OK the snapshot change). I lean 3
- Zara's customer is waiting, she's told them "end of week"
