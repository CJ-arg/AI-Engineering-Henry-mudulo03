from typing import Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class RouteQuery(BaseModel):
    topic: Literal["hr", "tech", "finance", "legal", "general"] = Field(
        ...,
        description="Dada una consulta de usuario, decide a qué departamento derivarla.",
    )

def get_orchestrator():
    llm = ChatOpenAI(model="gpt-5-nano", reasoning_effort="low")
    structured_llm = llm.with_structured_output(RouteQuery)
    
    system_prompt = """Sos un experto en clasificación de intenciones. 
    Tu trabajo es analizar la consulta del usuario y determinar qué departamento debe atenderla.
    
    Departamentos disponibles:
    - hr: Para temas de vacaciones, beneficios, recibos de sueldo, conducta.
    - tech: Para problemas de software, hardware, VPN, accesos, herramientas.
    - finance: Para reembolsos, facturación, auditorías, gastos.
    - legal: Para contratos, términos de servicio, privacidad, cumplimiento.
    - general: Si la pregunta no encaja en ninguna o es solo un saludo.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])
    
    return prompt | structured_llm