

class DataCapture:
    """
    Processing of positive numbers, generating statistical data about them, providing methods for accessing such
    information, relative to any processed number.
    """

    def __init__(self):
        self.numbers = list()
        self.stats = dict()

    def add(self, number: int) -> None:
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
        self.numbers.sort()

        for n in self.numbers:
            idx_less = self.numbers.index(n)
            idx_greater = len(self.numbers) - self.numbers[::-1].index(n) - 1
            if n not in self.stats:
                self.stats[n] = {
                    "less": self.numbers[:idx_less],
                    "greater": self.numbers[idx_greater + 1:],
                    "number_and_repetitions": self.numbers[idx_less: idx_greater + 1]
                }

        return self

    def less(self, x: int) -> list:
        return self.stats[x]["less"]

    def greater(self, x: int) -> list:
        return self.stats[x]["greater"]

    def between(self, start: int, end: int) -> list:
        end_idx = self.stats[start]["greater"].index(end)
        if len(self.stats[start]["number_and_repetitions"]) > 1:
            return self.stats[start]["number_and_repetitions"] + self.stats[start]["greater"][:end_idx + 1]
        else:
            return [start] + self.stats[start]["greater"][:end_idx + 1]
