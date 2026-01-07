import unittest

from exceptions import CreditCardException, UsernameException
from main import MiniVenmo


class TestCreateUser(unittest.TestCase):
    def test_create_user_sets_balance_and_card(self):
        venmo = MiniVenmo()

        user = venmo.create_user("Bobby", 5.0, "4111111111111111")

        self.assertEqual(user.username, "Bobby")
        self.assertEqual(user.balance, 5.0)
        self.assertEqual(user.credit_card_number, "4111111111111111")

    def test_create_user_invalid_username_raises(self):
        venmo = MiniVenmo()

        with self.assertRaises(UsernameException):
            venmo.create_user("a", 0.0, "4111111111111111")

    def test_create_user_invalid_card_raises(self):
        venmo = MiniVenmo()

        with self.assertRaises(CreditCardException):
            venmo.create_user("Bobby", 0.0, "1234")


if __name__ == "__main__":
    unittest.main()
