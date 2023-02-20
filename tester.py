class Node:
    def __init__(self, e):
        self.val = e
        self.next = None


class Linkedlist:
    def __init__(self):
        self.head = None
        self.size = 0

    def push(self, e):
        newest = Node(e)
        # while newest:
        newest.next = self.head
        self.head = newest

    def AtBegining(self, newdata):
        NewNode = Node(newdata)

        # Update the new nodes next val to existing node
        NewNode.next = self.head
        self.head = NewNode

    def printlist(self):
        temp = self.head
        while temp:
            print(temp.val,end = ",")
            temp = temp.next
k = Linkedlist()
k.head = Node(5)
# print(k.val)
f = Node(15)
k.head.next =f
f.next = Node(18)
# print(list(k))
k.push(23)
# k.AtBegining(34)
k.printlist()
# while




