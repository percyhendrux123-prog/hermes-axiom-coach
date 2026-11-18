# End-to-end check after 0.1.0 (OAuth sign-in, app tool call, skills session)

Run 2026-11-17 against Hermes Agent v0.23.1 and the plugin at `505892ab` (the commit the catalog pins).
The 0.1.0 release listed two things as not observed. Both are now observed. The run also found one
defect in 0.1.0, fixed in 0.1.1.

## Result in one table

| Item | Status |
|---|---|
| Install from the catalog entry by bare name, pinned commit | Observed |
| Full OAuth sign-in in a browser (PKCE, local callback) | Observed: `✓ Authenticated — 76 tool(s) available` |
| An app tool call through Hermes after that sign-in | Observed: `list_programs`, 2 rows |
| Model-driven session that loads a skill and calls an `axiom_lite_*` tool | Observed (skill `lite`, tool `axiom_lite_macros`) |
| Model-driven session using `coach-desk` against the signed-in app | Observed **with the 0.1.1 fix**; at `505892ab` the app tools were hidden (section 4) |
| Model-driven session using `my-plan` (self-serve member sign-in) | **Not observed** |
| A write through the approval prompt | **Not observed** (read-only connector code, by design of this run) |

## 1. The account used

A demo coach workspace on the hosted copy of the app, seeded with synthetic data (three seed client
rows, two programs, no linked client logins). No real client data was read. The coach made a
read-only connector code on the app's AI screen for this run.

## 2. OAuth sign-in

In a throwaway `HERMES_HOME` whose config held only:

```yaml
mcp_servers:
  axiom-coach:
    url: https://<app address>/mcp
    auth: oauth
    trust: untrusted
```

`hermes mcp login axiom-coach` opened the app's authorize page. The coach pasted the connector code
on that page himself; the agent did not type or see it. Hermes received the callback and printed
`✓ Authenticated — 76 tool(s) available`. Afterwards:

```
$ hermes mcp test axiom-coach
  Transport: HTTP → https://<app address>/mcp
  Auth: OAuth 2.0
  ✓ Connected (1196ms)
  ✓ Tools discovered: 76
```

The first attempt timed out: the coach typed an email into the email box, which is the self-serve
member path. A coach's email is not accepted there. The README wording was the cause (section 5).

## 3. One read-only app tool call through Hermes

Called through Hermes's own tool registry (`discover_mcp_tools()` then
`registry.dispatch("mcp__axiom_coach__list_programs", {})`), no model involved:

```
registered: 76 | has list_programs: True
call ms: 390 | return type: str
{"result": [ 2 items, each:
  {"id": str, "name": str, "is_default": bool, "origin": str,
   "days": int, "exercises": int, "archived_at": null} ]}
```

Shape only; values left out.

## 4. Model-driven coach-desk session, and the defect it found

**At `505892ab` (0.1.0) the session could not reach the app tools.** The plugin registered its three
Lite tools under the toolset name `axiom-coach`. The setup command tells the user to name the
connector `axiom-coach` too. Hermes resolves a toolset name before a server name, so with both
present the name pointed at the three Lite tools and the connector's 76 tools were left out of every
model session:

```
platform toolsets: ['axiom-coach', 'browser', ...]
axiom-coach      -> 3  ['axiom_lite_cardio', 'axiom_lite_macros', 'axiom_lite_split']
mcp-axiom-coach  -> 76 ['mcp__axiom_coach__add_brief_slide', ...]     (not in the platform set)
```

The model loaded `coach-desk`, found no `mcp__axiom_coach__*` tools, and correctly said the connector
was not set up. Anyone who installed 0.1.0 and followed its own setup steps would hit this.

**Fix (0.1.1): the Lite toolset is renamed `axiom-lite`.** One line in `__init__.py`, plus a test that
the toolset never equals the connector's default name. With the fix:

```
axiom-coach      -> 76 ['mcp__axiom_coach__add_brief_slide', ...]
```

and the same prompt ran end to end. The model loaded `coach-desk` and `lite`, called
`mcp__axiom_coach__get_support_queue` and `mcp__axiom_coach__list_programs`, then `axiom_lite_macros`,
and reported counts only (3 seed clients needing attention, 2 programs) with the education line the
Lite skill requires. No write tool was called. Transcript excerpt: `coach-desk-session-v0.1.x.txt`.
The earlier Lite-only session is in `skills-session-v0.1.x.txt`.

How the session got a model: the throwaway home was copied into a temporary Hermes profile so it
could use the machine's model sign-in read-only; the plugin was installed there from the catalog
entry (`505892ab`), then patched with the one-line fix for the passing run.

## 5. README finding, now confirmed by a real user

The README said to sign in "with your app email and the emailed code, or paste a connector code".
The email path is for self-serve members; a coach has to paste a connector code. A real coach took
the email path first and the login timed out. README corrected in 0.1.1.

## 6. Cleanup

- Temporary profile and throwaway home deleted, including Hermes's stored connector tokens.
- The app's connector publishes no token revocation endpoint, so the connector code is revoked by
  the coach on the app's AI screen.
- The machine's own Hermes config and plugins were not changed.

## 7. Noted, not tested

The read-only demo sign-in was offered all 76 tools, including write tools and two platform-level
list tools. Offered is not the same as allowed; none of these were called, so whether the server
refuses them for this sign-in was not observed here.

## Proposed known_issues text for the catalog entry (0.1.1)

> 0.1.0 named its Lite toolset like the connector it tells you to add, which hid the app's tools from
> model sessions; fixed in 0.1.1 (toolset `axiom-lite`). Observed on 0.1.1: full OAuth sign-in, an app
> tool call, and a model-driven coach-desk session on a demo workspace. Not observed: a my-plan
> session with a self-serve member sign-in, and a write through the approval prompt.
