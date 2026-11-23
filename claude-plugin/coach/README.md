# Axiom Coach for Claude Code

Axiom Coach is a small Claude Code plugin made only of skills. It is the Claude Code counterpart of [Axiom Coach for Hermes](https://github.com/percyhendrux123-prog/hermes-axiom-coach), and it works with the same three open projects: a coach app, its free self-serve plan, and the Lite calculators.

- **Coach app and self-serve plan.** The app already has its own connector (an MCP server at `<your site>/mcp`, OAuth sign-in). This plugin adds no copy of its tools. It ships the skills that tell Claude how to work there, and a skill that prints the connector steps for your site.
- **Lite.** The three Lite calculators are written out as step-by-step instructions, with the same numbers and rules as the open Lite app. No account, no network, nothing saved.

Built by Deploy Axiom.

## What it adds

All five are skills. Claude loads one when the task matches.

| Skill | What it does |
|---|---|
| `axiom-coach:coach-desk` | Work a coach's desk through the connector: read-only pass first, every send drafted and waiting for the coach |
| `axiom-coach:my-plan` | Work your own self-serve plan: read, log, adjust; never answers the health screen |
| `axiom-coach:connect` | Prints the steps to connect Claude Code to your own copy of the app. Changes nothing |
| `axiom-coach:deploy` | Walks someone through `SETUP.md` to run their own copy of the app |
| `axiom-coach:lite` | The training split, macro and cardio rules, with the five health questions asked first |

## Install

```
claude plugin marketplace add percyhendrux123-prog/hermes-axiom-coach
claude plugin install axiom-coach@deploy-axiom-coach
```

To try it for one session without installing, point Claude Code at the plugin folder:

```
claude --plugin-dir ./claude-plugin/coach
```

Then, if you run the coach app, ask Claude to connect it to your app address (the `connect` skill prints the steps). In short: `claude mcp add --transport http axiom-coach <site>/mcp`, then sign in with `/mcp` or `claude mcp login axiom-coach` (a coach pastes a connector code made on the app's AI screen; a self-serve member uses their app email and the emailed code).

## Limits

- The coach and self-serve parts need a running copy of the coach app (your own, or one someone hosts for you). Without one, only the `lite` and `deploy` skills are useful.
- Lite results are estimates for general education, not medical advice. Every result carries that line. Nothing is saved and nothing syncs for Lite; for a plan that follows you between phone and computer, use the self-serve plan.
- Claude cannot answer anyone's health screen or confirm a doctor's clearance. The skills say so and the app's server refuses it.
- Claude Code keeps the connector sign-in in its own store. This plugin never sees or stores it.

## Known gaps

This is a port of the Hermes plugin, and it is not the same thing. Differences, from reading both:

- **The Lite calculators are instructions, not code.** In the Hermes plugin they are local tools that return exact results, checked against 3,580 cases from the Lite app. Here Claude does the arithmetic itself from the written rules, so a slip is possible. The skill tells it to show each step. For exact results, install the separate `axiom-coach-lite` plugin from the same marketplace (see below).
- **No setup command.** Hermes has `hermes axiom-coach setup <site>` and `/axiom-coach <site>`. Here the `connect` skill gives the same steps, written for Claude Code's `claude mcp` commands. It cannot be run as a command.
- **Writes are not set to refuse in unattended runs.** Hermes marks the connector `trust: untrusted`, so a write asks first and is refused in cron or `hermes chat -q`. Claude Code uses its own permission prompt, which follows your permission mode and rules. The skills still require a drafted message and a yes from the coach before any write.
- **Connector sign-in was not tested end to end.** The app's OAuth endpoint is standard, and Claude Code supports OAuth for remote MCP servers, but I did not sign in to a live app from Claude Code for this release.
- **Tested with Claude Code 2.1.325.** The skills are plain Markdown and should work on newer versions.

## Lite tools as a separate plugin

`axiom-coach-lite` in the same marketplace runs the three calculators as local tools through a mod. It is separate because a mod is code that runs inside Claude Code, and this plugin is deliberately skills only. See its README.

```
claude plugin install axiom-coach-lite@deploy-axiom-coach
```

## Before you install

- **Files it reads:** its own skill files when Claude loads one. **Files it writes:** none.
- **Network at runtime:** none from the plugin. Connector traffic is Claude Code's own MCP client, set up by you.
- **Scripts, hooks, MCP servers, subprocesses, background work, model calls:** none. Stored credentials, telemetry: none.
- **Requires:** Claude Code. No other software.

## Undo

Run `claude plugin uninstall axiom-coach`, and if you added the marketplace, `claude plugin marketplace remove deploy-axiom-coach`. If you connected the app, `claude mcp logout axiom-coach` then `claude mcp remove axiom-coach`.

## Check it yourself

```
claude plugin validate --strict --profile directory claude-plugin/coach
python3 -m unittest discover -s claude-plugin/tests
```

The tests check that the numbers and tables in the skills match the Python engines, and that the skills-only edition holds no scripts, hooks or servers.

## Works with

- The open coach app: <https://github.com/percyhendrux123-prog/coachapp>
- The open Lite app: <https://github.com/percyhendrux123-prog/pkfit-lite-open>

## Licence and names

Code: MIT, see `LICENSE`. Names and marks are not licensed: "Axiom", "Deploy Axiom", "Axiom Coach", "PKFIT", "PKFIT SYSTEM", "PKFIT LITE", "Operate Fitness", their logos, and Percy Keith's name and likeness. You may say your project is based on this one. You may not use those names or marks for your own product, service or hosted copy, or in a way that suggests we run or endorse it. This plugin is not affiliated with or endorsed by Anthropic.

## How it was made

I designed it, set the rules for what it may say and refuse, and tested it on my own system. AI agents wrote the files under my spec and review.

Percy Keith, Deploy Axiom. MIT license.
