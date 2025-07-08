from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from recommend import get_recommendations
from predictor import predict_demand
from inventory import analyze_kirana_inventory
from replenish import get_replenishment_plan  
from chatbot import ask_chatbot
from typing import Literal
from fastapi.responses import JSONResponse

import pandas as pd
import io

app = FastAPI()

# -------------------------------
# 🔗 CORS Configuration
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/districts")
def get_districts():
    df = pd.read_csv("data/districts.csv")  # Make sure path is correct
    districts = df["district"].dropna().unique().tolist()
    return {"districts": sorted(districts)}

# -------------------------------
# 1. Rule-Based SKU Recommendation
# -------------------------------
@app.get("/recommend")
def recommend(district: str, mode: str = "walmart_only"):
    return get_recommendations(district, mode)

# -------------------------------
# 2. ML-Based Demand Prediction
# -------------------------------
# Pydantic model (inline)
class DemandInput(BaseModel):
    district: str
    month: str
    festival_flag: int
    income_level: Literal["Low", "Medium", "High"]
    kirana_density: Literal["Low", "Medium", "High"]

# Route: cleanly return the full result as JSON
@app.post("/predict_demand")
def predict(input: DemandInput):
    input_dict = input.dict()
    results = predict_demand(input_dict)  # returns dict with predictions, metrics, feature_importance
    return results 

# -------------------------------
# 3. Inventory Gap Analyzer
# -------------------------------
@app.post("/analyze_inventory")
async def analyze_inventory(
    district: str = Form(...),
    month: str = Form(...),
    festival_flag: int = Form(...),
    income_level: str = Form(...),
    kirana_density: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        df = pd.read_csv(file.file)
        result = analyze_kirana_inventory(
            district, month, festival_flag, income_level, kirana_density, df
        )
        return result
    except Exception as e:
        return JSONResponse(content={"error": f"Server error: {str(e)}"}, status_code=500)

# -------------------------------
# 4. RAG-style Chatbot (Ollama)
# -------------------------------
@app.get("/chat")
def chat(q: str):
    answer = ask_chatbot(q)
    return {"response": answer}

# -------------------------------
# 5. Auto-Replenish Planner ✅
# -------------------------------
@app.post("/replenish")
async def replenish(
    district: str = Form(...),
    month: str = Form(...),
    festival_flag: int = Form(...),
    income_level: str = Form(...),
    kirana_density: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        df = pd.read_csv(file.file)
        context = {
            "district": district,
            "month": month,
            "festival_flag": festival_flag,
            "income_level": income_level,
            "kirana_density": kirana_density
        }
        result = get_replenishment_plan(context, df)
        return result  # ✅ JSON-safe
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


