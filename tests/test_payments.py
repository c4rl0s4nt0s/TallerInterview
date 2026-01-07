import unittest

from exceptions import PaymentException
from venmo import User


class TestPayments(unittest.TestCase):
    def test_pay_uses_balance_when_available(self):
        payer = User("Bobby")
        target = User("Carol")
        payer.add_to_balance(10.0)

        payment = payer.pay(target, 5.0, "Coffee")

        self.assertEqual(payer.balance, 5.0)
        self.assertEqual(target.balance, 5.0)
        self.assertEqual(payment.amount, 5.0)
        self.assertIs(payer.activity[0], payment)
        self.assertIs(target.activity[0], payment)

    def test_pay_uses_card_when_balance_insufficient(self):
        payer = User("Bobby")
        target = User("Carol")
        payer.add_to_balance(2.0)
        payer.add_credit_card("4111111111111111")

        payment = payer.pay(target, 5.0, "Lunch")

        self.assertEqual(payer.balance, 2.0)
        self.assertEqual(target.balance, 5.0)
        self.assertEqual(payment.amount, 5.0)

    def test_pay_without_card_and_insufficient_balance_raises(self):
        payer = User("Bobby")
        target = User("Carol")
        payer.add_to_balance(1.0)

        with self.assertRaises(PaymentException):
            payer.pay(target, 5.0, "Snacks")

    def test_pay_self_raises(self):
        payer = User("Bobby")
        payer.add_to_balance(10.0)

        with self.assertRaises(PaymentException):
            payer.pay(payer, 5.0, "Invalid")

    def test_pay_invalid_amount_raises(self):
        payer = User("Bobby")
        target = User("Carol")
        payer.add_to_balance(10.0)

        with self.assertRaises(PaymentException):
            payer.pay(target, 0.0, "Zero")

        with self.assertRaises(PaymentException):
            payer.pay(target, -1.0, "Negative")


if __name__ == "__main__":
    unittest.main()
