"""
Factories to generate a new CreditCard instance
using Random strategy or Luhn Algorithm.

Please, use the builder.
"""
from .models import CreditCard
from .generators import (
    LuhnAlgorithmCardNumberGenerator,
    PINGenerator,
    RandomCardNumberGenerator,
)


class BaseCreditCardFactory:
    card_number_generator = None
    pin_number_generator = None

    def generate_new_credit_card(self):
        return CreditCard(
            number=self.card_number_generator.generate(),
            pin=self.pin_number_generator.generate(),
        )


class RandomCreditCardFactory(BaseCreditCardFactory):
    card_number_generator = RandomCardNumberGenerator()
    pin_number_generator = PINGenerator()


class LuhnAlgorithmCreditCardFactory(BaseCreditCardFactory):
    card_number_generator = LuhnAlgorithmCardNumberGenerator()
    pin_number_generator = PINGenerator()


# Generate a new credic card usign a factory
class CreditCardBuilder:
    # Factory to use to generate a new credit card
    factory = LuhnAlgorithmCreditCardFactory()

    def get_new_credit_card(self):
        return self.factory.generate_new_credit_card()
