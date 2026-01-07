import unittest

from exceptions import CreditCardException, PaymentException, UsernameException
from venmo import Friendship, Payment, User


class MiniVenmo:
    def __init__(self):
        self.users = []

    def create_user(self, username, balance, credit_card_number):
        user = User(username)

        if balance:
            user.add_to_balance(balance)

        if credit_card_number:
            user.add_credit_card(credit_card_number)

        self.users.append(user)
        return user

    def render_feed(self, feed):
        # Bobby paid Carol $5.00 for Coffee
        # Carol paid Bobby $15.00 for Lunch
        lines = []
        for item in feed:
            if isinstance(item, Payment):
                line = (
                    f"{item.actor.username} paid {item.target.username} "
                    f"${item.amount:.2f} for {item.note}"
                )
                print(line)
                lines.append(line)
            elif isinstance(item, Friendship):
                line = (
                    f"{item.actor.username} added {item.target.username} "
                    "as a friend"
                )
                print(line)
                lines.append(line)
        return lines

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")
 
            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        venmo.render_feed(feed)

        bobby.add_friend(carol)


class TestUser(unittest.TestCase):

    def test_this_works(self):
        with self.assertRaises(UsernameException):
            raise UsernameException()


if __name__ == '__main__':
    MiniVenmo.run()
    unittest.main()
