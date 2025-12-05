
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import classification_report, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

MODELS_DIR = Path("aviation-analytics/models")
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def train_turbulence_model(df):
    """
    Trains a Random Forest classifier to predict turbulence intensity.
    """
    print("Training Turbulence Model...")
    
    # Features: Altitude, Latitude, Longitude, Month, Hour
    # Target: turbulence_intensity
    
    # Feature Engineering
    df['month'] = df['timestamp'].dt.month
    df['hour'] = df['timestamp'].dt.hour
    
    features = ['altitude', 'latitude', 'longitude', 'month', 'hour']
    target = 'turbulence_intensity'
    
    X = df[features]
    y = df[target].astype(str)
    
    # Encode Target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Train
    # Using smaller n_estimators for speed in this demo, can increase later
    clf = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    print("Turbulence Model Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    # Save
    joblib.dump(clf, MODELS_DIR / "turbulence_model.pkl")
    joblib.dump(le, MODELS_DIR / "turbulence_le.pkl")
    print(f"Saved turbulence model to {MODELS_DIR}")
    
    return clf

def train_aei_model(df):
    """
    Trains a Gradient Boosting Regressor to predict Airport Efficiency (Avg Delay).
    """
    print("Training AEI Model...")
    
    # Features: Month, Total Flights, Cancellation Rate (Lagged? No, just concurrent for now or purely based on time/volume)
    # Let's try to predict avg_dep_delay based on volume and month
    
    features = ['total_flights', 'cancellation_rate'] 
    # Note: cancellation_rate is highly correlated but might be unknown ahead of time. 
    # For prediction, maybe we only use 'month' and 'total_flights' (projected).
    # Let's keep it simple.
    
    target = 'avg_dep_delay'
    
    # Ensure no NaNs
    df = df.dropna(subset=features + [target])
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    reg = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
    reg.fit(X_train, y_train)
    
    y_pred = reg.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"AEI Model MSE: {mse:.2f}, R2: {r2:.2f}")
    
    joblib.dump(reg, MODELS_DIR / "aei_model.pkl")
    print(f"Saved AEI model to {MODELS_DIR}")
    
    return reg
