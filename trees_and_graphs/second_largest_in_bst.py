"""
Write a function to find the 2nd largest element in a binary search tree.


Complexity:
We're doing one walk down our BST, which means O(h) time, where h is the
height of the tree (again, that's O(lg⁡ n) if the tree is balanced, O(n)
otherwise). O(1) space.

"""

# from binarytree import bst


class BinaryTreeNode(object):

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def insert_left(self, value):
        self.left = BinaryTreeNode(value)
        return self.left

    def insert_right(self, value):
        self.right = BinaryTreeNode(value)
        return self.right


def find_largest_recursive(root_node):
    if root_node is None:
        raise ValueError("Empty tree")
    if root_node.right is not None:
        return find_largest_recursive(root_node.right)
    return root_node.value


def find_second_largest_recursive(root_node):
    if (root_node is None or
            (root_node.right is None and root_node.left is None)):
        raise ValueError("Empty tree")

    if root_node.left and not root_node.right:
        return find_largest_recursive(root_node.left)

    if root_node.right and not root_node.right.left and \
            not root_node.right.right:
        return root_node.value

    return find_second_largest_recursive(root_node.right)


def find_largest(root_node):
    current = root_node

    while current:
        if not current.right:
            return current.value
        current = current.right


def find_second_largest(root_node):
    if (root_node is None or
            (root_node.right is None and root_node.left is None)):
        raise ValueError("Empty tree")

    current = root_node
    while current:
        if current.left and not current.right:
            return find_largest(current.left)

        if current.right and not current.right.left \
                and not current.right.right:
            return current.value

        current = current.right


bt = BinaryTreeNode(5)
bt.left = BinaryTreeNode(3)
bt.right = BinaryTreeNode(8)
bt.left = BinaryTreeNode(3)
bt.left.left = BinaryTreeNode(1)
bt.left.right = BinaryTreeNode(4)
bt.right.left = BinaryTreeNode(7)
bt.right.right = BinaryTreeNode(12)
bt.right.right.left = BinaryTreeNode(10)
bt.right.right.left.left = BinaryTreeNode(9)
bt.right.right.left.right = BinaryTreeNode(11)
print(find_largest(bt))
print(find_second_largest(bt))
print(find_largest_recursive(bt))  # something wrong with this function
print(find_second_largest_recursive(bt))  # something wrong with this function


# mt = bst()
# print(mt)
# print(find_largest(mt))
# print(find_second_largest(mt))
# print(find_largest_recursive(mt))  # something wrong with this function
# print(find_second_largest_recursive(mt))  # something wrong with this function
# print(mt.properties)
