"""

Write a function to see if a binary tree is "super-balanced".

A tree is "super-balanced" if the difference between the depths of any two
leaf nodes is no greater than one.

Complexity

O(n) time and O(n) space.

"""


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def add_left(self, value):
        self.left(Node(value))
        return self.left

    def add_right(self, value):
        self.right(Node(value))
        return self.right


def is_super_balanced(root):

    if not root:
        return True

    depths = list()
    visited = list()
    visited.append((root, 0))

    while len(visited):
        node, depth = visited.pop()

        # If leaf
        if (not node.left) and (not node.right):
            # If already visited depth
            if depth not in depths:
                depths.append(depth)

            # Two ways we might now have an unbalanced tree:
            #   1) more than 2 different leaf depths
            #   2) 2 leaf depths that are more than 1 apart
            if (len(depths) > 2) or \
                    (len(depths) == 2 and abs(depths[0]-depths[1]) > 2):
                return False

        else:
            if node.left:
                visited.append((node.left, depth+1))

            if node.right:
                visited.append((node.right, depth+1))

    return True


def is_balanced(root):
    # Time O(n), Space O(1)
    if not root:
        return 0

    return 1 + abs(is_balanced(root.left) - is_balanced(root.right))


# Balanced tree
root1 = Node(1)
root1.left = Node(2)
root1.right = Node(3)
root1.left.left = Node(4)
root1.left.right = Node(5)
root1.right.left = Node(6)
# root1.right.right = Node(8)
root1.left.left.left = Node(7)
print("SuperBalanced") if is_super_balanced(root1) else print("Unbalanced")
print("Balanced") if is_balanced(root1) == 1 else print("Unbalanced")

# Unbalanced tree
root2 = Node(1)
root2.left = Node(2)
root2.right = Node(3)
root2.left.left = Node(4)
root2.left.right = Node(5)
root2.left.left.left = Node(8)
print("SuperBalanced") if is_super_balanced(root2) else print("Unbalanced")
print("Balanced") if is_balanced(root2) == 1 else print("Unbalanced")
