Lean AI Assistant
Asistente de Inteligencia Artificial orientado a Lean Manufacturing que combina conocimiento en metodologías de mejora continua con análisis de datos y generación de respuestas mediante RAG.

Demo en producción
https://leanrag-fpayub2h46ogjcnn3kquub.streamlit.app/

Descripción
Proyecto enfocado en construir una herramienta práctica para consulta de conceptos Lean, cálculo de métricas productivas y apoyo en análisis de procesos industriales.

Funcionalidades actuales

Chat basado en RAG para preguntas sobre Lean Manufacturing

Calculadoras de métricas: OEE, Takt Time y Lead Time

Estructura preparada para generación de herramientas Lean (VSM, A3, PDCA en desarrollo)

Base preparada para análisis de procesos y detección de desperdicios

Arquitectura
Frontend en Streamlit conectado a un backend en FastAPI.
El backend gestiona embeddings en Qdrant, caché en Redis y persistencia en PostgreSQL.

Stack tecnológico

Backend

Python 3.11

FastAPI

LangChain

Qdrant (base de datos vectorial)

PostgreSQL

Redis

Integración con modelos LLM (OpenAI / Anthropic)

Frontend

Streamlit (MVP actual)

Migración futura a React + TypeScript

Ejecución rápida

Requisitos

Python 3.11

Docker (opcional)

API Key de OpenAI o Anthropic

Instalación básica

Clonar repositorio
git clone https://github.com/Jaume92/Lean_RAG.git

cd Lean_RAG

Crear entorno virtual
python -m venv venv
venv\Scripts\activate

Instalar dependencias
pip install -r backend/requirements.txt

Lanzar servicios necesarios
Qdrant, Redis y PostgreSQL pueden iniciarse con Docker si se desea.

Ejecutar backend
uvicorn app.main:app --reload

Ejecutar frontend
streamlit run app.py

Uso de la API

Ejemplo chat
POST /api/chat
mensaje: “¿Qué es el Takt Time?”

Ejemplo cálculo OEE
POST /api/calculate/oee
availability, performance, quality

Estructura del proyecto

lean-ai-assistant

backend

api

core

services

models

utils

frontend

scripts

docker-compose.yml

Estado del proyecto

Fase actual

Chat funcional con RAG

Calculadoras Lean básicas

Ingesta de documentos PDF

MVP funcional desplegado en Streamlit

Próximos pasos

Generación automática de VSM y A3

Análisis de procesos desde datos reales

Frontend en React

Sistema multiempresa

Autor
Jaume Ruiz-Ruano

GitHub
https://github.com/Jaume92

LinkedIn
https://www.linkedin.com/in/jaume-ruiz-ruano-marcos

Web
https://www.jaumerrm.dev
