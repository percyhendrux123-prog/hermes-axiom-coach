"""The three Lite calculators as Hermes tools: axiom_lite_split, axiom_lite_macros, axiom_lite_cardio.

Local only: no network, no files, no state. Each handler validates its input, converts
imperial units at the boundary exactly as the Lite web app does (``units.ts``), calls the
engine, and returns JSON. Every result, including a refusal, carries EDUCATION_LINE.
"""
import json
import math

from . import cardio_calc, meal_plan, training_split

EDUCATION_LINE = (
    "General education, not medical advice. If you are pregnant, have a medical condition, take "
    "medication, or have a history of an eating disorder, talk to a doctor or registered dietitian "
    "before changing how you eat."
)

CM_PER_INCH = 2.54
KG_PER_LB = 0.45359237

# Bounds copied from the Lite web app's input fields (MealPlanGenerator.tsx, CardioCalculator.tsx):
# age 13-90, height 4 ft 0 in to 7 ft 11 in, weight 80-550 lb, duration at least 1 minute,
# incline 0-15 percent. The web app sets no upper bound on duration, speed or distance; the
# limits marked PLUGIN below are this plugin's own, to refuse obvious typos.
AGE_RANGE = (13, 90)
HEIGHT_FT_RANGE = (4, 7)
HEIGHT_IN_RANGE = (0, 11)
HEIGHT_CM_RANGE = (4 * 12 * CM_PER_INCH, (7 * 12 + 11) * CM_PER_INCH)
WEIGHT_LB_RANGE = (80, 550)
WEIGHT_KG_RANGE = (80 * KG_PER_LB, 550 * KG_PER_LB)
DURATION_RANGE = (1, 600)        # PLUGIN upper bound
INCLINE_RANGE = (0, 15)
SPEED_RANGE = (0.5, 15)          # PLUGIN
DISTANCE_RANGE = (0.1, 100)      # PLUGIN

# The five health questions in the Lite macro calculator, word for word.
HEALTH_QUESTIONS = {
    "heart_condition": "Has a doctor ever told you that you have a heart condition?",
    "chest_pain_during_activity": "Do you have chest pain during physical activity?",
    "pregnant_or_nursing": "Are you currently pregnant or nursing?",
    "eating_disorder": "Do you have a diagnosed eating disorder, current or in recovery?",
    "metabolic_medication": "Are you on medication that affects metabolism, heart rate, or blood sugar?",
}


class InputError(ValueError):
    pass


def _number(args, key, lo, hi, required=True):
    value = args.get(key)
    if value is None:
        if required:
            raise InputError(f"{key} is required")
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise InputError(f"{key} must be a number")
    if value < lo or value > hi:
        raise InputError(f"{key} must be between {_fmt(lo)} and {_fmt(hi)}")
    return value


def _fmt(x):
    return f"{x:g}" if isinstance(x, float) else str(x)


def _choice(args, key, options):
    value = args.get(key)
    if value not in options:
        raise InputError(f"{key} must be one of: {', '.join(map(str, options))}")
    return value


def _only(args, allowed):
    if not isinstance(args, dict):
        raise InputError("arguments must be an object")
    extra = sorted(set(args) - set(allowed))
    if extra:
        raise InputError(f"unknown field(s): {', '.join(extra)}")


def _height_cm(args):
    has_cm = args.get("height_cm") is not None
    has_ft = args.get("height_ft") is not None or args.get("height_in") is not None
    if has_cm and has_ft:
        raise InputError("give height_cm or height_ft + height_in, not both")
    if has_cm:
        return _number(args, "height_cm", *HEIGHT_CM_RANGE)
    if has_ft:
        feet = _number(args, "height_ft", *HEIGHT_FT_RANGE)
        inches = _number(args, "height_in", *HEIGHT_IN_RANGE)
        return (feet * 12 + inches) * CM_PER_INCH
    return None


def _weight_kg(args):
    has_kg = args.get("weight_kg") is not None
    has_lb = args.get("weight_lb") is not None
    if has_kg and has_lb:
        raise InputError("give weight_kg or weight_lb, not both")
    if has_kg:
        return _number(args, "weight_kg", *WEIGHT_KG_RANGE)
    if has_lb:
        return _number(args, "weight_lb", *WEIGHT_LB_RANGE) * KG_PER_LB
    raise InputError("weight_kg or weight_lb is required")


def _ok(payload):
    payload["education"] = EDUCATION_LINE
    return json.dumps(payload)


def _refuse(message):
    return json.dumps({"error": message, "education": EDUCATION_LINE})


def _guard(fn):
    def handler(args, **_kwargs):
        try:
            return fn(args if args is not None else {})
        except InputError as exc:
            return _refuse(str(exc))
    handler.__name__ = fn.__name__
    return handler


@_guard
def split(args):
    _only(args, ("days_per_week", "equipment", "injuries"))
    days = args.get("days_per_week")
    if isinstance(days, bool) or days not in training_split.DAYS_PER_WEEK:
        raise InputError("days_per_week must be one of: 2, 3, 4, 5, 6")
    equipment = _choice(args, "equipment", training_split.EQUIPMENT)
    injuries = args.get("injuries", [])
    if not isinstance(injuries, list) or any(i not in training_split.INJURIES for i in injuries):
        raise InputError(f"injuries must be a list drawn from: {', '.join(training_split.INJURIES)}")
    return _ok(training_split.generate_training_program(days, equipment, list(dict.fromkeys(injuries))))


@_guard
def macros(args):
    _only(args, ("sex", "age_years", "height_cm", "height_ft", "height_in", "weight_kg", "weight_lb",
                 "activity_level", "goal", "health_screen"))
    sex = _choice(args, "sex", meal_plan.SEXES)
    age = _number(args, "age_years", *AGE_RANGE)
    height = _height_cm(args)
    if height is None:
        raise InputError("height_cm or height_ft + height_in is required")
    weight = _weight_kg(args)
    activity = _choice(args, "activity_level", tuple(meal_plan.ACTIVITY_FACTORS))
    goal = _choice(args, "goal", tuple(meal_plan.GOAL_ADJUSTMENT_KCAL))
    screen = args.get("health_screen")
    if not isinstance(screen, dict) or set(screen) != set(HEALTH_QUESTIONS) \
            or any(not isinstance(v, bool) for v in screen.values()):
        raise InputError("health_screen needs all five answers as true or false, given by the person: "
                         + "; ".join(f"{k}: {q}" for k, q in HEALTH_QUESTIONS.items()))
    result = meal_plan.generate_meal_plan(sex, age, height, weight, activity, goal, any(screen.values()))
    return _ok(result)


@_guard
def cardio(args):
    _only(args, ("modality", "sex", "height_cm", "height_ft", "height_in", "weight_kg", "weight_lb",
                 "duration_minutes", "intensity", "speed_mph", "distance_miles", "incline_percent"))
    modality = _choice(args, "modality", cardio_calc.MODALITIES)
    if args.get("sex") is not None:
        _choice(args, "sex", meal_plan.SEXES)
    _height_cm(args)  # accepted and range-checked like the web form; the formula does not use it
    weight = _weight_kg(args)
    duration = _number(args, "duration_minutes", *DURATION_RANGE)
    intensity = _choice(args, "intensity", cardio_calc.INTENSITIES)
    speed = _number(args, "speed_mph", *SPEED_RANGE, required=False)
    distance = _number(args, "distance_miles", *DISTANCE_RANGE, required=False)
    incline = _number(args, "incline_percent", *INCLINE_RANGE, required=False)
    if incline is not None and modality != "treadmill":
        raise InputError("incline_percent applies to the treadmill only")
    return _ok(cardio_calc.calculate_cardio_calories(modality, intensity, weight, duration, speed, distance, incline))


_HEIGHT = {
    "height_cm": {"type": "number", "description": "Height in cm (121.9-241.3). Or give height_ft and height_in."},
    "height_ft": {"type": "integer", "minimum": 4, "maximum": 7},
    "height_in": {"type": "number", "minimum": 0, "maximum": 11},
}
_WEIGHT = {
    "weight_kg": {"type": "number", "description": "Body weight in kg (36.3-249.5). Or give weight_lb."},
    "weight_lb": {"type": "number", "minimum": 80, "maximum": 550},
}
_SEX = {"type": "string", "enum": list(meal_plan.SEXES)}

SPLIT_SCHEMA = {
    "name": "axiom_lite_split",
    "description": ("Lite training split: one starting week of training for 2-6 days a week, by equipment, "
                    "swapping out exercises that load a flagged injury. Rule based and local: no account, no "
                    "network. Show the person the disclaimer and the education line with the result."),
    "parameters": {"type": "object", "additionalProperties": False, "required": ["days_per_week", "equipment"],
                   "properties": {
                       "days_per_week": {"type": "integer", "enum": list(training_split.DAYS_PER_WEEK)},
                       "equipment": {"type": "string", "enum": list(training_split.EQUIPMENT)},
                       "injuries": {"type": "array", "items": {"type": "string", "enum": list(training_split.INJURIES)},
                                    "description": "Areas the person says to protect. Empty if none."},
                   }},
}

MACROS_SCHEMA = {
    "name": "axiom_lite_macros",
    "description": ("Lite macro calculator: daily calorie, protein, fat and carb targets (Mifflin-St Jeor) and a "
                    "one-week meal structure. Local, no network. health_screen must hold the person's own answers "
                    "to the five questions, asked word for word; never fill one in for them. Any yes returns no "
                    "targets and points to a health professional. Estimates, not medical advice."),
    "parameters": {"type": "object", "additionalProperties": False,
                   "required": ["sex", "age_years", "activity_level", "goal", "health_screen"],
                   "properties": {
                       "sex": _SEX,
                       "age_years": {"type": "number", "minimum": 13, "maximum": 90},
                       **_HEIGHT, **_WEIGHT,
                       "activity_level": {"type": "string", "enum": list(meal_plan.ACTIVITY_FACTORS)},
                       "goal": {"type": "string", "enum": list(meal_plan.GOAL_ADJUSTMENT_KCAL)},
                       "health_screen": {
                           "type": "object", "additionalProperties": False,
                           "required": list(HEALTH_QUESTIONS),
                           "description": "The person's own yes/no answers. Ask each question exactly as written.",
                           "properties": {k: {"type": "boolean", "description": q} for k, q in HEALTH_QUESTIONS.items()},
                       },
                   }},
}

CARDIO_SCHEMA = {
    "name": "axiom_lite_cardio",
    "description": ("Lite cardio calculator: estimated calories for a cardio session from standard MET formulas "
                    "(ACSM treadmill equations when a speed or a distance is given). Local, no network. An "
                    "estimate, not a medical-grade measurement."),
    "parameters": {"type": "object", "additionalProperties": False,
                   "required": ["modality", "duration_minutes", "intensity"],
                   "properties": {
                       "modality": {"type": "string", "enum": list(cardio_calc.MODALITIES)},
                       "sex": _SEX, **_HEIGHT, **_WEIGHT,
                       "duration_minutes": {"type": "number", "minimum": 1, "maximum": 600},
                       "intensity": {"type": "string", "enum": list(cardio_calc.INTENSITIES)},
                       "speed_mph": {"type": "number", "minimum": 0.5, "maximum": 15},
                       "distance_miles": {"type": "number", "minimum": 0.1, "maximum": 100,
                                          "description": "Instead of speed_mph; speed is worked out from the duration."},
                       "incline_percent": {"type": "number", "minimum": 0, "maximum": 15, "description": "Treadmill only."},
                   }},
}

TOOLS = (
    ("axiom_lite_split", SPLIT_SCHEMA, split),
    ("axiom_lite_macros", MACROS_SCHEMA, macros),
    ("axiom_lite_cardio", CARDIO_SCHEMA, cardio),
)
