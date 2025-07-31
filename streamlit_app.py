import streamlit as st
import pandas as pd
from utils import progreso_por_set

st.set_page_config(page_title="LEGO Organizer", layout="wide")

@st.cache_data
def load_data():
    sets = pd.read_csv("data/sets.csv")
    inventory = pd.read_csv("data/inventory.csv")
    set_parts = pd.read_csv("data/set_parts.csv")
    return sets, inventory, set_parts

sets, inventory, set_parts = load_data()

st.title("LEGO Organizer 🧱")
st.write("Resumen general de tus sets y progreso de piezas.")

df = progreso_por_set(sets, set_parts, inventory)
st.dataframe(
    df[["set_num","name","year","required","have","missing","progress"]]
    .sort_values(by=["progress","year"], ascending=[False, True]),
    use_container_width=True
)

st.info("Usa el menú lateral para navegar entre páginas: Dashboard, Sets, Inventario y Piezas faltantes.")
