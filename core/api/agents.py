import uuid
from datetime import datetime

from sqlmodel import Session, select
from fastapi import HTTPException

from database.config import engine
from database.models.agent import AgentModel

class AgentsAPIView:
    def __init__(self):
        pass

    def create_agent(self, agent: AgentModel, user_id: str):
        agent.user_id = user_id
        with Session(engine) as session:
            session.add(agent)
            session.commit()
            session.refresh(agent)
            return agent
        
    def get_agent(self, agent_id: str, user_id: str):
        with Session(engine) as session:
            agent_db = session.get(AgentModel, uuid.UUID(agent_id))

            if not agent_db:
                raise HTTPException(status_code=404, detail="Agent not found")

            if agent_db.user_id != user_id:
                raise HTTPException(status_code=403, detail="Forbidden")
            
            return agent_db
    
    def get_all_agents(self, user_id: str):
        with Session(engine) as session:
            agents = session.exec(select(AgentModel).where(AgentModel.user_id == user_id)).all()
            return agents
    
    def update_agent(self, agent_id: str, agent: AgentModel, user_id: str):
        with Session(engine) as session:
            agent_db = session.get(AgentModel, uuid.UUID(agent_id))
            
            if not agent_db:
                raise HTTPException(status_code=404, detail="Agent not found")
            
            if agent_db.user_id != uuid.UUID(user_id):
                raise HTTPException(status_code=403, detail="Forbidden")
            
            agent_data = agent.model_dump(exclude_unset=True, exclude=["api_key"])
            agent_data["updated_at"] = datetime.now()
            agent_db.sqlmodel_update(agent_data)
            session.add(agent_db)
            session.commit()
            session.refresh(agent_db)
            return agent_db
    
    def delete_agent(self, agent_id: str, user_id: str):
        with Session(engine) as session:
            agent_db = session.get(AgentModel, uuid.UUID(agent_id))

            if not agent_db:
                raise HTTPException(status_code=404, detail="Agent not found")
            
            if agent_db.user_id != user_id:
                raise HTTPException(status_code=403, detail="Forbidden")
            
            session.delete(agent_db)
            session.commit()