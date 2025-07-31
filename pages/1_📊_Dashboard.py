import streamlit as st
import pandas as pd
from utils import progreso_por_set

st.title("📊 Dashboard")
st.write("Progreso por set, filtros y exportación.")

@st.cache_data
def load_data():
    sets = pd.read_csv("data/sets.csv")
    inventory = pd.read_csv("data/inventory.csv")
    set_parts = pd.read_csv("data/set_parts.csv")
    return sets, inventory, set_parts

sets, inventory, set_parts = load_data()
df = progreso_por_set(sets, set_parts, inventory)

col1, col2, col3 = st.columns(3)
with col1:
    min_year, max_year = int(df["year"].min()), int(df["year"].max())
    year_range = st.slider("Año", min_year, max_year, (min_year, max_year))
with col2:
    min_prog, max_prog = float(df["progress"].min()), float(df["progress"].max())
    prog_range = st.slider("Progreso", 0.0, 1.0, (0.0, 1.0))
with col3:
    search = st.text_input("Buscar por nombre o set_num")

mask = (
    (df["year"].between(year_range[0], year_range[1])) &
    (df["progress"].between(prog_range[0], prog_range[1])) &
    (df["name"].str.contains(search, case=False, na=False) | df["set_num"].astype(str).str.contains(search))
)
filtered = df[mask].copy()

st.dataframe(filtered.sort_values(by=["progress","year"], ascending=[False, True]), use_container_width=True)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Descargar CSV filtrado", data=csv, file_name="dashboard_filtrado.csv", mime="text/csv")
