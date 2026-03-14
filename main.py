from src.agents.orchestrator import get_orchestrator
from src.agents.hr_agent import get_hr_agent
from src.agents.tech_agent import get_tech_agent
from src.agents.finance_agent import get_finance_agent
from src.agents.legal_agent import get_legal_agent

def main():
    print("Sistema Multi-Agente SaaS - Iniciado")
    
    # 1. Inicializamos el Orquestador y los Agentes
    orchestrator = get_orchestrator()
    
    # Mapeo de agentes (Diccionario de Estrategia)
    agents = {
        "hr": get_hr_agent(),
        "tech": get_tech_agent(),
        "finance": get_finance_agent(),
        "legal": get_legal_agent()
    }

    print("\n--- Bienvenido al Soporte Inteligente ---")
    question = input("¿En qué puedo ayudarte hoy?: ")

    # 2. Paso del Orquestador (Clasificación)
    print(f"\n[Orquestador] Analizando intención...")
    route = orchestrator.invoke({"question": question})
    topic = route.topic
    print(f"[Orquestador] Clasificado como: {topic.upper()}")

    # 3. Lógica de Enrutamiento
    if topic in agents:
        agent_chain = agents[topic]
        print(f"[Agente {topic.upper()}] Buscando en manuales y generando respuesta...")
        
        response = agent_chain.invoke(question)
        print("\n" + "="*50)
        print(f"RESPUESTA FINAL:\n{response}")
        print("="*50)
        
    elif topic == "general":
        print("\n" + "="*50)
        print("RESPUESTA FINAL: Hola! Soy tu asistente SaaS. ¿Tenés alguna duda sobre HR, IT, Finanzas o Legales?")
        print("="*50)
        
    else:
        print("\n❌ Error: El orquestador devolvió una categoría no configurada.")

if __name__ == "__main__":
    main()