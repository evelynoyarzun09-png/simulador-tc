import streamlit as st

st.set_page_config(page_title="Tomografía Computada Aplicada", layout="wide")

# -------------------------
# ESTADO
# -------------------------
if "seccion" not in st.session_state:
    st.session_state.seccion = "Portada"

seccion = st.session_state.seccion

# -------------------------
# ESTILO
# -------------------------
st.markdown("""
<style>
.stApp {
    background-color: black;
}

h1, h2, h3, h4, h5, h6, p, label {
    color: #40E0D0;
}

.stButton > button {
    background-color: #40E0D0;
    color: black !important;
    border-radius: 10px;
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

    st.markdown(
        "<h1 style='text-align:center;'>Tomografía Computada Aplicada</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>Simulador interactivo de TC</p>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        if st.button("Ir a practicar", use_container_width=True):
            ir_a_practicar()
            st.rerun()

# -------------------------
# MENÚ
# -------------------------
elif seccion == "A Practicar":

    st.header("A Practicar")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Preparación de paciente"):
            st.session_state.seccion = "Preparación"
            st.rerun()

        if st.button("Jeringa inyectora"):
            st.session_state.seccion = "Jeringa"
            st.rerun()

    with col2:
        if st.button("Topograma"):
            st.session_state.seccion = "Topograma"
            st.rerun()

        if st.button("Adquisición"):
            st.session_state.seccion = "Adquisicion"
            st.rerun()

    with col3:
        if st.button("Reconstrucción"):
            st.session_state.seccion = "Reconstruccion"
            st.rerun()

        if st.button("Cálculos"):
            st.session_state.seccion = "Calculos"
            st.rerun()

# -------------------------
# SECCIONES
# -------------------------
elif seccion == "Preparación":
    if st.button("⬅ Volver"):
        volver()
        st.rerun()

    st.header("Preparación de paciente")
    st.selectbox("Ayuno", ["Sí", "No"])

elif seccion == "Jeringa":
    if st.button("⬅ Volver"):
        volver()
        st.rerun()

    st.header("Jeringa inyectora")
    st.number_input("Flujo", value=3.5)

elif seccion == "Topograma":
    if st.button("⬅ Volver"):
        volver()
        st.rerun()

    st.header("Topograma")
    st.selectbox("Región", ["Cabeza", "Tórax", "Abdomen"])

elif seccion == "Adquisicion":
    if st.button("⬅ Volver"):
        volver()
        st.rerun()

    st.header("Adquisición")
    st.selectbox("kVp", [80,100,120])

elif seccion == "Reconstruccion":
    if st.button("⬅ Volver"):
        volver()
        st.rerun()

    st.header("Reconstrucción")
    st.selectbox("Kernel", ["Blando", "Óseo"])

elif seccion == "Calculos":
    if st.button("⬅ Volver"):
        volver()
        st.rerun()

    st.header("Cálculos")
    ctdi = st.number_input("CTDI", value=10.0)
    largo = st.number_input("Longitud", value=30.0)
    st.metric("DLP", ctdi * largo)    font-size: 16px;
    padding: 12px;
}

.stButton > button:hover {
    background-color: #2ec4b6;
    color: black !important;
}

/* PORTADA */
.portada-container {
    height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}

.portada-titulo {
    font-size: 4rem;
    font-weight: 800;
    color: #40E0D0;
}

.portada-subtitulo {
    font-size: 1.3rem;
    opacity: 0.9;
}

/* BOTÓN ESQUINA */
.boton-esquina {
    position: fixed;
    bottom: 30px;
    right: 30px;
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
    if st.button("Ir a practicar"):
        ir_a_practicar()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# -------------------------
# MENÚ PRINCIPAL
# -------------------------
elif seccion == "A Practicar":

    st.header("A Practicar")

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


# -------------------------
# PLANTILLA SECCIONES
# -------------------------
def boton_volver():
    if st.button("⬅ Volver"):
        volver_menu()
        st.rerun()


# -------------------------
# SECCIONES
# -------------------------
elif seccion == "Preparación de paciente":
    boton_volver()
    st.header("Preparación de paciente")
    st.selectbox("Ayuno", ["Sí", "No"])


elif seccion == "Jeringa inyectora":
    boton_volver()
    st.header("Jeringa inyectora")
    st.number_input("Flujo (mL/s)", value=3.5)


elif seccion == "Topograma":
    boton_volver()
    st.header("Topograma")
    st.selectbox("Región", ["Cabeza", "Tórax", "Abdomen"])


elif seccion == "Adquisición":
    boton_volver()
    st.header("Adquisición")
    st.selectbox("kVp", [80, 100, 120, 140])


elif seccion == "Reconstrucción":
    boton_volver()
    st.header("Reconstrucción")
    st.selectbox("Kernel", ["Blando", "Óseo"])


elif seccion == "Reformación":
    boton_volver()
    st.header("Reformación")
    st.selectbox("Tipo", ["MPR", "MIP", "VR"])


elif seccion == "Medida paciente":
    boton_volver()
    st.header("Medida paciente")
    st.number_input("Diámetro AP", value=25.0)


elif seccion == "Cálculos":
    boton_volver()
    st.header("Cálculos")
    ctdi = st.number_input("CTDIvol", value=10.0)
    largo = st.number_input("Longitud", value=30.0)
    st.metric("DLP", ctdi * largo)
