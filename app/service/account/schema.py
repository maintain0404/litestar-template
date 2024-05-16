from __future__ import annotations

from typing import TypedDict


class OpenIDUserInfo(TypedDict):
    iss: str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: bool
    at_hash: str
    nonce: str
    name: str
    picture: str  # image url
    given_name: str
    family_name: str
    iat: int
    exp: int
