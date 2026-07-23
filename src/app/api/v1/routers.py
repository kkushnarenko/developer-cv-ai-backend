# src/app/api/routers.py
from fastapi import APIRouter

from src.app.api.v1.endpoints.contact import router as contact_router

api_router = APIRouter()

api_router.include_router(contact_router)
