from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime
import numpy as np
from sklearn.linear_model import LogisticRegression

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data

disease_df = pd.read_csv("../data/disease_data.csv")  
hospital_df = pd.read_csv("../data/hospital_data.csv") 
# Train AI Model
def train_outbreak_model():
    try:
        ward_stats = disease_df.groupby('ward')['cases'].agg(['sum', 'mean', 'max']).reset_index()
        X = ward_stats[['sum', 'mean', 'max']].values
        
        # Check if we have both classes before training
        y = (ward_stats['max'] > 20).astype(int).values
        if len(np.unique(y)) < 2:
            print("Warning: Only one class found, skipping model training")
            return None, ward_stats
        
        model = LogisticRegression()
        model.fit(X, y)
        return model, ward_stats
    except Exception as e:
        print(f"Model training failed: {e}")
        return None, None


model, ward_stats = train_outbreak_model()

@app.get("/")
def home():
    return {"message": "Smart Health Management System API - Solapur Municipal Corporation"}

@app.post("/add-case")
def add_case(ward: str, disease: str, cases: int):
    global disease_df
    new_row = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "ward": ward,
        "disease": disease,
        "cases": cases
    }
    disease_df = pd.concat([disease_df, pd.DataFrame([new_row])], ignore_index=True)
    
    disease_df.to_csv("../data/disease_data.csv", index=False)
    return {"status": "success", "message": "Case added"}

@app.get("/cases/{ward}")
def get_ward_cases(ward: str):
    ward_data = disease_df[disease_df['ward'] == ward].tail(30)
    return ward_data.to_dict(orient='records')

@app.get("/hospitals")
def get_hospitals():
    return hospital_df.to_dict(orient='records')

@app.get("/hospitals/{ward}")
def get_hospitals_by_ward(ward: str):
    ward_hospitals = hospital_df[hospital_df['ward'] == ward]
    return ward_hospitals.to_dict(orient='records')

@app.get("/predict-outbreak/{ward}")
def predict_outbreak(ward: str):
    ward_data = disease_df[disease_df['ward'] == ward]
    if ward_data.empty:
        raise HTTPException(status_code=404, detail="No data for this ward")
    
    total_cases = ward_data['cases'].sum()
    avg_cases = ward_data['cases'].mean()
    max_cases = ward_data['cases'].max()
    
    prediction = model.predict([[total_cases, avg_cases, max_cases]])
    risk = "High Risk" if prediction[0] == 1 else "Normal"
    
    return {
        "ward": ward,
        "total_cases": int(total_cases),
        "avg_daily_cases": round(avg_cases, 2),
        "max_cases": int(max_cases),
        "risk_level": risk
    }

@app.get("/dashboard-stats")
def dashboard_stats():
    total_cases = int(disease_df['cases'].sum())
    total_beds = int(hospital_df['total_beds'].sum())
    available_beds = int(hospital_df['available_beds'].sum())
    
    # High risk wards
    high_risk_wards = []
    for ward in disease_df['ward'].unique():
        ward_data = disease_df[disease_df['ward'] == ward]
        if ward_data['cases'].max() > 20:
            high_risk_wards.append(ward)
    
    return {
        "total_cases": total_cases,
        "total_beds": total_beds,
        "available_beds": available_beds,
        "high_risk_wards": high_risk_wards[:5]
    }