---
name: lite-tools
description: Use when someone wants a quick training split, macro targets or a cardio calorie estimate and the Lite tools are loaded. Says how to call the three tools and how to ask the five health questions.
---

# Lite tools

This plugin gives Claude three local tools. No account, no network, nothing saved. They appear as
`mcp__axiom-coach-lite__axiom_lite_split`, `mcp__axiom-coach-lite__axiom_lite_macros` and
`mcp__axiom-coach-lite__axiom_lite_cardio`.

| Tool | Gives | Needs |
|---|---|---|
| `axiom_lite_split` | One starting week of training, 2-6 days | days per week, equipment, areas to protect |
| `axiom_lite_macros` | Daily calories, protein, fat, carbs and a week of meal structure | sex, age, height, weight, activity, goal, five health questions |
| `axiom_lite_cardio` | Estimated calories for one cardio session | machine, minutes, intensity, weight; speed or distance and incline for a treadmill |

## How to use them

- Ask only for what the tool needs. Height and weight can be imperial (`height_ft` + `height_in`,
  `weight_lb`) or metric (`height_cm`, `weight_kg`), not both.
- If a tool returns `error`, tell the person what to fix in plain words and ask again. Do not guess a
  value to make it pass.
- Show the result as the tool gives it, with its disclaimer and the `education` line every time.
  These are estimates for general education, not a prescription.
- If the tool says it failed and produced no result, tell the person it did not run. Do not work the
  numbers out another way.

## The health screen in the macro calculator

- Ask the person all five questions, word for word, as listed in the tool's `health_screen` fields.
  Never answer one for them, never "assume no", and never fill it in from something they said earlier
  without asking.
- Any yes returns no numbers, on purpose. Pass on the tool's message: talk to a doctor or registered
  dietitian first. Do not work out targets another way, and do not suggest they answer differently.

## Limits

Results stay in this chat; nothing syncs across devices. For a plan that keeps a log and follows the
person between phone and computer, they need the self-serve plan in the coach app (skill
`axiom-coach:my-plan`, from the `axiom-coach` plugin).
