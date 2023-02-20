class Node:
    def __init__(self,e):
        self.val = e
        self.next = None

class lnk:
    def __init__(self):
        self.head = None
        self.size = 0

    def pppush(self, ef):
        new = Node(ef)
        new.next = self.head
        self.head = new
        
    # def push(self,e):
    #     current = Node(e)
    #     current.next = self.head
    #     self.head = current
    #     self.size+=1


    def pprt(self):
        temp = self.head
        while temp:
            print(temp.val, end='-->')
            temp = temp.next
        self.head = temp

    def rever(self):
        prev = None
        current = self.head
        while current is not None:
            next = current.next
            current.next = prev
            prev = current
            current = next
        self.head = prev


k = lnk()
k.head = Node(12)
k.head.next = Node(23)
k.pppush(34)

k.pprt()
k.pppush(34)
k.rever()
# print("hi")
# k.pprt()
print("there")
# d = lnk()
# d.head = Node(14)
# d.head.next = Node(20)
# d.head.next.next = Node(220)
# d.pppush(23)
# d.pppush(231)
# d.pprt()
# # d.pop()
# d.pprt()
# # d.reversedt()
# d.pprt()

class Noder:
    def __init__(self, e):
        self.val = e
        self.left = None
        self.right = None

# class bstree:
    # def __init__(self):

def insrtt(root,key):
    if root is None:
        return Noder(key)
    else:
        if root.val ==key:
            return root
        elif root.val<key:
            root.right = insrtt(root.left, key)
        else:
            root.left =  insrtt(root.left, key)

def inorder(root):
    # inorder = root
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)

ft = Noder(23)
ft = insrtt(ft,45)
ft = insrtt(ft,65)
inorder(ft)