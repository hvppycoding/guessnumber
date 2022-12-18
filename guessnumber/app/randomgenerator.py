import random

from guessnumber.model.positiveintegergenerator import PositiveIntegerGenerator


class RandomGenerator(PositiveIntegerGenerator):
    def generate_less_than_or_equal_to_hundred(self) -> int:
        random.randint(1, 100)
