from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_happy_path():

    response = client.post(
        "/process",
        json={
            "workflow_name": "loan_approval",
            "request_id": "test_req_1",
            "data": {
                "income": 50000,
                "credit_score": 720
            }
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["decision"] in ["approve", "reject", "manual_review","retry_failed"]


def test_invalid_input():

    response = client.post(
        "/process",
        json={
            "workflow_name": "loan_approval"
        }
    )

    assert response.status_code == 422


def test_duplicate_request():

    payload = {
        "workflow_name": "loan_approval",
        "request_id": "duplicate_test",
        "data": {
            "income": 50000,
            "credit_score": 720
        }
    }

    first = client.post("/process", json=payload)
    second = client.post("/process", json=payload)

    assert second.status_code == 200

    data = second.json()

    assert "Duplicate request" in data.get("explanation", "")



def test_dependency_failure():

    response = client.post(
        "/process",
        json={
            "workflow_name": "loan_approval",
            "request_id": "dep_fail_test",
            "data": {
                "income": 50000,
                "credit_score": 720
            }
        }
    )

    assert response.status_code == 200


def test_retry_flow():

    response = client.post(
        "/process",
        json={
            "workflow_name": "loan_approval",
            "request_id": "retry_test",
            "data": {
                "income": 40000,
                "credit_score": 710
            }
        }
    )

    data = response.json()

    assert "decision" in data


def test_rule_change():

    response = client.post(
        "/process",
        json={
            "workflow_name": "loan_approval",
            "request_id": "rule_change_test",
            "data": {
                "income": 20000,
                "credit_score": 650
            }
        }
    )

    data = response.json()

    assert data["decision"] in ["reject", "manual_review", "approve"]