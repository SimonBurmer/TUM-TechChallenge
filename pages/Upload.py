import streamlit as st


def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.imgur.com/At86a7L.png);
                background-repeat: no-repeat;
                background-size:30%;
                background-position: 100px 20px;
            }
            .css-ng1t4o {{width: 10rem;}}
        </style>
        """,
        unsafe_allow_html=True,
    )

def upload():
        
    st.set_page_config(
        page_title="LegalLens AI",
        page_icon="🔍",
        layout="wide",
        menu_items={"Get help": None, "Report a bug": None},
    )
    st.sidebar.header("📖 Last Cases")
    st.sidebar.text("- City Senior Court")
    st.sidebar.text("- Aggrevated assult charges")
    st.sidebar.text("- Surveilance footage")
    st.sidebar.text("- Pretrial hearings")
    st.sidebar.text("")
    st.sidebar.header("❤️ Liked Cases")
    st.sidebar.text("- Surveilance footage")
    st.sidebar.text("- Pretrial hearings")


    add_logo()

    st.title("📥 Upload & Connect")

    st.markdown(
    """
    Upload your documents or connect to your database / ERP system.
    """
    )
    st.markdown("""---""")


upload()


# Create two columns
col1, col2 = st.columns(2)

# Button in column 1
with col1:
    st.subheader("Upload new cases:")
    st.write("Securely upload your legal documents here to ensure they are organized and easily retrievable. Supported formats include .pdf, .docx, and .txt files.")
    button_text1 = st.button("Upload documents")


# Button in column 2
with col2:
    st.subheader("Connect to CRM system:")
    st.write("Connect to your CRM system to automatically retrieve documents and case information. Foster better client relationships through seamless access to case histories, contact information, and tailored communication logs directly from our platform. Our integration allows for a synchronized workflow, ensuring that client data is up-to-date and aligned with case proceedings.")
    button_text2 = st.button("Connect now")


