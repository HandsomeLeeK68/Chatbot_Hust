from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings as GPT4AllBgeEmbeddings
#Khai bao biến
pdf_data_path = "data"
vector_db_path = "vectorstores/db_faiss"
#create vector db from text

def create_db_from_pdf():
    #Load PDF documents
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    #Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)

    #Create embeddings
    embedding_model = GPT4AllBgeEmbeddings()

    #Create vector db
    db= FAISS.from_documents(chunks, embedding=embedding_model)
    db.save_local(vector_db_path)
    return db

create_db_from_pdf()


def create_db_from_text():
    raw_text = "test câu lệnh tạo vector db từ văn bản"

    #Split text into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )

    chunks = text_splitter.split_text(raw_text)

    #Create embeddings
    embedding_model = GPT4AllBgeEmbeddings(model_file = "models/all-MiniLM-L6-v2-f16.gguf")

    #Create vector db
    db= FAISS.from_texts(chunks, embedding=embedding_model)
    db.save_local(vector_db_path)
    return db