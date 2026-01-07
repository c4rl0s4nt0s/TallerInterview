import re
import uuid

from exceptions import CreditCardException, PaymentException, UsernameException


class Payment:
    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note


class Friendship:
    def __init__(self, actor, target):
        self.id = str(uuid.uuid4())
        self.actor = actor
        self.target = target


class User:
    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0
        self.activity = []  # Feed events (payments, friendships).
        self.friends = []  # Bidirectional friend list.

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException("Username not valid.")

    def retrieve_feed(self):
        return list(self.activity)

    def retrieve_activity(self):
        return self.retrieve_feed()

    def add_friend(self, new_friend):
        if new_friend is self or new_friend in self.friends:
            return None

        # Maintain bidirectional friendship and log in both feeds.
        self.friends.append(new_friend)
        new_friend.friends.append(self)
        friendship = Friendship(self, new_friend)
        self.activity.append(friendship)
        new_friend.activity.append(friendship)

        return friendship

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException("Only one credit card per user!")

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number
        else:
            raise CreditCardException("Invalid credit card number.")

    def pay(self, target, amount, note):
        amount = float(amount)
        # Prefer balance, fall back to card.
        if self.balance >= amount:
            return self.pay_with_balance(target, amount, note)
        return self.pay_with_card(target, amount, note)

    def pay_with_card(self, target, amount, note):
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException("User cannot pay themselves.")
        elif amount <= 0.0:
            raise PaymentException("Amount must be a non-negative number.")
        elif self.credit_card_number is None:
            raise PaymentException("Must have a credit card to make a payment.")

        self._charge_credit_card(self.credit_card_number)
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)
        # Record the payment in both users' feeds.
        self.activity.append(payment)
        target.activity.append(payment)

        return payment

    def pay_with_balance(self, target, amount, note):
        # TODO: add code here
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException("User cannot pay themselves.")
        elif amount <= 0.0:
            raise PaymentException("Amount must be a non-negative number.")
        elif self.balance < amount:
            raise PaymentException("Insufficient balance to make payment.")

        self.balance -= amount
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)
        # Record the payment in both users' feeds.
        self.activity.append(payment)
        target.activity.append(payment)

        return payment

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match("^[A-Za-z0-9_\\-]{4,15}$", username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass
