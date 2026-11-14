"""Parity: the Python engines must return exactly what the TypeScript engines return.

The fixture is produced from the real TypeScript files (see fixtures/export_fixture.ts) and
covers every input used by the Lite app's 44 vitest cases plus a wider grid: every split size x
equipment x injury combination, 672 macro inputs, 2,268 cardio inputs.
"""
import json
import unittest
from pathlib import Path

from _load import load_plugin

P = load_plugin()
FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "lite_parity.json").read_text())


class TrainingParity(unittest.TestCase):
    def test_every_case_matches(self):
        cases = FIXTURE["training"]
        self.assertEqual(len(cases), 640)
        for case in cases:
            i = case["input"]
            got = P.training_split.generate_training_program(i["daysPerWeek"], i["equipment"], i["injuries"])
            self.assertEqual(got, case["output"], i)


class MealParity(unittest.TestCase):
    def test_every_case_matches(self):
        cases = FIXTURE["meal"]
        self.assertEqual(len(cases), 672)
        for case in cases:
            i = case["input"]
            args = (i["sex"], i["ageYears"], i["heightCm"], i["weightKg"], i["activityLevel"], i["goal"])
            self.assertEqual(P.meal_plan.calculate_macros(*args), case["macros"], i)
            self.assertEqual(P.meal_plan.generate_meal_plan(*args, i["healthFlags"]), case["output"], i)


class CardioParity(unittest.TestCase):
    def test_every_case_matches(self):
        cases = FIXTURE["cardio"]
        self.assertGreater(len(cases), 2000)
        for case in cases:
            i = case["input"]
            got = P.cardio_calc.calculate_cardio_calories(
                i["modality"], i["intensity"], i["weightKg"], i["durationMinutes"],
                i.get("speedMph"), i.get("distanceMiles"), i.get("inclinePercent"))
            self.assertEqual(got, case["output"], i)


class JsRound(unittest.TestCase):
    def test_halves_round_up_like_javascript(self):
        r = P.meal_plan.js_round
        self.assertEqual([r(0.5), r(1.5), r(2.5), r(-0.5), r(-1.5), r(2.4999)], [1, 2, 3, 0, -1, 2])


if __name__ == "__main__":
    unittest.main()
