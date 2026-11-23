// Generated from lite/training_split.py, lite/meal_plan.py and lite/cardio_calc.py by
// claude-plugin/tests/gen_lite_data.py. Do not edit by hand; run the generator.
// Numbers and tables are those of the open Lite app's engines (trainingSplit.ts, mealPlan.ts,
// cardioCalc.ts).

export const SPLIT_TOOL = {
  "name": "axiom_lite_split",
  "description": "Lite training split: one starting week of training for 2-6 days a week, by equipment, swapping out exercises that load a flagged injury. Rule based and local: no account, no network. Show the person the disclaimer and the education line with the result.",
  "inputSchema": {
    "type": "object",
    "additionalProperties": false,
    "required": [
      "days_per_week",
      "equipment"
    ],
    "properties": {
      "days_per_week": {
        "type": "integer",
        "enum": [
          2,
          3,
          4,
          5,
          6
        ]
      },
      "equipment": {
        "type": "string",
        "enum": [
          "full_gym",
          "dumbbells_only",
          "bodyweight_only",
          "home_gym_basic"
        ]
      },
      "injuries": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": [
            "shoulder",
            "lower_back",
            "knee",
            "wrist",
            "hip"
          ]
        },
        "description": "Areas the person says to protect. Empty if none."
      }
    }
  }
}

export const MACROS_TOOL = {
  "name": "axiom_lite_macros",
  "description": "Lite macro calculator: daily calorie, protein, fat and carb targets (Mifflin-St Jeor) and a one-week meal structure. Local, no network. health_screen must hold the person's own answers to the five questions, asked word for word; never fill one in for them. Any yes returns no targets and points to a health professional. Estimates, not medical advice.",
  "inputSchema": {
    "type": "object",
    "additionalProperties": false,
    "required": [
      "sex",
      "age_years",
      "activity_level",
      "goal",
      "health_screen"
    ],
    "properties": {
      "sex": {
        "type": "string",
        "enum": [
          "male",
          "female"
        ]
      },
      "age_years": {
        "type": "number",
        "minimum": 13,
        "maximum": 90
      },
      "height_cm": {
        "type": "number",
        "description": "Height in cm (121.9-241.3). Or give height_ft and height_in."
      },
      "height_ft": {
        "type": "integer",
        "minimum": 4,
        "maximum": 7
      },
      "height_in": {
        "type": "number",
        "minimum": 0,
        "maximum": 11
      },
      "weight_kg": {
        "type": "number",
        "description": "Body weight in kg (36.3-249.5). Or give weight_lb."
      },
      "weight_lb": {
        "type": "number",
        "minimum": 80,
        "maximum": 550
      },
      "activity_level": {
        "type": "string",
        "enum": [
          "sedentary",
          "light",
          "moderate",
          "very_active"
        ]
      },
      "goal": {
        "type": "string",
        "enum": [
          "fat_loss",
          "maintenance",
          "muscle_gain"
        ]
      },
      "health_screen": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "heart_condition",
          "chest_pain_during_activity",
          "pregnant_or_nursing",
          "eating_disorder",
          "metabolic_medication"
        ],
        "description": "The person's own yes/no answers. Ask each question exactly as written.",
        "properties": {
          "heart_condition": {
            "type": "boolean",
            "description": "Has a doctor ever told you that you have a heart condition?"
          },
          "chest_pain_during_activity": {
            "type": "boolean",
            "description": "Do you have chest pain during physical activity?"
          },
          "pregnant_or_nursing": {
            "type": "boolean",
            "description": "Are you currently pregnant or nursing?"
          },
          "eating_disorder": {
            "type": "boolean",
            "description": "Do you have a diagnosed eating disorder, current or in recovery?"
          },
          "metabolic_medication": {
            "type": "boolean",
            "description": "Are you on medication that affects metabolism, heart rate, or blood sugar?"
          }
        }
      }
    }
  }
}

export const CARDIO_TOOL = {
  "name": "axiom_lite_cardio",
  "description": "Lite cardio calculator: estimated calories for a cardio session from standard MET formulas (ACSM treadmill equations when a speed or a distance is given). Local, no network. An estimate, not a medical-grade measurement.",
  "inputSchema": {
    "type": "object",
    "additionalProperties": false,
    "required": [
      "modality",
      "duration_minutes",
      "intensity"
    ],
    "properties": {
      "modality": {
        "type": "string",
        "enum": [
          "treadmill",
          "elliptical",
          "stationary_bike",
          "stair_climber",
          "rower"
        ]
      },
      "sex": {
        "type": "string",
        "enum": [
          "male",
          "female"
        ]
      },
      "height_cm": {
        "type": "number",
        "description": "Height in cm (121.9-241.3). Or give height_ft and height_in."
      },
      "height_ft": {
        "type": "integer",
        "minimum": 4,
        "maximum": 7
      },
      "height_in": {
        "type": "number",
        "minimum": 0,
        "maximum": 11
      },
      "weight_kg": {
        "type": "number",
        "description": "Body weight in kg (36.3-249.5). Or give weight_lb."
      },
      "weight_lb": {
        "type": "number",
        "minimum": 80,
        "maximum": 550
      },
      "duration_minutes": {
        "type": "number",
        "minimum": 1,
        "maximum": 600
      },
      "intensity": {
        "type": "string",
        "enum": [
          "low",
          "moderate",
          "high"
        ]
      },
      "speed_mph": {
        "type": "number",
        "minimum": 0.5,
        "maximum": 15
      },
      "distance_miles": {
        "type": "number",
        "minimum": 0.1,
        "maximum": 100,
        "description": "Instead of speed_mph; speed is worked out from the duration."
      },
      "incline_percent": {
        "type": "number",
        "minimum": 0,
        "maximum": 15,
        "description": "Treadmill only."
      }
    }
  }
}
