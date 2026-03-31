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
        proyeccion = st.selectbox("Plano", ["Seleccionar", "AP", "Lateral", "AP y lateral"], index=0)

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
