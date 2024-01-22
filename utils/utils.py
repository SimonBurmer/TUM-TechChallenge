import streamlit as st
import base64
from streamlit.components.v1 import html

# adding UI logos
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

# helper function to switch pages
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

def sidebar_content():
    st.sidebar.header("📖 Last Cases")
    st.sidebar.text("- City Senior Court")
    st.sidebar.text("- Aggrevated assult charges")
    st.sidebar.text("- Surveilance footage")
    st.sidebar.text("- Pretrial hearings")
    st.sidebar.text("")
    st.sidebar.header("❤️ Liked Cases")
    st.sidebar.text("- Surveilance footage")
    st.sidebar.text("- Pretrial hearings")