# 📚 Guía de Uso - Lean AI Assistant

## 🚀 Inicio Rápido

### Opción 1: Con Script de Inicio
```bash
./start.sh
```

### Opción 2: Manual
```bash
# 1. Copiar variables de entorno
cp .env.example .env

# 2. Editar .env y añadir API keys
nano .env  # o tu editor preferido

# 3. Iniciar servicios
docker-compose up -d

# 4. Verificar que todo funciona
curl http://localhost:8000/health
```

## 📝 Ejemplos de Uso

### 1. Chat - Preguntas sobre Lean

**Ejemplo 1: Conceptos básicos**
```
Q: ¿Qué es el Takt Time y por qué es importante?

A: El Takt Time es el ritmo al que debe producirse para cumplir con la 
demanda del cliente. Se calcula dividiendo el tiempo disponible entre 
la demanda. Es importante porque marca el "pulso" de la producción...
```

**Ejemplo 2: Metodologías**
```
Q: ¿Cómo implementar 5S en mi empresa?

A: La implementación de 5S sigue 5 pasos:
1. Seiri (Clasificar): Separar lo necesario de lo innecesario...
2. Seiton (Ordenar): Un lugar para cada cosa...
...
```

**Ejemplo 3: Problemas prácticos**
```
Q: Tengo un OEE de 65%, ¿qué puedo hacer para mejorarlo?

A: Un OEE de 65% indica oportunidades significativas de mejora...
[El asistente analizará y dará recomendaciones específicas]
```

### 2. Calculadora OEE

**Ejemplo: Análisis de una máquina**

Inputs:
- Disponibilidad: 85% (la máquina estuvo disponible el 85% del tiempo)
- Performance: 90% (trabajó al 90% de su velocidad ideal)
- Calidad: 95% (el 95% de las piezas fueron buenas)

Resultado:
```
OEE = 85% × 90% × 95% = 72.7%

Análisis:
- OEE: 72.7% (Por debajo de World-Class)
- Pérdida por Disponibilidad: 15%
- Pérdida por Performance: 10%
- Pérdida por Calidad: 5%

Recomendaciones:
1. Disponibilidad < 90%: Implementar TPM para reducir paradas
2. Performance < 95%: Analizar cuellos de botella
3. Enfocarse primero en mejorar la Disponibilidad (mayor pérdida)
```

### 3. Calculadora Takt Time

**Ejemplo: Línea de ensamblaje**

Inputs:
- Tiempo disponible: 480 minutos (8 horas)
- Demanda: 240 unidades por día

Resultado:
```
Takt Time: 2.0 minutos (120 segundos)

Interpretación:
Cada 2 minutos debe completarse una unidad para cumplir 
con la demanda del cliente.

Capacidad necesaria:
- 30 unidades/hora
- 240 unidades/día
```

### 4. API Endpoints

**Ejemplo con cURL:**

```bash
# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué es Kaizen?",
    "session_id": "user123"
  }'

# Calcular OEE
curl -X POST http://localhost:8000/api/calculate/oee \
  -H "Content-Type: application/json" \
  -d '{
    "availability": 85,
    "performance": 90,
    "quality": 95
  }'

# Calcular Takt Time
curl -X POST http://localhost:8000/api/calculate/takt-time \
  -H "Content-Type: application/json" \
  -d '{
    "available_time_minutes": 480,
    "customer_demand_units": 240
  }'
```

**Ejemplo con Python:**

```python
import requests

# Chat
response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "message": "¿Qué es Value Stream Mapping?",
        "session_id": "user123"
    }
)
result = response.json()
print(result["answer"])
print("\nFuentes:", result["sources"])

# Calcular OEE
oee_response = requests.post(
    "http://localhost:8000/api/calculate/oee",
    json={
        "availability": 85,
        "performance": 90,
        "quality": 95
    }
)
oee_result = oee_response.json()
print(f"OEE: {oee_result['oee']}%")
print("Recomendaciones:")
for rec in oee_result['recommendations']:
    print(f"  - {rec}")
```

## 📚 Añadir Conocimiento

### Paso 1: Obtener documentos Lean

Descarga PDFs de libros sobre Lean Manufacturing:

**Libros recomendados:**
1. Toyota Production System - Taiichi Ohno
2. Lean Thinking - Womack & Jones
3. The Machine That Changed the World - Womack, Jones, Roos
4. Learning to See - Mike Rother & John Shook
5. The Goal - Eliyahu Goldratt

**Otros recursos:**
- Papers académicos sobre Lean
- Casos de estudio de empresas
- Manuales de 5S, Kaizen, TPM
- Artículos de Lean Enterprise Institute

### Paso 2: Añadir PDFs

```bash
# Copiar PDFs a la carpeta de conocimiento
cp mi_libro_lean.pdf backend/data/knowledge_base/
```

### Paso 3: Ejecutar script de ingestión

```bash
# Desde la raíz del proyecto
python scripts/ingest_documents.py
```

Output esperado:
```
🏭 Lean AI Assistant - Document Ingestion
==================================================
Connecting to Qdrant at localhost:6333...
Loading embeddings model: sentence-transformers/all-MiniLM-L6-v2...
Collection 'lean_knowledge' already exists

Found 3 PDF files
--------------------------------------------------
Processing: toyota_production_system.pdf
Creating embeddings: 100%|████████| 245/245 [00:15<00:00]
✅ Added 245 chunks from toyota_production_system.pdf

Processing: lean_thinking.pdf
Creating embeddings: 100%|████████| 312/312 [00:18<00:00]
✅ Added 312 chunks from lean_thinking.pdf

Processing: learning_to_see.pdf
Creating embeddings: 100%|████████| 189/189 [00:11<00:00]
✅ Added 189 chunks from learning_to_see.pdf

==================================================
✅ Ingestion complete!
Total documents: 3
Total chunks: 746
Collection: lean_knowledge
Points in collection: 746
```

### Paso 4: Verificar

```bash
# Acceder a Qdrant UI
open http://localhost:6333/dashboard

# O verificar vía API
curl http://localhost:8000/api/knowledge/stats
```

## 🧪 Testing

### Test básico del chat
```python
# test_basic_chat.py
import requests

def test_chat():
    response = requests.post(
        "http://localhost:8000/api/chat",
        json={"message": "¿Qué es Lean?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 0
    print("✅ Chat test passed")

if __name__ == "__main__":
    test_chat()
```

### Test calculadoras
```python
def test_oee():
    response = requests.post(
        "http://localhost:8000/api/calculate/oee",
        json={
            "availability": 90,
            "performance": 95,
            "quality": 99
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "oee" in data
    expected_oee = 90 * 0.95 * 0.99
    assert abs(data["oee"] - expected_oee) < 0.01
    print("✅ OEE test passed")
```

## 🐛 Troubleshooting

### Problema: Backend no se conecta a Qdrant

**Solución:**
```bash
# Verificar que Qdrant está corriendo
docker ps | grep qdrant

# Ver logs de Qdrant
docker-compose logs qdrant

# Reiniciar servicios
docker-compose restart
```

### Problema: "OpenAI API key not found"

**Solución:**
1. Verificar que el archivo `.env` existe
2. Verificar que `OPENAI_API_KEY` está definido
3. Reiniciar el backend:
```bash
docker-compose restart backend
```

### Problema: No hay documentos en la base de conocimientos

**Solución:**
```bash
# Verificar que hay PDFs
ls backend/data/knowledge_base/

# Ejecutar script de ingestión
python scripts/ingest_documents.py

# Verificar en Qdrant
curl http://localhost:8000/api/knowledge/stats
```

### Problema: Frontend no se conecta al backend

**Solución:**
1. Verificar que ambos están corriendo:
```bash
docker-compose ps
```

2. Verificar variables de entorno del frontend:
```bash
docker-compose logs frontend | grep BACKEND_URL
```

## 📊 Monitoreo

### Ver logs en tiempo real
```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### Verificar salud de servicios
```bash
# Backend
curl http://localhost:8000/health

# Qdrant
curl http://localhost:6333/

# Redis
docker exec -it lean-ai-assistant_redis_1 redis-cli ping
```

## 🎯 Casos de Uso Reales

### Caso 1: Consultor Lean
"Uso el asistente para generar explicaciones personalizadas 
para mis clientes sobre conceptos Lean específicos."

### Caso 2: Ingeniero de Mejora Continua
"Calculo OEE rápidamente y obtengo recomendaciones específicas 
basadas en mis números."

### Caso 3: Estudiante
"Estudio para mi certificación Lean Six Sigma y uso el chat 
para repasar conceptos y obtener ejemplos prácticos."

### Caso 4: Gerente de Producción
"Analizo mis procesos y obtengo sugerencias de mejora basadas 
en mejores prácticas de la industria."
