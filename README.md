# mgta-452-final-project
Airline data : Weather patterns &amp; Airport Index-ing

# Aviation Operations Intelligence System  
### *Global Turbulence Analytics + Airport Efficiency Index*

## 1. Overview
This project aims to build a **comprehensive aviation analytics system** that analyzes and predicts key performance and safety metrics across global airspace and airports. It consists of two major interconnected modules:

1. **Global Turbulence Risk Analytics & Prediction**  
   Focuses on *in-air operational safety* and atmospheric risk patterns.

2. **Airport Efficiency Index (AEI)**  
   Measures and compares airport performance using a multi-factor operational index.

The combination of both modules provides a holistic view of aviation performance — covering **airborne safety** and **ground operational efficiency**, supported by strong visual analytics and machine learning models.

---

## 2. Motivation
Aviation systems generate massive amounts of data from weather, aircraft sensors, flight operations, delays, and airport infrastructure. However:

- Turbulence incidents are increasing globally.  
- Airports face congestion, delays, and operational inefficiencies.  
- Airlines need data-driven tools to enhance safety and efficiency.

By analyzing both **turbulence risk** and **airport efficiency**, this project addresses two of the most critical and resource-intensive challenges in modern aviation.

---

## 3. Project Goals

### A. Airborne Domain — Global Turbulence Analytics
- Identify turbulence hotspots across the world.  
- Visualize turbulence intensity by altitude, region, and season.  
- Build a machine learning model to **predict turbulence risk** based on weather and flight-level parameters.  
- Provide data-driven insights to improve route planning and flight safety.

### B. Ground Domain — Airport Efficiency Index
- Develop a composite **Airport Efficiency Index (AEI)** based on operational KPIs.  
- Compare airport performance on a global scale.  
- Visualize efficiency patterns using heatmaps, world maps, and multi-factor charts.  
- Build a model to **predict airport efficiency scores** and identify factors driving inefficiency.

---

## 4. Module 1 — Global Turbulence Risk Analytics

### 4.1 Purpose
To understand and predict turbulence occurrences using flight trajectory data, weather parameters, and atmospheric conditions.

### 4.2 Key Features
- Global turbulence heatmaps (latitude/longitude).  
- Vertical turbulence profiles by altitude.  
- Seasonal and regional turbulence trends.  
- Route-specific turbulence visualization.

### 4.3 Machine Learning Component

**Goal:** Predict turbulence severity (None, Light, Moderate, Severe).  

**Inputs may include:**  
- Wind speed & direction  
- Temperature gradients  
- Latitude, longitude  
- Pressure levels  
- Altitude (flight level)  
- Time of year  
- Aircraft type (optional)

**Methods:**  
- Random Forest Classifier  
- XGBoost / LightGBM  
- Multiclass classification  

**Output:**  
- Turbulence intensity class  
- Turbulence probability score  

---

## 5. Module 2 — Airport Efficiency Index (AEI)

### 5.1 Purpose
Build a global index to measure airport performance across operational, delay, and traffic metrics.

### 5.2 Components of the AEI
The index may combine (weighted or normalized):
- Average delay minutes  
- Taxi-in and taxi-out times  
- Runway throughput  
- Arrival on-time rate  
- Departure on-time rate  
- Weather disruption impact  
- Traffic volume vs capacity  
- Cancellation rates  

### 5.3 Key Visualizations
- Global airport efficiency map  
- Heatmap of efficiency components  
- KPI contribution charts  
- Airport ranking tables  
- Time-series performance trends  

### 5.4 Machine Learning Component

**Goal:** Predict the Airport Efficiency Index based on operational variables.

**Possible models:**
- Regression (Random Forest Regressor, Gradient Boosting)  
- Classification (High / Medium / Low efficiency)  
- Feature importance analysis  

**Output:**  
- Future AEI prediction  
- Identification of key drivers of inefficiency  

---

## 6. Why Both Modules Work Together
Although each module focuses on different domains, together they form a unified aviation intelligence system:

| Module | Focus Area | Benefit |
|--------|------------|----------|
| Turbulence Analytics | Airborne Safety | Reduces in-air risk, improves route planning |
| Efficiency Index | Ground Operations | Improves airport performance & reduces delays |

Combining them provides a **full operational picture** — from the sky to the runway.

---

## 7. Expected Deliverables
- Clean, reproducible dataset pipelines  
- Interactive visualizations (maps, heatmaps, dashboards)  
- Two ML models (turbulence prediction + AEI prediction)  
- Documentation explaining methodology and results  
- Insights and recommendations for improving safety and operational performance  

---

## 8. Final Objective
To produce an integrated aviation analytics system that uses data science, machine learning, and visualization to:

- Enhance flight safety  
- Improve airport operational performance  
- Provide actionable insights to airlines, airports, and aviation authorities  

This project aims to demonstrate advanced data analytics capability while delivering easy-to-understand, visually compelling results that show real-world aviation value.
