
    st.set_page_config(
        page_title="Your Page Title",
        page_icon="✅",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Specify the static directory
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url('static/background_image.jpg');
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

