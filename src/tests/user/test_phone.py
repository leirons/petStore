import unittest

from src.app.services.user import validate


class ValidationTestCase(unittest.TestCase):
    def test_one(self):
        res = validate.validate_phone("380992198852")
        self.assertEqual(res.string, "380992198852")

    def test_two(self):
        res = validate.validate_phone("380954466510")
        self.assertEqual(res.string, "380954466510")

    def test_three(self):
        res = validate.validate_phone("+34892131223")
        self.assertEqual(res, None)

    def test_four(self):
        res = validate.validate_phone("31232132123")
        self.assertEqual(res, None)

    def test_five(self):
        res = validate.validate_phone("380502906561")
        self.assertEqual(res.string, "380502906561")


if __name__ == "__main__":
    unittest.main()
