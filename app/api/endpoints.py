from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    ClassifyRequest, 
    ClassifyResponse, 
    RewriteRequest, 
    RewriteResponse
)
from app.services.llm_service import classify_email_with_llm, rewrite_email_with_llm

router = APIRouter()

@router.post("/classify_email", response_model=ClassifyResponse, summary="Classify an email")
async def classify_email(request: ClassifyRequest):
    """
    Classifies the given email content into Work, Personal, Finance, or Spam.
    """
    try:
        response = await classify_email_with_llm(request.email_content)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rewrite_email", response_model=RewriteResponse, summary="Rewrite an email")
async def rewrite_email(request: RewriteRequest):
    """
    Rewrites the given email into the desired tone (Professional, Friendly, Formal, Casual).
    """
    try:
        response = await rewrite_email_with_llm(request.email_content, request.desired_tone)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
