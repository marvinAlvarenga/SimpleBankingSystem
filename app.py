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
