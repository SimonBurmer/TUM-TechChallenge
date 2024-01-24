import streamlit as st
import base64
import API_Key
from utils.utils import add_logo, nav_page, sidebar_content
from openai import OpenAI
from pdfminer.high_level import extract_text


client = OpenAI(api_key=API_Key.OPEN_API_KEY)

def laws_applied_ai(file_path):
    pdf_text = extract_text(file_path)

    if len(pdf_text) > 10000:
        pdf_text = pdf_text[:10000] # limit to 10k characters for GPT-3
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {
                "role": "system",
                "content": "You are a lawyer assistant and you return bullet points of all german laws that are applied/used to the given text. Only answer with the pullet point's on other text.  Always answer in English.",
            },
            {
                "role": "user",
                "content": pdf_text,
            }
        ],
    )
    return response.choices[0].message.content


def laws_references_ai(file_path):
    pdf_text = extract_text(file_path)

    if len(pdf_text) > 10000:
        pdf_text = pdf_text[:10000] # limit to 10k characters for GPT-3
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {
                "role": "system",
                "content": "You are a lawyer assistant and you return bullet points of all german Citations & References that are applied/used to the given text. Only answer with the pullet point's on other text.  Always answer in English.",
            },
            {
                "role": "user",
                "content": pdf_text,
            }
        ],
    )
    return response.choices[0].message.content


def back():
    nav_page("Retrieval")
        

def app() -> None:
    # config
    st.set_page_config(
        page_title="LegalLens AI",
        page_icon="🔍",
        layout="wide",
        menu_items={"Get help": None, "Report a bug": None},
    )
    st.session_state["filename"] = ""
    st.button("Back to retrieval", on_click=back)
    add_logo()
    filename = ""

    # retrieve last opened file
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

        # display PDF
        with open(filename,"rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<p align="center"><iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0" width="100%" height="1000" type="application/pdf"></iframe></p>'
        col1.markdown(pdf_display, unsafe_allow_html=True)

        ##############################
        # Mock case info for pitch
        ##############################
        if "wrongful_termination" in filename:        
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
            
            
        ##############################
        # Dynamic case info
        ##############################
        else:
            col2.header("**Applied Laws:**")
            
            with col2:
                with st.spinner('Finding all applied laws...'):
                    try:
                        laws_applied = laws_applied_ai(filename)
                    except:
                        laws_applied = "OpenAI API is not Working!! Insert your api key in API_Key.py!!"
            col2.text(laws_applied)

            col2.header("**Citations & References:**")
            with col2:
                with st.spinner('Finding all used citations & references...'):
                    try:
                        references = laws_applied_ai(filename)
                    except:
                        references = "OpenAI API is not Working!! Insert your api key in API_Key.py!!"
            col2.text(references)

    sidebar_content()


if __name__ == "__main__":
    # run as a script to test streamlit app locally
    app()
