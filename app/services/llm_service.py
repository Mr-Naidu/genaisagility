import json
import google.generativeai as genai
from app.core.config import get_settings
from app.models.schemas import ClassifyResponse, RewriteResponse
from app.prompts.templates import (
    CLASSIFY_EMAIL_SYSTEM_PROMPT,
    REWRITE_EMAIL_SYSTEM_PROMPT,
    get_classify_prompt,
    get_rewrite_prompt
)

settings = get_settings()

# Initialize Gemini API if key is available
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

# Use gemini-2.5-flash as it is fast, cheap, and supports structured JSON outputs well
MODEL_NAME = "gemini-2.5-flash"

async def classify_email_with_llm(email_content: str) -> ClassifyResponse:
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")
    
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=CLASSIFY_EMAIL_SYSTEM_PROMPT,
        generation_config={"response_mime_type": "application/json"}
    )
    
    prompt = get_classify_prompt(email_content)
    # The SDK is synchronous by default, but we can wrap it or just use it.
    # In a real async environment, we might use run_in_executor. 
    # For now, generate_content runs synchronously but fast.
    response = model.generate_content(prompt)
    
    try:
        data = json.loads(response.text)
        return ClassifyResponse(**data)
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON.")

async def rewrite_email_with_llm(email_content: str, desired_tone: str) -> RewriteResponse:
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")
        
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=REWRITE_EMAIL_SYSTEM_PROMPT,
        generation_config={"response_mime_type": "application/json"}
    )
    
    prompt = get_rewrite_prompt(email_content, desired_tone)
    response = model.generate_content(prompt)
    
    try:
        data = json.loads(response.text)
        return RewriteResponse(**data)
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON.")
