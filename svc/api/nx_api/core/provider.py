from dishka import Provider, Scope, from_context, provide, AsyncContainer
from fastapi import Request, FastAPI, Response
from fastapi import Depends
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer
from typing import NewType
from jinja2 import Environment, FileSystemLoader
from nx_api.core.config import ApiConfig
from nx_api.core.di_proxy import DiProxy
from nx_api.core.lifespan import lifespan
from nx_api.core.middleware import add_middleware
from nx_api.exc.handlers import add_exc_handlers
from nx_api.svc.auth.guard import AuthGuard
from nx_api.router import root_router
from nx_api.svc.email.abstract import ISendMail
from nx_api.svc.email.smtp_send import SmtpSend

AppContainer = NewType("AppContainer", AsyncContainer)


class CoreProv(Provider):
    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def config(self) -> ApiConfig:
        return ApiConfig()

    di_proxy = provide(DiProxy, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def api(
        self, config: ApiConfig, guard: AuthGuard, di_proxy: DiProxy
    ) -> FastAPI:
        app = FastAPI(
            title=config.TITLE,
            debug=config.DEBUG,
            openapi_url="/api/openapi.json",
            dependencies=[
                Depends(di_proxy),
                Depends(guard),
            ],
            lifespan=lifespan,
        )

        add_middleware(app)
        add_exc_handlers(app)
        app.include_router(root_router())

        return app

    @provide(scope=Scope.APP)
    async def app_container(self, app: FastAPI) -> AppContainer:
        return app.state.dishka_container

    @provide(scope=Scope.APP)
    def uvicorn_config(self, config: ApiConfig, app: FastAPI) -> UvicornConfig:
        return UvicornConfig(
            app=app,
            host="0.0.0.0",
            port=config.PORT,
            ssl_keyfile="./ssl/private.key",
            ssl_certfile="./ssl/public.crt",
        )

    @provide(scope=Scope.APP)
    def uvicorn_server(self, config: UvicornConfig) -> UvicornServer:
        return UvicornServer(config=config)

    @provide(scope=Scope.REQUEST)
    def response(self, request: Request) -> Response:
        return getattr(request.state, "response")

    @provide(scope=Scope.APP)
    def jinja_tmpls(self) -> Environment:
        loader = FileSystemLoader("nx_api/tmpls")
        return Environment(loader=loader)

    send_mail = provide(SmtpSend, scope=Scope.REQUEST, provides=ISendMail)
