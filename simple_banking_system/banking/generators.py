"""
Generates pins, credit card numbers.

Add these generatos to factories in order to
generate a new credit card instance.
"""
import random

from .constants import get_bank_identifier
from .utils import LuhnAlgorithm


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
        random_identifier = (f'{get_bank_identifier()}'
                             f'{random.randint(0, 999999999):09}')

        # Send the generated card number with a generic checksum
        luhn_sum = LuhnAlgorithm.get_luhn_sum(random_identifier + '0')
        rest = luhn_sum % 10
        checksum = 0 if rest == 0 else 10 - rest

        return random_identifier + str(checksum)
