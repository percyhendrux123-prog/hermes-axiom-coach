# Connector check (build step 4.5.1), v0.1.0

Question: can Hermes connect straight to the coach app's own connector, with OAuth, and does Hermes
hold back write tools on a server marked untrusted? Checked against Hermes Agent v0.23.1 and a live
hosted copy of the app (host shown below as `<app host>`).

## 1. The app's connector advertises standard OAuth 2.1

`GET https://<app host>/.well-known/oauth-protected-resource`

```json
{"resource": "https://<app host>/mcp", "authorization_servers": ["https://<app host>"],
 "bearer_methods_supported": ["header"], "scopes_supported": ["mcp", "offline_access"]}
```

`GET https://<app host>/.well-known/oauth-authorization-server`

```json
{"issuer": "https://<app host>", "authorization_endpoint": "https://<app host>/oauth/authorize",
 "token_endpoint": "https://<app host>/oauth/token", "registration_endpoint": "https://<app host>/oauth/register",
 "response_types_supported": ["code"], "grant_types_supported": ["authorization_code", "refresh_token"],
 "code_challenge_methods_supported": ["S256"], "token_endpoint_auth_methods_supported": ["none"],
 "scopes_supported": ["mcp", "offline_access"]}
```

An unauthenticated `POST /mcp` returns `401` with
`www-authenticate: Bearer resource_metadata="https://<app host>/.well-known/oauth-protected-resource"`.

## 2. Hermes's own OAuth client completes discovery and registration

In a throwaway `HERMES_HOME` with this config:

```yaml
mcp_servers:
  axiom-coach:
    url: https://<app host>/mcp
    auth: oauth
    trust: untrusted
```

`hermes mcp login axiom-coach` printed:

```
Starting OAuth flow for 'axiom-coach'...
  MCP OAuth: authorization required.
  Open this URL in your browser:
    https://<app host>/oauth/authorize?response_type=code&client_id=coaching-mcp-<issued by DCR>&redirect_uri=http%3A%2F%2F127.0.0.1%3A27890%2Fcallback&state=<random>&code_challenge=<S256 of a random verifier>&code_challenge_method=S256&resource=https%3A%2F%2F<app host>%2Fmcp&scope=mcp+offline_access&prompt=consent
```

So Hermes found both metadata documents, registered itself through the app's
`/oauth/register` (the `client_id` comes from the app), and built a PKCE S256 request with the
resource indicator. `GET` on that authorize URL returned `200` with the app's "Connect your AI" page
(email sign-in, or paste a connector code). The sign-in itself needs a person, so it stopped there.

## 3. Header mode already runs in production

A long-running Hermes install connects to a hosted copy of this app as an HTTP MCP server with a
connector token in a header and `trust: untrusted`; its tools are discovered and used every day.

## 4. The trust rule for write tools

From Hermes v0.23.1 (`tools/mcp_tool_handlers.py`, docs `reference/mcp-config-reference.md`, key
`trust`): on a `trust: untrusted` server every tool call without a `readOnlyHint: true` annotation
needs approval before the request is sent (Allow Once, Session, Always). Where nobody can answer
(cron, `hermes chat -q`, a gateway with no approver) the approval fails closed and the call is not
run. `/yolo` and `approvals.mode: off` skip the prompt. The app annotates its tools with
`readOnlyHint` (checked by `supabase/functions/mcp/toolAnnotations.test.js` in the app repo), so reads
run freely and writes ask.

## 5. The health screen cannot be answered through the connector

The app has no connector tool that records clearance. `system-clearance` refuses connector tokens
before anything runs, and `regenerate_my_plan` refuses while the person's latest health screen is on
hold. Checked by reading the app source at its public commit.

## Result

Hermes connects to the app's connector directly. No plugin-side HTTP tools are needed, and the plugin
stores no token.

## Not exercised here

- A full OAuth sign-in followed by a tool call (needs a person to sign in).
- A model-driven Hermes session using the plugin (the throwaway home has no model credentials).
- A local copy of the app with fixture data (no local database stack was started for this check).
