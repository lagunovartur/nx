from dishka import FromDishka as Depends
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

import nx_api.dto as d
from nx_api.svc.auth.ia.login import LoginIA
from nx_api.svc.auth.ia.logout import LogoutIA
from nx_api.svc.auth.ia.refresh_tokens import RefreshTokensIA
from nx_api.svc.auth.ia.register import RegisterIA
from nx_api.svc.auth.ia.verify_email import VerifyEmailIA
from nx_api.svc.auth.ia.verify_email_end import VerifyEmailEndIA

router = APIRouter(route_class=DishkaRoute, prefix="/auth", tags=["auth"])


@router.post("/register", response_model=d.UserBase)
async def register(
    dto: d.NewUser,
    ia: Depends[RegisterIA],
):
    return await ia(dto)


@router.post(
    "/login",
)
async def login(
    dto: d.Login,
    ia: Depends[LoginIA],
):
    return await ia(dto)


@router.post(
    "/logout",
)
async def logout(
    ia: Depends[LogoutIA],
):
    return await ia()


@router.post(
    "/refresh",
)
async def token_pair(
    ia: Depends[RefreshTokensIA],
):
    return await ia()


@router.post(
    "/verify/email",
    response_model=None,
)
async def verify_email(
    dto: d.EmailReq,
    ia: Depends[VerifyEmailIA],
):
    return await ia(dto.email)


@router.get(
    "/verify/email/{token}",
    response_model=None,
)
async def verify_email_end(
    token: str,
    ia: Depends[VerifyEmailEndIA],
):
    return await ia(token)
