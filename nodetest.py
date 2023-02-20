class Node:
    def __init__(self,e):
        self.val = e
        self.next = None

class Linkedlist:
    def __init__(self):
        self.head = None
        self.size = 0

    def push(self,e):
        current = Node(e)
        current.next = self.head
        self.head = current
        self.size+=1

    def pop(self):
        # ele = self.head.val
        self.head = self.head.next

    def reversedt(self):
        prev= None
        current = self.head
        while current:
            next = current.next
            current.next = prev
            prev= current
            current = next
        self.head = prev

    def ppprint(self):
        temp = self.head
        count=0
        while temp:
            print(temp.val, end="-->")
            # print(self.size)
            temp = temp.next
            count+=1
        print("size", count)

d = Linkedlist()
d.head = Node(14)
d.head.next = Node(20)
d.head.next.next = Node(220)
d.push(23)
d.push(231)
d.ppprint()
d.pop()
d.ppprint()
d.reversedt()
d.ppprint()

import glob, os
print(glob.glob(r'C:\Users\*'))
for name in os.walk(r'C:\Users\hp\OneDrive\Documents'):
    print(name)