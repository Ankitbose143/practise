class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverseList(head: ListNode) -> ListNode:
    # Set the current and previous nodes to None
    curr = head
    prev = None

    # Iterate through the linked list
    while curr:
        # Save a reference to the next node
        next = curr.next
        # Update the next pointer to point to the previous node
        curr.next = prev
        # Update the previous and current nodes
        prev = curr
        curr = next

    # Return the reversed linked list
    return prev


# Define the linked list: 1 -> 2 -> 3 -> 4 -> 5
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)

# Reverse the linked list
result = reverseList(head)

# Print the reversed linked list
while result:
    print(result.val)
    result = result.next
