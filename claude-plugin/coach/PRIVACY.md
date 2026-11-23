# Privacy: Axiom Coach plugin for Claude

Applies to the `axiom-coach` plugin in `claude-plugin/coach` (skills only). Last updated 2026-11-23.

## What the plugin is
A set of written instructions (skills) that Claude loads when relevant. It contains no scripts, hooks, MCP servers, background processes or network code.

## Data the plugin handles
- **Collects:** nothing. The plugin has no code that runs, so it cannot collect, send or store data.
- **Reads:** when you connect your own coach app through its connector, Claude may read records from that app (for example a client's name, plan or check-in) while following these skills. That reading is done by Claude through the connector you set up, under your own permission settings.
- **Stores:** nothing. The plugin writes no files and keeps no copy of anything it reads.
- **Shares:** nothing. The plugin sends no data to Deploy Axiom or any other party. Connector traffic goes only between Claude and the app you connected.
- **Credentials:** connector sign-in is held by Claude in its own store. The plugin never sees it.
- **Retention:** none by the plugin. Your coach app and Claude keep data under their own policies.

## Health information
The calculators give general estimates, not medical advice. The skills stop and point to a doctor when the health screen calls for it.

## Contact
Questions or issues: https://github.com/percyhendrux123-prog/hermes-axiom-coach/issues
