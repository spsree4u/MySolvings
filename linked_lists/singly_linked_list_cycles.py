"""
You have a singly-linked list and check if it contains a cycle.

Complexity

O(n) time and O(1) space.

"""

import profile
import timeit


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


def is_cycled_v2(first_node):
    if not first_node:
        return "Node provided is null"

    runner = first_node.next
    while runner and runner is not first_node:
        runner = runner.next

    return runner == first_node


r = Node(1)
a = Node(2)
b = Node(3)
c = Node(4)
d = Node(5)
e = Node(6)
r.next = a
a.next = b
b.next = c
c.next = d
d.next = e
e.next = r
print(is_cycled(r))
print(is_cycled_v2(r))
print('\n\n')
profile.run('is_cycled(r)')
print('\n\n')
profile.run('is_cycled_v2(r)')

print('\n\n')
test_code1 = '''
def test():
    return is_cycled(r)
'''
test_code2 = '''
def test():
    return is_cycled_v2(r)
'''
print(timeit.repeat(stmt=test_code1, repeat=5))
print(timeit.repeat(stmt=test_code2, repeat=5))
