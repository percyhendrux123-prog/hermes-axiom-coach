"""Python-side checks for the mod edition (claude-plugin/lite).

- the generated engine files match what the generator renders from the Python engines;
- for a battery of valid and invalid inputs, the JavaScript tools answer exactly what the Hermes
  plugin's Python tool handlers answer (same numbers, same refusals, same messages);
- the mod source calls nothing but `$.tool.register`: no network, files, processes or model.
Needs `node` on PATH for the battery; those tests skip with a plain message if it is missing.
"""
import itertools
import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / "claude-plugin" / "lite"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tests"))

import gen_lite_data  # noqa: E402
from _load import load_plugin  # noqa: E402

P = load_plugin()
NODE = shutil.which("node")

SCREEN = {k: False for k in P.tools.HEALTH_QUESTIONS}


def battery():
    cases = []
    for days, eq, inj in itertools.product((2, 3, 4, 5, 6), P.training_split.EQUIPMENT, ([], ["knee"], ["shoulder", "wrist"], ["lower_back", "hip", "knee"])):
        cases.append(("axiom_lite_split", {"days_per_week": days, "equipment": eq, "injuries": inj}))
    cases += [
        ("axiom_lite_split", {"days_per_week": 7, "equipment": "full_gym"}),
        ("axiom_lite_split", {"days_per_week": True, "equipment": "full_gym"}),
        ("axiom_lite_split", {"days_per_week": "3", "equipment": "full_gym"}),
        ("axiom_lite_split", {"days_per_week": 3, "equipment": "pool"}),
        ("axiom_lite_split", {"days_per_week": 3, "equipment": "full_gym", "injuries": ["elbow"]}),
        ("axiom_lite_split", {"days_per_week": 3, "equipment": "full_gym", "injuries": "knee"}),
        ("axiom_lite_split", {"days_per_week": 3, "equipment": "full_gym", "injuries": None}),
        ("axiom_lite_split", {"days_per_week": 3, "equipment": "full_gym", "injuries": ["knee", "knee"]}),
        ("axiom_lite_split", {"days_per_week": 3, "equipment": "full_gym", "surprise": 1}),
        ("axiom_lite_split", {}),
    ]
    base = {"sex": "female", "age_years": 34, "height_cm": 168, "weight_kg": 71.5, "activity_level": "moderate",
            "goal": "fat_loss", "health_screen": dict(SCREEN)}
    for sex, act, goal in itertools.product(("male", "female"), ("sedentary", "light", "moderate", "very_active"),
                                            ("fat_loss", "maintenance", "muscle_gain")):
        cases.append(("axiom_lite_macros", {**base, "sex": sex, "activity_level": act, "goal": goal}))
    cases += [
        ("axiom_lite_macros", {**base, "age_years": 13, "height_cm": 121.92, "weight_kg": 36.28738}),
        ("axiom_lite_macros", {**{k: v for k, v in base.items() if k != "height_cm"}, "height_ft": 5, "height_in": 10, "weight_lb": 165}),
        ("axiom_lite_macros", {**{k: v for k, v in base.items() if k != "height_cm"}, "height_ft": 7, "height_in": 11, "weight_lb": 550}),
        ("axiom_lite_macros", {**{k: v for k, v in base.items() if k != "height_cm"}, "height_ft": 3, "height_in": 11}),
        ("axiom_lite_macros", {**{k: v for k, v in base.items() if k != "height_cm"}, "height_ft": 5}),
        ("axiom_lite_macros", {**{k: v for k, v in base.items() if k != "height_cm"}, "height_in": 5}),
        ("axiom_lite_macros", {**base, "height_ft": 5, "height_in": 10}),
        ("axiom_lite_macros", {**{k: v for k, v in base.items() if k != "height_cm"}}),
        ("axiom_lite_macros", {**{k: v for k, v in base.items() if k != "weight_kg"}}),
        ("axiom_lite_macros", {**base, "weight_lb": 150}),
        ("axiom_lite_macros", {**base, "age_years": 12}),
        ("axiom_lite_macros", {**base, "age_years": 91}),
        ("axiom_lite_macros", {**base, "age_years": "30"}),
        ("axiom_lite_macros", {**base, "age_years": True}),
        ("axiom_lite_macros", {**base, "weight_kg": 36}),
        ("axiom_lite_macros", {**base, "weight_kg": 250}),
        ("axiom_lite_macros", {**base, "sex": "other"}),
        ("axiom_lite_macros", {**base, "goal": "bulk"}),
        ("axiom_lite_macros", {**base, "activity_level": "extreme"}),
        ("axiom_lite_macros", {k: v for k, v in base.items() if k != "health_screen"}),
        ("axiom_lite_macros", {**base, "health_screen": None}),
        ("axiom_lite_macros", {**base, "health_screen": {}}),
        ("axiom_lite_macros", {**base, "health_screen": {**SCREEN, "extra": False}}),
        ("axiom_lite_macros", {**base, "health_screen": {**SCREEN, "heart_condition": "no"}}),
        ("axiom_lite_macros", {**base, "health_screen": {**SCREEN, "heart_condition": 0}}),
        ("axiom_lite_macros", {**base, "unknown": 1}),
    ]
    for key in SCREEN:
        cases.append(("axiom_lite_macros", {**base, "health_screen": {**SCREEN, key: True}}))
    cardio_base = {"modality": "treadmill", "duration_minutes": 30, "intensity": "moderate", "weight_kg": 80}
    for mod, inten in itertools.product(P.cardio_calc.MODALITIES, P.cardio_calc.INTENSITIES):
        cases.append(("axiom_lite_cardio", {**cardio_base, "modality": mod, "intensity": inten}))
    for speed, incline in itertools.product((0.5, 2.5, 4.3, 4.31, 6, 9.9, 15), (None, 0, 1.5, 15)):
        args = {**cardio_base, "speed_mph": speed}
        if incline is not None:
            args["incline_percent"] = incline
        cases.append(("axiom_lite_cardio", args))
    cases += [
        ("axiom_lite_cardio", {**cardio_base, "distance_miles": 2.5, "incline_percent": 3}),
        ("axiom_lite_cardio", {**cardio_base, "distance_miles": 0.1, "duration_minutes": 1}),
        ("axiom_lite_cardio", {**cardio_base, "speed_mph": 3, "distance_miles": 9}),
        ("axiom_lite_cardio", {"modality": "rower", "duration_minutes": 20, "intensity": "high", "weight_lb": 200, "sex": "male", "height_ft": 6, "height_in": 1}),
        ("axiom_lite_cardio", {"modality": "rower", "duration_minutes": 20, "intensity": "high", "weight_lb": 200, "sex": "robot"}),
        ("axiom_lite_cardio", {"modality": "rower", "duration_minutes": 20, "intensity": "high", "weight_lb": 200, "height_cm": 100}),
        ("axiom_lite_cardio", {"modality": "rower", "duration_minutes": 20, "intensity": "high", "weight_kg": 80, "incline_percent": 1}),
        ("axiom_lite_cardio", {**cardio_base, "incline_percent": 16}),
        ("axiom_lite_cardio", {**cardio_base, "incline_percent": -1}),
        ("axiom_lite_cardio", {**cardio_base, "speed_mph": 0.4}),
        ("axiom_lite_cardio", {**cardio_base, "speed_mph": 16}),
        ("axiom_lite_cardio", {**cardio_base, "distance_miles": 101}),
        ("axiom_lite_cardio", {**cardio_base, "duration_minutes": 0.5}),
        ("axiom_lite_cardio", {**cardio_base, "duration_minutes": 601}),
        ("axiom_lite_cardio", {**cardio_base, "duration_minutes": "30"}),
        ("axiom_lite_cardio", {**cardio_base, "modality": "swim"}),
        ("axiom_lite_cardio", {**cardio_base, "intensity": "max"}),
        ("axiom_lite_cardio", {k: v for k, v in cardio_base.items() if k != "weight_kg"}),
        ("axiom_lite_cardio", {k: v for k, v in cardio_base.items() if k != "duration_minutes"}),
        ("axiom_lite_cardio", {**cardio_base, "mood": "good"}),
    ]
    return cases


class GeneratedFilesAreCurrent(unittest.TestCase):
    def test_engine_data_and_schemas_match_the_generator(self):
        for filename, fn in gen_lite_data.TARGETS:
            shipped = (MOD / "hooks" / "engines" / filename).read_text(encoding="utf-8")
            self.assertEqual(shipped, fn(), f"{filename} is stale: run claude-plugin/tests/gen_lite_data.py")


@unittest.skipUnless(NODE, "node is not on PATH")
class JavaScriptMatchesPythonTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = battery()
        proc = subprocess.run([NODE, str(HERE / "run_js_tools.mjs")], input=json.dumps([{"tool": t, "args": a} for t, a in cls.cases]),
                              capture_output=True, text=True, timeout=60)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr)
        cls.js = json.loads(proc.stdout)
        handlers = {name: handler for name, _schema, handler in P.tools.TOOLS}
        cls.py = [handlers[t](a) for t, a in cls.cases]

    def test_battery_is_not_trivial(self):
        self.assertGreater(len(self.cases), 200)
        errors = sum(1 for r in self.py if "error" in json.loads(r))
        self.assertGreater(errors, 40)
        self.assertGreater(len(self.cases) - errors, 140)

    def test_every_answer_matches(self):
        for (tool, args), js, py in zip(self.cases, self.js, self.py):
            self.assertEqual(json.loads(js), json.loads(py), f"{tool} {json.dumps(args)}")

    def test_every_answer_has_the_education_line(self):
        for js in self.js:
            self.assertEqual(json.loads(js)["education"], P.tools.EDUCATION_LINE)

    def test_key_order_matches_for_results(self):
        # The model reads the JSON as text; keep the same order as the Hermes tools.
        for js, py in zip(self.js, self.py):
            self.assertEqual(list(json.loads(js)), list(json.loads(py)))


class ModSourceIsNarrow(unittest.TestCase):
    SOURCES = sorted((MOD / "hooks").rglob("*.js"))

    def test_only_tool_register_is_called(self):
        calls = set()
        for src in self.SOURCES:
            calls |= set(re.findall(r"\$\.[A-Za-z]+\.[A-Za-z]+", src.read_text(encoding="utf-8")))
        self.assertEqual(calls, {"$.tool.register"})

    def test_no_network_files_processes_or_model_in_source(self):
        banned = ["fetch(", "XMLHttpRequest", "child_process", "require(", "node:fs", "readFile", "writeFile", "process.env",
                  "eval(", "new Function", "WebSocket", "$.http", "$.fs", "$.process", "$.model", "$.store", "$.state", "$.clock"]
        for src in self.SOURCES:
            text = src.read_text(encoding="utf-8")
            for token in banned:
                self.assertNotIn(token, text, f"{src.name} contains {token}")

    def test_only_the_expected_hooks_are_registered(self):
        events = re.findall(r"on\('([a-z.]+)'", (MOD / "hooks" / "register.js").read_text(encoding="utf-8"))
        self.assertEqual(events, ["session.start", "tool.call", "tool.call", "tool.call"])

    def test_plugin_holds_no_mcp_server_and_no_command_hooks(self):
        manifest = json.loads((MOD / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        for key in ("mcpServers", "hooks", "bin", "monitors"):
            self.assertNotIn(key, manifest)
        self.assertFalse((MOD / ".mcp.json").exists())
        hooks = json.loads((MOD / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        self.assertEqual(set(hooks), {"description", "modules"})
        self.assertEqual(hooks["modules"], ["./register.js"])

    def test_tool_names_match_the_hermes_tools_and_hooks(self):
        schemas = (MOD / "hooks" / "engines" / "schemas.js").read_text(encoding="utf-8")
        register = (MOD / "hooks" / "register.js").read_text(encoding="utf-8")
        for name, _schema, _handler in P.tools.TOOLS:
            self.assertIn(f'"name": "{name}"', schemas)
            self.assertIn(f"mcp__axiom-coach-lite__{name}", register)


if __name__ == "__main__":
    unittest.main()
