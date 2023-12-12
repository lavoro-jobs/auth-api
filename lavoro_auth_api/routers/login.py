from typing import Annotated

from fastapi import APIRouter, Depends
from lavoro_auth_api.services import login_service

from lavoro_library.model.auth_api.dtos import LoginDTO, TokenDTO


router = APIRouter(prefix="/login", tags=["login"])


@router.post("/token", response_model=TokenDTO)
def login_for_access_token(form_data: Annotated[LoginDTO, Depends()]):
    return login_service.login(form_data)
