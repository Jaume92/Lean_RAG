import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes
from app.core.config import settings
from app.services.rag_service import RAGService

app = FastAPI(
    title="Lean AI Assistant",
    description="AI-powered assistant for Lean Manufacturing expertise",
    version="0.1.0"
)

# 🔹 Instancia global del RAG (warm memory)
rag_service = RAGService()


# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Routers =====
app.include_router(routes.router, prefix="/api", tags=["api"])


# ===== ROOT =====
@app.get("/")
async def root():
    return {
        "message": "Lean AI Assistant API",
        "version": "0.1.0",
        "status": "running"
    }


# ===== HEALTH CHECK PRO =====
@app.get("/health")
async def health_check():
    start = time.time()

    try:
        stats = await rag_service.get_knowledge_stats()
        status = "healthy"
    except Exception:
        stats = {}
        status = "degraded"

    latency_ms = round((time.time() - start) * 1000, 2)

    return {
        "status": status,
        "latency_ms": latency_ms,
        "rag_collection": stats.get("collection_name"),
        "documents": stats.get("total_points", 0),
        "version": "0.1.0"
    }


# ===== WARM START (CLAVE PARA RENDER) =====
@app.on_event("startup")
async def startup_event():
    """
    Preload embeddings + vector DB connection.
    Esto evita primera respuesta lenta en producción.
    """
    try:
        _ = rag_service.embedder.encode("warmup")
        await rag_service.get_knowledge_stats()
        print("🔥 RAG warm-up completado")
    except Exception as e:
        print("⚠️ Warm-up parcial:", e)


# ===== LOCAL RUN =====
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
