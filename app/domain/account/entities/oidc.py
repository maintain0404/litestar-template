from __future__ import annotations

from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import Integer, String

from app.domain.account.entities.account import Account


class OIDCAccount(UUIDAuditBase):
    __tablename__ = "oidc_account"

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("account.id", ondelete="cascade")
    )
    provider_name: Mapped[str] = mapped_column(
        String(length=100), index=True, nullable=False
    )
    access_token: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(
        String(length=1024), nullable=True
    )

    exp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sub: Mapped[str] = mapped_column(String(length=320), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(length=320), nullable=False)

    # -----------
    # ORM Relationships
    # ------------
    account_name: AssociationProxy[str] = association_proxy("account", "name")
    account_email: AssociationProxy[str] = association_proxy("account", "email")
    account: Mapped[Account] = relationship(
        back_populates="oidc_accounts",
        viewonly=True,
        innerjoin=True,
        lazy="joined",
    )
