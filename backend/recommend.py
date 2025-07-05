import pandas as pd
import os

# Adjust if you're running from another folder
DATA_PATH = os.path.join(os.path.dirname(__file__), '../data')

def get_recommendations(district, mode="walmart_only"):
    # Load data
    dist_df = pd.read_csv(os.path.join(DATA_PATH, 'districts.csv'))
    fest_df = pd.read_csv(os.path.join(DATA_PATH, 'festivals.csv'))
    sku_df = pd.read_csv(os.path.join(DATA_PATH, 'kirana_skus.csv'))

    # Get selected district data
    try:
        dist_info = dist_df[dist_df['district'].str.lower() == district.lower()].iloc[0]
    except IndexError:
        return {"error": f"District '{district}' not found"}

    # Upcoming festivals
    upcoming_fests = fest_df[fest_df['district'].str.lower() == district.lower()]['festival'].tolist()

    # Start recommendation list
    skus = []

    # Festival-based logic
    if any(fest in upcoming_fests for fest in ["Diwali", "Chhath Puja", "Navratri"]):
        skus += ["Sweets", "Lights", "Agarbatti"]

    if "Holi" in upcoming_fests:
        skus += ["Gulal (Colors)", "Snacks", "Thandai Mix"]

    if "Pongal" in upcoming_fests:
        skus += ["Jaggery", "Sambar Masala"]

    if "Ganesh Chaturthi" in upcoming_fests:
        skus += ["Modak", "Coconut"]

    # Income-based essentials
    if dist_info["income_level"] == "Low":
        skus += ["Rice (10kg)", "Washing Powder", "Tea Packets", "Sugar (1kg)"]
    elif dist_info["income_level"] == "Medium":
        skus += ["Poha (500g)", "Sandal Soap", "Besan (1kg)"]
    else:
        skus += ["Dairy Milk (small)", "Namkeen", "Sambar Masala"]

    # Remove SKUs if kiranas already stock them (if in coop mode)
    if mode == "coop":
        local_kirana_skus = sku_df[sku_df['district'].str.lower() == district.lower()]['sku'].tolist()
        skus = list(set(skus) - set(local_kirana_skus))  # Remove overlap

    # Return data
    return {
        "district": district,
        "population": int(dist_info["population"]),
        "kirana_density": dist_info["kirana_density"],
        "income_level": dist_info["income_level"],
        "mode": mode,
        "festivals": upcoming_fests,
        "recommended_skus": list(set(skus))
    }
