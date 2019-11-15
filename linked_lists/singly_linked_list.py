

class LinkedListNode(object):

    def __init__(self, value):
        self.value = value
        self.next = None


# This method is in-place edit and it'll save space and time.
# But it has side effects and disadvantages.
# So not recommended for real time systems
def delete_node(node_to_delete):
    next_node = node_to_delete.next

    if next_node:
        node_to_delete.value = next_node.value
        node_to_delete.next = next_node.next
    else:
        print("Trying to delete last node... Not possible with this method...")


a = LinkedListNode('A')
b = LinkedListNode('B')
c = LinkedListNode('C')

a.next = b
b.next = c

print(a.value, b.value, c.value)
delete_node(b)
print(a.value, b.value, c.value)
