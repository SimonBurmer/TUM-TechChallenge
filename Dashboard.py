import streamlit as st
import pandas as pd
import altair as alt


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

def generate_slide(title, text, image):
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    # Define your HTML code for the styled box
    styled_box_html = """
    <div style="
            width: 60%;
            margin: auto;
            background-color: #D9D9D9; 
            padding: 45px; 
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <div style="width: 45%; padding-right: 5%;">
                <h2 style="color: #333333;">{title}</h2>
            </div>
            <div style="width: 60%;">
                <p style="color: #555555;">{text}</p>
            </div>
            <img src="{image}" style="width: 25%; height: 140%; margin-top: -8%; position: absolute; right: 20%;">
        </div>
    """

    styled_box_html = styled_box_html.format(title=title, text=text, image=image)

    # Render the HTML code using st.markdown
    st.markdown(styled_box_html, unsafe_allow_html=True)

def colored_button_box(color, text):
    # Calculate the left margin to center the box
    left_margin = f"margin-left: {((100 - 30) / 2)}%;"

    # Define the style for the button-looking box
    button_style = f"border: 2px solid {color}; border-radius: 20px; padding: 10px; text-align: center; {left_margin} width: {30}%;"

    # Display the button-looking box
    st.markdown(f'<div style="{button_style}">{text}</div>', unsafe_allow_html=True)

# Main Streamlit app code

def app() -> None:
    # config
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
    st.sidebar.header("❤️ Liked cases")
    st.sidebar.text("- Surveilance footage")
    st.sidebar.text("- Pretrial hearings")

    add_logo()

    st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>LegalLens AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey;'>LegalLens offers an AI search solution to help lawyers research internal case data with the power of AI and the leverage of the best possible UX.</h3>", unsafe_allow_html=True)

    colored_button_box("#4318FF", "Get trial")

    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.header("What does LegalLens AI provide?")

    generate_slide(
        "Digitalize Documents",
        "Our AI-powered mobile application makes it easy to digitize and upload past case files, creating a centralized repository that is accessible from anywhere. This will save lawyers time, reduce the risk of errors, and improve their efficiency.",
        "https://i.imgur.com/Tjl0HwK.png",
    )

    generate_slide(
        "AI reviews cases",
        "By automatically identifying and applying relevant laws to specific cases, our AI-powered solution can help lawyers quickly grasp the legal framework of their cases and identify potential legal arguments. This can save them time and effort, and help lawyers make informed decisions more efficiently.",
        "https://i.imgur.com/dYp4MvH.png",
    )

    generate_slide(
        "Improve case analysis and preparation",
        "By providing a comprehensive overview of relevant laws and citations, our solution can empower lawyers to conduct thorough case analysis and preparation. This can lead to stronger legal strategies and more effective advocacy.",
        "https://i.imgur.com/iypfj1B.png",
    )

    generate_slide(
        "Centralized repository of case files",
        "Our case bank will provide lawyers with a single, searchable location for all of their case files. This will make it easy to find the information lawyers need, and to keep track of their cases. ",
        "https://i.imgur.com/Jt9oCHz.png",
    )

    generate_slide(
        "Empower lawyers to focus on strategic insights",
        "By handling the technical aspects of legal research, our solution can free up lawyers to focus on their core competencies, such as legal analysis, strategy development, and client communication. This can lead to more personalized and effective legal services.",
        "https://i.imgur.com/N0MIz7t.png",
    )

    generate_slide(
        "Reduce the risk of legal errors",
        "By automating the process of identifying and applying relevant laws, our solution can help lawyers avoid common legal errors, such as relying on outdated or irrelevant case law. This can protect clients and strengthen the reputation of law firms.",
        "https://i.imgur.com/dyQS4nT.png",
    )

    

if __name__ == "__main__":
    # run as a script to test streamlit app locally
    app()
