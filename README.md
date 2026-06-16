# Smart Email Classifier & Rewriter

This is a FastAPI-based microservice that leverages Generative AI (Google Gemini 2.5 Flash) to classify and rewrite emails.

## Features

*   **Email Classification** (`/api/v1/classify_email`): Categorizes emails into Work, Personal, Finance, or Spam.
*   **Email Rewriting** (`/api/v1/rewrite_email`): Rewrites emails into specified tones (Professional, Friendly, Formal, Casual).

## Project Structure

This project follows an industry-standard layout:

*   `app/main.py`: FastAPI application setup.
*   `app/api/endpoints.py`: API route definitions.
*   `app/core/config.py`: Environment and configuration management.
*   `app/models/schemas.py`: Pydantic data validation schemas.
*   `app/services/llm_service.py`: Integration with the Gemini API.
*   `app/prompts/templates.py`: Prompt templates for Gen-AI models.

## Setup Instructions

1.  **Clone the repository** (if applicable) or navigate to the project directory.
2.  **Set up a virtual environment**:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On Mac/Linux
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables**:
    Create a `.env` file in the root directory (you can use the provided template or just add the key directly):
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```
5.  **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```
6.  **Access Swagger UI**:
    Open your browser and navigate to `http://127.0.0.1:8000/docs` to test the API.

## API Usage Examples

### Classify Email
**Endpoint**: `POST /api/v1/classify_email`

**Request Body**:
```json
{
  "email_content": "Hey team, just a reminder that the Q3 project deadline is this Friday. Let's make sure all pull requests are reviewed by tomorrow."
}
```

**Response**:
```json
{
  "category": "Work",
  "confidence": 0.95,
  "reasoning": "The email discusses a project deadline and pull requests, which are clearly work-related tasks."
}
```

### Rewrite Email
**Endpoint**: `POST /api/v1/rewrite_email`

**Request Body**:
```json
{
  "email_content": "Give me the report now. I need it.",
  "desired_tone": "Professional"
}
```

**Response**:
```json
{
  "original_tone": "Demanding and abrupt",
  "rewritten_content": "Could you please provide the report at your earliest convenience? I need it as soon as possible. Thank you."
}
```
