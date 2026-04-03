import streamlit as st
from pathlib import Path
from datetime import date
import hmac
import openpyxl

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

# -------------------------
# ESTADO INICIAL
# -------------------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "seccion" not in st.session_state:
    st.session_state.seccion = "Portada"

DEFAULTS = {
    # Preparación
    "prep_nombres": "",
    "prep_apellidos": "",
    "prep_fecha_nac": date(2000, 1, 1),
    "prep_examen": "",
    "prep_peso": 70,
    "prep_embarazo": "Seleccionar",
    "prep_creatinina": "Seleccionar",
    "prep_medio_contraste_ev": "Seleccionar",
    "prep_via_venosa": "Seleccionar",
    "prep_cantidad_contraste": "Seleccionar",
    "prep_metodo_inyeccion": "Seleccionar",
    "prep_medio_contraste_oral": "Seleccionar",

    # Topograma
    "topo_entrada_paciente": "Seleccionar",
    "topo_posicionamiento": "Seleccionar",
    "topo_posicion_tubo": "Seleccionar",
    "topo_posicion_brazos": "Seleccionar",
    "topo_region": "Seleccionar",
    "topo_inicio": "", 
    "topo_termino": "",
    "topo_rx_iniciado": False,

    # Adquisición
    "adq_kvp": "Seleccionar",
    "adq_mas": 100,
    "adq_pitch": 1.0,
    "adq_rotacion": 0.5,
    "adq_colimacion": "",
    "adq_espesor_corte": 1.0,
    "adq_longitud": 30.0,
    "adq_modo": "Seleccionar",

    # Reconstrucción
    "recon_kernel": "Seleccionar",
    "recon_grosor": 1.0,
    "recon_intervalo": 0.5,
    "recon_planos": [],
    "recon_algoritmo": "Seleccionar",
    "recon_ventana": "Seleccionar",

    # Reformación
    "reform_tipo": [],
    "reform_grosor": 10.0,
    "reform_orientacion": "Seleccionar",
    "reform_observaciones": "",

    # Jeringa
    "jer_tipo_contraste": "Yodado",
    "jer_volumen_contraste": 80.0,
    "jer_flujo": 3.5,
    "jer_flush": 30.0,
    "jer_tiempo_delay": 25.0,
    "jer_sitio_puncion": "Seleccionar",
}

for clave, valor in DEFAULTS.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor

# -------------------------
# FUNCIONES PERSISTENCIA
# -------------------------
def load_widget(key):
    st.session_state[f"_{key}"] = st.session_state[key]

def store_widget(key):
    st.session_state[key] = st.session_state[f"_{key}"]

    if key.startswith("topo_"):
        st.session_state["topo_rx_iniciado"] = False


def persistent_text_input(label, key):
    load_widget(key)
    st.text_input(label, key=f"_{key}", on_change=store_widget, args=(key,))

def persistent_text_area(label, key):
    load_widget(key)
    st.text_area(label, key=f"_{key}", on_change=store_widget, args=(key,))

def persistent_date_input(label, key, min_value=None, max_value=None):
    load_widget(key)
    st.date_input(
        label,
        key=f"_{key}",
        min_value=min_value,
        max_value=max_value,
        on_change=store_widget,
        args=(key,)
    )

def mostrar_opcion_minuscula(opcion):
    if isinstance(opcion, str):
        return opcion.lower()
    return str(opcion)

def persistent_selectbox(label, options, key):
    load_widget(key)
    st.selectbox(
        label,
        options,
        key=f"_{key}",
        format_func=mostrar_opcion_minuscula,
        on_change=store_widget,
        args=(key,)
    )

def persistent_multiselect(label, options, key):
    load_widget(key)
    st.multiselect(
        label,
        options,
        key=f"_{key}",
        format_func=mostrar_opcion_minuscula,
        on_change=store_widget,
        args=(key,)
    )

def persistent_number_input(label, key, **kwargs):
    load_widget(key)
    st.number_input(label, key=f"_{key}", on_change=store_widget, args=(key,), **kwargs)

# -------------------------
# CONTROL DE ACCESO
# -------------------------
def verificar_clave():
    clave_ingresada = st.session_state.get("clave_ingresada", "")
    clave_correcta = st.secrets.get("app_password", "")

    if hmac.compare_digest(clave_ingresada, clave_correcta):
        st.session_state.autenticado = True
        st.session_state.error_clave = False
    else:
        st.session_state.autenticado = False
        st.session_state.error_clave = True


if not st.session_state.autenticado:
    st.markdown("""
    <style>
    .stApp { background-color: #111111; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 820px; }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText { color: white !important; text-transform: uppercase !important; }
    .login-box {
        background-color: #000000;
        padding: 2rem;
        border-radius: 18px;
        border: 1px solid #2d2d2d;
    }
    .login-titulo {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #20cfcf;
        margin-bottom: 0.35rem;
    }
    .login-subtitulo {
        text-align: center;
        color: white;
        font-size: 0.62rem;
        margin-bottom: 1.2rem;
    }
    div[data-baseweb="input"] > div {
        background-color: #d0d5dd !important;
        color: #111111 !important;
        border-radius: 8px !important;
    }
    input {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }
    div.stButton > button {
        background-color: #b8bec7 !important;
        color: #1f1f1f !important;
        border-radius: 8px !important;
        border: 1px solid #9ca3ad !important;
        font-weight: 600 !important;
    font-size: 0.7rem !important;
        min-height: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-titulo">Tomografía Computada Aplicada</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitulo">Ingrese la clave para acceder al simulador.</div>', unsafe_allow_html=True)

    if PORTADA_IMG.exists():
        st.image(str(PORTADA_IMG), use_container_width=True)

    st.text_input("Clave de acceso", type="password", key="clave_ingresada", on_change=verificar_clave)

    if st.session_state.get("error_clave", False):
        st.error("Clave incorrecta. Inténtalo nuevamente.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# -------------------------
# ESTILOS
# -------------------------
st.markdown("""
<style>
.stApp { background-color: #505050; }
.block-container { padding-top: 0.5rem; padding-bottom: 0.8rem; max-width: 1100px; }

/* Escala general más compacta */
html, body, [class*="css"]  {
    font-size: 10px !important;
}
h1 { font-size: 1.8rem !important; }
h2 { font-size: 1.45rem !important; }
h3 { font-size: 1.2rem !important; }
p, label, .stMarkdown, .stText, div, span {
    line-height: 1.15 !important;
}
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText { color: white !important; text-transform: uppercase !important; }

.portada-titulo {
    text-align: center;
    font-size: 1.45rem;
    font-weight: 700;
    color: #20cfcf;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;
}
.portada-subtitulo {
    text-align: center;
    color: white;
    font-size: 0.62rem;
    margin-bottom: 0.4rem;
}
.portada-fondo {
    background-color: black;
    padding: 1.2rem 1.2rem 2rem 1.2rem;
    border-radius: 18px;
}
div.stButton > button {
    background-color: #b8bec7 !important;
    color: #1f1f1f !important;
    border-radius: 8px !important;
    border: 1px solid #9ca3ad !important;
    font-weight: 600 !important;
    font-size: 0.7rem !important;
    min-height: 30px !important;
}
div.stButton > button:disabled {
    background-color: #8a8f97 !important;
    color: #e6e6e6 !important;
    border: 1px solid #7a7a7a !important;
    opacity: 0.75 !important;
}
.bloque-resumen {
    background-color: #616161;
    padding: 0.45rem 0.6rem;
    border-radius: 8px;
    border: 1px solid #7a7a7a;
}
.bloque-seccion {
    background-color: #616161;
    padding: 0.45rem 0.5rem 0.35rem 0.5rem;
    border-radius: 9px;
    border: 1px solid #7a7a7a;
    margin-bottom: 0.4rem;
}
.bloque-a-practicar {
    background-color: #616161;
    padding: 0.55rem;
    border-radius: 10px;
    border: 1px solid #7a7a7a;
    margin-bottom: 0.4rem;
}
.titulo-bloque {
    font-size: 0.62rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
    color: white;
}
.bloque-a-practicar img,
.bloque-seccion img { border-radius: 9px; }

[data-testid="stMetricValue"] { font-size: 0.8rem !important; }
[data-testid="stMetricLabel"] { color: white !important; }

div[data-baseweb="select"] > div {
    background-color: #b8bec7 !important;
    border-radius: 8px !important;
    color: #000000 !important;
}
div[data-baseweb="select"] div,
div[data-baseweb="select"] span,
div[data-baseweb="select"] input,
div[data-baseweb="select"] svg {
    color: #000000 !important;
    fill: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
div[data-baseweb="select"] > div,
div[data-baseweb="select"] div,
div[data-baseweb="select"] span,
div[data-baseweb="select"] input,
div[role="listbox"],
div[role="option"],
div[role="option"] * {
    text-transform: lowercase !important;
}
div[role="listbox"] {
    background-color: #c7ccd4 !important;
    border: 1px solid #9ca3ad !important;
}
div[role="option"] {
    background-color: #c7ccd4 !important;
    color: #000000 !important;
}
div[role="option"] * {
    color: #000000 !important;
    fill: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
div[role="option"]:hover {
    background-color: #b2b8c1 !important;
    color: #000000 !important;
}
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background-color: #b8bec7 !important;
    color: #1f1f1f !important;
    border-radius: 8px !important;
}
input, textarea {
    color: #1f1f1f !important;
    -webkit-text-fill-color: #1f1f1f !important;
}
input[type="date"] {
    color: #1f1f1f !important;
    -webkit-text-fill-color: #1f1f1f !important;
}
[data-testid="stInfo"] {
    background-color: #5a6478 !important;
    color: white !important;
}

/* Compacto para topograma */
.topo-compacto .titulo-bloque {
    font-size: 0.9rem !important;
    margin-bottom: 0.2rem !important;
}
.topo-compacto hr {
    margin: 0.15rem 0 0.25rem 0 !important;
}
.topo-compacto .stSelectbox label,
.topo-compacto .stTextInput label {
    font-size: 1.1rem !important;
}
.topo-compacto [data-baseweb="select"] > div,
.topo-compacto [data-baseweb="input"] > div {
    min-height: 3.6rem !important;
}
.topo-compacto [data-baseweb="select"] div,
.topo-compacto [data-baseweb="select"] span,
.topo-compacto [data-baseweb="select"] input,
.topo-compacto [data-baseweb="input"] input {
    font-size: 1.15rem !important;
}
.topo-compacto img {
    border-radius: 14px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# NAVEGACIÓN
# -------------------------
SECCION_ANTERIOR = {
    "Preparación de paciente": "A Practicar",
    "Topograma": "Preparación de paciente",
    "Adquisición": "Topograma",
    "Reconstrucción": "Adquisición",
    "Reformación": "Reconstrucción",
    "Jeringa inyectora": "Reformación",
}

SECCION_SIGUIENTE = {
    "Preparación de paciente": "Topograma",
    "Topograma": "Adquisición",
    "Adquisición": "Reconstrucción",
    "Reconstrucción": "Reformación",
    "Reformación": "Jeringa inyectora",
}

def ir_a(seccion_destino):
    st.session_state.seccion = seccion_destino

def volver_anterior():
    st.session_state.seccion = SECCION_ANTERIOR.get(st.session_state.seccion, "A Practicar")

# -------------------------
# VALIDACIONES
# -------------------------
def texto_completo(valor):
    return str(valor).strip() != ""

def seleccion_completa(valor):
    return valor not in ["", None, "Seleccionar"]

def lista_completa(valor):
    return isinstance(valor, list) and len(valor) > 0


def topograma_completo(prefijo="topo"):
    return all([
        seleccion_completa(st.session_state[f"{prefijo}_entrada_paciente"]),
        seleccion_completa(st.session_state[f"{prefijo}_posicionamiento"]),
        seleccion_completa(st.session_state[f"{prefijo}_posicion_tubo"]),
        seleccion_completa(st.session_state[f"{prefijo}_posicion_brazos"]),
        seleccion_completa(st.session_state[f"{prefijo}_region"]),
        texto_completo(st.session_state[f"{prefijo}_inicio"]),
        texto_completo(st.session_state[f"{prefijo}_termino"]),
    ])

def rx_campos_completos(prefijo="topo"):
    return all([
        seleccion_completa(st.session_state[f"{prefijo}_entrada_paciente"]),
        seleccion_completa(st.session_state[f"{prefijo}_posicionamiento"]),
        seleccion_completa(st.session_state[f"{prefijo}_posicion_tubo"]),
        seleccion_completa(st.session_state[f"{prefijo}_region"]),
    ])

# -------------------------
# IMAGEN DINÁMICA TOPOGRAMA
# -------------------------
def normalizar_texto_archivo(valor):
    return (
        str(valor)
        .strip()
        .lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .replace("izquerdo", "izquierdo")
        .replace("/", "_")
        .replace(" ", "_")
    )


# -------------------------
# MAPEO RX TOPOGRAMA DESDE REGLAS FIJAS
# -------------------------
PROTOCOLOS_TOPO_FALLBACK = [
    "Seleccionar",
    "cerebro",
    "cavidades perinasales",
    "maxilofacial",
    "orbitas",
    "oidos",
    "cuello",
    "columna cervical",
    "torax",
    "abdomen",
    "pelvis",
     "pielotac",
    "abdomen y pelvis",
    "columna dorsal",
    "columna lumbar",
    "torax abdomen y pelvis",
    "hombro",
    "brazo",
    "codo",
    "antebrazo",
    "muñeca",
    "mano",
    "cadera",
    "muslo",
    "rodilla",
    "pierna",
    "tobillo",
    "pie",   
]
TOPO_PROTOCOLOS = PROTOCOLOS_TOPO_FALLBACK
TOPO_RX_DIAG = {"archivo_encontrado": True, "filas_cargadas": 0, "error": ""}


def corregir_nombre_imagen(valor):
    nombre = normalizar_texto_archivo(valor)
    correcciones = {
        "abdomen_ateral": "abdomen_lateral",
        "abdomen_rontal": "abdomen_frontal",
        "abdomen__frontal": "abdomen_frontal",
        "abdomenpelvis__frontal": "abdomen_y_pelvis_frontal",
        "abdomenpelvis_frontal": "abdomen_y_pelvis_frontal",
        "abdomenpelvis_lateral": "abdomen_y_pelvis_lateral",
        "abdomen_y_pelvis__frontal": "abdomen_y_pelvis_frontal",
        "pelvis__frontal": "pelvis_frontal",
        "pelvis_pelvis__frontal": "pelvis_frontal",
        "torax_abdomen_pelvis_frontal": "torax_abdomen_y_pelvis_frontal",
        "torax_abdomen_pelvis_lateral": "torax_abdomen_y_pelvis_lateral",
        "mano_ateral": "mano_lateral",
        "mano_rontal": "mano_frontal",
        "muneca_frontal": "mano_muneca_frontal",
        "muneca_lateral": "mano_muneca_lateral",
        "mano_muneca_frontal": "mano_muneca_frontal",
        "mano_muneca_lateral": "mano_muneca_lateral",
        "pie_tobillo_frontal": "pie_tobillo_frontal",
        "pie_tobillo_lateral": "pie_tobillo_lateral",
        "columna_dorsal_frontal": "columna_frontal",
        "columna_dorsal_lateral": "columna_lateral",
        "columna_lumbar_frontal": "columna_frontal",
        "columna_lumbar_lateral": "columna_lateral",
    }
    nombre = correcciones.get(nombre, nombre)
    nombre = nombre.replace("__", "_").strip("_")
    return nombre


def determinar_vista_rx_topograma(posicionamiento, tubo):
    posicionamiento_norm = normalizar_texto_archivo(posicionamiento)
    tubo_norm = normalizar_texto_archivo(tubo)

    if posicionamiento_norm in ["supino", "prono"]:
        if tubo_norm in ["arriba", "abajo"]:
            return "frontal"
        if tubo_norm in ["derecha", "derecho", "izquierda", "izquierdo"]:
            return "lateral"

    if posicionamiento_norm in ["lateral_derecho", "lateral_izquierdo"]:
        if tubo_norm in ["derecha", "derecho", "izquierda", "izquierdo"]:
            return "frontal"
        if tubo_norm in ["arriba", "abajo"]:
            return "lateral"

    return None


def obtener_claves_rx(prefijo_estado="topo"):
    entrada = st.session_state.get(f"{prefijo_estado}_entrada_paciente", "Seleccionar")
    posicionamiento = st.session_state.get(f"{prefijo_estado}_posicionamiento", "Seleccionar")
    tubo = st.session_state.get(f"{prefijo_estado}_posicion_tubo", "Seleccionar")
    protocolo = st.session_state.get(f"{prefijo_estado}_region", "Seleccionar")

    if (
        entrada == "Seleccionar"
        or posicionamiento == "Seleccionar"
        or tubo == "Seleccionar"
        or protocolo == "Seleccionar"
    ):
        return []

    return [(
        normalizar_texto_archivo(entrada),
        normalizar_texto_archivo(posicionamiento),
        normalizar_texto_archivo(tubo),
        normalizar_texto_archivo(protocolo),
    )]


def obtener_clave_rx(prefijo_estado="topo"):
    claves = obtener_claves_rx(prefijo_estado)
    return claves[0] if claves else None


def _base_imagen_por_protocolo(protocolo_norm):
    mapa = {
        "cerebro": "cabeza",
        "cavidades_perinasales": "cabeza",
        "maxilofacial": "cabeza",
        "orbitas": "cabeza",
        "oidos": "cabeza",
        "cuello": "cuello",
        "columna_cervical": "cuello",
        "torax": "torax",
        "abdomen": "abdomen",
        "pelvis": "pelvis",
        "cadera": "pelvis",
        "abdomen_y_pelvis": "abdomen_y_pelvis",
        "pielotac": "pielotac",
        "columna_dorsal": "columna_dorsal",
        "columna_lumbar": "columna_lumbar",
        "torax_abdomen_y_pelvis": "torax_abdomen_y_pelvis",
        "hombro": "hombro",
        "brazo": "brazo",
        "codo": "codo",
        "antebrazo": "antebrazo",
        "muñeca": "mano_muneca",
        "muneca": "mano_muneca",
        "mano": "mano",
        "rodilla": "rodilla",
        "pierna": "pierna",
        "tobillo": "pie_tobillo",
        "pie": "pie_tobillo",
        "pielotac": "pielotac",
        "muslo": "muslo",
    }
    return mapa.get(protocolo_norm)


def obtener_nombre_imagen_rx(prefijo_estado="topo"):
    entrada = st.session_state.get(f"{prefijo_estado}_entrada_paciente", "Seleccionar")
    posicionamiento = st.session_state.get(f"{prefijo_estado}_posicionamiento", "Seleccionar")
    tubo = st.session_state.get(f"{prefijo_estado}_posicion_tubo", "Seleccionar")
    protocolo = st.session_state.get(f"{prefijo_estado}_region", "Seleccionar")

    if not all([
        seleccion_completa(entrada),
        seleccion_completa(posicionamiento),
        seleccion_completa(tubo),
        seleccion_completa(protocolo),
    ]):
        return None

    vista = determinar_vista_rx_topograma(posicionamiento, tubo)
    if vista is None:
        return None

    protocolo_norm = normalizar_texto_archivo(protocolo)
    base = _base_imagen_por_protocolo(protocolo_norm)
    if base is None:
        return None

    return f"{base} {vista}"


def combinacion_rx_disponible(prefijo_estado="topo"):
    return obtener_imagen_rx_topograma(prefijo_estado) is not None


def buscar_archivo_imagen_por_nombre(nombre_base):
    if not nombre_base:
        return None

    nombre_base = str(nombre_base).strip()
    candidatos = []
    candidatos_normalizados = set()

    def agregar_candidato(valor):
        valor = str(valor).strip()
        if not valor:
            return
        valor = corregir_nombre_imagen(valor)
        if valor not in candidatos_normalizados:
            candidatos.append(valor)
            candidatos_normalizados.add(valor)

    agregar_candidato(nombre_base)
    agregar_candidato(nombre_base.replace("_", " "))
    agregar_candidato(nombre_base.replace(" ", "_"))

    alias = {
        "abdomen_y_pelvis_frontal": ["abdomen_y_pelvis_frontal", "abdomen_pelvis_frontal", "abdomenpelvis_frontal"],
        "abdomen_y_pelvis_lateral": ["abdomen_y_pelvis_lateral", "abdomen_pelvis_lateral", "abdomenpelvis_lateral"],
        "torax_abdomen_y_pelvis_frontal": ["torax_abdomen_y_pelvis_frontal", "torax_abdomen_pelvis_frontal"],
        "torax_abdomen_y_pelvis_lateral": ["torax_abdomen_y_pelvis_lateral", "torax_abdomen_pelvis_lateral"],
        "mano_muneca_frontal": ["mano_muneca_frontal", "muneca_frontal", "mano_frontal"],
        "mano_muneca_lateral": ["mano_muneca_lateral", "muneca_lateral", "mano_lateral"],
        "pie_tobillo_frontal": ["pie_tobillo_frontal", "tobillo_frontal", "pie_frontal"],
        "pie_tobillo_lateral": ["pie_tobillo_lateral", "tobillo_lateral", "pie_lateral"],
        "columna_dorsal_frontal": ["columna_dorsal_frontal", "columna_frontal"],
        "columna_dorsal_lateral": ["columna_dorsal_lateral", "columna_lateral"],
        "columna_lumbar_frontal": ["columna_lumbar_frontal", "columna_frontal"],
        "columna_lumbar_lateral": ["columna_lumbar_lateral", "columna_lateral"],
    }
    for candidato in list(candidatos):
        for extra in alias.get(candidato, []):
            agregar_candidato(extra)

    extensiones_validas = {".png", ".jpg", ".jpeg", ".webp"}
    archivos = [p for p in BASE_DIR.iterdir() if p.is_file() and p.suffix.lower() in extensiones_validas]

    mapa_archivos = {}
    for archivo in archivos:
        stem_normalizado = corregir_nombre_imagen(archivo.stem)
        mapa_archivos.setdefault(stem_normalizado, archivo)

    for candidato in candidatos:
        if candidato in mapa_archivos:
            return mapa_archivos[candidato]

    extensiones = ["", ".png", ".jpg", ".jpeg", ".webp"]
    for candidato in candidatos:
        for ext in extensiones:
            ruta = BASE_DIR / f"{candidato}{ext}"
            if ruta.exists():
                return ruta

    return None


def obtener_imagen_topograma_generico(prefijo_estado="topo", sufijo_imagen=""):
    entrada = st.session_state.get(f"{prefijo_estado}_entrada_paciente", "Seleccionar")
    posicionamiento = st.session_state.get(f"{prefijo_estado}_posicionamiento", "Seleccionar")
    tubo = st.session_state.get(f"{prefijo_estado}_posicion_tubo", "Seleccionar")

    if (
        entrada == "Seleccionar"
        or posicionamiento == "Seleccionar"
        or tubo == "Seleccionar"
    ):
        return TOPOGRAMA_IMG if TOPOGRAMA_IMG.exists() else None

    entrada_norm = normalizar_texto_archivo(entrada)
    posicionamiento_norm = normalizar_texto_archivo(posicionamiento)
    tubo_norm = normalizar_texto_archivo(tubo)

    variantes_tubo = [tubo_norm]
    if tubo_norm == "derecha":
        variantes_tubo.append("derecho")
    elif tubo_norm == "izquierda":
        variantes_tubo.append("izquierdo")

    candidatos = []
    extensiones = [".png", ".jpg", ".jpeg", ".webp"]

    for tubo_variante in variantes_tubo:
        bases = [
            f"topograma_{entrada_norm}_{posicionamiento_norm}_{tubo_variante}",
            f"topograma_{entrada_norm}__{posicionamiento_norm}__{tubo_variante}",
            f"topograma_{entrada_norm}_{posicionamiento_norm}__{tubo_variante}",
            f"topograma_{entrada_norm}__{posicionamiento_norm}_{tubo_variante}",
        ]
        for base in bases:
            for ext in extensiones:
                candidatos.append(f"{base}{ext}")

    candidatos_unicos = []
    for nombre in candidatos:
        if nombre not in candidatos_unicos:
            candidatos_unicos.append(nombre)

    for nombre in candidatos_unicos:
        ruta_imagen = BASE_DIR / nombre
        if ruta_imagen.exists():
            if sufijo_imagen:
                st.session_state[f"nombre_topograma_actual_{sufijo_imagen}"] = nombre
            else:
                st.session_state["nombre_topograma_actual"] = nombre
            return ruta_imagen

    return TOPOGRAMA_IMG if TOPOGRAMA_IMG.exists() else None


def obtener_imagen_topograma():
    return obtener_imagen_topograma_generico("topo", "")


def obtener_imagen_rx_topograma(prefijo_estado="topo"):
    nombre_imagen = obtener_nombre_imagen_rx(prefijo_estado)
    if not nombre_imagen:
        return None
    return buscar_archivo_imagen_por_nombre(nombre_imagen)


# -------------------------
# PÁGINAS
# -------------------------
seccion = st.session_state.seccion

if seccion == "Portada":
    st.markdown('<div class="portada-fondo">', unsafe_allow_html=True)
    st.markdown('<div class="portada-titulo">Tomografía Computada Aplicada</div>', unsafe_allow_html=True)
    st.markdown('<div class="portada-subtitulo">Simulador interactivo para práctica de preparación, adquisición, reconstrucción y cálculos.</div>', unsafe_allow_html=True)

    if PORTADA_IMG.exists():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.image(str(PORTADA_IMG), use_container_width=True)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.5, 2, 1.5])
    with c2:
        if st.button("Ir a A Practicar", use_container_width=True):
            ir_a("A Practicar")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

elif seccion == "A Practicar":
    st.title("Simulador de Tomografía Computada")
    st.header("A Practicar")
    st.write("Selecciona una etapa del simulador:")

    col_img, col_menu = st.columns([1.15, 1], vertical_alignment="center")

    with col_img:
        st.markdown('<div class="bloque-a-practicar">', unsafe_allow_html=True)
        if A_PRACTICAR_IMG.exists():
            st.image(str(A_PRACTICAR_IMG), use_container_width=True)
        else:
            st.info("Guarda la imagen como 'a_practicar.png' en la misma carpeta del app.py.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_menu:
        st.markdown('<div class="bloque-a-practicar">', unsafe_allow_html=True)
        if st.button("Preparación del paciente", use_container_width=True):
            ir_a("Preparación de paciente"); st.rerun()
        if st.button("Topograma", use_container_width=True):
            ir_a("Topograma"); st.rerun()
        if st.button("Adquisición", use_container_width=True):
            ir_a("Adquisición"); st.rerun()
        if st.button("Reconstrucción", use_container_width=True):
            ir_a("Reconstrucción"); st.rerun()
        if st.button("Reformación", use_container_width=True):
            ir_a("Reformación"); st.rerun()
        if st.button("Jeringa inyectora", use_container_width=True):
            ir_a("Jeringa inyectora"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.info("Haz clic en una etapa para continuar.")

elif seccion == "Preparación de paciente":
    st.header("Preparación de paciente")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_anterior(); st.rerun()

    col_izq, col_centro, col_img = st.columns([1.15, 1.15, 0.75])

    with col_izq:
        st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-bloque">Datos del paciente</div>', unsafe_allow_html=True)

        persistent_text_input("Nombres", "prep_nombres")
        persistent_text_input("Apellidos", "prep_apellidos")

        c1, c2 = st.columns([1.2, 0.8])
        with c1:
            persistent_date_input(
                "Fecha de nacimiento",
                "prep_fecha_nac",
                min_value=date(1900, 1, 1),
                max_value=date.today()
            )
        with c2:
            hoy = date.today()
            fecha_nac = st.session_state["prep_fecha_nac"]
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric("Edad", f"{edad} años")

        persistent_text_input("Examen", "prep_examen")

        c3, c4 = st.columns(2)
        with c3:
            persistent_selectbox("Peso (kg)", list(range(1, 201)), "prep_peso")
        with c4:
            persistent_selectbox("Embarazo", ["Seleccionar", "SI", "NO", "NO APLICA"], "prep_embarazo")

        persistent_selectbox("Creatinina", ["Seleccionar", "SI", "NO"], "prep_creatinina")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_centro:
        st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-bloque">Preparación para contraste</div>', unsafe_allow_html=True)

        persistent_selectbox("Medio de contraste EV", ["Seleccionar", "SI", "NO", "NO APLICA"], "prep_medio_contraste_ev")

        if st.session_state["prep_medio_contraste_ev"] != "NO":
            c5, c6 = st.columns(2)
            with c5:
                persistent_selectbox("Vía venosa", ["Seleccionar", "24G", "22G", "20G", "18G", "16G", "CVC", "NO APLICA"], "prep_via_venosa")
            with c6:
                persistent_selectbox(
                    "Cantidad contraste",
                    ["Seleccionar", "10 cc", "20 cc", "30 cc", "40 cc", "50 cc", "60 cc", "70 cc", "80 cc",
                     "90 cc", "100 cc", "110 cc", "120 cc", "130 cc", "140 cc", "150 cc",
                     "160 cc", "170 cc", "180 cc", "190 cc", "200 cc"],
                    "prep_cantidad_contraste"
                )

            c7, c8 = st.columns(2)
            with c7:
                persistent_selectbox("Método de inyección", ["Seleccionar", "JERINGA INYECTORA", "JERINGA MANUAL", "NO APLICA"], "prep_metodo_inyeccion")
            with c8:
                persistent_selectbox("Contraste oral", ["Seleccionar", "NO APLICA", "AGUA", "AIRE", "CONTRASTE POSITIVO"], "prep_medio_contraste_oral")

        st.markdown('</div>', unsafe_allow_html=True)

    preparacion_completa = all([
        texto_completo(st.session_state["prep_nombres"]),
        texto_completo(st.session_state["prep_apellidos"]),
        texto_completo(st.session_state["prep_examen"]),
        seleccion_completa(st.session_state["prep_embarazo"]),
        seleccion_completa(st.session_state["prep_creatinina"]),
        seleccion_completa(st.session_state["prep_medio_contraste_ev"]),
    ])

    if st.session_state["prep_medio_contraste_ev"] != "NO":
        preparacion_completa = preparacion_completa and all([
            seleccion_completa(st.session_state["prep_via_venosa"]),
            seleccion_completa(st.session_state["prep_cantidad_contraste"]),
            seleccion_completa(st.session_state["prep_metodo_inyeccion"]),
            seleccion_completa(st.session_state["prep_medio_contraste_oral"]),
        ])

    with col_img:
        st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-bloque">Imagen</div>', unsafe_allow_html=True)
        if PACIENTE_IMG is not None and PACIENTE_IMG.exists():
            st.image(str(PACIENTE_IMG), width=260)
        else:
            st.info("Guarda la imagen como 'paciente.png' o 'paciente.jpg' en la misma carpeta del app.py.")

        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        if st.button("Siguiente", use_container_width=True, disabled=not preparacion_completa):
            ir_a("Topograma"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    hoy = date.today()
    fecha_nac = st.session_state["prep_fecha_nac"]
    edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

    st.divider()
    st.subheader("Resumen")
    st.markdown('<div class="bloque-resumen">', unsafe_allow_html=True)
    st.write(f"**Paciente:** {st.session_state['prep_nombres']} {st.session_state['prep_apellidos']}")
    st.write(f"**Edad:** {edad} años")
    st.write(f"**Examen:** {st.session_state['prep_examen']}")
    st.write(f"**Peso:** {st.session_state['prep_peso']} kg")
    st.write(f"**Embarazo:** {st.session_state['prep_embarazo']}")
    st.write(f"**Creatinina:** {st.session_state['prep_creatinina']}")
    st.write(f"**Medio de contraste EV:** {st.session_state['prep_medio_contraste_ev']}")
    if st.session_state["prep_medio_contraste_ev"] != "NO":
        st.write(f"**Vía venosa:** {st.session_state['prep_via_venosa']}")
        st.write(f"**Cantidad de contraste:** {st.session_state['prep_cantidad_contraste']}")
        st.write(f"**Método de inyección:** {st.session_state['prep_metodo_inyeccion']}")
        st.write(f"**Medio de contraste oral:** {st.session_state['prep_medio_contraste_oral']}")
    st.markdown('</div>', unsafe_allow_html=True)

elif seccion == "Topograma":
    st.header("Topograma")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_anterior(); st.rerun()

    st.markdown('<div class="topo-compacto">', unsafe_allow_html=True)

    st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-bloque">Topograma 1</div>', unsafe_allow_html=True)

    topograma1_completo = topograma_completo("topo")
    topograma1_rx_campos = rx_campos_completos("topo")
    topograma1_rx_disponible = combinacion_rx_disponible("topo")

    layout_izq, layout_der = st.columns([1.15, 0.65], vertical_alignment="top")

    with layout_izq:
        st.markdown(
            """
            <div style="
                border:1px solid #7a7a7a;
                border-radius:14px;
                overflow:hidden;
                background-color:#565656;
                margin-bottom:0.25rem;
            ">
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div style="padding:0.25rem 0.45rem 0.05rem 0.45rem; font-weight:700; color:white;">Configuración del topograma</div>', unsafe_allow_html=True)

        st.markdown('<div style="padding:0 0.55rem 0.3rem 0.55rem;">', unsafe_allow_html=True)
        persistent_selectbox("Entrada paciente", ["Seleccionar", "CABEZA PRIMERO", "PIES PRIMERO"], "topo_entrada_paciente")
        persistent_selectbox("Posición del tubo", ["Seleccionar", "Arriba", "Abajo", "Derecha", "Izquierda"], "topo_posicion_tubo")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="border-top:1px solid #8a8a8a; padding:0.3rem 0.55rem 0.3rem 0.55rem;">', unsafe_allow_html=True)
        persistent_selectbox("Posicionamiento", ["Seleccionar", "SUPINO", "PRONO", "LATERAL DERECHO", "LATERAL IZQUIERDO"], "topo_posicionamiento")
        persistent_selectbox(
            "Posición de brazos / extremidades",
            ["Seleccionar", "BRAZOS ARRIBA", "BRAZOS ABAJO", "ELEVA BRAZO DERECHO", "ELEVA BRAZO IZQUIERDO",
             "FLEXIÓN EXTREMIDAD INFERIOR DERECHA", "FLEXIÓN EXTREMIDAD INFERIOR IZQUIERDA"],
            "topo_posicion_brazos"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="border-top:1px solid #8a8a8a; padding:0.3rem 0.55rem 0.45rem 0.55rem;">', unsafe_allow_html=True)
        persistent_selectbox("Protocolo", TOPO_PROTOCOLOS, "topo_region")

        mini1, mini2 = st.columns(2)
        with mini1:
            persistent_text_input("Inicio topograma", "topo_inicio")
        with mini2:
            persistent_text_input("Término topograma", "topo_termino")
        st.markdown('</div></div>', unsafe_allow_html=True)

    with layout_der:
        imagen_equipo_topo_1 = obtener_imagen_topograma()
        c1, c2, c3 = st.columns([0.22, 0.56, 0.22])
        with c2:
            if imagen_equipo_topo_1 is not None and imagen_equipo_topo_1.exists():
                st.image(str(imagen_equipo_topo_1), use_container_width=True)
            else:
                st.info("No se encontró la imagen de posicionamiento del topograma 1.")

        st.markdown("<div style='height:3px;'></div>", unsafe_allow_html=True)

        c4, c5, c6 = st.columns([0.22, 0.56, 0.22])
        with c5:
            if st.session_state.get("topo_rx_iniciado", False):
                imagen_rx_topo_1 = obtener_imagen_rx_topograma("topo")
                if imagen_rx_topo_1 is not None and imagen_rx_topo_1.exists():
                    st.image(str(imagen_rx_topo_1), use_container_width=True)
                else:
                    st.markdown(
                        """
                        <div style="
                            min-height:120px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            border:1px solid #7a7a7a;
                            border-radius:14px;
                            background-color:#4a4a4a;
                            color:white;
                            font-weight:600;
                            text-align:center;
                            padding:0.35rem;
                        ">
                            No se encontró el archivo de imagen para esta combinación
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    """
                    <div style="
                        min-height:120px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        border:1px solid #7a7a7a;
                        border-radius:14px;
                        background-color:#4a4a4a;
                        color:white;
                        font-weight:600;
                        text-align:center;
                        padding:0.35rem;
                    ">
                        La imagen del topograma aparecerá al presionar<br><b>Iniciar RX</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    if topograma1_rx_campos and not topograma1_rx_disponible:
        st.warning("La combinación seleccionada no tiene imagen asociada, por eso Iniciar RX permanece desactivado.")

    btn1, btn2, btn3 = st.columns([1.5, 1.9, 1.5])
    with btn2:
        if st.button("Iniciar RX topograma 1", use_container_width=True, disabled=not (topograma1_rx_campos and topograma1_rx_disponible)):
            st.session_state["topo_rx_iniciado"] = True
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    sig1, sig2, sig3 = st.columns([2.2, 1.6, 2.2])
    with sig2:
        puede_avanzar = topograma1_completo and topograma1_rx_disponible

        if st.button("Siguiente", use_container_width=True, disabled=not puede_avanzar):
            ir_a("Adquisición")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("Resumen")
    st.markdown('<div class="bloque-resumen">', unsafe_allow_html=True)
    st.write(f"**Entrada paciente:** {st.session_state['topo_entrada_paciente']}")
    st.write(f"**Posición del tubo:** {st.session_state['topo_posicion_tubo']}")
    st.write(f"**Posicionamiento:** {st.session_state['topo_posicionamiento']}")
    st.write(f"**Posición de brazos / extremidades:** {st.session_state['topo_posicion_brazos']}")
    st.write(f"**Protocolo:** {st.session_state['topo_region']}")
    st.write(f"**Inicio:** {st.session_state['topo_inicio']}")
    st.write(f"**Término:** {st.session_state['topo_termino']}")
    nombre_img_1 = obtener_nombre_imagen_rx("topo")
    st.write(f"**Imagen RX asociada:** {nombre_img_1 if nombre_img_1 else 'No disponible para esta combinación'}")
    st.markdown('</div>', unsafe_allow_html=True)

elif seccion == "Adquisición":
    st.header("Adquisición")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_anterior(); st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        persistent_selectbox("kVp", ["Seleccionar", 80, 100, 120, 140], "adq_kvp")
        persistent_number_input("mAs", "adq_mas", min_value=1)
        persistent_number_input("Pitch", "adq_pitch", min_value=0.1, step=0.1)
        persistent_number_input("Tiempo de rotación (s)", "adq_rotacion", min_value=0.1, step=0.1)

    with col2:
        persistent_text_input("Colimación", "adq_colimacion")
        persistent_number_input("Espesor de corte (mm)", "adq_espesor_corte", min_value=0.1, step=0.1)
        persistent_number_input("Longitud de barrido (cm)", "adq_longitud", min_value=1.0)
        persistent_selectbox("Modo de adquisición", ["Seleccionar", "Helicoidal", "Secuencial"], "adq_modo")

    adquisicion_completa = all([
        seleccion_completa(st.session_state["adq_kvp"]),
        texto_completo(st.session_state["adq_colimacion"]),
        seleccion_completa(st.session_state["adq_modo"]),
    ])

    st.divider()
    st.subheader("Resumen")
    st.markdown('<div class="bloque-resumen">', unsafe_allow_html=True)
    st.write(f"**kVp:** {st.session_state['adq_kvp']}")
    st.write(f"**mAs:** {st.session_state['adq_mas']}")
    st.write(f"**Pitch:** {st.session_state['adq_pitch']}")
    st.write(f"**Tiempo de rotación:** {st.session_state['adq_rotacion']} s")
    st.write(f"**Colimación:** {st.session_state['adq_colimacion']}")
    st.write(f"**Espesor de corte:** {st.session_state['adq_espesor_corte']} mm")
    st.write(f"**Longitud:** {st.session_state['adq_longitud']} cm")
    st.write(f"**Modo:** {st.session_state['adq_modo']}")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.5, 2, 1.5])
    with c2:
        if st.button("Siguiente", use_container_width=True, disabled=not adquisicion_completa):
            ir_a("Reconstrucción"); st.rerun()

elif seccion == "Reconstrucción":
    st.header("Reconstrucción")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_anterior(); st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        persistent_selectbox("Kernel / filtro", ["Seleccionar", "Blando", "Estándar", "Óseo", "Pulmonar", "Otro"], "recon_kernel")
        persistent_number_input("Grosor de reconstrucción (mm)", "recon_grosor", min_value=0.1, step=0.1)
        persistent_number_input("Intervalo de reconstrucción (mm)", "recon_intervalo", min_value=0.1, step=0.1)

    with col2:
        persistent_multiselect("Planos reconstruidos", ["Axial", "Coronal", "Sagital", "Oblicuo"], "recon_planos")
        persistent_selectbox("Algoritmo", ["Seleccionar", "FBP", "Iterativa", "Otro"], "recon_algoritmo")
        persistent_selectbox("Ventana principal", ["Seleccionar", "Partes blandas", "Pulmón", "Ósea", "Otra"], "recon_ventana")

    reconstruccion_completa = all([
        seleccion_completa(st.session_state["recon_kernel"]),
        lista_completa(st.session_state["recon_planos"]),
        seleccion_completa(st.session_state["recon_algoritmo"]),
        seleccion_completa(st.session_state["recon_ventana"]),
    ])

    st.divider()
    st.subheader("Resumen")
    st.markdown('<div class="bloque-resumen">', unsafe_allow_html=True)
    st.write(f"**Kernel:** {st.session_state['recon_kernel']}")
    st.write(f"**Grosor:** {st.session_state['recon_grosor']} mm")
    st.write(f"**Intervalo:** {st.session_state['recon_intervalo']} mm")
    st.write(f"**Planos:** {', '.join(st.session_state['recon_planos']) if st.session_state['recon_planos'] else 'Ninguno'}")
    st.write(f"**Algoritmo:** {st.session_state['recon_algoritmo']}")
    st.write(f"**Ventana:** {st.session_state['recon_ventana']}")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.5, 2, 1.5])
    with c2:
        if st.button("Siguiente", use_container_width=True, disabled=not reconstruccion_completa):
            ir_a("Reformación"); st.rerun()

elif seccion == "Reformación":
    st.header("Reformación")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_anterior(); st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        persistent_multiselect("Tipo de reformación", ["MPR coronal", "MPR sagital", "MIP", "MinIP", "VR", "Curva"], "reform_tipo")
        persistent_number_input("Grosor MIP / slab (mm)", "reform_grosor", min_value=0.1, step=0.1)
    with col2:
        persistent_selectbox("Orientación principal", ["Seleccionar", "Coronal", "Sagital", "Oblicua"], "reform_orientacion")
        persistent_text_area("Observaciones de reformación", "reform_observaciones")

    reformacion_completa = all([
        lista_completa(st.session_state["reform_tipo"]),
        seleccion_completa(st.session_state["reform_orientacion"]),
        texto_completo(st.session_state["reform_observaciones"]),
    ])

    st.divider()
    st.subheader("Resumen")
    st.markdown('<div class="bloque-resumen">', unsafe_allow_html=True)
    st.write(f"**Tipo:** {', '.join(st.session_state['reform_tipo']) if st.session_state['reform_tipo'] else 'Ninguno'}")
    st.write(f"**Grosor slab:** {st.session_state['reform_grosor']} mm")
    st.write(f"**Orientación:** {st.session_state['reform_orientacion']}")
    st.write(f"**Observaciones:** {st.session_state['reform_observaciones']}")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.5, 2, 1.5])
    with c2:
        if st.button("Siguiente", use_container_width=True, disabled=not reformacion_completa):
            ir_a("Jeringa inyectora"); st.rerun()

elif seccion == "Jeringa inyectora":
    st.header("Jeringa inyectora")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_anterior(); st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        persistent_selectbox("Tipo de contraste", ["Yodado", "No iónico", "Isoosmolar"], "jer_tipo_contraste")
        persistent_number_input("Volumen de contraste (ml)", "jer_volumen_contraste", min_value=1.0, step=1.0)
        persistent_number_input("Flujo (ml/s)", "jer_flujo", min_value=0.1, step=0.1)

    with col2:
        persistent_number_input("Flush / suero (ml)", "jer_flush", min_value=0.0, step=1.0)
        persistent_number_input("Tiempo delay (s)", "jer_tiempo_delay", min_value=0.0, step=1.0)
        persistent_selectbox("Sitio de punción", ["Seleccionar", "MSD", "MSI", "Pliegue antecubital derecho", "Pliegue antecubital izquierdo", "CVC"], "jer_sitio_puncion")

    jeringa_completa = all([
        texto_completo(st.session_state["jer_tipo_contraste"]),
        seleccion_completa(st.session_state["jer_sitio_puncion"]),
    ])

    st.divider()
    st.subheader("Resumen")
    st.markdown('<div class="bloque-resumen">', unsafe_allow_html=True)
    st.write(f"**Tipo de contraste:** {st.session_state['jer_tipo_contraste']}")
    st.write(f"**Volumen de contraste:** {st.session_state['jer_volumen_contraste']} ml")
    st.write(f"**Flujo:** {st.session_state['jer_flujo']} ml/s")
    st.write(f"**Flush:** {st.session_state['jer_flush']} ml")
    st.write(f"**Tiempo delay:** {st.session_state['jer_tiempo_delay']} s")
    st.write(f"**Sitio de punción:** {st.session_state['jer_sitio_puncion']}")
    st.markdown('</div>', unsafe_allow_html=True)

    if jeringa_completa:
        st.success("Simulación completada.")
