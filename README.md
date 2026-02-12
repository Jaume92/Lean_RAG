# 🏭 Lean AI Assistant

Un asistente de IA especializado en Lean Manufacturing que combina conocimiento experto en metodologías Lean con capacidades de análisis de datos en tiempo real.

## 🎯 Características

- **Chat Inteligente**: Responde preguntas sobre metodologías Lean usando RAG (Retrieval-Augmented Generation)
- **Calculadoras Lean**: OEE, Takt Time, Lead Time, y más
- **Generación de Herramientas**: VSM, A3 Reports, PDCA (próximamente)
- **Análisis de Procesos**: Identifica desperdicios y sugiere mejoras

## 🏗️ Arquitectura

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Frontend   │────▶│   Backend   │────▶│  Qdrant DB  │
│ (Streamlit) │     │  (FastAPI)  │     │  (Vectors)  │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
              ┌─────▼────┐  ┌─────▼────┐
              │  Redis   │  │PostgreSQL│
              │ (Cache)  │  │   (DB)   │
              └──────────┘  └──────────┘
```

## 📋 Stack Tecnológico

**Backend:**
- FastAPI (Python 3.11+)
- OpenAI GPT-4 / Claude 3.5 Sonnet
- Qdrant (Vector Database)
- LangChain (RAG Framework)
- PostgreSQL + Redis

**Frontend:**
- Streamlit (MVP)
- React + TypeScript (próximamente)

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker & Docker Compose
- Python 3.11+
- API Key de OpenAI o Anthropic

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tuusuario/lean-ai-assistant.git
cd lean-ai-assistant
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env y añadir tus API keys
```

3. **Iniciar servicios con Docker**
```bash
docker-compose up -d
```

4. **Verificar que todo funciona**
```bash
# Backend API
curl http://localhost:8000/health

# Frontend
# Abrir http://localhost:8501 en el navegador
```

### Instalación Local (Sin Docker)

1. **Instalar dependencias del backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Iniciar servicios requeridos**
```bash
# Qdrant (necesitas Docker para esto)
docker run -p 6333:6333 qdrant/qdrant

# Redis
docker run -p 6379:6379 redis:7-alpine

# PostgreSQL
docker run -p 5432:5432 -e POSTGRES_PASSWORD=lean_password postgres:15-alpine
```

3. **Iniciar backend**
```bash
uvicorn app.main:app --reload
```

4. **Iniciar frontend (en otra terminal)**
```bash
cd frontend
pip install streamlit
streamlit run app.py
```

## 📊 Uso

### API Endpoints

**Chat:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué es el Takt Time?"}'
```

**Calcular OEE:**
```bash
curl -X POST http://localhost:8000/api/calculate/oee \
  -H "Content-Type: application/json" \
  -d '{
    "availability": 90,
    "performance": 95,
    "quality": 99
  }'
```

**Calcular Takt Time:**
```bash
curl -X POST http://localhost:8000/api/calculate/takt-time \
  -H "Content-Type: application/json" \
  -d '{
    "available_time_minutes": 480,
    "customer_demand_units": 240
  }'
```

### Interfaz de Chat

1. Abrir http://localhost:8501
2. Escribir tu pregunta sobre Lean
3. Recibir respuesta con fuentes

## 📚 Añadir Conocimiento

Para enriquecer la base de conocimientos:

1. Añadir PDFs a `backend/data/knowledge_base/`
2. Ejecutar script de ingestión:
```bash
python scripts/ingest_documents.py
```

**Libros recomendados para añadir:**
- Toyota Production System (Taiichi Ohno)
- Lean Thinking (Womack & Jones)
- The Machine That Changed the World
- Learning to See (Mike Rother)

## 🧪 Tests

```bash
cd backend
pytest tests/
```

## 📁 Estructura del Proyecto

```
lean-ai-assistant/
├── backend/
│   ├── app/
│   │   ├── api/          # Endpoints
│   │   ├── core/         # Configuración
│   │   ├── services/     # Lógica de negocio
│   │   ├── models/       # Modelos de datos
│   │   └── utils/        # Utilidades
│   ├── data/             # Datos y embeddings
│   ├── tests/            # Tests
│   └── requirements.txt
├── frontend/
│   └── app.py           # Streamlit app
├── scripts/
│   └── ingest_documents.py
├── docker-compose.yml
└── README.md
```

## 🗺️ Roadmap

### Fase 1: MVP (Actual) ✅
- [x] Chat básico con RAG
- [x] Calculadoras Lean (OEE, Takt Time, Lead Time)
- [x] Docker setup
- [ ] Script de ingestión de documentos
- [ ] Frontend Streamlit

### Fase 2: Herramientas Avanzadas
- [ ] Generador de VSM
- [ ] Generador de A3 Reports
- [ ] Análisis de procesos desde CSV
- [ ] Frontend React

### Fase 3: Características Empresariales
- [ ] Autenticación de usuarios
- [ ] Knowledge base privada por empresa
- [ ] Fine-tuning personalizado
- [ ] API pública

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la branch (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

MIT License - ver archivo LICENSE para detalles

## 👤 Autor

**Jaume RRM**
- GitHub: [@Jaume92](https://github.com/Jaume92)
- LinkedIn: [jaume-ruiz-ruano-marcos](https://www.linkedin.com/in/jaume-ruiz-ruano-marcos)
- Web: [www.jaumerrm.dev](http://www.jaumerrm.dev)

## 🙏 Agradecimientos

- Toyota Production System por las metodologías Lean
- OpenAI y Anthropic por los modelos de IA
- Comunidad open source

---

**¿Preguntas?** Abre un issue en GitHub o contacta al autor.
