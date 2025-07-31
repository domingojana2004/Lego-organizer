import streamlit as st
import pandas as pd
from utils import ensure_dtypes

st.title("📦 Inventario")
st.write("Edita tu inventario de piezas.")

@st.cache_data
def load_inventory():
    return pd.read_csv("data/inventory.csv")

def save_inventory(df):
    df = ensure_dtypes(df, int_cols=["qty_have"])
    df.to_csv("data/inventory.csv", index=False)

inv = load_inventory()
edited = st.data_editor(inv, use_container_width=True, num_rows="dynamic")
col1, col2 = st.columns(2)
with col1:
    if st.button("Guardar cambios"):
        save_inventory(edited)
        st.success("Inventario guardado.")
with col2:
    st.download_button("Descargar inventory.csv", data=edited.to_csv(index=False).encode("utf-8"), file_name="inventory.csv", mime="text/csv")

st.divider()
uploaded = st.file_uploader("Subir nuevo inventory.csv", type=["csv"])
if uploaded is not None:
    new_df = pd.read_csv(uploaded)
    st.write("Vista previa:", new_df.head())
    if st.button("Reemplazar inventory.csv con el archivo subido"):
        save_inventory(new_df)
        st.success("Archivo reemplazado. Recarga la página.")
