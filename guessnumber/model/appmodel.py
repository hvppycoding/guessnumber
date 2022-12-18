from guessnumber.model.positiveintegergenerator import PositiveIntegerGenerator


class AppModel:
    def __init__(self, generator: PositiveIntegerGenerator):
        pass

    def is_completed(self) -> bool:
        return True

    def flush_output(self) -> None:
        pass

    def process_input(self, input_str: str) -> None:
        pass
