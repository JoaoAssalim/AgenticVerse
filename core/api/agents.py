import uuid
from datetime import datetime

from sqlmodel import Session, select
from fastapi import HTTPException

from database.config import engine
from database.models.agent import AgentModel

class AgentsAPIView:
    def __init__(self):
        pass

    def create_agent(self, agent: AgentModel):
        with Session(engine) as session:
            session.add(agent)
            session.commit()
            session.refresh(agent)
            return agent
        
    def get_agent(self, agent_id: str):
        with Session(engine) as session:
            agent = session.get(AgentModel, uuid.UUID(agent_id))
            if not agent:
                raise HTTPException(status_code=404, detail="Agent not found")
            return agent
    
    def get_all_agents(self):
        with Session(engine) as session:
            agents = session.exec(select(AgentModel)).all()
            return agents
    
    def update_agent(self, agent_id: str, agent: AgentModel):
        with Session(engine) as session:
            agent_db = session.get(AgentModel, uuid.UUID(agent_id))
            
            if not agent:
                raise HTTPException(status_code=404, detail="Agent not found")
            
            agent_data = agent.model_dump(exclude_unset=True, exclude=["api_key"])
            agent_data["updated_at"] = datetime.now()
            agent_db.sqlmodel_update(agent_data)
            session.add(agent_db)
            session.commit()
            session.refresh(agent_db)
            return agent_db
    
    def delete_agent(self, agent_id: str):
        with Session(engine) as session:
            session.delete(session.get(AgentModel, uuid.UUID(agent_id)))
            session.commit()