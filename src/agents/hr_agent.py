import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_hr_agent():
    # 1. load FAISS  HR
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.load_local(
        "data/hr_docs/faiss_index", 
        embeddings, 
        allow_dangerous_deserialization=True 
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 2. System Prompt 
    template = """Sos un asistente experto en Recursos Humanos de nuestra empresa SaaS. 
    Usá los siguientes fragmentos de contexto para responder la pregunta del usuario. 
    Si no sabés la respuesta basándote en el contexto, decí que no tenés esa información y derivá al usuario al portal de empleados.
    Mantené un tono profesional, amable y empático.

    Contexto:
    {context}

    Pregunta: {question}
    Respuesta:"""

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(model="gpt-5-nano")

    # 3. La Chain (LCEL)
   
    hr_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return hr_chain