// node:test checks for the mod edition (claude-plugin/lite). Run: node --test claude-plugin/tests/
//
// 1. The JavaScript engines return exactly what the open Lite app's TypeScript engines returned, for
//    the same 3,580 cases the Hermes plugin's Python engines are checked against.
// 2. register.js registers three tools, answers each tool call with the engine result, and fails
//    closed if an engine throws.
// No network, no Claude Code, nothing written.
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import test from 'node:test'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const REPO = join(HERE, '..', '..')
const MOD = join(REPO, 'claude-plugin', 'lite', 'hooks')
const FIXTURE = JSON.parse(readFileSync(join(REPO, 'tests', 'fixtures', 'lite_parity.json'), 'utf8'))

const { generateTrainingProgram } = await import(join(MOD, 'engines', 'split.js'))
const { calculateMacros, generateMealPlan } = await import(join(MOD, 'engines', 'macros.js'))
const { calculateCardioCalories } = await import(join(MOD, 'engines', 'cardio.js'))
const { register } = await import(join(MOD, 'register.js'))
const { EDUCATION_LINE } = await import(join(MOD, 'engines', 'common.js'))

test('training split matches the Lite app for all 640 cases', () => {
  assert.equal(FIXTURE.training.length, 640)
  for (const { input, output } of FIXTURE.training) {
    assert.deepEqual(generateTrainingProgram(input.daysPerWeek, input.equipment, input.injuries), output, JSON.stringify(input))
  }
})

test('macros and meal plan match the Lite app for all 672 cases', () => {
  assert.equal(FIXTURE.meal.length, 672)
  for (const { input: i, output, macros } of FIXTURE.meal) {
    const args = [i.sex, i.ageYears, i.heightCm, i.weightKg, i.activityLevel, i.goal]
    assert.deepEqual(calculateMacros(...args), macros, JSON.stringify(i))
    assert.deepEqual(generateMealPlan(...args, i.healthFlags), output, JSON.stringify(i))
  }
})

test('cardio matches the Lite app for all 2,268 cases', () => {
  assert.ok(FIXTURE.cardio.length > 2000)
  for (const { input: i, output } of FIXTURE.cardio) {
    const got = calculateCardioCalories(i.modality, i.intensity, i.weightKg, i.durationMinutes,
      i.speedMph ?? null, i.distanceMiles ?? null, i.inclinePercent ?? null)
    assert.deepEqual(got, output, JSON.stringify(i))
  }
})

// A stand-in for the mods API: records what register() asks Claude Code for.
function load() {
  const hooks = []
  const tools = []
  const on = (event, matcher, fn) => {
    const hook = { event, matcher: typeof matcher === 'function' ? undefined : matcher, fn: typeof matcher === 'function' ? matcher : fn }
    hooks.push(hook)
    return { catch(handler) { hook.catchHandler = handler; return this } }
  }
  register(on)
  const $ = { tool: { register: async (t) => { tools.push(t) } } }
  return { hooks, tools, $ }
}

async function call(name, args, loaded = load()) {
  const hook = loaded.hooks.find((h) => h.event === 'tool.call' && h.matcher?.tool === `mcp__axiom-coach-lite__${name}`)
  assert.ok(hook, `no hook for ${name}`)
  // The event Claude Code sends is the arguments plus `tool` and `tool_use_id` (seen in a live run).
  const out = await hook.fn(loaded.$, { ...args, tool: hook.matcher.tool, tool_use_id: 'toolu_test' })
  return JSON.parse(out.result)
}

test('session.start registers exactly the three tools, loaded up front', async () => {
  const loaded = load()
  const start = loaded.hooks.find((h) => h.event === 'session.start')
  let passed = null
  await start.fn(loaded.$, { id: 'e' }, async (e) => { passed = e; return e })
  assert.deepEqual(loaded.tools.map((t) => t.name), ['axiom_lite_split', 'axiom_lite_macros', 'axiom_lite_cardio'])
  assert.ok(loaded.tools.every((t) => t.isDeferred === false && t.description && t.inputSchema.type === 'object'))
  assert.deepEqual(passed, { id: 'e' }, 'session.start still passes the event on')
})

test('only session.start and the three tool.call hooks are registered, each tool hook fails closed', () => {
  const { hooks } = load()
  assert.deepEqual(hooks.map((h) => h.event), ['session.start', 'tool.call', 'tool.call', 'tool.call'])
  for (const h of hooks.filter((x) => x.event === 'tool.call')) assert.equal(typeof h.catchHandler, 'function')
})

test('a split call returns the week and the education line', async () => {
  const r = await call('axiom_lite_split', { days_per_week: 3, equipment: 'full_gym', injuries: ['knee'] })
  assert.equal(r.splitName, 'Full Body')
  assert.equal(r.days.length, 3)
  assert.equal(r.education, EDUCATION_LINE)
  const squat = r.days[0].exercises[0]
  assert.equal(squat.name, 'Leg Press') // barbell squat skipped for a flagged knee, next candidate has no note
  assert.equal(squat.notes, undefined)
})

test('macros: a flagged health question returns no numbers', async () => {
  const base = { sex: 'male', age_years: 30, height_cm: 180, weight_kg: 85, activity_level: 'moderate', goal: 'maintenance' }
  const screen = { heart_condition: false, chest_pain_during_activity: false, pregnant_or_nursing: false, eating_disorder: false, metabolic_medication: false }
  const clear = await call('axiom_lite_macros', { ...base, health_screen: screen })
  assert.equal(clear.blocked, false)
  assert.equal(clear.days.length, 7)
  const flagged = await call('axiom_lite_macros', { ...base, health_screen: { ...screen, eating_disorder: true } })
  assert.equal(flagged.blocked, true)
  assert.equal(flagged.macros, undefined)
  assert.match(flagged.reason, /consult a qualified health professional/)
  assert.equal(flagged.education, EDUCATION_LINE)
})

test('macros: a missing or partial health screen is refused, never defaulted to no', async () => {
  const base = { sex: 'female', age_years: 30, height_cm: 165, weight_kg: 60, activity_level: 'light', goal: 'fat_loss' }
  for (const screen of [undefined, null, {}, { heart_condition: false }, { heart_condition: 'no', chest_pain_during_activity: false, pregnant_or_nursing: false, eating_disorder: false, metabolic_medication: false }]) {
    const r = await call('axiom_lite_macros', { ...base, ...(screen === undefined ? {} : { health_screen: screen }) })
    assert.match(r.error, /health_screen needs all five answers/)
    assert.equal(r.macros, undefined)
  }
})

test('cardio: a treadmill with speed and incline uses the ACSM equations', async () => {
  const r = await call('axiom_lite_cardio', { modality: 'treadmill', duration_minutes: 30, intensity: 'moderate', weight_kg: 80, speed_mph: 3, incline_percent: 5 })
  assert.deepEqual(Object.keys(r), ['met', 'caloriesBurned', 'disclaimer', 'education'])
  assert.ok(r.met > 3 && r.caloriesBurned > 0)
})

test('input problems come back as an error plus the education line', async () => {
  const bad = [
    ['axiom_lite_split', { days_per_week: 7, equipment: 'full_gym' }, /days_per_week must be one of: 2, 3, 4, 5, 6/],
    ['axiom_lite_split', { days_per_week: 3, equipment: 'full_gym', injuries: ['elbow'] }, /injuries must be a list drawn from/],
    ['axiom_lite_split', { days_per_week: 3, equipment: 'full_gym', extra: 1 }, /unknown field\(s\): extra/],
    ['axiom_lite_cardio', { modality: 'rower', duration_minutes: 30, intensity: 'low', weight_kg: 80, incline_percent: 2 }, /treadmill only/],
    ['axiom_lite_cardio', { modality: 'rower', duration_minutes: 0, intensity: 'low', weight_kg: 80 }, /duration_minutes must be between 1 and 600/],
    ['axiom_lite_cardio', { modality: 'rower', duration_minutes: 30, intensity: 'low', weight_kg: 80, weight_lb: 170 }, /not both/],
  ]
  for (const [name, args, pattern] of bad) {
    const r = await call(name, args)
    assert.match(r.error, pattern)
    assert.equal(r.education, EDUCATION_LINE)
  }
})

test('if an engine throws, the hook fails closed with a message that gives no numbers', async () => {
  const loaded = load()
  const hook = loaded.hooks.find((h) => h.matcher?.tool === 'mcp__axiom-coach-lite__axiom_lite_macros')
  const out = await hook.catchHandler(loaded.$, {}, { called: false, error: { kind: 'throw' } })
  const r = JSON.parse(out.result)
  assert.match(r.error, /no result was produced/)
  assert.equal(r.macros, undefined)
})
