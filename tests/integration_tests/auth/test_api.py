import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("vasyan@mail.ru", "12345", 200),
        ("vasyan1@mail.ru", "12345", 200),
        ("vasyan2@mail.ru", "12345", 200),
        ("vasyan2@mail.ru", "123453", 409)
    ]
)

async def test_auth(
        db, ac,
        email, password, status_code
):
    register_response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )
    assert register_response.status_code == status_code
    if register_response.status_code == 200:
        res = register_response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"

async def test_login(ac):
    login_response = await ac.post(
        "/auth/login",
        json={"email": "vasyan@mail.ru", "password": "12345"}
    )
    assert login_response.status_code == 200
    assert ac.cookies["access_token"]

async def test_me(ac):
    me_response = await ac.get("/auth/me")
    assert me_response.status_code == 200
    res = me_response.json()
    assert res["email"] == "vasyan@mail.ru"

async def test_logout(ac):
    logout_response = await ac.get("/auth/logout")
    assert logout_response.status_code == 200
    me_response = await ac.get("/auth/me")
    assert me_response.status_code == 401
    assert me_response.cookies.get("access_token") is None
