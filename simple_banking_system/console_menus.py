"""
This module handle all the user interaction through
different menus.
"""
from .banking import auth
from .banking.factories import CreditCardBuilder
from .banking.models import CreditCard
from .banking.validators import LuhnCardValidator


class BaseMenu:
    """Base interface to make a menu."""
    def next(self):
        """Return the next menu instance."""
        raise NotImplementedError


class MainMenu(BaseMenu):
    def next(self):
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        option = input()

        if option == '1':
            return CreateAccountMenu()
        elif option == '2':
            return LogIntoAccountMenu()

        return None


class CreateAccountMenu(BaseMenu):
    def next(self):
        credit_card = CreditCardBuilder().get_new_credit_card()
        credit_card.save()
        print('Your card has been created')
        print('Your card number:')
        print(credit_card.number)
        print('Your card PIN:')
        print(credit_card.pin)
        return MainMenu()


class LogIntoAccountMenu(BaseMenu):
    def next(self):
        print('Enter your card number:')
        card_number = input()
        print('Enter your PIN:')
        card_pin = input()
        card = CreditCard.get_by_card_number(card_number)

        if card and card.pin == card_pin:
            auth.set_logged_in_account(card)
            print('You have successfully logged in!')
            return UserLoggedInMenu()

        print('Wrong card number or PIN!')
        return MainMenu()


class UserLoggedInMenu(BaseMenu):
    def next(self):
        print('1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')
        option = input()

        if option == '0':
            return None
        elif option == '1':
            return BalanceMenu()
        elif option == '2':
            return IncomeMenu()
        elif option == '3':
            return TransferMenu()
        elif option == '4':
            return CloseAccountMenu()
        elif option == '5':
            auth.set_logged_in_account(None)
            print('You have successfully logged out!')
            return MainMenu()

        return None


class BalanceMenu(BaseMenu):
    def next(self):
        card = auth.get_logged_in_account()
        print(f'Balance: {card.balance}')
        return UserLoggedInMenu()


class IncomeMenu(BaseMenu):
    def next(self):
        print('Enter income:')
        income = int(input())
        card = auth.get_logged_in_account()
        card.balance += income
        card.update()
        print('Income was added!')
        return UserLoggedInMenu()


class TransferMenu(BaseMenu):
    def next(self):
        print('Enter card number:')
        card_number = input()
        if not LuhnCardValidator.is_valid(card_number):
            print(
                'Probably you made a mistake in the card number.',
                'Please try again!',
            )
            return UserLoggedInMenu()

        destination_card = CreditCard.get_by_card_number(card_number)
        if not destination_card:
            print('Such a card does not exist.')
            return UserLoggedInMenu()

        print('Enter how much money you want to transfer:')
        amount = int(input())
        my_card = auth.get_logged_in_account()
        if amount > my_card.balance:
            print('Not enough money!')
            return UserLoggedInMenu()

        my_card.balance -= amount
        destination_card.balance += amount
        my_card.update()
        destination_card.update()
        print('Success!')
        return UserLoggedInMenu()


class CloseAccountMenu(BaseMenu):
    def next(self):
        card = auth.get_logged_in_account()
        card.delete()
        auth.set_logged_in_account(None)
        print('The account has been closed!')
        return MainMenu()


# Entry point to interact with menus
class ContextMenu:
    current_menu = MainMenu()

    def execute(self):
        next_menu = self.current_menu.next()
        self.current_menu = next_menu
        return next_menu
