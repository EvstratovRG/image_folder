from fastapi import APIRouter

from users.endpoints import router as users_router

router = APIRouter()

router.include_router(users_router)
