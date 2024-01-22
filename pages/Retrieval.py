import streamlit as st
import json
from utils.utils import add_logo, nav_page, sidebar_content

def on_more_click(show_more, id, idx):
    show_more[id][idx] = True

def on_more_case_click(show_more_cases, idx):
    show_more_cases[idx] = True

def on_less_case_click(show_more_cases, idx):
    show_more_cases[idx] = False


def on_less_click(show_more, id, idx):
    show_more[id][idx] = False

def on_view_file(filename):
    f = open("filename.txt", "w")
    f.write(filename)
    f.close()
    nav_page("View_PDF")

# UI for displaying the header, folders, and files of each case
def case(title1, title2, title3, title4, title5, title6, key, case_id, show_more_cases, summary, entry, show_more):
    col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
    col1.write(str(title1))
    col2.write(str(title2))
    col3.write(str(title3))
    col4.write(str(title4))
    col5.write(str(title5))
    col6.write(str(title6))
    placeholder_case = col7.empty()
    if show_more_cases[case_id]:
        placeholder_case.button(
            "Close Folders", key=key + "__", on_click=on_less_case_click, args=[show_more_cases, case_id]
        )
        st.write("**Case Summary (AI)**")
        st.write(summary)
        st.write("")
        st.write("")
        col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
        col1.write(str("**Folders**"))
        
        for idx, row in enumerate(entry["response"]):
            col1, col2, col3, col4, col5, col6, col7 = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
            col1.write("📁    " + str(row["case_name"]))

            placeholder = col2.empty()
            if show_more[case_id][idx]:
                placeholder.button(
                    "Close", key=key + str(idx) + "_", on_click=on_less_click, args=[show_more, case_id, idx]
                )
               
                for file_id, file in enumerate(row["files"]):
                    col1, col2, col3 = st.columns((4, 2, 7))
                    col1.markdown("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄    " + f"{file}")
                    col2.button(
                    "view", key=key + str(idx) + "view" + file + str(file_id), on_click=on_view_file, args=[file]
                    ) 
            else:
                placeholder.button(
                    "Show Files",
                    key= key + str(idx),
                    on_click=on_more_click,
                    args=[show_more, case_id, idx],
                    type="primary",
                )
    else:
        placeholder_case.button(
            "Show Folders",
            key=str(case_id) + "folders",
            on_click=on_more_case_click,
            args=[show_more_cases, case_id],
            type="primary",
        )

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
            # call retriever module, and pass in query to get relevant documents & locations of source files
            # docs, sources = retriever.utils.retrieve_relevant_docs(rag_query)
            # replaced for now with mockdata for demonstration in pitch because no legal files.
            with open('data/data.json') as f:
                response = json.load(f)
        st.session_state["history"].append(dict(query=rag_query, response=response))
        st.experimental_rerun()

def history_display_container(history):
    entry = history[-1]
    st.text_area(
        label="Query:",
        value=entry["query"], height=150,
    )
    st.divider()
    st.subheader("Retrieved Documents:")

    if "show_more" not in st.session_state:
        st.session_state["show_more"] = [[False] * 4 for _ in range(3)]
    if "show_more_cases" not in st.session_state: 
        st.session_state["show_more_cases"] = dict.fromkeys(range(0, 3), False)
    show_more = st.session_state["show_more"]
    show_more_cases = st.session_state["show_more_cases"]

    cols = st.columns((4, 1.5, 1.5, 1, 1.5, 1.5, 2))
    fields = ["Case Name", "Added On", "Client", "Court ID", "Judgement ID", "Published Year", "View"]

    # header
    for col, field in zip(cols, fields):
        col.code(field)

    st.divider()

    # Mock data
    case(
            "**Wrong Termination Case Documentation**", "25.03.2023", "John", "HCA", "5", "1998", "0", 0, show_more_cases, 
            "The central legal issue in this case is whether Example GmbH's termination of John Doe violated employment laws, specifically regarding employee rights and termination procedures.",
            entry, show_more
         )

    st.write("")
    st.divider()
    st.write("")

    case(
            "**Wrong Termination With Coperate A**", "25.03.2022", "Lin", "HCA", "4", "2000", "1", 1, show_more_cases, 
            "The core legal question in the Johnson v. ABC Bank case pertains to whether the bank's foreclosure process adhered to the required legal procedures outlined in mortgage contracts and state regulations.",
            entry, show_more
         )

    st.write("")
    st.divider()
    st.write("")

    case(
            "**Class Wrong Termination**", "18.02.2022", "Simon", "HCA", "6", "2001", "2", 2, show_more_cases, 
            "In the Smith v. XYZ Corporation case, the central legal issue revolves around whether the company's handling of workplace harassment complaints complies with anti-discrimination laws, particularly with respect to creating a hostile work environment.",
            entry, show_more
         )


def app() -> None:
    st.set_page_config(
        page_title="LegalLens AI",
        page_icon="🔍",
        layout="wide",
        menu_items={"Get help": None, "Report a bug": None},
    )
    
    st.session_state["filename"] = ""

    add_logo()

    st.title("📤 Retrieval")
    st.markdown("Your chatAI based search will list the documents you are looking for.")
    st.markdown("""---""")

    if history := st.session_state.get("history"):
        history_display_container(history)
    else:
        st.session_state["history"] = list()
        retrieval_form_container()

    sidebar_content()

    


if __name__ == "__main__":
    # run as a script to test streamlit app locally
    app()
