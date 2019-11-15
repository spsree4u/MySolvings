

"""
We have two lists sorted numerically already, in lists. Write a
function to merge our lists into one sorted list.

For example:

list1 = [3, 4, 6, 10, 11, 15]
list2 = [1, 5, 8, 12, 14, 19]

# Prints [1, 3, 4, 5, 6, 8, 10, 11, 12, 14, 15, 19]
print(merge_lists(list1, list2))

Complexity

O(n) time and O(n) additional space, where n is the number of items in
the merged list.

"""


def merge_lists(list1, list2):
    """
    Edge case to be corrected
    """
    merged_list_length = len(list1) + len(list2)
    merged_list = [None] * merged_list_length

    current_index_list1 = 0
    current_index_list2 = 0
    current_index_merged_list = 0

    while current_index_merged_list < merged_list_length:

        head_list1 = list1[current_index_list1]
        head_list2 = list2[current_index_list2]

        if head_list1 < head_list2:
            merged_list[current_index_merged_list] = head_list1
            current_index_list1 += 1
        else:
            merged_list[current_index_merged_list] = head_list2
            current_index_list2 += 1

        current_index_merged_list += 1
    #     if current_index_list1 == len(list1):
    #         break
    #     if current_index_list2 == len(list2)-1:
    #         break
    #
    # if current_index_list1 == len(list1):
    #     for i in range(current_index_list2, len(list2)):
    #         merged_list[current_index_merged_list] = list2[i]
    #         current_index_merged_list += 1
    # elif current_index_list2 == len(list2):
    #     for i in range(current_index_list1, len(list1)):
    #         merged_list[current_index_merged_list] = list1[i]
    #         current_index_merged_list += 1

    return merged_list


list1 = [3, 4, 6, 10, 11, 15]
list2 = [1, 5, 8, 12, 14, 19]
print(merge_lists(list1, list2))
