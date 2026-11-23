# Training split tables

Source of truth for the `axiom-coach:lite` skill. Same rules as the open Lite app's training split.

## How an exercise is chosen

For each slot in a training day, look up its pattern and the person's equipment below. Take the
candidates in the order listed and use the first one that is not skipped by a flagged injury. If
every candidate is skipped, use the fallback for that pattern and add the note
`Substituted for flagged injury.` to that exercise. A later candidate chosen after an earlier one was
skipped carries no note; only the fallback does.

## Exercises by pattern and equipment

### squat

- full_gym: 1. Barbell Back Squat (skip if knee or lower_back is flagged); 2. Leg Press (skip if lower_back is flagged); 3. Goblet Squat (never skipped)
- home_gym_basic: 1. Barbell Back Squat (skip if knee or lower_back is flagged); 2. Goblet Squat (never skipped)
- dumbbells_only: 1. Dumbbell Goblet Squat (never skipped); 2. Dumbbell Front Squat (skip if wrist is flagged)
- bodyweight_only: 1. Bodyweight Squat (never skipped); 2. Tempo Bodyweight Squat (never skipped)
- fallback (all tiers): Wall Sit

### hinge

- full_gym: 1. Barbell Romanian Deadlift (skip if lower_back is flagged); 2. Cable Pull-Through (never skipped); 3. Glute Bridge (never skipped)
- home_gym_basic: 1. Barbell Romanian Deadlift (skip if lower_back is flagged); 2. Dumbbell Romanian Deadlift (skip if lower_back is flagged); 3. Glute Bridge (never skipped)
- dumbbells_only: 1. Dumbbell Romanian Deadlift (skip if lower_back is flagged); 2. Dumbbell Glute Bridge (never skipped)
- bodyweight_only: 1. Single-Leg Glute Bridge (never skipped); 2. Bodyweight Good Morning (skip if lower_back is flagged)
- fallback (all tiers): Glute Bridge

### horizontal_push

- full_gym: 1. Barbell Bench Press (skip if shoulder or wrist is flagged); 2. Machine Chest Press (skip if wrist is flagged); 3. Push-Up (skip if wrist is flagged)
- home_gym_basic: 1. Barbell Bench Press (skip if shoulder or wrist is flagged); 2. Dumbbell Bench Press (skip if shoulder or wrist is flagged); 3. Push-Up (skip if wrist is flagged)
- dumbbells_only: 1. Dumbbell Bench Press (skip if shoulder or wrist is flagged); 2. Dumbbell Floor Press (skip if shoulder is flagged)
- bodyweight_only: 1. Push-Up (skip if wrist is flagged); 2. Incline Push-Up (skip if wrist is flagged)
- fallback (all tiers): Incline Push-Up (knees down)

### vertical_push

- full_gym: 1. Barbell Overhead Press (skip if shoulder is flagged); 2. Machine Shoulder Press (skip if shoulder is flagged); 3. Dumbbell Seated Shoulder Press (skip if shoulder is flagged)
- home_gym_basic: 1. Barbell Overhead Press (skip if shoulder is flagged); 2. Dumbbell Seated Shoulder Press (skip if shoulder is flagged)
- dumbbells_only: 1. Dumbbell Seated Shoulder Press (skip if shoulder is flagged); 2. Dumbbell Arnold Press (skip if shoulder is flagged)
- bodyweight_only: 1. Pike Push-Up (skip if shoulder or wrist is flagged); 2. Wall Handstand Hold (skip if shoulder or wrist is flagged)
- fallback (all tiers): Standing Band-Free Arm Raise Hold

### horizontal_pull

- full_gym: 1. Seated Cable Row (skip if lower_back is flagged); 2. Chest-Supported Machine Row (never skipped); 3. Inverted Row (never skipped)
- home_gym_basic: 1. Barbell Bent-Over Row (skip if lower_back is flagged); 2. Dumbbell Bent-Over Row (skip if lower_back is flagged); 3. Inverted Row (never skipped)
- dumbbells_only: 1. Dumbbell Bent-Over Row (skip if lower_back is flagged); 2. Single-Arm Dumbbell Row (bench supported) (never skipped)
- bodyweight_only: 1. Inverted Row (never skipped); 2. Doorframe Towel Row (never skipped)
- fallback (all tiers): Chest-Supported Row (bodyweight)

### vertical_pull

- full_gym: 1. Lat Pulldown (skip if shoulder is flagged); 2. Assisted Pull-Up Machine (skip if shoulder is flagged); 3. Pull-Up (skip if shoulder is flagged)
- home_gym_basic: 1. Pull-Up (skip if shoulder is flagged); 2. Band-Assisted Pull-Up (skip if shoulder is flagged)
- dumbbells_only: 1. Dumbbell Pullover (skip if shoulder is flagged); 2. Dumbbell Renegade Row (skip if wrist or shoulder is flagged)
- bodyweight_only: 1. Pull-Up (skip if shoulder is flagged); 2. Doorframe Row (never skipped)
- fallback (all tiers): Scapular Retraction Hold

### unilateral_leg

- full_gym: 1. Walking Lunge (skip if knee is flagged); 2. Bulgarian Split Squat (skip if knee or hip is flagged); 3. Step-Up (skip if knee is flagged)
- home_gym_basic: 1. Dumbbell Walking Lunge (skip if knee is flagged); 2. Dumbbell Bulgarian Split Squat (skip if knee or hip is flagged)
- dumbbells_only: 1. Dumbbell Walking Lunge (skip if knee is flagged); 2. Dumbbell Bulgarian Split Squat (skip if knee or hip is flagged)
- bodyweight_only: 1. Bodyweight Walking Lunge (skip if knee is flagged); 2. Bodyweight Step-Up (skip if knee is flagged)
- fallback (all tiers): Standing Hip Hinge to Toe Tap

### core

- full_gym: 1. Plank (never skipped); 2. Dead Bug (never skipped)
- home_gym_basic: 1. Plank (never skipped); 2. Dead Bug (never skipped)
- dumbbells_only: 1. Plank (never skipped); 2. Dead Bug (never skipped)
- bodyweight_only: 1. Plank (never skipped); 2. Dead Bug (never skipped)
- fallback (all tiers): Dead Bug

### biceps

- full_gym: 1. Cable Bicep Curl (skip if wrist is flagged); 2. Dumbbell Bicep Curl (skip if wrist is flagged)
- home_gym_basic: 1. Dumbbell Bicep Curl (skip if wrist is flagged)
- dumbbells_only: 1. Dumbbell Bicep Curl (skip if wrist is flagged)
- bodyweight_only: 1. Isometric Bicep Hold (towel curl) (never skipped)
- fallback (all tiers): Isometric Bicep Hold

### triceps

- full_gym: 1. Cable Triceps Pushdown (skip if wrist or shoulder is flagged); 2. Dumbbell Overhead Triceps Extension (skip if shoulder or wrist is flagged)
- home_gym_basic: 1. Dumbbell Overhead Triceps Extension (skip if shoulder or wrist is flagged); 2. Dumbbell Skull Crusher (skip if wrist or shoulder is flagged)
- dumbbells_only: 1. Dumbbell Overhead Triceps Extension (skip if shoulder or wrist is flagged); 2. Dumbbell Skull Crusher (skip if wrist or shoulder is flagged)
- bodyweight_only: 1. Bench Dip (skip if shoulder or wrist is flagged); 2. Diamond Push-Up (skip if wrist is flagged)
- fallback (all tiers): Triceps Kickback (bodyweight arm only)

### calf

- full_gym: 1. Standing Calf Raise (never skipped)
- home_gym_basic: 1. Standing Calf Raise (never skipped)
- dumbbells_only: 1. Standing Calf Raise (never skipped)
- bodyweight_only: 1. Standing Calf Raise (never skipped)
- fallback (all tiers): Standing Calf Raise

### rear_delt

- full_gym: 1. Cable Face Pull (skip if shoulder is flagged); 2. Reverse Pec Deck (skip if shoulder is flagged)
- home_gym_basic: 1. Dumbbell Reverse Fly (skip if shoulder is flagged)
- dumbbells_only: 1. Dumbbell Reverse Fly (skip if shoulder is flagged)
- bodyweight_only: 1. Prone Y-Raise (skip if shoulder is flagged)
- fallback (all tiers): Prone Y-Raise (light)

## Split by days per week

### 2 days a week: Full Body

- Day 1 (Full Body): squat 3 x 8-12, horizontal_push 3 x 8-12, horizontal_pull 3 x 8-12, hinge 3 x 8-12, core 3 x 30-45s
- Day 2 (Full Body): hinge 3 x 8-12, vertical_push 3 x 8-12, vertical_pull 3 x 8-12, unilateral_leg 3 x 10-12/leg, core 3 x 30-45s

### 3 days a week: Full Body

- Day 1 (Full Body): squat 3 x 8-12, horizontal_push 3 x 8-12, horizontal_pull 3 x 8-12, hinge 3 x 8-12, core 3 x 30-45s
- Day 2 (Full Body): hinge 3 x 8-12, vertical_push 3 x 8-12, vertical_pull 3 x 8-12, unilateral_leg 3 x 10-12/leg, core 3 x 30-45s
- Day 3 (Full Body): squat 3 x 8-12, vertical_push 3 x 8-12, horizontal_pull 3 x 8-12, hinge 3 x 8-12, core 3 x 30-45s

### 4 days a week: Upper / Lower

- Day 1 (Upper Body): horizontal_push 4 x 8-12, horizontal_pull 4 x 8-12, vertical_push 3 x 8-12, vertical_pull 3 x 8-12, biceps 3 x 10-15, triceps 3 x 10-15
- Day 2 (Lower Body): squat 4 x 8-12, hinge 4 x 8-12, unilateral_leg 3 x 10-12/leg, calf 4 x 12-15, core 3 x 30-45s
- Day 3 (Upper Body): vertical_push 4 x 8-12, vertical_pull 4 x 8-12, horizontal_push 3 x 8-12, horizontal_pull 3 x 8-12, triceps 3 x 10-15, rear_delt 3 x 12-15
- Day 4 (Lower Body): hinge 4 x 8-12, squat 4 x 8-12, unilateral_leg 3 x 10-12/leg, calf 4 x 12-15, core 3 x 30-45s

### 5 days a week: Push / Pull / Legs + Upper / Lower

- Day 1 (Push): horizontal_push 4 x 8-12, vertical_push 4 x 8-12, triceps 4 x 10-15, core 3 x 30-45s
- Day 2 (Pull): vertical_pull 4 x 8-12, horizontal_pull 4 x 8-12, rear_delt 3 x 12-15, biceps 4 x 10-15
- Day 3 (Legs): squat 4 x 8-12, hinge 4 x 8-12, unilateral_leg 3 x 10-12/leg, calf 4 x 12-15, core 3 x 30-45s
- Day 4 (Upper Body): horizontal_push 4 x 8-12, horizontal_pull 4 x 8-12, vertical_push 3 x 8-12, vertical_pull 3 x 8-12, biceps 3 x 10-15, triceps 3 x 10-15
- Day 5 (Lower Body): squat 4 x 8-12, hinge 4 x 8-12, unilateral_leg 3 x 10-12/leg, calf 4 x 12-15, core 3 x 30-45s

### 6 days a week: Push / Pull / Legs (x2)

- Day 1 (Push): horizontal_push 4 x 8-12, vertical_push 4 x 8-12, triceps 4 x 10-15, core 3 x 30-45s
- Day 2 (Pull): vertical_pull 4 x 8-12, horizontal_pull 4 x 8-12, rear_delt 3 x 12-15, biceps 4 x 10-15
- Day 3 (Legs): squat 4 x 8-12, hinge 4 x 8-12, unilateral_leg 3 x 10-12/leg, calf 4 x 12-15, core 3 x 30-45s
- Day 4 (Push): horizontal_push 4 x 8-12, vertical_push 4 x 8-12, triceps 4 x 10-15, core 3 x 30-45s
- Day 5 (Pull): vertical_pull 4 x 8-12, horizontal_pull 4 x 8-12, rear_delt 3 x 12-15, biceps 4 x 10-15
- Day 6 (Legs): squat 4 x 8-12, hinge 4 x 8-12, unilateral_leg 3 x 10-12/leg, calf 4 x 12-15, core 3 x 30-45s
