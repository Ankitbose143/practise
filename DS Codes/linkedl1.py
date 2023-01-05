# merge two sorted list in linkedlist


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
    # Create a dummy node to hold the result
    dummy = ListNode()
    curr = dummy

    # Iterate through both lists
    while l1 and l2:
        # If the value in l1 is smaller, add it to the result
        if l1.val < l2.val:
            curr.next = l1
            l1 = l1.next
        # If the value in l2 is smaller, add it to the result
        else:
            curr.next = l2
            l2 = l2.next
        # Move to the next node in the result
        curr = curr.next

    # Add the remaining elements, if any
    curr.next = l1 or l2

    return dummy.next


# Define the first linked list: 1 -> 3 -> 5
l1 = ListNode(1)
l1.next = ListNode(3)
l1.next.next = ListNode(5)

# Define the second linked list: 2 -> 4 -> 6
l2 = ListNode(2)
l2.next = ListNode(4)
l2.next.next = ListNode(6)

# Merge the two linked lists
result = mergeTwoLists(l1, l2)

# Print the merged linked list
while result:
    print(result.val)
    result = result.next


