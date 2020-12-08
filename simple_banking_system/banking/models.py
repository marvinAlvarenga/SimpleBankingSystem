from .storages import SQLiteStorageHandler
# from .storages import DictionaryStorageHandler


class CreditCard:
    """Represent a credit card. It uses a storage."""

    storage_handler = SQLiteStorageHandler()
    # storage_handler = DictionaryStorageHandler()

    def __init__(self, number, pin, balance=0):
        self.number = number
        self.pin = pin
        self.balance = balance

    @classmethod
    def get_by_card_number(cls, card_number):
        data = cls.storage_handler.get_by_card_number(card_number)
        return cls(**data) if data else None

    def save(self):
        return self.storage_handler.save(self)

    def update(self):
        return self.storage_handler.update(self)

    def delete(self):
        return self.storage_handler.delete(self)
