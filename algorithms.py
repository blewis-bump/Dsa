import random


def _random_list(n):
    return [random.randint(0, n) for _ in range(n)]


def linear_search(n):
    data = _random_list(n)
    target = -1  # forces worst-case: scans the entire list
    for value in data:
        if value == target:
            return True
    return False


def binary_search(n):
    data = list(range(n))
    target = -1  # forces worst-case: never found
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == target:
            return True
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return False


def bubble_sort(n):
    data = _random_list(n)
    for i in range(len(data)):
        for j in range(0, len(data) - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


def nested_loops(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += 1
    return total


def insertion_sort(n):
    data = _random_list(n)
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data


def selection_sort(n):
    data = _random_list(n)
    for i in range(len(data)):
        min_idx = i
        for j in range(i + 1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    return data


ALGORITHMS = {
    "linear_search": linear_search,
    "binary_search": binary_search,
    "bubble_sort": bubble_sort,
    "nested_loops": nested_loops,
    "insertion_sort": insertion_sort,
    "selection_sort": selection_sort,
}

