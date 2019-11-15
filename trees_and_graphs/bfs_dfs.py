
# BFS and DFS in a Binary Tree


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


# BFS: O(n)
def level_order_traversal(root):

    if root is None:
        print("Empty tree!!")
        return

    queue = [root]

    while queue:
        print(queue[0].data)
        node = queue.pop(0)

        if node.left:
            queue.append(node.left)

        if node.right:
            queue.append(node.right)


root1 = Node(1)
root1.left = Node(2)
root1.right = Node(3)
root1.left.left = Node(4)
root1.left.right = Node(5)

print("Level Order Traversal of binary tree is -")
level_order_traversal(root1)


# DFS: O(n)


# DFS In-order
def in_order_traversal(root):
    """
    In case of binary search trees (BST), Inorder traversal gives nodes
    in non-decreasing order. To get nodes of BST in non-increasing order,
    a variation of Inorder traversal where Inorder traversal s reversed
    can be used.
    """
    if root:
        in_order_traversal(root.left)
        print(root.data)
        in_order_traversal(root.right)


# DFS Pre-order
def pre_order_traversal(root):
    """
    Preorder traversal is used to create a copy of the tree.
    Preorder traversal is also used to get prefix expression on of an
    expression tree. Please see http://en.wikipedia.org/wiki/Polish_notation
    to know why prefix expressions are useful.
    """
    if root:
        print(root.data)
        pre_order_traversal(root.left)
        pre_order_traversal(root.right)


# DFS Post-order
def post_order_traversal(root):
    """
    Postorder traversal is used to delete the tree. Please see the question
    for deletion of tree for details. Postorder traversal is also useful to
    get the postfix expression of an expression tree. Please
    see http://en.wikipedia.org/wiki/Reverse_Polish_notation to for the
    usage of postfix expression.
    """
    if root:
        post_order_traversal(root.left)
        post_order_traversal(root.right)
        print(root.data)


root2 = Node(1)
root2.left = Node(2)
root2.right = Node(3)
root2.left.left = Node(4)
root2.left.right = Node(5)
print("Preorder traversal of binary tree is")
pre_order_traversal(root2)

print("Inorder traversal of binary tree is")
in_order_traversal(root2)

print("Postorder traversal of binary tree is")
post_order_traversal(root2)
