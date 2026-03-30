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
    peso = st.number_input("Peso (kg)", min_value=1.0, value=70.0)

    st.write("**Resumen**")
    st.write(f"Ayuno: {ayuno}")
    st.write(f"Alergia a contraste: {alergia}")
    st.write(f"Peso: {peso} kg")

elif seccion == "Topograma":
    st.header("Topograma")
    region = st.selectbox("Región", ["Cabeza", "Tórax", "Abdomen", "Pelvis"])
    proyeccion = st.selectbox("Proyección", ["AP", "Lateral"])

    st.write("**Selección actual**")
    st.write(f"Región: {region}")
    st.write(f"Proyección: {proyeccion}")

elif seccion == "Adquisición":
    st.header("Adquisición")
    kvp = st.selectbox("kVp", [80, 100, 120, 140])
    mas = st.number_input("mAs", min_value=1, value=100)
    pitch = st.number_input("Pitch", min_value=0.1, value=1.0, step=0.1)
    longitud = st.number_input("Longitud de barrido (cm)", min_value=1.0, value=30.0)

    st.write("**Parámetros seleccionados**")
    st.write(f"kVp: {kvp}")
    st.write(f"mAs: {mas}")
    st.write(f"Pitch: {pitch}")
    st.write(f"Longitud: {longitud} cm")

elif seccion == "Cálculos":
    st.header("Cálculos")
    ctdi_vol = st.number_input("CTDIvol (mGy)", min_value=0.0, value=10.0)
    longitud = st.number_input("Longitud de escaneo (cm)", min_value=0.0, value=30.0)

    dlp = ctdi_vol * longitud

    st.metric("DLP (mGy·cm)", f"{dlp:.2f}")
