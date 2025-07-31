import streamlit as st
import pandas as pd
from utils import calcular_faltantes

st.title("🔎 Piezas faltantes")
st.write("Selecciona un set para ver qué piezas te faltan y en qué cantidad.")

@st.cache_data
def load_data():
    sets = pd.read_csv("data/sets.csv")
    inventory = pd.read_csv("data/inventory.csv")
    set_parts = pd.read_csv("data/set_parts.csv")
    return sets, inventory, set_parts

sets, inventory, set_parts = load_data()

set_options = sets.set_index("set_num")["name"].to_dict()
selected = st.selectbox("Elige un set", options=list(set_options.keys()), format_func=lambda k: f"{k} — {set_options[k]}")

parts_sel = set_parts[set_parts["set_num"] == selected].copy()
falt = calcular_faltantes(inventory, parts_sel)
falt_only = falt[falt["qty_missing"] > 0].copy()

st.subheader("Resumen")
total_req = int(parts_sel["qty_required"].sum())
total_missing = int(falt_only["qty_missing"].sum())
st.write(f"Total requeridas: **{total_req}** • Faltantes: **{total_missing}**")

st.dataframe(
    falt_only[["part_num","color_id","qty_required","qty_have","qty_missing"]].sort_values("qty_missing", ascending=False),
    use_container_width=True
)

csv = falt_only.to_csv(index=False).encode("utf-8")
st.download_button("Descargar faltantes (CSV)", data=csv, file_name=f"faltantes_{selected}.csv", mime="text/csv")
