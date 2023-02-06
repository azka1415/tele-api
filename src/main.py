from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.routes import task
app = FastAPI()

app.include_router(task.router)


@app.get('/')
async def home():
    return RedirectResponse('/docs')
