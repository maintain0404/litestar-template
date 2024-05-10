from __future__ import annotations

from app.core.orm import UUIDAuditBase, orm

__all__ = ["BaseAccount", "AnnonymousAccount", "Account"]


class BaseAccount:
    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def is_annonymous(self) -> bool:
        return True


class AnnonymousAccount(BaseAccount):
    ...


class Account(BaseAccount, UUIDAuditBase):
    email: orm.Mapped[str]

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_annonymous(self) -> bool:
        return False
