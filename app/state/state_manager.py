import json
from app.db.database import SessionLocal
from app.db.models import WorkflowRequestDB


class StateManager:

    def create_request(self, request_id, workflow_name):

        db = SessionLocal()

        record = WorkflowRequestDB(
            request_id=request_id,
            workflow_name=workflow_name,
            status="received",
            decision=None,
            history=json.dumps(["received"])
        )

        db.add(record)
        db.commit()
        db.close()

    def update_state(self, request_id, new_state):

        db = SessionLocal()

        record = db.query(WorkflowRequestDB).filter(
            WorkflowRequestDB.request_id == request_id
        ).first()

        history = json.loads(record.history)

        history.append(new_state)

        record.status = new_state
        record.history = json.dumps(history)

        db.commit()
        db.close()

    def complete(self, request_id, decision):

        db = SessionLocal()

        record = db.query(WorkflowRequestDB).filter(
            WorkflowRequestDB.request_id == request_id
        ).first()

        record.decision = decision

        db.commit()
        db.close()

    def get_request(self, request_id):

        db = SessionLocal()

        record = db.query(WorkflowRequestDB).filter(
            WorkflowRequestDB.request_id == request_id
        ).first()

        db.close()

        return record