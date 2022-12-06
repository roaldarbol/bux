import random
import time
import keyboard


def send_settings(settings):
    while True:
        settings = yield (settings)
        if settings is not None:
            settings["num"] += 2
            res = settings["num"]
        else:
            res = None
        yield (res)


if __name__ == "__main__":
    inp = {"num: 7"}
    a = send_settings(inp)
    a.send(None)
    x = 0
    new_inp = None
    b = []
    while True:
        if x == 5:
            new_inp = {"num": 7}
            b.append(a.send(new_inp))
            a.send(None)
            break
        x += 1
        # print(x)
        time.sleep(0.1)
    while True:
        if x == 5:
            new_inp = {"num": 8}
            b.append(a.send(new_inp))
            a.send(None)
            break
        x += 1
        # print(x)
        time.sleep(0.1)
    print(b)
