from __future__ import annotations

from dataclasses import dataclass

from app.domain.account.impl import AccountImpl


@dataclass
class AccountService:
    impl: AccountImpl

    async def register_oauth_client(
        self,
        sub: str,
        provider_name: str,
        access_token: str,
        exp: int | None,
        refresh_token: str | None,
    ):
        account = await self.impl.register_oidc(
            sub=sub,
            oauth_name=provider_name,
            access_token=access_token,
            exp=exp,
            refresh_token=refresh_token,
        )

        return account
