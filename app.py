import streamlit as st
from pathlib import Path
from datetime import date
import hmac
import openpyxl
import base64
import streamlit.components.v1 as components
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
    "topo_region_anatomica": "Seleccionar",
    "topo_region": "Seleccionar",
    "topo_inicio": "", 
    "topo_termino": "",
    "topo_rx_iniciado": False,

    # Topograma 2
    "mostrar_topo2": False,
    "topo2_entrada_paciente": "Seleccionar",
    "topo2_posicionamiento": "Seleccionar",
    "topo2_posicion_tubo": "Seleccionar",
    "topo2_posicion_brazos": "Seleccionar",
    "topo2_region_anatomica": "Seleccionar",
    "topo2_region": "Seleccionar",
    "topo2_inicio": "",
    "topo2_termino": "",
    "topo2_rx_iniciado": False,

    # Adquisición
    "adq_fase_adquisicion": "Seleccionar",
    "adq_instruccion_voz": "Seleccionar",
    "adq_delay": "Seleccionar",
    "adq_tipo_exploracion": "Seleccionar",
    "adq_espesor": "Seleccionar",
    "adq_matriz_detectores": "Seleccionar",
    "adq_colimacion": "",
    "adq_inicio_adquisicion": "",
    "adq_fin_adquisicion": "",
    "adq_giro_tubo": "Seleccionar",
    "adq_modulacion_corriente": "Seleccionar",
    "adq_kv_referencia": "Seleccionar",
    "adq_mas_referencia": "Seleccionar",
    "adq_kv_manual": 120,
    "adq_mas_manual": 100,
    "adq_pitch": "Seleccionar",
    "adq_sfov": "Seleccionar",
    "adq_topo1_limite_superior": 15,
    "adq_topo1_limite_inferior": 85,
    "adq_topo2_limite_superior": 15,
    "adq_topo2_limite_inferior": 85,

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

    if key == "topo_region_anatomica":
        st.session_state["topo_region"] = "Seleccionar"
        st.session_state["_topo_region"] = "Seleccionar"
    if key == "topo2_region_anatomica":
        st.session_state["topo2_region"] = "Seleccionar"
        st.session_state["_topo2_region"] = "Seleccionar"

    if key.startswith("topo_"):
        st.session_state["topo_rx_iniciado"] = False
    if key.startswith("topo2_"):
        st.session_state["topo2_rx_iniciado"] = False


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



def ajustar_imagen_a_lienzo_uniforme(imagen, tamano_lienzo=(420, 420), color_fondo=(32, 32, 32)):
    if imagen is None:
        return None

    try:
        imagen = imagen.convert("RGB")
        ancho_lienzo, alto_lienzo = tamano_lienzo
        ancho_img, alto_img = imagen.size

        escala = min(ancho_lienzo / ancho_img, alto_lienzo / alto_img)
        nuevo_ancho = max(1, int(ancho_img * escala))
        nuevo_alto = max(1, int(alto_img * escala))

        imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto))
        lienzo = Image.new("RGB", tamano_lienzo, color_fondo)

        offset_x = (ancho_lienzo - nuevo_ancho) // 2
        offset_y = (alto_lienzo - nuevo_alto) // 2
        lienzo.paste(imagen_redimensionada, (offset_x, offset_y))
        return lienzo
    except Exception:
        return imagen


def crear_topograma_con_limites(ruta_imagen, limite_superior_pct, limite_inferior_pct):
    if ruta_imagen is None:
        return None
    ruta = Path(ruta_imagen)
    if not ruta.exists():
        return None

    try:
        imagen = Image.open(ruta).convert("RGB")
        draw = ImageDraw.Draw(imagen)
        ancho, alto = imagen.size

        y_superior = int((limite_superior_pct / 100) * alto)
        y_inferior = int((limite_inferior_pct / 100) * alto)

        grosor = max(3, alto // 120)
        margen_texto = max(8, ancho // 40)

        draw.line([(0, y_superior), (ancho, y_superior)], fill=(0, 255, 255), width=grosor)
        draw.line([(0, y_inferior), (ancho, y_inferior)], fill=(255, 180, 0), width=grosor)

        draw.text((margen_texto, max(5, y_superior - 22)), "Inicio", fill=(0, 255, 255))
        draw.text((margen_texto, max(5, y_inferior - 22)), "Fin", fill=(255, 180, 0))

        return ajustar_imagen_a_lienzo_uniforme(imagen)
    except Exception:
        return None


def render_roi_interactiva_html(uploaded_file, key_suffix="roi"):
    if uploaded_file is None:
        return

    try:
        image_bytes = uploaded_file.getvalue()
        mime_type = getattr(uploaded_file, "type", None) or "image/png"
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        data_uri = f"data:{mime_type};base64,{image_b64}"

        html_code = f"""
        <div style="background:#4a4a4a;border:1px solid #7a7a7a;border-radius:12px;padding:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:10px;">
                <div style="color:white;font-weight:700;">ROI INTERACTIVA</div>
                <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
                    <button id="add-roi-{key_suffix}" style="background:#b8bec7;color:#1f1f1f;border:none;border-radius:8px;padding:8px 12px;font-weight:600;cursor:pointer;">Agregar ROI</button>
                    <button id="clear-roi-{key_suffix}" style="background:#b8bec7;color:#1f1f1f;border:none;border-radius:8px;padding:8px 12px;font-weight:600;cursor:pointer;">Quitar ROI</button>
                    <label style="color:white;font-size:14px;">Tamaño ROI</label>
                    <input id="radius-{key_suffix}" type="range" min="2" max="160" value="20" step="1" />
                </div>
            </div>
            <div style="color:#d8d8d8;font-size:13px;margin-bottom:10px;">Arrastra el círculo rojo con el mouse para mover la ROI libremente.</div>
            <canvas id="canvas-{key_suffix}" style="max-width:100%;width:100%;border-radius:10px;background:#222;cursor:grab;touch-action:none;display:block;"></canvas>
        </div>

        <script>
        (() => {{
            const canvas = document.getElementById('canvas-{key_suffix}');
            const ctx = canvas.getContext('2d');
            const addBtn = document.getElementById('add-roi-{key_suffix}');
            const clearBtn = document.getElementById('clear-roi-{key_suffix}');
            const radiusInput = document.getElementById('radius-{key_suffix}');
            const img = new Image();

            let hasROI = false;
            let dragging = false;
            let dragOffsetX = 0;
            let dragOffsetY = 0;
            let cssWidth = 0;
            let cssHeight = 0;
            let roi = {{ x: 0, y: 0, r: 20 }};

            function getCssSize() {{
                const maxWidth = 760;
                const width = Math.min(canvas.parentElement.clientWidth || 760, maxWidth);
                const height = width * (img.height / img.width);
                return {{ width, height }};
            }}

            function resizeCanvas() {{
                if (!img.width) return;
                const dpr = window.devicePixelRatio || 1;
                const size = getCssSize();
                cssWidth = size.width;
                cssHeight = size.height;

                canvas.style.width = cssWidth + 'px';
                canvas.style.height = cssHeight + 'px';
                canvas.width = Math.round(cssWidth * dpr);
                canvas.height = Math.round(cssHeight * dpr);
                ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
                draw();
            }}

            function draw() {{
                if (!img.width) return;
                ctx.clearRect(0, 0, cssWidth, cssHeight);
                ctx.drawImage(img, 0, 0, cssWidth, cssHeight);
                if (hasROI) {{
                    ctx.beginPath();
                    ctx.arc(roi.x, roi.y, roi.r, 0, Math.PI * 2);
                    ctx.strokeStyle = 'red';
                    ctx.lineWidth = 1.4;
                    ctx.stroke();
                }}
            }}

            function getPointerPos(event) {{
                const rect = canvas.getBoundingClientRect();
                const touch = event.touches && event.touches[0]
                    ? event.touches[0]
                    : (event.changedTouches && event.changedTouches[0] ? event.changedTouches[0] : null);

                const clientX = touch ? touch.clientX : (typeof event.clientX === 'number' ? event.clientX : rect.left);
                const clientY = touch ? touch.clientY : (typeof event.clientY === 'number' ? event.clientY : rect.top);

                return {{
                    x: clientX - rect.left,
                    y: clientY - rect.top
                }};
            }}

            function clampROI() {{
                roi.x = Math.max(roi.r, Math.min(cssWidth - roi.r, roi.x));
                roi.y = Math.max(roi.r, Math.min(cssHeight - roi.r, roi.y));
            }}

            function pointHitsROI(pos) {{
                const dx = pos.x - roi.x;
                const dy = pos.y - roi.y;
                return Math.sqrt(dx * dx + dy * dy) <= roi.r + 10;
            }}

            addBtn.addEventListener('click', (event) => {{
                event.preventDefault();
                hasROI = true;
                roi.r = parseInt(radiusInput.value, 10);
                roi.x = cssWidth / 2;
                roi.y = cssHeight / 2;
                clampROI();
                draw();
            }});

            clearBtn.addEventListener('click', (event) => {{
                event.preventDefault();
                hasROI = false;
                dragging = false;
                canvas.style.cursor = 'grab';
                draw();
            }});

            radiusInput.addEventListener('input', () => {{
                roi.r = parseInt(radiusInput.value, 10);
                clampROI();
                draw();
            }});

            function startDragging(event) {{
                if (!hasROI) return;
                const pos = getPointerPos(event);
                if (pointHitsROI(pos)) {{
                    dragging = true;
                    dragOffsetX = pos.x - roi.x;
                    dragOffsetY = pos.y - roi.y;
                    canvas.style.cursor = 'grabbing';
                    event.preventDefault();
                }}
            }}

            function moveDragging(event) {{
                if (!dragging || !hasROI) return;
                const pos = getPointerPos(event);
                roi.x = pos.x - dragOffsetX;
                roi.y = pos.y - dragOffsetY;
                clampROI();
                draw();
                event.preventDefault();
            }}

            function stopDragging() {{
                dragging = false;
                canvas.style.cursor = hasROI ? 'grab' : 'default';
            }}

            canvas.addEventListener('mousedown', startDragging);
            window.addEventListener('mousemove', moveDragging);
            window.addEventListener('mouseup', stopDragging);

            canvas.addEventListener('touchstart', startDragging, {{ passive: false }});
            window.addEventListener('touchmove', moveDragging, {{ passive: false }});
            window.addEventListener('touchend', stopDragging);
            window.addEventListener('touchcancel', stopDragging);

            canvas.addEventListener('click', (event) => {{
                if (!hasROI || dragging) return;
                const pos = getPointerPos(event);
                roi.x = pos.x;
                roi.y = pos.y;
                clampROI();
                draw();
            }});

            img.onload = () => {{
                resizeCanvas();
                roi.x = cssWidth / 2;
                roi.y = cssHeight / 2;
                draw();
                window.addEventListener('resize', resizeCanvas);
            }};

            img.src = '{data_uri}';
        }})();
        </script>
        """

        components.html(html_code, height=700)
    except Exception as e:
        st.warning(f"No fue posible cargar la ROI interactiva: {{e}}")

def render_linea_corte_bolus_interactiva_html(imagen_fuente, key_suffix="bolus_line"):
    try:
        if isinstance(imagen_fuente, Image.Image):
            from io import BytesIO
            buffer = BytesIO()
            imagen_fuente.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            mime = "image/png"
        else:
            ruta = Path(imagen_fuente)
            image_bytes = ruta.read_bytes()
            sufijo = ruta.suffix.lower()
            mime = "image/png" if sufijo == ".png" else "image/jpeg"

        encoded = base64.b64encode(image_bytes).decode("utf-8")
        data_uri = f"data:{mime};base64,{encoded}"

        html_code = f"""
        <div style="background:#3f3f3f;padding:14px 14px 10px 14px;border-radius:12px;border:1px solid #727272;">
            <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:10px;">
                <button id="add-line-{key_suffix}" style="padding:8px 14px;border:none;border-radius:8px;background:#c8cdd4;color:#111;font-weight:700;cursor:pointer;">Agregar corte de bolus</button>
                <button id="clear-line-{key_suffix}" style="padding:8px 14px;border:none;border-radius:8px;background:#8e949c;color:white;font-weight:700;cursor:pointer;">Borrar corte</button>
            </div>
            <div style="color:#d8d8d8;font-size:13px;margin-bottom:10px;">Arrastra la línea roja verticalmente para ubicar el corte de bolus.</div>
            <canvas id="canvas-line-{key_suffix}" style="max-width:100%;width:100%;border-radius:10px;background:#222;cursor:ns-resize;"></canvas>
        </div>

        <script>
        (() => {{
            const canvas = document.getElementById('canvas-line-{key_suffix}');
            const ctx = canvas.getContext('2d');
            const addBtn = document.getElementById('add-line-{key_suffix}');
            const clearBtn = document.getElementById('clear-line-{key_suffix}');
            const img = new Image();

            let hasLine = false;
            let dragging = false;
            let scale = 1;
            let lineY = 200;

            function resizeCanvas() {{
                const maxWidth = 760;
                const containerWidth = Math.min(canvas.parentElement.clientWidth, maxWidth);
                scale = containerWidth / img.width;
                canvas.width = containerWidth;
                canvas.height = img.height * scale;
                draw();
            }}

            function drawLabel(yPx) {{
                const text = 'Corte de bolus';
                ctx.font = 'bold 16px Arial';
                const textWidth = ctx.measureText(text).width;
                const boxX = Math.max(10, canvas.width - textWidth - 24);
                const boxY = Math.max(8, yPx - 30);
                ctx.fillStyle = 'rgba(255, 0, 0, 0.88)';
                ctx.fillRect(boxX, boxY, textWidth + 14, 24);
                ctx.fillStyle = 'white';
                ctx.fillText(text, boxX + 7, boxY + 17);
            }}

            function draw() {{
                if (!img.width) return;
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                if (hasLine) {{
                    const yPx = lineY * scale;
                    ctx.beginPath();
                    ctx.moveTo(0, yPx);
                    ctx.lineTo(canvas.width, yPx);
                    ctx.strokeStyle = 'red';
                    ctx.lineWidth = 2;
                    ctx.stroke();
                    drawLabel(yPx);
                }}
            }}

            function getPointerY(event) {{
                const rect = canvas.getBoundingClientRect();
                const touch = event.touches && event.touches[0]
                    ? event.touches[0]
                    : event.changedTouches && event.changedTouches[0]
                        ? event.changedTouches[0]
                        : null;
                const clientY = touch ? touch.clientY : (typeof event.clientY === 'number' ? event.clientY : rect.top);
                return (clientY - rect.top) / scale;
            }}

            function clampLine(y) {{
                return Math.max(0, Math.min(img.height, y));
            }}

            function startDragging(event) {{
                if (!hasLine) return;
                const y = getPointerY(event);
                if (Math.abs(y - lineY) <= 28) {{
                    dragging = true;
                    event.preventDefault();
                }}
            }}

            function moveDragging(event) {{
                if (!dragging || !hasLine) return;
                const y = getPointerY(event);
                lineY = clampLine(y);
                draw();
                event.preventDefault();
            }}

            function stopDragging() {{
                dragging = false;
            }}

            addBtn.addEventListener('click', () => {{
                hasLine = true;
                lineY = img.height / 2;
                draw();
            }});

            clearBtn.addEventListener('click', () => {{
                hasLine = false;
                dragging = false;
                draw();
            }});

            canvas.addEventListener('mousedown', startDragging);
            window.addEventListener('mousemove', moveDragging);
            window.addEventListener('mouseup', stopDragging);

            canvas.addEventListener('touchstart', startDragging, {{ passive: false }});
            window.addEventListener('touchmove', moveDragging, {{ passive: false }});
            window.addEventListener('touchend', stopDragging);
            window.addEventListener('touchcancel', stopDragging);

            canvas.addEventListener('click', (event) => {{
                if (!hasLine || dragging) return;
                lineY = clampLine(getPointerY(event));
                draw();
            }});

            img.onload = () => {{
                lineY = img.height / 2;
                resizeCanvas();
                window.addEventListener('resize', resizeCanvas);
            }};

            img.src = '{data_uri}';
        }})();
        </script>
        """

        components.html(html_code, height=560)
    except Exception as e:
        st.warning(f"No fue posible cargar la línea interactiva del corte de bolus: {e}")
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
        mostrar_imagen_actualizada(PORTADA_IMG, use_container_width=True)

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
# MAPEO RX TOPOGRAMA SEGÚN LISTADO VÁLIDO ENVIADO
# -------------------------
REGIONES_ANATOMICAS_TOPO = [
    "Seleccionar",
    "cabeza",
    "cuello",
    "torax",
    "abdomen",
    "pelvis",
    "columnas",
    "extremidad superior",
    "extremidad inferior",
    "angiotac",
]

MAPA_REGION_ANATOMICA_A_PROTOCOLOS = {
    "cabeza": ["Seleccionar", "cerebro", "cavidades perinasales", "maxilofacial", "orbitas", "oidos"],
    "cuello": ["Seleccionar", "cuello"],
    "torax": ["Seleccionar", "torax", "torax abdomen y pelvis"],
    "abdomen": ["Seleccionar", "abdomen", "abdomen y pelvis", "pielotac"],
    "pelvis": ["Seleccionar", "pelvis"],
    "columnas": ["Seleccionar", "columna cervical", "columna dorsal", "columna lumbar"],
    "extremidad superior": ["Seleccionar", "hombro", "brazo", "codo", "antebrazo", "muñeca", "mano"],
    "extremidad inferior": ["Seleccionar", "cadera", "rodilla", "pierna", "tobillo", "pie"],
    "angiotac": [
        "Seleccionar",
        "angiotac extremidad superior derecha",
        "angiotac extremidad superior izquierda",
        "angiotac cerebro",
        "angiotac cuello",
        "angiotac cerebro cuello",
        "angiotac torax",
        "angiotac abdomen",
        "angiotac abdomen y pelvis",
        "angiotac torax abdomen y pelvis",
        "angiotac extremidad inferior",
    ],
}

TOPORAMA_REGLAS_TSV = """entrada del paciente	posicionamiento	posicion del tubo	protolocolo	nombre exacto de la imagen
				
cabeza primero	supino	arriba	cerebro 	cabeza frontal
cabeza primero	supino	abajo	cerebro 	cabeza frontal
cabeza primero	supino	derecha 	cerebro 	cabeza lateral
cabeza primero	supino	izquierda	cerebro 	cabeza lateral
cabeza primero	supino	arriba	cavidades perinasales	cabeza frontal
cabeza primero	supino	abajo	cavidades perinasales	cabeza frontal
cabeza primero	supino	derecha 	cavidades perinasales	cabeza lateral
cabeza primero	supino	izquierda	cavidades perinasales	cabeza lateral
cabeza primero	supino	arriba	maxilofacial	cabeza frontal
cabeza primero	supino	abajo	maxilofacial	cabeza frontal
cabeza primero	supino	derecha 	maxilofacial	cabeza lateral
cabeza primero	supino	izquierda	maxilofacial	cabeza lateral
cabeza primero	supino	arriba	orbitas	cabeza frontal
cabeza primero	supino	abajo	orbitas	cabeza frontal
cabeza primero	supino	derecha 	orbitas	cabeza lateral
cabeza primero	supino	izquierda	orbitas	cabeza lateral
cabeza primero	supino	arriba	oidos	cabeza frontal
cabeza primero	supino	abajo	oidos	cabeza frontal
cabeza primero	supino	derecha 	oidos	cabeza lateral
cabeza primero	supino	izquierda	oidos	cabeza lateral
				
cabeza primero	prono	arriba	cerebro	cabeza frontal
cabeza primero	prono	abajo	cerebro	cabeza frontal
cabeza primero	prono	derecha 	cerebro	cabeza lateral
cabeza primero	prono	izquierda	cerebro	cabeza lateral
cabeza primero	prono	arriba	cavidades perinasales	cabeza frontal
cabeza primero	prono	abajo	cavidades perinasales	cabeza frontal
cabeza primero	prono	derecha 	cavidades perinasales	cabeza lateral
cabeza primero	prono	izquierda	cavidades perinasales	cabeza lateral
cabeza primero	prono	arriba	maxilofacial	cabeza frontal
cabeza primero	prono	abajo	maxilofacial	cabeza frontal
cabeza primero	prono	derecha 	maxilofacial	cabeza lateral
cabeza primero	prono	izquierda	maxilofacial	cabeza lateral
cabeza primero	prono	arriba	orbitas	cabeza frontal
cabeza primero	prono	abajo	orbitas	cabeza frontal
cabeza primero	prono	derecha 	orbitas	cabeza lateral
cabeza primero	prono	izquierda	orbitas	cabeza lateral
cabeza primero	prono	arriba	oidos	cabeza frontal
cabeza primero	prono	abajo	oidos	cabeza frontal
cabeza primero	prono	derecha 	oidos	cabeza lateral
cabeza primero	prono	izquierda	oidos	cabeza lateral
				
cabeza primero	lateral derecho	arriba	cerebro	cabeza lateral
cabeza primero	lateral derecho	abajo	cerebro	cabeza lateral
cabeza primero	lateral derecho	derecha 	cerebro	cabeza frontal
cabeza primero	lateral derecho	izquierda	cerebro	cabeza frontal
cabeza primero	lateral derecho	arriba	cavidades perinasales	cabeza lateral
cabeza primero	lateral derecho	abajo	cavidades perinasales	cabeza lateral
cabeza primero	lateral derecho	derecha 	cavidades perinasales	cabeza frontal
cabeza primero	lateral derecho	izquierda	cavidades perinasales	cabeza frontal
cabeza primero	lateral derecho	arriba	maxilofacial	cabeza lateral
cabeza primero	lateral derecho	abajo	maxilofacial	cabeza lateral
cabeza primero	lateral derecho	derecha 	maxilofacial	cabeza frontal
cabeza primero	lateral derecho	izquierda	maxilofacial	cabeza frontal
cabeza primero	lateral derecho	arriba	orbitas	cabeza lateral
cabeza primero	lateral derecho	abajo	orbitas	cabeza lateral
cabeza primero	lateral derecho	derecha 	orbitas	cabeza frontal
cabeza primero	lateral derecho	izquierda	orbitas	cabeza frontal
cabeza primero	lateral derecho	arriba	oidos	cabeza lateral
cabeza primero	lateral derecho	abajo	oidos	cabeza lateral
cabeza primero	lateral derecho	derecha 	oidos	cabeza frontal
cabeza primero	lateral derecho	izquierda	oidos	cabeza frontal
				
cabeza primero	lateral izquerdo	arriba	cerebro	cabeza lateral
cabeza primero	lateral izquerdo	abajo	cerebro	cabeza lateral
cabeza primero	lateral izquerdo	derecha 	cerebro	cabeza frontal
cabeza primero	lateral izquerdo	izquierda	cerebro	cabeza frontal
cabeza primero	lateral izquerdo	arriba	cavidades perinasales	cabeza lateral
cabeza primero	lateral izquerdo	abajo	cavidades perinasales	cabeza lateral
cabeza primero	lateral izquerdo	derecha 	cavidades perinasales	cabeza frontal
cabeza primero	lateral izquerdo	izquierda	cavidades perinasales	cabeza frontal
cabeza primero	lateral izquerdo	arriba	maxilofacial	cabeza lateral
cabeza primero	lateral izquerdo	abajo	maxilofacial	cabeza lateral
cabeza primero	lateral izquerdo	derecha 	maxilofacial	cabeza frontal
cabeza primero	lateral izquerdo	izquierda	maxilofacial	cabeza frontal
cabeza primero	lateral izquerdo	arriba	orbitas	cabeza lateral
cabeza primero	lateral izquerdo	abajo	orbitas	cabeza lateral
cabeza primero	lateral izquerdo	derecha 	orbitas	cabeza frontal
cabeza primero	lateral izquerdo	izquierda	orbitas	cabeza frontal
cabeza primero	lateral izquerdo	arriba	oidos	cabeza lateral
cabeza primero	lateral izquerdo	abajo	oidos	cabeza lateral
cabeza primero	lateral izquerdo	derecha 	oidos	cabeza frontal
cabeza primero	lateral izquerdo	izquierda	oidos	cabeza frontal
				
cabeza primero	supino	arriba	cuello	cuello frontal
cabeza primero	supino	abajo	cuello	cuello frontal
cabeza primero	supino	derecha 	cuello	cuello lateral
cabeza primero	supino	izquierda	cuello	cuello lateral
cabeza primero	prono	arriba	cuello	cuello frontal
cabeza primero	prono	abajo	cuello	cuello frontal
cabeza primero	prono	derecha 	cuello	cuello lateral
cabeza primero	prono	izquierda	cuello	cuello lateral
cabeza primero	lateral derecho 	arriba	cuello	cuello lateral
cabeza primero	lateral derecho 	abajo	cuello	cuello lateral
cabeza primero	lateral derecho 	derecha 	cuello	cuello frontal
cabeza primero	lateral derecho 	izquierda	cuello	cuello frontal
cabeza primero	lateral izquierdo 	arriba	cuello	cuello lateral
cabeza primero	lateral izquierdo 	abajo	cuello	cuello lateral
cabeza primero	lateral izquierdo 	derecha 	cuello	cuello frontal
cabeza primero	lateral izquierdo 	izquierda	cuello	cuello frontal
				
				
cabeza primero	supino	arriba	columna cervical	cuello frontal
cabeza primero	supino	abajo	columna cervical	cuello frontal
cabeza primero	supino	derecha 	columna cervical	cuello lateral
cabeza primero	supino	izquierda	columna cervical	cuello lateral
cabeza primero	prono	arriba	columna cervical	cuello frontal
cabeza primero	prono	abajo	columna cervical	cuello frontal
cabeza primero	prono	derecha 	columna cervical	cuello lateral
cabeza primero	prono	izquierda	columna cervical	cuello lateral
cabeza primero	lateral derecho 	arriba	columna cervical	cuello lateral
cabeza primero	lateral derecho 	abajo	columna cervical	cuello lateral
cabeza primero	lateral derecho 	derecha 	columna cervical	cuello frontal
cabeza primero	lateral derecho 	izquierda	columna cervical	cuello frontal
cabeza primero	lateral izquierdo 	arriba	columna cervical	cuello lateral
cabeza primero	lateral izquierdo 	abajo	columna cervical	cuello lateral
cabeza primero	lateral izquierdo 	derecha 	columna cervical	cuello frontal
cabeza primero	lateral izquierdo 	izquierda	columna cervical	cuello frontal
				
cabeza primero	supino	arriba	torax	torax frontal
cabeza primero	supino	abajo	torax	torax frontal
cabeza primero	supino	derecha 	torax	torax lateral
cabeza primero	supino	izquierda	torax	torax lateral
cabeza primero	prono	arriba	torax	torax frontal
cabeza primero	prono	abajo	torax	torax frontal
cabeza primero	prono	derecha 	torax	torax lateral
cabeza primero	prono	izquierda	torax	torax lateral
cabeza primero	lateral derecho 	arriba	torax	torax lateral
cabeza primero	lateral derecho 	abajo	torax	torax lateral
cabeza primero	lateral derecho 	derecha 	torax	torax frontal
cabeza primero	lateral derecho 	izquierda	torax	torax frontal
cabeza primero	lateral izquierdo 	arriba	torax	torax lateral
cabeza primero	lateral izquierdo 	abajo	torax	torax lateral
cabeza primero	lateral izquierdo 	derecha 	torax	torax frontal
cabeza primero	lateral izquierdo 	izquierda	torax	torax frontal
				
pies primero	supino	arriba	torax	torax frontal
pies primero	supino	abajo	torax	torax frontal
pies primero	supino	derecha 	torax	torax lateral
pies primero	supino	izquierda	torax	torax lateral
pies primero	prono	arriba	torax	torax frontal
pies primero	prono	abajo	torax	torax frontal
pies primero	prono	derecha 	torax	torax lateral
pies primero	prono	izquierda	torax	torax lateral
pies primero	lateral derecho 	arriba	torax	torax lateral
pies primero	lateral derecho 	abajo	torax	torax lateral
pies primero	lateral derecho 	derecha 	torax	torax frontal
pies primero	lateral derecho 	izquierda	torax	torax frontal
pies primero	lateral izquierdo 	arriba	torax	torax lateral
pies primero	lateral izquierdo 	abajo	torax	torax lateral
pies primero	lateral izquierdo 	derecha 	torax	torax frontal
pies primero	lateral izquierdo 	izquierda	torax	torax frontal
				
cabeza primero	supino	arriba	abdomen	abdomen frontal
cabeza primero	supino	abajo	abdomen	abdomen frontal
cabeza primero	supino	derecha 	abdomen	abdomen lateral
cabeza primero	supino	izquierda	abdomen	abdomen lateral
cabeza primero	prono	arriba	abdomen	abdomen frontal
cabeza primero	prono	abajo	abdomen	abdomen frontal
cabeza primero	prono	derecha 	abdomen	abdomen ateral
cabeza primero	prono	izquierda	abdomen	abdomen lateral
cabeza primero	lateral derecho 	arriba	abdomen	abdomen lateral
cabeza primero	lateral derecho 	abajo	abdomen	abdomen lateral
cabeza primero	lateral derecho 	derecha 	abdomen	abdomen frontal
cabeza primero	lateral derecho 	izquierda	abdomen	abdomen frontal
cabeza primero	lateral izquierdo 	arriba	abdomen	abdomen lateral
cabeza primero	lateral izquierdo 	abajo	abdomen	abdomen lateral
cabeza primero	lateral izquierdo 	derecha 	abdomen	abdomen frontal
cabeza primero	lateral izquierdo 	izquierda	abdomen	abdomen frontal
				
pies primero	supino	arriba	abdomen	abdomen frontal
pies primero	supino	abajo	abdomen	abdomen frontal
pies primero	supino	derecha 	abdomen	abdomen lateral
pies primero	supino	izquierda	abdomen	abdomen lateral
pies primero	prono	arriba	abdomen	abdomen frontal
pies primero	prono	abajo	abdomen	abdomen  frontal
pies primero	prono	derecha 	abdomen	abdomen lateral
pies primero	prono	izquierda	abdomen	abdomen ateral
pies primero	lateral derecho 	arriba	abdomen	abdomen ateral
pies primero	lateral derecho 	abajo	abdomen	abdomen lateral
pies primero	lateral derecho 	derecha 	abdomen	abdomen  frontal
pies primero	lateral derecho 	izquierda	abdomen	abdomen frontal
pies primero	lateral izquierdo 	arriba	abdomen	abdomen lateral
pies primero	lateral izquierdo 	abajo	abdomen	abdomen lateral
pies primero	lateral izquierdo 	derecha 	abdomen	abdomen rontal
pies primero	lateral izquierdo 	izquierda	abdomen	abdomen frontal
				
cabeza primero	supino	arriba	pelvis	pelvis  frontal
cabeza primero	supino	abajo	pelvis	pelvis  frontal
cabeza primero	supino	derecha 	pelvis	pelvis lateral
cabeza primero	supino	izquierda	pelvis	pelvis lateral
cabeza primero	prono	arriba	pelvis	pelvis  frontal
cabeza primero	prono	abajo	pelvis	pelvis  frontal
cabeza primero	prono	derecha 	pelvis	pelvis lateral
cabeza primero	prono	izquierda	pelvis	pelvis lateral
cabeza primero	lateral derecho 	arriba	pelvis	pelvis lateral
cabeza primero	lateral derecho 	abajo	pelvis	pelvis lateral
cabeza primero	lateral derecho 	derecha 	pelvis	pelvis  frontal
cabeza primero	lateral derecho 	izquierda	pelvis	pelvis  frontal
cabeza primero	lateral izquierdo 	arriba	pelvis	pelvis lateral
cabeza primero	lateral izquierdo 	abajo	pelvis	pelvis lateral
cabeza primero	lateral izquierdo 	derecha 	pelvis	pelvis  frontal
cabeza primero	lateral izquierdo 	izquierda	pelvis	abdomen y pelvis  frontal
				
pies primero	supino	arriba	pelvis	pelvis  frontal
pies primero	supino	abajo	pelvis	pelvis  frontal
pies primero	supino	derecha 	pelvis	pelvis lateral
pies primero	supino	izquierda	pelvis	pelvis lateral
pies primero	prono	arriba	pelvis	pelvis  frontal
pies primero	prono	abajo	pelvis	pelvis  frontal
pies primero	prono	derecha 	pelvis	pelvis lateral
pies primero	prono	izquierda	pelvis	pelvis lateral
pies primero	lateral derecho 	arriba	pelvis	pelvis lateral
pies primero	lateral derecho 	abajo	pelvis	pelvis lateral
pies primero	lateral derecho 	derecha 	pelvis	pelvis  frontal
pies primero	lateral derecho 	izquierda	pelvis	pelvis  frontal
pies primero	lateral izquierdo 	arriba	pelvis	pelvis lateral
pies primero	lateral izquierdo 	abajo	pelvis	pelvis lateral
pies primero	lateral izquierdo 	derecha 	pelvis	pelvis  frontal
pies primero	lateral izquierdo 	izquierda	pelvis	pelvis  frontal
				
cabeza primero	supino	arriba	abdomen y pelvis 	abdomenpelvis frontal
cabeza primero	supino	abajo	abdomen y pelvis 	abdomenpelvis frontal
cabeza primero	supino	derecha 	abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	supino	izquierda	abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	prono	arriba	abdomen y pelvis 	abdomenpelvis frontal
cabeza primero	prono	abajo	abdomen y pelvis 	abdomenpelvis frontal
cabeza primero	prono	derecha 	abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	prono	izquierda	abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	lateral derecho 	arriba	abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	lateral derecho 	abajo	abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	lateral derecho 	derecha 	abdomen y pelvis 	abdomenpelvis  frontal
cabeza primero	lateral derecho 	izquierda	abdomen y pelvis 	abdomenpelvis frontal
cabeza primero	lateral izquierdo 	arriba	abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	lateral izquierdo 	abajo	abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	lateral izquierdo 	derecha 	abdomen y pelvis 	abdomenpelvis frontal
cabeza primero	lateral izquierdo 	izquierda	abdomen y pelvis 	abdomenpelvis frontal
				
pies primero	supino	arriba	abdomen y pelvis 	abdomenpelvis frontal
pies primero	supino	abajo	abdomen y pelvis 	abdomenpelvis frontal
pies primero	supino	derecha 	abdomen y pelvis 	abdomenpelvis lateral
pies primero	supino	izquierda	abdomen y pelvis 	abdomenpelvis lateral
pies primero	prono	arriba	abdomen y pelvis 	abdomenpelvis frontal
pies primero	prono	abajo	abdomen y pelvis 	abdomenpelvis frontal
pies primero	prono	derecha 	abdomen y pelvis 	abdomenpelvis lateral
pies primero	prono	izquierda	abdomen y pelvis 	abdomenpelvis lateral
pies primero	lateral derecho 	arriba	abdomen y pelvis 	abdomenpelvis lateral
pies primero	lateral derecho 	abajo	abdomen y pelvis 	abdomenpelvis lateral
pies primero	lateral derecho 	derecha 	abdomen y pelvis 	abdomenpelvis frontal
pies primero	lateral derecho 	izquierda	abdomen y pelvis 	abdomenpelvis frontal
pies primero	lateral izquierdo 	arriba	abdomen y pelvis 	abdomenpelvis lateral
pies primero	lateral izquierdo 	abajo	abdomen y pelvis 	abdomenpelvis lateral
pies primero	lateral izquierdo 	derecha 	abdomen y pelvis 	abdomenpelvis frontal
pies primero	lateral izquierdo 	izquierda	abdomen y pelvis 	abdomenpelvis frontal
				
pies primero	supino	arriba	pielotac	pielotac frontal
pies primero	supino	abajo	pielotac	pielotac frontal
pies primero	supino	derecha 	pielotac	pielotac lateral
pies primero	supino	izquierda	pielotac	pielotac lateral
pies primero	prono	arriba	pielotac	pielotac frontal
pies primero	prono	abajo	pielotac	pielotac frontal
pies primero	prono	derecha 	pielotac	pielotac lateral
pies primero	prono	izquierda	pielotac	pielotac lateral
pies primero	lateral derecho 	arriba	pielotac	pielotac lateral
pies primero	lateral derecho 	abajo	pielotac	pielotac lateral
pies primero	lateral derecho 	derecha 	pielotac	pielotac frontal
pies primero	lateral derecho 	izquierda	pielotac	pielotac frontal
pies primero	lateral izquierdo 	arriba	pielotac	pielotac lateral
pies primero	lateral izquierdo 	abajo	pielotac	pielotac lateral
pies primero	lateral izquierdo 	derecha 	pielotac	pielotac frontal
pies primero	lateral izquierdo 	izquierda	pielotac	pielotac frontal
				
cabeza primero	supino	arriba	pielotac	pielotac frontal
cabeza primero	supino	abajo	pielotac	pielotac frontal
cabeza primero	supino	derecha 	pielotac	pielotac lateral
cabeza primero	supino	izquierda	pielotac	pielotac lateral
cabeza primero	prono	arriba	pielotac	pielotac frontal
cabeza primero	prono	abajo	pielotac	pielotac frontal
cabeza primero	prono	derecha 	pielotac	pielotac lateral
cabeza primero	prono	izquierda	pielotac	pielotac lateral
cabeza primero	lateral derecho 	arriba	pielotac	pielotac lateral
cabeza primero	lateral derecho 	abajo	pielotac	pielotac lateral
cabeza primero	lateral derecho 	derecha 	pielotac	pielotac frontal
cabeza primero	lateral derecho 	izquierda	pielotac	pielotac frontal
cabeza primero	lateral izquierdo 	arriba	pielotac	pielotac lateral
cabeza primero	lateral izquierdo 	abajo	pielotac	pielotac lateral
cabeza primero	lateral izquierdo 	derecha 	pielotac	pielotac frontal
cabeza primero	lateral izquierdo 	izquierda	pielotac	pielotac frontal
				
cabeza primero	supino	arriba	columna dorsal	columna dorsal frontal
cabeza primero	supino	abajo	columna dorsal	columna dorsal frontal
cabeza primero	supino	derecha 	columna dorsal	columna dorsal lateral
cabeza primero	supino	izquierda	columna dorsal	columna dorsal lateral
cabeza primero	prono	arriba	columna dorsal	columna dorsal frontal
cabeza primero	prono	abajo	columna dorsal	columna dorsal frontal
cabeza primero	prono	derecha 	columna dorsal	columna dorsal lateral
cabeza primero	prono	izquierda	columna dorsal	columna dorsal lateral
cabeza primero	lateral derecho 	arriba	columna dorsal	columna dorsal lateral
cabeza primero	lateral derecho 	abajo	columna dorsal	columna dorsal lateral
cabeza primero	lateral derecho 	derecha 	columna dorsal	columna dorsal frontal
cabeza primero	lateral derecho 	izquierda	columna dorsal	columna dorsal frontal
cabeza primero	lateral izquierdo 	arriba	columna dorsal	columna dorsal lateral
cabeza primero	lateral izquierdo 	abajo	columna dorsal	columna dorsal lateral
cabeza primero	lateral izquierdo 	derecha 	columna dorsal	columna dorsal frontal
cabeza primero	lateral izquierdo 	izquierda	columna dorsal	columna dorsal frontal
				
pies primero	supino	arriba	columna dorsal	columna dorsal frontal
pies primero	supino	abajo	columna dorsal	columna dorsal frontal
pies primero	supino	derecha 	columna dorsal	columna dorsal lateral
pies primero	supino	izquierda	columna dorsal	columna dorsal lateral
pies primero	prono	arriba	columna dorsal	columna dorsal frontal
pies primero	prono	abajo	columna dorsal	columna dorsal frontal
pies primero	prono	derecha 	columna dorsal	columna dorsal lateral
pies primero	prono	izquierda	columna dorsal	columna dorsal lateral
pies primero	lateral derecho 	arriba	columna dorsal	columna dorsal lateral
pies primero	lateral derecho 	abajo	columna dorsal	columna dorsal lateral
pies primero	lateral derecho 	derecha 	columna dorsal	columna dorsal frontal
pies primero	lateral derecho 	izquierda	columna dorsal	columna dorsal frontal
pies primero	lateral izquierdo 	arriba	columna dorsal	columna dorsal lateral
pies primero	lateral izquierdo 	abajo	columna dorsal	columna dorsal lateral
pies primero	lateral izquierdo 	derecha 	columna dorsal	columna dorsal frontal
pies primero	lateral izquierdo 	izquierda	columna dorsal	columna dorsal frontal
				
cabeza primero	supino	arriba	columna lumbar	columna lumbar frontal
cabeza primero	supino	abajo	columna lumbar	columna lumbar frontal
cabeza primero	supino	derecha 	columna lumbar	columna lumbar lateral
cabeza primero	supino	izquierda	columna lumbar	columna lumbar lateral
cabeza primero	prono	arriba	columna lumbar	columna lumbar frontal
cabeza primero	prono	abajo	columna lumbar	columna lumbar frontal
cabeza primero	prono	derecha 	columna lumbar	columna lumbar lateral
cabeza primero	prono	izquierda	columna lumbar	columna lumbar lateral
cabeza primero	lateral derecho 	arriba	columna lumbar	columna lumbar lateral
cabeza primero	lateral derecho 	abajo	columna lumbar	columna lumbar lateral
cabeza primero	lateral derecho 	derecha 	columna lumbar	columna lumbar frontal
cabeza primero	lateral derecho 	izquierda	columna lumbar	columna lumbar frontal
cabeza primero	lateral izquierdo 	arriba	columna lumbar	columna lumbar lateral
cabeza primero	lateral izquierdo 	abajo	columna lumbar	columna lumbar lateral
cabeza primero	lateral izquierdo 	derecha 	columna lumbar	columna lumbar frontal
cabeza primero	lateral izquierdo 	izquierda	columna lumbar	columna lumbar frontal
				
pies primero	supino	arriba	columna lumbar	columna lumbar frontal
pies primero	supino	abajo	columna lumbar	columna lumbar frontal
pies primero	supino	derecha 	columna lumbar	columna lumbar lateral
pies primero	supino	izquierda	columna lumbar	columna lumbar lateral
pies primero	prono	arriba	columna lumbar	columna lumbar frontal
pies primero	prono	abajo	columna lumbar	columna lumbar frontal
pies primero	prono	derecha 	columna lumbar	columna lumbar lateral
pies primero	prono	izquierda	columna lumbar	columna lumbar lateral
pies primero	lateral derecho 	arriba	columna lumbar	columna lumbar lateral
pies primero	lateral derecho 	abajo	columna lumbar	columna lumbar lateral
pies primero	lateral derecho 	derecha 	columna lumbar	columna lumbar frontal
pies primero	lateral derecho 	izquierda	columna lumbar	columna lumbar frontal
pies primero	lateral izquierdo 	arriba	columna lumbar	columna lumbar lateral
pies primero	lateral izquierdo 	abajo	columna lumbar	columna lumbar lateral
pies primero	lateral izquierdo 	derecha 	columna lumbar	columna lumbar frontal
pies primero	lateral izquierdo 	izquierda	columna lumbar	columna lumbar frontal
				
cabeza primero	supino	arriba	torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	supino	abajo	torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	supino	derecha 	torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	supino	izquierda	torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	prono	arriba	torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	prono	abajo	torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	prono	derecha 	torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	prono	izquierda	torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	lateral derecho 	arriba	torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	lateral derecho 	abajo	torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	lateral derecho 	derecha 	torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	lateral derecho 	izquierda	torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	lateral izquierdo 	arriba	torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	lateral izquierdo 	abajo	torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	lateral izquierdo 	derecha 	torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	lateral izquierdo 	izquierda	torax abdomen y pelvis	torax abdomen pelvis frontal
				
pies primero	supino	arriba	torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	supino	abajo	torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	supino	derecha 	torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	supino	izquierda	torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	prono	arriba	torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	prono	abajo	torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	prono	derecha 	torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	prono	izquierda	torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	lateral derecho 	arriba	torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	lateral derecho 	abajo	torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	lateral derecho 	derecha 	torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	lateral derecho 	izquierda	torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	lateral izquierdo 	arriba	torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	lateral izquierdo 	abajo	torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	lateral izquierdo 	derecha 	torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	lateral izquierdo 	izquierda	torax abdomen y pelvis	torax abdomen pelvis frontal
				
cabeza primero	supino	arriba	hombro	hombro frontal
cabeza primero	supino	abajo	hombro	hombro frontal
cabeza primero	supino	derecha 	hombro	hombro lateral
cabeza primero	supino	izquierda	hombro	hombro lateral
cabeza primero	prono	arriba	hombro	hombro frontal
cabeza primero	prono	abajo	hombro	hombro frontal
cabeza primero	prono	derecha 	hombro	hombro lateral
cabeza primero	prono	izquierda	hombro	hombro lateral
cabeza primero	lateral derecho 	arriba	hombro	hombro lateral
cabeza primero	lateral derecho 	abajo	hombro	hombro lateral
cabeza primero	lateral derecho 	derecha 	hombro	hombro frontal
cabeza primero	lateral derecho 	izquierda	hombro	hombro frontal
cabeza primero	lateral izquierdo 	arriba	hombro	hombro lateral
cabeza primero	lateral izquierdo 	abajo	hombro	hombro lateral
cabeza primero	lateral izquierdo 	derecha 	hombro	hombro frontal
cabeza primero	lateral izquierdo 	izquierda	hombro	hombro frontal
				
cabeza primero	supino	arriba	brazo	brazo frontal
cabeza primero	supino	abajo	brazo	brazo frontal
cabeza primero	supino	derecha 	brazo	brazo lateral
cabeza primero	supino	izquierda	brazo	brazo lateral
cabeza primero	prono	arriba	brazo	brazo frontal
cabeza primero	prono	abajo	brazo	brazo frontal
cabeza primero	prono	derecha 	brazo	brazo lateral
cabeza primero	prono	izquierda	brazo	brazo lateral
cabeza primero	lateral derecho 	arriba	brazo	brazo lateral
cabeza primero	lateral derecho 	abajo	brazo	brazo lateral
cabeza primero	lateral derecho 	derecha 	brazo	brazo frontal
cabeza primero	lateral derecho 	izquierda	brazo	brazo frontal
cabeza primero	lateral izquierdo 	arriba	brazo	brazo lateral
cabeza primero	lateral izquierdo 	abajo	brazo	brazo lateral
cabeza primero	lateral izquierdo 	derecha 	brazo	brazo frontal
cabeza primero	lateral izquierdo 	izquierda	brazo	brazo frontal
				
cabeza primero	supino	arriba	codo	codo frontal
cabeza primero	supino	abajo	codo	codo frontal
cabeza primero	supino	derecha 	codo	codo lateral
cabeza primero	supino	izquierda	codo	codo lateral
cabeza primero	prono	arriba	codo	codo frontal
cabeza primero	prono	abajo	codo	codo frontal
cabeza primero	prono	derecha 	codo	codo lateral
cabeza primero	prono	izquierda	codo	codo lateral
cabeza primero	lateral derecho 	arriba	codo	codo lateral
cabeza primero	lateral derecho 	abajo	codo	codo lateral
cabeza primero	lateral derecho 	derecha 	codo	codo frontal
cabeza primero	lateral derecho 	izquierda	codo	codo frontal
cabeza primero	lateral izquierdo 	arriba	codo	codo lateral
cabeza primero	lateral izquierdo 	abajo	codo	codo lateral
cabeza primero	lateral izquierdo 	derecha 	codo	codo frontal
cabeza primero	lateral izquierdo 	izquierda	codo	codo frontal
				
cabeza primero	supino	arriba	antebrazo	antebrazo frontal
cabeza primero	supino	abajo	antebrazo	antebrazo frontal
cabeza primero	supino	derecha 	antebrazo	antebrazo lateral 
cabeza primero	supino	izquierda	antebrazo	antebrazo lateral 
cabeza primero	prono	arriba	antebrazo	antebrazo frontal
cabeza primero	prono	abajo	antebrazo	antebrazo frontal
cabeza primero	prono	derecha 	antebrazo	antebrazo lateral 
cabeza primero	prono	izquierda	antebrazo	antebrazo lateral 
cabeza primero	lateral derecho 	arriba	antebrazo	antebrazo lateral 
cabeza primero	lateral derecho 	abajo	antebrazo	antebrazo lateral 
cabeza primero	lateral derecho 	derecha 	antebrazo	antebrazo frontal
cabeza primero	lateral derecho 	izquierda	antebrazo	antebrazo frontal
cabeza primero	lateral izquierdo 	arriba	antebrazo	antebrazo lateral 
cabeza primero	lateral izquierdo 	abajo	antebrazo	antebrazo lateral 
cabeza primero	lateral izquierdo 	derecha 	antebrazo	antebrazo frontal
cabeza primero	lateral izquierdo 	izquierda	antebrazo	antebrazo frontal
				
cabeza primero	supino	arriba	muñeca	muñeca frontal
cabeza primero	supino	abajo	muñeca	mano muñeca frontal
cabeza primero	supino	derecha 	muñeca	muñeca lateral 
cabeza primero	supino	izquierda	muñeca	muñeca lateral 
cabeza primero	prono	arriba	muñeca	muñeca frontal
cabeza primero	prono	abajo	muñeca	muñeca frontal
cabeza primero	prono	derecha 	muñeca	muñeca lateral 
cabeza primero	prono	izquierda	muñeca	muñeca lateral 
cabeza primero	lateral derecho 	arriba	muñeca	muñeca lateral 
cabeza primero	lateral derecho 	abajo	muñeca	muñeca lateral 
cabeza primero	lateral derecho 	derecha 	muñeca	muñeca frontal
cabeza primero	lateral derecho 	izquierda	muñeca	muñeca frontal
cabeza primero	lateral izquierdo 	arriba	muñeca	muñeca lateral 
cabeza primero	lateral izquierdo 	abajo	muñeca	muñeca lateral 
cabeza primero	lateral izquierdo 	derecha 	muñeca	muñeca frontal
cabeza primero	lateral izquierdo 	izquierda	muñeca	muñeca frontal
				
cabeza primero	supino	arriba	mano	mano frontal
cabeza primero	supino	abajo	mano	mano frontal
cabeza primero	supino	derecha 	mano	mano ateral 
cabeza primero	supino	izquierda	mano	mano lateral 
cabeza primero	prono	arriba	mano	mano rontal
cabeza primero	prono	abajo	mano	mano frontal
cabeza primero	prono	derecha 	mano	mano lateral 
cabeza primero	prono	izquierda	mano	mano ateral 
cabeza primero	lateral derecho 	arriba	mano	mano ateral 
cabeza primero	lateral derecho 	abajo	mano	mano lateral 
cabeza primero	lateral derecho 	derecha 	mano	mano frontal
cabeza primero	lateral derecho 	izquierda	mano	mano frontal
cabeza primero	lateral izquierdo 	arriba	mano	mano lateral 
cabeza primero	lateral izquierdo 	abajo	mano	mano lateral 
cabeza primero	lateral izquierdo 	derecha 	mano	mano frontal
cabeza primero	lateral izquierdo 	izquierda	mano	mano frontal
				
pies primero	supino	arriba	cadera	pelvis frontal
pies primero	supino	abajo	cadera	pelvis frontal
pies primero	supino	derecha 	cadera	pelvis lateral 
pies primero	supino	izquierda	cadera	pelvis lateral 
pies primero	prono	arriba	cadera	pelvis frontal
pies primero	prono	abajo	cadera	pelvis frontal
pies primero	prono	derecha 	cadera	pelvis lateral 
pies primero	prono	izquierda	cadera	pelvis lateral 
pies primero	lateral derecho 	arriba	cadera	pelvis lateral 
pies primero	lateral derecho 	abajo	cadera	pelvis lateral 
pies primero	lateral derecho 	derecha 	cadera	pelvis frontal
pies primero	lateral derecho 	izquierda	cadera	pelvis frontal
pies primero	lateral izquierdo 	arriba	cadera	pelvis lateral 
pies primero	lateral izquierdo 	abajo	cadera	pelvis lateral 
pies primero	lateral izquierdo 	derecha 	cadera	pelvis frontal
pies primero	lateral izquierdo 	izquierda	cadera	pelvis frontal
				
pies primero	supino	arriba	rodilla	rodilla frontal
pies primero	supino	abajo	rodilla	rodilla frontal
pies primero	supino	derecha 	rodilla	rodilla lateral 
pies primero	supino	izquierda	rodilla	rodilla lateral 
pies primero	prono	arriba	rodilla	rodilla frontal
pies primero	prono	abajo	rodilla	rodilla frontal
pies primero	prono	derecha 	rodilla	rodilla lateral 
pies primero	prono	izquierda	rodilla	rodilla lateral 
pies primero	lateral derecho 	arriba	rodilla	rodilla lateral 
pies primero	lateral derecho 	abajo	rodilla	rodilla lateral 
pies primero	lateral derecho 	derecha 	rodilla	rodilla frontal
pies primero	lateral derecho 	izquierda	rodilla	rodilla frontal
pies primero	lateral izquierdo 	arriba	rodilla	rodilla lateral 
pies primero	lateral izquierdo 	abajo	rodilla	rodilla lateral 
pies primero	lateral izquierdo 	derecha 	rodilla	rodilla frontal
pies primero	lateral izquierdo 	izquierda	rodilla	rodilla frontal
				
pies primero	supino	arriba	pierna	pierna frontal
pies primero	supino	abajo	pierna	pierna frontal
pies primero	supino	derecha 	pierna	pierna lateral 
pies primero	supino	izquierda	pierna	pierna lateral 
pies primero	prono	arriba	pierna	pierna frontal
pies primero	prono	abajo	pierna	pierna frontal
pies primero	prono	derecha 	pierna	pierna lateral 
pies primero	prono	izquierda	pierna	pierna lateral 
pies primero	lateral derecho 	arriba	pierna	pierna lateral 
pies primero	lateral derecho 	abajo	pierna	pierna lateral 
pies primero	lateral derecho 	derecha 	pierna	pierna frontal
pies primero	lateral derecho 	izquierda	pierna	pierna frontal
pies primero	lateral izquierdo 	arriba	pierna	pierna lateral 
pies primero	lateral izquierdo 	abajo	pierna	pierna lateral 
pies primero	lateral izquierdo 	derecha 	pierna	pierna frontal
pies primero	lateral izquierdo 	izquierda	pierna	pierna frontal
				
pies primero	supino	arriba	tobillo	pie tobillo frontal
pies primero	supino	abajo	tobillo	pie tobillo frontal
pies primero	supino	derecha 	tobillo	pie tobillo lateral 
pies primero	supino	izquierda	tobillo	pie tobillo lateral 
pies primero	prono	arriba	tobillo	pie tobillo frontal
pies primero	prono	abajo	tobillo	pie tobillo frontal
pies primero	prono	derecha 	tobillo	pie tobillo lateral 
pies primero	prono	izquierda	tobillo	pie tobillo lateral 
pies primero	lateral derecho 	arriba	tobillo	pie tobillo lateral 
pies primero	lateral derecho 	abajo	tobillo	pie tobillo lateral 
pies primero	lateral derecho 	derecha 	tobillo	pie tobillo frontal
pies primero	lateral derecho 	izquierda	tobillo	pie tobillo frontal
pies primero	lateral izquierdo 	arriba	tobillo	pie tobillo lateral 
pies primero	lateral izquierdo 	abajo	tobillo	pie tobillo lateral 
pies primero	lateral izquierdo 	derecha 	tobillo	pie tobillo frontal
pies primero	lateral izquierdo 	izquierda	tobillo	pie tobillo frontal
				
pies primero	supino	arriba	pie	pie tobillo frontal
pies primero	supino	abajo	pie	pie tobillo frontal
pies primero	supino	derecha 	pie	pie tobillo lateral 
pies primero	supino	izquierda	pie	pie tobillo lateral 
pies primero	prono	arriba	pie	pie tobillo frontal
pies primero	prono	abajo	pie	pie tobillo frontal
pies primero	prono	derecha 	pie	pie tobillo lateral 
pies primero	prono	izquierda	pie	pie tobillo lateral 
pies primero	lateral derecho 	arriba	pie	pie tobillo lateral 
pies primero	lateral derecho 	abajo	pie	pie tobillo lateral 
pies primero	lateral derecho 	derecha 	pie	pie tobillo frontal
pies primero	lateral derecho 	izquierda	pie	pie tobillo frontal
pies primero	lateral izquierdo 	arriba	pie	pie tobillo lateral 
pies primero	lateral izquierdo 	abajo	pie	pie tobillo lateral 
pies primero	lateral izquierdo 	derecha 	pie	pie tobillo frontal
pies primero	lateral izquierdo 	izquierda	pie	pie tobillo frontal
				
cabeza primero	supino	arriba	angiotac cerebro	cabeza frontal
cabeza primero	supino	abajo	angiotac cerebro	cabeza frontal
cabeza primero	supino	derecha 	angiotac cerebro	cabeza lateral
cabeza primero	supino	izquierda	angiotac cerebro	cabeza lateral
cabeza primero	prono	arriba	angiotac cerebro	cabeza frontal
cabeza primero	prono	abajo	angiotac cerebro	cabeza frontal
cabeza primero	prono	derecha 	angiotac cerebro	cabeza lateral
cabeza primero	prono	izquierda	angiotac cerebro	cabeza lateral
cabeza primero	lateral derecho	arriba	angiotac cerebro	cabeza lateral
cabeza primero	lateral derecho	abajo	angiotac cerebro	cabeza lateral
cabeza primero	lateral derecho	derecha 	angiotac cerebro	cabeza frontal
cabeza primero	lateral derecho	izquierda	angiotac cerebro	cabeza frontal
cabeza primero	lateral izquerdo	arriba	angiotac cerebro	cabeza lateral
cabeza primero	lateral izquerdo	abajo	angiotac cerebro	cabeza lateral
cabeza primero	lateral izquerdo	derecha 	angiotac cerebro	cabeza frontal
cabeza primero	lateral izquerdo	izquierda	angiotac cerebro	cabeza frontal
				
cabeza primero	supino	arriba	angiotac cuello	angiotac cuello frontal
cabeza primero	supino	abajo	angiotac cuello	angiotac cuello frontal
cabeza primero	supino	derecha 	angiotac cuello	angiotac cuello lateral
cabeza primero	supino	izquierda	angiotac cuello	angiotac cuello lateral
cabeza primero	prono	arriba	angiotac cuello	angiotac cuello frontal
cabeza primero	prono	abajo	angiotac cuello	angiotac cuello frontal
cabeza primero	prono	derecha 	angiotac cuello	angiotac cuello lateral
cabeza primero	prono	izquierda	angiotac cuello	angiotac cuello lateral
cabeza primero	lateral derecho	arriba	angiotac cuello	angiotac cuello lateral
cabeza primero	lateral derecho	abajo	angiotac cuello	angiotac cuello lateral
cabeza primero	lateral derecho	derecha 	angiotac cuello	angiotac cuello frontal
cabeza primero	lateral derecho	izquierda	angiotac cuello	angiotac cuello frontal
cabeza primero	lateral izquerdo	arriba	angiotac cuello	angiotac cuello lateral
cabeza primero	lateral izquerdo	abajo	angiotac cuello	angiotac cuello lateral
cabeza primero	lateral izquerdo	derecha 	angiotac cuello	angiotac cuello frontal
cabeza primero	lateral izquerdo	izquierda	angiotac cuello	angiotac cuello frontal
				
cabeza primero	supino	arriba	angiotac cerebro cuello	angiotac cerebro cuello frontal
cabeza primero	supino	abajo	angiotac cerebro cuello	angiotac cerebro cuello frontal
cabeza primero	supino	derecha 	angiotac cerebro cuello	angiotac cerebro cuello lateral
cabeza primero	supino	izquierda	angiotac cerebro cuello	angiotac cerebro cuello lateral
cabeza primero	prono	arriba	angiotac cerebro cuello	angiotac cerebro cuello frontal
cabeza primero	prono	abajo	angiotac cerebro cuello	angiotac cerebro cuello frontal
cabeza primero	prono	derecha 	angiotac cerebro cuello	angiotac cerebro cuello lateral
cabeza primero	prono	izquierda	angiotac cerebro cuello	angiotac cerebro cuello lateral
cabeza primero	lateral derecho	arriba	angiotac cerebro cuello	angiotac cerebro cuello lateral
cabeza primero	lateral derecho	abajo	angiotac cerebro cuello	angiotac cerebro cuello lateral
cabeza primero	lateral derecho	derecha 	angiotac cerebro cuello	angiotac cerebro cuello frontal
cabeza primero	lateral derecho	izquierda	angiotac cerebro cuello	angiotac cerebro cuello frontal
cabeza primero	lateral izquerdo	arriba	angiotac cerebro cuello	angiotac cerebro cuello lateral
cabeza primero	lateral izquerdo	abajo	angiotac cerebro cuello	angiotac cerebro cuello lateral
cabeza primero	lateral izquerdo	derecha 	angiotac cerebro cuello	angiotac cerebro cuello frontal
cabeza primero	lateral izquerdo	izquierda	angiotac cerebro cuello	angiotac cerebro cuello frontal
				
cabeza primero	supino	arriba	angiotac torax	torax frontal
cabeza primero	supino	abajo	angiotac torax	torax frontal
cabeza primero	supino	derecha 	angiotac torax	torax lateral
cabeza primero	supino	izquierda	angiotac torax	torax lateral
cabeza primero	prono	arriba	angiotac torax	torax frontal
cabeza primero	prono	abajo	angiotac torax	torax frontal
cabeza primero	prono	derecha 	angiotac torax	torax lateral
cabeza primero	prono	izquierda	angiotac torax	torax lateral
cabeza primero	lateral derecho 	arriba	angiotac torax	torax lateral
cabeza primero	lateral derecho 	abajo	angiotac torax	torax lateral
cabeza primero	lateral derecho 	derecha 	angiotac torax	torax frontal
cabeza primero	lateral derecho 	izquierda	angiotac torax	torax frontal
cabeza primero	lateral izquierdo 	arriba	angiotac torax	torax lateral
cabeza primero	lateral izquierdo 	abajo	angiotac torax	torax lateral
cabeza primero	lateral izquierdo 	derecha 	angiotac torax	torax frontal
cabeza primero	lateral izquierdo 	izquierda	angiotac torax	torax frontal
				
pies primero	supino	arriba	angiotac torax	torax frontal
pies primero	supino	abajo	angiotac torax	torax frontal
pies primero	supino	derecha 	angiotac torax	torax lateral
pies primero	supino	izquierda	angiotac torax	torax lateral
pies primero	prono	arriba	angiotac torax	torax frontal
pies primero	prono	abajo	angiotac torax	torax frontal
pies primero	prono	derecha 	angiotac torax	torax lateral
pies primero	prono	izquierda	angiotac torax	torax lateral
pies primero	lateral derecho 	arriba	angiotac torax	torax lateral
pies primero	lateral derecho 	abajo	angiotac torax	torax lateral
pies primero	lateral derecho 	derecha 	angiotac torax	torax frontal
pies primero	lateral derecho 	izquierda	angiotac torax	torax frontal
pies primero	lateral izquierdo 	arriba	angiotac torax	torax lateral
pies primero	lateral izquierdo 	abajo	angiotac torax	torax lateral
pies primero	lateral izquierdo 	derecha 	angiotac torax	torax frontal
pies primero	lateral izquierdo 	izquierda	angiotac torax	torax frontal
				
cabeza primero	supino	arriba	angiotac abdomen	abdomen frontal
cabeza primero	supino	abajo	angiotac abdomen	abdomen frontal
cabeza primero	supino	derecha 	angiotac abdomen	abdomen lateral
cabeza primero	supino	izquierda	angiotac abdomen	abdomen lateral
cabeza primero	prono	arriba	angiotac abdomen	abdomen frontal
cabeza primero	prono	abajo	angiotac abdomen	abdomen frontal
cabeza primero	prono	derecha 	angiotac abdomen	abdomen ateral
cabeza primero	prono	izquierda	angiotac abdomen	abdomen lateral
cabeza primero	lateral derecho 	arriba	angiotac abdomen	abdomen lateral
cabeza primero	lateral derecho 	abajo	angiotac abdomen	abdomen lateral
cabeza primero	lateral derecho 	derecha 	angiotac abdomen	abdomen frontal
cabeza primero	lateral derecho 	izquierda	angiotac abdomen	abdomen frontal
cabeza primero	lateral izquierdo 	arriba	angiotac abdomen	abdomen lateral
cabeza primero	lateral izquierdo 	abajo	angiotac abdomen	abdomen lateral
cabeza primero	lateral izquierdo 	derecha 	angiotac abdomen	abdomen frontal
cabeza primero	lateral izquierdo 	izquierda	angiotac abdomen	abdomen frontal
				
pies primero	supino	arriba	angiotac abdomen	abdomen frontal
pies primero	supino	abajo	angiotac abdomen	abdomen frontal
pies primero	supino	derecha 	angiotac abdomen	abdomen lateral
pies primero	supino	izquierda	angiotac abdomen	abdomen lateral
pies primero	prono	arriba	angiotac abdomen	abdomen frontal
pies primero	prono	abajo	angiotac abdomen	abdomen  frontal
pies primero	prono	derecha 	angiotac abdomen	abdomen lateral
pies primero	prono	izquierda	angiotac abdomen	abdomen ateral
pies primero	lateral derecho 	arriba	angiotac abdomen	abdomen ateral
pies primero	lateral derecho 	abajo	angiotac abdomen	abdomen lateral
pies primero	lateral derecho 	derecha 	angiotac abdomen	abdomen  frontal
pies primero	lateral derecho 	izquierda	angiotac abdomen	abdomen frontal
pies primero	lateral izquierdo 	arriba	angiotac abdomen	abdomen lateral
pies primero	lateral izquierdo 	abajo	angiotac abdomen	abdomen lateral
pies primero	lateral izquierdo 	derecha 	angiotac abdomen	abdomen rontal
pies primero	lateral izquierdo 	izquierda	angiotac abdomen	abdomen frontal
				
cabeza primero	supino	arriba	angiotac abdomen y pelvis 	abdomenpelvis frontal
cabeza primero	supino	abajo	angiotac abdomen y pelvis 	abdomenpelvis frontal
cabeza primero	supino	derecha 	angiotac abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	supino	izquierda	angiotac abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	prono	arriba	angiotac abdomen y pelvis 	abdomenpelvis frontal
cabeza primero	prono	abajo	angiotac abdomen y pelvis 	abdomenpelvis frontal
cabeza primero	prono	derecha 	angiotac abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	prono	izquierda	angiotac abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	lateral derecho 	arriba	angiotac abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	lateral derecho 	abajo	angiotac abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	lateral derecho 	derecha 	angiotac abdomen y pelvis 	abdomenpelvis  frontal
cabeza primero	lateral derecho 	izquierda	angiotac abdomen y pelvis 	abdomenpelvis frontal
cabeza primero	lateral izquierdo 	arriba	angiotac abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	lateral izquierdo 	abajo	angiotac abdomen y pelvis 	abdomenpelvis lateral
cabeza primero	lateral izquierdo 	derecha 	angiotac abdomen y pelvis 	abdomenpelvis frontal
cabeza primero	lateral izquierdo 	izquierda	angiotac abdomen y pelvis 	abdomenpelvis frontal
				
pies primero	supino	arriba	angiotac abdomen y pelvis 	abdomenpelvis frontal
pies primero	supino	abajo	angiotac abdomen y pelvis 	abdomenpelvis frontal
pies primero	supino	derecha 	angiotac abdomen y pelvis 	abdomenpelvis lateral
pies primero	supino	izquierda	angiotac abdomen y pelvis 	abdomenpelvis lateral
pies primero	prono	arriba	angiotac abdomen y pelvis 	abdomenpelvis frontal
pies primero	prono	abajo	angiotac abdomen y pelvis 	abdomenpelvis frontal
pies primero	prono	derecha 	angiotac abdomen y pelvis 	abdomenpelvis lateral
pies primero	prono	izquierda	angiotac abdomen y pelvis 	abdomenpelvis lateral
pies primero	lateral derecho 	arriba	angiotac abdomen y pelvis 	abdomenpelvis lateral
pies primero	lateral derecho 	abajo	angiotac abdomen y pelvis 	abdomenpelvis lateral
pies primero	lateral derecho 	derecha 	angiotac abdomen y pelvis 	abdomenpelvis frontal
pies primero	lateral derecho 	izquierda	angiotac abdomen y pelvis 	abdomenpelvis frontal
pies primero	lateral izquierdo 	arriba	angiotac abdomen y pelvis 	abdomenpelvis lateral
pies primero	lateral izquierdo 	abajo	angiotac abdomen y pelvis 	abdomenpelvis lateral
pies primero	lateral izquierdo 	derecha 	angiotac abdomen y pelvis 	abdomenpelvis frontal
pies primero	lateral izquierdo 	izquierda	angiotac abdomen y pelvis 	abdomenpelvis frontal
				
cabeza primero	supino	arriba	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	supino	abajo	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	supino	derecha 	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	supino	izquierda	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	prono	arriba	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	prono	abajo	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	prono	derecha 	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	prono	izquierda	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	lateral derecho 	arriba	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	lateral derecho 	abajo	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	lateral derecho 	derecha 	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	lateral derecho 	izquierda	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	lateral izquierdo 	arriba	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	lateral izquierdo 	abajo	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
cabeza primero	lateral izquierdo 	derecha 	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
cabeza primero	lateral izquierdo 	izquierda	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
				
pies primero	supino	arriba	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	supino	abajo	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	supino	derecha 	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	supino	izquierda	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	prono	arriba	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	prono	abajo	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	prono	derecha 	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	prono	izquierda	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	lateral derecho 	arriba	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	lateral derecho 	abajo	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	lateral derecho 	derecha 	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	lateral derecho 	izquierda	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	lateral izquierdo 	arriba	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	lateral izquierdo 	abajo	angiotac torax abdomen y pelvis	torax abdomen pelvis lateral
pies primero	lateral izquierdo 	derecha 	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
pies primero	lateral izquierdo 	izquierda	angiotac torax abdomen y pelvis	torax abdomen pelvis frontal
				
cabeza primero	supino	arriba	angiotac extremidad superior derecha	angiotac extremidad superior derecha frontal
cabeza primero	supino	abajo	angiotac extremidad superior derecha	angiotac extremidad superior derecha frontal
cabeza primero	supino	derecha 	angiotac extremidad superior derecha	angiotac extremidad superior derecha lateral 
cabeza primero	supino	izquierda	angiotac extremidad superior derecha	angiotac extremidad superior derecha lateral 
cabeza primero	prono	arriba	angiotac extremidad superior derecha	angiotac extremidad superior derecha frontal
cabeza primero	prono	abajo	angiotac extremidad superior derecha	angiotac extremidad superior derecha frontal
cabeza primero	prono	derecha 	angiotac extremidad superior derecha	angiotac extremidad superior derecha lateral 
cabeza primero	prono	izquierda	angiotac extremidad superior derecha	angiotac extremidad superior derecha lateral 
cabeza primero	lateral derecho 	arriba	angiotac extremidad superior derecha	angiotac extremidad superior derecha lateral 
cabeza primero	lateral derecho 	abajo	angiotac extremidad superior derecha	angiotac extremidad superior derecha lateral 
cabeza primero	lateral derecho 	derecha 	angiotac extremidad superior derecha	angiotac extremidad superior derecha frontal
cabeza primero	lateral derecho 	izquierda	angiotac extremidad superior derecha	angiotac extremidad superior derecha frontal
cabeza primero	lateral izquierdo 	arriba	angiotac extremidad superior derecha	angiotac extremidad superior derecha lateral 
cabeza primero	lateral izquierdo 	abajo	angiotac extremidad superior derecha	angiotac extremidad superior derecha lateral 
cabeza primero	lateral izquierdo 	derecha 	angiotac extremidad superior derecha	angiotac extremidad superior derecha frontal
cabeza primero	lateral izquierdo 	izquierda	angiotac extremidad superior derecha	angiotac extremidad superior derecha frontal
				
cabeza primero	supino	arriba	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo frontal
cabeza primero	supino	abajo	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo frontal
cabeza primero	supino	derecha 	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo lateral 
cabeza primero	supino	izquierda	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo lateral 
cabeza primero	prono	arriba	angiotac extremidad superior izquierda	 angiotac extremidad superior izquierdo frontal
cabeza primero	prono	abajo	angiotac extremidad superior izquierda	fangiotac extremidad superior izquierdo frontal
cabeza primero	prono	derecha 	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo lateral 
cabeza primero	prono	izquierda	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo lateral 
cabeza primero	lateral derecho 	arriba	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo lateral 
cabeza primero	lateral derecho 	abajo	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo lateral 
cabeza primero	lateral derecho 	derecha 	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo frontal
cabeza primero	lateral derecho 	izquierda	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo frontal
cabeza primero	lateral izquierdo 	arriba	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo lateral 
cabeza primero	lateral izquierdo 	abajo	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo lateral 
cabeza primero	lateral izquierdo 	derecha 	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo frontal
cabeza primero	lateral izquierdo 	izquierda	angiotac extremidad superior izquierda	angiotac extremidad superior izquierdo frontal
				
pies primero	supino	arriba	angiotac extremidad inferior	angiotac extremidad inferior frontal
pies primero	supino	abajo	angiotac extremidad inferior	angiotac extremidad inferior frontal
pies primero	supino	derecha 	angiotac extremidad inferior	angiotac extremidad inferior lateral 
pies primero	supino	izquierda	angiotac extremidad inferior	angiotac extremidad inferior lateral 
pies primero	prono	arriba	angiotac extremidad inferior	angiotac extremidad inferior frontal
pies primero	prono	abajo	angiotac extremidad inferior	angiotac extremidad inferior frontal
pies primero	prono	derecha 	angiotac extremidad inferior	angiotac extremidad inferior lateral 
pies primero	prono	izquierda	angiotac extremidad inferior	angiotac extremidad inferior lateral 
pies primero	lateral derecho 	arriba	angiotac extremidad inferior	angiotac extremidad inferior lateral 
pies primero	lateral derecho 	abajo	angiotac extremidad inferior	angiotac extremidad inferior lateral 
pies primero	lateral derecho 	derecha 	angiotac extremidad inferior	angiotac extremidad inferior frontal
pies primero	lateral derecho 	izquierda	angiotac extremidad inferior	angiotac extremidad inferior frontal
pies primero	lateral izquierdo 	arriba	angiotac extremidad inferior	angiotac extremidad inferior lateral 
pies primero	lateral izquierdo 	abajo	angiotac extremidad inferior	angiotac extremidad inferior lateral 
pies primero	lateral izquierdo 	derecha 	angiotac extremidad inferior	angiotac extremidad inferior frontal
pies primero	lateral izquierdo 	izquierda	angiotac extremidad inferior	angiotac extremidad inferior frontal"""

def cargar_reglas_rx_desde_tsv(tsv_texto):
    reglas = {}
    filas_cargadas = 0
    errores = []

    for numero_linea, linea in enumerate(tsv_texto.splitlines(), start=1):
        if not linea.strip():
            continue

        partes = [p.strip() for p in linea.split("\t")]
        if len(partes) < 5:
            continue

        entrada, posicionamiento, posicion_tubo, protocolo, nombre_imagen = partes[:5]

        if not entrada or entrada.lower() == "entrada del paciente":
            continue

        clave = (
            normalizar_texto_archivo(entrada),
            normalizar_texto_archivo(posicionamiento),
            normalizar_texto_archivo(posicion_tubo),
            normalizar_texto_archivo(protocolo),
        )

        if not all(clave) or not nombre_imagen.strip():
            errores.append(f"Línea {numero_linea} incompleta")
            continue

        reglas[clave] = nombre_imagen.strip()
        filas_cargadas += 1

    return reglas, filas_cargadas, errores

REGLAS_RX_VALIDAS, FILAS_RX_CARGADAS, ERRORES_RX_CARGA = cargar_reglas_rx_desde_tsv(TOPORAMA_REGLAS_TSV)
TOPO_PROTOCOLOS = ["Seleccionar"] + sorted({clave[3].replace("_", " ") for clave in REGLAS_RX_VALIDAS.keys()})
TOPO_RX_DIAG = {"archivo_encontrado": True, "filas_cargadas": FILAS_RX_CARGADAS, "error": "; ".join(ERRORES_RX_CARGA[:5])}

def obtener_protocolos_filtrados(prefijo_estado="topo"):
    region_anatomica = st.session_state.get(f"{prefijo_estado}_region_anatomica", "Seleccionar")
    entrada = st.session_state.get(f"{prefijo_estado}_entrada_paciente", "Seleccionar")

    if region_anatomica in ["", None, "Seleccionar"]:
        return ["Seleccionar"]

    protocolos_base = MAPA_REGION_ANATOMICA_A_PROTOCOLOS.get(str(region_anatomica).lower(), ["Seleccionar"])

    if entrada in ["", None, "Seleccionar"]:
        return protocolos_base

    entrada_norm = normalizar_texto_archivo(entrada)
    protocolos_validos = ["Seleccionar"]

    for protocolo in protocolos_base:
        if protocolo == "Seleccionar":
            continue
        protocolo_norm = normalizar_texto_archivo(protocolo)
        existe = any(
            clave[0] == entrada_norm and clave[3] == protocolo_norm
            for clave in REGLAS_RX_VALIDAS.keys()
        )
        if existe:
            protocolos_validos.append(protocolo)

    return protocolos_validos


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
        "fangiotac_extremidad_superior_izquierdo_frontal": "angiotac_extremidad_superior_izquierdo_frontal",
        "angiotac_extremidad_superior_izquierdo_frontal": "angiotac_extremidad_superior_izquierda_frontal",
        "angiotac_extremidad_superior_izquierdo_lateral": "angiotac_extremidad_superior_izquierda_lateral",
        "angiotac_extremidad_superior_derecho_frontal": "angiotac_extremidad_superior_derecha_frontal",
        "angiotac_extremidad_superior_derecho_lateral": "angiotac_extremidad_superior_derecha_lateral",
        "angiotac_extremidad_inferior_frontal": "angiotac_extremidad_inferior_frontal",
        "angiotac_extremidad_inferior_lateral": "angiotac_extremidad_inferior_lateral",
    }
    nombre = correcciones.get(nombre, nombre)
    nombre = nombre.replace("__", "_").strip("_")
    return nombre


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


def obtener_nombre_imagen_rx(prefijo_estado="topo"):
    clave = obtener_clave_rx(prefijo_estado)
    if not clave:
        return None

    nombre = REGLAS_RX_VALIDAS.get(clave)
    if not nombre:
        return None

    return corregir_nombre_imagen(nombre)


def combinacion_rx_disponible(prefijo_estado="topo"):
    return obtener_clave_rx(prefijo_estado) in REGLAS_RX_VALIDAS


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
        "columna_frontal": ["columna_frontal", "columna_dorsal_frontal", "columna_lumbar_frontal"],
        "columna_lateral": ["columna_lateral", "columna_dorsal_lateral", "columna_lumbar_lateral"],
        "angiotac_extremidad_superior_derecha_frontal": ["angiotac_extremidad_superior_derecha_frontal", "angiotac_extremidad_superior_derecho_frontal"],
        "angiotac_extremidad_superior_derecha_lateral": ["angiotac_extremidad_superior_derecha_lateral", "angiotac_extremidad_superior_derecho_lateral"],
        "angiotac_extremidad_superior_izquierda_frontal": ["angiotac_extremidad_superior_izquierda_frontal", "angiotac_extremidad_superior_izquierdo_frontal", "fangiotac_extremidad_superior_izquierdo_frontal"],
        "angiotac_extremidad_superior_izquierda_lateral": ["angiotac_extremidad_superior_izquierda_lateral", "angiotac_extremidad_superior_izquierdo_lateral"],
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

def obtener_imagen_topograma_por_prefijo(prefijo_estado="topo"):
    if prefijo_estado == "topo":
        return obtener_imagen_topograma_generico("topo", "")
    return obtener_imagen_topograma_generico(prefijo_estado, prefijo_estado)


def obtener_imagen_rx_topograma(prefijo_estado="topo"):
    nombre_imagen = obtener_nombre_imagen_rx(prefijo_estado)
    if not nombre_imagen:
        return None
    return buscar_archivo_imagen_por_nombre(nombre_imagen)



def render_bloque_topograma(prefijo, titulo_visible, numero_boton):
    completo = topograma_completo(prefijo)
    rx_campos = rx_campos_completos(prefijo)
    rx_disponible = combinacion_rx_disponible(prefijo)

    st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
    st.markdown(f'<div class="titulo-bloque">{titulo_visible}</div>', unsafe_allow_html=True)

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
        persistent_selectbox("Entrada paciente", ["Seleccionar", "CABEZA PRIMERO", "PIES PRIMERO"], f"{prefijo}_entrada_paciente")
        persistent_selectbox("Posición del tubo", ["Seleccionar", "Arriba", "Abajo", "Derecha", "Izquierda"], f"{prefijo}_posicion_tubo")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="border-top:1px solid #8a8a8a; padding:0.3rem 0.55rem 0.3rem 0.55rem;">', unsafe_allow_html=True)
        persistent_selectbox("Posicionamiento", ["Seleccionar", "SUPINO", "PRONO", "LATERAL DERECHO", "LATERAL IZQUIERDO"], f"{prefijo}_posicionamiento")
        persistent_selectbox(
            "Posición de brazos / extremidades",
            ["Seleccionar", "BRAZOS ARRIBA", "BRAZOS ABAJO", "ELEVA BRAZO DERECHO", "ELEVA BRAZO IZQUIERDO",
             "FLEXIÓN EXTREMIDAD INFERIOR DERECHA", "FLEXIÓN EXTREMIDAD INFERIOR IZQUIERDA"],
            f"{prefijo}_posicion_brazos"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="border-top:1px solid #8a8a8a; padding:0.3rem 0.55rem 0.45rem 0.55rem;">', unsafe_allow_html=True)
        persistent_selectbox("Región anatómica", REGIONES_ANATOMICAS_TOPO, f"{prefijo}_region_anatomica")
        protocolos_filtrados = obtener_protocolos_filtrados(prefijo)
        persistent_selectbox("Protocolo", protocolos_filtrados, f"{prefijo}_region")

        mini1, mini2 = st.columns(2)
        with mini1:
            persistent_text_input("Inicio topograma", f"{prefijo}_inicio")
        with mini2:
            persistent_text_input("Término topograma", f"{prefijo}_termino")
        st.markdown('</div></div>', unsafe_allow_html=True)

    with layout_der:
        imagen_equipo = obtener_imagen_topograma_por_prefijo(prefijo)
        c1, c2, c3 = st.columns([0.22, 0.56, 0.22])
        with c2:
            if imagen_equipo is not None and imagen_equipo.exists():
                mostrar_imagen_actualizada(imagen_equipo, use_container_width=True)
            else:
                st.info(f"No se encontró la imagen de posicionamiento del {titulo_visible.lower()}.")

        st.markdown("<div style='height:3px;'></div>", unsafe_allow_html=True)

        c4, c5, c6 = st.columns([0.22, 0.56, 0.22])
        with c5:
            if st.session_state.get(f"{prefijo}_rx_iniciado", False):
                imagen_rx = obtener_imagen_rx_topograma(prefijo)
                if imagen_rx is not None and imagen_rx.exists():
                    mostrar_imagen_actualizada(imagen_rx, use_container_width=True)
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

    if rx_campos and not rx_disponible:
        st.warning("La combinación seleccionada no tiene imagen asociada, por eso Iniciar RX permanece desactivado.")

    btn1, btn2, btn3 = st.columns([1.5, 1.9, 1.5])
    with btn2:
        if st.button(
            f"Iniciar RX topograma {numero_boton}",
            key=f"btn_rx_{prefijo}",
            use_container_width=True,
            disabled=not (rx_campos and rx_disponible)
        ):
            st.session_state[f"{prefijo}_rx_iniciado"] = True
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    return completo, rx_disponible
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
            mostrar_imagen_actualizada(PORTADA_IMG, use_container_width=True)

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
            mostrar_imagen_actualizada(A_PRACTICAR_IMG, use_container_width=True)
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

    topo1_completo, topo1_rx_disponible = render_bloque_topograma("topo", "Topograma 1", 1)

    c_add1, c_add2, c_add3 = st.columns([2.4, 1.6, 2.4])
    with c_add2:
        if not st.session_state.get("mostrar_topo2", False):
            if st.button("Agregar otro topograma", key="agregar_topo2", use_container_width=True):
                st.session_state["mostrar_topo2"] = True
                st.rerun()

    topo2_completo = True
    topo2_rx_disponible = True

    if st.session_state.get("mostrar_topo2", False):
        e1, e2, e3 = st.columns([2.4, 1.6, 2.4])
        with e2:
            if st.button("Eliminar topograma 2", key="eliminar_topo2", use_container_width=True):
                st.session_state["mostrar_topo2"] = False
                for k, v in {
                    "topo2_entrada_paciente": "Seleccionar",
                    "topo2_posicionamiento": "Seleccionar",
                    "topo2_posicion_tubo": "Seleccionar",
                    "topo2_posicion_brazos": "Seleccionar",
                    "topo2_region_anatomica": "Seleccionar",
                    "topo2_region": "Seleccionar",
                    "topo2_inicio": "",
                    "topo2_termino": "",
                    "topo2_rx_iniciado": False,
                }.items():
                    st.session_state[k] = v
                    if f"_{k}" in st.session_state:
                        st.session_state[f"_{k}"] = v
                st.rerun()
        topo2_completo, topo2_rx_disponible = render_bloque_topograma("topo2", "Topograma 2", 2)

    sig1, sig2, sig3 = st.columns([2.2, 1.6, 2.2])
    with sig2:
        puede_avanzar = topo1_completo and topo1_rx_disponible and topo2_completo and topo2_rx_disponible
        if st.button("Siguiente", use_container_width=True, disabled=not puede_avanzar):
            ir_a("Adquisición")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("Resumen")
    st.markdown('<div class="bloque-resumen">', unsafe_allow_html=True)

    st.write("**Topograma 1**")
    st.write(f"**Entrada paciente:** {st.session_state['topo_entrada_paciente']}")
    st.write(f"**Posición del tubo:** {st.session_state['topo_posicion_tubo']}")
    st.write(f"**Posicionamiento:** {st.session_state['topo_posicionamiento']}")
    st.write(f"**Posición de brazos / extremidades:** {st.session_state['topo_posicion_brazos']}")
    st.write(f"**Región anatómica:** {st.session_state['topo_region_anatomica']}")
    st.write(f"**Protocolo:** {st.session_state['topo_region']}")
    st.write(f"**Inicio:** {st.session_state['topo_inicio']}")
    st.write(f"**Término:** {st.session_state['topo_termino']}")
    nombre_img_1 = obtener_nombre_imagen_rx("topo")
    st.write(f"**Imagen RX asociada:** {nombre_img_1 if nombre_img_1 else 'No disponible para esta combinación'}")

    if st.session_state.get("mostrar_topo2", False):
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("**Topograma 2**")
        st.write(f"**Entrada paciente:** {st.session_state['topo2_entrada_paciente']}")
        st.write(f"**Posición del tubo:** {st.session_state['topo2_posicion_tubo']}")
        st.write(f"**Posicionamiento:** {st.session_state['topo2_posicionamiento']}")
        st.write(f"**Posición de brazos / extremidades:** {st.session_state['topo2_posicion_brazos']}")
        st.write(f"**Región anatómica:** {st.session_state['topo2_region_anatomica']}")
        st.write(f"**Protocolo:** {st.session_state['topo2_region']}")
        st.write(f"**Inicio:** {st.session_state['topo2_inicio']}")
        st.write(f"**Término:** {st.session_state['topo2_termino']}")
        nombre_img_2 = obtener_nombre_imagen_rx("topo2")
        st.write(f"**Imagen RX asociada:** {nombre_img_2 if nombre_img_2 else 'No disponible para esta combinación'}")

    st.markdown('</div>', unsafe_allow_html=True)

elif seccion == "Adquisición":
    st.header("Adquisición")

    colv1, colv2, colv3 = st.columns([1, 6, 1])
    with colv1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_anterior(); st.rerun()

    st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-bloque">Topogramas seleccionados y límites de barrido</div>', unsafe_allow_html=True)
    st.caption("Ajusta de forma interactiva el límite superior e inferior en cada topograma.")

    mostrar_topo2 = st.session_state.get("mostrar_topo2", False)
    imagen_topo_1 = obtener_imagen_rx_topograma("topo")
    imagen_topo_2 = obtener_imagen_rx_topograma("topo2") if mostrar_topo2 else None

    if mostrar_topo2:
        topo_col1, topo_col2 = st.columns(2)
        bloques_topo = [
            (topo_col1, "topo", "Topograma 1", imagen_topo_1, "adq_topo1_limite_superior", "adq_topo1_limite_inferior"),
            (topo_col2, "topo2", "Topograma 2", imagen_topo_2, "adq_topo2_limite_superior", "adq_topo2_limite_inferior"),
        ]
    else:
        margen1, topo_col1, margen2 = st.columns([1.2, 1.6, 1.2])
        bloques_topo = [
            (topo_col1, "topo", "Topograma 1", imagen_topo_1, "adq_topo1_limite_superior", "adq_topo1_limite_inferior"),
        ]

    for columna_topo, prefijo_topo, titulo_topo, imagen_topo, key_sup, key_inf in bloques_topo:
        with columna_topo:
            st.markdown(
                f"""
                <div style="font-weight:700; color:white; margin-bottom:0.35rem; text-align:center;">{titulo_topo}</div>
                """,
                unsafe_allow_html=True
            )
            if imagen_topo is not None and imagen_topo.exists():
                limite_superior = st.slider(
                    "Inicio",
                    min_value=0,
                    max_value=100,
                    value=int(st.session_state.get(key_sup, 15)),
                    key=key_sup,
                )
                limite_inferior = st.slider(
                    "Fin",
                    min_value=0,
                    max_value=100,
                    value=int(st.session_state.get(key_inf, 85)),
                    key=key_inf,
                )

                if limite_superior >= limite_inferior:
                    st.warning("El límite superior debe quedar por encima del inferior.")
                imagen_con_limites = crear_topograma_con_limites(imagen_topo, limite_superior, limite_inferior)
                delay_bolus_activo = st.session_state.get("adq_delay") in ["Bolus tracking", "Bolus test"]
                if imagen_con_limites is not None:
                    if delay_bolus_activo:
                        render_linea_corte_bolus_interactiva_html(imagen_con_limites, key_suffix=f"{prefijo_topo}_bolus")
                    else:
                        st.image(imagen_con_limites, width=260)
                else:
                    try:
                        imagen_base = ajustar_imagen_a_lienzo_uniforme(Image.open(imagen_topo).convert("RGB"))
                        if delay_bolus_activo:
                            render_linea_corte_bolus_interactiva_html(imagen_base, key_suffix=f"{prefijo_topo}_bolus")
                        else:
                            st.image(imagen_base, width=260)
                    except Exception:
                        if delay_bolus_activo and imagen_topo is not None and imagen_topo.exists():
                            render_linea_corte_bolus_interactiva_html(imagen_topo, key_suffix=f"{prefijo_topo}_bolus")
                        else:
                            mostrar_imagen_actualizada(imagen_topo, width=260)
            else:
                st.markdown(
                    """
                    <div style="
                        min-height:160px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        border:1px solid #7a7a7a;
                        border-radius:14px;
                        background-color:#4a4a4a;
                        color:white;
                        font-weight:600;
                        text-align:center;
                        padding:0.45rem;
                    ">
                        No se encontró la imagen del topograma seleccionado
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.caption(
                f"{st.session_state.get(f'{prefijo_topo}_region', 'Seleccionar')} · "
                f"{st.session_state.get(f'{prefijo_topo}_posicionamiento', 'Seleccionar')} · "
                f"tubo {str(st.session_state.get(f'{prefijo_topo}_posicion_tubo', 'Seleccionar')).lower()}"
            )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="bloque-seccion">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-bloque">Parámetros de adquisición</div>', unsafe_allow_html=True)

    opciones_delay = [
        "Seleccionar", "Bolus tracking", "Bolus test", "0 sg", "5 sg", "10 sg", "15 sg", "20 sg",
        "25 sg", "30 sg", "35 sg", "40 sg", "45 sg", "50 sg", "55 sg", "1 min", "2 min", "3 min",
        "4 min", "5 min", "6 min", "7 min", "8 min", "9 min", "10 min", "11 min", "12 min",
        "13 min", "14 min", "15 min", "16 min", "17 min", "18 min", "19 min", "20 min"
    ]
    opciones_pitch = ["Seleccionar", "0,1", "0,2", "0,3", "0,4", "0,5", "0,6", "0,7", "0,8", "0,9", "1", "1,1", "1,2", "1,3", "1,4", "1,5"]
    opciones_kv_referencia = ["Seleccionar", "70", "80", "100", "110", "120", "130", "140"]
    opciones_mas_referencia = ["Seleccionar", "50", "100", "150", "200", "250", "300", "350", "400", "450", "500", "550", "600"]

    tipo_exploracion = st.session_state.get("adq_tipo_exploracion", "Seleccionar")
    if tipo_exploracion == "Helicoidal":
        opciones_matriz = ["Seleccionar", "64 x 0,625", "32 x 1,25", "16 x 0,625"]
    elif tipo_exploracion == "Secuencial":
        opciones_matriz = ["Seleccionar", "2 x 0,625", "1 x 1,25", "32 x 1,25", "64 x 0,625"]
    else:
        opciones_matriz = ["Seleccionar"]

    if st.session_state.get("adq_matriz_detectores") not in opciones_matriz:
        st.session_state["adq_matriz_detectores"] = "Seleccionar"
        st.session_state["_adq_matriz_detectores"] = "Seleccionar"

    col1, col2, col3 = st.columns(3)

    with col1:
        persistent_selectbox(
            "Fase de adquisición",
            ["Seleccionar", "Sin contraste", "Angiográfica", "Arterial", "Venosa o portal", "Tardía"],
            "adq_fase_adquisicion"
        )
        persistent_selectbox(
            "Instrucción de voz",
            ["Seleccionar", "Ninguna", "Inspiración", "Espiración", "No trague", "No respire"],
            "adq_instruccion_voz"
        )
        persistent_selectbox("Delay", opciones_delay, "adq_delay")
        persistent_selectbox(
            "Tipo de exploración",
            ["Seleccionar", "Helicoidal", "Secuencial"],
            "adq_tipo_exploracion"
        )
        persistent_selectbox("Matriz de detectores", opciones_matriz, "adq_matriz_detectores")

    with col2:
        persistent_selectbox(
            "Giro del tubo",
            ["Seleccionar", "0,33 sg", "0,5 sg", "1 sg", "1,5 sg"],
            "adq_giro_tubo"
        )
        if tipo_exploracion == "Helicoidal":
            persistent_selectbox("Pitch", opciones_pitch, "adq_pitch")
        else:
            st.session_state["adq_pitch"] = "Seleccionar"
            st.session_state["_adq_pitch"] = "Seleccionar"
            st.markdown("<div style='height: 74px;'></div>", unsafe_allow_html=True)

        persistent_selectbox(
            "Modulación de corriente",
            ["Seleccionar", "Si", "No"],
            "adq_modulacion_corriente"
        )

        modulacion = st.session_state.get("adq_modulacion_corriente", "Seleccionar")
        if modulacion == "Si":
            persistent_selectbox("kV referencia", opciones_kv_referencia, "adq_kv_referencia")
            persistent_selectbox("mAs referencia", opciones_mas_referencia, "adq_mas_referencia")

            st.session_state["adq_kv_manual"] = 120
            st.session_state["adq_mas_manual"] = 100
            st.session_state["_adq_kv_manual"] = 120
            st.session_state["_adq_mas_manual"] = 100
        elif modulacion == "No":
            persistent_number_input("kV", "adq_kv_manual", min_value=1, max_value=200, step=1)
            persistent_number_input("mAs", "adq_mas_manual", min_value=1, max_value=1000, step=1)

            st.session_state["adq_kv_referencia"] = "Seleccionar"
            st.session_state["adq_mas_referencia"] = "Seleccionar"
            st.session_state["_adq_kv_referencia"] = "Seleccionar"
            st.session_state["_adq_mas_referencia"] = "Seleccionar"
        else:
            st.session_state["adq_kv_referencia"] = "Seleccionar"
            st.session_state["adq_mas_referencia"] = "Seleccionar"
            st.session_state["_adq_kv_referencia"] = "Seleccionar"
            st.session_state["_adq_mas_referencia"] = "Seleccionar"
            st.markdown("<div style='height: 148px;'></div>", unsafe_allow_html=True)

    with col3:
        persistent_selectbox(
            "Espesor (mm)",
            ["Seleccionar", "0,625", "1,25", "2,5", "5"],
            "adq_espesor"
        )
        persistent_selectbox(
            "SFOV",
            ["Seleccionar", "Small 200", "Head 350", "Large 500"],
            "adq_sfov"
        )
        persistent_text_input("Colimación (mm)", "adq_colimacion")
        persistent_text_input("Inicio de adquisición", "adq_inicio_adquisicion")
        persistent_text_input("Fin de adquisición", "adq_fin_adquisicion")
        st.session_state["_adq_kv_referencia"] = "Seleccionar"
        st.session_state["_adq_mas_referencia"] = "Seleccionar"

    if st.session_state.get("adq_delay") in ["Bolus tracking", "Bolus test"]:
        st.markdown("<div style='height:0.4rem;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='titulo-bloque'>ROI PARA BOLUS TEST / BOLUS TRACKING</div>", unsafe_allow_html=True)
        archivo_roi = st.file_uploader(
            "SUBIR IMAGEN PARA ROI",
            type=["png", "jpg", "jpeg"],
            key="adq_roi_imagen_bolus"
        )
        if archivo_roi is not None:
            render_roi_interactiva_html(archivo_roi, key_suffix="adq_bolus")

    st.markdown('</div>', unsafe_allow_html=True)

    modulacion_ok = False
    if modulacion == "Si":
        modulacion_ok = all([
            seleccion_completa(st.session_state["adq_kv_referencia"]),
            seleccion_completa(st.session_state["adq_mas_referencia"]),
        ])
    elif modulacion == "No":
        modulacion_ok = all([
            st.session_state["adq_kv_manual"] is not None,
            st.session_state["adq_mas_manual"] is not None,
        ])

    pitch_ok = True if tipo_exploracion != "Helicoidal" else seleccion_completa(st.session_state["adq_pitch"])

    adquisicion_completa = all([
        seleccion_completa(st.session_state["adq_fase_adquisicion"]),
        seleccion_completa(st.session_state["adq_instruccion_voz"]),
        seleccion_completa(st.session_state["adq_delay"]),
        seleccion_completa(st.session_state["adq_tipo_exploracion"]),
        seleccion_completa(st.session_state["adq_espesor"]),
        seleccion_completa(st.session_state["adq_matriz_detectores"]),
        texto_completo(st.session_state["adq_colimacion"]),
        texto_completo(st.session_state["adq_inicio_adquisicion"]),
        texto_completo(st.session_state["adq_fin_adquisicion"]),
        seleccion_completa(st.session_state["adq_giro_tubo"]),
        seleccion_completa(st.session_state["adq_sfov"]),
        seleccion_completa(st.session_state["adq_modulacion_corriente"]),
        modulacion_ok,
        pitch_ok,
    ])

    st.divider()
    st.subheader("Resumen")
    st.markdown('<div class="bloque-resumen">', unsafe_allow_html=True)
    st.write(f"**Fase de adquisición:** {st.session_state['adq_fase_adquisicion']}")
    st.write(f"**Instrucción de voz:** {st.session_state['adq_instruccion_voz']}")
    st.write(f"**Delay:** {st.session_state['adq_delay']}")
    st.write(f"**Tipo de exploración:** {st.session_state['adq_tipo_exploracion']}")
    st.write(f"**Espesor (mm):** {st.session_state['adq_espesor']}")
    st.write(f"**Matriz de detectores:** {st.session_state['adq_matriz_detectores']}")
    st.write(f"**Colimación (mm):** {st.session_state['adq_colimacion']}")
    st.write(f"**Inicio de adquisición:** {st.session_state['adq_inicio_adquisicion']}")
    st.write(f"**Fin de adquisición:** {st.session_state['adq_fin_adquisicion']}")
    st.write(f"**Giro del tubo:** {st.session_state['adq_giro_tubo']}")
    st.write(f"**SFOV:** {st.session_state['adq_sfov']}")
    if tipo_exploracion == "Helicoidal":
        st.write(f"**Pitch:** {st.session_state['adq_pitch']}")
    st.write(f"**Modulación de corriente:** {st.session_state['adq_modulacion_corriente']}")
    if modulacion == "Si":
        st.write(f"**kV referencia:** {st.session_state['adq_kv_referencia']}")
        st.write(f"**mAs referencia:** {st.session_state['adq_mas_referencia']}")
    elif modulacion == "No":
        st.write(f"**kV:** {st.session_state['adq_kv_manual']}")
        st.write(f"**mAs:** {st.session_state['adq_mas_manual']}")
    st.write(f"**Topograma 1:** inicio {st.session_state['adq_topo1_limite_superior']}% · fin {st.session_state['adq_topo1_limite_inferior']}%")
    if mostrar_topo2:
        st.write(f"**Topograma 2:** inicio {st.session_state['adq_topo2_limite_superior']}% · fin {st.session_state['adq_topo2_limite_inferior']}%")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.5, 2, 1.5])
    with c1:
        if st.button("⬅ Volver a Topograma", use_container_width=True):
            ir_a("Topograma"); st.rerun()
    with c3:
        if st.button("Siguiente: Reconstrucción ➡", use_container_width=True, disabled=not adquisicion_completa):
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
