from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from nx_api.router import auth
from nx_api.router import lead


def root_router():
    router = APIRouter(route_class=DishkaRoute, prefix="/api")
    router.include_router(auth.router)
    router.include_router(lead.router)
    return router
