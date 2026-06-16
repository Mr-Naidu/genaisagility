import json
import time
import google.generativeai as genai
from app.core.config import get_settings
from app.core.logging import logger
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

# Use gemini-2.0-flash-lite — higher free-tier rate limit (30 req/min vs 5)
MODEL_NAME = "gemini-2.0-flash-lite"

# Retry settings for rate limit errors
MAX_RETRIES = 3
BASE_WAIT_SECONDS = 10

def _call_with_retry(model, prompt: str) -> str:
    """Calls Gemini with automatic retry on rate limit (429) errors."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                wait_time = BASE_WAIT_SECONDS * attempt  # 10s, 20s, 30s
                logger.warning(
                    f"Rate limit hit (attempt {attempt}/{MAX_RETRIES}). "
                    f"Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)
            else:
                raise  # Not a rate limit error, raise immediately
    raise ValueError(
        "Rate limit exceeded after multiple retries. "
        "Please wait a moment and try again."
    )

async def classify_email_with_llm(email_content: str) -> ClassifyResponse:
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")
    
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=CLASSIFY_EMAIL_SYSTEM_PROMPT,
        generation_config={"response_mime_type": "application/json"}
    )
    
    prompt = get_classify_prompt(email_content)
    response_text = _call_with_retry(model, prompt)
    
    try:
        data = json.loads(response_text)
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
    response_text = _call_with_retry(model, prompt)
    
    try:
        data = json.loads(response_text)
        return RewriteResponse(**data)
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON.")
