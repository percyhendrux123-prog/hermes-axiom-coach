"""MET-based cardio calorie estimate.

Python port of the Lite engine ``cardioCalc.ts``: the ACSM walking/running equations for a
treadmill with a speed (or a distance and a duration), otherwise a fixed MET by modality and
self-reported intensity. Estimates only, not a medical-grade measurement.
"""
from .meal_plan import js_round

MODALITIES = ("treadmill", "elliptical", "stationary_bike", "stair_climber", "rower")
INTENSITIES = ("low", "moderate", "high")
MPH_TO_M_PER_MIN = 26.8224
WALK_RUN_THRESHOLD_MPH = 4.3

MET_TABLE = {
    "elliptical": {"low": 4.6, "moderate": 5.0, "high": 7.0},
    "stationary_bike": {"low": 3.5, "moderate": 6.8, "high": 10.5},
    "stair_climber": {"low": 4.0, "moderate": 8.0, "high": 9.8},
    "rower": {"low": 3.5, "moderate": 7.0, "high": 12.0},
}
TREADMILL_INTENSITY_MET = {"low": 3.5, "moderate": 6.0, "high": 9.8}
DISCLAIMER = "Estimate only, based on standard MET formulas. Not a medical-grade measurement."


def calculate_treadmill_met(speed_mph, incline_percent):
    speed = speed_mph * MPH_TO_M_PER_MIN
    grade = incline_percent / 100
    if speed_mph <= WALK_RUN_THRESHOLD_MPH:
        vo2 = 0.1 * speed + 1.8 * speed * grade + 3.5
    else:
        vo2 = 0.2 * speed + 0.9 * speed * grade + 3.5
    return vo2 / 3.5


def resolve_effective_speed_mph(duration_minutes, speed_mph=None, distance_miles=None):
    if speed_mph is not None:
        return speed_mph
    if distance_miles is not None and duration_minutes > 0:
        return distance_miles / (duration_minutes / 60)
    return None


def resolve_met(modality, intensity, duration_minutes, speed_mph=None, distance_miles=None, incline_percent=None):
    speed = resolve_effective_speed_mph(duration_minutes, speed_mph, distance_miles)
    if modality == "treadmill" and speed is not None:
        return calculate_treadmill_met(speed, incline_percent if incline_percent is not None else 0)
    if modality == "treadmill":
        return TREADMILL_INTENSITY_MET[intensity]
    return MET_TABLE[modality][intensity]


def calculate_cardio_calories(modality, intensity, weight_kg, duration_minutes,
                              speed_mph=None, distance_miles=None, incline_percent=None):
    """Same contract as ``calculateCardioCalories``. Inputs must already be validated."""
    met = resolve_met(modality, intensity, duration_minutes, speed_mph, distance_miles, incline_percent)
    calories = js_round((met * 3.5 * weight_kg * duration_minutes) / 200)
    return {"met": js_round(met * 10) / 10, "caloriesBurned": calories, "disclaimer": DISCLAIMER}
