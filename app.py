if "seccion" not in st.session_state:
    st.session_state.seccion = "A Practicar"

seccion = st.session_state.seccion
    st.write("Selecciona una etapa:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Preparación paciente"):
            st.session_state.seccion = "Preparación de paciente"

        if st.button("Jeringa inyectora"):
            st.session_state.seccion = "Jeringa inyectora"

        if st.button("Topograma"):
            st.session_state.seccion = "Topograma"

    with col2:
        if st.button("Adquisición"):
            st.session_state.seccion = "Adquisición"

        if st.button("Reconstrucción"):
            st.session_state.seccion = "Reconstrucción"

        if st.button("Reformación"):
            st.session_state.seccion = "Reformación"

    with col3:
        if st.button("Medida paciente"):
            st.session_state.seccion = "Medida paciente"

        if st.button("Cálculos"):
            st.session_state.seccion = "Cálculos"
