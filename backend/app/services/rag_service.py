from typing import List, Dict
import os

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Filter

from app.core.config import settings
from app.services.llm_service import LLMService


class RAGService:
    """
    Retrieval-Augmented Generation service optimized for low latency.
    """

    def __init__(self):
        # 🔹 LLM service
        self.llm_service = LLMService()

        # 🔹 Load embeddings ONCE (critical for speed)
        self.embedder = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        # 🔹 Persistent Qdrant client
        self.qdrant = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )

    async def retrieve_context(self, query: str, k: int = None) -> List[Dict]:
        """
        Retrieve relevant context from Qdrant vector DB.
        """
        if k is None:
            k = settings.RAG_TOP_K

        # 🔹 Embed query
        query_vector = self.embedder.encode(query).tolist()

        # 🔹 Vector search
        results = self.qdrant.search(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=k
        )

        # 🔹 Format docs
        docs = []
        for r in results:
            payload = r.payload or {}
            docs.append({
                "content": payload.get("content", ""),
                "metadata": payload.get("metadata", {})
            })

        return docs

    async def answer_with_context(self, query: str) -> Dict:
        """
        Generate Lean expert answer using retrieved context.
        """

        context_docs = await self.retrieve_context(query)

        if context_docs:
            context_text = "\n\n".join(
                [f"Fuente {i+1}:\n{doc['content']}" for i, doc in enumerate(context_docs)]
            )

            prompt = f"""
Eres un experto en Lean Manufacturing.

Contexto:
{context_text}

Pregunta:
{query}

Responde de forma clara, práctica y directa, con ejemplos industriales reales.
"""
        else:
            prompt = f"""
Eres un experto en Lean Manufacturing.
Responde de forma clara, rápida y práctica:

{query}
"""

        system_prompt = """
Ingeniero Lean industrial experto.
Respuestas breves, accionables y útiles en planta.
Tono directo con ligero humor y se sarcastico , si te preguntan prioriza practica sobre teoria 
"""

        answer = await self.llm_service.generate(
            prompt=prompt,
            system_prompt=system_prompt
        )

        sources = [
            {
                "content": doc.get("content", "")[:200] + "...",
                "metadata": doc.get("metadata", {})
            }
            for doc in context_docs
        ]

        return {
            "answer": answer,
            "sources": sources
        }

    async def get_knowledge_stats(self) -> Dict:
        """
        Basic stats from Qdrant.
        """
        try:
            info = self.qdrant.get_collection(settings.QDRANT_COLLECTION_NAME)
            return {
                "total_points": info.points_count,
                "collection_name": settings.QDRANT_COLLECTION_NAME,
                "status": "ready"
            }
        except Exception:
            return {
                "total_points": 0,
                "collection_name": settings.QDRANT_COLLECTION_NAME,
                "status": "collection not found"
            }
