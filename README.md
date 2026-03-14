# Corporate Support Multi-Agent System

## Sistema Multi-Agente RAG - Soporte Corporativo SaaS

Este proyecto implementa una arquitectura de soporte automatizado basada en **agentes especializados** y **Recuperación Aumentada por Generación (RAG)**.

El sistema utiliza:

- Un **orquestador central** para el ruteo de consultas
- **Agentes especializados por departamento**
- Un **agente evaluador independiente** que controla la calidad de las respuestas (*LLM-as-a-Judge*)
- **Trazabilidad completa mediante Langfuse** para monitoreo y auditoría

---

# Requisitos e Instalación

## 1. Requisitos

- **Python 3.12 o superior**
- **uv** como administrador de paquetes
- Archivo `.env` con las siguientes variables:

```env
OPENAI_API_KEY=s***************************
LANGFUSE_SECRET_KEY="******************************"
LANGFUSE_PUBLIC_KEY="****************************************"
LANGFUSE_BASE_URL="https://***********.langfuse.com"
```

---

## 2. Instalación de dependencias

Sincronizar el entorno con:

```bash
uv sync
```

Esto instalará todas las dependencias definidas en `requirements.txt`.

---

# Ejecución del Sistema

Antes de ejecutar el sistema:

1. Verificar que los **índices FAISS** de cada departamento estén generados en la carpeta:

```
data/
```

2. Iniciar la aplicación:

```bash
uv run main.py
```

---

# Arquitectura del Sistema

El flujo de trabajo se basa en una **estructura de orquestación centralizada** que gestiona:

- Clasificación de consultas
- Recuperación de conocimiento
- Generación de respuestas
- Auditoría automática de calidad

---

# Agentes y Roles

## Orchestrator

Actúa como **clasificador de intenciones** utilizando salida estructurada.

Responsabilidades:

- Analizar la consulta del usuario
- Determinar el departamento correspondiente
- Derivar la consulta al agente adecuado

Departamentos soportados:

- HR
- Tech
- Finance
- Legal

---

## Especialistas RAG

Son **cuatro agentes independientes** que utilizan recuperación de contexto desde bases vectoriales FAISS.

Cada agente responde consultas basándose en **documentación corporativa interna**.

Agentes disponibles:

- `hr_agent.py`
- `tech_agent.py`
- `finance_agent.py`
- `legal_agent.py`

---

## Evaluator Agent (LLM-as-a-Judge)

Agente independiente encargado de **evaluar la calidad de las respuestas**.

Analiza la siguiente tríada:

```
Pregunta
Contexto Recuperado
Respuesta Generada
```

Luego asigna un **puntaje de calidad** basado en:

- Fidelidad al contexto
- Utilidad de la respuesta
- Coherencia

---

# Especificaciones Técnicas

## Framework

- **LangChain**
- Uso de **LCEL (LangChain Expression Language)**

---

## Modelos

- **OpenAI gpt-5-nano**

Configuración diferenciada de:

- `reasoning_effort` para el orquestador
- `reasoning_effort` para el evaluador

---

## Base de Datos Vectorial

- **FAISS**

Utilizado para:

- almacenamiento local de embeddings
- recuperación por similitud semántica

---

## Observabilidad

Integración con **Langfuse** mediante:

```
CallbackHandler
```

Permite:

- monitoreo de trazas
- seguimiento de prompts
- control de costos

---

## Gestión de Calidad

Se implementa **scoring automático de respuestas** persistido en el dashboard de Langfuse.

Métodos utilizados:

- `create_score`
- `last_trace_id`

Esto permite **auditar cada interacción del sistema**.

---

# Estructura del Repositorio

```
project/
│
├── main.py
│
├── src/
│   └── agents/
│       ├── orchestrator.py
│       ├── evaluator_agent.py
│       ├── hr_agent.py
│       ├── tech_agent.py
│       ├── finance_agent.py
│       └── legal_agent.py
│
├── data/
│   ├── manuals/
│   └── vector_indexes/
│
├── requirements.txt
└── README.md
```

---

# Descripción de Archivos Principales

### main.py

Punto de entrada del sistema.

Responsable de:

- iniciar la sesión
- ejecutar el flujo de agentes
- persistir métricas de calidad

---

### src/agents/orchestrator.py

Implementa la lógica de **ruteo semántico estructurado**.

---

### src/agents/evaluator_agent.py

Implementa el patrón **LLM-as-a-Judge** para auditoría automática.

---

### src/agents/\*_agent.py

Definen los **agentes especializados por departamento** utilizando cadenas RAG.

---

### data/

Contiene:

- manuales corporativos
- índices vectoriales FAISS

---

### requirements.txt

Lista de dependencias bloqueadas generadas con `uv` para garantizar **reproducibilidad del entorno**.

---
