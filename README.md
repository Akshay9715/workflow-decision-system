# Resilient Workflow Decision System

A configurable workflow decision platform designed to process business requests, evaluate rules, execute workflow stages, maintain lifecycle state, and provide explainable decisions.

This system was built as part of a hackathon assignment to demonstrate a resilient and configurable decision engine capable of handling real-world operational constraints.

---

## Key Features

- Configurable workflows using JSON
- Rule-based decision engine
- Workflow lifecycle tracking
- Audit logging for explainable decisions
- External dependency simulation
- Retry handling for failures
- Idempotent request processing
- REST API built with FastAPI
- Automated tests using pytest

---

## System Architecture

Detailed architecture documentation can be found here:

ARCHITECTURE.md

---

## Supported Example Workflows

The system is designed to support multiple workflows through configuration.

Example workflows include:

- Loan approval
- Employee onboarding
- Vendor approval

New workflows can be added by updating `config/workflows.json` without modifying application code.

---

## API Documentation

FastAPI automatically generates interactive documentation.

Example:
```
http://127.0.0.1:8000/docs
```

## Setup

Install dependencies:

pip install -r requirements.txt

---

## Run Server

Start the API server:

uvicorn app.main:app --reload

---

## API Documentation

FastAPI auto-generated docs:

http://127.0.0.1:8000/docs

---

## Example Request
```
POST /process
{
"workflow_name": "loan_approval",
"request_id": "req100",
"data": {
"income": 50000,
"credit_score": 720
}
}
```

Example Response

```
{
"decision": "approve",
"rule_triggered": "R2",
"explanation": {
"field": "credit_score",
"input_value": 720,
"operator": ">=",
"rule_value": 700
}
}
```

---

## Run Tests

pytest

---

## Project Structure

```
app/
├── api/
├── engine/
├── rules/
├── state/
├── config/
├── db/
└── audit/

tests/
```

---

## Technologies Used

- Python
- FastAPI
- SQLite
- Pydantic
- SQLAlchemy
- Pytest