from fastapi import APIRouter, Query
from app.services.apis.yahoo import search_yahoo_finance

router = APIRouter()

@router.get("/enlighten")
async def enlighten(company: str = Query(...)):
    suggestions = search_yahoo_finance(company)
    return {"original_query": company, "candidates": suggestions}
