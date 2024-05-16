from __future__ import annotations

from sqlalchemy.sql import select

from app.core.component import SQLARepo
from app.domain.account.entities import Account
from app.domain.account.entities.oidc import OIDCAccount

__all__ = ["AccountRepo"]


class AccountRepo(SQLARepo[Account]):
    model_type = Account

    async def get_or_upsert_by_oidc(self, provider_name: str, sub: str) -> Account:
        account = await self.get_one_or_none(
            select(Account).where(
                Account.id
                == select(OIDCAccount.account_id)
                .filter_by(provider_name=provider_name, sub=sub)
                .scalar_subquery()
            )
        )

        if not account:
            account = Account()


class OIDCRepo(SQLARepo[OIDCAccount]):
    model_type = OIDCAccount
