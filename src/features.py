DEMOGRAPHICS = [
    "Age",
    "Gender",
    "Ethnicity",
    "EducationLevel",
]

LIFESTYLE = [
    "BMI",
    "Smoking",
    "AlcoholConsumption",
    "PhysicalActivity",
    "DietQuality",
    "SleepQuality",
]

MEDICAL_HISTORY = [
    "FamilyHistoryAlzheimers",
    "CardiovascularDisease",
    "Diabetes",
    "Depression",
    "HeadInjury",
    "Hypertension",
]

VITALS = [
    "SystolicBP",
    "DiastolicBP",
    "CholesterolTotal",
    "CholesterolLDL",
    "CholesterolHDL",
    "CholesterolTriglycerides",
]

CLINICAL = [
    "MMSE",
    "FunctionalAssessment",
    "ADL",
    "MemoryComplaints",
    "BehavioralProblems",
    "Confusion",
    "Disorientation",
    "PersonalityChanges",
    "DifficultyCompletingTasks",
    "Forgetfulness",
]

TARGET = "Diagnosis"

FEATURE_SETS = {
    "demografi": DEMOGRAPHICS,
    "livsstil": LIFESTYLE,
    "sjukdomshistorik": MEDICAL_HISTORY,
    "kliniskt": CLINICAL,
    "allt": DEMOGRAPHICS + LIFESTYLE + MEDICAL_HISTORY + VITALS + CLINICAL,
}