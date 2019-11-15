

# In-order Tree Traversal without recursion and without stack
# O(n) time and O(1) space - Morris traversal
"""
1. Initialize current as root
2. While current is not NULL
   If the current does not have left child
      a) Print current’s data
      b) Go to the right, i.e., current = current->right
   Else
      a) Make current as the right child of the rightmost
         node in current's left subtree
      b) Go to this left child, i.e., current = current->left
"""


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def morris_traversal(root):
    current = root

    while current:
        if not current.left:
            yield current.data
            current = current.right
        else:
            temp = current.left
            while temp.right and temp.right != current:
                temp = temp.right

            if not temp.right:
                temp.right = current
                current = current.left

            else:
                temp.right = None
                yield current.data
                current = current.right


root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)

for i in morris_traversal(root):
    print(i)
