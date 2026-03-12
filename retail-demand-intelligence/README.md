# Retail Demand Intelligence & Decision Optimization System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![LightGBM](https://img.shields.io/badge/Model-LightGBM-green)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)
![MLflow](https://img.shields.io/badge/Experiment-MLflow-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Project-Active-success)

A **machine learning–driven demand forecasting and inventory optimization system** designed to help retailers make better stocking decisions, reduce stockouts, and minimize excess inventory.

This project demonstrates a **full end-to-end data science system**, including:

* Data pipelines
* Feature engineering
* Machine learning forecasting
* Inventory optimization
* Business impact simulation
* Explainable AI
* Interactive dashboards
* Model monitoring

---

# Project Overview

Retail demand fluctuates due to:

* promotions
* holidays
* seasonality
* local shopping behavior

Traditional methods like **moving averages or manual planning** fail to capture these patterns.

This system uses **machine learning forecasting + inventory optimization** to generate intelligent stocking recommendations.

### Key Outcomes

* Improved demand forecast accuracy
* Reduced stockouts
* Lower inventory holding costs
* Data-driven retail decision making

---

# System Architecture

```
Raw Data Sources
      ↓
Data Ingestion Pipeline
      ↓
Processed Dataset
      ↓
Feature Engineering Pipeline
      ↓
Machine Learning Training Pipeline
      ↓
Trained Forecast Model
      ↓
Forecasting Service
      ↓
Inventory Optimization Engine
      ↓
Decision Impact Simulation
      ↓
Business Dashboard
      ↓
Monitoring & Logging
```

---

# Example Dashboard

*(Example placeholder — replace with screenshots later)*

```
Forecast vs Actual Sales
Inventory Recommendation
Demand Drivers
Model Performance
```

Example:

```
Product: Milk
Forecast: 135 units
Recommended Stock: 160 units
```

---

# Dataset

This project uses the **M5 Forecasting Dataset**, a widely used retail demand forecasting dataset.

Dataset characteristics:

* daily sales data
* multiple stores
* multiple products
* promotions and pricing
* calendar events

Dataset components:

| File        | Description       |
| ----------- | ----------------- |
| sales_train | historical sales  |
| calendar    | holidays & events |
| sell_prices | product prices    |

---

# Machine Learning Pipeline

### Feature Engineering

Features used for forecasting include:

| Feature        | Description       |
| -------------- | ----------------- |
| lag_7          | sales 7 days ago  |
| lag_14         | sales 14 days ago |
| lag_28         | sales 28 days ago |
| rolling_mean_7 | weekly average    |
| rolling_std_14 | demand volatility |
| week_of_year   | seasonality       |

Additional signals:

* promotions
* holidays
* weekend indicators

---

### Models Evaluated

| Model             | Role             |
| ----------------- | ---------------- |
| Linear Regression | baseline         |
| Random Forest     | benchmark        |
| LightGBM          | production model |

Primary model:

**LightGBM Gradient Boosting**

Evaluation metrics:

* MAE
* RMSE
* MAPE

Target:

```
MAPE < 15%
```

---

# Inventory Optimization

The system converts demand forecasts into stocking recommendations.

### Inventory Formula

```
Recommended Inventory =
Predicted Demand + Safety Stock
```

### Safety Stock

```
Safety Stock = Z × demand_std × √lead_time
```

Where:

* **Z** = service level factor
* **demand_std** = demand variability
* **lead_time** = replenishment delay

Example output:

| Product | Forecast | Recommended Stock |
| ------- | -------- | ----------------- |
| Milk    | 135      | 160               |
| Bread   | 82       | 95                |

---

# Decision Impact Simulation

The system evaluates **business impact** of ML-based inventory planning.

### Baseline Strategy

```
Next Week Stock =
Average Sales Last 4 Weeks
```

### ML Strategy

```
Next Week Stock =
Forecast + Safety Stock
```

### Example Results

| Strategy  | Stockouts | Overstock | Cost  |
| --------- | --------- | --------- | ----- |
| Baseline  | 18%       | 24%       | $145k |
| ML System | 11%       | 15%       | $98k  |

---

# Explainable AI

Predictions are explained using **SHAP values**.

Example demand drivers:

| Feature   | Impact      |
| --------- | ----------- |
| Promotion | +40% demand |
| Weekend   | +18% demand |
| Holiday   | +25% demand |

Benefits:

* interpretability
* business trust
* actionable insights

---

# Forecast API

The system exposes a simple forecasting endpoint.

### Endpoint

```
POST /forecast
```

### Input

```
{
  "store_id": "store_1",
  "product_id": "milk",
  "date": "2024-01-15"
}
```

### Output

```
{
  "predicted_demand": 135,
  "recommended_stock": 160
}
```

Framework:

**FastAPI**

---

# Dashboard

The project includes an interactive **Streamlit dashboard**.

Features:

* Demand forecast visualization
* Inventory recommendation table
* Demand driver insights
* Model performance monitoring

Run locally:

```
streamlit run dashboard/app.py
```

---

# Model Monitoring

Model performance is tracked over time.

Key metrics:

| Metric           | Purpose                    |
| ---------------- | -------------------------- |
| weekly_MAE       | forecast accuracy          |
| prediction_bias  | systematic error           |
| data_drift_score | feature distribution shift |

Retraining rule:

```
If MAPE > threshold → retrain model
```

---

# Project Structure

```
retail-demand-intelligence/

data/
notebooks/

src/
    data_pipeline.py
    feature_engineering.py
    train_model.py
    forecasting.py
    inventory_optimizer.py
    business_simulation.py
    monitoring.py

dashboard/
    app.py

models/
logs/
reports/

README.md
```

---

# Tech Stack

| Component           | Technology |
| ------------------- | ---------- |
| Programming         | Python     |
| Data Processing     | Pandas     |
| Machine Learning    | LightGBM   |
| Visualization       | Streamlit  |
| Experiment Tracking | MLflow     |
| API                 | FastAPI    |
| Testing             | Pytest     |
| Version Control     | Git        |

---

# Installation

Clone the repository:

```
git clone https://github.com/yourusername/retail-demand-intelligence.git
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Running the Project

### Train Model

```
python src/train_model.py
```

### Generate Forecasts

```
python src/forecasting.py
```

### Run Dashboard

```
streamlit run dashboard/app.py
```

---

# Testing

Run tests using:

```
pytest
```

---

# Future Improvements

Potential enhancements:

* hierarchical demand forecasting
* deep learning time-series models (LSTM / Transformer)
* reinforcement learning inventory policies
* automated retraining pipelines
* cloud deployment (AWS / GCP)

---

# License

MIT License

---

# Author

Data Science Portfolio Project

Built to demonstrate:

* machine learning system design
* demand forecasting
* decision optimization
* production-style ML pipelines
