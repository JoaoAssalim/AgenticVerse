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
        try:
            agent.user_id = user_id
            with Session(engine) as session:
                session.add(agent)
                session.commit()
                session.refresh(agent)
                return agent
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error to create agent: {e}")
        
    def get_agent(self, agent_id: str, user_id: str):
        try:
            with Session(engine) as session:
                agent_db = session.get(AgentModel, uuid.UUID(agent_id))

                if not agent_db:
                    raise HTTPException(status_code=404, detail="Agent not found")

                if str(agent_db.user_id) != str(user_id):
                    raise HTTPException(status_code=403, detail="Forbidden")
                
                return agent_db
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error to get agent {agent_id}: {e}")
    
    def get_all_agents(self, user_id: str):
        try:
            with Session(engine) as session:
                agents = session.exec(select(AgentModel).where(AgentModel.user_id == user_id)).all()
                return agents
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error to get all agent: {e}")
    
    def update_agent(self, agent_id: str, agent: AgentModel, user_id: str):
        try:
            with Session(engine) as session:
                agent_db = session.get(AgentModel, uuid.UUID(agent_id))
                
                if not agent_db:
                    raise HTTPException(status_code=404, detail="Agent not found")
                
                if str(agent_db.user_id) != str(user_id):
                    raise HTTPException(status_code=403, detail="Forbidden")
                
                agent_data = agent.model_dump(exclude_unset=True, exclude=["api_key"])
                agent_data["updated_at"] = datetime.now()
                agent_db.sqlmodel_update(agent_data)
                session.add(agent_db)
                session.commit()
                session.refresh(agent_db)
                return agent_db
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error to update agent {agent_id}: {e}")
    
    def delete_agent(self, agent_id: str, user_id: str):
        try:
            with Session(engine) as session:
                agent_db = session.get(AgentModel, uuid.UUID(agent_id))

                if not agent_db:
                    raise HTTPException(status_code=404, detail="Agent not found")
                
                if str(agent_db.user_id) != str(user_id):
                    raise HTTPException(status_code=403, detail="Forbidden")
                
                session.delete(agent_db)
                session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error to delete agent {agent_id}: {e}")