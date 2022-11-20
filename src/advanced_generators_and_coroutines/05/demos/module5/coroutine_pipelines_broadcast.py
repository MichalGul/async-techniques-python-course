from coroutine_decorator import coroutine


@coroutine
def broadcast(targets):
    while True:
        item = yield
        for target in targets:
            target.send(item)


@coroutine
def filter_by_pattern(pattern, target):
    print(f'I am going to filter lines by pattern {pattern}')
    while True:
        line = yield
        if pattern in line:
            target.send(line)


def iterate_file(file, target):
    with open(file) as f:
        for line in f:
            target.send(line)
    print('Im done!')


@coroutine
def coprint():
    while True:
        line = yield
        print(f'-->{line}\n')

# Example usage
printer = coprint()

filter_1 = filter_by_pattern('python', printer)
filter_2 = filter_by_pattern('favicon', printer)
filter_3 = filter_by_pattern('C89', printer)

broadcaster = broadcast([filter_1, filter_2, filter_3])

iterate_file("test.txt", broadcaster)


