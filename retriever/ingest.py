# Importing Dependencies
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Dataset Directory Path
DATASET = "dataset/"

# Faiss Index Path
FAISS_INDEX = "vectorstore/"

# Create Vector Store and Index
def embed_all():
    # Create the document loader
    text_loader_kwargs={'autodetect_encoding': True}
    loader = DirectoryLoader(DATASET, glob="./*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
    # Load the documents
    documents = loader.load()
    # Create the splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    # Split the documents into chunks
    chunks = splitter.split_documents(documents)
    # Load the embeddings
    embeddings = HuggingFaceEmbeddings()
    # Create the vector store
    vector_store = FAISS.from_documents(chunks, embeddings)
    # Save the vector store
    vector_store.save_local(FAISS_INDEX)

if __name__ == "__main__":
    embed_all()