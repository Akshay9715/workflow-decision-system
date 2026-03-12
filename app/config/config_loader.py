import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def load_workflows():
    path = BASE_DIR / "workflows.json"
    with open(path) as f:
        return json.load(f)


def load_rules():
    path = BASE_DIR / "rules.json"
    with open(path) as f:
        return json.load(f)