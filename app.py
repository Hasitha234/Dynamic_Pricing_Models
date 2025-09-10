from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
from pricing_utils import pricing_policy   # ✅ use policy wrapper only

# Load trained model + features
demand_model = joblib.load("demand_model.pkl")
feature_cols = joblib.load("feature_cols.pkl")

app = Flask(__name__)



@app.route("/get_price", methods=["POST"])
def get_price():
    data = request.get_json()
    print("🔍 Received JSON:", data)

    if "data" in data:
        route_df = pd.DataFrame(data["data"])
    else:
        route_df = pd.DataFrame([data])

    # Extract values
    origin = route_df.iloc[0]["origin"]
    destination = route_df.iloc[0]["destination"]
    price = float(route_df.iloc[0]["price"])

    # --- Enrichment ---
    # Simulate demand elasticity (fewer passengers if price is too high)
    base_demand = 200  
    elasticity = -0.05  
    demand = max(50, base_demand + elasticity * (price - 300))

    # Competitor pricing simulation
    competitor_price = np.random.randint(280, 360)

    # Revenue calculations
    current_revenue = price * demand
    optimal_price = (competitor_price + price) / 2  # naive strategy
    optimal_demand = base_demand + elasticity * (optimal_price - 300)
    optimal_revenue = optimal_price * optimal_demand

    result = {
        "route": f"{origin} → {destination}",
        "avg_price": price,
        "competitor_price": competitor_price,
        "estimated_demand": demand,
        "current_revenue": current_revenue,
        "optimal_price": round(optimal_price, 2),
        "optimal_revenue": round(optimal_revenue, 2),
        "uplift_%": ((optimal_revenue - current_revenue) / current_revenue) * 100
    }

    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True, port=5000)
