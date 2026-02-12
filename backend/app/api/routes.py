from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from app.services.rag_service import RAGService
from app.services.calculator import LeanCalculator, OEEInput
from app.core.config import settings

router = APIRouter()

# Initialize services
rag_service = RAGService()
calculator = LeanCalculator()

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict] = []

class TaktTimeRequest(BaseModel):
    available_time_minutes: float
    customer_demand_units: int

# Chat endpoint
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - answers Lean Manufacturing questions using RAG
    """
    try:
        response = await rag_service.answer_with_context(request.message)
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Calculator endpoints
@router.post("/calculate/oee")
async def calculate_oee(input: OEEInput):
    """
    Calculate Overall Equipment Effectiveness (OEE)
    """
    try:
        result = calculator.calculate_oee(input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calculate/takt-time")
async def calculate_takt_time(input: TaktTimeRequest):
    """
    Calculate Takt Time
    """
    try:
        result = calculator.calculate_takt_time(
            input.available_time_minutes,
            input.customer_demand_units
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calculate/lead-time")
async def calculate_lead_time(process_steps: List[dict]):
    """
    Calculate Lead Time from process steps
    """
    try:
        result = calculator.calculate_lead_time(process_steps)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Knowledge base endpoints
@router.get("/knowledge/stats")
async def get_knowledge_stats():
    """
    Get statistics about the knowledge base
    """
    try:
        stats = await rag_service.get_knowledge_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
