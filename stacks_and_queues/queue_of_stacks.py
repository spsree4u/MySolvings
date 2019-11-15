"""
Implement a queue with 2 stacks. Your queue should have an enqueue and
a dequeue method and it should be "first in first out" (FIFO).

Optimize for the time cost of m calls on your queue.
These can be any mix of enqueue and dequeue calls.

Assume you already have a stack with O(1) time push and pop.


For enqueue, we simply push the enqueued item onto in_stack.

For dequeue on an empty out_stack, the oldest item is at the bottom of
in_stack. So we dig to the bottom of in_stack by pushing each item one-by-one
onto out_stack until we reach the bottom item, which we return.

After moving everything from in_stack to out_stack, the item that was
enqueued the 2nd longest ago (after the item we just returned) is at
the top of out_stack, the item enqueued 3rd longest ago is just below
it, etc. So to dequeue on a non-empty out_stack, we simply return the
top item from out_stack.

Each enqueue is clearly O(1) time, and so is each dequeue
when out_stack has items. Dequeue on an empty out_stack is order of the
number of items in in_stack at that moment, which can vary significantly.

"""


class Stack(object):

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop()


class Queue(object):

    def __init__(self):
        self.stack1 = Stack()
        self.stack2 = Stack()

    def enqueue(self, item):
        self.stack1.push(item)

    def dequeue(self):
        if len(self.stack2.items) == 0:
            while len(self.stack1.items) > 0:
                self.stack2.push(self.stack1.pop())
            if len(self.stack2.items) == 0:
                raise IndexError("Can't dequeue from empty queue")

        return self.stack2.pop()


q = Queue()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)

print(q.dequeue())
print(q.dequeue())
print(q.dequeue())
