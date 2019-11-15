"""
You have a singly-linked list and check if it contains a cycle.

Complexity

O(n) time and O(1) space.

"""


class Node(object):

    def __init__(self, value):
        self.next = None
        self.value = value


def is_cycled(first_node):
    slow_runner = first_node
    fast_runner = first_node

    while fast_runner is not None and fast_runner.next is not None:
        slow_runner = slow_runner.next
        fast_runner = fast_runner.next.next

        if fast_runner is slow_runner:
            return True

    return False
