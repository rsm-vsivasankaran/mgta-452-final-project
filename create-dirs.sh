# Create root folder
mkdir -p aviation-analytics
cd aviation-analytics

# Data folders
mkdir -p data/raw
mkdir -p data/processed

# Notebooks
mkdir -p notebooks

# Source code folder
mkdir -p src

# Reports & figures
mkdir -p reports/figures

# Docs folder
mkdir -p docs

# Website folder (empty for now)
mkdir -p website

# Notebooks templates
touch notebooks/01_turbulence_eda.ipynb
touch notebooks/02_turbulence_model.ipynb
touch notebooks/03_aei_eda.ipynb
touch notebooks/04_aei_model.ipynb
touch notebooks/05_visualizations.ipynb

# Source code templates
touch src/data_preprocessing.py
touch src/turbulence_utils.py
touch src/aei_utils.py
touch src/modeling.py
touch src/visualization.py

# Documentation templates
touch docs/methodology.md
touch docs/data_sources.md
touch docs/turbulence_analysis_summary.md
touch docs/aei_analysis_summary.md