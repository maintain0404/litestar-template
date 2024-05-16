from __future__ import annotations

from secrets import token_urlsafe
from typing import Annotated, Any
from urllib.parse import urlencode

import httpx
from litestar import Controller, Request, Router, get
from litestar.connection import ASGIConnection
from litestar.params import Parameter
from litestar.response import Redirect
from litestar.security.jwt import OAuth2Login, OAuth2PasswordBearerAuth
from pydantic import BaseModel

from app.domain.account.entities import Account


async def get_user(token: Any, conn: ASGIConnection) -> Account: ...


oauth2_auth = OAuth2PasswordBearerAuth[Account](
    retrieve_user_handler=get_user,
    token_secret="secret",
    # we are specifying the URL for retrieving a JWT access token
    token_url="/login",
    # we are specifying which endpoints should be excluded from authentication.
    # note that this is a list regex patterns
)


class OIDCConfig(BaseModel):
    auth_uri: str
    token_uri: str
    userinfo_uri: str
    client_id: str
    client_secret: str
    redirect_uri: str
    nonce: str
    prompt: str | None = None


@get("/me")
async def me(self): ...


class OIDCController(Controller):
    path = "/google"
    config: OIDCConfig = OIDCConfig(
        auth_uri="https://accounts.google.com/o/oauth2/v2/auth",
        token_uri="https://oauth2.googleapis.com/token",
        redirect_uri="http://localhost:8000/api/v0.1.0/auth/google/callback",
        userinfo_uri="https://openidconnect.googleapis.com/v1/userinfo",
        client_id="83645434081-5rild3sqthkreughf4rgghkg6chdid9d.apps.googleusercontent.com",
        client_secret="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",
        nonce="nonce",
    )

    @get(
        "/sign_in",
        status_code=302,
    )
    async def sign_in(self, request: Request) -> Redirect:
        state = token_urlsafe(16)
        query_params = {
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "scope": "openid email profile",
            "state": state,
            "nonce": self.config.nonce,
            "response_type": "code",
            "response_mode": "query",
        }

        if self.config.prompt:
            query_params["prompt"] = self.config.prompt

        request.session["oauth_state"] = state

        return Redirect(f"{self.config.auth_uri}?{urlencode(query_params)}")

    @get("/callback")
    async def callback(
        self,
        request: Request,
        code: Annotated[str, Parameter()],
        oidc_state: Annotated[str, Parameter(query="state")],
    ) -> Redirect:
        if oidc_state != request.session["oauth_state"]:
            raise ValueError

        del request.session["oauth_state"]

        query_params = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.config.redirect_uri,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.config.token_uri, data=query_params)
            ret = resp.json()

            access_token = ret["access_token"]
            exp = ret["exp"]
            refresh_token = ret.get("refresh_token", None)

            resp = await client.get(
                "https://openidconnect.googleapis.com/v1/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                params={"scope": "openid email profile"},
            )
            ret = resp.json()

        # print('*' * 20)
        # print('user_response')
        # print(user_response)
        unique_id = ret.get("sub")
        user_email = ret.get("email")
        user_name = ret.get("given_name")

        auth_user = oauth2_auth.login(identifier=str(unique_id))
        auth_user.content

        # user = User(
        #     id=unique_id, name=user_name, email=user_email, token=auth_user.content
        # )

        # if not USERS_DB.get(unique_id):
        #     USERS_DB[unique_id] = user

        # request.set_session({"user": user})
        # # print('use the following token to access endpoints')
        # # print(auth_user.content)
        request.session["account"] = ""

        return Redirect("/")


router = Router("/auth", route_handlers=[OIDCController])
