from collections import namedtuple
from numpy import random
from coroutine_decorator import coroutine


@coroutine
def averager_with_result():
    Result = namedtuple('Result', ['Count', 'Average'])
    total = 0
    sum = 0
    average = None
    while True:
        value = yield average
        if value is None:
            break
        total += 1
        sum += value
        average = sum / total
    return Result(total, average)


def generator_with_return(size):
    magic_values = random.random_integers(0, 10, size=size)
    for value in magic_values:
        yield value
    return magic_values


def generate_with_negated_and_data(negated, data):
    result = namedtuple('Result', ['Data', 'Negated'])
    for d in data:
        for n in negated:
            yield n + d + 1
    return result(data, negated)


def pipeline(number):
    data = (i for i in range(number))
    squared = (i**2 for i in data)
    negated = (-i for i in squared)
    return generate_with_negated_and_data(negated=negated, data=data)


averager = averager_with_result()

print(averager.send(2))

print(averager.send(5))
print(averager.send(1))

print(averager.send(0))
try:
    print(averager.send(None))
except StopIteration as e:
    print(e)

for i in pipeline(20):
    print(i)
