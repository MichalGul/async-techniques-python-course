def my_coroutine(a):
    print(f'--> Started with {a}')
    b = yield
    print(f'But continues with {b}')


coro=my_coroutine(2)
next(coro)
coro.close()
coro.send(33)
# next(coro)