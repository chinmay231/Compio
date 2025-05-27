from fastapi import FastAPI
from app.routes.enlighten import router as enlighten_router
from app.routes.generate import router as generate_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Compio API")
app.include_router(enlighten_router, prefix="/api")
app.include_router(generate_router, prefix="/api")

frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
