import sentry_sdk

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routers import users, store, pet
from core.db.sessions import Base, engine
from core.middlewares.authentication import (
    AuthenticationMiddleware,
    AuthBackend
)
from core.config import settings
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware


def init_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routers(app: FastAPI) -> None:
    app.include_router(users.router, prefix='/api/v1')
    app.include_router(pet.router, prefix='/api/v1')
    app.include_router(store.router, prefix='/api/v1')


def init_middleware(app: FastAPI) -> None:
    app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())
    app.add_middleware(SessionMiddleware, secret_key="SECRET")
    app.add_middleware(SentryAsgiMiddleware)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Pet Store Server",
        description="API",
        version="1.0.0",
        docs_url="/docs"
    )
    init_routers(app=app)
    init_cors(app=app)
    init_middleware(app=app)
    return app


sentry_sdk.init(
    dsn=settings.DSN,

)

app = create_app()


