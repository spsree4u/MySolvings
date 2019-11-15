

def bubble(lst):
    """
    compare adjacent and swap. This is optimized bubble sort. swap variable is
    used to stop iteration when the whole list is sorted as conventional
    bubble sort will keep continue loop until last.
    Time: O(n^2)
    Space: O(1)
    """
    # We set swapped to True so the loop looks runs at least once
    swap = True
    while swap:
        swap = False
        for i in range(len(lst)-1):
            if lst[i] > lst[i+1]:
                # Swap the elements
                lst[i+1], lst[i] = lst[i], lst[i+1]
                # Set the flag to True so we'll loop again
                swap = True


arr1 = [29, 72, 98, 13, 87, 66, 52, 51, 36, -21]
bubble(arr1)
print(arr1)


def selection(lst):
    """
    find lesser value for each index from remaining array and swap.
    Time: O(n^2)
    Space: O(1)
    """
    # This value of i corresponds to how many values were sorted
    for i in range(len(lst)):
        # We assume that the first item of the unsorted segment is the smallest
        minimum = i
        # This loop iterates over the unsorted items
        for j in range(i+1, len(lst)):
            if lst[j] < lst[minimum]:
                minimum = j

        # Swap values of the lowest unsorted element with the first unsorted
        # element
        lst[minimum], lst[i] = lst[i], lst[minimum]


arr2 = [29, 72, 98, 13, 87, 66, 52, 51, 36, -21]
selection(arr2)
print(arr2)


def insertion(lst):
    """
    Think about card game. start from second card and insert to right
    position on left.
    Time: O(n^2)
    Space: O(1)
    """
    # Assume first element is already sorted
    for i in range(1, len(lst)):
        insert_item = lst[i]
        j = i - 1

        while j >= 0 and lst[j] > insert_item:
            lst[j+1] = lst[j]
            j -= 1

        lst[j+1] = insert_item


arr3 = [29, 72, 98, 13, 87, 66, 52, 51, 36, -21]
insertion(arr3)
print(arr3)


def max_heap(lst, length, root_index):
    # Assume the index of the largest element is the root index
    large = root_index
    left = (root_index * 2) + 1
    right = (root_index * 2) + 2

    # If the left child of the root is a valid index, and the element is
    # greater than the current largest element, then update the largest element
    if left < length and lst[left] > lst[large]:
        large = left

    # Do the same for the right child of the root
    if right < length and lst[right] > lst[large]:
        large = right

    # If the largest element is no longer the root element, swap them
    if large != root_index:
        lst[root_index], lst[large] = lst[large], lst[root_index]
        # Heapify (max_heap) the new root element to ensure it's the largest
        max_heap(lst, length, large)


def heap_sort(lst):
    """
    create max heap and swap max with last element in unsorted array.
    Time: O(n * log(n))
    Space: O(1)
    """
    length = len(lst)

    # Create a Max Heap from the list
    # The 2nd argument of range means we stop at the element before -1 i.e.
    # the first element of the list.
    # The 3rd argument of range means we iterate backwards, reducing the count
    # of i by 1
    for i in range(length, -1, -1):
        max_heap(lst, length, i)

    # Move the root of the max heap to the end of
    for i in range(length-1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        max_heap(lst, i, 0)


arr4 = [29, 72, 98, 13, 87, 66, 52, 51, 36, -21]
heap_sort(arr4)
print(arr4)


def merge(left_lst, right_lst):
    sorted_list = []
    left_lst_index = right_lst_index = 0
    # We use the list lengths often, so its handy to make variables
    left_lst_length, right_lst_length = len(left_lst), len(right_lst)

    for _ in range(left_lst_length + right_lst_length):
        if left_lst_index < left_lst_length \
                and right_lst_index < right_lst_length:
            # We check which value from the start of each list is smaller
            # If the item at the beginning of the left list is smaller, add it
            # to the sorted list
            if left_lst[left_lst_index] <= right_lst[right_lst_index]:
                sorted_list.append(left_lst[left_lst_index])
                left_lst_index += 1
            # If the item at the beginning of the right list is smaller, add it
            # to the sorted list
            else:
                sorted_list.append(right_lst[right_lst_index])
                right_lst_index += 1

        # If we've reached the end of the of the left list, add the elements
        # from the right list
        elif left_lst_index == left_lst_length:
            sorted_list.append(right_lst[right_lst_index])
            right_lst_index += 1

        # If we've reached the end of the of the right list, add the elements
        # from the left list
        elif right_lst_index == right_lst_length:
            sorted_list.append(left_lst[left_lst_index])
            left_lst_index += 1


def merge_sort(lst):
    """
    Divide and merge back with sorting to a new list.
    Time: O(n * log(n))
    Space: O(n)
    """
    # If the list is a single element, return it
    if len(lst) <= 1:
        return lst

    # Use floor division to get midpoint, indices must be integers
    mid = len(lst)//2

    # Sort and merge each half
    left_lst = merge_sort(lst[:mid])
    right_lst = merge_sort(lst[mid:])

    # Merge the sorted lists into a new one
    return merge(left_lst, right_lst)


arr5 = [29, 72, 98, 13, 87, 66, 52, 51, 36, -21]
heap_sort(arr5)
print(arr5)


def partition(lst, low, high):
    # We select the middle element to be the pivot. Some implementations select
    # the first element or the last element. Sometimes the median value becomes
    # the pivot, or a random one. There are many more strategies that can be
    # chosen or created.
    pivot = (low + high) // 2
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while lst[i] < pivot:
            i += 1
        j -= 1
        while lst[j] > pivot:
            j -= 1

        if i >= j:
            return j

        # If an element at i (on the left of the pivot) is larger than the
        # element at j (on right right of the pivot), then swap them
        lst[i], lst[j] = lst[j], lst[i]


def _quick(items, low, high):
    if low < high:
        # This is the index after the pivot, where our lists are split
        split = partition(items, low, high)
        _quick(items, low, split)
        _quick(items, split+1, high)


def quick(lst):
    """

    Time: O(n^2) Avg: O(n * log(n))
    Space: O(log(n))
    """
    _quick(lst, 0, len(lst)-1)


arr6 = [29, 72, 98, 13, 87, 66, 52, 51, 36, -21]
heap_sort(arr6)
print(arr6)
