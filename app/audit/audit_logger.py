import json
import datetime


def log_decision(request_id, decision_data):

    log_entry = {
        "timestamp": str(datetime.datetime.utcnow()),
        "request_id": request_id,
        "decision_data": decision_data
    }

    with open("audit.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")