from guessnumber.model.positiveintegergenerator import PositiveIntegerGenerator
from typing import Callable, List

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
        
    def print(self, s: str):
        self.output += s
        
    def println(self, s: str):
        self.output += s + "\n"

    def is_completed(self) -> bool:
        return self.completed

    def flush_output(self) -> str:
        s = self.output
        self.output = ""
        return s

    def process_input(self, input_str: str) -> None:
        self.processor = self.processor(self, input_str)

    def process_mode_selection(self, input_str: str) -> Processor:
        if input_str == "1":
            answer = self.generator.generate_less_than_or_equal_to_hundred()
            self.println("Single player game")
            self.println("I'm thinking of a number between 1 and 100.")
            self.print("Enter your guess: ")
            return self.get_single_player_game_processor(answer, 1)
        elif input_str == "2":
            self.println("Multiplayer game")
            self.print("Enter player names separated with commas: ")
            return AppModel.start_multi_player_game
        else:
            self.completed = True
            return None
        
    def get_single_player_game_processor(self, answer: int, tries: int) -> Processor:
        
        def single_player_game_processor(self: "AppModel", input_str: str) -> Processor:
            guess = int(input_str)
            if guess < answer:
                self.println("Your guess is too low.")
                self.print("Enter your guess: ")
                return self.get_single_player_game_processor(answer, tries + 1)
            elif guess > answer:
                self.println("Your guess is too high.")
                self.print("Enter your guess: ")
                return self.get_single_player_game_processor(answer, tries + 1)
            else:
                word = "guess" if tries == 1 else "guesses"
                self.println(f"Correct! {tries} {word}.")
                self.print(self.SELECT_MODE_MESSAGE)
                return AppModel.process_mode_selection
            
        return single_player_game_processor
    
    def start_multi_player_game(self, input_str: str):
        player_names = [name.strip() for name in input_str.split(",")]
        self.println("I'm thinking of a number between 1 and 100.")
        answer = self.generator.generate_less_than_or_equal_to_hundred()
        return self.get_multi_player_game_processor(player_names, answer, 1)
    
    def get_multi_player_game_processor(self, players: List[str], answer: int, tries: int) -> Processor:
        player = players[(tries - 1) % len(players)]
        self.print(f"Enter {player}'s guess: ")
        
        def multi_player_game_processor(self: "AppModel", input_str: str) -> Processor:
            guess = int(input_str)
            if answer > guess:
                self.println(f"{player}'s guess is too low.")
            elif answer < guess:
                self.println(f"{player}'s guess is too high.")
            else:
                self.println(f"Correct! {player} wins.")
                self.print(self.SELECT_MODE_MESSAGE)
                return AppModel.process_mode_selection
            return self.get_multi_player_game_processor(players, answer, tries + 1)
        
        return multi_player_game_processor