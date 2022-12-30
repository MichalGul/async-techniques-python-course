import datetime
import colorama
import random
import time
import threading


def main():
    t0 = datetime.datetime.now()
    print(colorama.Fore.WHITE + "App started.", flush=True)

    data = []
    con = threading.Condition()
    threads = [
        threading.Thread(target=generate_data, args=(1, data), daemon=True),
        threading.Thread(target=generate_data, args=(2, data), daemon=True),
        threading.Thread(target=process_data, args=(40, data), daemon=True),
    ]
    abort_thread = threading.Thread(target=check_cancel, daemon=True)
    abort_thread.start()

    [t.start() for t in threads]

    while any([t.is_alive() for t in threads]):
        [t.join(.001) for t in threads]
        print(colorama.Fore.WHITE + "quick alive check")
        if not abort_thread.is_alive():
            print("Cancelling on your request!", flush=True)
            break

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + f"App exiting, total time: {dt.total_seconds():,.2f} sec.", flush=True)


def check_cancel():
    print(colorama.Fore.RED + "Press enter to cancel...", flush=True)
    input()
    time.sleep(5)
    print('Waited 5 sec')


def check_cancel_condition(con):
    print(colorama.Fore.RED + "Press enter to cancel...", flush=True)
    input()
    while True:
        text = input("type in enter")
        if text == "":
            con.acquire()
            con.notify()
            print("Notified thread")
            con.release()
        else:
            print("Pressed sth else")
def generate_data(num: int, data: list):
        while True:
            item = random.randrange(1, 10000)
            data.append((item, datetime.datetime.now()))

            print(colorama.Fore.YELLOW + f" -- generated item {item}", flush=True)
            time.sleep(0.02)


def generate_data_condition(num: int, data: list, condition_obj):
    condition_obj.acquire()
    # exit_flag = threading.Event()
    # with condition_obj:
    # while not exit_flag.wait(timeout=0.02):
    while True:
        item = random.randrange(1, 10000)
        data.append((item, datetime.datetime.now()))
        print(colorama.Fore.RED + f" -- generated item {item}", flush=True)
        condition_obj.wait(1)

    condition_obj.release()

def generate_data_event(num: int, data: list, condition_obj):
    # exit_flag = threading.Event()
    # while not exit_flag.wait(timeout=0.02):

    while True:
        if num==1:
            item = random.randrange(1,2)
        else:
            item = random.randrange(2,3)

        data.append((item, datetime.datetime.now()))
        f = open(f"demofile{num}.txt", "a")
        f.write(f'{str(item)} \n')
        f.close()
        print(colorama.Fore.RED + f" -- generated item {item}", flush=True)
        time.sleep(5)

def process_data(num: int, data: list):
    processed = 0
    while True:
        item = None

        if data:
            item = data.pop(0)
        if not item:
            time.sleep(.01)
            continue

        processed += 1
        value = item[0]
        t = item[1]
        dt = datetime.datetime.now() - t

        print(colorama.Fore.CYAN +
              f" +++ Processed value {value} after {dt.total_seconds():,.2f} sec.", flush=True)
        time.sleep(0.02)


if __name__ == '__main__':
    main()
