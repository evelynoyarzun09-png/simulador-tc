import streamlit as st
from pathlib import Path
from datetime import date
import hmac

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

# -------------------------
# INICIALIZAR DATOS DE FORMULARIOS
# -------------------------
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
    "topo_plano": "Seleccionar",
    "topo_inicio": "",
    "topo_termino": "",

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
    .stApp {
        background-color: #111111;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 820px;
    }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText {
        color: white !important;
    }
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
        margin-bottom: 0.8rem;
    }
    .login-subtitulo {
        text-align: center;
        color: white;
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
    }
    div[data-baseweb="input"] > div {
        background-color: #d0d5dd !important;
        color: #111111 !important;
        border-radius: 12px !important;
    }
    input {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }
    div.stButton > button {
        background-color: #b8bec7 !important;
        color: #1f1f1f !important;
        border-radius: 12px !important;
        border: 1px solid #9ca3ad !important;
        font-weight: 600 !important;
        min-height: 46px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-titulo">Tomografía Computada Aplicada</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="login-subtitulo">Ingrese la clave para acceder al simulador.</div>',
        unsafe_allow_html=True
    )

    if PORTADA_IMG.exists():
        st.image(str(PORTADA_IMG), use_container_width=True)

    st.text_input(
        "Clave de acceso",
        type="password",
        key="clave_ingresada",
        on_change=verificar_clave
    )

    if st.session_state.get("error_clave", False):
        st.error("Clave incorrecta. Inténtalo nuevamente.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

seccion = st.session_state.seccion

# -------------------------
# ESTILOS
# -------------------------
st.markdown("""
<style>
.stApp {
    background-color: #505050;
}
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText {
    color: white !important;
}
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
div.stButton > button {
    background-color: #b8bec7 !important;
    color: #1f1f1f !important;
    border-radius: 12px !important;
    border: 1px solid #9ca3ad !important;
    font-weight: 600 !important;
    min-height: 46px !important;
}
div.stButton > button:disabled {
    background-color: #8a8f97 !important;
    color: #e6e6e6 !important;
    border: 1px solid #7a7a7a !important;
    opacity: 0.75 !important;
}
.bloque-resumen {
    background-color: #616161;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    border: 1px solid #7a7a7a;
}
.bloque-seccion {
    background-color: #616161;
    padding: 1rem 1rem 0.8rem 1rem;
    border-radius: 14px;
    border: 1px solid #7a7a7a;
    margin-bottom: 1rem;
}
.bloque-a-practicar {
    background-color: #616161;
    padding: 1.2rem;
    border-radius: 16px;
    border: 1px solid #7a7a7a;
    margin-bottom: 1rem;
}
.titulo-bloque {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
    color: white;
}
.bloque-a-practicar img,
.bloque-seccion img {
    border-radius: 14px;
}
[data-testid="stMetricValue"] {
    font-size: 1.35rem !important;
}
[data-testid="stMetricLabel"] {
    color: white !important;
}
div[data-baseweb="select"] > div {
    background-color: #b8bec7 !important;
    border-radius: 12px !important;
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
div[data-baseweb="input"] > div {
    background-color: #b8bec7 !important;
    color: #1f1f1f !important;
    border-radius: 12px !important;
}
div[data-baseweb="textarea"] > div {
    background-color: #b8bec7 !important;
    color: #1f1f1f !important;
    border-radius: 12px !important;
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
.boton-volver {
    margin-top: 0.4rem;
    margin-bottom: 1rem;
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

def ir_a_practicar():
    st.session_state.seccion = "A Practicar"

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

def topograma_texto_completo(valor):
    return str(valor).strip() != ""

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

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    col_btn1, col_btn2, col_btn3 = st.columns([1.5, 2, 1.5])
    with col_btn2:
        if st.button("Ir a A Practicar", use_container_width=True):
            ir_a_practicar()
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# A PRACTICAR
# -------------------------
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
            ir_a("Preparación de paciente")
            st.rerun()

        if st.button("Topograma", use_container_width=True):
            ir_a("Topograma")
            st.rerun()

        if st.button("Adquisición", use_container_width=True):
            ir_a("Adquisición")
            st.rerun()

        if st.button("Reconstrucción", use_container_width=True):
            ir_a("Reconstrucción")
            st.rerun()

        if st.button("Reformación", use_container_width=True):
            ir_a("Reformación")
            st.rerun()

        if st.button("Jeringa inyectora", use_container_width=True):
            ir_a("Jeringa inyectora")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# PREPARACIÓN
# -------------------------
elif seccion == "Preparación de paciente":
    st.header("Preparación de paciente")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True, key="btn_volver_prep"):
            volver_anterior()
            st.rerun()

    col_izq, col_centro, col_img = st.columns([1.15, 1.15, 0.75])

    with col_izq:
        st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-bloque">Datos del paciente</div>', unsafe_allow_html=True)

        nombres = st.text_input("Nombres", key="prep_nombres")
        apellidos = st.text_input("Apellidos", key="prep_apellidos")

        c1, c2 = st.columns([1.2, 0.8])
        with c1:
            fecha_nac = st.date_input("Fecha de nacimiento", key="prep_fecha_nac")
        with c2:
            hoy = date.today()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric("Edad", f"{edad} años")

        examen = st.text_input("Examen", key="prep_examen")

        c3, c4 = st.columns(2)
        with c3:
            peso = st.selectbox("Peso (kg)", list(range(1, 201)), key="prep_peso")
        with c4:
            embarazo = st.selectbox("Embarazo", ["Seleccionar", "SI", "NO", "NO APLICA"], key="prep_embarazo")

        creatinina = st.selectbox("Creatinina", ["Seleccionar", "SI", "NO"], key="prep_creatinina")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_centro:
        st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-bloque">Preparación para contraste</div>', unsafe_allow_html=True)

        medio_contraste_ev = st.selectbox(
            "Medio de contraste EV",
            ["Seleccionar", "SI", "NO", "NO APLICA"],
            key="prep_medio_contraste_ev"
        )

        if medio_contraste_ev != "NO":
            c5, c6 = st.columns(2)
            with c5:
                via_venosa = st.selectbox(
                    "Vía venosa",
                    ["Seleccionar", "24G", "22G", "20G", "18G", "16G", "CVC", "NO APLICA"],
                    key="prep_via_venosa"
                )
            with c6:
                cantidad_contraste = st.selectbox(
                    "Cantidad contraste",
                    [
                        "Seleccionar", "10 cc", "20 cc", "30 cc", "40 cc", "50 cc", "60 cc", "70 cc", "80 cc",
                        "90 cc", "100 cc", "110 cc", "120 cc", "130 cc", "140 cc", "150 cc",
                        "160 cc", "170 cc", "180 cc", "190 cc", "200 cc"
                    ],
                    key="prep_cantidad_contraste"
                )

            c7, c8 = st.columns(2)
            with c7:
                metodo_inyeccion = st.selectbox(
                    "Método de inyección",
                    ["Seleccionar", "JERINGA INYECTORA", "JERINGA MANUAL", "NO APLICA"],
                    key="prep_metodo_inyeccion"
                )
            with c8:
                medio_contraste_oral = st.selectbox(
                    "Contraste oral",
                    ["Seleccionar", "NO APLICA", "AGUA", "AIRE", "CONTRASTE POSITIVO"],
                    key="prep_medio_contraste_oral"
                )
        else:
            via_venosa = st.session_state["prep_via_venosa"]
            cantidad_contraste = st.session_state["prep_cantidad_contraste"]
            metodo_inyeccion = st.session_state["prep_metodo_inyeccion"]
            medio_contraste_oral = st.session_state["prep_medio_contraste_oral"]

        st.markdown('</div>', unsafe_allow_html=True)

    preparacion_completa = all([
        texto_completo(nombres),
        texto_completo(apellidos),
        texto_completo(examen),
        seleccion_completa(embarazo),
        seleccion_completa(creatinina),
        seleccion_completa(medio_contraste_ev),
    ])

    if medio_contraste_ev != "NO":
        preparacion_completa = preparacion_completa and all([
            seleccion_completa(via_venosa),
            seleccion_completa(cantidad_contraste),
            seleccion_completa(metodo_inyeccion),
            seleccion_completa(medio_contraste_oral),
        ])

    with col_img:
        st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-bloque">Imagen</div>', unsafe_allow_html=True)

        if PACIENTE_IMG is not None and PACIENTE_IMG.exists():
            st.image(str(PACIENTE_IMG), width=260)
        else:
            st.info("Guarda la imagen como 'paciente.png' o 'paciente.jpg' en la misma carpeta del app.py.")

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        if st.button("Siguiente", use_container_width=True, disabled=not preparacion_completa, key="btn_sig_prep"):
            ir_a("Topograma")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# TOPOGRAMA
# -------------------------
elif seccion == "Topograma":
    st.header("Topograma")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True, key="btn_volver_topo"):
            volver_anterior()
            st.rerun()

    col_izq, col_der = st.columns([1.35, 0.85], vertical_alignment="top")

    with col_izq:
        st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-bloque">Posicionamiento del paciente</div>', unsafe_allow_html=True)

        fila1_col1, fila1_col2 = st.columns(2)
        with fila1_col1:
            entrada_paciente = st.selectbox(
                "Entrada paciente",
                ["Seleccionar", "CABEZA PRIMERO", "PIES PRIMERO"],
                key="topo_entrada_paciente"
            )
        with fila1_col2:
            posicionamiento = st.selectbox(
                "Posicionamiento",
                ["Seleccionar", "SUPINO", "PRONO", "LATERAL DERECHO", "LATERAL IZQUIERDO"],
                key="topo_posicionamiento"
            )

        fila2_col1, fila2_col2 = st.columns(2)
        with fila2_col1:
            posicion_tubo = st.selectbox(
                "Posición del tubo",
                ["Seleccionar", "Arriba", "Abajo", "Derecha", "Izquierda"],
                key="topo_posicion_tubo"
            )
        with fila2_col2:
            posicion_brazos = st.selectbox(
                "Posición de brazos / extremidades",
                [
                    "Seleccionar",
                    "BRAZOS ARRIBA",
                    "BRAZOS ABAJO",
                    "ELEVA BRAZO DERECHO",
                    "ELEVA BRAZO IZQUIERDO",
                    "FLEXIÓN EXTREMIDAD INFERIOR DERECHA",
                    "FLEXIÓN EXTREMIDAD INFERIOR IZQUIERDA"
                ],
                key="topo_posicion_brazos"
            )

        fila3_col1, fila3_col2 = st.columns(2)
        with fila3_col1:
            region = st.selectbox(
                "Región anatómica",
                ["Seleccionar", "Cabeza", "Cuello", "Tórax", "Abdomen", "Pelvis", "Cuerpo completo"],
                key="topo_region"
            )
        with fila3_col2:
            plano = st.selectbox(
                "Plano",
                ["Seleccionar", "AP", "Lateral", "AP y lateral"],
                key="topo_plano"
            )

        fila4_col1, fila4_col2 = st.columns(2)
        with fila4_col1:
            inicio = st.text_input("Inicio topograma", key="topo_inicio")
        with fila4_col2:
            termino = st.text_input("Término topograma", key="topo_termino")

        st.markdown('</div>', unsafe_allow_html=True)

    topograma_completo = all([
        seleccion_completa(entrada_paciente),
        seleccion_completa(posicionamiento),
        seleccion_completa(posicion_tubo),
        seleccion_completa(posicion_brazos),
        seleccion_completa(region),
        seleccion_completa(plano),
        topograma_texto_completo(inicio),
        topograma_texto_completo(termino),
    ])

    with col_der:
        st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-bloque">Imagen de topograma</div>', unsafe_allow_html=True)

        if TOPOGRAMA_IMG.exists():
            st.image(str(TOPOGRAMA_IMG), use_container_width=True)
        else:
            st.info("Guarda la imagen como 'topograma.png' en la misma carpeta del app.py.")

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        if st.button("Siguiente", use_container_width=True, disabled=not topograma_completo, key="btn_sig_topo"):
            ir_a("Adquisición")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# ADQUISICIÓN
# -------------------------
elif seccion == "Adquisición":
    st.header("Adquisición")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True, key="btn_volver_adq"):
            volver_anterior()
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        kvp = st.selectbox("kVp", ["Seleccionar", 80, 100, 120, 140], key="adq_kvp")
        mas = st.number_input("mAs", min_value=1, key="adq_mas")
        pitch = st.number_input("Pitch", min_value=0.1, step=0.1, key="adq_pitch")
        rotacion = st.number_input("Tiempo de rotación (s)", min_value=0.1, step=0.1, key="adq_rotacion")

    with col2:
        colimacion = st.text_input("Colimación", key="adq_colimacion")
        espesor_corte = st.number_input("Espesor de corte (mm)", min_value=0.1, step=0.1, key="adq_espesor_corte")
        longitud = st.number_input("Longitud de barrido (cm)", min_value=1.0, key="adq_longitud")
        modo = st.selectbox("Modo de adquisición", ["Seleccionar", "Helicoidal", "Secuencial"], key="adq_modo")

    adquisicion_completa = all([
        seleccion_completa(kvp),
        texto_completo(colimacion),
        seleccion_completa(modo),
    ])

    if st.button("Siguiente", use_container_width=True, disabled=not adquisicion_completa, key="btn_sig_adq"):
        ir_a("Reconstrucción")
        st.rerun()

# -------------------------
# RECONSTRUCCIÓN
# -------------------------
elif seccion == "Reconstrucción":
    st.header("Reconstrucción")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True, key="btn_volver_recon"):
            volver_anterior()
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        kernel = st.selectbox(
            "Kernel / filtro",
            ["Seleccionar", "Blando", "Estándar", "Óseo", "Pulmonar", "Otro"],
            key="recon_kernel"
        )
        grosor_recon = st.number_input("Grosor de reconstrucción (mm)", min_value=0.1, step=0.1, key="recon_grosor")
        intervalo_recon = st.number_input("Intervalo de reconstrucción (mm)", min_value=0.1, step=0.1, key="recon_intervalo")

    with col2:
        plano_recon = st.multiselect("Planos reconstruidos", ["Axial", "Coronal", "Sagital", "Oblicuo"], key="recon_planos")
        algoritmo = st.selectbox("Algoritmo", ["Seleccionar", "FBP", "Iterativa", "Otro"], key="recon_algoritmo")
        ventana = st.selectbox("Ventana principal", ["Seleccionar", "Partes blandas", "Pulmón", "Ósea", "Otra"], key="recon_ventana")

    reconstruccion_completa = all([
        seleccion_completa(kernel),
        lista_completa(plano_recon),
        seleccion_completa(algoritmo),
        seleccion_completa(ventana),
    ])

    if st.button("Siguiente", use_container_width=True, disabled=not reconstruccion_completa, key="btn_sig_recon"):
        ir_a("Reformación")
        st.rerun()

# -------------------------
# REFORMACIÓN
# -------------------------
elif seccion == "Reformación":
    st.header("Reformación")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True, key="btn_volver_reform"):
            volver_anterior()
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        tipo_reformacion = st.multiselect(
            "Tipo de reformación",
            ["MPR coronal", "MPR sagital", "MIP", "MinIP", "VR", "Curva"],
            key="reform_tipo"
        )
        grosor_mip = st.number_input("Grosor MIP / slab (mm)", min_value=0.1, step=0.1, key="reform_grosor")

    with col2:
        orientacion = st.selectbox("Orientación principal", ["Seleccionar", "Coronal", "Sagital", "Oblicua"], key="reform_orientacion")
        observaciones_reform = st.text_area("Observaciones de reformación", key="reform_observaciones")

    reformacion_completa = all([
        lista_completa(tipo_reformacion),
        seleccion_completa(orientacion),
        texto_completo(observaciones_reform),
    ])

    if st.button("Siguiente", use_container_width=True, disabled=not reformacion_completa, key="btn_sig_reform"):
        ir_a("Jeringa inyectora")
        st.rerun()

# -------------------------
# JERINGA INYECTORA
# -------------------------
elif seccion == "Jeringa inyectora":
    st.header("Jeringa inyectora")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True, key="btn_volver_jeringa"):
            volver_anterior()
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Tipo de contraste", key="jer_tipo_contraste")
        st.number_input("Volumen de contraste (mL)", min_value=0.0, key="jer_volumen_contraste")
        st.number_input("Flujo (mL/s)", min_value=0.1, step=0.1, key="jer_flujo")

    with col2:
        st.number_input("Volumen de flush / suero (mL)", min_value=0.0, key="jer_flush")
        st.number_input("Delay / retardo (s)", min_value=0.0, key="jer_tiempo_delay")
        st.selectbox("Sitio de punción", ["Seleccionar", "Brazo derecho", "Brazo izquierdo", "Otro"], key="jer_sitio_puncion")
