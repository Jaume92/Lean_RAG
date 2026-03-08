# Lean AI Assistant

Asistente de inteligencia artificial especializado en Lean Manufacturing que combina RAG sobre base de conocimiento técnico con calculadoras de métricas productivas.

Demo en producción: [leanrag-fpayub2h46ogjcnn3kquub.streamlit.app](https://leanrag-fpayub2h46ogjcnn3kquub.streamlit.app)

---

## El problema que resuelve

Los ingenieros y responsables de operaciones en entornos Lean necesitan respuestas rápidas a preguntas técnicas concretas: cómo calcular el OEE de una línea, qué desperdicios están afectando al Takt Time, cómo estructurar un análisis A3. La información existe, pero está dispersa en manuales, formaciones y documentos internos.

Este asistente centraliza ese conocimiento y lo hace consultable en lenguaje natural, con calculadoras integradas para las métricas más usadas en planta.

---

## Funcionalidades

**Chat con RAG**

El sistema embebe la consulta con `sentence-transformers/all-MiniLM-L6-v2`, recupera los fragmentos más relevantes de Qdrant y construye el contexto antes de llamar al LLM. Si no hay contexto relevante, responde directamente desde el modelo.

**Calculadoras de métricas productivas**
- OEE (Overall Equipment Effectiveness)
- Takt Time
- Lead Time

**En desarrollo**
- Generación automática de VSM y A3
- Análisis de procesos desde datos reales de planta
- Detección de desperdicios a partir de datos operativos
- Frontend en React + TypeScript

---

## Arquitectura
```
Frontend (Streamlit)
        ↓
Backend (FastAPI)
        ↓
    ┌──────────────────────────────────┐
    │  LangChain + LLM                 │  ← OpenAI / Anthropic
    │  Qdrant (vector store)           │  ← Base de conocimiento Lean
    │  SentenceTransformers (embedder) │  ← all-MiniLM-L6-v2
    │  Redis (caché)                   │
    │  PostgreSQL (persistencia)       │
    └──────────────────────────────────┘
```

El backend hace warm-up de embeddings en startup para evitar latencia en la primera consulta en producción.

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python 3.11, FastAPI |
| RAG | LangChain, SentenceTransformers |
| Vector store | Qdrant Cloud |
| Caché | Redis |
| Persistencia | PostgreSQL |
| Frontend | Streamlit (MVP) → React + TypeScript |
| LLM | OpenAI / Anthropic |
| Deploy | Streamlit Cloud + Render |

---

## Instalación
```bash
git clone https://github.com/Jaume92/Lean_RAG.git
cd Lean_RAG
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
```

Configurar variables de entorno:
```bash
cp .env.example .env
# Añadir OPENAI_API_KEY o ANTHROPIC_API_KEY, QDRANT_URL, QDRANT_API_KEY
```

Arrancar servicios con Docker:
```bash
docker-compose up -d
```

Arrancar backend y frontend:
```bash
uvicorn app.main:app --reload
streamlit run frontend/app.py
```

---

## API — Ejemplos de uso
```bash
# Consulta al asistente
POST /api/chat
{ "message": "¿Qué es el Takt Time?" }

# Cálculo de OEE
POST /api/calculate/oee
{ "availability": 0.90, "performance": 0.85, "quality": 0.95 }

# Cálculo de Takt Time
POST /api/calculate/takt-time
{ "available_time_minutes": 480, "customer_demand_units": 240 }

# Estado de la base de conocimiento
GET /api/knowledge/stats
```

---

## Estado del proyecto

Chat RAG operativo en producción, calculadoras Lean integradas, ingesta de documentos PDF activa y health check con latencia en tiempo real.

Próximos pasos: generación automática de VSM y A3, análisis desde datos reales de planta, frontend en React y arquitectura multiempresa.

---

## Estructura del proyecto
```
lean-ai-assistant/
├── backend/
│   └── app/
│       ├── api/routes.py        ← Endpoints FastAPI
│       ├── core/config.py       ← Configuración centralizada
│       ├── services/
│       │   ├── rag_service.py   ← RAG + Qdrant
│       │   ├── llm_service.py   ← Integración LLM
│       │   └── calculator.py    ← Métricas Lean
│       └── models/schemas.py    ← Modelos Pydantic
├── frontend/app.py              ← Streamlit UI
├── scripts/ingest_documents.py  ← Ingesta de PDFs
└── docker-compose.yml
```

---

[jaumerrm.dev](https://www.jaumerrm.dev) · [LinkedIn](https://www.linkedin.com/in/jaume-ruiz-ruano-marcos) · [GitHub](https://github.com/Jaume92)

---

[jaumerrm.dev](https://www.jaumerrm.dev) · [LinkedIn](https://www.linkedin.com/in/jaume-ruiz-ruano-marcos) · [GitHub](https://github.com/Jaume92)
