import uuid

import pytest


@pytest.mark.asyncio
async def test_register_login_me_flow(client):
    slug = f"acme-{uuid.uuid4().hex[:8]}"
    register_payload = {
        "tenant_name": "Acme Trading",
        "tenant_slug": slug,
        "owner_full_name": "Sara Al-Thani",
        "owner_email": "sara@acme.example.com",
        "owner_password": "correct-horse-battery-staple",
    }
    register_res = await client.post("/api/v1/auth/register", json=register_payload)
    assert register_res.status_code == 201
    tokens = register_res.json()["data"]
    assert tokens["access_token"]

    me_res = await client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    assert me_res.status_code == 200
    profile = me_res.json()["data"]
    assert profile["email"] == "sara@acme.example.com"
    assert profile["role"] == "owner"

    login_res = await client.post(
        "/api/v1/auth/login",
        json={"tenant_slug": slug, "email": "sara@acme.example.com", "password": "correct-horse-battery-staple"},
    )
    assert login_res.status_code == 200

    today_res = await client.get(
        "/api/v1/dashboard/today", headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    assert today_res.status_code == 200
    assert today_res.json()["data"]["pending_approvals"] == 0
