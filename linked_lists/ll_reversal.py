
# Linked List Reversal


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def reverse_ll(head):
    prev = None
    current = head
    while current:
        next = current.next
        current.next = prev
        prev = current
        current = next
    head = prev
    return head


def reverse_ll_recur(head, prev=None):
    next = head.next
    head.next = prev
    if not next:
        return head
    return reverse_ll_recur(next, head)


def print_ll(head):
    while head:
        print(head.data)
        head = head.next


ll = Node(1)
ll.next = Node(2)
ll.next.next = Node(3)
ll.next.next.next = Node(4)
print_ll(ll)
ll_r = reverse_ll(ll)
print_ll(ll_r)
ll_r_r = reverse_ll_recur(ll_r)
print_ll(ll_r_r)
