---
name: deploy
description: Use when someone wants their own copy of the open coach app running. Walks SETUP.md step by step.
---

# Deploy your own copy

The coach app is open source (MIT): a web app on Netlify with a Supabase database. Each person or coach
runs their own copy under their own accounts. This skill walks them through the repo's `SETUP.md`; it
does not deploy anything for them.

## How to run it

1. **Get the current guide.** Open `SETUP.md` from the repo they are deploying (their fork, or
   `https://github.com/percyhendrux123-prog/coachapp`). Read it from the copy, not from memory; steps
   and setting names change between versions. Also read `COSTS.md` before they turn anything on.
2. **One step at a time.** Give one step, wait for them to say it is done or paste what they see, then
   the next. Name the exact screen and button. Plain words; they may not be a developer.
3. **Secrets stay with them.** They paste keys into Netlify and Supabase themselves. Never ask them to
   paste a secret key, service-role key, Stripe key or token into this chat, and never write one to a
   file. If one is pasted anyway, tell them to rotate it.
4. **Their accounts, their spend.** Any step that can cost money (a paid plan, a custom domain, an
   email sender, payments) is their decision; say what it costs according to `COSTS.md` and wait.
5. **Payments are optional.** The free self-serve plan needs no Stripe. If they want to charge, they
   set up their own Stripe products; you never create, change or test a live charge.
6. **Prove it works.** At the end: the site loads, they can sign in with the code the app emails them,
   and the connector answers. Then use the `axiom-coach:connect` skill with their site address and hand
   them the steps to connect Claude Code.

## Names

The code is MIT. The names and marks listed in the repo's `TRADEMARKS.md` are not licensed: their copy
needs its own name and logo, and must not suggest Deploy Axiom runs or endorses it. Mention this once,
when they pick a site name.
