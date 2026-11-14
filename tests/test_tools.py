"""Tool wrappers, registration and the setup command."""
import json
import unittest
from pathlib import Path

from _load import ROOT, load_plugin

P = load_plugin()
T = P.tools
EDU = T.EDUCATION_LINE
NO_SCREEN = {k: False for k in T.HEALTH_QUESTIONS}


def call(fn, args):
    return json.loads(fn(args))


class EducationLine(unittest.TestCase):
    def test_every_result_and_refusal_carries_it(self):
        results = [
            call(T.split, {"days_per_week": 3, "equipment": "full_gym"}),
            call(T.split, {"days_per_week": 9, "equipment": "full_gym"}),
            call(T.macros, {"sex": "male", "age_years": 30, "height_cm": 180, "weight_kg": 85,
                            "activity_level": "moderate", "goal": "maintenance", "health_screen": NO_SCREEN}),
            call(T.macros, {"sex": "male", "age_years": 30, "height_cm": 180, "weight_kg": 85,
                            "activity_level": "moderate", "goal": "maintenance",
                            "health_screen": {**NO_SCREEN, "pregnant_or_nursing": True}}),
            call(T.macros, {}),
            call(T.cardio, {"modality": "rower", "weight_kg": 80, "duration_minutes": 30, "intensity": "low"}),
            call(T.cardio, {"modality": "rower"}),
            call(T.split, None),
            call(T.split, "not an object"),
        ]
        for r in results:
            self.assertEqual(r["education"], EDU, r)
        self.assertIn("pregnant", EDU)
        self.assertIn("not medical advice", EDU)


class Split(unittest.TestCase):
    def test_matches_engine(self):
        r = call(T.split, {"days_per_week": 5, "equipment": "bodyweight_only", "injuries": ["shoulder", "shoulder"]})
        self.assertEqual(r["splitName"], "Push / Pull / Legs + Upper / Lower")
        self.assertEqual(len(r["days"]), 5)
        self.assertTrue(any(e.get("notes") == "Substituted for flagged injury." for d in r["days"] for e in d["exercises"]))

    def test_refuses_bad_input(self):
        bad = [
            {"days_per_week": 1, "equipment": "full_gym"},
            {"days_per_week": 7, "equipment": "full_gym"},
            {"days_per_week": True, "equipment": "full_gym"},
            {"days_per_week": "3", "equipment": "full_gym"},
            {"days_per_week": 3, "equipment": "kettlebells"},
            {"days_per_week": 3, "equipment": "full_gym", "injuries": ["neck"]},
            {"days_per_week": 3, "equipment": "full_gym", "injuries": "knee"},
            {"days_per_week": 3, "equipment": "full_gym", "extra": 1},
        ]
        for args in bad:
            self.assertIn("error", call(T.split, args), args)


BASE = {"sex": "female", "age_years": 28, "height_ft": 5, "height_in": 5, "weight_lb": 132,
        "activity_level": "light", "goal": "fat_loss", "health_screen": NO_SCREEN}


class Macros(unittest.TestCase):
    def test_imperial_converts_like_the_web_app(self):
        r = call(T.macros, BASE)
        cm = (5 * 12 + 5) * 2.54
        kg = 132 * 0.45359237
        expect = P.meal_plan.calculate_macros("female", 28, cm, kg, "light", "fat_loss")
        self.assertEqual(r["macros"], expect)
        self.assertFalse(r["blocked"])

    def test_any_yes_blocks_with_no_numbers(self):
        for key in T.HEALTH_QUESTIONS:
            r = call(T.macros, {**BASE, "health_screen": {**NO_SCREEN, key: True}})
            self.assertTrue(r["blocked"], key)
            self.assertNotIn("macros", r)
            self.assertIn("health professional", r["reason"])

    def test_health_screen_must_be_complete_and_boolean(self):
        partial = dict(NO_SCREEN)
        partial.pop("eating_disorder")
        for screen in (None, {}, partial, {**NO_SCREEN, "heart_condition": "no"},
                       {**NO_SCREEN, "heart_condition": 0}, {**NO_SCREEN, "extra": False}):
            args = {**BASE, "health_screen": screen}
            if screen is None:
                args.pop("health_screen")
            r = call(T.macros, args)
            self.assertIn("error", r, screen)
            self.assertNotIn("macros", r)

    def test_ranges_follow_the_web_form(self):
        cases = [
            {"age_years": 12}, {"age_years": 91}, {"weight_lb": 79}, {"weight_lb": 551},
            {"height_ft": 3}, {"height_ft": 8}, {"height_in": 12}, {"height_in": -1},
            {"age_years": float("nan")}, {"age_years": True}, {"weight_lb": "150"},
        ]
        for patch in cases:
            self.assertIn("error", call(T.macros, {**BASE, **patch}), patch)
        for patch in ({"age_years": 13}, {"age_years": 90}, {"weight_lb": 80}, {"weight_lb": 550},
                      {"height_ft": 4, "height_in": 0}, {"height_ft": 7, "height_in": 11}):
            self.assertNotIn("error", call(T.macros, {**BASE, **patch}), patch)

    def test_metric_and_imperial_cannot_mix(self):
        self.assertIn("error", call(T.macros, {**BASE, "weight_kg": 60}))
        self.assertIn("error", call(T.macros, {**BASE, "height_cm": 165}))
        no_height = {k: v for k, v in BASE.items() if k not in ("height_ft", "height_in")}
        self.assertIn("error", call(T.macros, no_height))

    def test_unknown_choices_refused(self):
        for patch in ({"sex": "other"}, {"goal": "bulk"}, {"activity_level": "extreme"}):
            self.assertIn("error", call(T.macros, {**BASE, **patch}), patch)

    def test_huge_integers_are_refused_not_raised(self):
        # Review R1 finding 2: math.isfinite(10**400) raised OverflowError past the guard.
        r = call(T.macros, {**BASE, "age_years": 10 ** 400})
        self.assertIn("error", r)
        self.assertEqual(r["education"], EDU)
        r = call(T.cardio, {"modality": "rower", "weight_kg": 10 ** 400, "duration_minutes": 30, "intensity": "low"})
        self.assertIn("error", r)
        r = call(T.cardio, {"modality": "rower", "weight_kg": 80, "duration_minutes": -(10 ** 400), "intensity": "low"})
        self.assertIn("error", r)


class Cardio(unittest.TestCase):
    def test_treadmill_distance_path(self):
        r = call(T.cardio, {"modality": "treadmill", "weight_kg": 80, "duration_minutes": 30,
                            "intensity": "moderate", "distance_miles": 2.5})
        self.assertEqual(r, json.loads(json.dumps({**P.cardio_calc.calculate_cardio_calories(
            "treadmill", "moderate", 80, 30, None, 2.5, None), "education": EDU})))

    def test_refuses_bad_input(self):
        base = {"modality": "treadmill", "weight_kg": 80, "duration_minutes": 30, "intensity": "low"}
        for patch in ({"duration_minutes": 0}, {"duration_minutes": 601}, {"incline_percent": 16},
                      {"incline_percent": -1}, {"speed_mph": 0}, {"speed_mph": 16}, {"distance_miles": 0},
                      {"modality": "swim"}, {"intensity": "max"}, {"modality": "rower", "incline_percent": 2},
                      {"weight_kg": 30}, {"sex": "x"}, {"note": "hi"}):
            self.assertIn("error", call(T.cardio, {**base, **patch}), patch)
        no_weight = dict(base)
        no_weight.pop("weight_kg")
        self.assertIn("error", call(T.cardio, no_weight))


class FakeCtx:
    def __init__(self):
        self.tools, self.skills, self.commands, self.cli, self.hooks = {}, {}, {}, {}, []

    def register_tool(self, name, toolset, schema, handler, **kw):
        self.tools[name] = (toolset, schema, handler)

    def register_skill(self, name, path, description=""):
        self.skills[name] = (Path(path), description)

    def register_command(self, name, handler, **kw):
        self.commands[name] = handler

    def register_cli_command(self, name, help, setup_fn, handler_fn=None, description=""):
        self.cli[name] = (setup_fn, handler_fn)

    def register_hook(self, *a, **kw):
        self.hooks.append(a)


class Registration(unittest.TestCase):
    def setUp(self):
        self.ctx = FakeCtx()
        P.register(self.ctx)

    def test_surfaces(self):
        self.assertEqual(set(self.ctx.tools), {"axiom_lite_split", "axiom_lite_macros", "axiom_lite_cardio"})
        for name, (_, schema, _) in self.ctx.tools.items():
            self.assertEqual(schema["name"], name)
            self.assertFalse(schema["parameters"]["additionalProperties"])
        self.assertEqual(set(self.ctx.skills), {"coach-desk", "my-plan", "deploy", "lite"})
        for path, desc in self.ctx.skills.values():
            self.assertTrue(path.is_file())
            self.assertTrue(desc)
        self.assertEqual(set(self.ctx.commands), {"axiom-coach"})
        self.assertEqual(set(self.ctx.cli), {"axiom-coach"})
        self.assertEqual(self.ctx.hooks, [], "v0.1 ships no hooks")

    def test_manifest_matches_registrations(self):
        text = (ROOT / "plugin.yaml").read_text()
        for name in self.ctx.tools:
            self.assertIn(name, text)
        self.assertIn("provides_hooks: []", text)


class Setup(unittest.TestCase):
    def test_prints_steps_for_a_site(self):
        out = P.setup.slash("https://my-coach.example.com/")
        self.assertIn("hermes mcp add axiom-coach --url https://my-coach.example.com/mcp --auth oauth", out)
        self.assertIn("trust: untrusted", out)
        self.assertIn("hermes mcp login axiom-coach", out)
        self.assertIn("Add to Home Screen", out)
        self.assertIn("Nothing was written", out)
        self.assertIn("mcp__axiom_coach__*", out)  # Hermes names MCP tools mcp__<server>__<tool>

    def test_bare_host_and_name(self):
        out = P.setup.slash("setup my-coach.example.com --name coach2")
        self.assertIn("--url https://my-coach.example.com/mcp", out)
        self.assertIn("mcp_servers.coach2.trust", out)

    def test_refuses_unsafe_addresses(self):
        for raw in ("", "http://my-coach.example.com", "https://u:p@x.example.com", "https://x.example.com/?a=1",
                    "ftp://x.example.com", "https://x.example.com; rm -rf ~", "https://x.example.com --name BAD NAME"):
            out = P.setup.slash(raw)
            self.assertIn("Usage:", out, raw)
            self.assertNotIn("hermes mcp add", out, raw)

    def test_localhost_http_allowed(self):
        self.assertIn("--url http://localhost:8888/mcp", P.setup.slash("http://localhost:8888"))

    def test_no_shell_metacharacters_reach_the_printed_commands(self):
        # Review R1 finding 1: a host like "example.com;id;" used to be printed unquoted.
        for raw in ("https://example.com;id;", "https://example.com|id", "https://ex$(id).com", "https://ex`id`.com",
                    "https://example.com&id", "https://exa mple.com", "https://example.com>x", "https://ex'a.com",
                    "https://-bad.example.com", "https://example..com", "https://exämple.com", "https://example",
                    "https://example.com\nid", "https://example.com\rid"):
            out = P.setup.slash(raw)
            self.assertNotIn("hermes mcp add", out, repr(raw))
        with self.assertRaises(ValueError):
            P.setup.render("https://example.com", "coach\n")
        with self.assertRaises(ValueError):
            P.setup.render("https://example.com", "coach;id")

    def test_ip_and_ipv6_hosts(self):
        self.assertIn("--url https://203.0.113.5/mcp", P.setup.slash("https://203.0.113.5"))
        self.assertIn("--url 'http://[::1]:8888/mcp'", P.setup.slash("http://[::1]:8888"))

    def test_writes_nothing(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as home:
            before = sorted(os.listdir(home))
            old = os.environ.get("HERMES_HOME")
            os.environ["HERMES_HOME"] = home
            try:
                P.setup.slash("https://my-coach.example.com")
            finally:
                if old is None:
                    os.environ.pop("HERMES_HOME")
                else:
                    os.environ["HERMES_HOME"] = old
            self.assertEqual(sorted(os.listdir(home)), before)

    def test_no_network_or_file_writes_in_source(self):
        banned = ("urllib.request", "requests", "http.client", "socket", "subprocess", "open(", "write_text", "os.system")
        for path in list(ROOT.glob("*.py")) + list((ROOT / "lite").glob("*.py")):
            src = path.read_text()
            for word in banned:
                self.assertNotIn(word, src, f"{path.name}: {word}")


class Skills(unittest.TestCase):
    def test_health_rule_is_in_the_plan_and_lite_skills(self):
        for skill in ("my-plan", "lite", "coach-desk"):
            text = (ROOT / "skills" / skill / "SKILL.md").read_text().lower()
            self.assertIn("health screen", text, skill)
            self.assertIn("never", text, skill)

    def test_no_price_or_coaching_upsell(self):
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            text = path.read_text()
            for word in ("$", "price", "PKFIT", "upgrade", "buy "):
                self.assertNotIn(word, text, f"{path.parent.name}: {word}")


if __name__ == "__main__":
    unittest.main()
