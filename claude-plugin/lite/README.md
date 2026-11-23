# Axiom Coach Lite Tools for Claude Code

Three small calculators, as local tools for Claude Code: a training split, daily macro targets, and a cardio calorie estimate. They are the Lite calculators from the open Lite app, with the same rules and numbers, and they are the Claude Code counterpart of the three `axiom_lite_*` tools in [Axiom Coach for Hermes](https://github.com/percyhendrux123-prog/hermes-axiom-coach).

This is a **mod**: a few JavaScript functions that run inside Claude Code and answer the tool calls. It is not an MCP server. It is a separate plugin from `axiom-coach` (skills only) because a mod is code; read "Before you install" first.

Built by Deploy Axiom.

## What it adds

| Tool | What it does |
|---|---|
| `axiom_lite_split` | One starting week of training for 2-6 days a week, by equipment, swapping exercises that load a flagged injury |
| `axiom_lite_macros` | Daily calorie and macro targets (Mifflin-St Jeor) and a week of meal structure; five health questions first, any yes returns no numbers |
| `axiom_lite_cardio` | Estimated calories for one cardio session (MET tables, ACSM treadmill equations) |

Claude sees them as `mcp__axiom-coach-lite__axiom_lite_split`, `..._macros` and `..._cardio`. The plugin also carries one skill, `axiom-coach-lite:lite-tools`, which says how to call them and how to ask the health questions.

## Install

```
claude plugin marketplace add percyhendrux123-prog/hermes-axiom-coach
claude plugin install axiom-coach-lite@deploy-axiom-coach
```

If you install or update it while a session is open, run `/reload-plugins` there. To try it for one session without installing:

```
claude --plugin-dir ./claude-plugin/lite
```

## Before you install

A mod runs inside Claude Code with your permissions. Claude Code can list what this one does without running it:

```
claude plugin validate --strict claude-plugin/lite
```

The output lists `hooks:` (`session.start` and `tool.call`, filtered to this plugin's three tools) and `calls:` (`$.tool.register` only).

- **Files it reads:** its own source files at load. **Files it writes:** none.
- **Network, shell commands, subprocesses, background work, model calls, timers:** none.
- **State, stored credentials, telemetry, environment variables:** none.
- **Hooks used:** `session.start` registers the three tools. One `tool.call` hook per tool answers that tool's calls. No other event is hooked, so it cannot see, change or approve any other tool call or prompt.
- **Fails closed:** if a calculator ever throws (a bug, not bad input), the call returns a message saying no result was produced and not to work the numbers out another way.
- **Requires:** Claude Code 2.1.293 or later (mods need 2.1.287; the tools are loaded up front with `isDeferred: false`, which needs 2.1.293). Tested with 2.1.325. No other software.

Organizations can switch mods off (`disableAllHooks`, `--safe-mode`, managed settings). Then the tools do not load and the plugin does nothing. The skills-only `axiom-coach` plugin still carries the same calculators as written instructions.

## The health screen

`axiom_lite_macros` needs the person's own yes or no to five questions, word for word. A missing, partial or non-boolean screen is refused, never treated as "no". Any yes returns no targets, only a note to talk to a doctor or registered dietitian first. Claude is told never to answer a question for the person.

## Limits

- Results are estimates for general education, not medical advice. Every result carries that line. Nothing is saved and nothing syncs.
- Input limits are the Lite app's own (age 13-90, height 4 ft 0 in to 7 ft 11 in, weight 80-550 lb, incline 0-15 percent). Duration (1-600 minutes), speed (0.5-15 mph) and distance (0.1-100 miles) limits are this plugin's own, to catch typos.

## Known gaps

- **Mods do not run everywhere.** They run in the Claude Code terminal, the Desktop app's Code tab and the VS Code extension, but not in a WSL or SSH Desktop session. See Claude Code's page "Where mods run". Where they do not run, the tools are missing.
- **Directory.** Plugins with mods are not eligible for Anthropic's plugin directory unless the publisher is verified. This one ships from GitHub. The skills-only `axiom-coach` plugin is the directory edition.
- **Argument names.** Claude Code passes a tool call's arguments as fields of the event together with `tool` and `tool_use_id` (seen in a live run, not in the docs). The plugin ignores those two and refuses any other field it does not know, as the Hermes tools do. If a future Claude Code adds more event fields, a call may be refused with `unknown field(s)` until `META_FIELDS` in `hooks/engines/common.js` is updated.
- **No setup command and no connector skills here.** Those are in `axiom-coach`.

## Check it yourself

```
node --test claude-plugin/tests/
python3 -m unittest discover -s claude-plugin/tests
```

The JavaScript engines are run against `tests/fixtures/lite_parity.json`: 3,580 cases exported from the TypeScript engines of the open Lite app. They are also run against the Hermes plugin's Python tool handlers on a battery of valid and invalid inputs, comparing every answer and every refusal message. The data tables in `hooks/engines/data.js` and `schemas.js` are generated from the Python engines by `claude-plugin/tests/gen_lite_data.py`.

## Undo

Run `claude plugin uninstall axiom-coach-lite`, and if you added the marketplace, `claude plugin marketplace remove deploy-axiom-coach`. Nothing else was written.

## Works with

- The open Lite app: <https://github.com/percyhendrux123-prog/pkfit-lite-open>
- The skills-only `axiom-coach` plugin in the same marketplace

## Licence and names

Code: MIT, see `LICENSE`. Names and marks are not licensed: "Axiom", "Deploy Axiom", "Axiom Coach", "PKFIT", "PKFIT SYSTEM", "PKFIT LITE", "Operate Fitness", their logos, and Percy Keith's name and likeness. You may say your project is based on this one. You may not use those names or marks for your own product, service or hosted copy, or in a way that suggests we run or endorse it. This plugin is not affiliated with or endorsed by Anthropic.

## How it was made

I designed it, set the rules for what it may do and refuse, and tested it on my own system. AI agents wrote the code under my spec and review.

Percy Keith, Deploy Axiom. MIT license.
