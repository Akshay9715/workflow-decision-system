from pydantic import BaseModel
from typing import Dict, Any

class WorkflowRequest(BaseModel):
    workflow_name: str
    request_id: str
    data: Dict[str, Any]