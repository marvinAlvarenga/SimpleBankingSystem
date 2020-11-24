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
