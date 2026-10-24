notes for weekly update - week of 9 march
- csv export: done, merged tue. handles the 50k row case now (was timing out). sam reviewed
- pdf export: blocked. the rendering lib drops non-latin fonts. tried 2 workarounds, neither good. need decision: switch lib (approx 1 wk) or ship latin-only first?
- login bug (users logged out after 10 min) - root cause was token refresh using wrong clock. fixed, in staging, prod thurs
- onboarding emails: copy approved by marketing. sending starts 23 mar
- hiring: 2 interviews this week for backend role, 1 more next week
- me out fri 20 mar
- infra cost up 18% this month, mostly the new search cluster. looking at smaller instance size
