from typing import Type, Annotated
from types import NoneType
from uuid import UUID

from dishka import FromDishka as Depends
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query

from nx_api.svc.crud.crud_svc import CrudSvc
from nx_api.svc.crud.list_svc import ListSvc
from nx_api.svc.crud.types_ import ListSlice


def crud_router(SVC: Type[CrudSvc]):
    C, R, U, RP = SVC.__orig_bases__[0].__args__

    M = RP.__orig_bases__[0].__args__[0]
    prefix = M.__tablename__

    router = APIRouter(
        route_class=DishkaRoute,
        prefix=f"/{prefix}",
        tags=[prefix],
    )

    async def create(
        dto: C,
        svc: Depends[SVC],
    ):
        return await svc.create(dto)

    router.add_api_route(path="", endpoint=create, methods=["POST"], response_model=R)

    async def get(
        id: UUID,
        svc: Depends[SVC],
    ):
        return await svc.get(id)

    router.add_api_route(
        path="/{id}",
        endpoint=get,
        methods=["GET"],
        response_model=R,
    )

    if not U is NoneType:

        async def update(
            dto: U,
            svc: Depends[SVC],
        ):
            return await svc.update(dto)

        router.add_api_route(
            path=f"", endpoint=update, methods=["PUT"], response_model=R
        )

    async def delete(
        id: UUID,
        svc: Depends[SVC],
    ):
        return await svc.delete(id)

    router.add_api_route(
        path="/{id}",
        endpoint=delete,
        methods=["DELETE"],
    )

    return router


def add_list_route(router: APIRouter, SVC: Type[ListSvc]) -> None:
    R, M, LP = SVC.__orig_bases__[0].__args__

    async def list(
        params: Annotated[LP, Query()],
        svc: Depends[SVC],
    ):
        return await svc(params)

    router.add_api_route(
        path=f"", endpoint=list, methods=["GET"], response_model=ListSlice[R]
    )
