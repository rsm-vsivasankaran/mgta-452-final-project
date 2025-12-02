# ✅ Aviation Analytics Project Checklist  
### *Global Turbulence Analytics + Airport Efficiency Index*

---

## 🧱 PHASE 1 – Problem & Project Setup
- [ ] Define clear scope for both modules  
- [ ] Write 1–2 paragraph descriptions for Turbulence Analytics  
- [ ] Write 1–2 paragraph descriptions for Airport Efficiency Index  
- [ ] Define out-of-scope items  
- [ ] Select technical stack (Python, libraries)  
- [ ] Create project folder structure  
- [ ] Initialize GitHub repo (optional but recommended)

---

## 🌍 PHASE 2 – Data Hunting & Collection
- [ ] Identify datasets for turbulence analytics  
- [ ] Identify datasets for weather/atmospheric data  
- [ ] Identify datasets for flight paths or flight-level info  
- [ ] Identify datasets for airport operational metrics  
- [ ] Download all datasets  
- [ ] Save into `data/raw/`  
- [ ] Document each dataset (source, columns, limitations)

---

## 🧹 PHASE 3 – Data Cleaning & Preparation
- [ ] Clean turbulence-related data  
- [ ] Clean weather data  
- [ ] Clean flight path or PIREP-style data  
- [ ] Clean airport delay/efficiency-related data  
- [ ] Convert all timestamps, locations, and units  
- [ ] Merge dataset(s) for turbulence analysis  
- [ ] Build dataset for AEI computation  
- [ ] Save processed files in `data/processed/`

---

## 🔍 PHASE 4 – Exploratory Data Analysis (EDA)
### Turbulence EDA
- [ ] Analyze distribution of turbulence levels  
- [ ] World map of turbulence events  
- [ ] Analyze turbulence vs altitude  
- [ ] Seasonal/temporal turbulence patterns  
- [ ] Correlation analysis with weather features  

### Airport Efficiency Index EDA
- [ ] Compute basic airport stats (delay, cancellations, traffic)  
- [ ] Airport delay world map  
- [ ] Time-series analysis  
- [ ] Correlation of airport metrics  
- [ ] Identify major patterns  

---

## 📏 PHASE 5 – Metric & Index Definition
### Turbulence Labeling
- [ ] Decide turbulence categories or score definition  
- [ ] Create final label column  

### Airport Efficiency Index (AEI)
- [ ] Select AEI components (KPIs)  
- [ ] Normalize metrics  
- [ ] Define AEI formula (weights or equal)  
- [ ] Compute AEI for each airport  
- [ ] Validate AEI with visual checks  

---

## 🧪 PHASE 6 – Feature Engineering
### Turbulence Model
- [ ] Select input features  
- [ ] Engineer weather and location-based features  
- [ ] Train-test split  

### AEI Model
- [ ] Select features for AEI prediction  
- [ ] Encode/scale as needed  
- [ ] Train-test split  

---

## 🤖 PHASE 7 – Modeling & Evaluation
### Turbulence Model
- [ ] Train baseline models  
- [ ] Evaluate using accuracy/F1/CM  
- [ ] Tune models  
- [ ] Feature importance  

### AEI Model
- [ ] Train baseline models  
- [ ] Evaluate regression or classification metrics  
- [ ] Tune models  
- [ ] Feature importance  

---

## 📊 PHASE 8 – Visualization & Story Design
### Turbulence Visuals
- [ ] Global turbulence heatmap  
- [ ] Altitude vs turbulence chart  
- [ ] Seasonal patterns  
- [ ] ML performance plots  

### AEI Visuals
- [ ] Global AEI airport map  
- [ ] Top/bottom airports  
- [ ] Radar chart per airport  
- [ ] Feature importance  

---

## 🧾 PHASE 9 – Documentation & Writing
- [ ] Write methodology for turbulence module  
- [ ] Write methodology for AEI module  
- [ ] Summaries of EDA findings  
- [ ] Model summary and results  
- [ ] Limitations & future work  
- [ ] Final insights  

---

## 🌐 PHASE 10 – Website Development
- [ ] Select framework (Streamlit/Dash/etc.)  
- [ ] Build Home Page  
- [ ] Build Turbulence Analytics Page  
- [ ] Build Turbulence ML Model Page  
- [ ] Build AEI Analytics Page  
- [ ] Build AEI Model Page  
- [ ] Build Conclusions Page  
- [ ] Integrate plots & interactivity  
- [ ] Final UI/UX polish  
- [ ] Local testing  

---

## 🎤 PHASE 11 – Presentation Prep
- [ ] Build slide deck  
- [ ] Add visuals & screenshots from website  
- [ ] Create project storyline  
- [ ] Rehearse demo flow  

---

# 🎉 DONE!