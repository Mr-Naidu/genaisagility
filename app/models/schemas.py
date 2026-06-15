from pydantic import BaseModel, Field
from enum import Enum

# Enums for strict validation
class EmailCategory(str, Enum):
    WORK = "Work"
    PERSONAL = "Personal"
    FINANCE = "Finance"
    SPAM = "Spam"

class RewriteTone(str, Enum):
    PROFESSIONAL = "Professional"
    FRIENDLY = "Friendly"
    FORMAL = "Formal"
    CASUAL = "Casual"

# Request & Response Models for /classify_email
class ClassifyRequest(BaseModel):
    email_content: str = Field(..., description="The raw content of the email to classify")

class ClassifyResponse(BaseModel):
    category: EmailCategory = Field(..., description="The predicted category of the email")
    confidence: float = Field(..., description="Confidence score from the LLM (0.0 to 1.0)", ge=0.0, le=1.0)
    reasoning: str = Field(..., description="Brief reasoning behind the classification")

# Request & Response Models for /rewrite_email
class RewriteRequest(BaseModel):
    email_content: str = Field(..., description="The raw content of the email to rewrite")
    desired_tone: RewriteTone = Field(..., description="The target tone for the rewritten email")

class RewriteResponse(BaseModel):
    original_tone: str = Field(..., description="The inferred tone of the original email")
    rewritten_content: str = Field(..., description="The rewritten email content")
