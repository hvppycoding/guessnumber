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
    
    sut.process_input(str(guess))
    
    actual = sut.flush_output()
    expected = "Your guess is too high.\nEnter your guess: "
    
    assert actual == expected
    
@pytest.mark.parametrize('answer', [1, 3, 10, 100])
def test_sut_correctly_prints_correct_message_in_single_player_game(answer: int):
    sut = AppModel(PositiveIntegerGeneratorStub([answer]))
    sut.flush_output()
    sut.process_input("1")
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