
# Queue implementation using Linked List


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue(object):

    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, item):
        temp = Node(item)
        if self.rear is None:
            self.front = temp
            self.rear = temp
            return
        self.rear.next = temp
        # update rear with newly added
        self.rear = temp

    def dequeue(self):
        if self.front is None:
            return
        temp = self.front
        self.front = temp.next

        if self.front is None:
            self.rear = None

        return str(temp.data)


# Test Queue
q = Queue()
q.enqueue(10)
q.enqueue(20)
q.dequeue()
q.dequeue()
q.enqueue(30)
q.enqueue(40)
q.enqueue(50)
print("Dequeued item is " + q.dequeue())
