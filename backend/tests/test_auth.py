import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    """ユーザー登録テスト"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "display_name": "テストユーザー"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    """ログインテスト"""
    # まず登録
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test2@example.com",
            "password": "password123"
        }
    )
    
    # ログイン
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test2@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    """ログイン失敗テスト"""
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test3@example.com",
            "password": "password123"
        }
    )
    
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test3@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401