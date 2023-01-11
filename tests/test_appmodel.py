import pytest
from typing import List

from guessnumber.model.appmodel import AppModel
from guessnumber.model.positiveintegergenerator import PositiveIntegerGenerator

class PositiveIntegerGeneratorStub(PositiveIntegerGenerator):
    def __init__(self, numbers: List[int]) -> None:
        super().__init__()
        self.numbers = numbers
        self.index = 0
    
    def generate_less_than_or_equal_to_hundred(self) -> int:
        number = self.numbers[self.index]
        self.index = (self.index + 1) % len(self.numbers)
        return number


def test_sut_is_incompleted_when_it_is_initialized():
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    actual = sut.is_completed()
    assert not actual


def test_sut_correctly_prints_select_mode_message():
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    actual = sut.flush_output()
    expected = (
        "1: Single player game\n"
        + "2: Multiplayer game\n"
        + "3: Exit\n"
        + "Enter selection: "
    )
    
    assert actual == expected

def test_sut_correctly_exits():
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.process_input("3")
    
    actual = sut.is_completed()
    
    assert actual
    
def test_sut_corectly_prints_single_player_game_start_message():
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.flush_output()
    sut.process_input("1")
    
    actual = sut.flush_output()
    
    expected = (
        "Single player game\n"
        + "I'm thinking of a number between 1 and 100.\n"
        + "Enter your guess: "
    )
    assert actual == expected
    
@pytest.mark.parametrize(
    'answer, guess',
    [
        (50, 40),
        (30, 29),
        (89, 9),
    ]
)
def test_sut_correctly_prints_too_low_message_in_single_player_game(answer: int, guess: int):
    sut = AppModel(PositiveIntegerGeneratorStub([answer]))
    sut.flush_output()
    
    sut.process_input("1")
    actual = sut.flush_output()
    
    sut.process_input(str(guess))
    actual = sut.flush_output()
    expected = "Your guess is too low.\nEnter your guess: "
    
    assert actual == expected
    

@pytest.mark.parametrize(
    'answer, guess',
    [
        (50, 60),
        (80, 81),
    ]
)
def test_sut_correctly_prints_too_high_message_in_single_player_game(answer: int, guess: int):
    sut = AppModel(PositiveIntegerGeneratorStub([answer]))
    sut.flush_output()
    
    sut.process_input("1")
    sut.flush_output()
    
    sut.process_input(str(guess))
    actual = sut.flush_output()
    expected = "Your guess is too high.\nEnter your guess: "
    
    assert actual == expected
    
@pytest.mark.parametrize('answer', [1, 3, 10, 100])
def test_sut_correctly_prints_correct_message_in_single_player_game(answer: int):
    sut = AppModel(PositiveIntegerGeneratorStub([answer]))
    sut.flush_output()
    sut.process_input("1")
    sut.flush_output()
    sut.process_input(str(answer))
    actual = sut.flush_output()
    assert actual.startswith("Correct! ")
    
    
@pytest.mark.parametrize('fails', [1, 10, 100])
def test_sut_correctly_prints_guess_count_if_single_player_game_finished(fails: int):
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.flush_output()
    sut.process_input("1")
    
    for i in range(fails):
        sut.process_input("30")
    sut.process_input("50")
    
    actual = sut.flush_output()
     
    assert f"{fails + 1} guesses.\n" in actual
    
def test_sut_correctly_prints_one_guess_if_single_player_game_finished():
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.flush_output()
    sut.process_input("1")
    sut.process_input("50")
    actual = sut.flush_output()
    assert "1 guess." in actual
    
def test_sut_prints_select_mode_message_if_single_player_game_finished():
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.flush_output()
    sut.process_input("1")
    sut.process_input("50")
    actual = sut.flush_output()
    assert actual.endswith(
        "1: Single player game\n"
        + "2: Multiplayer game\n"
        + "3: Exit\n"
        + "Enter selection: "
    )
    
def test_sut_returns_to_mode_selection_if_single_player_game_finished():
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.flush_output()
    sut.process_input("1")
    sut.process_input("50")
    sut.process_input("3")

    assert sut.is_completed()
    
@pytest.mark.parametrize('source', ["100, 10, 1"])
def test_sut_generates_answer_for_each_game(source: str):
    answers = [int(w.strip()) for w in source.split(",")]
    
    sut = AppModel(PositiveIntegerGeneratorStub(answers))
    for ans in answers:
        sut.process_input("1")
        sut.flush_output()
        sut.process_input(str(ans))
        actual = sut.flush_output()
        assert actual.startswith("Correct! ")
        
def test_sut_correctly_prints_multiplayer_game_setup_message():
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.flush_output()
    sut.process_input("2")
    actual = sut.flush_output()
    
    assert actual == "Multiplayer game\nEnter player names separated with commas: "
    
def test_sut_correctly_prints_multiplayer_game_start_message():
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.process_input("2")
    sut.flush_output()
    sut.process_input("Foo, Bar")
    
    actual = sut.flush_output()
    assert actual.startswith("I'm thinking of a number between 1 and 100.\n")
    
@pytest.mark.parametrize(
    'player1, player2, player3',
    [
        ("Foo", "Bar", "Baz"),
        ("Bar", "Baz", "Foo"),
        ("Baz", "Foo", "Bar"),
    ]
)
def test_sut_correctly_prompts_first_player_name(player1: str, player2: str, player3: str):
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.process_input("2")
    sut.flush_output()
    sut.process_input(", ".join([player1, player2, player3]))
    
    actual = sut.flush_output()
    assert actual.endswith(f"Enter {player1}'s guess: ")
    
@pytest.mark.parametrize(
    'player1, player2, player3',
    [
        ("Foo", "Bar", "Baz"),
        ("Bar", "Baz", "Foo"),
        ("Baz", "Foo", "Bar"),
    ]
)
def test_sut_correctly_prompts_second_player_name(player1: str, player2: str, player3: str):
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.process_input("2")
    sut.flush_output()
    sut.process_input(", ".join([player1, player2, player3]))
    sut.process_input("10")
    
    actual = sut.flush_output()
    assert actual.endswith(f"Enter {player2}'s guess: ")
    
@pytest.mark.parametrize(
    'player1, player2, player3',
    [
        ("Foo", "Bar", "Baz"),
        ("Bar", "Baz", "Foo"),
        ("Baz", "Foo", "Bar"),
    ]
)
def test_sut_correctly_prompts_third_player_name(player1: str, player2: str, player3: str):
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.process_input("2")
    sut.flush_output()
    sut.process_input(", ".join([player1, player2, player3]))
    sut.process_input("10")
    sut.process_input("10")
    
    actual = sut.flush_output()
    assert actual.endswith(f"Enter {player3}'s guess: ")

@pytest.mark.parametrize(
    'player1, player2, player3',
    [
        ("Foo", "Bar", "Baz"),
        ("Bar", "Baz", "Foo"),
        ("Baz", "Foo", "Bar"),
    ]
)
def test_sut_correctly_rounds_players(player1: str, player2: str, player3: str):
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.process_input("2")
    sut.flush_output()
    sut.process_input(", ".join([player1, player2, player3]))
    sut.process_input("10")
    sut.process_input("10")
    sut.process_input("10")
    
    actual = sut.flush_output()
    assert actual.endswith(f"Enter {player1}'s guess: ")
    
@pytest.mark.parametrize(
    'answer, guess, fails, lastPlayer',
    [
        (50, 40, 1, "Foo"),
        (30, 29, 2, "Bar"),
    ]
)
def test_sut_correctly_prints_too_low_message_in_multiplayer_game(answer: int, guess: int, fails: int, lastPlayer: str):
    sut = AppModel(PositiveIntegerGeneratorStub([answer]))
    sut.process_input("2")
    sut.flush_output()
    sut.process_input("Foo, Bar, Baz")
    
    for _ in range(fails):
        sut.flush_output()
        sut.process_input(str(guess))
    
    actual = sut.flush_output()
    assert actual.startswith(f"{lastPlayer}'s guess is too low.")
    
@pytest.mark.parametrize(
    'answer, guess, fails, lastPlayer',
    [
        (50, 60, 1, "Foo"),
        (30, 39, 2, "Bar"),
    ]
)
def test_sut_correctly_prints_too_high_message_in_multiplayer_game(answer: int, guess: int, fails: int, lastPlayer: str):
    sut = AppModel(PositiveIntegerGeneratorStub([answer]))
    sut.process_input("2")
    sut.flush_output()
    sut.process_input("Foo, Bar, Baz")
    
    for _ in range(fails):
        sut.flush_output()
        sut.process_input(str(guess))
    
    actual = sut.flush_output()
    assert actual.startswith(f"{lastPlayer}'s guess is too high.")
    
@pytest.mark.parametrize('answer', [1, 10, 100])
def test_sut_correctly_prints_correct_message_in_multiplayer_game(answer: int):
    sut = AppModel(PositiveIntegerGeneratorStub([answer]))
    sut.process_input("2")
    sut.flush_output()
    sut.process_input("Foo, Bar, Baz")
    sut.flush_output()
    sut.process_input(str(answer))
    actual = sut.flush_output()
    assert actual.startswith("Correct! ")
    
@pytest.mark.parametrize(
    "fails, winner",
    [
        (0, "Foo"),
        (1, "Bar"),
        (2, "Baz"),
        (99, "Foo"),
        (100, "Bar"),
    ]
)
def test_sut_correctly_prints_winner_if_multiplayer_game_finished(fails: int, winner: str):
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.process_input("2")
    sut.flush_output()
    sut.process_input("Foo, Bar, Baz")
    sut.flush_output()
    for i in range(fails):
        sut.process_input("30")
        sut.flush_output()
    sut.process_input(str(50))
    actual = sut.flush_output()
    assert f"{winner} wins.\n" in actual
        
def test_sut_prints_select_mode_message_if_multiplayer_game_finished():
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.process_input("2")
    sut.flush_output()
    sut.process_input("Foo, Bar, Baz")
    sut.flush_output()
    sut.process_input("50")
    actual = sut.flush_output()
    assert actual.endswith(
        "1: Single player game\n"
        + "2: Multiplayer game\n"
        + "3: Exit\n"
        + "Enter selection: "
    )
    
def test_sut_prints_select_mode_message_if_multiplayer_game_finished():
    sut = AppModel(PositiveIntegerGeneratorStub([50]))
    sut.process_input("2")
    sut.flush_output()
    sut.process_input("Foo, Bar, Baz")
    sut.process_input("20")
    sut.process_input("50")
    sut.process_input("3")
    assert sut.is_completed()
    
