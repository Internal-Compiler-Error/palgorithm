import math


def remove(arr, v):
    writer = 0

    for reader in range(len(arr)):
        if arr[reader] == v:
            continue

        # they will differ if and only if some element has been skipped
        if writer != reader: arr[writer] = arr[reader]
        writer += 1

    return writer


def unique(arr):
    if not arr:
        return 0

    writer = 1
    for reader in range(1, len(arr)):
        # invariant: arr[:writer] is unique and sorted
        if arr[writer - 1] == arr[reader]:
            continue

        arr[writer] = arr[reader]
        writer += 1

    return writer


def set_union(x, y, out):
    x_i, y_i = 0, 0

    while x_i != len(x):
        if y_i == len(y):
            out.extend(x[x_i:])
            break

        if x[x_i] < y[y_i]:
            out.append(x[x_i])
            x_i += 1
        else:
            out.append(y[y_i])
            if x[x_i] == y[y_i]:
                x_i += 1
            y_i += 1

    if y_i < len(y):
        out.extend(y[y_i:])

    return len(out)


def set_intersection(x, y, out):
    x_i, y_i = 0, 0

    while x_i != len(x) and y_i != len(y):
        if x[x_i] < y[y_i]:
            x_i += 1
        elif x[x_i] > y[y_i]:
            y_i += 1
        else:
            out.append(x[x_i])
            x_i += 1

    return len(out)


def cycle_from(arr, i, f):
    tmp = arr[i]

    writer, reader = i, f(i)

    while reader != i:
        arr[writer] = arr[reader]
        writer = reader
        reader = f(reader)
    arr[writer] = tmp


# Identical to rotate(arr, k) with a different implementation
def cyclic_shift_right(arr, k):
    n = len(arr)
    if n == 0:
        return

    k %= n
    if k == 0:
        return

    cycles = math.gcd(n - k, k)

    for offset in range(cycles):
        cycle_from(arr, offset, lambda i: (i + (n - k)) % n)
