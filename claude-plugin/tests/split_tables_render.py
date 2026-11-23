"""Render the split reference tables for the skills-only edition from the Python engine data.

The reference file shipped in the skill (`skills/lite/references/split-tables.md`) is generated
by `render()` and checked byte for byte against it in `test_skills.py`, so the instructions Claude
follows cannot drift from the engine the open Lite app's parity fixture was checked against.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lite import training_split as ts  # noqa: E402

TIERS = ("full_gym", "home_gym_basic", "dumbbells_only", "bodyweight_only")


def _cand(name, avoid):
    if not avoid:
        return f"{name} (never skipped)"
    return f"{name} (skip if {' or '.join(avoid)} is flagged)"


def render():
    out = [
        "# Training split tables",
        "",
        "Source of truth for the `axiom-coach:lite` skill. Same rules as the open Lite app's training split.",
        "",
        "## How an exercise is chosen",
        "",
        "For each slot in a training day, look up its pattern and the person's equipment below. Take the",
        "candidates in the order listed and use the first one that is not skipped by a flagged injury. If",
        "every candidate is skipped, use the fallback for that pattern and add the note",
        f"`{ts.SUBSTITUTED_NOTE}` to that exercise. A later candidate chosen after an earlier one was",
        "skipped carries no note; only the fallback does.",
        "",
        "## Exercises by pattern and equipment",
        "",
    ]
    for pattern, table in ts.EXERCISE_TABLE.items():
        out.append(f"### {pattern}")
        out.append("")
        for tier in TIERS:
            cands = "; ".join(f"{i}. {_cand(n, a)}" for i, (n, a) in enumerate(table[tier], 1))
            out.append(f"- {tier}: {cands}")
        out.append(f"- fallback (all tiers): {table['safe']}")
        out.append("")
    out += ["## Split by days per week", ""]
    for days, (split_name, templates) in ts.SPLIT_TABLE.items():
        out.append(f"### {days} days a week: {split_name}")
        out.append("")
        for index, day in enumerate(templates, 1):
            slots = ", ".join(f"{s['pattern']} {s['sets']} x {s['reps']}" for s in day["slots"])
            out.append(f"- Day {index} ({day['focus']}): {slots}")
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


if __name__ == "__main__":
    target = ROOT / "claude-plugin" / "coach" / "skills" / "lite" / "references" / "split-tables.md"
    target.write_text(render(), encoding="utf-8")
    print(f"wrote {target}")
