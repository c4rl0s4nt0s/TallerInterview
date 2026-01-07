import unittest

from venmo import User


class TestFriends(unittest.TestCase):
    def test_add_friend_adds_both_and_activity(self):
        bobby = User("Bobby")
        carol = User("Carol")

        event = bobby.add_friend(carol)

        self.assertIn(carol, bobby.friends)
        self.assertIn(bobby, carol.friends)
        self.assertIs(bobby.activity[0], event)
        self.assertIs(carol.activity[0], event)

    def test_add_friend_is_idempotent(self):
        bobby = User("Bobby")
        carol = User("Carol")

        bobby.add_friend(carol)
        bobby.add_friend(carol)

        self.assertEqual(len(bobby.friends), 1)
        self.assertEqual(len(carol.friends), 1)
        self.assertEqual(len(bobby.activity), 1)
        self.assertEqual(len(carol.activity), 1)


if __name__ == "__main__":
    unittest.main()
