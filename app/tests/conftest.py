# tests/conftest.py

import os
import asyncio
import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from httpx import AsyncClient, ASGITransport

from app.infrastructure.db.base import Base
from app.api.dependencies.db import get_async_db
from app.main import app


# -----------------------------
# DATABASE CONFIG
# -----------------------------
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:experion%40123@localhost:5432/ms_test_db"
)

engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool   #  prevents asyncpg connection issues
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


# -----------------------------
# EVENT LOOP FIX (IMPORTANT)
# -----------------------------
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# -----------------------------
# SETUP / TEARDOWN DB PER TEST
# -----------------------------
@pytest_asyncio.fixture(scope="function")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# -----------------------------
# DB SESSION FIX
# -----------------------------
@pytest_asyncio.fixture
async def db_session(setup_db):
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()   #  critical


# -----------------------------so
# FASTAPI TEST CLIENT
# -----------------------------
@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_async_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()