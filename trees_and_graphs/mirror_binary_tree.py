
"""
Find mirror tree of a binary tree
"""


class Node:
    def __init__(self, data):
        self.data = data
        self.left = self.right = None


def mirror(root):
    if not root:
        return

    mirror(root.left)
    mirror(root.right)

    temp = root.left
    root.left = root.right
    root.right = temp


def in_order(root):
    if not root:
        return

    in_order(root.left)
    print(root.data)
    in_order(root.right)


root1 = Node(1)
root1.left = Node(2)
root1.right = Node(3)
root1.left.left = Node(4)
root1.left.right = Node(5)

""" Print inorder traversal of 
    the input tree """
print("Inorder traversal of the",
      "constructed tree is")
in_order(root1)

""" Convert tree to its mirror """
mirror(root1)

""" Print inorder traversal of  
    the mirror tree """
print("\nInorder traversal of",
      "the mirror treeis ")
in_order(root1)
