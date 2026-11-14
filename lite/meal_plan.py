"""Macro targets and a one-week meal structure.

Python port of the Lite engine ``mealPlan.ts``: Mifflin-St Jeor BMR, activity factor,
flat goal adjustment, a calorie floor by sex, then protein, fat and carbs from the final
calorie number. No model calls. Arithmetic follows the TypeScript operation order exactly
so results match to the last bit; ``js_round`` copies JavaScript's ``Math.round``.
"""
import math

SEXES = ("male", "female")
ACTIVITY_FACTORS = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "very_active": 1.725}
GOAL_ADJUSTMENT_KCAL = {"fat_loss": -500, "maintenance": 0, "muscle_gain": 300}
PROTEIN_G_PER_KG = 2.1
FAT_FLOOR_G_PER_KG = 0.5
FAT_FLOOR_PCT_OF_CALORIES = 0.25
CALORIE_FLOOR = {"female": 1300, "male": 1600}
MEAL_SPLIT = ("Meal 1", "Meal 2", "Meal 3", "Snack")
MEAL_DESCRIPTION = "Lean protein source + complex carbohydrate + vegetables (portion to hit daily macro targets)."

BLOCKED_REASON = (
    "We can't safely auto-generate a nutrition plan based on what you told us. Please consult a "
    "qualified health professional before starting a calorie or macro plan."
)
DISCLAIMER = "Estimates based on the Mifflin-St Jeor equation. Not medical advice. Adjust based on real-world progress."


def js_round(x):
    """JavaScript Math.round: halves round toward positive infinity (Python's round() does not)."""
    return math.floor(x + 0.5)


def calculate_bmr(sex, weight_kg, height_cm, age_years):
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age_years
    return base + 5 if sex == "male" else base - 161


def calculate_macros(sex, age_years, height_cm, weight_kg, activity_level, goal):
    bmr = calculate_bmr(sex, weight_kg, height_cm, age_years)
    tdee = bmr * ACTIVITY_FACTORS[activity_level]
    adjusted = tdee + GOAL_ADJUSTMENT_KCAL[goal]
    floored = max(adjusted, CALORIE_FLOOR[sex])
    calories = js_round(floored / 10) * 10

    protein_g = js_round(weight_kg * PROTEIN_G_PER_KG)
    fat_from_weight = weight_kg * FAT_FLOOR_G_PER_KG
    fat_from_calories = (calories * FAT_FLOOR_PCT_OF_CALORIES) / 9
    fat_g = js_round(max(fat_from_weight, fat_from_calories))

    remaining = calories - protein_g * 4 - fat_g * 9
    carbs_g = max(0, js_round(remaining / 4))
    return {"calories": calories, "proteinG": protein_g, "fatG": fat_g, "carbsG": carbs_g}


def _week():
    return [
        {"dayLabel": f"Day {i}", "meals": [{"label": label, "description": MEAL_DESCRIPTION} for label in MEAL_SPLIT]}
        for i in range(1, 8)
    ]


def generate_meal_plan(sex, age_years, height_cm, weight_kg, activity_level, goal, health_flags):
    """Same contract as ``generateMealPlan``: any health flag blocks the plan entirely."""
    if health_flags:
        return {"blocked": True, "reason": BLOCKED_REASON}
    return {
        "blocked": False,
        "macros": calculate_macros(sex, age_years, height_cm, weight_kg, activity_level, goal),
        "days": _week(),
        "disclaimer": DISCLAIMER,
    }
