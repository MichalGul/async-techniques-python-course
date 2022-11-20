import inspect

from coroutine_decorator import coroutine


@coroutine
def coroutine_exception(number):
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except ValueError:
            print('*** ValueError handled. Continuing...')
        except GeneratorExit:
            print('This is executed if I get closed, so I need to cleanup here and die gracefully')
            raise
        else:
            print('-> coroutine received: {!r}'.format(x))
            number + x


@coroutine
def coroutine_wihtout_reraise():
    while True:
        try:
            x = yield
        except GeneratorExit:
            print('I do nothing')
        else:
            print(f'Got value {x}')


coro = coroutine_exception(5)
coro.send(2)

coro.throw(ValueError)
coro.throw(TypeError)

# try:
#     coro.send(None)
# except TypeError as e:
#     print(f"Cauth {e}")
#     print(inspect.getgeneratorstate((coro)))


# coro1 = coroutine_wihtout_reraise()
# coro1.send(3)
# coro1.send(11)
#
# coro1.close()
