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
    st.metric("DLP", ctdi * largo)
