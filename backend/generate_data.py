import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate Disease Data for 48 Wards of Solapur
np.random.seed(42)

wards = [f"Ward {i}" for i in range(1, 49)]
diseases = ["Dengue", "Malaria", "Typhoid", "Cholera", "COVID-19", "TB"]
dates = [(datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(90, 0, -1)]

disease_records = []
for date in dates:
    for ward in wards:
        for disease in np.random.choice(diseases, 2):  # 2 diseases per ward per day
            cases = np.random.randint(0, 30)
            disease_records.append({
                "date": date,
                "ward": ward,
                "disease": disease,
                "cases": cases
            })

disease_df = pd.DataFrame(disease_records)
disease_df.to_csv("data/disease_data.csv", index=False)

# Generate Hospital Data
hospitals = [
    {"hospital": "Civil Hospital Solapur", "ward": "Ward 15", "total_beds": 500, "available_beds": 120, "icu_beds": 20, "ventilators": 10},
    {"hospital": "District Hospital", "ward": "Ward 8", "total_beds": 300, "available_beds": 75, "icu_beds": 15, "ventilators": 5},
    {"hospital": "Ashwini Sahakari Hospital", "ward": "Ward 22", "total_beds": 200, "available_beds": 45, "icu_beds": 10, "ventilators": 3},
    {"hospital": "Primary Health Center 1", "ward": "Ward 3", "total_beds": 50, "available_beds": 12, "icu_beds": 0, "ventilators": 0},
    {"hospital": "Primary Health Center 2", "ward": "Ward 35", "total_beds": 50, "available_beds": 8, "icu_beds": 0, "ventilators": 0},
]

hospital_df = pd.DataFrame(hospitals)
hospital_df.to_csv("data/hospital_data.csv", index=False)

print("✅ Datasets created: disease_data.csv, hospital_data.csv")