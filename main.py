from collections import defaultdict


def validate_parameter(func):
    """
    Decorator for validating single input of multiple methods.
    """
    def inner(self, x: int):
        if not isinstance(x, int):
            raise TypeError(f"only 'int' values are allowed (received '{type(x).__name__}'")
        if func.__name__ == "add" and 1 > x or x >= 1000:
            raise ValueError(f"only values from 1 to 999 are allowed (received {x})")
        if func.__name__ in ("less", "greater") and x not in self.numbers:
            raise ValueError(f"'{x}' was not added/processed. See add() and build_stats() for more info.")
        return func(self, x)

    return inner


def validate_parameters(func):
    """
    Decorator for validating "self.between" method inputs.
    """
    def inner(self, start: int, end: int):
        if not isinstance(start, int) or not isinstance(start, int):
            raise TypeError(f"only 'int' values are allowed (received '{type(start).__name__}' and "
                            f"'{type(end).__name__}'")
        if start not in self.numbers or end not in self.numbers:
            raise ValueError(f"'{start}' and/or '{end}' was/were not processed. See add() and "
                             f"build_stats() for more info.")
        return func(self, start, end)

    return inner


class DataCapture:
    """
    Processing of positive numbers, generating statistical data about them, providing methods for accessing such
    information, relative to any processed number.
    """

    def __init__(self):
        self.numbers = list()
        self.stats = defaultdict(lambda: {"less": list(), "greater": list(), "number_and_repetitions": list()})

    @validate_parameter
    def add(self, number: int) -> None:
        """
        Appends integers between 1 and 999 to a list (self.numbers) for further statistical processing.
        """
        if number > 0:
            self.numbers.append(number)

    def build_stats(self):
        """
        Builds self.stats dict, using self.numbers as keys.

        Each "key number", has a dictionary as value, containing statistical data about the "key number", regarding
        other numbers from self.numbers: numbers that are lesser or greater than the "key number", are listed, as well
        as the "key number" number itself (and possible repetitions), are also listed

        Example: self.numbers = [2, 4, 4, 6]

        {
            2: {
                "less": [],
                "greater": [4, 6],
                "number_and_repetitions": [2],
            },
            4: {
                "less": [2],
                "greater": [6],
                "number_and_repetitions": [4, 4],
            },
            6: {
                "less": [2, 4, 4],
                "greater": [],
                "number_and_repetitions": [6],
            }
        }

        """
        if not self.numbers:
            raise TypeError("cannot build statistics without numbers. Use add() method to add some.")

        self.numbers.sort()

        for n in self.numbers:
            idx_less = self.numbers.index(n)
            idx_greater = len(self.numbers) - self.numbers[::-1].index(n) - 1
            self.stats[n] = {
                "less": self.numbers[:idx_less],
                "greater": self.numbers[idx_greater + 1:],
                "number_and_repetitions": self.numbers[idx_less: idx_greater + 1]
            }

        return self

    @validate_parameter
    def less(self, x: int) -> list:
        """
        Returns a list of numbers lesser than "x".
        """
        return self.stats[x]["less"]

    @validate_parameter
    def greater(self, x: int) -> list:
        """
        Returns a list of numbers greater than "x".
        """
        return self.stats[x]["greater"]

    @validate_parameters
    def between(self, start: int, end: int) -> list:
        """
        Returns list of integers between "start" and "end" that were processed via "add()" and "build_stats()" methods.
        """
        end_idx = self.stats[start]["greater"].index(end)
        if len(self.stats[start]["number_and_repetitions"]) > 1:
            return self.stats[start]["number_and_repetitions"] + self.stats[start]["greater"][:end_idx + 1]
        else:
            return [start] + self.stats[start]["greater"][:end_idx + 1]
