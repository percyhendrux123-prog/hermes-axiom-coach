"""hermes-axiom-coach: the Hermes side of the open coach app, the self-serve plan and the Lite calculators.

What it registers (public plugin surfaces only):
  - tools axiom_lite_split, axiom_lite_macros, axiom_lite_cardio (local math, no network, no files)
  - skills hermes-axiom-coach:coach-desk, :my-plan, :deploy, :lite (read-only instructions)
  - CLI `hermes axiom-coach setup <site>` and slash `/axiom-coach <site>` (print steps, write nothing)
No hooks, no stored tokens, no background work. The coach app's own tools come from the app's
connector through Hermes's built-in MCP client, not from this plugin.
"""
from pathlib import Path

from . import setup_cmd
from .lite.tools import TOOLS

ROOT = Path(__file__).resolve().parent
SKILLS = ("coach-desk", "my-plan", "deploy", "lite")


def _frontmatter_description(path):
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        for line in text.split("---", 2)[1].splitlines():
            if line.startswith("description:"):
                return line.split(":", 1)[1].strip().strip('"')
    return ""


def register(ctx):
    for name, schema, handler in TOOLS:
        ctx.register_tool(name=name, toolset="axiom-coach", schema=schema, handler=handler,
                          description=schema["description"])
    for skill in SKILLS:
        path = ROOT / "skills" / skill / "SKILL.md"
        ctx.register_skill(skill, path, description=_frontmatter_description(path))
    ctx.register_command("axiom-coach", setup_cmd.slash, args_hint="<your app address>",
                         description="Print the steps to connect Hermes to your coach app. Writes nothing.")
    ctx.register_cli_command(name="axiom-coach", help="Axiom Coach: print connector setup steps (writes nothing)",
                             setup_fn=setup_cmd.setup_cli, handler_fn=setup_cmd.run_cli,
                             description="Print the steps to connect Hermes to your own coach app.")
