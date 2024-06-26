from __future__ import annotations

from app.core.component import SQLARepo
from app.domain.account.entities import Account

__all__ = ["AccountRepo"]


class AccountRepo(SQLARepo[Account]):
    model_type = Account
