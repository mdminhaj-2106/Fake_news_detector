import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.text_verifier.verifier import verify_news



router = APIRouter()

class ClaimRequest(BaseModel):
    claim: str

@router.post("/processText")
async def process_text(req: ClaimRequest):
    try:
        result = verify_news(req.claim)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))