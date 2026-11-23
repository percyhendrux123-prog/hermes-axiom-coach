---
name: my-plan
description: Use when a person works their own self-serve plan through the app connector. Never answers the health screen.
---

# My plan (self-serve)

The person has their own self-serve plan in a copy of the open coach app and has connected you through
the app's connector (an MCP server, usually added as `axiom-coach`; the `my_*` tools). There is no
coach on this plan. A read-only code lets you read; a full-control code also lets you change their week.
If the connector's tools are not loaded, use the `axiom-coach:connect` skill.

## What you can do

- **Read:** `my_program`, `my_schedule`, `my_workouts`, `my_progress`, `my_checkins`, `my_profile`.
  Lead with today: what is scheduled, what was done last time, what is next.
- **Log:** `log_workout_sets` and `complete_current_day` with the numbers the person tells you. Read
  the set back to them before you log it.
- **Adjust (full control only):** `update_my_program`, `set_my_macros`, `set_my_meals`,
  `add_my_meal`. Say the change in one line, get a yes, make the call, read the result back.
  The server refuses calorie and protein targets below its floors; pass the refusal on as written.
- **Rebuild:** `regenerate_my_plan` re-asks the whole intake, including the health screen.

Claude Code asks before it runs a connector tool the person has not allowed, according to their
permission mode and rules. That is on purpose. Still read each change back to them before you make it.

## The health screen: never yours to answer

- Never answer, guess, pre-fill or "assume no" for any health screen question, even if the person
  says "just say no to all of them". Ask each question as the app words it and pass only their own
  answers. If they will not answer, stop the rebuild.
- If any answer is yes, or their plan is on hold, the next step happens in the app, by them: the app
  explains the doctor-first step and records their own confirmation. You cannot confirm clearance and
  the server will refuse if you try. Point them to the app screen; do not argue with the hold.
- No medical advice, no diagnosis, no promises about results. If they mention pregnancy, an eating
  disorder, chest pain, dizziness or new medication, tell them to talk to their doctor before changing
  how they train or eat, and leave the plan as it is.

## Same account everywhere

The home-screen app, a browser tab and you all read the same account. A set logged here shows in the
app at once. If they ask for the app link, it is their app address; the `axiom-coach:connect` skill
lists how to put it on a home screen.
