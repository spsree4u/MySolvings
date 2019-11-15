

# Find median of BST in O(n) time and O(1) space
class Node:

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def insert(root, value):
    if not root:
        return Node(value)

    if value < root.data:
        root.left = insert(root.left, value)
    elif value > root.data:
        root.right = insert(root.right, value)

    return root


def find_node_count(root):
    count = 0

    if not root:
        return count

    current = root
    while current:
        if not current.left:
            count += 1
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
                count += 1
                current = current.right

    return count


# O(n) time and O(1) space
def find_median(root):
    if not root:
        return
    count = find_node_count(root)
    current_count = 0
    current = root

    while current:
        if not current.left:
            current_count += 1
            if count % 2 != 0 and current_count == (count+1)//2:
                return prev.data
            elif count % 2 == 0 and current_count == (count//2)+1:
                return (prev.data + current.data)//2

            prev = current
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
                prev = temp
                current_count += 1

                if count % 2 != 0 and current_count == (count+1)//2:
                    return current.data
                elif count % 2 == 0 and current_count == (count//2)+1:
                    return (prev.data + current.data)//2

                prev = current
                current = current.right


root = Node(50)
insert(root, 30)
insert(root, 20)
insert(root, 40)
insert(root, 70)
insert(root, 60)
insert(root, 80)
print("Median of BST is ", find_median(root))
