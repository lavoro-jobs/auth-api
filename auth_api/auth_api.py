from fastapi import APIRouter, FastAPI
from auth_api.routers.login import router as login_router
from auth_api.database import db


router = APIRouter()
router.include_router(login_router)


@router.get("/")
def root():
    return {"message": "Hello from auth root"}


app = FastAPI()
app.include_router(router)
