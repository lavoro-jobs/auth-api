from fastapi import APIRouter, FastAPI
from lavoro_auth_api.routers.login import router as login_router
from lavoro_auth_api.routers.account import router as account_router
from lavoro_auth_api.database import db


router = APIRouter()
router.include_router(login_router)
router.include_router(account_router)


app = FastAPI()
app.include_router(router)
