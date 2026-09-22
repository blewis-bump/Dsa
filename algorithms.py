import random

from data_structures import Stack, Queue


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


def stack_push_pop(n):
    """Push n items then pop them all back off. Both ops are O(1), so this
    is expected to scale as O(n) overall."""
    s = Stack()
    for i in range(n):
        s.push(i)
    while not s.is_empty():
        s.pop()
    return True


def queue_enqueue_dequeue(n):
    """Enqueue n items then dequeue them all. enqueue is O(1) but this
    Queue's dequeue is O(n) (list.pop(0) shifts every remaining element),
    so this is expected to scale as O(n^2) overall."""
    q = Queue()
    for i in range(n):
        q.enqueue(i)
    while not q.is_empty():
        q.dequeue()
    return True


def stack_based_reversal(n):
    """Reverse a list of n items using a Stack. Push is O(1) * n, pop is
    O(1) * n, so this is expected to scale as O(n)."""
    data = _random_list(n)
    s = Stack()
    for value in data:
        s.push(value)
    reversed_data = []
    while not s.is_empty():
        reversed_data.append(s.pop())
    return reversed_data


def queue_based_rotation(n):
    """Rotate a list of n items by repeatedly dequeuing from the front and
    enqueuing back to the end. dequeue is O(n) here, so this is expected to
    scale as O(n^2)."""
    data = _random_list(n)
    q = Queue()
    for value in data:
        q.enqueue(value)
    for _ in range(len(data)):
        front = q.dequeue()
        q.enqueue(front)
    return True


ALGORITHMS = {
    "linear_search": linear_search,
    "binary_search": binary_search,
    "bubble_sort": bubble_sort,
    "nested_loops": nested_loops,
    "insertion_sort": insertion_sort,
    "selection_sort": selection_sort,
    "stack_push_pop": stack_push_pop,
    "queue_enqueue_dequeue": queue_enqueue_dequeue,
    "stack_based_reversal": stack_based_reversal,
    "queue_based_rotation": queue_based_rotation,
}

