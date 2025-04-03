from typing import Annotated

from dishka import FromDishka as Depends
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query

import nx_api.dto as d
from nx_api.svc.user.service import UserList
from nx_api.svc.crud import ListSlice, BaseLP

router = APIRouter(route_class=DishkaRoute, prefix="/user", tags=["user"])


@router.get(
    "",
    response_model=ListSlice[d.User],
)
async def list(
    params: Annotated[BaseLP, Query()],
    svc: Depends[UserList],
):
    return await svc(params)
