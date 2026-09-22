

"""Run with:
    python -m unittest test_data_structures.py -v
"""
import unittest

from data_structures import Stack, Queue


class TestStack(unittest.TestCase):
    def test_new_stack_is_empty(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        self.assertEqual(len(s), 0)

    def test_push_increases_length(self):
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(len(s), 2)
        self.assertFalse(s.is_empty())

    def test_pop_returns_last_pushed_item(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.pop(), 1)

    def test_pop_decreases_length(self):
        s = Stack()
        s.push("a")
        s.push("b")
        s.pop()
        self.assertEqual(len(s), 1)

    def test_pop_empty_raises_index_error(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.pop()

    def test_peek_returns_top_without_removing(self):
        s = Stack()
        s.push(10)
        s.push(20)
        self.assertEqual(s.peek(), 20)
        self.assertEqual(len(s), 2)  # peek must not remove

    def test_peek_empty_raises_index_error(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.peek()

    def test_lifo_order_with_mixed_operations(self):
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(s.pop(), 2)
        s.push(3)
        s.push(4)
        self.assertEqual(s.pop(), 4)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.pop(), 1)
        self.assertTrue(s.is_empty())

    def test_repr_contains_class_name(self):
        s = Stack()
        s.push(1)
        self.assertIn("Stack", repr(s))

    def test_handles_none_and_falsy_values(self):
        s = Stack()
        s.push(None)
        s.push(0)
        s.push(False)
        self.assertEqual(s.pop(), False)
        self.assertEqual(s.pop(), 0)
        self.assertIsNone(s.pop())


class TestQueue(unittest.TestCase):
    def test_new_queue_is_empty(self):
        q = Queue()
        self.assertTrue(q.is_empty())
        self.assertEqual(len(q), 0)

    def test_enqueue_increases_length(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(len(q), 2)
        self.assertFalse(q.is_empty())

    def test_dequeue_returns_first_enqueued_item(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)

    def test_dequeue_decreases_length(self):
        q = Queue()
        q.enqueue("a")
        q.enqueue("b")
        q.dequeue()
        self.assertEqual(len(q), 1)

    def test_dequeue_empty_raises_index_error(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.dequeue()

    def test_front_returns_first_without_removing(self):
        q = Queue()
        q.enqueue(10)
        q.enqueue(20)
        self.assertEqual(q.front(), 10)
        self.assertEqual(len(q), 2)  # front must not remove

    def test_front_empty_raises_index_error(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.front()

    def test_fifo_order_with_mixed_operations(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(q.dequeue(), 1)
        q.enqueue(3)
        q.enqueue(4)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)
        self.assertEqual(q.dequeue(), 4)
        self.assertTrue(q.is_empty())

    def test_repr_contains_class_name(self):
        q = Queue()
        q.enqueue(1)
        self.assertIn("Queue", repr(q))

    def test_handles_none_and_falsy_values(self):
        q = Queue()
        q.enqueue(None)
        q.enqueue(0)
        q.enqueue(False)
        self.assertIsNone(q.dequeue())
        self.assertEqual(q.dequeue(), 0)
        self.assertEqual(q.dequeue(), False)


if __name__ == "__main__":
    unittest.main()
