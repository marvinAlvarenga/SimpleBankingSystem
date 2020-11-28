from .utils import LuhnAlgorithm


class BaseCardValidator:
    def is_valid(self, number_card):
        raise NotImplementedError


class LuhnCardValidator(BaseCardValidator):
    @staticmethod
    def is_valid(number_card):
        luhn_sum = LuhnAlgorithm.get_luhn_sum(number_card)
        checksum = int(number_card[-1])
        return (luhn_sum + checksum) % 10 == 0
