"""`hermes axiom-coach setup` and `/axiom-coach`: print the connector steps for one site. Writes nothing.

The plugin never edits Hermes config, never stores a token and makes no network call. It prints
the commands (or the equivalent config block) for the person to run or paste themselves.
"""
import re
from urllib.parse import urlsplit

DEFAULT_NAME = "axiom-coach"
_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,39}$")
_LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}

USAGE = ("Usage: hermes axiom-coach setup <your app address> [--name <server name>]\n"
         "   or: /axiom-coach <your app address>\n"
         "Example: hermes axiom-coach setup https://your-coach-app.netlify.app\n"
         "Prints the steps to connect Hermes to your copy of the coach app. Writes nothing.")


def normalise_site(raw):
    """Return the site origin (scheme://host[:port]) or raise ValueError with a plain reason."""
    text = str(raw or "").strip()
    if not text:
        raise ValueError("Give the address of your running coach app, for example https://your-coach-app.netlify.app")
    if "://" not in text:
        text = "https://" + text
    parts = urlsplit(text)
    host = (parts.hostname or "").lower()
    if not host or any(c in text for c in " \t\n\"'`$\\"):
        raise ValueError("That does not look like a web address.")
    if parts.username or parts.password or parts.query or parts.fragment:
        raise ValueError("Use the plain site address, with no login, ? or # parts.")
    if parts.scheme == "http" and host not in _LOCAL_HOSTS:
        raise ValueError("Use https. Plain http is only accepted for a copy running on this computer (localhost).")
    if parts.scheme not in ("https", "http"):
        raise ValueError("Use an https:// address.")
    try:
        port = parts.port
    except ValueError:
        raise ValueError("That port number is not valid.") from None
    netloc = f"[{host}]" if ":" in host else host
    if port:
        netloc += f":{port}"
    return f"{parts.scheme}://{netloc}"


def render(site, name=DEFAULT_NAME):
    origin = normalise_site(site)
    if not _NAME_RE.match(name or ""):
        raise ValueError("Server name: lowercase letters, numbers, - or _, up to 40 characters.")
    url = f"{origin}/mcp"
    return f"""Axiom Coach: connect Hermes to {origin}
This prints steps only. Nothing was written to your Hermes config.

1. Add the server and mark it untrusted, so every write asks you first:
   hermes mcp add {name} --url {url} --auth oauth
   hermes config set mcp_servers.{name}.trust untrusted
   (hermes mcp add may open the sign-in page straight away; that is step 2.)

   Same thing as a config block, if you prefer to paste:
   mcp_servers:
     {name}:
       url: {url}
       auth: oauth
       trust: untrusted

2. Sign in:
   hermes mcp login {name}
   Your browser opens your app's "Connect your AI" page. Either sign in with your app email and
   the code it emails you, then choose what the agent may do (Read-only, or Full control on a
   self-serve plan), or paste a connector code you made in the app (coach: the AI tab in the
   coach console; self-serve: "Connect your own AI" in your app). A code is shown once.
   Hermes keeps the sign-in in its own token store (~/.hermes/mcp-tokens/); this plugin never sees it.

3. Restart Hermes (or start a new session). The app's tools appear as mcp_{name.replace('-', '_')}_*.
   Reads run on their own. Every write (a message, a logged set, a program change) waits for your yes,
   and in unattended runs (cron, hermes chat -q) a write is refused, not run.

Open the app: {origin}/
Put it on your Home Screen:
   iPhone: open it in Safari, tap Share, then Add to Home Screen.
   Android: open it in Chrome, tap the menu, then Add to Home screen (or Install app).
The home-screen app, a browser tab and a connected agent all read the same account.

Skills: hermes-axiom-coach:coach-desk, hermes-axiom-coach:my-plan, hermes-axiom-coach:deploy,
hermes-axiom-coach:lite. The Lite calculators (axiom_lite_split, axiom_lite_macros,
axiom_lite_cardio) run locally and need no app."""


def parse_args(raw):
    tokens = str(raw or "").split()
    if tokens and tokens[0] == "setup":
        tokens = tokens[1:]
    name, site = DEFAULT_NAME, None
    i = 0
    while i < len(tokens):
        if tokens[i] == "--name" and i + 1 < len(tokens):
            name = tokens[i + 1]
            i += 2
            continue
        if site is None:
            site = tokens[i]
        else:
            raise ValueError("Give one app address.")
        i += 1
    return site, name


def slash(raw=""):
    try:
        site, name = parse_args(raw)
        if not site or site in ("help", "-h", "--help"):
            return USAGE
        return render(site, name)
    except ValueError as exc:
        return f"{exc}\n\n{USAGE}"


def setup_cli(parser):
    sub = parser.add_subparsers(dest="axiom_coach_action")
    run = sub.add_parser("setup", help="Print the steps to connect Hermes to your coach app (writes nothing)")
    run.add_argument("site", nargs="?", help="Your app address, for example https://your-coach-app.netlify.app")
    run.add_argument("--name", default=DEFAULT_NAME, help="MCP server name to use in the printed steps")


def run_cli(args):
    if getattr(args, "axiom_coach_action", None) != "setup" or not getattr(args, "site", None):
        print(USAGE)
        return 0 if getattr(args, "axiom_coach_action", None) is None else 2
    try:
        print(render(args.site, args.name))
        return 0
    except ValueError as exc:
        print(f"{exc}\n\n{USAGE}")
        return 2
