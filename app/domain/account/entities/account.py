from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

__all__ = ["BaseAccount", "AnnonymousAccount", "Account"]

if TYPE_CHECKING:
    from .oidc import OIDCAccount


class BaseAccount:
    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def is_annonymous(self) -> bool:
        return True


class AnnonymousAccount(BaseAccount): ...


class Account(BaseAccount, UUIDAuditBase):
    __tablename__ = "account"

    email: Mapped[str]
    name: Mapped[str | None] = mapped_column(nullable=True, default=None)
    hashed_password: Mapped[str | None] = mapped_column(
        String(length=255), nullable=True, default=None
    )
    is_super_account: Mapped[bool] = mapped_column(nullable=False, default=False)
    verified_at: Mapped[datetime | None] = mapped_column(nullable=True, default=None)

    # -----------
    # ORM Relationships
    # ------------
    oidc_accounts: Mapped[list[OIDCAccount]] = relationship(
        back_populates="user",
        lazy="noload",
        cascade="all, delete",
        uselist=True,
    )

    # -----------
    # Properties
    # ------------
    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_annonymous(self) -> bool:
        return False
