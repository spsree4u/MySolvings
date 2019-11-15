
"""
Find nodes at k distance from a given node. root node is also given.
As tree traversal upwards not possible, to keep track of the parents
of each node, use a hash.
Reference: https://www.youtube.com/watch?v=nPtARJ2cYrg
"""

import datetime


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def create_node_parent_map(root, parent, node_parent_map):
    if not root:
        return
    node_parent_map[root] = parent

    create_node_parent_map(root.left, root, node_parent_map)
    create_node_parent_map(root.right, root, node_parent_map)

    return node_parent_map


def find_nodes_at_k_distance(root, start, k):
    level = 0
    visited = [start]
    queue = [start]

    if root is None:
        print("Empty tree!!")
        return

    node_parent_map = create_node_parent_map(root, None, {})
    while queue:
        if level == k:
            print([i.data for i in queue])
            return 1

        layer_size = len(queue)
        for i in range(layer_size):
            node = queue.pop(0)
            if node.left and node.left not in visited:
                visited.append(node.left)
                queue.append(node.left)

            if node.right and node.right not in visited:
                visited.append(node.right)
                queue.append(node.right)

            parent_node = node_parent_map[node]
            if parent_node and parent_node not in visited:
                visited.append(parent_node)
                queue.append(parent_node)

        level += 1


root1 = Node(20)
root1.left = Node(8)
root1.right = Node(22)
root1.left.left = Node(4)
root1.left.right = Node(12)
root1.left.right.left = Node(10)
root1.left.right.right = Node(14)
target1 = root1.left.right
start1 = datetime.datetime.now()
find_nodes_at_k_distance(root1, target1, 2)
end1 = datetime.datetime.now()
print(end1-start1)


# Recursive approach #########################################################
def find_nodes_at_k_distance_down(root, k):
    # Base Case
    if root is None or k < 0:
        return

    # If we reach a k distant node, print it
    if k == 0:
        print(root.data)
        return

    # Recur for left and right subtree
    find_nodes_at_k_distance_down(root.left, k - 1)
    find_nodes_at_k_distance_down(root.right, k - 1)


# Prints all nodes at distance k from a given target node
# The k distant nodes may be upward or downward. This function
# returns distance of root from target node, it returns -1
# if target node is not present in tree rooted with root
def find_nodes_at_k_distance_recursive(root, target, k):
    # Base Case 1 : IF tree is empty return -1
    if root is None:
        return -1

    # If target is same as root. Use the downward function
    # to print all nodes at distance k in subtree rooted with
    # target or root
    if root == target:
        find_nodes_at_k_distance_down(root, k)
        return 0

    # Recur for left subtree
    dl = find_nodes_at_k_distance_recursive(root.left, target, k)

    # Check if target node was found in left subtree
    if dl != -1:

        # If root is at distance k from target, print root
        # Note: dl is distance of root's left child
        # from target
        if dl + 1 == k:
            print(root.data)

        # Else go to right subtree and print all k-dl-2
        # distant nodes
        # Note: that the right child is 2 edges away from
        # left child
        else:
            find_nodes_at_k_distance_down(root.right, k - dl - 2)

        # Add 1 to the distance and return value for
        # for parent calls
        return 1 + dl

    # MIRROR OF ABOVE CODE FOR RIGHT SUBTREE
    # Note that we reach here only when node was not found
    # in left subtree
    dr = find_nodes_at_k_distance_recursive(root.right, target, k)
    if dr != -1:
        if dr + 1 == k:
            print(root.data)
        else:
            find_nodes_at_k_distance_down(root.left, k - dr - 2)
        return 1 + dr

    # If target was neither present in left nor in right subtree
    return -1


root2 = Node(20)
root2.left = Node(8)
root2.right = Node(22)
root2.left.left = Node(4)
root2.left.right = Node(12)
root2.left.right.left = Node(10)
root2.left.right.right = Node(14)
target2 = root2.left.right
start2 = datetime.datetime.now()
find_nodes_at_k_distance_recursive(root2, target2, 2)
end2 = datetime.datetime.now()
print(end2-start2)
target3 = root2.left
find_nodes_at_k_distance_recursive(root2, target3, 2)
root3 = Node(30)
root3.left = root2
find_nodes_at_k_distance_recursive(root3, target3, 2)
