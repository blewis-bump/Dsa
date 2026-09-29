import random

from data_structures import Queue, Stack


def random_list(n):
    """Return a list of n random integers between 0 and n."""
    return [random.randint(0, n) for _ in range(n)]


# ---------- Searching ----------

def linear_search(n):
    """O(n): check every item one by one."""
    data = random_list(n)
    target = -1  # never in the list, so every item gets checked
    for value in data:
        if value == target:
            return True
    return False


def binary_search(n):
    """O(log n): repeatedly halve a sorted list."""
    data = list(range(n))  # already sorted
    target = -1  # never in the list
    low, high = 0, len(data) - 1
    while low <= high:
        middle = (low + high) // 2
        if data[middle] == target:
            return True
        if data[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return False


# ---------- Sorting ----------

def bubble_sort(n):
    """O(n^2): keep swapping neighbours that are in the wrong order."""
    data = random_list(n)
    for i in range(len(data)):
        for j in range(len(data) - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


def insertion_sort(n):
    """O(n^2): insert each item into its place in the already-sorted front part."""
    data = random_list(n)
    for i in range(1, len(data)):
        current = data[i]
        j = i - 1
        while j >= 0 and data[j] > current:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = current
    return data


def selection_sort(n):
    """O(n^2): find the smallest remaining item and move it to the front."""
    data = random_list(n)
    for i in range(len(data)):
        smallest = i
        for j in range(i + 1, len(data)):
            if data[j] < data[smallest]:
                smallest = j
        data[i], data[smallest] = data[smallest], data[i]
    return data


# ---------- Baseline ----------

def nested_loops(n):
    """O(n^2): two loops inside each other, with no other work. A reference curve."""
    count = 0
    for _ in range(n):
        for _ in range(n):
            count += 1
    return count


# ---------- Stack and Queue ----------

def stack_push_pop(n):
    """O(n): push n items, then pop them all. Each push/pop is O(1)."""
    stack = Stack()
    for i in range(n):
        stack.push(i)
    while not stack.is_empty():
        stack.pop()
    return True


def queue_enqueue_dequeue(n):
    """O(n^2): enqueue n items, then dequeue them all. Each dequeue is O(n) here."""
    queue = Queue()
    for i in range(n):
        queue.enqueue(i)
    while not queue.is_empty():
        queue.dequeue()
    return True


def stack_based_reversal(n):
    """O(n): reverse a list by pushing every item onto a stack and popping them off."""
    data = random_list(n)
    stack = Stack()
    for value in data:
        stack.push(value)
    reversed_data = []
    while not stack.is_empty():
        reversed_data.append(stack.pop())
    return reversed_data


def queue_based_rotation(n):
    """O(n^2): move the front item to the back, n times. Each dequeue is O(n) here."""
    queue = Queue()
    for value in random_list(n):
        queue.enqueue(value)
    for _ in range(n):
        queue.enqueue(queue.dequeue())
    return True


# The name used in API requests (?algo=...) -> the function to run.
ALGORITHMS = {
    "linear_search": linear_search,
    "binary_search": binary_search,
    "bubble_sort": bubble_sort,
    "insertion_sort": insertion_sort,
    "selection_sort": selection_sort,
    "nested_loops": nested_loops,
    "stack_push_pop": stack_push_pop,
    "queue_enqueue_dequeue": queue_enqueue_dequeue,
    "stack_based_reversal": stack_based_reversal,
    "queue_based_rotation": queue_based_rotation,
}

