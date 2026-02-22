from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes.creatives import router as creatives_router

app = FastAPI(title="Criativos Growth", version="1.0.0")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(creatives_router)
