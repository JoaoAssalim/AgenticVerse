import uuid

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_all_agents(user_test):
    response = client.get("agent/get-all", headers={"x-api-key": str(user_test.api_key)})
    assert response.status_code == 200

def test_get_all_agents_unauthorized_with_invalid_api_key():
    response = client.get("agent/get-all", headers={"x-api-key": str(uuid.uuid4())})
    assert response.status_code == 401

def test_get_agent(user_test, agent_test):
    response = client.get(f"agent/get/{str(agent_test.id)}", headers={"x-api-key": str(user_test.api_key)})
    assert response.status_code == 200

def test_get_agent_unauthorized_with_invalid_api_key(agent_test):
    response = client.get(f"agent/get/{str(agent_test.id)}", headers={"x-api-key": str(uuid.uuid4())})
    assert response.status_code == 401