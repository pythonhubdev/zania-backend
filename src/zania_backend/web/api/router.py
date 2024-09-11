from fastapi import APIRouter

from zania_backend.web.api.docs.views import docs_router

api_router = APIRouter()
api_router.include_router(docs_router)
