import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_tech_agent():
    # 1. load FAISS  Tech
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.load_local(
        "data/tech_docs/faiss_index", 
        embeddings, 
        allow_dangerous_deserialization=True 
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 2. System Prompt 
    template = """Sos el Ingeniero de Soporte Técnico de la empresa. 
                Tu misión es resolver problemas técnicos usando el contexto proporcionado.
                Si la solución requiere varios pasos, usá listas numeradas y poné los comandos o nombres de botones en **negrita**.

                Si no encontrás la solución en el contexto, sugerí abrir un ticket en el portal de Jira y pedí los logs de la consola.
                Tono: Resolutivo, claro y técnico pero accesible.
    Contexto:
    {context}

    Pregunta: {question}
    Respuesta:"""

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(model="gpt-5-nano")

    # 3. La Chain (LCEL)
   
    tech_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return tech_chain