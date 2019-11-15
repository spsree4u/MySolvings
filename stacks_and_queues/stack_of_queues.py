
# Stack using 2 Queues


from queue import Queue


class Stack(object):

    def __init__(self):
        self.q1 = Queue()
        self.q2 = Queue()
        self.current_size = 0

    def push(self, item):
        self.q1.put(item)
        self.current_size += 1

    def pop(self):
        if not self.q1:
            return

        while self.q1.qsize() != 1:
            self.q2.put(self.q1.queue[0])
            self.q1.get()

        temp = self.q1.get()
        self.current_size -= 1

        # swap queues
        temp_queue = self.q1
        self.q1 = self.q2
        self.q2 = temp_queue

        return temp

    def top(self):
        if not self.q1:
            return

        while self.q1.qsize() != 1:
            self.q2.put(self.q1.queue[0])
            self.q1.get()

        temp = self.q1.get()
        self.q2.put(temp)

        # swap queues
        temp_queue = self.q1
        self.q1 = self.q2
        self.q2 = temp_queue

        return temp

    def size(self):
        return self.current_size


s = Stack()
s.push(1)
s.push(2)
s.push(3)

print("current size: ", s.size())
print(s.top())
print(s.pop())
print(s.top())
print(s.pop())
print(s.top())

print("current size: ", s.size())
