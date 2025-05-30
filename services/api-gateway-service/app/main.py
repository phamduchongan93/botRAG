# services/api-gateway-service/app/main.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import httpx # For making asynchronous HTTP requests to other services
import os

# --- FastAPI App Initialization ---
app = FastAPI(
    title="OmniRAG API Gateway Service",
    description="Orchestrates chatbot interactions by routing queries to Retrieval and Generation services.",
    version="1.0.0"
)

# --- Configuration (from Environment Variables) ---
# Use Kubernetes Service names for internal communication
RETRIEVAL_SERVICE_URL = os.getenv("RETRIEVAL_SERVICE_URL", "http://omnirag-retrieval-service:8000")
GENERATION_SERVICE_URL = os.getenv("GENERATION_SERVICE_URL", "http://omnirag-generation-service:8000")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO") # Example: For logging configuration

# Basic logging setup (you'd typically use a proper logging library in production)
import logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper()), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("api_gateway_service")

# --- Pydantic Models for Request/Response ---
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

class ErrorResponse(BaseModel):
    detail: str

# --- Health Check Endpoint ---
@app.get("/", summary="Health Check", response_model=dict)
async def health_check():
    """
    Returns the health status of the API Gateway Service.
    """
    logger.info("Health check endpoint hit.")
    return {"status": "API Gateway is healthy", "service": "omnirag-api-gateway"}

# --- Main Chat Endpoint ---
@app.post(
    "/chat",
    summary="Chat with OmniRAG Bot",
    response_model=ChatResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Invalid Input"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal Server Error"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ErrorResponse, "description": "Dependent Service Unavailable"}
    }
)
async def chat_with_bot(request: ChatRequest):
    """
    Processes a user's natural language query and returns an AI-generated answer.
    """
    user_query = request.query.strip()
    if not user_query:
        logger.warning("Received empty query.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Query cannot be empty.")

    logger.info(f"Received query: '{user_query}'")

    try:
        # 1. Call Retrieval Service to get context
        async with httpx.AsyncClient() as client:
            logger.debug(f"Calling Retrieval Service: {RETRIEVAL_SERVICE_URL}/retrieve")
            retrieval_response = await client.post(
                f"{RETRIEVAL_SERVICE_URL}/retrieve",
                json={"query": user_query},
                timeout=10 # Set a timeout for the request
            )
            retrieval_response.raise_for_status() # Raise an exception for 4xx/5xx responses
            context = retrieval_response.json().get("context", [])

        if not context:
            logger.info(f"No relevant context found for query: '{user_query}'")
            return ChatResponse(answer="I couldn't find relevant information in my knowledge base. Please try rephrasing your question.")

        logger.debug(f"Retrieved context length: {len(''.join(context))} characters.")

        # 2. Call Generation Service to get the answer
        async with httpx.AsyncClient() as client:
            logger.debug(f"Calling Generation Service: {GENERATION_SERVICE_URL}/generate")
            generation_response = await client.post(
                f"{GENERATION_SERVICE_URL}/generate",
                json={"query": user_query, "context": context},
                timeout=30 # Generation can take longer, set appropriate timeout
            )
            generation_response.raise_for_status()
            answer = generation_response.json().get("answer", "Error: Could not generate an answer.")

        logger.info(f"Successfully processed query: '{user_query}'")
        return ChatResponse(answer=answer)

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Error calling downstream service: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Downstream service error: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Network error calling downstream service: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Cannot connect to a required service. Please try again later. ({str(e)})"
        )
    except Exception as e:
        logger.exception(f"An unexpected error occurred while processing query: '{user_query}'")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected internal error occurred: {str(e)}"
        )

# --- Uvicorn Entry Point (for running the app) ---
if __name__ == "__main__":
    import uvicorn
    # When running locally via 'python main.py', use a .env file or direct env vars
    # In Kubernetes, these are set by Deployment.
    uvicorn.run(app, host="0.0.0.0", port=8000)
