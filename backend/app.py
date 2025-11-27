from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from . import fetcher
import os

STATIC_DIR=os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

app=FastAPI(title="Real-Time Weather Backend")

@app.on_event("startup")
def startup_event():
    fetcher.fetch_and_convert()


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def home():
    return {"message":"Weather backend running", "endpoints": [
        "/static/temperature.json",
        "/static/humidity.json",
        "/static/pressure.json",
        "/static/wind_u.json",
        "/static/wind_v.json"
    ]}

import uvicorn

def start():
    uvicorn.run("backend.app:app",host="0.0.0.0", port=10000)
