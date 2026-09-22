"""Stack and Queue implementations.

Both are built on a Python list and raise ``IndexError`` on underflow
(pop/dequeue/peek/front on an empty structure), matching the behavior of
list.pop() on an empty list rather than returning a sentinel value.
"""


class Stack:
    """LIFO (last-in, first-out) stack backed by a Python list."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items!r})"


class Queue:
    """FIFO (first-in, first-out) queue backed by a Python list.

    Enqueue appends to the end (O(1) amortized); dequeue removes from the
    front with ``pop(0)``, which is O(n). That's fine for the visualizer's
    purposes (see ALGORITHMS in algorithms.py) since it gives queue
    operations a distinct, measurable time-complexity curve from the
    stack's O(1) operations. For a production O(1) dequeue, back this with
    collections.deque instead.
    """

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def front(self):
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Queue({self._items!r})"
