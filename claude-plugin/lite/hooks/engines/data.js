// Generated from lite/training_split.py, lite/meal_plan.py and lite/cardio_calc.py by
// claude-plugin/tests/gen_lite_data.py. Do not edit by hand; run the generator.
// Numbers and tables are those of the open Lite app's engines (trainingSplit.ts, mealPlan.ts,
// cardioCalc.ts).

export const EQUIPMENT = [
  "full_gym",
  "dumbbells_only",
  "bodyweight_only",
  "home_gym_basic"
]

export const INJURIES = [
  "shoulder",
  "lower_back",
  "knee",
  "wrist",
  "hip"
]

export const DAYS_PER_WEEK = [
  2,
  3,
  4,
  5,
  6
]

export const SPLIT_DISCLAIMER = "This is a single-week starting template, not a progressive program. Consult a professional before starting if you have any medical concerns."

export const SUBSTITUTED_NOTE = "Substituted for flagged injury."

export const EXERCISE_TABLE = {
  "squat": {
    "full_gym": [
      [
        "Barbell Back Squat",
        [
          "knee",
          "lower_back"
        ]
      ],
      [
        "Leg Press",
        [
          "lower_back"
        ]
      ],
      [
        "Goblet Squat",
        []
      ]
    ],
    "dumbbells_only": [
      [
        "Dumbbell Goblet Squat",
        []
      ],
      [
        "Dumbbell Front Squat",
        [
          "wrist"
        ]
      ]
    ],
    "bodyweight_only": [
      [
        "Bodyweight Squat",
        []
      ],
      [
        "Tempo Bodyweight Squat",
        []
      ]
    ],
    "home_gym_basic": [
      [
        "Barbell Back Squat",
        [
          "knee",
          "lower_back"
        ]
      ],
      [
        "Goblet Squat",
        []
      ]
    ],
    "safe": "Wall Sit"
  },
  "hinge": {
    "full_gym": [
      [
        "Barbell Romanian Deadlift",
        [
          "lower_back"
        ]
      ],
      [
        "Cable Pull-Through",
        []
      ],
      [
        "Glute Bridge",
        []
      ]
    ],
    "dumbbells_only": [
      [
        "Dumbbell Romanian Deadlift",
        [
          "lower_back"
        ]
      ],
      [
        "Dumbbell Glute Bridge",
        []
      ]
    ],
    "bodyweight_only": [
      [
        "Single-Leg Glute Bridge",
        []
      ],
      [
        "Bodyweight Good Morning",
        [
          "lower_back"
        ]
      ]
    ],
    "home_gym_basic": [
      [
        "Barbell Romanian Deadlift",
        [
          "lower_back"
        ]
      ],
      [
        "Dumbbell Romanian Deadlift",
        [
          "lower_back"
        ]
      ],
      [
        "Glute Bridge",
        []
      ]
    ],
    "safe": "Glute Bridge"
  },
  "horizontal_push": {
    "full_gym": [
      [
        "Barbell Bench Press",
        [
          "shoulder",
          "wrist"
        ]
      ],
      [
        "Machine Chest Press",
        [
          "wrist"
        ]
      ],
      [
        "Push-Up",
        [
          "wrist"
        ]
      ]
    ],
    "dumbbells_only": [
      [
        "Dumbbell Bench Press",
        [
          "shoulder",
          "wrist"
        ]
      ],
      [
        "Dumbbell Floor Press",
        [
          "shoulder"
        ]
      ]
    ],
    "bodyweight_only": [
      [
        "Push-Up",
        [
          "wrist"
        ]
      ],
      [
        "Incline Push-Up",
        [
          "wrist"
        ]
      ]
    ],
    "home_gym_basic": [
      [
        "Barbell Bench Press",
        [
          "shoulder",
          "wrist"
        ]
      ],
      [
        "Dumbbell Bench Press",
        [
          "shoulder",
          "wrist"
        ]
      ],
      [
        "Push-Up",
        [
          "wrist"
        ]
      ]
    ],
    "safe": "Incline Push-Up (knees down)"
  },
  "vertical_push": {
    "full_gym": [
      [
        "Barbell Overhead Press",
        [
          "shoulder"
        ]
      ],
      [
        "Machine Shoulder Press",
        [
          "shoulder"
        ]
      ],
      [
        "Dumbbell Seated Shoulder Press",
        [
          "shoulder"
        ]
      ]
    ],
    "dumbbells_only": [
      [
        "Dumbbell Seated Shoulder Press",
        [
          "shoulder"
        ]
      ],
      [
        "Dumbbell Arnold Press",
        [
          "shoulder"
        ]
      ]
    ],
    "bodyweight_only": [
      [
        "Pike Push-Up",
        [
          "shoulder",
          "wrist"
        ]
      ],
      [
        "Wall Handstand Hold",
        [
          "shoulder",
          "wrist"
        ]
      ]
    ],
    "home_gym_basic": [
      [
        "Barbell Overhead Press",
        [
          "shoulder"
        ]
      ],
      [
        "Dumbbell Seated Shoulder Press",
        [
          "shoulder"
        ]
      ]
    ],
    "safe": "Standing Band-Free Arm Raise Hold"
  },
  "horizontal_pull": {
    "full_gym": [
      [
        "Seated Cable Row",
        [
          "lower_back"
        ]
      ],
      [
        "Chest-Supported Machine Row",
        []
      ],
      [
        "Inverted Row",
        []
      ]
    ],
    "dumbbells_only": [
      [
        "Dumbbell Bent-Over Row",
        [
          "lower_back"
        ]
      ],
      [
        "Single-Arm Dumbbell Row (bench supported)",
        []
      ]
    ],
    "bodyweight_only": [
      [
        "Inverted Row",
        []
      ],
      [
        "Doorframe Towel Row",
        []
      ]
    ],
    "home_gym_basic": [
      [
        "Barbell Bent-Over Row",
        [
          "lower_back"
        ]
      ],
      [
        "Dumbbell Bent-Over Row",
        [
          "lower_back"
        ]
      ],
      [
        "Inverted Row",
        []
      ]
    ],
    "safe": "Chest-Supported Row (bodyweight)"
  },
  "vertical_pull": {
    "full_gym": [
      [
        "Lat Pulldown",
        [
          "shoulder"
        ]
      ],
      [
        "Assisted Pull-Up Machine",
        [
          "shoulder"
        ]
      ],
      [
        "Pull-Up",
        [
          "shoulder"
        ]
      ]
    ],
    "dumbbells_only": [
      [
        "Dumbbell Pullover",
        [
          "shoulder"
        ]
      ],
      [
        "Dumbbell Renegade Row",
        [
          "wrist",
          "shoulder"
        ]
      ]
    ],
    "bodyweight_only": [
      [
        "Pull-Up",
        [
          "shoulder"
        ]
      ],
      [
        "Doorframe Row",
        []
      ]
    ],
    "home_gym_basic": [
      [
        "Pull-Up",
        [
          "shoulder"
        ]
      ],
      [
        "Band-Assisted Pull-Up",
        [
          "shoulder"
        ]
      ]
    ],
    "safe": "Scapular Retraction Hold"
  },
  "unilateral_leg": {
    "full_gym": [
      [
        "Walking Lunge",
        [
          "knee"
        ]
      ],
      [
        "Bulgarian Split Squat",
        [
          "knee",
          "hip"
        ]
      ],
      [
        "Step-Up",
        [
          "knee"
        ]
      ]
    ],
    "dumbbells_only": [
      [
        "Dumbbell Walking Lunge",
        [
          "knee"
        ]
      ],
      [
        "Dumbbell Bulgarian Split Squat",
        [
          "knee",
          "hip"
        ]
      ]
    ],
    "bodyweight_only": [
      [
        "Bodyweight Walking Lunge",
        [
          "knee"
        ]
      ],
      [
        "Bodyweight Step-Up",
        [
          "knee"
        ]
      ]
    ],
    "home_gym_basic": [
      [
        "Dumbbell Walking Lunge",
        [
          "knee"
        ]
      ],
      [
        "Dumbbell Bulgarian Split Squat",
        [
          "knee",
          "hip"
        ]
      ]
    ],
    "safe": "Standing Hip Hinge to Toe Tap"
  },
  "core": {
    "full_gym": [
      [
        "Plank",
        []
      ],
      [
        "Dead Bug",
        []
      ]
    ],
    "dumbbells_only": [
      [
        "Plank",
        []
      ],
      [
        "Dead Bug",
        []
      ]
    ],
    "bodyweight_only": [
      [
        "Plank",
        []
      ],
      [
        "Dead Bug",
        []
      ]
    ],
    "home_gym_basic": [
      [
        "Plank",
        []
      ],
      [
        "Dead Bug",
        []
      ]
    ],
    "safe": "Dead Bug"
  },
  "biceps": {
    "full_gym": [
      [
        "Cable Bicep Curl",
        [
          "wrist"
        ]
      ],
      [
        "Dumbbell Bicep Curl",
        [
          "wrist"
        ]
      ]
    ],
    "dumbbells_only": [
      [
        "Dumbbell Bicep Curl",
        [
          "wrist"
        ]
      ]
    ],
    "bodyweight_only": [
      [
        "Isometric Bicep Hold (towel curl)",
        []
      ]
    ],
    "home_gym_basic": [
      [
        "Dumbbell Bicep Curl",
        [
          "wrist"
        ]
      ]
    ],
    "safe": "Isometric Bicep Hold"
  },
  "triceps": {
    "full_gym": [
      [
        "Cable Triceps Pushdown",
        [
          "wrist",
          "shoulder"
        ]
      ],
      [
        "Dumbbell Overhead Triceps Extension",
        [
          "shoulder",
          "wrist"
        ]
      ]
    ],
    "dumbbells_only": [
      [
        "Dumbbell Overhead Triceps Extension",
        [
          "shoulder",
          "wrist"
        ]
      ],
      [
        "Dumbbell Skull Crusher",
        [
          "wrist",
          "shoulder"
        ]
      ]
    ],
    "bodyweight_only": [
      [
        "Bench Dip",
        [
          "shoulder",
          "wrist"
        ]
      ],
      [
        "Diamond Push-Up",
        [
          "wrist"
        ]
      ]
    ],
    "home_gym_basic": [
      [
        "Dumbbell Overhead Triceps Extension",
        [
          "shoulder",
          "wrist"
        ]
      ],
      [
        "Dumbbell Skull Crusher",
        [
          "wrist",
          "shoulder"
        ]
      ]
    ],
    "safe": "Triceps Kickback (bodyweight arm only)"
  },
  "calf": {
    "full_gym": [
      [
        "Standing Calf Raise",
        []
      ]
    ],
    "dumbbells_only": [
      [
        "Standing Calf Raise",
        []
      ]
    ],
    "bodyweight_only": [
      [
        "Standing Calf Raise",
        []
      ]
    ],
    "home_gym_basic": [
      [
        "Standing Calf Raise",
        []
      ]
    ],
    "safe": "Standing Calf Raise"
  },
  "rear_delt": {
    "full_gym": [
      [
        "Cable Face Pull",
        [
          "shoulder"
        ]
      ],
      [
        "Reverse Pec Deck",
        [
          "shoulder"
        ]
      ]
    ],
    "dumbbells_only": [
      [
        "Dumbbell Reverse Fly",
        [
          "shoulder"
        ]
      ]
    ],
    "bodyweight_only": [
      [
        "Prone Y-Raise",
        [
          "shoulder"
        ]
      ]
    ],
    "home_gym_basic": [
      [
        "Dumbbell Reverse Fly",
        [
          "shoulder"
        ]
      ]
    ],
    "safe": "Prone Y-Raise (light)"
  }
}

export const SPLIT_TABLE = {
  "2": {
    "name": "Full Body",
    "days": [
      {
        "focus": "Full Body",
        "slots": [
          {
            "pattern": "squat",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "horizontal_push",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "horizontal_pull",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "hinge",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      },
      {
        "focus": "Full Body",
        "slots": [
          {
            "pattern": "hinge",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_push",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_pull",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "unilateral_leg",
            "sets": 3,
            "reps": "10-12/leg"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      }
    ]
  },
  "3": {
    "name": "Full Body",
    "days": [
      {
        "focus": "Full Body",
        "slots": [
          {
            "pattern": "squat",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "horizontal_push",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "horizontal_pull",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "hinge",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      },
      {
        "focus": "Full Body",
        "slots": [
          {
            "pattern": "hinge",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_push",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_pull",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "unilateral_leg",
            "sets": 3,
            "reps": "10-12/leg"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      },
      {
        "focus": "Full Body",
        "slots": [
          {
            "pattern": "squat",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_push",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "horizontal_pull",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "hinge",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      }
    ]
  },
  "4": {
    "name": "Upper / Lower",
    "days": [
      {
        "focus": "Upper Body",
        "slots": [
          {
            "pattern": "horizontal_push",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "horizontal_pull",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_push",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_pull",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "biceps",
            "sets": 3,
            "reps": "10-15"
          },
          {
            "pattern": "triceps",
            "sets": 3,
            "reps": "10-15"
          }
        ]
      },
      {
        "focus": "Lower Body",
        "slots": [
          {
            "pattern": "squat",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "hinge",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "unilateral_leg",
            "sets": 3,
            "reps": "10-12/leg"
          },
          {
            "pattern": "calf",
            "sets": 4,
            "reps": "12-15"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      },
      {
        "focus": "Upper Body",
        "slots": [
          {
            "pattern": "vertical_push",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_pull",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "horizontal_push",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "horizontal_pull",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "triceps",
            "sets": 3,
            "reps": "10-15"
          },
          {
            "pattern": "rear_delt",
            "sets": 3,
            "reps": "12-15"
          }
        ]
      },
      {
        "focus": "Lower Body",
        "slots": [
          {
            "pattern": "hinge",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "squat",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "unilateral_leg",
            "sets": 3,
            "reps": "10-12/leg"
          },
          {
            "pattern": "calf",
            "sets": 4,
            "reps": "12-15"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      }
    ]
  },
  "5": {
    "name": "Push / Pull / Legs + Upper / Lower",
    "days": [
      {
        "focus": "Push",
        "slots": [
          {
            "pattern": "horizontal_push",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_push",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "triceps",
            "sets": 4,
            "reps": "10-15"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      },
      {
        "focus": "Pull",
        "slots": [
          {
            "pattern": "vertical_pull",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "horizontal_pull",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "rear_delt",
            "sets": 3,
            "reps": "12-15"
          },
          {
            "pattern": "biceps",
            "sets": 4,
            "reps": "10-15"
          }
        ]
      },
      {
        "focus": "Legs",
        "slots": [
          {
            "pattern": "squat",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "hinge",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "unilateral_leg",
            "sets": 3,
            "reps": "10-12/leg"
          },
          {
            "pattern": "calf",
            "sets": 4,
            "reps": "12-15"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      },
      {
        "focus": "Upper Body",
        "slots": [
          {
            "pattern": "horizontal_push",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "horizontal_pull",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_push",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_pull",
            "sets": 3,
            "reps": "8-12"
          },
          {
            "pattern": "biceps",
            "sets": 3,
            "reps": "10-15"
          },
          {
            "pattern": "triceps",
            "sets": 3,
            "reps": "10-15"
          }
        ]
      },
      {
        "focus": "Lower Body",
        "slots": [
          {
            "pattern": "squat",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "hinge",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "unilateral_leg",
            "sets": 3,
            "reps": "10-12/leg"
          },
          {
            "pattern": "calf",
            "sets": 4,
            "reps": "12-15"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      }
    ]
  },
  "6": {
    "name": "Push / Pull / Legs (x2)",
    "days": [
      {
        "focus": "Push",
        "slots": [
          {
            "pattern": "horizontal_push",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_push",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "triceps",
            "sets": 4,
            "reps": "10-15"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      },
      {
        "focus": "Pull",
        "slots": [
          {
            "pattern": "vertical_pull",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "horizontal_pull",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "rear_delt",
            "sets": 3,
            "reps": "12-15"
          },
          {
            "pattern": "biceps",
            "sets": 4,
            "reps": "10-15"
          }
        ]
      },
      {
        "focus": "Legs",
        "slots": [
          {
            "pattern": "squat",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "hinge",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "unilateral_leg",
            "sets": 3,
            "reps": "10-12/leg"
          },
          {
            "pattern": "calf",
            "sets": 4,
            "reps": "12-15"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      },
      {
        "focus": "Push",
        "slots": [
          {
            "pattern": "horizontal_push",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "vertical_push",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "triceps",
            "sets": 4,
            "reps": "10-15"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      },
      {
        "focus": "Pull",
        "slots": [
          {
            "pattern": "vertical_pull",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "horizontal_pull",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "rear_delt",
            "sets": 3,
            "reps": "12-15"
          },
          {
            "pattern": "biceps",
            "sets": 4,
            "reps": "10-15"
          }
        ]
      },
      {
        "focus": "Legs",
        "slots": [
          {
            "pattern": "squat",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "hinge",
            "sets": 4,
            "reps": "8-12"
          },
          {
            "pattern": "unilateral_leg",
            "sets": 3,
            "reps": "10-12/leg"
          },
          {
            "pattern": "calf",
            "sets": 4,
            "reps": "12-15"
          },
          {
            "pattern": "core",
            "sets": 3,
            "reps": "30-45s"
          }
        ]
      }
    ]
  }
}

export const SEXES = [
  "male",
  "female"
]

export const ACTIVITY_FACTORS = {
  "sedentary": 1.2,
  "light": 1.375,
  "moderate": 1.55,
  "very_active": 1.725
}

export const GOAL_ADJUSTMENT_KCAL = {
  "fat_loss": -500,
  "maintenance": 0,
  "muscle_gain": 300
}

export const PROTEIN_G_PER_KG = 2.1

export const FAT_FLOOR_G_PER_KG = 0.5

export const FAT_FLOOR_PCT_OF_CALORIES = 0.25

export const CALORIE_FLOOR = {
  "female": 1300,
  "male": 1600
}

export const MEAL_SPLIT = [
  "Meal 1",
  "Meal 2",
  "Meal 3",
  "Snack"
]

export const MEAL_DESCRIPTION = "Lean protein source + complex carbohydrate + vegetables (portion to hit daily macro targets)."

export const BLOCKED_REASON = "We can't safely auto-generate a nutrition plan based on what you told us. Please consult a qualified health professional before starting a calorie or macro plan."

export const MEAL_DISCLAIMER = "Estimates based on the Mifflin-St Jeor equation. Not medical advice. Adjust based on real-world progress."

export const MODALITIES = [
  "treadmill",
  "elliptical",
  "stationary_bike",
  "stair_climber",
  "rower"
]

export const INTENSITIES = [
  "low",
  "moderate",
  "high"
]

export const MPH_TO_M_PER_MIN = 26.8224

export const WALK_RUN_THRESHOLD_MPH = 4.3

export const MET_TABLE = {
  "elliptical": {
    "low": 4.6,
    "moderate": 5.0,
    "high": 7.0
  },
  "stationary_bike": {
    "low": 3.5,
    "moderate": 6.8,
    "high": 10.5
  },
  "stair_climber": {
    "low": 4.0,
    "moderate": 8.0,
    "high": 9.8
  },
  "rower": {
    "low": 3.5,
    "moderate": 7.0,
    "high": 12.0
  }
}

export const TREADMILL_INTENSITY_MET = {
  "low": 3.5,
  "moderate": 6.0,
  "high": 9.8
}

export const CARDIO_DISCLAIMER = "Estimate only, based on standard MET formulas. Not a medical-grade measurement."
