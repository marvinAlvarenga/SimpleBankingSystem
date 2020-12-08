import sqlite3


class BaseStorageHandler:
    def save(self, credit_card):
        raise NotImplementedError

    def update(self, credit_card):
        raise NotImplementedError

    def delete(self, credit_card):
        raise NotImplementedError

    def get_by_card_number(self, credit_card):
        """Return data for unpacking."""
        raise NotImplementedError


class DictionaryStorageHandler(BaseStorageHandler):
    """Stores credit cards in a dictionary."""
    def __init__(self, storage: dict = None):
        self.storage = storage if storage is not None else {}

    def save(self, credit_card):
        self.storage[credit_card.number] = credit_card

    def update(self, credit_card):
        pass

    def delete(self, credit_card):
        del self.storage[credit_card.number]

    def get_by_card_number(self, card_number):
        credit_card = self.storage.get(card_number, None)

        # Transfor data for unpacking
        return {
            'number': credit_card.number,
            'pin': credit_card.pin,
            'balance': credit_card.balance,
        }


class SQLiteStorageHandler(BaseStorageHandler):
    """Stores credit cards in a sqlite database."""
    db_name = 'card.s3db'
    table_name = 'card'
    field_number = 'number'
    field_pin = 'pin'
    field_balance = 'balance'

    def __init__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS card(
            number  VARCHAR(16),
            pin     CHAR(4),
            balance DECIMAL(8,2) DEFAULT 0.0
        );
        """
        self.cursor.execute(query)
        self.connection.commit()

    def save(self, credit_card):
        query = (f'INSERT INTO {self.table_name}'
                 f' VALUES ("{credit_card.number}", '
                 f'"{credit_card.pin}", {credit_card.balance});')

        self.cursor.execute(query)
        self.connection.commit()

    def update(self, credit_card):
        query = (f'UPDATE {self.table_name} '
                 f'SET {self.field_balance}={credit_card.balance} '
                 f'WHERE {self.field_number}="{credit_card.number}";')
        self.cursor.execute(query)
        self.connection.commit()

    def delete(self, credit_card):
        query = (f'DELETE FROM {self.table_name} '
                 f'WHERE {self.field_number}="{credit_card.number}";')
        self.cursor.execute(query)
        self.connection.commit()

    def get_by_card_number(self, card_number):
        query = (f'SELECT * FROM {self.table_name} '
                 f'WHERE {self.field_number}="{card_number}";')
        self.cursor.execute(query)
        row = self.cursor.fetchone()  # Returns a tuple

        return {
            'number': row[0],
            'pin': row[1],
            'balance': row[2],
        } if row else None
