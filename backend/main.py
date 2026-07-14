import os
import sys

# Force UTF-8 output on Windows to prevent charmap codec errors
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv, find_dotenv

# Load env variables BEFORE importing routers that depend on them
load_dotenv(find_dotenv())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from dependencies import limiter

from api.analyze import router as analyze_router
from api.optimize import router as optimize_router
from api.gbp_report import router as gbp_report_router
import models
from database import engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Competitor Analysis & SEO Optimizer API",
    description="API for comparing websites and generating SEO recommendations using AI.",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
frontend_url = os.environ.get("FRONTEND_URL")
if frontend_url:
    origins = [frontend_url]
    if "localhost" in frontend_url or "127.0.0.1" in frontend_url:
        origins.extend([
            "http://localhost:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
        ])
else:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router, prefix="/api")
app.include_router(optimize_router, prefix="/api")
app.include_router(gbp_report_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Competitor Analysis API. Visit /docs for API documentation."}
