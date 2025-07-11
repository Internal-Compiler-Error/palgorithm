
def remove(arr, v):
    writer = 0

    for reader in range(len(arr)):
        if arr[reader] == v:
            continue

        if writer != reader: arr[writer] = arr[reader]
        writer += 1

    return writer

l = [1, 2, 3]
end = remove(l, 1)
assert l[:end] == [2, 3]

l = [1, 1, 1]
end = remove(l, 1)
assert l[:end] == []

l = [1, 2, 3, 4, 5]
end = remove(l, 3)
assert l[:end] == [1, 2, 4, 5]

l = [1, 2, 3, 4, 5]
end = remove(l, 6)
assert l[:end] == [1, 2, 3, 4, 5]

l = []
end = remove(l, 1)
assert l[:end] == []

l = [1]
end = remove(l, 1)
assert l[:end] == []

l = [1, 2, 1, 3, 1]
end = remove(l, 1)
assert l[:end] == [2, 3]

l = [5, 4, 3, 2, 1]
end = remove(l, 5)
assert l[:end] == [4, 3, 2, 1]

l = [1, 2, 3, 4, 5]
end = remove(l, 5)
assert l[:end] == [1, 2, 3, 4]

def unique(arr):
    if not arr:
        return 0

    writer = 1
    for reader in range(1, len(arr)):
        if arr[reader] != arr[writer - 1]:
            arr[writer] = arr[reader]
            writer += 1

    return writer


l = [1, 1, 2, 2, 3, 3]
end = unique(l)
assert l[:end] == [1, 2, 3]

l = [1, 2, 3, 4, 5]
end = unique(l)
assert l[:end] == [1, 2, 3, 4, 5]

l = [1, 1, 1, 1, 1]
end = unique(l)
assert l[:end] == [1]

l = []
end = unique(l)
assert l[:end] == []

l = [1]
end = unique(l)
assert l[:end] == [1]

l = [1, 1]
end = unique(l)
assert l[:end] == [1]

l = [1, 2, 2, 3, 3, 3, 4, 5, 5]
end = unique(l)
assert l[:end] == [1, 2, 3, 4, 5]

l = [0, 0, 0, 1, 1, 2, 3, 3, 3, 3, 4, 5, 5, 5]
end = unique(l)
assert l[:end] == [0, 1, 2, 3, 4, 5]

def set_union(x, y, out):
    x_i, y_i = 0, 0

    while x_i != len(x):
        if y_i == len(y):
            out.extend(x[x_i:])
            break

        if x[x_i] < y[y_i]:
            out.append(x[x_i])
            x_i += 1
        elif x[x_i] >= y[y_i]:
            out.append(y[y_i])
            if x[x_i] == y[y_i]:
                x_i += 1
            y_i += 1

    if y_i < len(y):
        out.extend(y[y_i:])

    return len(out)


x = [1, 2, 3]
y = [4, 5, 6]
out = []
end = set_union(x, y, out)
assert out[:end] == [1, 2, 3, 4, 5, 6]

x = [1, 3, 5]
y = [2, 3, 4, 5]
out = []
end = set_union(x, y, out)
assert out[:end] == [1, 2, 3, 4, 5]

x = []
y = [1, 2, 3]
out = []
end = set_union(x, y, out)
assert out[:end] == [1, 2, 3]

x = [1, 2, 3]
y = []
out = []
end = set_union(x, y, out)
assert out[:end] == [1, 2, 3]

x = []
y = []
out = []
end = set_union(x, y, out)
assert out[:end] == []

x = [1, 1, 2, 3]
y = [2, 3, 3, 4]
out = []
end = set_union(x, y, out)
assert out[:end] == [1, 1, 2, 3, 3, 4]

x = [5, 6]
y = [1, 2, 3]
out = []
end = set_union(x, y, out)
assert out[:end] == [1, 2, 3, 5, 6]

x = [1, 2, 5, 7, 8, 10]
y = [2, 3, 6, 8, 9, 11]
out = []
end = set_union(x, y, out)
assert out[:end] == [1, 2, 3, 5, 6, 7, 8, 9, 10, 11]

x = [1, 2, 3]
y = [1, 2, 3]
out = []
end = set_union(x, y, out)
assert out[:end] == [1, 2, 3]

x = [-3, -1, 0, 2]
y = [-2, -1, 0, 1]
out = []
end = set_union(x, y, out)
assert out[:end] == [-3, -2, -1, 0, 1, 2]

def set_intersection(x, y, out):
    x_i, y_i = 0, 0

    while x_i != len(x) and y_i != len(y):
        if x[x_i] < y[y_i]:
            x_i += 1
        elif x[x_i] > y[y_i]:
            y_i += 1
        elif x[x_i] == y[y_i]:
            out.append(x[x_i])
            x_i += 1

    return len(out)

out = []
end = set_intersection([2, 3, 4, 5, 6, 7, 7, 8],  [5, 7, 7, 9], out)
assert out[:end] == [5, 7, 7]


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

    import math
    m = n - k
    cycles = math.gcd(m, n - m)

    for offset in range(cycles):
        cycle_from(arr, offset, lambda i: (i + (n - k)) % len(arr))


l = [1, 2, 3, 4, 5]
cyclic_shift_right(l, 2)
print(l)
assert l == [4, 5, 1, 2, 3]
