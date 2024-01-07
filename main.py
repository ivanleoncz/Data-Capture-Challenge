

def validate_parameter(func):
    """
    Decorator for validating single input of multiple methods.
    """
    def inner(self, x: int):
        if not isinstance(x, int):
            raise TypeError(f"only 'int' values are allowed (received '{type(x).__name__}'")
        if func.__name__ == "add" and 1 > x or x > 1000:
            raise ValueError(f"only values from 1 to 1000 are allowed (received {x})")
        if (func.__name__ == "less" or func.__name__ == "greater") and not self.stats.get(x):
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
        if not self.stats.get(start) or not self.stats.get(end):
            raise ValueError(f"'{start}' and/or '{end}' was/were not processed. See add() and "
                             f"build_stats() for more info.")
        if start > end:
            raise ValueError(f"'{start}' must be lesser than '{end}', or equal.")
        return func(self, start, end)

    return inner


class DataCapture:
    """
    Processing of positive numbers, generating statistical data about them, providing methods for accessing such
    information, relative to any processed number.
    """

    def __init__(self):
        self.numbers = []
        self.stats = {}

    @validate_parameter
    def add(self, number: int) -> None:
        """
        Appends integers to self.numbers for further statistical processing.
        """
        self.numbers.append(number)

    def build_stats(self):
        """
        Builds self.stats dict, using self.numbers as keys.

        Each "key number", has a dictionary as value, containing statistical data about the "key number", regarding
        other numbers from self.numbers.

        Input: self.numbers = [4, 2, 4, 6]
        Output: self.stats = {
                                2: {"less": 0, "greater": 3, "frequency": 1, "pointer_processed": True},
                                4: {"less": 1, "greater": 1, "frequency": 2, "pointer_processed": True},
                                6: {"less": 3, "greater": 0, "frequency": 1, "pointer_processed": True}
                            }
        """
        if not self.numbers:
            raise TypeError("cannot build statistics without numbers. Use add() method to add some.")

        pointer = 0
        index = 0

        while True:

            # Increment 'pointer' and reset 'index', if 'index' reached the size of 'numbers'
            if index == len(self.numbers):
                pointer += 1
                index = 0

            # End of processing, if 'pointer' reached the size of 'numbers'
            if pointer == len(self.numbers):
                break

            pointer_number = self.numbers[pointer]
            index_number = self.numbers[index]

            # Adding entry for new number
            pointer_data = self.stats.get(pointer_number)
            if not pointer_data:
                self.stats[pointer_number] = {
                    "less": 0,
                    "greater": 0,
                    "frequency": 0,
                    "pointer_processed": False
                }

            # If 'pointer_number' was already processed, increment index until it gets exhausted,
            # then 'pointer' is incremented, moving to another 'pointer_number'.
            if pointer_data and pointer_data.get("pointer_processed"):
                index += 1
                continue

            # If 'pointer_number' was already processed, and it's the same number as 'index_number',
            # then 'pointer_number'['frequency'] is incremented
            pointer_data = self.stats.get(pointer_number)
            if pointer_data and pointer_number == index_number:
                self.stats[pointer_number]["frequency"] += 1

            # Determining if 'index_number' is lesser or greater than 'pointer_number'
            if index_number < pointer_number:
                self.stats[pointer_number]["less"] += 1
            elif index_number > pointer_number:
                self.stats[pointer_number]["greater"] += 1

            # If 'pointer_number' is not marked as processed (yet) and the last index of 'numbers' was reached
            if (index + 1) == len(self.numbers) and not self.stats[pointer_number]["pointer_processed"]:
                self.stats[pointer_number]["pointer_processed"] = True

            index += 1

        return self

    @validate_parameter
    def less(self, x: int) -> int:
        """
        Returns amount of numbers lesser than "x".
        """
        return self.stats[x]["less"]

    @validate_parameter
    def greater(self, x: int) -> int:
        """
        Returns amount of numbers greater than "x".
        """
        return self.stats[x]["greater"]

    @validate_parameters
    def between(self, start: int, end: int) -> int:
        """
        Returns number of integers between "start" and "end" (both inclusive) from self.stats.
        """
        start_data = self.stats[start]
        end_data = self.stats[end]
        if start_data["less"] == 0 and end_data["greater"] == 0:
            return start_data["greater"] + start_data["frequency"]
        else:
            return (end_data["less"] + end_data["frequency"]) - start_data["less"]
