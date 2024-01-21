import streamlit as st
import json
from streamlit_modal import Modal
import base64
from streamlit.components.v1 import html

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)


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

def pdf():
    add_logo()

    filename = ""

    try:
        with open("filename.txt", "r") as f:
            filename = f.read()
            f.close()
    except IOError:
        filename = ""

    if filename == "":
        st.header("Please type in your query and retrieve documents in retrieval section")
    elif filename != "":
        col1, col2 = st.columns((2.5, 1.5))

        with open("./data/files/" + filename,"rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<p align="center"><iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0" width="100%" height="1000" type="application/pdf"></iframe></p>'
        # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(ui_width)} height={str(ui_width*4/3)} type="application/pdf"></iframe>'
        col1.markdown(pdf_display, unsafe_allow_html=True)

        col2.header("**Applied Laws:**")
        col2.write("**German Civil Code (Bürgerliches Gesetzbuch - BGB)**")
        col2.write("- [§611a]() Employment Contract")
        col2.write("    - [§622]() Notice periods for employment contracts")
        col2.text("")

        col2.write("**Works Constitution Act (Betriebsverfassungsgesetz - BetrVG)**")
        col2.markdown("- [§102]() Involvement of the Works Council in Termination Procedures")
        col2.text("")
        col2.text("")
        col2.text("")

        col2.header("**Citations & References:**")

        col2.markdown("- Employment at Will Doctrine, Restatement (Second) of Contracts, [§205]()")
        col2.markdown("- Smith v. XYZ Corp., 123 F.3d 456 (Court of Appeals, 2020)")
        col2.markdown("- Fair Labor Standards Act, 29 U.S.C. § 201 et seq")

def back():
    nav_page("Retrieval")
        

def app() -> None:
    """Streamlit entrypoint for PDF Summarize frontend"""
    # config
    st.set_page_config(
        page_title="LegalLens AI",
        page_icon="🔍",
        layout="wide",
        menu_items={"Get help": None, "Report a bug": None},
    )
    
    st.session_state["filename"] = ""

    st.button(
                    "Back to retrieval", on_click=back, 
                )

    pdf()

    # page_names_to_funcs = {
    #     "Retrieval": retrieval,
    #     "PDF Details": pdf,
    # }

    # selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
    # page_names_to_funcs[selected_page]()


    st.sidebar.header("📖 Last Cases")
    st.sidebar.text("- City Senior Court")
    st.sidebar.text("- Aggrevated assult charges")
    st.sidebar.text("- Surveilance footage")
    st.sidebar.text("- Pretrial hearings")
    st.sidebar.text("")
    st.sidebar.header("❤️ Liked Cases")
    st.sidebar.text("- Surveilance footage")
    st.sidebar.text("- Pretrial hearings")


    


if __name__ == "__main__":
    # run as a script to test streamlit app locally
    app()
