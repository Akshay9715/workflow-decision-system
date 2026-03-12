from app.config.config_loader import load_workflows
from app.rules.rule_engine import RuleEngine
from app.state.state_manager import StateManager
from app.audit.audit_logger import log_decision
import time

MAX_RETRIES = 3


class WorkflowEngine:

    def __init__(self):

        self.workflows = load_workflows()
        self.rule_engine = RuleEngine()
        self.state_manager = StateManager()

    def process(self, request_id, workflow_name, data):

        # -------- IDPOTENCY CHECK --------
        existing = self.state_manager.get_request(request_id)

        if existing:
            return {
                "decision": existing.decision,
                "rule_triggered": None,
                "explanation" : "Duplicate request detected",
                "message": "Duplicate request detected"
            }

        # -------- WORKFLOW VALIDATION --------
        if workflow_name not in self.workflows:
            raise ValueError("Workflow not found")

        # -------- CREATE REQUEST --------
        self.state_manager.create_request(
            request_id,
            workflow_name
        )

        steps = self.workflows[workflow_name]["steps"]

        decision = None
        triggered_rule = None
        explanation = None

        # -------- WORKFLOW EXECUTION --------
        for step in steps:

            self.state_manager.update_state(request_id, step)

            if step == "rule_check":

                retries = 0

                while retries < MAX_RETRIES:

                    try:

                        result = self.rule_engine.evaluate(
                            workflow_name,
                            data
                        )

                        decision = result["decision"]
                        triggered_rule = result["rule_id"]
                        explanation = result["explanation"]

                        break

                    except Exception:

                        retries += 1
                        time.sleep(1) # This simulates real retry behavior.
                        # record retry attempt in history
                        self.state_manager.update_state(
                            request_id,
                            f"rule_check_attempt_{retries}"
                        )

                        if retries == MAX_RETRIES:

                            decision = "retry_failed"
                            triggered_rule = None
                            explanation = "External dependency failed after retries"

        # -------- COMPLETE WORKFLOW --------
        self.state_manager.complete(
            request_id,
            decision
        )
         # ---- AUDIT LOGGING ----
        log_decision(request_id,{
            "decision": decision,
            "rule" : triggered_rule,
            "explanation": explanation
        })

        return {
            "decision": decision,
            "rule_triggered": triggered_rule,
            "explanation": explanation
        }