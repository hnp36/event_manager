"""
File: test_database_operations.py

Overview:
This test file uses pytest to validate FastAPI + SQLAlchemy functionality. It defines fixtures for isolated, clean tests, creating users in various states (verified, locked, etc.), and managing DB sessions and HTTP clients.
"""

# === Imports ===
from builtins import range
from datetime import datetime
from uuid import uuid4

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session

from app.main import app
from app.database import Base, Database
from app.models.user_model import User, UserRole
from app.dependencies import get_db, get_settings
from app.utils.security import hash_password
from app.utils.template_manager import TemplateManager
from app.services.email_service import EmailService

# === Globals ===
fake = Faker()
settings = get_settings()
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(TEST_DATABASE_URL, echo=settings.debug)
AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
AsyncSessionScoped = scoped_session(AsyncTestingSessionLocal)


# === Shared Helper ===
def generate_user_data(
    role=UserRole.AUTHENTICATED,
    email_verified=False,
    is_locked=False,
    password="MySuperPassword$1234",
    **overrides
):
    data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "hashed_password": hash_password(password),
        "role": role,
        "email_verified": email_verified,
        "is_locked": is_locked,
    }
    data.update(overrides)
    return data


# === Fixtures ===

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    try:
        Database.initialize(settings.database_url)
    except Exception as e:
        pytest.fail(f"Failed to initialize the database: {str(e)}")


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(setup_database):
    async with AsyncSessionScoped() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(scope="function")
async def async_client(db_session):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        app.dependency_overrides[get_db] = lambda: db_session
        try:
            yield client
        finally:
            app.dependency_overrides.clear()


@pytest.fixture
def email_service():
    template_manager = TemplateManager()
    return EmailService(template_manager=template_manager)


@pytest.fixture
async def create_user(db_session):
    async def _create_user(**kwargs):
        user_data = generate_user_data(**kwargs)
        user = User(**user_data)
        db_session.add(user)
        await db_session.commit()
        return user
    return _create_user


# === User Fixtures ===

@pytest.fixture
async def user(create_user):
    return await create_user()

@pytest.fixture
async def locked_user(create_user):
    return await create_user(is_locked=True, email_verified=False, failed_login_attempts=settings.max_login_attempts)

@pytest.fixture
async def verified_user(create_user):
    return await create_user(email_verified=True)

@pytest.fixture
async def unverified_user(create_user):
    return await create_user(email_verified=False)

@pytest.fixture
async def users_with_same_role_50_users(create_user):
    return [await create_user() for _ in range(50)]

@pytest.fixture
async def admin_user(create_user):
    return await create_user(
        nickname="admin_user",
        email="admin@example.com",
        first_name="John",
        last_name="Doe",
        hashed_password="securepassword",
        role=UserRole.ADMIN
    )

@pytest.fixture
async def manager_user(create_user):
    return await create_user(
        nickname="manager_john",
        email="manager_user@example.com",
        first_name="John",
        last_name="Doe",
        hashed_password="securepassword",
        role=UserRole.MANAGER
    )


# === Test Data Fixtures ===

@pytest.fixture
def user_base_data():
    return {
        "email": "john.doe@example.com",
        "nickname": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "Experienced backend developer",
        "profile_picture_url": "https://example.com/profile.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe"
    }

@pytest.fixture
def user_create_data(user_base_data):
    return {**user_base_data, "password": "SecurePassword123!"}

@pytest.fixture
def user_update_data():
    return {
        "email": "john.doe.new@example.com",
        "nickname": "johnny123",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "Specialized in backend development",
        "profile_picture_url": "https://example.com/profile_updated.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johnny",
        "github_profile_url": "https://github.com/johnny"
    }

@pytest.fixture
def user_response_data():
    return {
        "id": uuid4(),
        "email": "test@example.com",
        "nickname": "jane_doe",
        "first_name": "Jane",
        "last_name": "Doe",
        "bio": "QA engineer",
        "profile_picture_url": "https://example.com/profile.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/janedoe",
        "github_profile_url": "https://github.com/janedoe",
        "role": "AUTHENTICATED",
        "is_professional": True,
        "last_login_at": datetime.utcnow()
    }

@pytest.fixture
def login_request_data():
    return {
        "email": "john.doe@example.com",
        "password": "SecurePassword123!"
    }

@pytest.fixture
def user_base_data_invalid():
    return {
        "email": "invalid-email.com",
        "nickname": "john_doe"
    }
