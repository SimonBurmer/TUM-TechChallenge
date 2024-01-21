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

def retrieval():
    add_logo()

    st.title("📤 Retrieval")

    st.markdown(
        """
    Your chatAI based search will list the documents you are looking for.
    """
    )
    st.markdown("""---""")

    

    if history := st.session_state.get("history"):
        history_display_container(history)
    else:
        st.session_state["history"] = list()
        retrieval_form_container()


def on_more_click(show_more, idx):
    show_more[idx] = True

def on_more_case_click(show_more_cases, idx):
    show_more_cases[idx] = True

def on_less_case_click(show_more_cases, idx):
    show_more_cases[idx] = False


def on_less_click(show_more, idx):
    show_more[idx] = False

def on_view_file(filename):
    f = open("filename.txt", "w")
    f.write(filename)
    f.close()
    nav_page("View_PDF")



def retrieval_form_container() -> None:
    form = st.form(key="retrieval_query")
    rag_query = form.text_area(
        "Case Retrieval Query", value="Please describe the cases you are interested in here.", height=200,
    )

    form.selectbox('Select a range of the time of files.', ("All", "Yesterday", "Last 7 days", "last 30 days"))

    form.text_input('Case Topic')
    form.text_input('Case Number')
    form.text_input('Court Number')
    form.text_input('Judgement Number')

    submitted = form.form_submit_button("Search")

    if submitted:
        with st.status("Running"):
            with open('data.json') as f:
                response = json.load(f)
        st.session_state["history"].append(dict(query=rag_query, response=response))

    
    



def history_display_container(history):
    # if len(history) > 1:
    #     st.header("Search History")
    #     max_idx = len(history) - 1
    #     history_idx = st.slider("History", 0, max_idx, value=max_idx, label_visibility="collapsed")
    #     entry = history[history_idx]
    # else:
    
    entry = history[-1]
    rag_query = st.text_area(
        label="Query:",
        value=entry["query"], height=150,
    )
        
    st.divider()

    # st.subheader("Query")
    # st.write(entry["query"])

    st.subheader("Retrieved Documents:")

    if "show_more" not in st.session_state:
        st.session_state["show_more"] = dict.fromkeys(range(0, len(entry["response"])), False)
    if "show_more_cases" not in st.session_state: 
        st.session_state["show_more_cases"] = dict.fromkeys(range(0, 3), False)
    show_more = st.session_state["show_more"]
    show_more_cases = st.session_state["show_more_cases"]

    cols = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
    fields = ["Case Name", "Added On", "Client", "Court ID", "Judgement ID", "Published Year", "View"]

    # header
    for col, field in zip(cols, fields):
        col.markdown('''**:violet[''' + field + ''']**''')
        #col.markdown(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">{field}</p>', unsafe_allow_html=True)
        col.code(field)

    st.divider()

    col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
    col1.write(str("**Wrong Termination Case Documentation**"))
    col2.write(str("25.03.2023"))
    col3.write(str("Johanna"))
    col4.write(str("HCA"))
    col5.write(str("5"))
    col6.write(str("1998"))
    placeholder_case = col7.empty()
    if show_more_cases[0]:
        placeholder_case.button(
            "Close Folders", key=str(0) + "__", on_click=on_less_case_click, args=[show_more_cases, 0]
        )

        st.write("**Case Summary (AI)**")
        st.write("The central legal issue in this case is whether Example GmbH's termination of John Doe violated employment laws, specifically regarding employee rights and termination procedures.")
        
        st.write("")
        st.write("")
        col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
        col1.write(str("**Folders**"))
        # rows
        for idx, row in enumerate(entry["response"]):
            
            col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
            col1.write("📁    " + str(row["case_name"]))
            # col2.write("" + str(row["added_on"]))
            # col3.write("" + str(row["client"]))
            # col4.write("" + str(row["UCI"]))
            # col5.write("" + str(row["JN"]))
            # col6.write("" + str(row["year"]))
            

            placeholder = col2.empty()

            if show_more[idx]:
                placeholder.button(
                    "Close", key=str(idx) + "_", on_click=on_less_click, args=[show_more, idx]
                )

                # do stuff
               
                for id, file in enumerate(row["files"]):
                    col1, col2, col3 = st.columns((4, 2, 7))
                    col1.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄    " + f"{file}")
                    col2.button(
                    "view", key=str(idx) + "view" + file + str(id), on_click=on_view_file, args=[file]
                    ) 
            else:
                placeholder.button(
                    "Show Files",
                    key=idx,
                    on_click=on_more_click,
                    args=[show_more, idx],
                    type="primary",
                )
    else:
        placeholder_case.button(
            "Show Folders",
            key=str(0) + "folders",
            on_click=on_more_case_click,
            args=[show_more_cases, 0],
            type="primary",
        )
    st.write("")
    st.divider()
    st.write("")
    col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
    col1.write(str("**Wrong Termination With Coperate A**"))
    col2.write(str("25.03.2022"))
    col3.write(str("Lin"))
    col4.write(str("HCA"))
    col5.write(str("4"))
    col6.write(str("2000"))
    placeholder_case_1 = col7.empty()
    if show_more_cases[1]:
        placeholder_case_1.button(
            "Close Folders", key=str(1) + "__", on_click=on_less_case_click, args=[show_more_cases, 1]
        )


        st.write("**Case Summary (AI)**")
        st.write("The core legal question in the Johnson v. ABC Bank case pertains to whether the bank's foreclosure process adhered to the required legal procedures outlined in mortgage contracts and state regulations.")   
        

        st.write("")
        st.write("")
        col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
        col1.write(str("**Folders**"))
        # rows
        for idx, row in enumerate(entry["response"]):
            
            col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
            col1.write("📁    " + str(row["case_name"]))
            # col2.write("" + str(row["added_on"]))
            # col3.write("" + str(row["client"]))
            # col4.write("" + str(row["UCI"]))
            # col5.write("" + str(row["JN"]))
            # col6.write("" + str(row["year"]))
            

            placeholder = col2.empty()

            if show_more[idx]:
                placeholder.button(
                    "Close", key=str(idx) + "_1", on_click=on_less_click, args=[show_more, idx]
                )

                # do stuff
               
                for id, file in enumerate(row["files"]):
                    col1, col2, col3 = st.columns((4, 2, 7))
                    col1.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄    " + f"{file}")
                    col2.button(
                    "view", key=str(idx) + "view1" + file + str(id), on_click=on_view_file, args=[file]
                    ) 
            else:
                placeholder.button(
                    "Show Files",
                    key=str(idx) + "11",
                    on_click=on_more_click,
                    args=[show_more, idx],
                    type="primary",
                )
    else:
        placeholder_case_1.button(
            "Show Folders",
            key=str(1) + "folders",
            on_click=on_more_case_click,
            args=[show_more_cases, 1],
            type="primary",
        )
    st.write("")
    st.divider()
    st.write("")
    col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
    col1.write(str("**Class Wrong Termination**"))
    col2.write(str("25.03.2023"))
    col3.write(str("Simon"))
    col4.write(str("HCA"))
    col5.write(str("5"))
    col6.write(str("2001"))
    placeholder_case_2 =  col7.empty()
    if show_more_cases[2]:
        placeholder_case_2.button(
            "Close Folders", key=str(2) + "__", on_click=on_less_case_click, args=[show_more_cases, 2]
        )

        st.write("**Case Summary (AI)**")
        st.write("In the Smith v. XYZ Corporation case, the central legal issue revolves around whether the company's handling of workplace harassment complaints complies with anti-discrimination laws, particularly with respect to creating a hostile work environment.")
        
        st.write("")
        st.write("")
        col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
        col1.write(str("**Folders**"))
        # rows
        for idx, row in enumerate(entry["response"]):
            
            col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
            col1.write("📁    " + str(row["case_name"]))
            # col2.write("" + str(row["added_on"]))
            # col3.write("" + str(row["client"]))
            # col4.write("" + str(row["UCI"]))
            # col5.write("" + str(row["JN"]))
            # col6.write("" + str(row["year"]))
            

            placeholder = col2.empty()

            if show_more[idx]:
                placeholder.button(
                    "Close", key=str(idx) + "_2", on_click=on_less_click, args=[show_more, idx]
                )

                # do stuff
                
                for id, file in enumerate(row["files"]):
                    col1, col2, col3 = st.columns((4, 2, 7))
                    col1.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄    " + f"{file}")
                    col2.button(
                    "view", key=str(idx) + "view2" + file + str(id), on_click=on_view_file, args=[file]
                    ) 
            else:
                placeholder.button(
                    "Show Files",
                    key=str(idx) + "2",
                    on_click=on_more_click,
                    args=[show_more, idx],
                    type="primary",
                )
    else:
        placeholder_case_2.button(
            "Show Folders",
            key=str(2) + "folders",
            on_click=on_more_case_click,
            args=[show_more_cases, 2],
            type="primary",
        )

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

    retrieval()

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
    st.sidebar.header("❤️ Liked cases")
    st.sidebar.text("- Surveilance footage")
    st.sidebar.text("- Pretrial hearings")

    


if __name__ == "__main__":
    # run as a script to test streamlit app locally
    app()
