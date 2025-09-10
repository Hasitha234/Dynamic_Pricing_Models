import streamlit as st
import requests

st.title("✈️ Dynamic Pricing Recommendation Engine")

origin = st.text_input("Origin City", "Los Angeles, CA (Metropolitan Area)")
destination = st.text_input("Destination City", "New York City, NY (Metropolitan Area)")
price = st.number_input("Current Average Price ($)", min_value=50, value=320)

if st.button("Get Recommendation"):
    payload = {
        "origin": origin,
        "destination": destination,
        "price": price
    }

    try:
        response = requests.post("http://127.0.0.1:5000/get_price", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Recommendation Retrieved!")

            st.write(f"**Route:** {result['route']}")
            st.metric("Competitor Price", f"${result['competitor_price']}")
            st.metric("Estimated Demand", f"{result['estimated_demand']:.0f} passengers")
            st.metric("Current Revenue", f"${result['current_revenue']:.2f}")
            st.metric("Optimal Price", f"${result['optimal_price']}")
            st.metric("Optimal Revenue", f"${result['optimal_revenue']:.2f}")
            st.metric("Revenue Uplift (%)", f"{result['uplift_%']:.2f}%")

        else:
            st.error("❌ API request failed")
    except Exception as e:
        st.error(f"Request error: {e}")
