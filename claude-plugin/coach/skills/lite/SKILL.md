---
name: lite
description: Use when someone wants a quick training split, daily macro targets or a cardio calorie estimate with no account. Gives the Lite calculator rules as step-by-step instructions, with the health questions asked first.
---

# Lite calculators

Three small calculators from the open Lite app, written here as instructions. No account, no network,
nothing saved. You work each one out in this chat from the rules below. Results are estimates for
general education, not a prescription.

| Calculator | Gives | Needs |
|---|---|---|
| Training split | One starting week of training, 2-6 days | days per week, equipment, areas to protect |
| Macros | Daily calories, protein, fat, carbs and a week of meal structure | sex, age, height, weight, activity, goal, five health questions |
| Cardio | Estimated calories for one cardio session | machine, minutes, intensity, weight; speed or distance and incline for a treadmill |

## How to use them

- Ask only for what the calculator needs. Height and weight can be imperial or metric, not both.
- If an input is outside the limits below, tell the person what to fix in plain words and ask again.
  Do not guess a value to make it pass.
- Work the arithmetic one step at a time and show each step, so the person can check it. Use the
  rounding rule below exactly.
- End every result with the disclaimer for that calculator and this line, word for word:
  "General education, not medical advice. If you are pregnant, have a medical condition, take medication, or have a history of an eating disorder, talk to a doctor or registered dietitian before changing how you eat."
- Nothing here is stored. Results stay in this chat.

## Rounding and units

- **Round** means round half up: add 0.5, then drop the fraction (2.5 becomes 3, 1.5 becomes 2). Do not
  use round-half-to-even.
- Inches to cm: multiply by 2.54. Pounds to kg: multiply by 0.45359237.
- Height in feet and inches: `height_cm = (feet x 12 + inches) x 2.54`.
- Convert at the start, keep full precision through the steps, round only where a step says to.

## Input limits

| Input | Allowed |
|---|---|
| Age | 13 to 90 years |
| Height | 4 ft 0 in to 7 ft 11 in (121.92 to 241.3 cm). Feet 4 to 7, inches 0 to 11 |
| Weight | 80 to 550 lb (36.3 to 249.5 kg) |
| Cardio duration | 1 to 600 minutes (600 is this plugin's own limit, to catch typos) |
| Treadmill speed | 0.5 to 15 mph (plugin limit) |
| Distance | 0.1 to 100 miles (plugin limit) |
| Incline | 0 to 15 percent, treadmill only |

## 1. Training split

Inputs: `days_per_week` (2, 3, 4, 5 or 6), `equipment` (`full_gym`, `home_gym_basic`, `dumbbells_only`,
`bodyweight_only`), and `injuries`: any of `shoulder`, `lower_back`, `knee`, `wrist`, `hip`, or none.

1. Open [the split tables](references/split-tables.md). Find the split for the person's days per week.
   It lists each day's focus and its slots (a movement pattern, sets and reps).
2. For each slot, pick the exercise for that pattern and equipment using the table's rule: first
   candidate not skipped by a flagged injury, otherwise the fallback with its note.
3. Present the week as Day 1, Day 2, and so on: the focus, then each exercise with sets x reps (and the
   note where there is one).
4. Close with this disclaimer: "This is a single-week starting template, not a progressive program.
   Consult a professional before starting if you have any medical concerns."

The same inputs always give the same week. Nothing is random.

## 2. Macros

Inputs: sex (`male` or `female`), age, height, weight, activity level (`sedentary`, `light`,
`moderate`, `very_active`), goal (`fat_loss`, `maintenance`, `muscle_gain`), and the five health
questions.

### The health questions come first

- Ask the person all five questions, word for word, and take their own yes or no for each:
  1. Has a doctor ever told you that you have a heart condition?
  2. Do you have chest pain during physical activity?
  3. Are you currently pregnant or nursing?
  4. Do you have a diagnosed eating disorder, current or in recovery?
  5. Are you on medication that affects metabolism, heart rate, or blood sugar?
- Never answer one for them, never "assume no", and never fill one in from something they said earlier
  without asking.
- **Any yes: stop. Give no numbers.** Say exactly: "We can't safely auto-generate a nutrition plan
  based on what you told us. Please consult a qualified health professional before starting a calorie
  or macro plan." Do not work out targets another way and do not suggest they answer differently.

### The arithmetic (all five answers no)

1. `BMR = 10 x weight_kg + 6.25 x height_cm - 5 x age`, then add 5 for male or subtract 161 for female
   (Mifflin-St Jeor).
2. `TDEE = BMR x activity factor`:

   | Activity | Factor |
   |---|---|
   | sedentary | 1.2 |
   | light | 1.375 |
   | moderate | 1.55 |
   | very_active | 1.725 |

3. `adjusted = TDEE + goal adjustment`:

   | Goal | kcal |
   |---|---|
   | fat_loss | -500 |
   | maintenance | 0 |
   | muscle_gain | +300 |

4. Apply the calorie floor: `floored = the larger of adjusted and the floor`. Floor: 1300 for female,
   1600 for male.
5. `calories = round(floored / 10) x 10`.
6. `protein_g = round(weight_kg x 2.1)`.
7. `fat_g = round(the larger of (weight_kg x 0.5) and (calories x 0.25 / 9))`.
8. `carbs_g = the larger of 0 and round((calories - protein_g x 4 - fat_g x 9) / 4)`.
9. Week of meal structure: Day 1 to Day 7, each with four entries, Meal 1, Meal 2, Meal 3 and Snack,
   and each entry reads: "Lean protein source + complex carbohydrate + vegetables (portion to hit
   daily macro targets)."
10. Close with: "Estimates based on the Mifflin-St Jeor equation. Not medical advice. Adjust based on
    real-world progress."

Give the four targets (calories, protein, fat, carbs in grams) and the week. The week is the same
structure every day; do not invent menus, foods or portions beyond that line.

## 3. Cardio

Inputs: modality (`treadmill`, `elliptical`, `stationary_bike`, `stair_climber`, `rower`), duration in
minutes, intensity (`low`, `moderate`, `high`), body weight, and for a treadmill optionally speed in
mph or a distance in miles, and incline percent. Sex and height may be asked, but the formula does not
use them.

1. **Find the MET value.**
   - **Treadmill with a speed or a distance:** speed in mph is the given speed, or
     `distance_miles / (duration_minutes / 60)` if only a distance is given. Then:
     - `speed = speed_mph x 26.8224` (meters per minute), `grade = incline_percent / 100`
       (incline is 0 if not given).
     - If speed_mph is 4.3 or less (walking): `vo2 = 0.1 x speed + 1.8 x speed x grade + 3.5`.
     - If speed_mph is above 4.3 (running): `vo2 = 0.2 x speed + 0.9 x speed x grade + 3.5`.
     - `MET = vo2 / 3.5` (ACSM treadmill equations).
   - **Treadmill with no speed or distance:** low 3.5, moderate 6.0, high 9.8.
   - **Every other machine:** look up the MET by machine and intensity:

     | Machine | low | moderate | high |
     |---|---|---|---|
     | elliptical | 4.6 | 5.0 | 7.0 |
     | stationary_bike | 3.5 | 6.8 | 10.5 |
     | stair_climber | 4.0 | 8.0 | 9.8 |
     | rower | 3.5 | 7.0 | 12.0 |

   - Incline applies to the treadmill only; if it is given for another machine, tell the person it does
     not apply and ask again.
2. `calories = round(MET x 3.5 x weight_kg x duration_minutes / 200)`.
3. Show the MET rounded to one decimal place (`round(MET x 10) / 10`) and the calories.
4. Close with: "Estimate only, based on standard MET formulas. Not a medical-grade measurement."

## Limits

- You are doing the arithmetic yourself. Recheck each step before you give numbers. If the person needs
  numbers they can rely on to the last digit, the `axiom-coach-lite` plugin from the same marketplace
  runs the same rules as local tools.
- Results stay in this chat; nothing syncs across devices. For a plan that keeps a log and follows the
  person between phone and computer, they need the self-serve plan in the coach app (skill
  `axiom-coach:my-plan`).
