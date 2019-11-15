
"""

Write a function to check that a binary tree is a valid binary search tree.

O(n) time and O(n) space.

"""


class Node:
    def __init__(self, data):
        self.value = data
        self.left = self.right = None

    def insert_left(self, data):
        self.left = Node(data)
        return self.left

    def insert_right(self, data):
        self.right = Node(data)
        return self.right


def is_binary_search_tree(root):
    node_bound_stack = [(root, -float('inf'), float('inf'))]
    while node_bound_stack:
        node, low, high = node_bound_stack.pop()

        if node.value <= low or node.value >= high:
            return False

        if node.left:
            node_bound_stack.append((node.left, low, node.value))

        if node.right:
            node_bound_stack.append((node.right, node.value, high))

    return True


def is_binary_search_tree_recur(root, low=-float('inf'), high=float('inf')):

    if not root:
        return True
    if root.value <= low or root.value >= high:
        return False

    return (is_binary_search_tree_recur(root.left, low, root.value)) and \
           (is_binary_search_tree_recur(root.right, root.value, high))


def insert(root, value):

    if not root:
        root = Node(value)
        return root
    else:
        if root.value > value:
            if not root.left:
                root.left = Node(value)
            else:
                insert(root.left, value)
        else:
            if not root.right:
                root.right = Node(value)
            else:
                insert(root.right, value)


# def insert(root, value):
#
#     if not root:
#         return Node(value)
#     elif root.value > value:
#         root.left = insert(root.left, value)
#     else:
#         root.right = insert(root.right, value)


def inorder(root):
    if root:
        inorder(root.left)
        print(root.value)
        inorder(root.right)


root1 = Node(50)
a = root1.insert_left(30)
b = root1.insert_right(80)
c = a.insert_left(20)
d = a.insert_right(60)
# d = a.insert_right(40)
e = b.insert_left(70)
f = b.insert_right(90)
print(is_binary_search_tree(root1))
print(is_binary_search_tree_recur(root1))

r = Node(50)
insert(r, 30)
insert(r, 20)
insert(r, 40)
insert(r, 70)
insert(r, 60)
insert(r, 80)
inorder(r)
