# services/generation-service/app/main.py (excerpt)
import os
import boto3 # Make sure boto3 is in your requirements.txt
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger("generation_service")

secrets_client = boto3.client('secretsmanager', region_name=os.getenv("AWS_REGION", "us-west-2"))

def get_secret(secret_arn):
    try:
        get_secret_value_response = secrets_client.get_secret_value(SecretId=secret_arn)
    except ClientError as e:
        logger.error(f"Error retrieving secret '{secret_arn}': {e}")
        # Depending on criticality, you might exit, raise, or use a fallback
        raise RuntimeError(f"Could not retrieve secret from Secrets Manager: {e}") from e
    else:
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        # Handle binary secrets if needed: elif 'SecretBinary' in get_secret_value_response:
        # return get_secret_value_response['SecretBinary']

# Global variable to store the retrieved API key (on startup)
LLM_API_KEY = None

@app.on_event("startup")
async def startup_event():
    global LLM_API_KEY
    llm_api_key_secret_arn = os.getenv("LLM_API_KEY_SECRET_ARN") # Read ARN from env var
    if not llm_api_key_secret_arn:
        logger.error("LLM_API_KEY_SECRET_ARN environment variable not set. LLM initialization skipped.")
        return # Or raise HTTPException if startup must fail

    try:
        LLM_API_KEY = get_secret(llm_api_key_secret_arn)
        logger.info("LLM API key retrieved from Secrets Manager successfully.")
        # Initialize LLM only if key is successfully retrieved
        global llm
        llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=LLM_API_KEY) # Assuming ChatOpenAI is imported
        logger.info("LLM initialized.")
    except RuntimeError as e:
        logger.critical(f"Failed to initialize LLM: {e}")
        llm = None # Indicate LLM is not ready
    except Exception as e: # Catch any other unexpected errors during LLM init
        logger.critical(f"An unexpected error occurred during LLM initialization: {e}")
        llm = None

# ... rest of your FastAPI app ...
