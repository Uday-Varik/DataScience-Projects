import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.model_diagnostics import (
    add_forecast_intervals,
    detect_demand_anomalies,
    compute_model_metrics
)

from src.model_diagnostics import (
    add_forecast_intervals,
    detect_demand_anomalies,
    compute_model_metrics,
    compute_demand_risk
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Retail Demand Intelligence",
    layout="wide"
)

st.title("Retail Demand Intelligence & Inventory Optimization")

# remove top spacing
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

inventory = pd.read_csv("reports/inventory_recommendations.csv")
impact = pd.read_csv("reports/business_impact_analysis.csv")

inventory["date"] = pd.to_datetime(inventory["date"])

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("Filters")

store = st.sidebar.selectbox(
    "Select Store",
    sorted(inventory["store_id"].unique())
)

product = st.sidebar.selectbox(
    "Select Product",
    sorted(inventory["item_id"].unique())
)

filtered = inventory[
    (inventory["store_id"] == store) &
    (inventory["item_id"] == product)
]

filtered = add_forecast_intervals(filtered)
filtered = detect_demand_anomalies(filtered)
filtered = compute_demand_risk(filtered)

# --------------------------------------------------
# KPI Metrics
# --------------------------------------------------
st.subheader("System-wide performance metrics")

baseline_cost = impact.loc[impact["strategy"]=="baseline","total_cost"].values[0]
ml_cost = impact.loc[impact["strategy"]=="ml_system","total_cost"].values[0]

savings = baseline_cost - ml_cost
percent = savings / baseline_cost * 100

stockouts = impact.loc[impact["strategy"]=="ml_system","stockouts"].values[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "ML System Cost",
    f"${ml_cost:,.0f}"
)

col2.metric(
    "Cost Savings",
    f"${savings:,.0f}",
    f"{percent:.1f}% improvement"
)

col3.metric(
    "Remaining Stockouts",
    f"{stockouts:,.0f}"
)

st.divider()

# -----------------------------------------------
## Selected Product Insights (Professional KPI Metrics)
# -----------------------------------------------
st.markdown("Selected Product Insights")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Sales",
    int(filtered["sales"].sum())
)

col2.metric(
    "Avg Predicted Demand",
    round(filtered["predicted_demand"].mean(),2)
)

col3.metric(
    "Avg Recommended Stock",
    round(filtered["recommended_stock"].mean(),2)
)

### Demand Risk Assessment KPI (Professional Feature)
st.subheader("Demand Risk Assessment")

avg_risk = filtered["risk_score"].mean()

col1, col2 = st.columns(2)

col1.metric(
    "Average Risk Score",
    f"{avg_risk:.1f}/100"
)

if avg_risk < 20:
    col2.success("Low Stockout Risk")

elif avg_risk < 50:
    col2.warning("Moderate Stock Risk")

else:
    col2.error("High Stockout Risk")


st.subheader("Demand Risk Over Time")


## Risk Visualization
fig_risk = px.line(
    filtered,
    x="date",
    y="risk_score",
    title="Stockout Risk Trend",
)
fig_risk.update_layout(height=350)
st.plotly_chart(fig_risk)


## High-risk days
high_risk = filtered[filtered["risk_score"] > 60]

if len(high_risk) > 0:

    st.warning("⚠ High Stockout Risk Detected")

    st.dataframe(
        high_risk[
            ["date","sales","predicted_demand","recommended_stock","risk_score"]
        ].tail(10)
    )

# --------------------------------------------------
# Tabs (Professional Dashboard Layout)
# --------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    ["Demand Forecast", "Inventory Intelligence", "Business Impact", "Model Monitoring"]
)

# ==================================================
# TAB 1 — DEMAND FORECAST
# ==================================================

with tab1:

    col1, col2 = st.columns([2,1])

    with col1:

        st.subheader("Demand Forecast vs Actual")

        fig = px.line(
            filtered,
            x="date",
            y=["sales","predicted_demand"],
            labels={"value":"Units","variable":"Legend"},
        )

        fig.update_layout(
            height=400,
            margin=dict(l=20,r=20,t=40,b=20)
        )

        st.plotly_chart(fig)

    with col2:

        st.subheader("Demand Insights")

        st.metric(
            "Average Demand",
            f"{filtered['sales'].mean():.2f}"
        )

        st.metric(
            "Peak Demand",
            f"{filtered['sales'].max():.0f}"
        )

        st.metric(
            "Avg Forecast",
            f"{filtered['predicted_demand'].mean():.2f}"
        )

# ==================================================
# TAB 2 — INVENTORY INTELLIGENCE
# ==================================================

with tab2:

    st.subheader("Inventory Recommendations")

    st.dataframe(
        filtered[
            [
                "date",
                "sales",
                "predicted_demand",
                "safety_stock",
                "recommended_stock"
            ]
        ].tail(20),
        height=350
    )

    st.divider()

    st.subheader("Inventory Risk Alerts")

    risk = filtered[
        filtered["recommended_stock"] < filtered["predicted_demand"]
    ]

    if len(risk) > 0:

        st.warning("⚠ Potential Stockout Risk Detected")

        st.dataframe(risk.tail(10), height=250)

    else:

        st.success("Inventory levels sufficient")

    st.divider()

    st.subheader("Top Overstock Products")

    inventory["overstock"] = inventory["recommended_stock"] - inventory["sales"]

    top_overstock = (
        inventory.groupby("item_id")["overstock"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig3 = px.bar(
        top_overstock,
        labels={"value":"Overstock Units","item_id":"Product"},
        title="Products With Highest Overstock Risk"
    )

    fig3.update_layout(height=350)

    st.plotly_chart(fig3)

# ==================================================
# TAB 3 — BUSINESS IMPACT
# ==================================================

with tab3:

    col1, col2 = st.columns([2,1])

    with col1:

        st.subheader("Total Inventory Cost Comparison")

        fig2 = px.bar(
            impact,
            x="strategy",
            y="total_cost",
            color="strategy",
            text="total_cost"
        )

        fig2.update_layout(
            showlegend=False,
            height=400
        )

        st.plotly_chart(fig2)

    with col2:

        st.subheader("Impact Summary")

        st.metric(
            "Baseline Cost",
            f"${baseline_cost:,.0f}"
        )

        st.metric(
            "ML System Cost",
            f"${ml_cost:,.0f}"
        )

        st.metric(
            "Total Savings",
            f"${savings:,.0f}"
        )

    st.divider()

    # Store heatmap (cool professional feature)

    st.subheader("Store Demand Heatmap")

    heatmap_data = (
        inventory.groupby(["store_id","date"])["sales"]
        .sum()
        .reset_index()
    )

    fig_heat = px.density_heatmap(
        heatmap_data,
        x="date",
        y="store_id",
        z="sales",
        color_continuous_scale="Blues"
    )

    fig_heat.update_layout(height=350)

    st.plotly_chart(fig_heat)


# ==================================================
# TAB 4 — MODEL MONITORING  
# ==================================================
with tab4:

    st.subheader("Model Monitoring")

    metrics = compute_model_metrics(filtered)

    col1, col2, col3 = st.columns(3)

    col1.metric("MAE", metrics["MAE"])
    col2.metric("MAPE (%)", metrics["MAPE"])
    col3.metric("RMSE", metrics["RMSE"])

    st.divider()

    st.subheader("Forecast Confidence Intervals")

    fig_ci = px.line(
        filtered,
        x="date",
        y=["predicted_demand","upper_ci","lower_ci"],
        title="Prediction Uncertainty"
    )

    fig_ci.update_layout(height=400)

    st.plotly_chart(fig_ci)

    st.divider()

    st.subheader("Demand Anomaly Detection")

    anomalies = filtered[filtered["anomaly"] == True]

    if len(anomalies) > 0:

        fig_anomaly = px.scatter(
            anomalies,
            x="date",
            y="sales",
            color="sales",
            title="Detected Demand Anomalies"
        )

        fig_anomaly.update_layout(height=350)

        st.plotly_chart(fig_anomaly)

        st.dataframe(anomalies)

    else:

        st.success("No demand anomalies detected")