from __future__ import annotations

from unittest.mock import create_autospec
from uuid import uuid4

import pytest
from advanced_alchemy.repository import SQLAlchemyAsyncMockRepository
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.domain.account.entities.account import Account
from app.domain.account.entities.oidc import OIDCAccount
from app.domain.account.impl import AccountImpl


class AccountMockRepo(SQLAlchemyAsyncMockRepository[Account]):
    model_type = Account


class OIDCAccountMockRepo(SQLAlchemyAsyncMockRepository[OIDCAccount]):
    model_type = OIDCAccount


@pytest.fixture()
def session():
    session = create_autospec(AsyncSession)
    session.bind = create_autospec(AsyncEngine)
    return session


@pytest.fixture
async def impl(session):
    impl = AccountImpl(session=session)
    impl.repository = AccountMockRepo()
    impl.oidc_repository = OIDCAccountMockRepo()

    yield impl
    impl.repository.__database_clear__()
    impl.oidc_repository.__database_clear__()


async def test_register_oidc_new_account(impl: AccountImpl):
    account = await impl.register_oidc(
        provider_name="google",
        access_token="access_token",
        sub="sub",
        exp=123,
        email="maintain0404@gmail.com",
    )

    oidc = account.oidc_accounts[0]
    assert oidc.provider_name == "google"
    assert oidc.access_token == "access_token"
    assert oidc.sub == "sub"


async def test_register_oidc_to_existing_oidc_account(impl: AccountImpl):
    existing_id = uuid4()
    impl.oidc_repository.__database_add__(
        existing_id,
        OIDCAccount(
            id=existing_id,
            provider_name="google",
            access_token="access_token",
            sub="sub",
            exp=123,
            email="maintain0404@gmail.com",
        ),
    )

    account = await impl.register_oidc(
        provider_name="google",
        access_token="access_token",
        sub="sub",
        exp=123,
        email="maintain0404@gmail.com",
    )

    oidc = account.oidc_accounts[0]
    assert oidc.id == existing_id
    assert oidc.provider_name == "google"
    assert oidc.access_token == "access_token"
    assert oidc.sub == "sub"
