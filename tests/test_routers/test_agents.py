import uuid
import json

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

def test_create_and_delete_agent(user_test, agent_data_creation):
    response = client.post(
        "agent/create", 
        data=json.dumps(agent_data_creation), 
        headers={
            "x-api-key": str(user_test.api_key),
            "accept": "application/json"
        }
    )

    data = json.loads(response.text)

    assert response.status_code == 200
    assert data["name"] == "Agent Test 2"

    response = client.delete(
        f"agent/delete/{data["id"]}", 
        headers={
            "x-api-key": str(user_test.api_key)
        }
    )

    assert response.status_code == 200

def test_create_agent_unauthorized_with_invalid_api_key(agent_data_creation):
    response = client.post(
        "agent/create", 
        data=json.dumps(agent_data_creation), 
        headers={
            "x-api-key": str(uuid.uuid4()),
            "accept": "application/json"
        }
    )

    assert response.status_code == 401

def test_update_agent(user_test, agent_test, agent_data_update):
    response = client.patch(
        f"agent/update/{str(agent_test.id)}", 
        data=json.dumps(agent_data_update), 
        headers={
            "x-api-key": str(user_test.api_key),
            "accept": "application/json"
        }
    )

    data = json.loads(response.text)

    assert response.status_code == 200
    assert data["name"] == "Agent Test 3"

def test_update_agent_unauthorized_with_invalid_api_key(agent_test, agent_data_update):
    response = client.patch(
        f"agent/update/{str(agent_test.id)}", 
        data=json.dumps(agent_data_update), 
        headers={
            "x-api-key": str(uuid.uuid4()),
            "accept": "application/json"
        }
    )

    assert response.status_code == 401