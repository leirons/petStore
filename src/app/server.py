import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routers import pet, store, users
from core.config import settings
from core.dependencies.logging import Logging
from core.middlewares.authentication import AuthBackend, AuthenticationMiddleware
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi


def init_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routers(app: FastAPI) -> None:
    app.include_router(pet.router, prefix="/api/v1")
    app.include_router(store.router, prefix="/api/v1")
    app.include_router(users.router, prefix="/api/v1")


def init_middleware(app: FastAPI) -> None:
    app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())
    app.add_middleware(SessionMiddleware, secret_key="SECRET")
    app.add_middleware(SentryAsgiMiddleware)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Pet Store Server",
        description="API",
        version="1.0.0",
        docs_url="/docs",
        dependencies=[Depends(Logging)],
    )
    init_routers(app=app)
    init_cors(app=app)
    init_middleware(app=app)
    return app


sentry_sdk.init(
    dsn=settings.DSN,
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    tags_desc_list = [
        {"name": "user", "description": "Operations about user"},
        {"name": "pet", "description": "Everything about your Pets"},
        {"name": "store", "description": "Access to Petstore orders"},
    ]
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["tags"] = tags_desc_list
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = create_app()
app.openapi = custom_openapi
