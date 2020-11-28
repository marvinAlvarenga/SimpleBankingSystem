"""
Represents a basic authentication system
storing a global CreditCard object.
"""
LOGGED_IN_ACCOUNT = None


def get_logged_in_account():
    return LOGGED_IN_ACCOUNT


def set_logged_in_account(card):
    global LOGGED_IN_ACCOUNT
    LOGGED_IN_ACCOUNT = card
