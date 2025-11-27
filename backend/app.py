from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from . import fetcher
import os
import uvicorn

# ------------------------------
# FastAPI App
# ------------------------------
app = FastAPI(title="Real-Time Weather Backend")

# Enable CORS for all domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Static File Directory
# ------------------------------
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ------------------------------
# Startup Event (fetch weather)
# ------------------------------
@app.on_event("startup")
def startup_event():
    fetcher.fetch_and_convert()

# ------------------------------
# Home Route
# ------------------------------
@app.get("/")
def home():
    return {
        "message": "Weather backend running",
        "endpoints": [
            "/static/temperature.json",
            "/static/humidity.json",
            "/static/pressure.json",
            "/static/wind_u.json",
            "/static/wind
