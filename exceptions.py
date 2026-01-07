#Exceptions could be customized to provide more specific error messages or behavior

class UsernameException(Exception):
    pass


class PaymentException(Exception):
    pass


class CreditCardException(Exception):
    pass
