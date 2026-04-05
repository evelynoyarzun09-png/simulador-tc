import streamlit as st
from pathlib import Path
from datetime import date
import hmac
import openpyxl
from PIL import Image, ImageDraw

st.set_page_config(page_title="Simulador TC", layout="wide")

# -------------------------
# RUTA DE IMÁGENES
# -------------------------
BASE_DIR = Path(__file__).parent
PORTADA_IMG = BASE_DIR / "tomografo_portada.png"
A_PRACTICAR_IMG = BASE_DIR / "a_practicar.png"
TOPOGRAMA_IMG = BASE_DIR / "topograma.png"

PACIENTE_IMG_PNG = BASE_DIR / "paciente.png"
PACIENTE_IMG_JPG = BASE_DIR / "paciente.jpg"

if PACIENTE_IMG_PNG.exists():
    PACIENTE_IMG = PACIENTE_IMG_PNG
elif PACIENTE_IMG_JPG.exists():
    PACIENTE_IMG = PACIENTE_IMG_JPG
else:
    PACIENTE_IMG = None

def mostrar_imagen_actualizada(ruta, **kwargs):
    if ruta is None:
        return
    ruta = Path(ruta)
    if ruta.exists():
        st.image(ruta.read_bytes(), **kwargs)

# -------------------------
# ESTADO INICIAL
