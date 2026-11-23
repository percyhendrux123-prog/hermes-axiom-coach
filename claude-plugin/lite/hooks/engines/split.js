// Training split selector and exercise substitution (trainingSplit.ts of the Lite app).
// Rule based, no randomness: the same input always gives the same output.
import {
  DAYS_PER_WEEK, EQUIPMENT, EXERCISE_TABLE, INJURIES, SPLIT_DISCLAIMER, SPLIT_TABLE, SUBSTITUTED_NOTE,
} from './data.js'
import { InputError, choice, ok, only } from './common.js'

function pick(pattern, equipment, injuries) {
  const table = EXERCISE_TABLE[pattern]
  for (const [name, avoid] of table[equipment]) {
    if (!avoid.some((flag) => injuries.includes(flag))) return [name, false]
  }
  return [table.safe, true]
}

export function generateTrainingProgram(daysPerWeek, equipment, injuries) {
  const { name: splitName, days: templates } = SPLIT_TABLE[String(daysPerWeek)]
  const days = templates.map((template, index) => {
    const exercises = template.slots.map((slot) => {
      const [name, substituted] = pick(slot.pattern, equipment, injuries)
      const exercise = { name, sets: slot.sets, reps: slot.reps }
      if (substituted) exercise.notes = SUBSTITUTED_NOTE
      return exercise
    })
    return { dayLabel: `Day ${index + 1}`, focus: template.focus, exercises }
  })
  return { splitName, daysPerWeek, days, disclaimer: SPLIT_DISCLAIMER }
}

export function split(args) {
  only(args, ['days_per_week', 'equipment', 'injuries'])
  const days = args.days_per_week
  if (typeof days !== 'number' || !DAYS_PER_WEEK.includes(days)) {
    throw new InputError('days_per_week must be one of: 2, 3, 4, 5, 6')
  }
  const equipment = choice(args, 'equipment', EQUIPMENT)
  const injuries = args.injuries === undefined ? [] : args.injuries
  if (!Array.isArray(injuries) || injuries.some((i) => !INJURIES.includes(i))) {
    throw new InputError(`injuries must be a list drawn from: ${INJURIES.join(', ')}`)
  }
  return ok(generateTrainingProgram(days, equipment, [...new Set(injuries)]))
}
