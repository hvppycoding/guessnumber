import sys
from typing import List

from guessnumber.app import RandomGenerator
from guessnumber.model import AppModel


class App:
    def main(self, args: List[str]):
        model = AppModel(RandomGenerator())
        self.run_loop(model)

    def run_loop(self, model: AppModel):
        while not model.is_completed():
            print(model.flush_output())
            model.process_input(input())


def main():
    app = App()
    app.main(sys.argv)


if __name__ == "__main__":
    main()
