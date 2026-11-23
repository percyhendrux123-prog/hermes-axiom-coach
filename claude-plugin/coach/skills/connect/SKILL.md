---
name: connect
description: Use when someone has a running copy of the open coach app and wants to connect Claude Code to it. Prints the connector steps for their app address; changes nothing.
---

# Connect Claude Code to your coach app

The open coach app has its own connector: an MCP server at `<your app address>/mcp`, with OAuth
sign-in. This plugin adds no copy of the app's tools. This skill gives the person the steps to connect
Claude Code to their own copy. It prints steps only. Do not run the commands for them, do not edit
their Claude Code settings, and do not ask for or handle any sign-in code or token.

## 1. Check the address

Ask for the address of their running app, for example `https://your-coach-app.netlify.app`. Turn it
into a plain origin, `https://host` with an optional port, and refuse anything else, saying why in
plain words:

- Use `https`. Plain `http` is accepted only for a copy running on the same computer
  (`localhost`, `127.0.0.1` or `::1`).
- No login (`user:password@`), no path, no `?` and no `#` part. Strip a trailing slash. If they gave a
  path such as `/mcp`, take the origin only.
- It must look like a web address: letters, numbers, dots and hyphens in the host, at least two parts
  (or `localhost`), or an IP address.

If there is no running copy yet, stop and offer the `axiom-coach:deploy` skill. Without a running app
only the Lite calculators are useful.

## 2. Give them these steps

Replace `<origin>` with the checked address.

1. Add the server (the name `axiom-coach` is a suggestion; lowercase letters, numbers, `-` or `_`, up to
   40 characters):

   ```
   claude mcp add --transport http axiom-coach <origin>/mcp
   ```

2. Sign in. In Claude Code run `/mcp`, choose `axiom-coach` and follow the sign-in, or run
   `claude mcp login axiom-coach` in a terminal. Their browser opens the app's "Connect your AI"
   page. Either sign in with the app email and the code it emails them, then choose what the agent may
   do (Read-only, or Full control on a self-serve plan), or paste a connector code made in the app
   (coach: the AI tab in the coach console; self-serve: "Connect your own AI" in their app). A code is
   shown once. Claude Code keeps the sign-in in its own store; this plugin never sees it.

3. Start a new session (or run `/reload-plugins` if they changed plugins, and `/mcp` to confirm the
   server shows as connected). The app's tools appear under the server's name, as
   `mcp__axiom-coach__<tool>`.

4. Writes (a message, a logged set, a program change) go through Claude Code's normal permission
   prompt. They decide what to allow; do not suggest allowing more than they ask for.

To undo: `claude mcp logout axiom-coach`, then `claude mcp remove axiom-coach`.

## 3. Open the app

The app itself is at `<origin>/`. To put it on a Home Screen:

- iPhone: open it in Safari, tap Share, then Add to Home Screen.
- Android: open it in Chrome, tap the menu, then Add to Home screen (or Install app).

The home-screen app, a browser tab and a connected agent all read the same account.

## 4. Then

- A coach works the desk with the `axiom-coach:coach-desk` skill.
- A self-serve member works their own plan with the `axiom-coach:my-plan` skill.
- The Lite calculators (skill `axiom-coach:lite`) need no app.
