class LuhnAlgorithm:
    @staticmethod
    def get_luhn_sum(card_number):
        digits = [int(digit) for digit in card_number[:-1]]

        for i in range(len(digits)):
            if (i+1) % 2 != 0:
                digits[i] *= 2

            if digits[i] > 9:
                digits[i] -= 9

        return sum(digits)
