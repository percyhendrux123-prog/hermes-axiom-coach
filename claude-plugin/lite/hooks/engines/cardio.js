// MET-based cardio calorie estimate (cardioCalc.ts of the Lite app): the ACSM walking and running
// equations for a treadmill with a speed (or a distance and a duration), otherwise a fixed MET by
// modality and self-reported intensity. An estimate, not a medical-grade measurement.
import {
  CARDIO_DISCLAIMER, INTENSITIES, MET_TABLE, MODALITIES, MPH_TO_M_PER_MIN, SEXES, TREADMILL_INTENSITY_MET,
  WALK_RUN_THRESHOLD_MPH,
} from './data.js'
import {
  DISTANCE_RANGE, DURATION_RANGE, INCLINE_RANGE, InputError, SPEED_RANGE, choice, heightCm, number, ok, only,
  weightKg,
} from './common.js'

export function calculateTreadmillMet(speedMph, inclinePercent) {
  const speed = speedMph * MPH_TO_M_PER_MIN
  const grade = inclinePercent / 100
  const vo2 = speedMph <= WALK_RUN_THRESHOLD_MPH
    ? 0.1 * speed + 1.8 * speed * grade + 3.5
    : 0.2 * speed + 0.9 * speed * grade + 3.5
  return vo2 / 3.5
}

export function resolveEffectiveSpeedMph(durationMinutes, speedMph, distanceMiles) {
  if (speedMph != null) return speedMph
  if (distanceMiles != null && durationMinutes > 0) return distanceMiles / (durationMinutes / 60)
  return null
}

export function resolveMet(modality, intensity, durationMinutes, speedMph, distanceMiles, inclinePercent) {
  const speed = resolveEffectiveSpeedMph(durationMinutes, speedMph, distanceMiles)
  if (modality === 'treadmill' && speed !== null) {
    return calculateTreadmillMet(speed, inclinePercent != null ? inclinePercent : 0)
  }
  if (modality === 'treadmill') return TREADMILL_INTENSITY_MET[intensity]
  return MET_TABLE[modality][intensity]
}

export function calculateCardioCalories(modality, intensity, weightKgValue, durationMinutes, speedMph,
  distanceMiles, inclinePercent) {
  const met = resolveMet(modality, intensity, durationMinutes, speedMph, distanceMiles, inclinePercent)
  const calories = Math.round((met * 3.5 * weightKgValue * durationMinutes) / 200)
  return { met: Math.round(met * 10) / 10, caloriesBurned: calories, disclaimer: CARDIO_DISCLAIMER }
}

export function cardio(args) {
  only(args, ['modality', 'sex', 'height_cm', 'height_ft', 'height_in', 'weight_kg', 'weight_lb',
    'duration_minutes', 'intensity', 'speed_mph', 'distance_miles', 'incline_percent'])
  const modality = choice(args, 'modality', MODALITIES)
  if (args.sex != null) choice(args, 'sex', SEXES)
  heightCm(args) // accepted and range-checked like the web form; the formula does not use it
  const weight = weightKg(args)
  const duration = number(args, 'duration_minutes', ...DURATION_RANGE)
  const intensity = choice(args, 'intensity', INTENSITIES)
  const speed = number(args, 'speed_mph', ...SPEED_RANGE, false)
  const distance = number(args, 'distance_miles', ...DISTANCE_RANGE, false)
  const incline = number(args, 'incline_percent', ...INCLINE_RANGE, false)
  if (incline !== null && modality !== 'treadmill') throw new InputError('incline_percent applies to the treadmill only')
  return ok(calculateCardioCalories(modality, intensity, weight, duration, speed, distance, incline))
}
