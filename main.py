from fastapi import FastAPI

from api.v1 import router as v1_router
from core.logging_config import configure_logging
from core.database import Base, engine
import logging

configure_logging(log_level=logging.INFO)

# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(v1_router, prefix="/v1", tags=["v1"])

