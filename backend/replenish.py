import pandas as pd
from predictor import predict_demand

def get_replenishment_plan(context, inventory_df):
    """
    Predict demand using the model and suggest how much to restock
    based on current kirana inventory.
    """

    # 🔧 Normalize columns
    inventory_df.columns = inventory_df.columns.str.strip().str.lower()
    inventory_df["sku"] = inventory_df["sku"].str.strip().str.lower()

    # ✅ 1. Predict demand
    predicted = predict_demand(context)["predictions"]  # list of {sku, predicted_demand}

    # ✅ 2. Create inventory lookup
    current_inventory = dict(zip(inventory_df["sku"], inventory_df["stock"]))

    replenishment_plan = []

    # ✅ 3. Match & calculate recommended quantity
    for item in predicted:
        sku = item["sku"].strip().lower()
        predicted_qty = item["predicted_demand"]
        current_qty = current_inventory.get(sku, 0)

        replenish_qty = max(predicted_qty - current_qty, 0)

        if replenish_qty > 0:
            replenishment_plan.append({
                "sku": sku,
                "predicted_demand": predicted_qty,
                "current_stock": current_qty,
                "recommended_qty": replenish_qty
            })

    # ✅ 4. Return full JSON structure
    return {
        "replenishment_plan": replenishment_plan
    }
