# services/api-gateway-service/tests/test_api_gateway.py
from fastapi.testclient import TestClient
# Assuming your FastAPI app object is named 'app' in main.py
from services.api-gateway-service.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API Gateway is healthy"}

def test_chat_empty_query():
    response = client.post("/chat", json={"query": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Query cannot be empty"

# --- More advanced tests would involve mocking ---
import pytest
from unittest.mock import patch # For mocking external dependencies

# Example of testing the /chat endpoint by mocking downstream services
def test_chat_success_with_mocks():
    # Mock the httpx.AsyncClient.post method to control its return values
    with patch("httpx.AsyncClient.post") as mock_post:
        # Configure mock_post for the retrieval service call
        mock_post.side_effect = [
            # First call (retrieval service)
            pytest.mock.Mock(
                status_code=200,
                json=lambda: {"context": ["Kubernetes is an orchestration system."]},
                raise_for_status=lambda: None
            ),
            # Second call (generation service)
            pytest.mock.Mock(
                status_code=200,
                json=lambda: {"answer": "Kubernetes helps manage containers."},
                raise_for_status=lambda: None
            )
        ]

        response = client.post("/chat", json={"query": "What is Kubernetes?"})
        assert response.status_code == 200
        assert response.json()["answer"] == "Kubernetes helps manage containers."

        # Verify that the downstream services were called as expected
        assert mock_post.call_count == 2
        assert "retrieve" in mock_post.call_args_list[0].args[0]
        assert "generate" in mock_post.call_args_list[1].args[0]
