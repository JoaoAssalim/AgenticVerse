import pytest
import json

from database.models import AgentModel, UserModel
from core.api import UsersAPIView, AgentsAPIView

@pytest.fixture
def user_test() -> UserModel:
    user_data_test = {
        "name": "User Test",
        "email": "test@test.com",
        "password": "UserTest123"
    }   
    
    user_data_test_string = json.dumps(user_data_test)
    user_test_db = UserModel.model_validate_json(user_data_test_string)
    user_test = UsersAPIView().create_user(user_test_db)
    
    yield user_test

    UsersAPIView().delete_user(str(user_test.id))

@pytest.fixture
def agent_test(user_test) -> AgentModel:
    agent_data_test = {
        "name": "Agent Test",
        "description": "Agent test",
        "system_prompt": "Test agent",
        "tools": [],
        "provider": "openai"
    }   

    agent_data_test_string = json.dumps(agent_data_test)
    agent_test_db = AgentModel.model_validate_json(agent_data_test_string)
    agent_test = AgentsAPIView().create_agent(agent_test_db, user_test.id)
    
    yield agent_test

    AgentsAPIView().delete_agent(str(agent_test.id), user_test.id)

@pytest.fixture
def agent_data_creation():
    return {
        "name": "Agent Test 2",
        "description": "Agent test 2",
        "system_prompt": "Test agent 2",
        "tools": [],
        "provider": "openai"
    } 

@pytest.fixture
def agent_data_update():
    return {
        "name": "Agent Test 3",
    }  