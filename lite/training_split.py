"""Training split selector and exercise substitution.

Python port of the Lite engine ``trainingSplit.ts``. Rule based, no model calls, no
randomness: the same input always gives the same output. Parity with the TypeScript
engine is checked in ``tests/test_parity.py`` against ``tests/fixtures/lite_parity.json``.
"""

EQUIPMENT = ("full_gym", "dumbbells_only", "bodyweight_only", "home_gym_basic")
INJURIES = ("shoulder", "lower_back", "knee", "wrist", "hip")
DAYS_PER_WEEK = (2, 3, 4, 5, 6)

DISCLAIMER = (
    "This is a single-week starting template, not a progressive program. Consult a "
    "professional before starting if you have any medical concerns."
)
SUBSTITUTED_NOTE = "Substituted for flagged injury."


def _c(name, *avoid):
    return (name, tuple(avoid))


# pattern -> equipment tier -> ordered candidates, plus an injury-neutral fallback.
EXERCISE_TABLE = {
    "squat": {
        "full_gym": [_c("Barbell Back Squat", "knee", "lower_back"), _c("Leg Press", "lower_back"), _c("Goblet Squat")],
        "home_gym_basic": [_c("Barbell Back Squat", "knee", "lower_back"), _c("Goblet Squat")],
        "dumbbells_only": [_c("Dumbbell Goblet Squat"), _c("Dumbbell Front Squat", "wrist")],
        "bodyweight_only": [_c("Bodyweight Squat"), _c("Tempo Bodyweight Squat")],
        "safe": "Wall Sit",
    },
    "hinge": {
        "full_gym": [_c("Barbell Romanian Deadlift", "lower_back"), _c("Cable Pull-Through"), _c("Glute Bridge")],
        "home_gym_basic": [_c("Barbell Romanian Deadlift", "lower_back"), _c("Dumbbell Romanian Deadlift", "lower_back"), _c("Glute Bridge")],
        "dumbbells_only": [_c("Dumbbell Romanian Deadlift", "lower_back"), _c("Dumbbell Glute Bridge")],
        "bodyweight_only": [_c("Single-Leg Glute Bridge"), _c("Bodyweight Good Morning", "lower_back")],
        "safe": "Glute Bridge",
    },
    "horizontal_push": {
        "full_gym": [_c("Barbell Bench Press", "shoulder", "wrist"), _c("Machine Chest Press", "wrist"), _c("Push-Up", "wrist")],
        "home_gym_basic": [_c("Barbell Bench Press", "shoulder", "wrist"), _c("Dumbbell Bench Press", "shoulder", "wrist"), _c("Push-Up", "wrist")],
        "dumbbells_only": [_c("Dumbbell Bench Press", "shoulder", "wrist"), _c("Dumbbell Floor Press", "shoulder")],
        "bodyweight_only": [_c("Push-Up", "wrist"), _c("Incline Push-Up", "wrist")],
        "safe": "Incline Push-Up (knees down)",
    },
    "vertical_push": {
        "full_gym": [_c("Barbell Overhead Press", "shoulder"), _c("Machine Shoulder Press", "shoulder"), _c("Dumbbell Seated Shoulder Press", "shoulder")],
        "home_gym_basic": [_c("Barbell Overhead Press", "shoulder"), _c("Dumbbell Seated Shoulder Press", "shoulder")],
        "dumbbells_only": [_c("Dumbbell Seated Shoulder Press", "shoulder"), _c("Dumbbell Arnold Press", "shoulder")],
        "bodyweight_only": [_c("Pike Push-Up", "shoulder", "wrist"), _c("Wall Handstand Hold", "shoulder", "wrist")],
        "safe": "Standing Band-Free Arm Raise Hold",
    },
    "horizontal_pull": {
        "full_gym": [_c("Seated Cable Row", "lower_back"), _c("Chest-Supported Machine Row"), _c("Inverted Row")],
        "home_gym_basic": [_c("Barbell Bent-Over Row", "lower_back"), _c("Dumbbell Bent-Over Row", "lower_back"), _c("Inverted Row")],
        "dumbbells_only": [_c("Dumbbell Bent-Over Row", "lower_back"), _c("Single-Arm Dumbbell Row (bench supported)")],
        "bodyweight_only": [_c("Inverted Row"), _c("Doorframe Towel Row")],
        "safe": "Chest-Supported Row (bodyweight)",
    },
    "vertical_pull": {
        "full_gym": [_c("Lat Pulldown", "shoulder"), _c("Assisted Pull-Up Machine", "shoulder"), _c("Pull-Up", "shoulder")],
        "home_gym_basic": [_c("Pull-Up", "shoulder"), _c("Band-Assisted Pull-Up", "shoulder")],
        "dumbbells_only": [_c("Dumbbell Pullover", "shoulder"), _c("Dumbbell Renegade Row", "wrist", "shoulder")],
        "bodyweight_only": [_c("Pull-Up", "shoulder"), _c("Doorframe Row")],
        "safe": "Scapular Retraction Hold",
    },
    "unilateral_leg": {
        "full_gym": [_c("Walking Lunge", "knee"), _c("Bulgarian Split Squat", "knee", "hip"), _c("Step-Up", "knee")],
        "home_gym_basic": [_c("Dumbbell Walking Lunge", "knee"), _c("Dumbbell Bulgarian Split Squat", "knee", "hip")],
        "dumbbells_only": [_c("Dumbbell Walking Lunge", "knee"), _c("Dumbbell Bulgarian Split Squat", "knee", "hip")],
        "bodyweight_only": [_c("Bodyweight Walking Lunge", "knee"), _c("Bodyweight Step-Up", "knee")],
        "safe": "Standing Hip Hinge to Toe Tap",
    },
    "core": {
        "full_gym": [_c("Plank"), _c("Dead Bug")],
        "home_gym_basic": [_c("Plank"), _c("Dead Bug")],
        "dumbbells_only": [_c("Plank"), _c("Dead Bug")],
        "bodyweight_only": [_c("Plank"), _c("Dead Bug")],
        "safe": "Dead Bug",
    },
    "biceps": {
        "full_gym": [_c("Cable Bicep Curl", "wrist"), _c("Dumbbell Bicep Curl", "wrist")],
        "home_gym_basic": [_c("Dumbbell Bicep Curl", "wrist")],
        "dumbbells_only": [_c("Dumbbell Bicep Curl", "wrist")],
        "bodyweight_only": [_c("Isometric Bicep Hold (towel curl)")],
        "safe": "Isometric Bicep Hold",
    },
    "triceps": {
        "full_gym": [_c("Cable Triceps Pushdown", "wrist", "shoulder"), _c("Dumbbell Overhead Triceps Extension", "shoulder", "wrist")],
        "home_gym_basic": [_c("Dumbbell Overhead Triceps Extension", "shoulder", "wrist"), _c("Dumbbell Skull Crusher", "wrist", "shoulder")],
        "dumbbells_only": [_c("Dumbbell Overhead Triceps Extension", "shoulder", "wrist"), _c("Dumbbell Skull Crusher", "wrist", "shoulder")],
        "bodyweight_only": [_c("Bench Dip", "shoulder", "wrist"), _c("Diamond Push-Up", "wrist")],
        "safe": "Triceps Kickback (bodyweight arm only)",
    },
    "calf": {
        "full_gym": [_c("Standing Calf Raise")],
        "home_gym_basic": [_c("Standing Calf Raise")],
        "dumbbells_only": [_c("Standing Calf Raise")],
        "bodyweight_only": [_c("Standing Calf Raise")],
        "safe": "Standing Calf Raise",
    },
    "rear_delt": {
        "full_gym": [_c("Cable Face Pull", "shoulder"), _c("Reverse Pec Deck", "shoulder")],
        "home_gym_basic": [_c("Dumbbell Reverse Fly", "shoulder")],
        "dumbbells_only": [_c("Dumbbell Reverse Fly", "shoulder")],
        "bodyweight_only": [_c("Prone Y-Raise", "shoulder")],
        "safe": "Prone Y-Raise (light)",
    },
}


def _day(focus, *slots):
    return {"focus": focus, "slots": [{"pattern": p, "sets": s, "reps": r} for p, s, r in slots]}


FULL_BODY_A = _day("Full Body", ("squat", 3, "8-12"), ("horizontal_push", 3, "8-12"), ("horizontal_pull", 3, "8-12"), ("hinge", 3, "8-12"), ("core", 3, "30-45s"))
FULL_BODY_B = _day("Full Body", ("hinge", 3, "8-12"), ("vertical_push", 3, "8-12"), ("vertical_pull", 3, "8-12"), ("unilateral_leg", 3, "10-12/leg"), ("core", 3, "30-45s"))
FULL_BODY_C = _day("Full Body", ("squat", 3, "8-12"), ("vertical_push", 3, "8-12"), ("horizontal_pull", 3, "8-12"), ("hinge", 3, "8-12"), ("core", 3, "30-45s"))
UPPER_A = _day("Upper Body", ("horizontal_push", 4, "8-12"), ("horizontal_pull", 4, "8-12"), ("vertical_push", 3, "8-12"), ("vertical_pull", 3, "8-12"), ("biceps", 3, "10-15"), ("triceps", 3, "10-15"))
UPPER_B = _day("Upper Body", ("vertical_push", 4, "8-12"), ("vertical_pull", 4, "8-12"), ("horizontal_push", 3, "8-12"), ("horizontal_pull", 3, "8-12"), ("triceps", 3, "10-15"), ("rear_delt", 3, "12-15"))
LOWER_A = _day("Lower Body", ("squat", 4, "8-12"), ("hinge", 4, "8-12"), ("unilateral_leg", 3, "10-12/leg"), ("calf", 4, "12-15"), ("core", 3, "30-45s"))
LOWER_B = _day("Lower Body", ("hinge", 4, "8-12"), ("squat", 4, "8-12"), ("unilateral_leg", 3, "10-12/leg"), ("calf", 4, "12-15"), ("core", 3, "30-45s"))
PUSH = _day("Push", ("horizontal_push", 4, "8-12"), ("vertical_push", 4, "8-12"), ("triceps", 4, "10-15"), ("core", 3, "30-45s"))
PULL = _day("Pull", ("vertical_pull", 4, "8-12"), ("horizontal_pull", 4, "8-12"), ("rear_delt", 3, "12-15"), ("biceps", 4, "10-15"))
LEGS = _day("Legs", ("squat", 4, "8-12"), ("hinge", 4, "8-12"), ("unilateral_leg", 3, "10-12/leg"), ("calf", 4, "12-15"), ("core", 3, "30-45s"))

SPLIT_TABLE = {
    2: ("Full Body", [FULL_BODY_A, FULL_BODY_B]),
    3: ("Full Body", [FULL_BODY_A, FULL_BODY_B, FULL_BODY_C]),
    4: ("Upper / Lower", [UPPER_A, LOWER_A, UPPER_B, LOWER_B]),
    5: ("Push / Pull / Legs + Upper / Lower", [PUSH, PULL, LEGS, UPPER_A, LOWER_A]),
    6: ("Push / Pull / Legs (x2)", [PUSH, PULL, LEGS, PUSH, PULL, LEGS]),
}


def _pick(pattern, equipment, injuries):
    table = EXERCISE_TABLE[pattern]
    for name, avoid in table[equipment]:
        if not any(flag in injuries for flag in avoid):
            return name, False
    return table["safe"], True


def generate_training_program(days_per_week, equipment, injuries):
    """Same contract as ``generateTrainingProgram``. Inputs must already be validated."""
    split_name, templates = SPLIT_TABLE[days_per_week]
    days = []
    for index, template in enumerate(templates):
        exercises = []
        for slot in template["slots"]:
            name, substituted = _pick(slot["pattern"], equipment, injuries)
            exercise = {"name": name, "sets": slot["sets"], "reps": slot["reps"]}
            if substituted:
                exercise["notes"] = SUBSTITUTED_NOTE
            exercises.append(exercise)
        days.append({"dayLabel": f"Day {index + 1}", "focus": template["focus"], "exercises": exercises})
    return {"splitName": split_name, "daysPerWeek": days_per_week, "days": days, "disclaimer": DISCLAIMER}
