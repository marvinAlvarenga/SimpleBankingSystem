import random

BANK_IDENTIFIER = '400000'

def get_bank_identifier():
    return BANK_IDENTIFIER


LOGGED_IN_ACCOUNT = None

def get_logged_in_account():
    return LOGGED_IN_ACCOUNT


def set_logged_in_account(card):
    global LOGGED_IN_ACCOUNT
    LOGGED_IN_ACCOUNT = card


# Storages
class BaseStorageHandler:
    def save(self):
        raise NotImplementedError


class DictionaryStorageHandler(BaseStorageHandler):
    def __init__(self, storage :dict = None):
        self.storage = storage if storage is not None else {}

    def save(self, credit_card):
        self.storage[credit_card.number] = credit_card

    def get_by_card_number(self, card_number):
        return self.storage.get(card_number, None)


# Generators
class BaseGenerator:
    def generate(self):
        raise NotImplementedError


class PINGenerator(BaseGenerator):
    def generate(self):
        pin = random.randint(0, 9999)
        return f'{pin:04}'


class RandomCardNumberGenerator(BaseGenerator):
    def generate(self):
        account_identifier = random.randint(0, 999999999)
        checksum = random.randint(0, 9)
        return f'{get_bank_identifier()}{account_identifier:09}{checksum}'


class LuhnAlgorithmCardNumberGenerator(BaseGenerator):
    def generate(self):
        random_identifier = f'{get_bank_identifier()}{random.randint(0, 999999999):09}'
        digits = [int(digit) for digit in random_identifier]

        for i in range(len(digits)):
            if (i+1) % 2 != 0:
                digits[i] *= 2

            if digits[i] > 9:
                digits[i] -= 9

        x = sum(digits)

        rest = x % 10
        checksum = 0 if rest == 0 else 10 - rest

        return random_identifier + str(checksum)


# Factories
class BaseCreditCardFactory:
    card_number_generator = None
    pin_number_generator = None

    def generate_new_credit_card(self):
        return CreditCard(
            number=self.card_number_generator.generate(),
            pin=self.pin_number_generator.generate(),
        )


class RandomCreditCardFactory(BaseCreditCardFactory):
    card_number_generator = RandomCardNumberGenerator()
    pin_number_generator = PINGenerator()


class LuhnAlgorithmCreditCardFactory(BaseCreditCardFactory):
    card_number_generator = LuhnAlgorithmCardNumberGenerator()
    pin_number_generator = PINGenerator()


# Entities
class CreditCard:

    storage_handler = DictionaryStorageHandler()
    generator_factory = LuhnAlgorithmCreditCardFactory()

    def __init__(self, number, pin):
        self.number = number
        self.pin = pin
        self.balance = 0

    @classmethod
    def get_by_card_number(cls, card_number):
        return cls.storage_handler.get_by_card_number(card_number)

    @classmethod
    def generate_one(cls):
        new_credid_card = cls.generator_factory.generate_new_credit_card()
        new_credid_card.save()
        return new_credid_card

    def save(self):
        return self.storage_handler.save(self)


# Menú
class BaseMenu:
    def next(self):
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
        credit_card = CreditCard.generate_one()
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
            set_logged_in_account(card)
            print('You have successfully logged in!')
            return UserLoggedInMenu()

        print('Wrong card number or PIN!')
        return MainMenu()


class UserLoggedInMenu(BaseMenu):
    def next(self):
        print('1. Balance')
        print('2. Log out')
        print('0. Exit')
        option = input()

        if option == '0':
            return None
        elif option == '1':
            return BalanceMenu()
        elif option == '2':
            set_logged_in_account(None)
            print('You have successfully logged out!')
            return MainMenu()

        return None


class BalanceMenu(BaseMenu):
    def next(self):
        card = get_logged_in_account()
        print(f'Balance: {card.balance}')
        return UserLoggedInMenu()


# Entry point
class ContextMenu:
    current_menu = MainMenu()

    def execute(self):
        next_menu = self.current_menu.next()
        self.current_menu = next_menu
        return next_menu


def run():
    entry_point = ContextMenu()
    while True:
        next_ = entry_point.execute()
        if not next_:
            break

    print('Bye!')


if __name__ == "__main__":
    run()
