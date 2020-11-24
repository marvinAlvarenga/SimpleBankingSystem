# Models and storage
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


class CreditCard:

    storage_handler = DictionaryStorageHandler()

    def __init__(self, number, pin):
        self.number = number
        self.pin = pin
        self.balance = 0

    @classmethod
    def get_by_card_number(cls, card_number):
        return cls.storage_handler.get_by_card_number(card_number)

    def save(self):
        return self.storage_handler.save(self)


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


# Factories
class BaseCreditCardFactory:
    card_number_generator = None
    pin_number_generator = None

    def generate_new_credit_card(self):
        raise NotImplementedError


class RandomCreditCardFactory(BaseCreditCardFactory):
    card_number_generator = RandomCardNumberGenerator()
    pin_number_generator = PINGenerator()

    def generate_new_credit_card(self) -> CreditCard:
        return CreditCard(
            number=self.card_number_generator.generate(),
            pin=self.pin_number_generator.generate(),
        )


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
        credit_card = RandomCreditCardFactory().generate_new_credit_card()
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
