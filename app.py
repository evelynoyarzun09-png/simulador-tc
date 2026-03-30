import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador TC", layout="wide")

st.title("Simulador de Tomografía Computada")

seccion = st.sidebar.selectbox(
    "Selecciona etapa",
    [
        "A Practicar",
        "Preparación de paciente",
        "Jeringa inyectora",
        "Topograma",
        "Adquisición",
        "Reconstrucción",
        "Reformación",
        "Medida paciente",
        "Cálculos"
    ]
)

if seccion == "A Practicar":
    st.header("A Practicar")
    st.write("Bienvenida al simulador de Tomografía Computada.")
    st.info("Selecciona una etapa desde el menú lateral para comenzar.")

elif seccion == "Preparación de paciente":
    st.header("Preparación de paciente")

    col1, col2 = st.columns(2)

    with col1:
        ayuno = st.selectbox("Ayuno", ["Sí", "No"])
        alergia = st.selectbox("Alergia a contraste", ["Sí", "No"])
        creatinina = st.selectbox("Creatinina evaluada", ["Sí", "No"])

    with col2:
        peso = st.number_input("Peso (kg)", min_value=1.0, value=70.0)
        talla = st.number_input("Talla (cm)", min_value=30.0, value=165.0)
        via_venosa = st.selectbox("Vía venosa permeable", ["Sí", "No"])

    st.subheader("Resumen")
    st.write(f"Ayuno: {ayuno}")
    st.write(f"Alergia a contraste: {alergia}")
    st.write(f"Creatinina evaluada: {creatinina}")
    st.write(f"Peso: {peso} kg")
    st.write(f"Talla: {talla} cm")
    st.write(f"Vía venosa permeable: {via_venosa}")

elif seccion == "Jeringa inyectora":
    st.header("Jeringa inyectora")

    col1, col2 = st.columns(2)

    with col1:
        tipo_contraste = st.text_input("Tipo de contraste", value="Yodado")
        volumen_contraste = st.number_input("Volumen de contraste (mL)", min_value=0.0, value=80.0)
        flujo = st.number_input("Flujo (mL/s)", min_value=0.1, value=3.5, step=0.1)

    with col2:
        flush = st.number_input("Volumen de flush / suero (mL)", min_value=0.0, value=30.0)
        tiempo_delay = st.number_input("Delay / retardo (s)", min_value=0.0, value=25.0)
        sitio_puncion = st.selectbox("Sitio de punción", ["Brazo derecho", "Brazo izquierdo", "Otro"])

    st.subheader("Resumen")
    st.write(f"Tipo de contraste: {tipo_contraste}")
    st.write(f"Volumen de contraste: {volumen_contraste} mL")
    st.write(f"Flujo: {flujo} mL/s")
    st.write(f"Flush: {flush} mL")
    st.write(f"Delay: {tiempo_delay} s")
    st.write(f"Sitio de punción: {sitio_puncion}")

elif seccion == "Topograma":
    st.header("Topograma")

    col1, col2 = st.columns(2)

    with col1:
        region = st.selectbox(
            "Región anatómica",
            ["Cabeza", "Cuello", "Tórax", "Abdomen", "Pelvis", "Cuerpo completo"]
        )
        proyeccion = st.selectbox("Proyección", ["AP", "Lateral", "AP y lateral"])

    with col2:
        inicio = st.text_input("Inicio topograma", value="Desde")
        termino = st.text_input("Término topograma", value="Hasta")
        observaciones_topo = st.text_area("Observaciones")

    st.subheader("Resumen")
    st.write(f"Región: {region}")
    st.write(f"Proyección: {proyeccion}")
    st.write(f"Inicio: {inicio}")
    st.write(f"Término: {termino}")
    st.write(f"Observaciones: {observaciones_topo}")

elif seccion == "Adquisición":
    st.header("Adquisición")

    col1, col2 = st.columns(2)

    with col1:
        kvp = st.selectbox("kVp", [80, 100, 120, 140])
        mas = st.number_input("mAs", min_value=1, value=100)
        pitch = st.number_input("Pitch", min_value=0.1, value=1.0, step=0.1)
        rotacion = st.number_input("Tiempo de rotación (s)", min_value=0.1, value=0.5, step=0.1)

    with col2:
        colimacion = st.text_input("Colimación", value="64 x 0.625 mm")
        espesor_corte = st.number_input("Espesor de corte (mm)", min_value=0.1, value=1.0, step=0.1)
        longitud = st.number_input("Longitud de barrido (cm)", min_value=1.0, value=30.0)
        modo = st.selectbox("Modo de adquisición", ["Helicoidal", "Secuencial"])

    st.subheader("Resumen")
    st.write(f"kVp: {kvp}")
    st.write(f"mAs: {mas}")
    st.write(f"Pitch: {pitch}")
    st.write(f"Tiempo de rotación: {rotacion} s")
    st.write(f"Colimación: {colimacion}")
    st.write(f"Espesor de corte: {espesor_corte} mm")
    st.write(f"Longitud: {longitud} cm")
    st.write(f"Modo: {modo}")

elif seccion == "Reconstrucción":
    st.header("Reconstrucción")

    col1, col2 = st.columns(2)

    with col1:
        kernel = st.selectbox(
            "Kernel / filtro",
            ["Blando", "Estándar", "Óseo", "Pulmonar", "Otro"]
        )
        grosor_recon = st.number_input("Grosor de reconstrucción (mm)", min_value=0.1, value=1.0, step=0.1)
        intervalo_recon = st.number_input("Intervalo de reconstrucción (mm)", min_value=0.1, value=0.5, step=0.1)

    with col2:
        plano_recon = st.multiselect(
            "Planos reconstruidos",
            ["Axial", "Coronal", "Sagital", "Oblicuo"],
            default=["Axial"]
        )
        algoritmo = st.selectbox("Algoritmo", ["FBP", "Iterativa", "Otro"])
        ventana = st.selectbox("Ventana principal", ["Partes blandas", "Pulmón", "Ósea", "Otra"])

    st.subheader("Resumen")
    st.write(f"Kernel: {kernel}")
    st.write(f"Grosor: {grosor_recon} mm")
    st.write(f"Intervalo: {intervalo_recon} mm")
    st.write(f"Planos: {', '.join(plano_recon) if plano_recon else 'Ninguno'}")
    st.write(f"Algoritmo: {algoritmo}")
    st.write(f"Ventana: {ventana}")

elif seccion == "Reformación":
    st.header("Reformación")

    col1, col2 = st.columns(2)

    with col1:
        tipo_reformacion = st.multiselect(
            "Tipo de reformación",
            ["MPR coronal", "MPR sagital", "MIP", "MinIP", "VR", "Curva"],
            default=["MPR coronal", "MPR sagital"]
        )
        grosor_mip = st.number_input("Grosor MIP / slab (mm)", min_value=0.1, value=10.0, step=0.1)

    with col2:
        orientacion = st.selectbox("Orientación principal", ["Coronal", "Sagital", "Oblicua"])
        observaciones_reform = st.text_area("Observaciones de reformación")

    st.subheader("Resumen")
    st.write(f"Tipo: {', '.join(tipo_reformacion) if tipo_reformacion else 'Ninguno'}")
    st.write(f"Grosor slab: {grosor_mip} mm")
    st.write(f"Orientación: {orientacion}")
    st.write(f"Observaciones: {observaciones_reform}")

elif seccion == "Medida paciente":
    st.header("Medida paciente")

    col1, col2 = st.columns(2)

    with col1:
        diametro_ap = st.number_input("Diámetro AP (cm)", min_value=0.0, value=25.0)
        diametro_lat = st.number_input("Diámetro lateral (cm)", min_value=0.0, value=35.0)

    with col2:
        edad = st.number_input("Edad", min_value=0, value=30)
        sexo = st.selectbox("Sexo", ["Femenino", "Masculino", "Otro"])

    if diametro_ap > 0 and diametro_lat > 0:
        diametro_efectivo = (diametro_ap * diametro_lat) ** 0.5
    else:
        diametro_efectivo = 0.0

    st.metric("Diámetro efectivo (cm)", f"{diametro_efectivo:.2f}")

    st.subheader("Resumen")
    st.write(f"Edad: {edad}")
    st.write(f"Sexo: {sexo}")

elif seccion == "Cálculos":
    st.header("Cálculos")

    col1, col2 = st.columns(2)

    with col1:
        ctdi_vol = st.number_input("CTDIvol (mGy)", min_value=0.0, value=10.0)
        longitud_scan = st.number_input("Longitud de escaneo (cm)", min_value=0.0, value=30.0)

    with col2:
        factor_ssde = st.number_input("Factor SSDE", min_value=0.1, value=1.0, step=0.1)
        usar_ssde = st.selectbox("¿Calcular SSDE?", ["Sí", "No"])

    dlp = ctdi_vol * longitud_scan
    st.metric("DLP (mGy·cm)", f"{dlp:.2f}")

    if usar_ssde == "Sí":
        ssde = ctdi_vol * factor_ssde
        st.metric("SSDE (mGy)", f"{ssde:.2f}")
