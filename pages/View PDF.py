import streamlit as st
import base64
import time
import os
from utils.utils import add_logo, nav_page, sidebar_content
from openai import OpenAI
from pdfminer.high_level import extract_text


client = OpenAI(api_key='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')
pdf_text = extract_text("./data/cases/test_case/judgement.pdf")

def summary_ai(pdf_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",  
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant for text summarization",
            },
            {
                "role": "user",
                "content": pdf_text,
            }
        ],
    )
    return response.choices[0].message.content


print(summary_ai(pdf_text))


















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
        
        print(filename)

        # display PDF
        with open(filename,"rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<p align="center"><iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0" width="100%" height="1000" type="application/pdf"></iframe></p>'
        col1.markdown(pdf_display, unsafe_allow_html=True)



        # display case info

        ##############################
        # Mock case into for pitch
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
            
            # Text input
            user_input = st.text_input("Enter your query:")

            # Button to trigger the API call
            if st.button("Get Response"):
                if user_input:
                    # Call the OpenAI API and display the response
                    response = get_openai_response(user_input)
                    st.text_area("Response:", value=response, height=300)
                else:
                    st.error("Please enter a query.")
            


        ##############################
        # Dynamic case info
        ##############################
        else:
            col2.header("**Applied Laws:**")
            col2.write("**Wait for it...**")
            col2.text("")
            col2.text("")
            col2.text("")

            col2.header("**Citations & References:**")
            col2.write("**Wait for it...**")
            col2.text("")
            col2.text("")
            col2.text("")

    sidebar_content()


if __name__ == "__main__":
    # run as a script to test streamlit app locally
    app()
