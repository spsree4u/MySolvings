
# Binary Heap implementation


def max_heapify(heap, index):
    n = len(heap)
    largest = index
    left = 2 * index + 1
    right = 2 * index + 2

    if left < n and heap[left] > heap[largest]:
        largest = left

    if right < n and heap[right] > heap[largest]:
        largest = right

    if largest != index:
        heap[index], heap[largest] = heap[largest], heap[index]
        max_heapify(heap, largest)


def min_heapify(heap, index):
    n = len(heap)
    smallest = index
    left = 2 * index + 1
    right = 2 * index + 2

    if left < n and heap[left] < heap[smallest]:
        smallest = left

    if right < n and heap[right] < heap[smallest]:
        smallest = right

    if smallest != index:
        heap[index], heap[smallest] = heap[smallest], heap[index]
        min_heapify(heap, smallest)


def delete_node(heap, value):
    index = -1
    for i in range(len(heap)):
        if heap[i] == value:
            index = i
            break

    if index < 0:
        return False
    heap[index] = heap[len(heap)-1]
    heap.pop()
    max_heapify(heap, index)


def delete_node_min_heap(heap, value):
    index = -1
    for i in range(len(heap)):
        if heap[i] == value:
            index = i
            break
    if index < 0:
        return False
    heap[index] = heap[len(heap)-1]
    heap.pop()
    min_heapify(heap, index)


def heapify(heap, index):
    parent = (index - 1) // 2
    if parent >= 0 and heap[index] > heap[parent]:
        heap[index], heap[parent] = heap[parent], heap[index]
        heapify(heap, parent)


def insert(heap, value):
    heap.append(value)
    heapify(heap, len(heap) - 1)


def add(heap, value):
    heap.append(value)
    i = len(heap) - 1
    while i > 0 and heap[i] < heap[(i-1)//2]:
        heap[i], heap[(i-1)//2] = heap[(i-1)//2], heap[i]
        i = (i-1)//2


def remove(heap, value):
    """Some issue with this"""
    index = -1
    for i in range(len(heap)):
        if heap[i] == value:
            index = i
            break

    if index < 0:
        return False
    heap[index] = heap[len(heap) - 1]
    heap.pop()

    # heapify
    left = 2 * index + 1
    right = 2 * index + 2
    n = len(heap)
    while (left < n and heap[left] < heap[index]) \
            or (right < n and heap[right] < heap[index]):
        if heap[left] < heap[right]:
            heap[left], heap[index] = heap[index], heap[left]
            index = left
        else:
            heap[right], heap[index] = heap[index], heap[right]
            index = right
        left = 2 * index + 1
        right = 2 * index + 2


def contains_in_minheap(heap, value, index=-1):
    """Some issue with this"""
    n = len(heap)
    index += 1
    left = 2 * index + 1
    right = 2 * index + 2
    if heap[index] == value:
        return True
    elif heap[index] > value:
        index = (index - 1) // 2
    else:
        # if left < n and heap[left] < value:
        if left < n:
            index = left
        if right < n and heap[right] < value:
            index = right
    contains_in_minheap(heap, value, index)


heap1 = [10, 5, 3, 2, 4]
delete_node(heap1, 10)
print(heap1)
heap2 = [1, 3, 9, 12, 13]
delete_node_min_heap(heap2, 1)
print(heap2)
# print(contains_in_minheap(heap2, 12))
# print(contains_in_minheap(heap2, 14))
heap3 = [10, 5, 3, 2, 4]
print(heap3)
insert(heap3, 15)
print(heap3)
heap4 = [3, 7, 12, 9]
print(heap4)
add(heap4, 1)
print(heap4)
