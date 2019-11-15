

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def is_palindrome(head):
    head1 = head
    temp_stack = []
    while head1 is not None:
        temp_stack.append(head1)
        head1 = head1.next

    while head is not None:
        item_data = temp_stack.pop().data
        if head.data != item_data:
            print("Not palindrome")
            return
        head = head.next
    print("Palindrome")


one = Node(1)
two = Node(2)
three = Node(3)
four = Node(2)
five = Node(1)
one.next = two
two.next = three
three.next = four
four.next = five
is_palindrome(one)


def is_palindrome2(head):
    """
    useful only to check number palindrome
    """
    p = head
    t1 = 0
    t2 = 0
    n = 1
    while p is not None:
        t1 = t1 + (p.data * n)
        t2 = (t2 * 10) + p.data
        p = p.next
        n = n * 10

    if t1 == t2:
        print("Palindrome")
        return 1
    print("Not palindrome")


one2 = Node(1)
two2 = Node(2)
three2 = Node(3)
four2 = Node(2)
five2 = Node(1)
one2.next = two2
two2.next = three2
three2.next = four2
four2.next = five2
is_palindrome2(one2)
