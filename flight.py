#problem
# 1.passenger details
# 2.source he is starting at source
# 3.destination he is landing dest
# 4. circumstances places stops1, stops2

# table - passenger
# journey table - flight XYZ 
# journey - flight name, source, destination, stop - list
# XYZ Bhu, Bangalore, hyd, cochin

# class sensitive info
# one instance created, any other instance if created singelton class
class Node:
    def __init__(self,data):
        self.data = data #a
        # print("123",type(self.data))
        self.next = None #b
        # print("2",type(self.next))

class func_flight:

    def __init__(self):
        # self.flight_nm = flight_nm
        self.source = None # head c
        print("self.source", self.source)

    def change_destination(self,stop):
        temp = Node(stop)# a
        print("temp", type(temp),temp)
        temp.next = self.source #b = #c
        print("temp.next", type(temp.next), temp.next)
        self.source = temp  #c = #a
        print("self.source2", self.source)
        # a = BHu, b = None, C = Bhu
        # a = Hyd, b = Bhu, C = Hyd
        # a = Bang, b = Hyd, C = Bang

    def reverse(self):
        prev = None
        current = self.source
        while current:
            next = current.next
            current.next = prev
            prev = current
            current = next
        self.source = prev

    def printlist(self):
        temp = self.source
        # print(temp())
        while temp:
            print("print ", temp.data)
            temp = temp.next

obj = func_flight()
obj.change_destination("BHu")
obj.change_destination("HYd")
obj.change_destination("Bang")
# obj.printlist()
obj.reverse()
obj.printlist()












