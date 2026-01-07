import unittest

from main import MiniVenmo
from venmo import User


class TestFeed(unittest.TestCase):
    def test_retrieve_feed_orders_payments(self):
        bobby = User("Bobby")
        carol = User("Carol")
        bobby.add_to_balance(10.0)
        bobby.pay(carol, 5.0, "Coffee")
        carol.add_credit_card("4111111111111111")
        carol.pay(bobby, 15.0, "Lunch")

        feed = bobby.retrieve_feed()

        self.assertEqual(len(feed), 2)
        self.assertEqual(feed[0].note, "Coffee")
        self.assertEqual(feed[1].note, "Lunch")

    def test_render_feed_includes_payment_and_friendship(self):
        venmo = MiniVenmo()
        bobby = User("Bobby")
        carol = User("Carol")
        bobby.add_to_balance(10.0)
        bobby.pay(carol, 5.0, "Coffee")
        bobby.add_friend(carol)

        feed = bobby.retrieve_feed()
        output = venmo.render_feed(feed)

        self.assertEqual(output[0], "Bobby paid Carol $5.00 for Coffee")
        self.assertEqual(output[1], "Bobby added Carol as a friend")

    def test_render_feed_matches_readme_example(self):
        venmo = MiniVenmo()
        bobby = User("Bobby")
        carol = User("Carol")
        bobby.add_to_balance(5.0)
        carol.add_credit_card("4111111111111111")

        bobby.pay(carol, 5.0, "Coffee")
        carol.pay(bobby, 15.0, "Lunch")

        feed = bobby.retrieve_activity()
        output = venmo.render_feed(feed)

        self.assertEqual(output[0], "Bobby paid Carol $5.00 for Coffee")
        self.assertEqual(output[1], "Carol paid Bobby $15.00 for Lunch")


if __name__ == "__main__":
    unittest.main()
