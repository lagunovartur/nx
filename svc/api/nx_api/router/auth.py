from dishka import FromDishka as Depends
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

import nx_api.dto as d
from nx_api.svc.auth.ia.login import LoginIA
from nx_api.svc.auth.ia.logout import LogoutIA
from nx_api.svc.auth.ia.register import RegisterIA

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
