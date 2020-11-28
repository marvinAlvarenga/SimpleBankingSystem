from .storages import SQLiteStorageHandler


class CreditCard:

    storage_handler = SQLiteStorageHandler()

    def __init__(self, number, pin, balance=0):
        self.number = number
        self.pin = pin
        self.balance = balance

    @classmethod
    def get_by_card_number(cls, card_number):
        return cls.storage_handler.get_by_card_number(card_number)

    def save(self):
        return self.storage_handler.save(self)

    def update(self):
        return self.storage_handler.update(self)

    def delete(self):
        return self.storage_handler.delete(self)