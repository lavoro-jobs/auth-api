from typing import Annotated

from fastapi import APIRouter, Depends
from lavoro_auth_api.services import register_service

from lavoro_library.model.auth_api.dtos import RegisterDTO

router = APIRouter(prefix="/register", tags=["register"])


@router.post("")
async def register(form_data: Annotated[RegisterDTO, Depends()]):
    return await register_service.register(form_data)


@router.post("/no-confirm")
def register_no_confirm(form_data: Annotated[RegisterDTO, Depends()]):
    return register_service.register_no_confirm(form_data)


@router.post("/confirm/{verification_token}")
def confirm_email(verification_token: str):
    return register_service.confirm_email(verification_token)
