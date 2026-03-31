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

PACIENTE_IMG_PNG = BASE_DIR / "paciente.png"
PACIENTE_IMG_JPG = BASE_DIR / "paciente.jpg"

if PACIENTE_IMG_PNG.exists():
    PACIENTE_IMG = PACIENTE_IMG_PNG
elif PACIENTE_IMG_JPG.exists():
    PACIENTE_IMG = PACIENTE_IMG_JPG
else:
    PACIENTE_IMG = None

# -------------------------
# CONTROL DE ACCESO
# -------------------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "seccion" not in st.session_state:
    st.session_state.seccion = "Portada"


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
        st.image(str(PORTADA_IMG), width="stretch")

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

/* Texto general */
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText {
    color: white !important;
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
    margin-bottom: 0.6rem;
    color: white;
}

/* Imagen */
.bloque-a-practicar img,
.bloque-seccion img {
    border-radius: 14px;
}

/* Edad más pequeña */
[data-testid="stMetricValue"] {
    font-size: 1.35rem !important;
}
[data-testid="stMetricLabel"] {
    color: white !important;
}

/* Selectbox cerrado */
div[data-baseweb="select"] > div {
    background-color: #b8bec7 !important;
    border-radius: 12px !important;
    color: #000000 !important;
}

/* Todo el texto del select cerrado */
div[data-baseweb="select"] div,
div[data-baseweb="select"] span,
div[data-baseweb="select"] input,
div[data-baseweb="select"] svg {
    color: #000000 !important;
    fill: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* Menú desplegable */
div[role="listbox"] {
    background-color: #c7ccd4 !important;
    border: 1px solid #9ca3ad !important;
}

/* Opciones del desplegable */
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

input, textarea {
    color: #1f1f1f !important;
    -webkit-text-fill-color: #1f1f1f !important;
}

/* Calendario */
input[type="date"] {
    color: #1f1f1f !important;
    -webkit-text-fill-color: #1f1f1f !important;
}

/* Caja info */
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
# FUNCIONES
# -------------------------
def ir_a_practicar():
    st.session_state.seccion = "A Practicar"

def volver_menu():
    st.session_state.seccion = "A Practicar"

def ir_a_topograma():
    st.session_state.seccion = "Topograma"

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
            st.image(str(PORTADA_IMG), width="stretch")
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
# PANTALLA PRINCIPAL
# -------------------------
elif seccion == "A Practicar":
    st.title("Simulador de Tomografía Computada")
    st.header("A Practicar")
    st.write("Selecciona una etapa del simulador:")

    col_img, col_menu = st.columns([1.15, 1], vertical_alignment="center")

    with col_img:
        st.markdown('<div class="bloque-a-practicar">', unsafe_allow_html=True)

        if A_PRACTICAR_IMG.exists():
            st.image(str(A_PRACTICAR_IMG), width="stretch")
        else:
            st.info("Guarda la imagen como 'a_practicar.png' en la misma carpeta del app.py.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_menu:
        st.markdown('<div class="bloque-a-practicar">', unsafe_allow_html=True)

        if st.button("Preparación del paciente", use_container_width=True):
            st.session_state.seccion = "Preparación de paciente"
            st.rerun()

        if st.button("Topograma", use_container_width=True):
            st.session_state.seccion = "Topograma"
            st.rerun()

        if st.button("Adquisición", use_container_width=True):
            st.session_state.seccion = "Adquisición"
            st.rerun()

        if st.button("Reconstrucción", use_container_width=True):
            st.session_state.seccion = "Reconstrucción"
            st.rerun()

        if st.button("Reformación", use_container_width=True):
            st.session_state.seccion = "Reformación"
            st.rerun()

        if st.button("Jeringa inyectora", use_container_width=True):
            st.session_state.seccion = "Jeringa inyectora"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.info("Haz clic en una etapa para continuar.")

# -------------------------
# PREPARACIÓN DE PACIENTE
# -------------------------
elif seccion == "Preparación de paciente":
    st.header("Preparación de paciente")

    st.markdown('<div class="boton-volver">', unsafe_allow_html=True)
    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    col_izq, col_centro, col_img = st.columns([1.15, 1.15, 0.75])

    with col_izq:
        st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-bloque">Datos del paciente</div>', unsafe_allow_html=True)

        nombres = st.text_input("Nombres")
        apellidos = st.text_input("Apellidos")

        c1, c2 = st.columns([1.2, 0.8])
        with c1:
            fecha_nac = st.date_input("Fecha de nacimiento", value=date(2000, 1, 1))
        with c2:
            hoy = date.today()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            st.markdown("<br>", unsafe_allow_html=True)
            st.metric("Edad", f"{edad} años")

        examen = st.text_input("Examen")

        c3, c4 = st.columns(2)
        with c3:
            peso = st.selectbox("Peso (kg)", list(range(1, 201)), index=69)
        with c4:
            embarazo = st.selectbox("Embarazo", ["Seleccionar", "SI", "NO", "NO APLICA"], index=0)

        creatinina = st.selectbox("Creatinina", ["Seleccionar", "SI", "NO"], index=0)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_centro:
        st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-bloque">Preparación para contraste</div>', unsafe_allow_html=True)

        medio_contraste_ev = st.selectbox(
            "Medio de contraste EV",
            ["Seleccionar", "SI", "NO", "NO APLICA"],
            index=0
        )

        if medio_contraste_ev != "NO":
            c5, c6 = st.columns(2)
            with c5:
                via_venosa = st.selectbox(
                    "Vía venosa",
                    ["Seleccionar", "24G", "22G", "20G", "18G", "16G", "CVC", "NO APLICA"],
                    index=0
                )
            with c6:
                cantidad_contraste = st.selectbox(
                    "Cantidad contraste",
                    [
                        "Seleccionar", "10 cc", "20 cc", "30 cc", "40 cc", "50 cc", "60 cc", "70 cc", "80 cc",
                        "90 cc", "100 cc", "110 cc", "120 cc", "130 cc", "140 cc", "150 cc",
                        "160 cc", "170 cc", "180 cc", "190 cc", "200 cc"
                    ],
                    index=0
                )

            c7, c8 = st.columns(2)
            with c7:
                metodo_inyeccion = st.selectbox(
                    "Método de inyección",
                    ["Seleccionar", "JERINGA INYECTORA", "JERINGA MANUAL", "NO APLICA"],
                    index=0
                )
            with c8:
                medio_contraste_oral = st.selectbox(
                    "Contraste oral",
                    ["Seleccionar", "NO APLICA", "AGUA", "AIRE", "CONTRASTE POSITIVO"],
                    index=0
                )
        else:
            via_venosa = ""
            cantidad_contraste = ""
            metodo_inyeccion = ""
            medio_contraste_oral = ""

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-bloque">Posicionamiento del paciente</div>', unsafe_allow_html=True)

        c9, c10 = st.columns(2)
        with c9:
            entrada_paciente = st.selectbox(
                "Entrada paciente",
                ["Seleccionar", "CABEZA PRIMERO", "PIES PRIMERO"],
                index=0
            )
        with c10:
            posicionamiento = st.selectbox(
                "Posicionamiento",
                ["Seleccionar", "SUPINO", "PRONO", "LATERAL DERECHO", "LATERAL IZQUIERDO"],
                index=0
            )

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
            index=0
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col_img:
        st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-bloque">Imagen</div>', unsafe_allow_html=True)

        if PACIENTE_IMG is not None and PACIENTE_IMG.exists():
            st.image(str(PACIENTE_IMG), width=260)
        else:
            st.info("Guarda la imagen como 'paciente.png' o 'paciente.jpg' en la misma carpeta del app.py.")

        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("Resumen")

    st.markdown('<div class="bloque-resumen">', unsafe_allow_html=True)
    st.write(f"**Paciente:** {nombres} {apellidos}")
    st.write(f"**Edad:** {edad} años")
    st.write(f"**Examen:** {examen}")
    st.write(f"**Peso:** {peso} kg")
    st.write(f"**Embarazo:** {embarazo}")
    st.write(f"**Creatinina:** {creatinina}")
    st.write(f"**Medio de contraste EV:** {medio_contraste_ev}")

    if medio_contraste_ev != "NO":
        st.write(f"**Vía venosa:** {via_venosa}")
        st.write(f"**Cantidad de contraste:** {cantidad_contraste}")
        st.write(f"**Método de inyección:** {metodo_inyeccion}")
        st.write(f"**Medio de contraste oral:** {medio_contraste_oral}")

    st.write(f"**Entrada del paciente:** {entrada_paciente}")
    st.write(f"**Posicionamiento:** {posicionamiento}")
    st.write(f"**Posición de brazos / extremidades:** {posicion_brazos}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    col_sig1, col_sig2, col_sig3 = st.columns([1.5, 2, 1.5])

    with col_sig2:
        if st.button("Siguiente", use_container_width=True):
            ir_a_topograma()
            st.rerun()

# -------------------------
# JERINGA INYECTORA
# -------------------------
elif seccion == "Jeringa inyectora":
    st.header("Jeringa inyectora")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        tipo_contraste = st.text_input("Tipo de contraste", value="Yodado")
        volumen_contraste = st.number_input("Volumen de contraste (mL)", min_value=0.0, value=80.0)
        flujo = st.number_input("Flujo (mL/s)", min_value=0.1, value=3.5, step=0.1)

    with col2:
        flush = st.number_input("Volumen de flush / suero (mL)", min_value=0.0, value=30.0)
        tiempo_delay = st.number_input("Delay / retardo (s)", min_value=0.0, value=25.0)
        sitio_puncion = st.selectbox("Sitio de punción", ["Seleccionar", "Brazo derecho", "Brazo izquierdo", "Otro"], index=0)

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
    st.header("Topograma")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        region = st.selectbox("Región anatómica", ["Seleccionar", "Cabeza", "Cuello", "Tórax", "Abdomen", "Pelvis", "Cuerpo completo"], index=0)
        proyeccion = st.selectbox("Plano", ["Seleccionar", "AP", "Lateral"], index=0)

    with col2:
        inicio = st.text_input("Inicio topograma", value="Desde")
        termino = st.text_input("Término topograma", value="Hasta")
        observaciones_topo = st.text_area("Observaciones")

    st.subheader("Resumen")
    st.write(f"Región: {region}")
    st.write(f"Plano: {proyeccion}")
    st.write(f"Inicio: {inicio}")
    st.write(f"Término: {termino}")
    st.write(f"Observaciones: {observaciones_topo}")

# -------------------------
# ADQUISICIÓN
# -------------------------
elif seccion == "Adquisición":
    st.header("Adquisición")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        kvp = st.selectbox("kVp", ["Seleccionar", 80, 100, 120, 140], index=0)
        mas = st.number_input("mAs", min_value=1, value=100)
        pitch = st.number_input("Pitch", min_value=0.1, value=1.0, step=0.1)
        rotacion = st.number_input("Tiempo de rotación (s)", min_value=0.1, value=0.5, step=0.1)

    with col2:
        colimacion = st.text_input("Colimación", value="64 x 0.625 mm")
        espesor_corte = st.number_input("Espesor de corte (mm)", min_value=0.1, value=1.0, step=0.1)
        longitud = st.number_input("Longitud de barrido (cm)", min_value=1.0, value=30.0)
        modo = st.selectbox("Modo de adquisición", ["Seleccionar", "Helicoidal", "Secuencial"], index=0)

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
    st.header("Reconstrucción")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        kernel = st.selectbox("Kernel / filtro", ["Seleccionar", "Blando", "Estándar", "Óseo", "Pulmonar", "Otro"], index=0)
        grosor_recon = st.number_input("Grosor de reconstrucción (mm)", min_value=0.1, value=1.0, step=0.1)
        intervalo_recon = st.number_input("Intervalo de reconstrucción (mm)", min_value=0.1, value=0.5, step=0.1)

    with col2:
        plano_recon = st.multiselect("Planos reconstruidos", ["Axial", "Coronal", "Sagital", "Oblicuo"], default=[])
        algoritmo = st.selectbox("Algoritmo", ["Seleccionar", "FBP", "Iterativa", "Otro"], index=0)
        ventana = st.selectbox("Ventana principal", ["Seleccionar", "Partes blandas", "Pulmón", "Ósea", "Otra"], index=0)

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
    st.header("Reformación")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        tipo_reformacion = st.multiselect("Tipo de reformación", ["MPR coronal", "MPR sagital", "MIP", "MinIP", "VR", "Curva"], default=[])
        grosor_mip = st.number_input("Grosor MIP / slab (mm)", min_value=0.1, value=10.0, step=0.1)

    with col2:
        orientacion = st.selectbox("Orientación principal", ["Seleccionar", "Coronal", "Sagital", "Oblicua"], index=0)
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
    st.header("Medida paciente")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        diametro_ap = st.number_input("Diámetro AP (cm)", min_value=0.0, value=25.0)
        diametro_lat = st.number_input("Diámetro lateral (cm)", min_value=0.0, value=35.0)

    with col2:
        edad_medida = st.number_input("Edad", min_value=0, value=30)
        sexo = st.selectbox("Sexo", ["Seleccionar", "Femenino", "Masculino", "Otro"], index=0)

    if diametro_ap > 0 and diametro_lat > 0:
        diametro_efectivo = (diametro_ap * diametro_lat) ** 0.5
    else:
        diametro_efectivo = 0.0

    st.metric("Diámetro efectivo (cm)", f"{diametro_efectivo:.2f}")

    st.subheader("Resumen")
    st.write(f"Edad: {edad_medida}")
    st.write(f"Sexo: {sexo}")

# -------------------------
# CÁLCULOS
# -------------------------
elif seccion == "Cálculos":
    st.header("Cálculos")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        ctdi_vol = st.number_input("CTDIvol (mGy)", min_value=0.0, value=10.0)
        longitud_scan = st.number_input("Longitud de escaneo (cm)", min_value=0.0, value=30.0)

    with col2:
        factor_ssde = st.number_input("Factor SSDE", min_value=0.1, value=1.0, step=0.1)
        usar_ssde = st.selectbox("¿Calcular SSDE?", ["Seleccionar", "Sí", "No"], index=0)

    dlp = ctdi_vol * longitud_scan
    st.metric("DLP (mGy·cm)", f"{dlp:.2f}")

    if usar_ssde == "Sí":
        ssde = ctdi_vol * factor_ssde
        st.metric("SSDE (mGy)", f"{ssde:.2f}")
