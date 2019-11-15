

"""
Write a function for doing an in-place shuffle of a list.

The shuffle must be "uniform," meaning each item in the original list must
have the same probability of ending up in each spot in the final list.

Assume that you have a function get_random(floor, ceiling) for getting a
random integer that is >= floor and <= ceiling.

Complexity
O(n) time and O(1) space.

"""

import random


def get_random(floor, ceiling):
    return random.randrange(floor, ceiling + 1)


# Common method
def naive_shuffle(the_list):
    # For each index in the list
    for first_index in range(0, len(the_list) - 1):
        # Grab a random other index
        second_index = get_random(0, len(the_list) - 1)
        # And swap the values
        if second_index != first_index:
            the_list[first_index], the_list[second_index] = \
                the_list[second_index], the_list[first_index]


def shuffle(the_list):
    # If it's 1 or 0 items, just return
    if len(the_list) <= 1:
        return the_list

    last_index_in_the_list = len(the_list) - 1

    # Walk through from beginning to end
    for index_we_are_choosing_for in range(0, len(the_list) - 1):

        # Choose a random not-yet-placed item to place there
        # (could also be the item currently in that spot)
        # Must be an item AFTER the current item, because the stuff
        # before has all already been placed
        random_choice_index = get_random(index_we_are_choosing_for,
                                         last_index_in_the_list)

        # Place our random choice in the spot by swapping
        if random_choice_index != index_we_are_choosing_for:
            the_list[index_we_are_choosing_for], the_list[random_choice_index] = \
                the_list[random_choice_index], the_list[index_we_are_choosing_for]


sample_list_1 = [11, 44, 99, 33, 55, 22, 66, 88, 00, 77]
print(sample_list_1)
naive_shuffle(sample_list_1)
print(sample_list_1)
sample_list_2 = [11, 44, 99, 33, 55, 22, 66, 88, 00, 77]
print(sample_list_2)
shuffle(sample_list_2)
print(sample_list_2)
