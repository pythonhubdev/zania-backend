from fastapi import APIRouter

from zania_backend.web.api.docs import docs_router
from zania_backend.web.api.montior import monitor_router

api_router = APIRouter()
api_router.include_router(docs_router)
api_router.include_router(monitor_router)
