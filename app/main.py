from fastapi import FastAPI
from app.api.routes import router
from app.db.init_db import init_db

app = FastAPI(title="Workflow Decision System")

init_db()

app.include_router(router)