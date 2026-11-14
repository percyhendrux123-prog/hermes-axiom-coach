// Exports TS engine outputs as a parity fixture for the Python ports.
// Inputs: every input used in the 44 vitest cases plus a wider grid.
import { generateTrainingProgram } from "./trainingSplit.ts";
import { generateMealPlan, calculateMacros } from "./mealPlan.ts";
import { calculateCardioCalories } from "./cardioCalc.ts";
import { writeFileSync } from "node:fs";

const INJ = ["shoulder", "lower_back", "knee", "wrist", "hip"] as const;
const EQ = ["full_gym", "dumbbells_only", "bodyweight_only", "home_gym_basic"] as const;
const training: any[] = [];
for (const d of [2, 3, 4, 5, 6] as const)
  for (const e of EQ)
    for (let m = 0; m < 32; m++) {
      const injuries = INJ.filter((_, i) => Math.floor(m / 2 ** i) % 2 === 1);
      const input = { daysPerWeek: d, equipment: e, injuries: [...injuries] };
      training.push({ input, output: generateTrainingProgram(input as any) });
    }

const meal: any[] = [];
const people = [
  [30, 180, 85], [28, 165, 60], [60, 150, 45], [45, 160, 55], [45, 150, 42],
  [13, 121.92, 36.28738], [90, 241.3, 249.4758], [35, 177.8, 79.83226],
  [22, 170.18, 61.23497], [50, 190, 120], [40, 175.26, 90.718474], [19, 162.56, 50.802345],
  [33, 168, 71.5], [27, 183, 77.1],
];
for (const sex of ["male", "female"])
  for (const act of ["sedentary", "light", "moderate", "very_active"])
    for (const goal of ["fat_loss", "maintenance", "muscle_gain"])
      for (const [a, h, w] of people)
        for (const hf of [false, true]) {
          const input = { sex, ageYears: a, heightCm: h, weightKg: w, activityLevel: act, goal, healthFlags: hf };
          meal.push({ input, output: generateMealPlan(input as any), macros: calculateMacros(input as any) });
        }

const cardio: any[] = [];
const bodies = [
  ["male", 178, 80], ["female", 165, 70], ["male", 180, 60], ["female", 160, 100],
  ["male", 150, 36.28738], ["female", 241.3, 249.4758], ["male", 175, 77.3],
];
for (const mod of ["treadmill", "elliptical", "stationary_bike", "stair_climber", "rower"])
  for (const it of ["low", "moderate", "high"])
    for (const [s, h, w] of bodies)
      for (const dur of [1, 30, 45, 60, 90, 37]) {
        const variants: any[] = [{}];
        if (mod === "treadmill")
          variants.push(
            { speedMph: 3 }, { speedMph: 4.3 }, { speedMph: 4.31 },
            { speedMph: 6, inclinePercent: 5 }, { speedMph: 2.5, inclinePercent: 15 },
            { distanceMiles: 2.5 }, { distanceMiles: 1.5, inclinePercent: 3 },
            { speedMph: 5, distanceMiles: 10 }, { speedMph: 3.7, inclinePercent: 7.5 },
          );
        else variants.push({ speedMph: 12 });
        for (const v of variants) {
          const input = { modality: mod, sex: s, heightCm: h, weightKg: w, durationMinutes: dur, intensity: it, ...v };
          cardio.push({ input, output: calculateCardioCalories(input as any) });
        }
      }

writeFileSync(
  process.argv[2],
  JSON.stringify({ source: "pkfit-lite-open@86d86b7 src/lib engines, exported with node --experimental-strip-types", training, meal, cardio }),
);
console.log(training.length, meal.length, cardio.length);
