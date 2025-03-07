class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class Linkedlist:
    # head = None
    def __init__(self):
        # self.data = data
        # self.next = None
        self.head = None

    def add(self,e):        
        # while self.head is not None:
        temp = Node(e)
        temp.next = self.head
        self.head = temp
    
    def printlist(self):
        temp = self.head
        while temp:
            print(temp.data)
            temp = temp.next

    def insertAtIndex(self, data, index):
        if (index == 0):
            self.add(data)
            return

        position = 0
        current_node = self.head
        while (current_node != None and position+1 != index):
            position = position+1
            current_node = current_node.next

        if current_node != None:
            new_node = Node(data)
            new_node.next = current_node.next
            current_node.next = new_node
        else:
            print("Index not present")
            
            

obj = Linkedlist()
obj.add(10)
obj.add(20)
obj.add(30)
obj.add(40)
obj.add(50)
obj.printlist()
obj.insertAtIndex(45, 2)
obj.insertAtIndex(35, 0)
obj.insertAtIndex(32, 0)
print(obj) 
obj.printlist()