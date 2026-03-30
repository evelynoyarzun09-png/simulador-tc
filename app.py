import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tomografía Computada Aplicada", layout="wide")

# -------------------------
# ESTADO INICIAL
# -------------------------
if "seccion" not in st.session_state:
    st.session_state.seccion = "Portada"

seccion = st.session_state.seccion

# -------------------------
# ESTILOS GENERALES
# -------------------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: black;
    color: #40E0D0;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

[data-testid="stToolbar"] {
    right: 1rem;
}

h1, h2, h3, h4, h5, h6, p, label, div, span {
    color: #40E0D0 !important;
}

.stButton > button {
    background-color: #40E0D0;
    color: black;
    border: none;
    border-radius: 10px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #2ec4b6;
    color: black;
}

.portada-container {
    height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
}

.portada-titulo {
    font-size: 4rem;
    font-weight: 800;
    color: #40E0D0;
    margin-bottom: 1rem;
}

.portada-subtitulo {
    font-size: 1.3rem;
    color: #40E0D0;
    opacity: 0.9;
}

.boton-esquina {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 9999;
}
</style>
""", unsafe_allow_html=True)


# -------------------------
# FUNCIONES
# -------------------------
def ir_a_practicar():
    st.session_state.seccion = "A Practicar"

def volver_menu():
    st.session_state.seccion = "A Practicar"


# -------------------------
# PORTADA
# -------------------------
if seccion == "Portada":
    st.markdown("""
    <div class="portada-container">
        <div class="portada-titulo">Tomografía Computada Aplicada</div>
        <div class="portada-subtitulo">
            Simulador interactivo para práctica de adquisición, reconstrucción,
            reformación y cálculos en tomografía computada
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="boton-esquina">', unsafe_allow_html=True)
    if st.button("Ir a practicar", use_container_width=False):
        ir_a_practicar()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# -------------------------
# PANTALLA PRINCIPAL
# -------------------------
elif seccion == "A Practicar":
    st.title("Tomografía Computada Aplicada")
    st.header("A Practicar")
    st.write("Selecciona una etapa del simulador:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Preparación de paciente", use_container_width=True):
            st.session_state.seccion = "Preparación de paciente"
            st.rerun()

        if st.button("Jeringa inyectora", use_container_width=True):
            st.session_state.seccion = "Jeringa inyectora"
            st.rerun()

        if st.button("Topograma", use_container_width=True):
            st.session_state.seccion = "Topograma"
            st.rerun()

    with col2:
        if st.button("Adquisición", use_container_width=True):
            st.session_state.seccion = "Adquisición"
            st.rerun()

        if st.button("Reconstrucción", use_container_width=True):
            st.session_state.seccion = "Reconstrucción"
            st.rerun()

        if st.button("Reformación", use_container_width=True):
            st.session_state.seccion = "Reformación"
            st.rerun()

    with col3:
        if st.button("Medida paciente", use_container_width=True):
            st.session_state.seccion = "Medida paciente"
            st.rerun()

        if st.button("Cálculos", use_container_width=True):
            st.session_state.seccion = "Cálculos"
            st.rerun()

    st.divider()
    st.info("Haz clic en una etapa para continuar.")


# -------------------------
# PREPARACIÓN DE PACIENTE
# -------------------------
elif seccion == "Preparación de paciente":
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

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


# -------------------------
# JERINGA INYECTORA
# -------------------------
elif seccion == "Jeringa inyectora":
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

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


# -------------------------
# TOPOGRAMA
# -------------------------
elif seccion == "Topograma":
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

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


# -------------------------
# ADQUISICIÓN
# -------------------------
elif seccion == "Adquisición":
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

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


# -------------------------
# RECONSTRUCCIÓN
# -------------------------
elif seccion == "Reconstrucción":
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

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


# -------------------------
# REFORMACIÓN
# -------------------------
elif seccion == "Reformación":
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

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


# -------------------------
# MEDIDA PACIENTE
# -------------------------
elif seccion == "Medida paciente":
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

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


# -------------------------
# CÁLCULOS
# -------------------------
elif seccion == "Cálculos":
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

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
