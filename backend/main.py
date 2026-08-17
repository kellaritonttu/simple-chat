import sys
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.message import router as message_router
from routers.user import router as user_router
from core.config import settings
from core.firebase import init_firebase

# ── Logger ────────────────────────────────────────────────────────────────────

logger = logging.getLogger("chat")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
logger.addHandler(handler)


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Chat Backend...")
    init_firebase()

    yield
    logger.info("Shutting down Chat Backend...")


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title    = "Chat Backend",
    version  = "0.1.0",
    lifespan = lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message_router)
app.include_router(user_router)