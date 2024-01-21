# Importing Dependencies
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from langchain import PromptTemplate, HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import CTransformers

# Faiss Index Path
FAISS_INDEX = "vectorstore/"


# Return the LLM
def load_llm():
    """
    Load the LLM
    """
    # Model ID

    # Load the model
    llm = CTransformers(model='TheBloke/Llama-2-7b-Chat-GGUF', model_type='llama')

    return llm


# Return the chain
def retriever():
    # Load the HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings()

    # Load the index
    db = FAISS.load_local("vectorstore/", embeddings)

    retriever = db.as_retriever()

    return retriever