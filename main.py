import os
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from src.agents.orchestrator import get_orchestrator
from src.agents.hr_agent import get_hr_agent
from src.agents.tech_agent import get_tech_agent
from src.agents.finance_agent import get_finance_agent
from src.agents.legal_agent import get_legal_agent
from src.agents.evaluator_agent import get_evaluator_agent

load_dotenv()

def main():
    langfuse_client = Langfuse()
    langfuse_handler = CallbackHandler()

    orchestrator = get_orchestrator()
    evaluator = get_evaluator_agent()
    
    agents = {
        "hr": get_hr_agent(),
        "tech": get_tech_agent(),
        "finance": get_finance_agent(),
        "legal": get_legal_agent()
    }

    print("\n--- Sistema Multi-Agente SaaS ---")
    question = input("¿En qué puedo ayudarte?: ")

    route = orchestrator.invoke({"question": question}, config={"callbacks": [langfuse_handler]})
    topic = route.topic

    if topic in agents:
        agent_chain = agents[topic]
        answer = agent_chain.invoke(question, config={"callbacks": [langfuse_handler]})
        
        score_val = evaluator.invoke({
            "context": "Informacion recuperada de manuales internos",
            "question": question,
            "answer": answer
        }, config={"callbacks": [langfuse_handler]})
        
        langfuse_client.create_score(
            trace_id=langfuse_handler.last_trace_id,
            name="calidad-rag",
            value=float(score_val)
        )
        
        print(f"\n[Departamento: {topic.upper()}]")
        print(f"Calidad detectada: {score_val}/10")
        print(f"BOT: {answer}")
        
    elif topic == "general":
        print("\nBOT: ¡Hola! Soy tu asistente. ¿Tenés dudas sobre HR, Tech, Finanzas o Legales?")
    
    else:
        print("\nError: No se pudo determinar el departamento.")

if __name__ == "__main__":
    main()