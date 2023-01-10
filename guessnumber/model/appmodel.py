from guessnumber.model.positiveintegergenerator import PositiveIntegerGenerator
from typing import Callable

Processor = Callable

class AppModel:
    SELECT_MODE_MESSAGE = (
        "1: Single player game\n"
        + "2: Multiplayer game\n"
        + "3: Exit\n"
        + "Enter selection: "
    )

    def __init__(self, generator: PositiveIntegerGenerator):
        self.completed = False
        self.output = self.SELECT_MODE_MESSAGE
        self.generator = generator
        self.processor: Processor = AppModel.process_mode_selection

    def is_completed(self) -> bool:
        return self.completed

    def flush_output(self) -> str:
        return self.output

    def process_input(self, input_str: str) -> None:
        self.processor = self.processor(self, input_str)

    def process_mode_selection(self, input_str: str) -> Processor:
        if input_str == "1":
            answer = self.generator.generate_less_than_or_equal_to_hundred()
            self.output = (
                    "Single player game\n"
                    + "I'm thinking of a number between 1 and 100.\n"
                    + "Enter your guess: "
                )
            self.single_player_mode = True
            return self.get_single_player_game_processor(answer, 1)
        else:
            self.completed = True
            return None
        
    def get_single_player_game_processor(self, answer: int, tries: int) -> Processor:
        def single_player_game_processor(self, input_str: str) -> Processor:
            guess = int(input_str)
            if guess < answer:
                self.output = "Your guess is too low.\nEnter your guess: "
                return self.get_single_player_game_processor(answer, tries + 1)
            elif guess > answer:
                self.output = "Your guess is too high.\nEnter your guess: "
                return self.get_single_player_game_processor(answer, tries + 1)
            else:
                word = "guess" if tries == 1 else "guesses"
                self.output = f"Correct! {tries} {word}.\n" + self.SELECT_MODE_MESSAGE
                return AppModel.process_mode_selection
        return single_player_game_processor