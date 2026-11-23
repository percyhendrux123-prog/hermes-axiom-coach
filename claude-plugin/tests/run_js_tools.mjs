// Test helper: read [{"tool": "...", "args": {...}}, ...] on stdin, run each through the mod's
// engines the way register.js does, and print the raw result strings as a JSON array.
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const MOD = join(dirname(fileURLToPath(import.meta.url)), '..', 'lite', 'hooks')
const { guard } = await import(join(MOD, 'engines', 'common.js'))
const { split } = await import(join(MOD, 'engines', 'split.js'))
const { macros } = await import(join(MOD, 'engines', 'macros.js'))
const { cardio } = await import(join(MOD, 'engines', 'cardio.js'))
const engines = { axiom_lite_split: split, axiom_lite_macros: macros, axiom_lite_cardio: cardio }

const cases = JSON.parse(readFileSync(0, 'utf8'))
console.log(JSON.stringify(cases.map(({ tool, args }) => guard(engines[tool], args))))
