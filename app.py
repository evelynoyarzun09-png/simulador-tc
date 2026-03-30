import streamlit as st
from pathlib import Path
from datetime import date

st.set_page_config(page_title="Simulador TC", layout="wide")

# -------------------------
# RUTA IMÁGENES
# -------------------------
BASE_DIR = Path(__file__).parent
PORTADA_IMG = BASE_DIR / "tomografo_portada.png"
PACIENTE_IMG = BASE_DIR / "paciente.png"

# -------------------------
# ESTADO
# -------------------------
if "seccion" not in st.session_state:
    st.session_state.seccion = "Portada"

seccion = st.session_state.seccion

# -------------------------
# ESTILOS
# -------------------------
st.markdown("""
<style>
.boton-inferior-derecha {
    position: fixed;
    right: 2rem;
    bottom: 1.5rem;
}
.portada {
    background-color: black;
    padding: 2rem;
    border-radius: 15px;
}
.titulo {
    text-align: center;
    font-size: 2.5rem;
    color: #20cfcf;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# FUNCIONES
# -------------------------
def ir_a_practicar():
    st.session_state.seccion = "A Practicar"

def volver():
    st.session_state.seccion = "A Practicar"

# -------------------------
# PORTADA
# -------------------------
if seccion == "Portada":

    st.markdown('<div class="portada">', unsafe_allow_html=True)
    st.markdown('<div class="titulo">Tomografía Computada Aplicada</div>', unsafe_allow_html=True)

    if PORTADA_IMG.exists():
        st.image(PORTADA_IMG, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="boton-inferior-derecha">', unsafe_allow_html=True)
    if st.button("Ir a A Practicar"):
        ir_a_practicar()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# MENU PRINCIPAL
# -------------------------
elif seccion == "A Practicar":

    st.title("Simulador TC")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Preparación de paciente", use_container_width=True):
            st.session_state.seccion = "Preparación de paciente"
            st.rerun()

# -------------------------
# PREPARACIÓN DE PACIENTE (REPLICADO DEL EXCEL)
# -------------------------
elif seccion == "Preparación de paciente":

    if st.button("⬅ Volver"):
        volver()
        st.rerun()

    st.header("Preparación de paciente")

    col1, col2 = st.columns([2,1])

    # -------------------------
    # DATOS PACIENTE
    # -------------------------
    with col1:
        nombres = st.text_input("Nombres")
        apellidos = st.text_input("Apellidos")

        fecha_nac = st.date_input("Fecha de nacimiento", value=date(2000,1,1))

        # cálculo edad automático
        edad = date.today().year - fecha_nac.year
        st.write(f"Edad: {edad} años")

        examen = st.selectbox(
            "Examen",
            [
                "TC Cerebro",
                "TC Tórax",
                "TC Abdomen y pelvis",
                "AngioTC",
                "Otro"
            ]
        )

        peso = st.number_input("Peso (kg)", min_value=1.0, value=70.0)

        embarazo = st.selectbox("Embarazo", ["No", "Sí"])
        creatinina = st.selectbox("Creatinina evaluada", ["Sí", "No"])

    # -------------------------
    # IMAGEN (como Excel)
    # -------------------------
    with col2:
        st.subheader("Paciente")

        if PACIENTE_IMG.exists():
            st.image(PACIENTE_IMG, use_container_width=True)
        else:
            st.info("Agrega una imagen llamada 'paciente.png'")

    # -------------------------
    # RESUMEN
    # -------------------------
    st.divider()
    st.subheader("Resumen")

    st.write(f"Paciente: {nombres} {apellidos}")
    st.write(f"Edad: {edad} años")
    st.write(f"Examen: {examen}")
    st.write(f"Peso: {peso} kg")
    st.write(f"Embarazo: {embarazo}")
    st.write(f"Creatinina: {creatinina}")
