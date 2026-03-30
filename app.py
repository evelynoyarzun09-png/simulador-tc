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
    background-color: #505050;
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
    padding: 1.2rem 1.2rem 2rem 1.2rem;
    border-radius: 18px;
}

/* Botones */
div.stButton > button {
    background-color: #b8bec7 !important;
    color: #1f1f1f !important;
    border-radius: 12px !important;
    border: 1px solid #9ca3ad !important;
    font-weight: 600 !important;
    min-height: 46px !important;
}

/* Bloques */
.bloque-resumen {
    background-color: #616161;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    border: 1px solid #7a7a7a;
}
.bloque-seccion {
    background-color: #616161;
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

/* Edad más pequeña */
[data-testid="stMetricValue"] {
    font-size: 1.35rem !important;
}

/* SELECTBOX: caja cerrada */
div[data-baseweb="select"] > div {
    background-color: #b8bec7 !important;
    border-radius: 12px !important;
    color: #000000 !important;
}

/* TODO el texto dentro del select cerrado */
div[data-baseweb="select"] div,
div[data-baseweb="select"] span,
div[data-baseweb="select"] input,
div[data-baseweb="select"] svg {
    color: #000000 !important;
    fill: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    opacity: 1 !important;
}

/* Placeholder y valor seleccionado */
div[data-baseweb="select"] [data-testid="stMarkdownContainer"],
div[data-baseweb="select"] p {
    color: #000000 !important;
}

/* Menú desplegable abierto */
div[role="listbox"] {
    background-color: #c7ccd4 !important;
    color: #000000 !important;
    border: 1px solid #9ca3ad !important;
}

/* Opciones del desplegable */
div[role="option"] {
    background-color: #c7ccd4 !important;
    color: #000000 !important;
}

/* Todo lo que esté dentro de cada opción */
div[role="option"] *,
ul[role="listbox"] *,
li[role="option"] * {
    color: #000000 !important;
    fill: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    opacity: 1 !important;
}

/* Hover */
div[role="option"]:hover,
li[role="option"]:hover {
    background-color: #b2b8c1 !important;
    color: #000000 !important;
}

/* Inputs */
div[data-baseweb="input"] > div {
    background-color: #b8bec7 !important;
    color: #1f1f1f !important;
    border-radius: 12px !important;
}

/* Textarea */
div[data-baseweb="textarea"] > div {
    background-color: #b8bec7 !important;
    color: #1f1f1f !important;
    border-radius: 12px !important;
}

/* Texto dentro de inputs */
input, textarea {
    color: #1f1f1f !important;
    -webkit-text-fill-color: #1f1f1f !important;
}

/* Etiquetas */
label, .stMarkdown, p, span, div {
    color: white;
}

/* Caja info */
[data-testid="stInfo"] {
    background-color: #5a6478 !important;
    color: white !important;
}

/* Separación del botón volver */
.boton-volver {
    margin-top: 0.4rem;
    margin-bottom: 1rem;
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
if seccion
