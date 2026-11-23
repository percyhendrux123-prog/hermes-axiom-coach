// Axiom Coach Lite Tools: the Lite calculators as three local tools.
//
// session.start registers the tools; tool.call answers each one with the result of a pure function.
// No network, no files, no processes, no model calls, no state, and no other event is touched.
import { guard } from './engines/common.js'
import { split } from './engines/split.js'
import { macros } from './engines/macros.js'
import { cardio } from './engines/cardio.js'
import { CARDIO_TOOL, MACROS_TOOL, SPLIT_TOOL } from './engines/schemas.js'

// If a calculator ever throws (a bug, not bad input), fail closed: tell Claude no numbers were produced,
// so it does not improvise them, least of all past the macro calculator's health questions.
async function failed($, e, next) {
  return {
    result: JSON.stringify({
      error: 'This calculator failed, so no result was produced. Do not work out numbers another way; tell the person it did not run.',
    }),
  }
}

// Claude sees each tool as mcp__<plugin name>__<tool name>.
export function register(on) {
  on('session.start', async ($, e, next) => {
    await $.tool.register({ ...SPLIT_TOOL, isDeferred: false })
    await $.tool.register({ ...MACROS_TOOL, isDeferred: false })
    await $.tool.register({ ...CARDIO_TOOL, isDeferred: false })
    return next(e)
  })

  on('tool.call', { tool: 'mcp__axiom-coach-lite__axiom_lite_split' }, async ($, e) => {
    return { result: guard(split, e) }
  }).catch(failed)

  on('tool.call', { tool: 'mcp__axiom-coach-lite__axiom_lite_macros' }, async ($, e) => {
    return { result: guard(macros, e) }
  }).catch(failed)

  on('tool.call', { tool: 'mcp__axiom-coach-lite__axiom_lite_cardio' }, async ($, e) => {
    return { result: guard(cardio, e) }
  }).catch(failed)
}
