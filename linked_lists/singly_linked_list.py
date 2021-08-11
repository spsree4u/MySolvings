

class LinkedListNode(object):

    def __init__(self, value):
        self.value = value
        self.next = None


# This method is in-place edit and it'll save space and time.
# But it has side effects and disadvantages.
# So not recommended for real time systems
def delete_node(node_to_delete):
    next_node = node_to_delete.next
    # print(next_node.value, next_node.next)

    if next_node:
        node_to_delete.value = next_node.value
        node_to_delete.next = next_node.next
        del next_node
    else:
        print("Trying to delete last node... Not possible with this method...")


def print_nodes(node):
    while node:
        print(node.value)
        node = node.next


class LinkedList:

    def __init__(self):
        self.head = None

    def insert_at_first(self, data):
        new = LinkedListNode(data)
        new.next = self.head
        self.head = new

    def insert_after_node(self, node_value, data):
        head = self.head
        n = None
        while head:
            if head.value == node_value:
                n = head
                break
            head = head.next

        new = LinkedListNode(data)
        new.next = n.next
        n.next = new

    def append(self, data):
        new = LinkedListNode(data)

        if self.head is None:
            self.head = new
            return

        node = self.head
        while node.next:
            node = node.next

        node.next = new

    def delete_from_first(self):
        self.head = self.head.next

    def delete_node_with_value(self, value):
        head = self.head
        while head.next:
            if head.next.value == value:
                break
            head = head.next
        head.next = head.next.next

    def delete_from_last(self):
        node = self.head
        while node.next.next:
            node = node.next

        node.next = node.next.next

    def is_value_present(self, value):
        head = self.head
        node = None
        while head:
            if head.value == value:
                node = head
                break
            head = head.next
        if node:
            print(True)
        else:
            print(False)

    def print_list(self):
        node = self.head
        while node:
            print(node.value)
            node = node.next


a = LinkedListNode('A')
b = LinkedListNode('B')
c = LinkedListNode('C')

a.next = b
b.next = c

print_nodes(a)
delete_node(b)
print_nodes(a)

ll = LinkedList()
ll.insert_at_first(12)
ll.append(13)
ll.insert_at_first(11)
ll.insert_after_node(12, 15)
ll.append(14)
ll.print_list()
ll.is_value_present(13)
ll.is_value_present(16)
ll.insert_after_node(12, 16)
ll.delete_from_first()
ll.delete_from_last()
ll.delete_node_with_value(15)
ll.print_list()
