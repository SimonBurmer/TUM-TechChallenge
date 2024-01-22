import streamlit as st
from utils.utils import add_logo, sidebar_content

def app() -> None:
    st.set_page_config(
        page_title="LegalLens AI",
        page_icon="🔍",
        layout="wide",
        menu_items={"Get help": None, "Report a bug": None},
    )
    
    sidebar_content()

    add_logo()

    st.title("📥 Upload & Connect")

    st.markdown(
    """
    Upload your documents or connect to your database / ERP system.
    """
    )
    st.markdown("""---""")

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


    st.write("")
    st.write("")
    st.write("")

    html_code = """
        <div style="display: flex; width: 75%; align-items: center; text-align: center;">
            <img src="https://i.imgur.com/jBZdklp.png" alt="Mobile App" style="width: 30%; margin-right: 20px;">
            <div>
                <h1>Download</h1>
                <h2>LegalLens AI mobile 🚀</h2>
                <h3>Scan and Upload Documents on the Go!</h3>
                <p>Discover the power of convenience at your fingertips! Download our user-friendly mobile app today to effortlessly scan and upload your important documents anytime, anywhere. Whether it's legal documents, contracts, or handwritten notes, our app transforms your smartphone into a portable scanner, making document management a breeze.</p>
                <img src="https://i.imgur.com/HnBVGBO.png" alt="Google Play" style="width: 30%; margin-right: 20px;">
                <img src="https://i.imgur.com/Oca2pWa.png" alt="App Store" style="width: 30%;">
            </div>
        </div>
    """

    col1, col2, col3 = st.columns((1,6,1))
    col2.markdown(html_code, unsafe_allow_html=True)


if __name__ == "__main__":
    # run as a script to test streamlit app locally
    app()