from sqlalchemy import Column, String, Text
from app.db.database import Base


class WorkflowRequestDB(Base):

    __tablename__ = "workflow_requests"

    request_id = Column(String, primary_key=True, index=True)

    workflow_name = Column(String)

    status = Column(String)

    decision = Column(String)

    history = Column(Text)