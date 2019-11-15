
# AVL tree implementation


class Node:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVL:
    def insert(self, root, value):
        if not root:
            return Node(value)
        elif value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)

        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        balance = self.get_balance_factor(root)

        if balance > 1 and value < root.left.value:
            return self.right_rotate(root)

        if balance < -1 and value > root.right.value:
            return self.left_rotate(root)

        if balance > 1 and value > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and value < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, value):
        if not root:
            return root
        elif value < root.value:
            root.left = self.delete(root.left, value)
        elif value > root.value:
            root.right = self.delete(root.right, value)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            temp = self.get_min_node(root.right)
            root.value = temp.value
            root.right = self.delete(root.right, temp.value)

        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        balance = self.get_balance_factor(root)

        if balance > 1 and self.get_balance_factor(root.left) >= 0:
            return self.right_rotate(root)

        if balance < -1 and self.get_balance_factor(root.right) <= 0:
            return self.left_rotate(root)

        if balance > 1 and self.get_balance_factor(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and self.get_balance_factor(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, root):
        if not root.right:
            return
        right_node = root.right
        root.right = right_node.left
        right_node.left = root
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))
        right_node.height = 1 + max(self.get_height(right_node.left),
                                    self.get_height(right_node.right))

        return right_node

    def right_rotate(self, root):
        if not root.left:
            return
        left_node = root.left
        root.left = left_node.right
        left_node.right = root
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))
        left_node.height = 1 + max(self.get_height(left_node.left),
                                   self.get_height(left_node.right))

        return left_node

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance_factor(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_min_node(self, root):
        if not root or not root.left:
            return root
        return self.get_min_node(root.left)

    def pre_order_traversal(self, root):
        if root:
            print(root.value)
            self.pre_order_traversal(root.left)
            self.pre_order_traversal(root.right)


myTree = AVL()
root = None

root = myTree.insert(root, 10)
root = myTree.insert(root, 20)
root = myTree.insert(root, 30)
root = myTree.insert(root, 40)
root = myTree.insert(root, 50)
root = myTree.insert(root, 25)
myTree.pre_order_traversal(root)

myTree = AVL()
root = None
nums = [9, 5, 10, 0, 6, 11, -1, 1, 2]
for num in nums:
    root = myTree.insert(root, num)
print("Preorder Traversal after insertion -")
myTree.pre_order_traversal(root)
root = myTree.delete(root, 10)
print("Preorder Traversal after deletion -")
myTree.pre_order_traversal(root)
