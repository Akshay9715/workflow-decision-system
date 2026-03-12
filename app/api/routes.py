from fastapi import APIRouter
from .models import WorkflowRequest
from app.engine.workflow_engine import WorkflowEngine

router = APIRouter()

engine = WorkflowEngine()


@router.post("/process")
def process_request(request: WorkflowRequest):

    result = engine.process(
        request.request_id,
        request.workflow_name,
        request.data
    )

    return {
        "request_id": request.request_id,
        "decision": result["decision"],
        "rule_triggered": result["rule_triggered"],
        "explanation": result["explanation"]
    }