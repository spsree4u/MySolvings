

# To get post order traversal of a binary tree from given
# pre and in-order traversals

# Recursive function which traverse through pre-order values based
# on the in-order index values for root, left and right sub-trees
# Explanation in https://www.youtube.com/watch?v=wGmJatvjANY&t=301s
def print_post_order(start, end, p_order, p_index, i_index_map):
    # base case
    if start > end:
        return p_index

    # get value for current p_index for updating p_index value
    val = p_order[p_index]
    p_index += 1

    # Print value if retrieved value is of a leaf as there is no more child
    if start == end:
        print(val)
        return p_index

    # If not leaf node, get root node index from in-order map
    # corresponding to value to call recursively for sub-trees
    i = i_index_map[val]

    p_index = print_post_order(start, i-1, p_order, p_index, i_index_map)
    p_index = print_post_order(i+1, end, p_order, p_index, i_index_map)

    # Print value of root node as subtrees are traversed
    print(val)

    return p_index


def get_post_order(in_order, pre_order):
    in_order_index_map = {}
    tree_size = len(in_order)

    # dictionary to store the indices of in-order travel sequence
    # O(n) time and O(n) space is required for the hash map
    for n in range(tree_size):
        in_order_index_map[in_order[n]] = n

    pre_index = 0

    print_post_order(0, tree_size-1, pre_order, pre_index, in_order_index_map)


get_post_order([4, 2, 1, 7, 5, 8, 3, 6], [1, 2, 4, 3, 5, 7, 8, 6])
