![Action](https://github.com/ivanleoncz/Data-Capture-Challenge/actions/workflows/tests.yml/badge.svg)

# Data-Capture-Challenge
Code challenge of obtaining statistical data from a list of numbers.

### Requirements
- [Python 3.8](https://www.python.org/downloads/release/python-3816/)

### Usage

```
>>> from main import DataCapture
>>> dc = DataCapture()
>>> dc.add(4)
>>> dc.add(1)
>>> dc.add(3)
>>> dc.add(1)
>>> dc.add(8)
>>> stats = dc.build_stats()
>>> stats.less(3)
[1, 1]
>>> stats.greater(1)
[3, 4, 8]
>>> stats.between(1, 3)
[1, 1, 3]
```

### Running Tests

```
python tests.py
```