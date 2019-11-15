
"""
You have a linked list and want to find the k-th to last node.

Write a function kth_to_last_node() that takes an integer k and the head_node 
of a singly-linked list, and returns the k-th to last node in the list.

Complexity

Both approaches use O(n) time and O(1) space.

"""


class LinkedListNode:

    def __init__(self, value):
        self.value = value
        self.next = None


def kth_to_last_node(k, start_node):

    if k < 1:
        raise ValueError(
            'Impossible to find less than first to last node: %s' % k
        )

    length = 1
    current_node = start_node
    while current_node.next:
        length += 1
        current_node = current_node.next

    if k > length:
        raise ValueError(
            'k is larger than the length of the linked list: %s' % k
        )

    current_node = start_node
    for i in range(0, length-k):
        current_node = current_node.next

    print(current_node.value)


def kth_to_last_node_2(k, start_node):

    if k < 1:
        raise ValueError(
            'Impossible to find less than first to last node: %s' % k
        )

    left_node = start_node
    right_node = start_node

    for _ in range(k-1):
        if not right_node.next:
            raise ValueError(
                'k is larger than the length of the linked list: %s' % k
            )
        right_node = right_node.next

    while right_node.next:
        left_node = left_node.next
        right_node = right_node.next

    print(left_node.value)


a = LinkedListNode("Angel Food")
b = LinkedListNode("Bundt")
c = LinkedListNode("Cheese")
d = LinkedListNode("Devil's Food")
e = LinkedListNode("Eccles")

a.next = b
b.next = c
c.next = d
d.next = e

kth_to_last_node(2, a)
kth_to_last_node_2(4, a)
