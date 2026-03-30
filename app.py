import streamlit as st
from pathlib import Path
from datetime import date

st.set_page_config(page_title="Simulador TC", layout="wide")

# -------------------------
# RUTA DE IMÁGENES
# -------------------------
BASE_DIR = Path(__file__).parent
PORTADA_IMG = BASE_DIR / "tomografo_portada.png"
PACIENTE_IMG = BASE_DIR / "paciente.png"

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
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.boton-inferior-derecha {
    position: fixed;
    right: 2rem;
    bottom: 1.5rem;
    z-index: 999;
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
    padding: 1.2rem 1.2rem 5rem 1.2rem;
    border-radius: 18px;
}
div.stButton > button {
    border-radius: 12px;
    font-weight: 600;
}
.bloque-resumen {
    background-color: #f7f7f7;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    border: 1px solid #e5e5e5;
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
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        if st.button("⬅ Volver", use_container_width=True):
            volver_menu()
            st.rerun()

    st.header("Preparación de paciente")

    col_form, col_img = st.columns([2.2, 1])

    with col_form:
        st.subheader("Datos del paciente")

        nombres = st.text_input("Nombres")
        apellidos = st.text_input("Apellidos")
        fecha_nac = st.date_input("Fecha de nacimiento", value=date(2000, 1, 1))

        hoy = date.today()
        edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        st.write(f"**Edad:** {edad} años")

        examen = st.text_input("Examen")
        peso = st.number_input("Peso (kg)", min_value=0.0, value=70.0, step=0.1)

        embarazo = st.selectbox(
            "Embarazo",
            ["SI", "NO", "NO APLICA"]
        )

        creatinina = st.selectbox(
            "Creatinina",
            ["SI", "NO"]
        )

        st.subheader("Preparación para contraste")

        medio_contraste_ev = st.selectbox(
            "Medio de contraste EV",
            ["SI", "NO", "NO APLICA"]
        )

        via_venosa = st.selectbox(
            "Vía venosa",
            ["24G", "22G", "20G", "18G", "16G", "CVC", "NO APLICA"]
        )

        cantidad_contraste = st.selectbox(
            "Cantidad de contraste (ml)",
            [
                "10 cc", "20 cc", "30 cc", "40 cc", "50 cc", "60 cc", "70 cc", "80 cc",
                "90 cc", "100 cc", "110 cc", "120 cc", "130 cc", "140 cc", "150 cc",
                "160 cc", "170 cc", "180 cc", "190 cc", "200 cc"
            ]
        )

        metodo_inyeccion = st.selectbox(
            "Método de inyección",
            ["JERINGA INYECTORA", "JERINGA MANUAL", "NO APLICA"]
        )

        medio_contraste_oral = st.selectbox(
            "Medio de contraste oral",
            ["NO APLICA", "AGUA", "AIRE", "CONTRASTE POSITIVO"]
        )

        st.subheader("Posicionamiento del paciente")

        entrada_paciente = st.selectbox(
            "Entrada paciente",
            ["CABEZA PRIMERO", "PIES PRIMERO"]
        )

        posicionamiento = st.selectbox(
            "Posicionamiento",
            ["SUPINO", "PRONO", "LATERAL DERECHO", "LATERAL IZQUIERDO"]
        )

        posicion_brazos = st.selectbox(
            "Posición de brazos / extremidades",
            [
                "BRAZOS ARRIBA",
                "BRAZOS ABAJO",
                "ELEVA BRAZO DERECHO",
                "ELEVA BRAZO IZQUIERDO",
                "FLEXIÓN EXTREMIDAD INFERIOR DERECHA",
                "FLEXIÓN EXTREMIDAD INFERIOR IZQUIERDA"
            ]
        )

    with col_img:
        st.subheader("Imagen")

        if PACIENTE_IMG.exists():
            st.image(str(PACIENTE_IMG), use_container_width=True)
        else:
            st.info("Si quieres mostrar una imagen aquí, guarda un archivo llamado 'paciente.png' en la misma carpeta del app.py.")

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
    st.write(f"**Vía venosa:** {via_venosa}")
    st.write(f"**Cantidad de contraste:** {cantidad_contraste}")
    st.write(f"**Método de inyección:** {metodo_inyeccion}")
    st.write(f"**Medio de contraste oral:** {medio_contraste_oral}")
    st.write(f"**Entrada del paciente:** {entrada_paciente}")
    st.write(f"**Posicionamiento:** {posicionamiento}")
    st.write(f"**Posición de brazos / extremidades:** {posicion_brazos}")
    st.markdown('</div>', unsafe_allow_html=True)

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
