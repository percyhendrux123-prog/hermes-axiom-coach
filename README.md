# Axiom Coach for Hermes

`hermes-axiom-coach` is the Hermes side of three open projects: a coach app, its free self-serve
plan, and the Lite calculators.

- **Coach app and self-serve plan.** The app already has its own connector (an MCP server at
  `<your site>/mcp`, OAuth sign-in). Hermes connects to it with its built-in MCP client. This plugin
  adds no duplicate app tools. It ships the skills that tell the agent how to work there, and a setup
  command that prints the connector steps for your site.
- **Lite.** The three Lite calculators run inside Hermes as local tools: no account, no network.

Built by Deploy Axiom.

## What it adds

| Kind | Name | What it does |
|---|---|---|
| Tool | `axiom_lite_split` | One starting week of training for 2-6 days a week, by equipment, swapping exercises that load a flagged injury |
| Tool | `axiom_lite_macros` | Daily calorie and macro targets (Mifflin-St Jeor) and a week of meal structure; five health questions first, any yes returns no numbers |
| Tool | `axiom_lite_cardio` | Estimated calories for one cardio session (MET tables, ACSM treadmill equations) |
| Skill | `hermes-axiom-coach:coach-desk` | Work a coach's desk through the connector: read-only pass first, every send drafted and waiting for the coach |
| Skill | `hermes-axiom-coach:my-plan` | Work your own self-serve plan: read, log, adjust; never answers the health screen |
| Skill | `hermes-axiom-coach:deploy` | Walk someone through `SETUP.md` to run their own copy of the app |
| Skill | `hermes-axiom-coach:lite` | How to use the three calculators and their health questions |
| CLI | `hermes axiom-coach setup <site>` | Prints the connector steps and app links for your site. Writes nothing |
| Slash | `/axiom-coach <site>` | Same as the CLI, inside a chat |

## Install

```bash
hermes plugins install percyhendrux123-prog/hermes-axiom-coach --ref <commit sha>
hermes plugins enable hermes-axiom-coach
```

Then, if you run the coach app:

```bash
hermes axiom-coach setup https://your-coach-app.example.com
```

and follow the printed steps. In short: `hermes mcp add axiom-coach --url <site>/mcp --auth oauth`,
`hermes config set mcp_servers.axiom-coach.trust untrusted`, `hermes mcp login axiom-coach` (sign in on
your app's page with your app email and the emailed code, or paste a connector code made in the app),
then restart Hermes.

`trust: untrusted` is the point: reads run on their own, a write (a message, a logged set, a program
change) asks you first, and in unattended runs (cron, `hermes chat -q`) it is refused. The exceptions
are yours to choose: answering Session or Always for a tool, `/yolo`, or `approvals.mode: off` skip the
question (see Hermes's MCP `trust` setting).

## Limits

- The coach and self-serve parts need a running copy of the coach app (your own, or one someone hosts
  for you). Without one, only the Lite tools and the deploy skill are useful.
- Lite results are estimates for general education, not medical advice. Every result carries that
  line. Nothing is saved and nothing syncs for Lite; for a plan that follows you between phone and
  computer, use the self-serve plan.
- The agent cannot answer anyone's health screen or confirm a doctor's clearance. The skills say so and
  the app's server refuses it.
- Hermes keeps the connector sign-in in its own token store. This plugin never sees or stores it.

## Disclosures

- **Hermes surfaces used:** `ctx.register_tool` (three tools, toolset `axiom-coach`),
  `ctx.register_skill` (four bundled read-only skills), `ctx.register_command` (`/axiom-coach`),
  `ctx.register_cli_command` (`hermes axiom-coach`). No hooks, no middleware, no dashboard or Desktop half.
- **Files read:** its own four `SKILL.md` files at load time. **Files written:** none.
- **Network:** none from the plugin. The connector traffic is Hermes's own MCP client, set up by you.
- **Shell commands, subprocesses, background work, model calls:** none.
- **Credentials:** none read, none stored. No environment variables required. No telemetry.

## Verification

```bash
python3 -m unittest discover -s tests -v
hermes plugins validate . --install-deps
hermes plugins doctor . --ci
```

`tests/test_parity.py` runs the Python engines against `tests/fixtures/lite_parity.json`: 3,580 cases
exported from the TypeScript engines of the open Lite app (every input its 44 tests use, every split
size x equipment x injury combination, and grids of macro and cardio inputs). The exporter is
`tests/fixtures/export_fixture.ts`. Recorded outputs are in `docs/evidence/`.

## Works with

- The open coach app: <https://github.com/percyhendrux123-prog/coachapp>
- The open Lite app: <https://github.com/percyhendrux123-prog/pkfit-lite-open>
- Hermes Agent 0.23.1 or later

## Licence and names

Code: MIT, see `LICENSE`. Names and marks are not licensed; see `TRADEMARKS.md`. This plugin is not
affiliated with or endorsed by Nous Research.
