from guessnumber.model.positiveintegergenerator import PositiveIntegerGenerator


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
        self.answer = None
        self.single_player_mode = False
        self.tries = 0

    def is_completed(self) -> bool:
        return self.completed

    def flush_output(self) -> str:
        return self.output

    def process_input(self, input_str: str) -> None:
        if self.single_player_mode:
            self.process_single_player_game(input_str)
        else:
            self.prcess_mode_selection(input_str)

    def process_single_player_game(self, input_str):
        self.tries += 1
        guess = int(input_str)
        if guess < self.answer:
            self.output = "Your guess is too low.\nEnter your guess: "
        elif guess > self.answer:
            self.output = "Your guess is too high.\nEnter your guess: "
        else:
            word = "guess" if self.tries == 1 else "guesses"
            self.output = f"Correct! {self.tries} {word}.\n" + self.SELECT_MODE_MESSAGE
            self.single_player_mode = False

    def prcess_mode_selection(self, input_str):
        if input_str == "1":
            self.answer = self.generator.generate_less_than_or_equal_to_hundred()
            self.output = (
                    "Single player game\n"
                    + "I'm thinking of a number between 1 and 100.\n"
                    + "Enter your guess: "
                )
            self.single_player_mode = True
        else:
            self.completed = True
        