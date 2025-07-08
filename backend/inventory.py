import pandas as pd
from predictor import predict_demand  # Must return dict with key "predictions"

def analyze_kirana_inventory(district, month, festival_flag, income_level, kirana_density, inventory_df):
    """
    Compares kirana inventory with ML-predicted demand and returns SKU-wise status.
    """
    input_data = {
        "district": district,
        "month": month,
        "festival_flag": festival_flag,
        "income_level": income_level,
        "kirana_density": kirana_density
    }

    # Get predictions from model
    try:
        predicted = predict_demand(input_data)["predictions"]  # Ensure we get the list of dicts
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

    results = []

    # Normalize inventory input
    inventory_df["sku"] = inventory_df["sku"].str.strip().str.lower()

    for item in predicted:
        sku = item["sku"]
        demand = item["predicted_demand"]

        # Match with inventory
        match = inventory_df[inventory_df["sku"] == sku.lower()]
        stock = int(match.iloc[0]["stock"]) if not match.empty else 0

        # Status logic
        if stock == 0:
            status = "❌ Missing"
        elif stock < 0.3 * demand:
            status = "⚠️ Low"
        else:
            status = "✅ OK"

        results.append({
            "sku": sku,
            "predicted_demand": int(demand),
            "stock": stock,
            "status": status  # ✅ Must be lowercase
        })

    return {"analysis": results}
