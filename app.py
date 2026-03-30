import streamlit as st
from pathlib import Path
from datetime import date

st.set_page_config(page_title="Simulador TC", layout="wide")

# -------------------------
# RUTA DE IMÁGENES
# -------------------------
BASE_DIR = Path(__file__).parent
PORTADA_IMG = BASE_DIR / "tomografo_portada.png"

PACIENTE_IMG_PNG = BASE_DIR / "paciente.png"
PACIENTE_IMG_JPG = BASE_DIR / "paciente.jpg"

if PACIENTE_IMG_PNG.exists():
    PACIENTE_IMG = PACIENTE_IMG_PNG
elif PACIENTE_IMG_JPG.exists():
    PACIENTE_IMG = PACIENTE_IMG_JPG
else:
    PACIENTE_IMG = None

# -------------------------
# ESTADO INICIAL
# -------------------------
if "seccion" not in st.session_state:
    st.session_state.seccion = "Portada"

seccion = st.session_state.seccion

# -------------------------
# ESTILOS
# -------------------------
st.markdown("""
<style>
/* Fondo general */
.stApp {
    background-color: #4b4b4b;
}

/* Contenedor principal */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

/* Texto general */
html, body, [class*="css"] {
    color: white;
}

/* Botón inferior portada */
.boton-inferior-derecha {
    position: fixed;
    right: 2rem;
    bottom: 1.5rem;
    z-index: 999;
}

/* Portada */
.portada-titulo {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 700;
    color: #20cfcf;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;
}
.portada-subtitulo {
    text-align: center;
    color: white;
    font-size: 1.1rem;
    margin-bottom: 1rem;
}
.portada-fondo {
    background-color: black;
    padding: 1.2rem 1.2rem 5rem 1.2rem;
    border-radius: 18px;
}

/* Botones */
div.stButton > button {
    border-radius: 12px;
    font-weight: 600;
}

/* Bloques */
.bloque-resumen {
    background-color: #5a5a5a;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    border: 1px solid #7a7a7a;
}
.bloque-seccion {
    background-color: #5a5a5a;
    padding: 1rem 1rem 0.6rem 1rem;
    border-radius: 14px;
    border: 1px solid #7a7a7a;
    margin-bottom: 1rem;
}
.titulo-bloque {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
    color: white;
}

/* Reducir tamaño del valor de edad del metric */
[data-testid="stMetricValue"] {
    font-size: 1.5rem;
}

/* Etiquetas de formularios */
label, .stMarkdown, .stText, p, div {
    color: white;
}

/* Inputs y select */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background-color: #d9dde3;
    color: black;
}

/* Texto dentro de inputs */
input, textarea {
    color: black !important;
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
    st.markdown('<div class="portada-fondo">', unsafe_allow_html=True)
    st.markdown('<div class="portada-titulo">Tomografía Computada Aplicada</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="portada-subtitulo">Simulador interactivo para práctica de preparación, adquisición, reconstrucción y cálculos.</div>',
        unsafe_allow_html=True
    )

    if PORTADA_IMG.exists():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.image(str(PORTADA_IMG), use_container_width=True)
    else:
        st.warning("No se encontró la imagen de portada 'tomografo_portada.png'.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="boton-inferior-derecha">', unsafe_allow_html=True)
    if st.button("Ir a A Practicar"):
        ir_a_practicar()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# PANTALLA PRINCIPAL
# -------------------------
elif seccion == "A Practicar":
    st.title("Simulador de Tomografía Computada")
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
    col_btn1, col_btn2 = st.columns([1, 6])
    with col_btn1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

    st.header("Preparación de paciente")

    col
