import streamlit as st
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Experimentation Engine", layout="wide")

st.title("🚀 Experimentation & Uplift Modeling Dashboard")

script_dir = Path(__file__).resolve().parent
data_candidates = [
    script_dir / "data" / "experiment_simulated.csv",
    script_dir.parent / "data" / "experiment_simulated.csv",
]
data_path = next((p for p in data_candidates if p.exists()), None)
if data_path is None:
    expected_paths = ", ".join(str(p) for p in data_candidates)
    st.error(f"Data file not found. Checked: {expected_paths}")
    st.stop()

df = pd.read_csv(data_path)

required_cols = {"treatment", "converted"}
missing_cols = required_cols - set(df.columns)
if missing_cols:
    st.error(f"Missing required columns: {sorted(missing_cols)}")
    st.stop()

# Normalize common string encodings to numeric labels expected by this dashboard.
df["treatment"] = (
    df["treatment"]
    .replace({"control": 0, "treatment": 1, "Control": 0, "Treatment": 1})
)
df["treatment"] = pd.to_numeric(df["treatment"], errors="coerce")
df["converted"] = pd.to_numeric(df["converted"], errors="coerce")

if df[["treatment", "converted"]].isna().any().any():
    st.error("Columns 'treatment' and 'converted' must be numeric (or coercible to numeric).")
    st.stop()

# Conversion Summary
summary = df.groupby("treatment")["converted"].mean().reindex([0, 1])
if summary.isna().any():
    st.error("Data must include both treatment groups: 0 (control) and 1 (treatment).")
    st.stop()

control = summary.loc[0]
treatment = summary.loc[1]
lift = treatment - control

col1, col2, col3 = st.columns(3)

col1.metric("Control CR", f"{control:.2%}")
col2.metric("Treatment CR", f"{treatment:.2%}")
col3.metric("Absolute Lift", f"{lift:.2%}")

# Statistical Test
counts = df.groupby("treatment")["converted"].sum().reindex([0, 1])
nobs = df.groupby("treatment")["converted"].count().reindex([0, 1])

z_stat, p_value = proportions_ztest(counts, nobs)

st.subheader("Statistical Significance")

if p_value < 0.05:
    st.success(f"Significant (p = {p_value:.4f})")
else:
    st.error(f"Not Significant (p = {p_value:.4f})")

# Uplift Distribution
st.subheader("Uplift Distribution")

fig, ax = plt.subplots()
if "uplift" not in df.columns:
    st.warning("Column 'uplift' not found. Showing conversion distribution instead.")
    ax.hist(df["converted"], bins=2)
else:
    ax.hist(df["uplift"], bins=30)
st.pyplot(fig)

# Segmentation
st.subheader("Segment Performance")

segment = st.selectbox("Choose Segment", ["new_user", "high_value_user"])

segment_data = df.groupby([segment, 'treatment'])['converted'].mean().unstack()

st.dataframe(segment_data)
