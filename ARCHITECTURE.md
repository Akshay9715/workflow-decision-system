# System Architecture – Resilient Decision System

## 1. Overview

The system is a configurable workflow decision platform designed to process business requests using configurable rules and workflow stages.

It supports:
* rule-based decision making
* configurable workflows
* lifecycle tracking
* auditability
* external dependency handling
* retries and idempotency

The system is designed to support multiple business workflows such as:
* loan approval
* claim processing
* vendor onboarding
* document verification

without requiring code changes.


## 2. High-Level Architecture

System flow:
```Code
Client
   │
   ▼
FastAPI REST API
   │
   ▼
Workflow Engine
   │
   ├── Rule Engine
   │
   ├── State Manager
   │
   ├── External Dependency Service
   │
   └── Audit Logger
   │
   ▼
Database (SQLite)
```

## 3. Component Breakdown
### a. API Layer

Implemented using FastAPI.

Responsibilities:
* receive workflow requests
* validate schema using Pydantic
* route request to workflow engine
* return structured decision response

Example endpoint:
```code
POST /process
```
### b. Workflow Engine

Core orchestration component.

Responsibilities:
* execute workflow stages
* coordinate rule evaluation
* manage retries
* handle idempotency
* trigger audit logging

Key features:
* configurable workflows
* retry logic for failures
* consistent response format

### b. Rule Engine

Responsible for evaluating decision rules defined in configuration.

Rules are stored in:
```
config/rules.json
```
Example rule:
```
{
 "rule_id": "R2",
 "field": "credit_score",
 "operator": ">=",
 "value": 700,
 "action": "approve"
}
```
Capabilities:
* threshold checks
* conditional branching
* configurable rules

### c. State Manager

Responsible for lifecycle tracking of requests.

Stored fields:
```
request_id
workflow_name
status
decision
history
```
Example lifecycle:
```
received → validate → rule_check → decision
```
This ensures traceability and debugging capability.

### d. External Dependency Service

A simulated credit score service is used to emulate real-world system dependencies.

Purpose:
* simulate external API failures
* test retry mechanisms
* validate robustness

Failures are handled with retries.

### e. Retry System

To handle dependency failures, the system implements a retry mechanism.

Configuration:
```
MAX_RETRIES = 3
```
Workflow:
```
rule_check_attempt_1
rule_check_attempt_2
rule_check_attempt_3
```
If all retries fail:
```
decision = retry_failed
```

### f. Idempotency Handling
Duplicate requests are prevented using request IDs.

If a request with the same request_id already exists:

* the system returns * the previous result

avoids duplicate processing

### g. Audit Logging

Every decision is recorded in:
```
audit.log
```
Example log:
```
{
 "request_id": "req50",
 "decision": "approve",
 "rule": "R2",
 "explanation": {
   "field": "credit_score",
   "value": 720
 }
}
```
This enables:

* decision explainability
* regulatory compliance
* debugging


## 4. Configuration System

The system is fully configuration driven.

Workflows
```
config/workflows.json
```
Example:
```
{
 "loan_approval": {
  "steps": ["validate","rule_check","decision"]
 }
}
```
Rules
```
config/rules.json
```
Rules can be changed without modifying application code.

## 5. Data Flow
```
Client Request
      │
      ▼
API Validation
      │
      ▼
Workflow Engine
      │
      ├─ Rule Evaluation
      │
      ├─ External Service Call
      │
      ├─ Retry Handling
      │
      ├─ State Update
      │
      ▼
Decision Generation
      │
      ▼
Audit Logging
      │
      ▼
Response to Client
```

## 6. Error Handling

System handles:
* invalid input
* external dependency failures
* duplicate requests
* rule evaluation errors

Robustness features:
* retries
* idempotency
* structured error responses

## 7. Scaling Considerations

Current implementation uses SQLite for simplicity.

Production improvements could include:

| Component          | Production Upgrade   |
| ------------------ | -------------------- |
| Database           | PostgreSQL           |
| Caching            | Redis                |
| Async processing   | Kafka / RabbitMQ     |
| Service deployment | Docker + Kubernetes  |
| Observability      | Prometheus + Grafana |


These changes would allow the system to scale to millions of requests per day.

## 8. Design Trade-offs
Decision	Reason
FastAPI	lightweight and fast API framework
SQLite	simple local persistence
JSON configuration	high configurability
retry logic in engine	centralized error handling

Trade-offs:
* SQLite not ideal for large scale
* rule evaluation currently sequential

## 9. Testing Strategy

Testing implemented using pytest.

Covered scenarios:
* happy path
* invalid input
* duplicate requests
* dependency failure
* retry flow
* rule change scenario