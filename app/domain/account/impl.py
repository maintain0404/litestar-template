from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.sql import Select, StatementLambdaElement, select

from app.core.component import SQLAImpl
from app.domain.account.entities import Account
from app.domain.account.entities.oidc import OIDCAccount
from app.domain.account.repo import AccountRepo, OIDCRepo

__all__ = ["AccountImpl"]


class AccountImpl(SQLAImpl[Account]):
    repository_type = AccountRepo

    oidc_repository: OIDCRepo[OIDCAccount]

    def __init__(
        self,
        session: AsyncSession | async_scoped_session[AsyncSession],
        statement: Select[tuple[Account]] | StatementLambdaElement | None = None,
        auto_expunge: bool = False,
        auto_refresh: bool = True,
        auto_commit: bool = False,
        **repo_kwargs: Any,
    ) -> None:
        super().__init__(
            session, statement, auto_expunge, auto_refresh, auto_commit, **repo_kwargs
        )
        self.oidc_repository = OIDCRepo(
            session=session,
            auto_expunge=auto_expunge,
            auto_refresh=auto_refresh,
            auto_commit=auto_commit,
        )

    async def register_oidc(self, provider_name: str, **kwargs) -> Account:
        kwargs["account"] = Account(email=kwargs.get("email"), name=kwargs.get("name"))

        oidc = await self.oidc_repository.get_one_or_none(
            provider_name=provider_name, sub=kwargs["sub"]
        )

        if not oidc:
            account = Account(email=kwargs["email"], name=kwargs["name"])
            oidc = OIDCAccount(provider_name=str, account=account, **kwargs)
            self.repository.get_or_create()

        return oidc.account
