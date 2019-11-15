"""
Find the largest element in a stack.

Use a Stack class to implement a new class MaxStack with a method
get_max() that returns the largest element in the stack.
get_max() should not remove the item.

Assume stacks will contain only integers.

Complexity

O(1) time for push(), pop(), and get_max(). O(m) additional space,
where m is the number of operations performed on the stack.

"""


class Stack(object):

    def __init__(self):
        """Initialize an empty stack"""
        self.items = []

    def push(self, item):
        """Push a new item onto the stack"""
        self.items.append(item)

    def pop(self):
        """Remove and return the last item"""
        # If the stack is empty, return None
        # (it would also be reasonable to throw an exception)
        if not self.items:
            return None

        return self.items.pop()

    def peek(self):
        """Return the last item without removing it"""
        if not self.items:
            return None
        return self.items[-1]


class MaxStack(object):

    def __init__(self):
        self.stack = Stack()
        self.max_values_stack = Stack()

    def push(self, item):
        self.stack.push(item)
        if self.max_values_stack.peek() is None \
                or item > self.max_values_stack.peek():
            self.max_values_stack.push(item)

    def pop(self):
        item = self.stack.pop()
        if item == self.max_values_stack.peek():
            self.max_values_stack.pop()

    def get_max(self):
        return self.max_values_stack.peek()
