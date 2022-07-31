import unittest

from src.app.services.user import validate


class ValidationTestCase(unittest.TestCase):
    def test_one(self):
        res = validate.validate_email("grecig1gmail.com")
        self.assertEqual(res, None)

    def test_two(self):
        res = validate.validate_email("grecig1@gmail.com")
        self.assertEqual(res.string, "grecig1@gmail.com")

    def test_three(self):
        res = validate.validate_email("grecig1asdsadsa.com")
        self.assertEqual(res, None)

    def test_four(self):
        res = validate.validate_email("grecig1asdsadsa.c@om")
        self.assertEqual(res, None)

    def test_five(self):
        res = validate.validate_email("grecig23123@gmail.com")
        self.assertEqual(res.string, "grecig23123@gmail.com")


if __name__ == "__main__":
    unittest.main()
