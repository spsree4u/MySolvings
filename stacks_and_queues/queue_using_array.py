

class Queue:
    def __init__(self, s):
        self.rear = 0
        self.front = 0
        self.queue = []
        self.max_size = s
        # self.imposter_rear = 0
        self.imposter_front = 0

    # O(1) time
    def enqueue(self, data):
        if self.rear == self.max_size:
            print('Queue is full')
            return
        self.queue.append(data)
        self.rear += 1

    # O(n) time
    def dequeue(self):
        if self.front == self.rear:
            print('Queue is empty')
            return
        self.queue.pop(0)
        self.rear -= 1

    # O(1) time
    def imposter_dequeue(self):
        if self.imposter_front == self.rear:
            print('Queue is empty')
            return
        print('Appeared dequeued element: {}'.format(
            self.queue[self.imposter_front]))
        self.imposter_front += 1

    # O(1) time
    def get_front(self):
        if self.front == self.rear:
            print('Queue is empty')
            return
        print(self.queue[self.front])

    # O(1) time
    def get_rear(self):
        if self.front == self.rear:
            print('Queue is empty')
            return
        print(self.queue[self.rear-1])

    def print_queue(self):
        print(self.queue)


q = Queue(4)

# Print queue elements
q.print_queue()

# Inserting elements in the queue
q.enqueue(20)
q.enqueue(30)
q.enqueue(40)
q.enqueue(50)

# Print queue elements
q.print_queue()

# Insert element in queue
q.enqueue(60)

# Print queue elements
q.print_queue()

q.dequeue()
q.dequeue()

# Print queue elements
q.print_queue()

# Print front and rear of queue
q.get_front()
q.get_rear()

q.dequeue()
q.dequeue()

# Print queue elements
q.print_queue()

# Accessing from empty queue
q.dequeue()
q.get_front()
q.get_rear()

# Testing imposter deque
q.enqueue(60)
q.enqueue(70)
q.print_queue()
q.imposter_dequeue()
q.imposter_dequeue()
q.print_queue()
