# Lean AI Assistant

Asistente de inteligencia artificial especializado en Lean Manufacturing que combina una base de conocimiento técnico con RAG, calculadoras de métricas productivas y análisis de procesos industriales.

Demo en producción: [leanrag-fpayub2h46ogjcnn3kquub.streamlit.app](https://leanrag-fpayub2h46ogjcnn3kquub.streamlit.app)

---

## El problema que resuelve

Los ingenieros y responsables de operaciones en entornos Lean necesitan respuestas rápidas a preguntas técnicas concretas: cómo calcular el OEE de una línea, qué desperdicios están afectando al Takt Time, cómo estructurar un análisis A3. La información existe, pero está dispersa en manuales, formaciones y documentos internos.

Este asistente centraliza ese conocimiento y lo hace consultable en lenguaje natural, con calculadoras integradas para las métricas más usadas en planta.

---

## Funcionalidades

**Chat con RAG**
Consulta de conceptos, metodologías y buenas prácticas Lean mediante lenguaje natural. El sistema recupera contexto relevante de la base de conocimiento antes de generar la respuesta.

**Calculadoras de métricas productivas**
- OEE (Overall Equipment Effectiveness)
- Takt Time
- Lead Time

**En desarrollo**
- Generación automática de VSM y A3
- Análisis de procesos desde datos reales de planta
- Detección de desperdicios a partir de datos operativos

---

## Arquitectura
```
Frontend (Streamlit)
        ↓
Backend (FastAPI)
        ↓
    ┌───────────────────────────┐
    │  LangChain + LLM          │  ← OpenAI / Anthropic
    │  Qdrant (vector store)    │  ← Base de conocimiento Lean
    │  Redis (caché)            │
    │  PostgreSQL (persistencia)│
    └───────────────────────────┘
```

El frontend actual en Streamlit está planificado para migrar a React + TypeScript.

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python 3.11, FastAPI, LangChain |
| Vector store | Qdrant |
| Caché | Redis |
| Persistencia | PostgreSQL |
| Frontend | Streamlit (MVP) → React + TypeScript |
| LLM | OpenAI / Anthropic |

---

## Instalación
```bash
git clone https://github.com/Jaume92/Lean_RAG.git
cd Lean_RAG
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
```

Qdrant, Redis y PostgreSQL pueden iniciarse con Docker:
```bash
docker-compose up -d
```

Arrancar backend y frontend:
```bash
uvicorn app.main:app --reload
streamlit run app.py
```

---

## API — Ejemplos de uso
```bash
# Consulta al asistente
POST /api/chat
{ "mensaje": "¿Qué es el Takt Time?" }

# Cálculo de OEE
POST /api/calculate/oee
{ "availability": 0.90, "performance": 0.85, "quality": 0.95 }
```

---

## Estado del proyecto

Funcional en producción como MVP. Chat RAG operativo, calculadoras Lean integradas e ingesta de documentos PDF activa.

Próximos pasos: generación automática de VSM y A3, análisis de procesos desde datos reales, frontend en React y sistema multiempresa.

---

## Estructura del proyecto
```
lean-ai-assistant/
├── backend/
│   ├── api/
│   ├── core/
│   ├── services/
│   ├── models/
│   └── utils/
├── frontend/
├── scripts/
└── docker-compose.yml
```

---

[jaumerrm.dev](https://www.jaumerrm.dev) · [LinkedIn](https://www.linkedin.com/in/jaume-ruiz-ruano-marcos) · [GitHub](https://github.com/Jaume92)
