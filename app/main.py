from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
from .router_chat import router as chat_router
from fastapi.responses import Response
from .router_chat import router as chat_router
from .router_ingest import router as ingest_router 
load_dotenv()

app = FastAPI(title="SAP Data Entry Chatbot (Starter)")

# CORS
origins = os.getenv("ALLOW_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(chat_router, prefix="")
# app/main.py (เติมท้ายไฟล์ ก่อน mount static ก็ได้)

@app.get("/favicon.ico")
def favicon():
    return Response(content=b"", media_type="image/x-icon")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/version")
def version():
    return {"name": "sap-chatbot-starter", "version": "0.1.0"}

# Static web (serve the demo chat UI)
static_dir = os.path.join(os.path.dirname(__file__), "..", "web")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="web")
app.include_router(chat_router, prefix="")
app.include_router(ingest_router, prefix="")