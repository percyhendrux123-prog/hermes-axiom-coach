// Macro targets and a one-week meal structure (mealPlan.ts of the Lite app).
// Mifflin-St Jeor BMR, activity factor, flat goal adjustment, a calorie floor by sex, then protein,
// fat and carbs from the final calorie number. Any health flag blocks the plan entirely.
import {
  ACTIVITY_FACTORS, BLOCKED_REASON, CALORIE_FLOOR, FAT_FLOOR_G_PER_KG, FAT_FLOOR_PCT_OF_CALORIES,
  GOAL_ADJUSTMENT_KCAL, MEAL_DESCRIPTION, MEAL_DISCLAIMER, MEAL_SPLIT, PROTEIN_G_PER_KG, SEXES,
} from './data.js'
import {
  AGE_RANGE, HEALTH_QUESTIONS, InputError, choice, heightCm, isPlainObject, number, ok, only, weightKg,
} from './common.js'

export function calculateBmr(sex, weightKgValue, heightCmValue, ageYears) {
  const base = 10 * weightKgValue + 6.25 * heightCmValue - 5 * ageYears
  return sex === 'male' ? base + 5 : base - 161
}

export function calculateMacros(sex, ageYears, heightCmValue, weightKgValue, activityLevel, goal) {
  const bmr = calculateBmr(sex, weightKgValue, heightCmValue, ageYears)
  const tdee = bmr * ACTIVITY_FACTORS[activityLevel]
  const adjusted = tdee + GOAL_ADJUSTMENT_KCAL[goal]
  const floored = Math.max(adjusted, CALORIE_FLOOR[sex])
  const calories = Math.round(floored / 10) * 10

  const proteinG = Math.round(weightKgValue * PROTEIN_G_PER_KG)
  const fatFromWeight = weightKgValue * FAT_FLOOR_G_PER_KG
  const fatFromCalories = (calories * FAT_FLOOR_PCT_OF_CALORIES) / 9
  const fatG = Math.round(Math.max(fatFromWeight, fatFromCalories))

  const remaining = calories - proteinG * 4 - fatG * 9
  const carbsG = Math.max(0, Math.round(remaining / 4))
  return { calories, proteinG, fatG, carbsG }
}

function week() {
  return Array.from({ length: 7 }, (_, i) => ({
    dayLabel: `Day ${i + 1}`,
    meals: MEAL_SPLIT.map((label) => ({ label, description: MEAL_DESCRIPTION })),
  }))
}

export function generateMealPlan(sex, ageYears, heightCmValue, weightKgValue, activityLevel, goal, healthFlags) {
  if (healthFlags) return { blocked: true, reason: BLOCKED_REASON }
  return {
    blocked: false,
    macros: calculateMacros(sex, ageYears, heightCmValue, weightKgValue, activityLevel, goal),
    days: week(),
    disclaimer: MEAL_DISCLAIMER,
  }
}

export function macros(args) {
  only(args, ['sex', 'age_years', 'height_cm', 'height_ft', 'height_in', 'weight_kg', 'weight_lb',
    'activity_level', 'goal', 'health_screen'])
  const sex = choice(args, 'sex', SEXES)
  const age = number(args, 'age_years', ...AGE_RANGE)
  const height = heightCm(args)
  if (height === null) throw new InputError('height_cm or height_ft + height_in is required')
  const weight = weightKg(args)
  const activity = choice(args, 'activity_level', Object.keys(ACTIVITY_FACTORS))
  const goal = choice(args, 'goal', Object.keys(GOAL_ADJUSTMENT_KCAL))
  const screen = args.health_screen
  const keys = Object.keys(HEALTH_QUESTIONS)
  if (!isPlainObject(screen) || Object.keys(screen).length !== keys.length
      || !keys.every((k) => k in screen) || Object.values(screen).some((v) => typeof v !== 'boolean')) {
    throw new InputError('health_screen needs all five answers as true or false, given by the person: '
      + Object.entries(HEALTH_QUESTIONS).map(([k, q]) => `${k}: ${q}`).join('; '))
  }
  return ok(generateMealPlan(sex, age, height, weight, activity, goal, Object.values(screen).some(Boolean)))
}
