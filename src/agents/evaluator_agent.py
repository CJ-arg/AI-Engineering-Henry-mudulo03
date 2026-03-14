from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_evaluator_agent():
    llm = ChatOpenAI(model="gpt-5-nano", reasoning_effort="medium")
    
    template = """Sos un auditor de calidad experto en sistemas de IA. 
    Tu tarea es ponerle una nota a la respuesta que dio nuestro asistente.
    
    CRITERIOS PARA EVALUAR:
    1. Fidelidad: ¿La respuesta se basa SOLAMENTE en el contexto legal/técnico provisto?
    2. Utilidad: ¿Realmente resuelve la duda del usuario?
    3. Tono: ¿Es profesional y acorde al departamento?

    CONTEXTO: {context}
    PREGUNTA: {question}
    RESPUESTA: {answer}

    INSTRUCCIÓN: Responde ÚNICAMENTE con un número del 1 al 10.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    return prompt | llm | StrOutputParser()