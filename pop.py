import time

a = [1, 2, 3, 4, 5, 6, 7]
i = len(a) - 1

while True:
    # takes latest out
    if i < 0:
        a = [1, 2, 3, 4, 5, 6, 7]
        i = len(a) - 1
    a.pop(i)
    i = -1
    print(a)
    time.sleep(1)
