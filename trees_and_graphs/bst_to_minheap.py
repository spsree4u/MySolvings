
"""
Convert a BST to a min-heap with condition that all the values in the
left subtree of a node should be less than all the values in the
right subtree of the node
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.left = self.right = None


def in_order(root, arr):
    if root:
        in_order(root.left, arr)
        arr.append(root.value)
        in_order(root.right, arr)


def pre_order(root, arr, i):
    if root:
        i[0] += 1
        root.value = arr[i[0]]
        pre_order(root.left, arr, i)
        pre_order(root.right, arr, i)


def print_tree(root):
    if root:
        print(root.value)
        print_tree(root.left)
        print_tree(root.right)


def convert(root):
    arr = []
    i = [-1]
    in_order(root, arr)
    pre_order(root, arr, i)


root = Node(4)
root.left = Node(2)
root.right = Node(6)
root.left.left = Node(1)
root.left.right = Node(3)
root.right.left = Node(5)
root.right.right = Node(7)

print("Pre order traversal on tree before conversion:")
print_tree(root)
convert(root)
print("Pre order traversal on tree after conversion:")
print_tree(root)
