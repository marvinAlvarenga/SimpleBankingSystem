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
