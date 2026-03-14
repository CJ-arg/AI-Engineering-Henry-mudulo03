import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def generate_synthetic_data():
    llm = ChatOpenAI(model="gpt-5-nano") 
    
    departments = {
        "hr_docs": "políticas de vacaciones, manual de conducta, beneficios corporativos",
        "tech_docs": "protocolos de seguridad IT, configuración de VPN, manual de soporte de software",
        "finance_docs": "procedimiento de reembolso de gastos, auditoría interna, políticas de viáticos",
        "legal_docs": "términos de servicio, contratos de confidencialidad, cumplimiento de protección de datos"
    }

    for dept, topic in departments.items():
        print(f"Generando datos para {dept}...")
        
        prompt = ChatPromptTemplate.from_template(
            "Sos un redactor técnico experto. Generá un documento extenso y detallado sobre {topic} "
            "para una empresa SaaS. El documento debe tener al menos 10 secciones numeradas y ser "
            "lo suficientemente largo para ser dividido en 50 fragmentos de información clara."
        )
        
        chain = prompt | llm
        response = chain.invoke({"topic": topic})
        
        
        path = f"data/{dept}/manual.txt"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(response.content)
            
    print("¡Fábrica de datos terminada!")

if __name__ == "__main__":
    generate_synthetic_data()