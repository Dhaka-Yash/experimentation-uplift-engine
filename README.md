# Experiment Uplifting Engine

A practical experimentation and uplift-modeling project for analyzing treatment impact on conversion outcomes.

## What This Project Includes

- A full notebook workflow from data preparation to decisioning.
- A Streamlit dashboard for A/B test metrics and segment-level performance.
- Simulated experiment data with treatment, conversion, and uplift fields.

## Project Structure

```text
experiment-uplifting engine/
|-- app/
|   `-- streamlit_app.py
|-- data/
|   |-- ecommerce_product_dataset.csv
|   `-- experiment_simulated.csv
|-- notebooks/
|   |-- 01_data_preparation.ipynb
|   |-- 02_power_analysis.ipynb
|   |-- 03_ab_test_analysis.ipynb
|   |-- 04_uplift_modeling.ipynb
|   `-- 05_segmentation_and_decision.ipynb
|-- requirements.txt
`-- README.md
```

## Setup

### 1) Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Streamlit Dashboard

From the project root:

```bash
streamlit run app/streamlit_app.py
```

The dashboard shows:

- Control vs Treatment conversion rate
- Absolute lift
- Two-proportion z-test significance
- Uplift (or conversion fallback) distribution
- Segment performance by `new_user` or `high_value_user`

## Notebook Workflow

Run notebooks in order:

1. `notebooks/01_data_preparation.ipynb`  
   Prepares/simulates experiment features and writes `data/experiment_simulated.csv`.
2. `notebooks/02_power_analysis.ipynb`  
   Checks experimental design and sample/power assumptions.
3. `notebooks/03_ab_test_analysis.ipynb`  
   Calculates control/treatment CR, lift, and significance.
4. `notebooks/04_uplift_modeling.ipynb`  
   Trains treatment/control models and computes individual-level uplift.
5. `notebooks/05_segmentation_and_decision.ipynb`  
   Compares uplift by segments and supports go/no-go decisions.

## Data Notes

Main experiment dataset: `data/experiment_simulated.csv`

Important columns used in analysis/app:

- `treatment` (0 = control, 1 = treatment)
- `converted` (0/1 outcome)
- `uplift` (predicted individual uplift; optional for dashboard)
- `new_user`, `high_value_user` (segmentation fields)
- `prior_purchases` (uplift modeling feature)

## Requirements

Python packages are listed in `requirements.txt`.

## License

No license file is currently included in this repository.
