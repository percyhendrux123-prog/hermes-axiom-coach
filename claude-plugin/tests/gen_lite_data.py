"""Emit the data tables of the mod edition (`lite/hooks/engines/data.js`) from the Python engines.

The tables are copied by machine, not by hand, so a typo cannot get in. `test_lite_mod.py` checks
the shipped file against `render()` and runs the JavaScript engines against the same 3,580-case
parity fixture the Python engines are checked against.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lite import cardio_calc as cc, meal_plan as mp, tools as lite_tools, training_split as ts  # noqa: E402

HEADER = (
    "// Generated from lite/training_split.py, lite/meal_plan.py and lite/cardio_calc.py by\n"
    "// claude-plugin/tests/gen_lite_data.py. Do not edit by hand; run the generator.\n"
    "// Numbers and tables are those of the open Lite app's engines (trainingSplit.ts, mealPlan.ts,\n"
    "// cardioCalc.ts).\n"
)


def _const(name, value):
    return f"export const {name} = {json.dumps(value, indent=2)}\n"


def render():
    exercise = {
        pattern: {**{tier: [[n, list(a)] for n, a in table[tier]] for tier in ts.EQUIPMENT}, "safe": table["safe"]}
        for pattern, table in ts.EXERCISE_TABLE.items()
    }
    split = {str(days): {"name": name, "days": templates} for days, (name, templates) in ts.SPLIT_TABLE.items()}
    parts = [
        HEADER,
        _const("EQUIPMENT", list(ts.EQUIPMENT)),
        _const("INJURIES", list(ts.INJURIES)),
        _const("DAYS_PER_WEEK", list(ts.DAYS_PER_WEEK)),
        _const("SPLIT_DISCLAIMER", ts.DISCLAIMER),
        _const("SUBSTITUTED_NOTE", ts.SUBSTITUTED_NOTE),
        _const("EXERCISE_TABLE", exercise),
        _const("SPLIT_TABLE", split),
        _const("SEXES", list(mp.SEXES)),
        _const("ACTIVITY_FACTORS", mp.ACTIVITY_FACTORS),
        _const("GOAL_ADJUSTMENT_KCAL", mp.GOAL_ADJUSTMENT_KCAL),
        _const("PROTEIN_G_PER_KG", mp.PROTEIN_G_PER_KG),
        _const("FAT_FLOOR_G_PER_KG", mp.FAT_FLOOR_G_PER_KG),
        _const("FAT_FLOOR_PCT_OF_CALORIES", mp.FAT_FLOOR_PCT_OF_CALORIES),
        _const("CALORIE_FLOOR", mp.CALORIE_FLOOR),
        _const("MEAL_SPLIT", list(mp.MEAL_SPLIT)),
        _const("MEAL_DESCRIPTION", mp.MEAL_DESCRIPTION),
        _const("BLOCKED_REASON", mp.BLOCKED_REASON),
        _const("MEAL_DISCLAIMER", mp.DISCLAIMER),
        _const("MODALITIES", list(cc.MODALITIES)),
        _const("INTENSITIES", list(cc.INTENSITIES)),
        _const("MPH_TO_M_PER_MIN", cc.MPH_TO_M_PER_MIN),
        _const("WALK_RUN_THRESHOLD_MPH", cc.WALK_RUN_THRESHOLD_MPH),
        _const("MET_TABLE", cc.MET_TABLE),
        _const("TREADMILL_INTENSITY_MET", cc.TREADMILL_INTENSITY_MET),
        _const("CARDIO_DISCLAIMER", cc.DISCLAIMER),
    ]
    return "\n".join(parts)


def render_schemas():
    """The three tool declarations, from the Hermes plugin's schemas (parameters become inputSchema)."""
    parts = [HEADER]
    for name, schema, _handler in lite_tools.TOOLS:
        const = name.upper().replace("AXIOM_LITE_", "") + "_TOOL"
        decl = {"name": schema["name"], "description": schema["description"], "inputSchema": schema["parameters"]}
        parts.append(_const(const, decl))
    return "\n".join(parts)


TARGETS = (
    ("data.js", render),
    ("schemas.js", render_schemas),
)

if __name__ == "__main__":
    for filename, fn in TARGETS:
        target = ROOT / "claude-plugin" / "lite" / "hooks" / "engines" / filename
        target.write_text(fn(), encoding="utf-8")
        print(f"wrote {target}")
