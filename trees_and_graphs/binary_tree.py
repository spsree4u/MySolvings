
# Binary Tree and Operations


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinaryTree:

    def __init__(self, root):
        self.root = root

    def in_order_non_recursive_travel(self):
        current = self.root
        stack = []

        print('In-order non-recursive travel')
        while True:
            if current is not None:
                stack.append(current)
                current = current.left
            elif stack:
                current = stack.pop()
                print(current.data)
                current = current.right
            else:
                break

    def in_order_recursive_travel(self):
        root = self.root

        def _in_order(node):
            if node:
                _in_order(node.left)
                print(node.data)
                _in_order(node.right)

        print('In-order recursive travel')
        _in_order(root)

    def post_order_recursive_travel(self):
        root = self.root

        def _post_order(node):
            if node:
                _post_order(node.left)
                _post_order(node.right)
                print(node.data)

        print('Post-order recursive travel')
        _post_order(root)

    def pre_order_recursive_travel(self):
        root = self.root

        def _pre_order(node):
            if node:
                print(node.data)
                _pre_order(node.left)
                _pre_order(node.right)

        print('Pre-order recursive travel')
        _pre_order(root)

    def convert_to_mirror_image(self):
        print('Converting the tree to its mirror image')
        root = self.root

        def _mirror(node):
            if node:
                _mirror(node.left)
                _mirror(node.right)

                temp = node.left
                node.left = node.right
                node.right = temp

        _mirror(root)

    def is_symmetric(self):
        def _is_mirror(root_1, root_2):
            if root_1 is None and root_2 is None:
                return True

            if root_1 and root_2:
                if root_1.data == root_2.data:
                    return _is_mirror(root_1.left, root_2.right) \
                           and _is_mirror(root_1.right, root_2.left)

            return False

        return _is_mirror(self.root, self.root)


r = Node(1)
r.left = Node(2)
r.right = Node(3)
r.left.left = Node(4)
r.left.right = Node(5)
bt = BinaryTree(r)
bt.in_order_non_recursive_travel()
bt.in_order_recursive_travel()
bt.post_order_recursive_travel()
bt.pre_order_recursive_travel()
bt.convert_to_mirror_image()
bt.in_order_recursive_travel()
print(bt.is_symmetric())
root = Node(1)
root.left = Node(2)
root.right = Node(2)
root.left.left = Node(3)
root.left.right = Node(4)
root.right.left = Node(4)
root.right.right = Node(3)
bt = BinaryTree(root)
print(bt.is_symmetric())
