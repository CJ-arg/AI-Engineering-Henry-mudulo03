import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def create_vector_stores():
    embeddings = OpenAIEmbeddings()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=25,
        add_start_index=True
    )

    departments = ["hr_docs", "tech_docs", "finance_docs", "legal_docs"]

    for dept in departments:
        print(f"Procesando y vectorizando {dept}...")
        file_path = f"data/{dept}/manual.txt"
        
        if not os.path.exists(file_path):
            print(f"No se encontró el archivo en {file_path}")
            continue

        # 1. load document
        loader = TextLoader(file_path, encoding="utf-8")
        documents = loader.load()

        # 2. Dcreate chunks
        chunks = text_splitter.split_documents(documents)
        print(f"   -> Generados {len(chunks)} chunks para {dept}")

        # 3. FAISS index and store
        vector_store = FAISS.from_documents(chunks, embeddings)
        vector_store.save_local(f"data/{dept}/faiss_index")

    print("¡Bases de datos vectoriales listas y guardadas!")

if __name__ == "__main__":
    create_vector_stores()