from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from core.config import settings
from app.server import app
from core.db.sessions import get_db
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.sessions import Base
import pytest

SQLALCHEMY_DATABASE_URL = settings.TEST_DB

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def override_get_db() -> AsyncSession:
    """
    Get db to create session
    :return Session:
    """
    async with session_local() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def test_db():
    async def run_engine():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_engine())


client = TestClient(app)


