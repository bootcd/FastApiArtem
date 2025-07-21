from src.services.auth import AuthService


def test_encode_end_decode_access_token(db):
    data = {"user_id": 1}
    jwt_token = AuthService(db).create_access_token(data=data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthService(db).decode_token(jwt_token)

    assert payload
    assert payload["user_id"] == data["user_id"]