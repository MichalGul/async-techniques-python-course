def pipeline(number):
    data = (i for i in range(number))
    squared = (i**2 for i in data)
    negated = (-i for i in squared)
    return (n + 1 for n in negated)


a = pipeline(10)

next(a)

print(next(a))
print(next(a))
print(next(a))
print(next(a))