input = [2,2,1,3,4,2,3,4,1,2,3,4]


# print([{t:input.count(t)} for t in set(input)])

# for t in input:
#     d = input.count(t)
#     print(d)

# input = [2,3,4,6,7,9,11]
# output = [5,8,10]
# d = min(input)
# mx = max(input)
# df = d
# # print(d,mx)
# op = []
# for y in range(d, mx):
#     if y not in input:
#         op.append(y)

# print(op)

# Define a class called 'Movie', which has 3 attributes (title, ticket, cost)
# return the values with __str__ function.

class Movie:
    def __init__(self,title, ticket, cost):
        self.title = title
        self.ticket = ticket
        self.cost = cost

    def __str__(self):
        return self.title,self.ticket,self.cost
        # self.cost = cost

A = Movie('xyz',2,500)
print(A.__str__())

