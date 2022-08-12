import unittest

from core.auth import AuthHandler


class ValidationTestCase(unittest.TestCase):
    def test_one(self):
        auth_handler = AuthHandler()
        token = auth_handler.encode_token(user_id=1)
        assert token is not None

    def test_two(self):
        auth_handler = AuthHandler()
        token = auth_handler.encode_token(user_id=1)
        assert token is not None
        auth_user = auth_handler.decode_token(token)
        assert auth_user is not None

    def test_tree(self):
        auth_handler = AuthHandler()
        auth_user = auth_handler.decode_token("token")
        assert auth_user.status_code == 401
