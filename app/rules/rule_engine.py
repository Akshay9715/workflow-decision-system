from app.config.config_loader import load_rules
from app.services.credit_service import CreditScoreService

class RuleEngine:

    def __init__(self):
        self.rules = load_rules()
        self.credit_service = CreditScoreService()

    def evaluate(self, workflow_name, data):
        workflow_rules = self.rules.get(workflow_name, [])

        triggered_rules = []

        for rule in workflow_rules:

            field = rule["field"]
            operator = rule["operator"]
            value = rule["value"]


            if field not in data:
                continue

            if field == "credit_score":
                try :
                    input_value = self.credit_service.get_credit_score(data)
                except Exception :
                    raise
            else :
                input_value = data[field]

            if self._compare(input_value, operator, value):

                return {
                    "decision": rule["action"],
                    "rule_id": rule["rule_id"],
                    "explanation": {
                        "field": field,
                        "input_value": input_value,
                        "operator": operator,
                        "rule_value": value
                }
                }

        return {
            "decision": "approve",
            "rule_id": None,
            "explanation": "No rule triggered. Default approve."
        }

    def _compare(self, a, operator, b):

        if operator == "<":
            return a < b

        if operator == ">":
            return a > b

        if operator == ">=":
            return a >= b

        if operator == "<=":
            return a <= b

        if operator == "==":
            return a == b

        return False