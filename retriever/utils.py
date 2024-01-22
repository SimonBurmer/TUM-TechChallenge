# Importing Dependencies
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains.summarize import load_summarize_chain

# Faiss Index Path
FAISS_INDEX = "vectorstore/"

# Custom prompt template
custom_prompt_template = """[INST] <<SYS>>
You are a trained bot to give a summary on the given context about legal case. You will summarize on the essential details of the case to provide a general understanding. 
<</SYS>>
Context : {context}
Summary : [/INST]
"""

# Return the LLM
def load_llm():
    """
    Load the LLM
    """
    # Load the model
    llm = CTransformers(model='TheBloke/Llama-2-7b-Chat-GGUF', model_type='llama')

    return llm

def generate_summary_chain():
    llm = load_llm()
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain

# generate a summary about a case based on the documents provided
def generate_summary(docs):
    chain = generate_summary_chain()
    return chain.run(docs)

# Return the chain
def retriever():
    # Load the HuggingFace embeddings funciton
    embeddings = HuggingFaceEmbeddings()

    # Load the index
    db = FAISS.load_local("vectorstore/", embeddings)
    retriever = db.as_retriever()

    return retriever

# Based on user input query, return the retrieved documents of similar semantic content to the query, and also a list of relevant source files
def retrieve_relevant_docs(query):
    retriever_db = retriever()
    docs = retriever_db.invoke(query)

    sources = []
    for doc in docs:
            sources.append(doc.metadata['source']) 
    return docs, sources