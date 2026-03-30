import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador TC", layout="wide")

st.title("Simulador de Tomografía Computada")

seccion = st.sidebar.selectbox(
    "Selecciona etapa",
    [
        "Preparación de paciente",
        "Topograma",
        "Adquisición",
        "Cálculos"
    ]
)

if seccion == "Preparación de paciente":
    st.header("Preparación de paciente")
    ayuno = st.selectbox("Ayuno", ["Sí", "No"])
    alergia = st.selectbox("Alergia a contraste", ["Sí", "No"])
    peso = st.number_input("Peso (kg)", min_value=1.0)

elif seccion == "Topograma":
    st.header("Topograma")
    region = st.selectbox("Región", ["Cabeza", "Tórax", "Ab
