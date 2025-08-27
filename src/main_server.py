import uvicorn
import os
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles

app = FastAPI()

public_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "public")

app.mount("/", StaticFiles(directory=public_path, html=True), name='static')

lang_router = APIRouter(prefix="lang")

app.include_router(lang_router)

def run_server():
    uvicorn.run(app=app, host="0.0.0.0", port=5050)

if __name__ == '__main__':
    run_server()
