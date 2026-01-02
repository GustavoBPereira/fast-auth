from contextlib import contextmanager
from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
import pytest_asyncio
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fast_auth.app import app
from fast_auth.database import get_session
from fast_auth.models import User, table_registry




@pytest_asyncio.fixture
async def session():
    engine = create_async_engine( 
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn: 
        await conn.run_sync(table_registry.metadata.create_all) 


    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    # async with engine.begin() as conn: 
    #      await conn.run_sync(table_registry.metadata.drop_all(engine))


@pytest_asyncio.fixture
def client(session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@contextmanager 
def _mock_db_time(*, model, time=datetime(2024, 1, 1)): 

    def fake_time_hook(mapper, connection, target): 
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', fake_time_hook) 

    yield time 

    event.remove(model, 'before_insert', fake_time_hook) 

@pytest_asyncio.fixture
def mock_db_time():
    return _mock_db_time

@pytest_asyncio.fixture
async def user(session):
    db_user = User(
        username="Alice",
        password="123",
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user