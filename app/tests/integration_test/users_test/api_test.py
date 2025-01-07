import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code", [
    ("kotopes@gmail.com", "ass_assovich", 200),
    ("kotopes@.com", "ass_assovich", 409),
    ("joepeach", "kotleta", 200),
    ("abcde", "joepeach", 422)
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code