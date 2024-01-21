import streamlit as st
from utils import qa_pipeline, retriever

chain = qa_pipeline()
retriever_query = retriever()

def main():
    global chain
    # Set the title of the web application
    st.title('⚖️ 🔎 LegalLens AI - case retrieval')

    # Initialize the session state if it doesn't exist
    if 'chat_log' not in st.session_state:
        st.session_state['chat_log'] = []

    st.write("Please describe what kind of the cases you wish to find.")

    # Get the user's question
    user_input = st.text_area("Insert your query")

    # On user input, generate response and add to the chat log
    if st.button("Submit Query", type="primary"):
        # Generate the answer
        docs = retriever_query.invoke(user_input)
        bot_output = ''
        for doc in docs:
            bot_output += doc.metadata['source'] + '      ' + doc.page_content + '\n\n'
        # bot_output = bot_output['result']
        # Add the user input and bot output to the chat log
        st.session_state['chat_log'].append({"User": user_input, "Bot": bot_output})

    # Display the chat log
    for exchange in st.session_state['chat_log']:
        st.markdown(f'**You:** {exchange["User"]}')
        st.markdown(f'**Bot:** {exchange["Bot"]}')

if __name__ == "__main__":
    main()
