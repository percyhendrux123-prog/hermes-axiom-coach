// Input checks and output shaping shared by the three calculators.
// Mirrors lite/tools.py of the Hermes plugin: same bounds, same messages, same order of checks.
import { SEXES } from './data.js'

export const EDUCATION_LINE =
  'General education, not medical advice. If you are pregnant, have a medical condition, take ' +
  'medication, or have a history of an eating disorder, talk to a doctor or registered dietitian ' +
  'before changing how you eat.'

export const CM_PER_INCH = 2.54
export const KG_PER_LB = 0.45359237

// Bounds copied from the Lite web app's input fields: age 13-90, height 4 ft 0 in to 7 ft 11 in,
// weight 80-550 lb, duration at least 1 minute, incline 0-15 percent. The web app sets no upper
// bound on duration, speed or distance; the limits marked PLUGIN are this plugin's own.
export const AGE_RANGE = [13, 90]
export const HEIGHT_FT_RANGE = [4, 7]
export const HEIGHT_IN_RANGE = [0, 11]
export const HEIGHT_CM_RANGE = [4 * 12 * CM_PER_INCH, (7 * 12 + 11) * CM_PER_INCH]
export const WEIGHT_LB_RANGE = [80, 550]
export const WEIGHT_KG_RANGE = [80 * KG_PER_LB, 550 * KG_PER_LB]
export const DURATION_RANGE = [1, 600] // PLUGIN upper bound
export const INCLINE_RANGE = [0, 15]
export const SPEED_RANGE = [0.5, 15] // PLUGIN
export const DISTANCE_RANGE = [0.1, 100] // PLUGIN

// The five health questions in the Lite macro calculator, word for word.
export const HEALTH_QUESTIONS = {
  heart_condition: 'Has a doctor ever told you that you have a heart condition?',
  chest_pain_during_activity: 'Do you have chest pain during physical activity?',
  pregnant_or_nursing: 'Are you currently pregnant or nursing?',
  eating_disorder: 'Do you have a diagnosed eating disorder, current or in recovery?',
  metabolic_medication: 'Are you on medication that affects metabolism, heart rate, or blood sugar?',
}

// Fields Claude Code adds to a tool call event next to the tool's own arguments. Seen in a live
// run (Claude Code 2.1.325): the event is the arguments plus `tool` and `tool_use_id`.
export const META_FIELDS = ['tool', 'tool_use_id']

export class InputError extends Error {}

// Python's `:g` format, as the Hermes plugin prints its limits: six significant digits.
function fmt(x) {
  return String(Number(x.toPrecision(6)))
}

export function isPlainObject(value) {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

export function number(args, key, lo, hi, required = true) {
  const value = args[key]
  if (value === undefined || value === null) {
    if (required) throw new InputError(`${key} is required`)
    return null
  }
  if (typeof value !== 'number') throw new InputError(`${key} must be a number`)
  if (!Number.isFinite(value)) throw new InputError(`${key} must be a number between ${fmt(lo)} and ${fmt(hi)}`)
  if (value < lo || value > hi) throw new InputError(`${key} must be between ${fmt(lo)} and ${fmt(hi)}`)
  return value
}

export function choice(args, key, options) {
  if (!options.includes(args[key])) throw new InputError(`${key} must be one of: ${options.join(', ')}`)
  return args[key]
}

export function only(args, allowed) {
  if (!isPlainObject(args)) throw new InputError('arguments must be an object')
  const extra = Object.keys(args)
    .filter((k) => !META_FIELDS.includes(k) && !allowed.includes(k))
    .sort()
  if (extra.length) throw new InputError(`unknown field(s): ${extra.join(', ')}`)
}

export function heightCm(args) {
  const hasCm = args.height_cm != null
  const hasFt = args.height_ft != null || args.height_in != null
  if (hasCm && hasFt) throw new InputError('give height_cm or height_ft + height_in, not both')
  if (hasCm) return number(args, 'height_cm', ...HEIGHT_CM_RANGE)
  if (hasFt) {
    const feet = number(args, 'height_ft', ...HEIGHT_FT_RANGE)
    const inches = number(args, 'height_in', ...HEIGHT_IN_RANGE)
    return (feet * 12 + inches) * CM_PER_INCH
  }
  return null
}

export function weightKg(args) {
  const hasKg = args.weight_kg != null
  const hasLb = args.weight_lb != null
  if (hasKg && hasLb) throw new InputError('give weight_kg or weight_lb, not both')
  if (hasKg) return number(args, 'weight_kg', ...WEIGHT_KG_RANGE)
  if (hasLb) return number(args, 'weight_lb', ...WEIGHT_LB_RANGE) * KG_PER_LB
  throw new InputError('weight_kg or weight_lb is required')
}

export function sexChoice(args) {
  return choice(args, 'sex', SEXES)
}

export function ok(payload) {
  payload.education = EDUCATION_LINE
  return JSON.stringify(payload)
}

export function refuse(message) {
  return JSON.stringify({ error: message, education: EDUCATION_LINE })
}

// Run one calculator. An input problem becomes a refusal the model can read; nothing else is caught,
// so a real bug shows up as a failed tool call rather than as a plausible wrong answer.
export function guard(fn, args) {
  try {
    return fn(args === undefined || args === null ? {} : args)
  } catch (error) {
    if (error instanceof InputError) return refuse(error.message)
    throw error
  }
}
