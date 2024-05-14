from __future__ import annotations

from app.core.component import SQLAImpl
from app.domain.account.entities import Account
from app.domain.account.repo import AccountRepo

__all__ = ["AccountImpl"]


class AccountImpl(SQLAImpl[Account]):
    repository_type = AccountRepo
