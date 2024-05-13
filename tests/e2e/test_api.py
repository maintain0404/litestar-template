from __future__ import annotations

from async_asgi_testclient import TestClient

from app.app import app


async def test_healthcheck():
    async with TestClient(app) as client:
        resp = await client.get("api/v0.1.0/system/health")

        assert resp.json() == {"is_database_online": True}
        assert resp.status_code == 200
