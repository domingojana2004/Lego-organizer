import streamlit as st
import pandas as pd

st.title("🧱 Sets")
st.write("Gestiona tu lista de sets. Puedes editar la tabla y subir/descargar CSV.")

@st.cache_data
def load_sets():
    return pd.read_csv("data/sets.csv")

def save_sets(df):
    df.to_csv("data/sets.csv", index=False)

sets = load_sets()
edited = st.data_editor(sets, use_container_width=True, num_rows="dynamic")
col1, col2 = st.columns(2)
with col1:
    if st.button("Guardar cambios"):
        save_sets(edited)
        st.success("Sets guardados.")
with col2:
    st.download_button("Descargar sets.csv", data=edited.to_csv(index=False).encode("utf-8"), file_name="sets.csv", mime="text/csv")

st.divider()
uploaded = st.file_uploader("Subir nuevo sets.csv", type=["csv"])
if uploaded is not None:
    new_df = pd.read_csv(uploaded)
    st.write("Vista previa:", new_df.head())
    if st.button("Reemplazar sets.csv con el archivo subido"):
        new_df.to_csv("data/sets.csv", index=False)
        st.success("Archivo reemplazado. Recarga la página.")
