from fastapi import APIRouter
from users.endpoints import router as users_router
from auth.endpoints import router as auth_router

router = APIRouter()


router.include_router(users_router)
router.include_router(auth_router)
