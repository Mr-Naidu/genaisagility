import json
import time
from groq import Groq
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

# Initialize Groq client
client = None
if settings.GROQ_API_KEY:
    client = Groq(api_key=settings.GROQ_API_KEY)

# Using Llama-3-8b-8192 which is extremely fast and free on Groq
MODEL_NAME = "llama-3.3-70b-versatile"

# Retry settings for rate limit errors
MAX_RETRIES = 3
BASE_WAIT_SECONDS = 5

def _call_with_retry(system_prompt: str, user_prompt: str) -> str:
    """Calls Groq with automatic retry on rate limit (429) errors."""
    if not client:
        raise ValueError("GROQ_API_KEY is not set.")
        
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
                model=MODEL_NAME,
                response_format={"type": "json_object"},
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "rate limit" in error_msg.lower():
                wait_time = BASE_WAIT_SECONDS * attempt
                logger.warning(
                    f"Rate limit hit (attempt {attempt}/{MAX_RETRIES}). "
                    f"Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)
            else:
                raise
    raise ValueError(
        "Rate limit exceeded after multiple retries. "
        "Please wait a moment and try again."
    )

async def classify_email_with_llm(email_content: str) -> ClassifyResponse:
    prompt = get_classify_prompt(email_content)
    response_text = _call_with_retry(CLASSIFY_EMAIL_SYSTEM_PROMPT, prompt)
    
    try:
        data = json.loads(response_text)
        return ClassifyResponse(**data)
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON.")

async def rewrite_email_with_llm(email_content: str, desired_tone: str) -> RewriteResponse:
    prompt = get_rewrite_prompt(email_content, desired_tone)
    response_text = _call_with_retry(REWRITE_EMAIL_SYSTEM_PROMPT, prompt)
    
    try:
        data = json.loads(response_text)
        return RewriteResponse(**data)
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON.")
